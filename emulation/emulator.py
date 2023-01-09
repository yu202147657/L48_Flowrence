from typing import Tuple, Optional

import numpy as np
import pandas
import scipy

from GPy.kern import Matern52, RBF
from GPy.models import GPRegression

from emukit.core import ContinuousParameter, ParameterSpace
from emukit.core.loop.stopping_conditions import StoppingCondition
from emukit.core.loop.user_function import UserFunctionWrapper, UserFunctionResult
from emukit.core.loop.loop_state import LoopState
from emukit.core.initial_designs import RandomDesign
from emukit.bayesian_optimization.loops import BayesianOptimizationLoop
from emukit.bayesian_optimization.acquisitions import ExpectedImprovement
from emukit.sensitivity.monte_carlo import MonteCarloSensitivity
from emukit.model_wrappers.gpy_model_wrappers import GPyModelWrapper

from emulation.simulator import Simulator
from emulation.utils import results_to_df

from simulation_builder.flows import FlowStrategy
from simulation_builder.graph import Graph


class ProgressStoppingCondition(StoppingCondition):
    """
    Stops after N iterations without improvement
    """
    def __init__(self, N: int, max_iterations: int) -> None:

        self.N = N  
        self.max_iterations = max_iterations

        self.best = None
        self.count = 0

    def should_stop(self, loop_state: LoopState) -> bool:

        # first iteration find best of start points
        if self.best is None:
            self.best = np.min(loop_state.Y)
            print(f'start points: {loop_state.Y.flatten()}')
            return False

        # get current output
        current_y = loop_state.Y[-1][0]

        # new best
        if current_y < self.best:
            print(f'iteration {loop_state.iteration}: {current_y} - new best!')
            self.count = 0
            self.best = current_y

        # not new best
        else:
            print(f'iteration {loop_state.iteration}: {current_y}')
            self.count += 1

        # if reached max_iterations return True regardless
        if loop_state.iteration > self.max_iterations:
            print('exceeded max iterations, stopping')
            return True

        # exceeded N
        elif self.count > self.N:
            print(f'stopping due to {self.N} iterations without progress')
            return True

        else:
            return False


class Emulator:
    def __init__(self, graph: Graph, flow_strategy: FlowStrategy, simulation_iterations: int = 1000,
                 fixed_time_period: Optional[float] = None):
        self._g = graph
        self._strategy = FlowStrategy() if flow_strategy is None else flow_strategy
        self._sim_iterations = simulation_iterations
        self._time_period = fixed_time_period

        intersections = len([v for v in self._g if len(self._g[v]) > 2])

        if self._time_period is None:
            self._num_params = intersections * 4
        else:
            self._num_params = intersections * 3

    def bayes_opt(
            self, 
            metric, 
            interval: Tuple[float, float],
            max_iterations: int,
            progress_N: int,
            num_init_points: Optional[int] = 1):

        print(f'\nbayesian optimisation on {metric().name}, interval {interval} with {num_init_points} init points')

        np.random.seed(42)

        sim = Simulator(self._g, metric, self._strategy, self._time_period, self._sim_iterations)

        target_function = UserFunctionWrapper(sim.evaluate, extra_output_names=['raw metric'])

        # parameter space
        parameter_space = ParameterSpace([ContinuousParameter(f"x{i}", *interval) for i in range(self._num_params)])

        # random sample init points
        design = RandomDesign(parameter_space)
        x_init = design.get_samples(num_init_points)

        # evaluate at all init points, and prep for input to BOLoop
        y_init = []
        raw_metric = []
        for i in range(x_init.shape[0]):
            output = target_function(x_init[i:i+1])[0]
            y_init.append(np.expand_dims(output.Y, axis=1))
            raw_metric.append(output.extra_outputs['raw metric'])
        raw_metric = np.stack(raw_metric)
        y_init = np.concatenate(y_init, axis=0)

        # choose kernel
        kernel = Matern52(self._num_params, variance=1.0, ARD=False)

        # evaluate GP on initial points
        gpmodel = GPRegression(x_init, y_init, kernel)
        gpmodel.optimize()

        # no noise in target_function
        gpmodel.Gaussian_noise.constrain_fixed(0.001)

        # wrap for emukit
        model = GPyModelWrapper(gpmodel)

        # create the BO loop
        bo_loop = BayesianOptimizationLoop(
                space=parameter_space,
                model=model,
                acquisition=ExpectedImprovement(model),
                )

        # put the inital raw metrics into the bo_loop results
        for i, row in enumerate(bo_loop.loop_state.results):
            row.extra_outputs['raw metric'] = raw_metric[i]

        stopping_condition = ProgressStoppingCondition(N=progress_N, max_iterations=max_iterations)

        # run optimisation
        bo_loop.run_loop(target_function, stopping_condition)

        # get x and raw metric values from loop state results
        x = [step.X for step in bo_loop.loop_state.results]
        raw_metric = [step.extra_outputs['raw metric'] for step in bo_loop.loop_state.results]

        # convert into arrays
        x = np.stack(x, axis=0)
        raw_metric = np.concatenate(raw_metric)

        return results_to_df(x, self._time_period, raw_metric, metric().name, num_init_points), bo_loop.model

    def sensitivity(self, bo_model, interval: Tuple[float, float], num_mc: int = 10000):

        parameter_list = [ContinuousParameter(f"x{i}", *interval) for i in range(self._num_params)]

        senstivity = MonteCarloSensitivity(model=bo_model, input_domain=ParameterSpace(parameter_list))
        main_effects, total_effects, _ = senstivity.compute_effects(num_monte_carlo_points=num_mc)

        # converting from dict into arrays for results_df function
        main_effects = np.fromiter(main_effects.values(), dtype=float)
        main_effects = np.reshape(main_effects, (1, len(main_effects)))

        total_effects = np.fromiter(total_effects.values(), dtype=float)
        total_effects = np.reshape(total_effects, (1, len(total_effects)))

        return results_to_df(main_effects, self._time_period), \
            results_to_df(total_effects, self._time_period)

    def grid_search_opt(self, metric, interval: Tuple[float, float], steps_per_axis: int):
        """Evaluates target_function on all combinations of parameters taken from the same interval"""

        print(f'\ngrid search on {metric().name}, interval {interval} with {steps_per_axis**self._num_params} grid points')
        np.random.seed(42)

        sim = Simulator(self._g, metric, self._strategy, self._time_period, self._sim_iterations)

        # lambda function for selecting raw metric from outputs
        target_function = lambda x: sim.evaluate(x)[1]

        x_min, f_min, grid, results = scipy.optimize.brute(func=target_function,
                                                           ranges=(interval,) * self._num_params,
                                                           Ns=steps_per_axis,
                                                           full_output=True,
                                                           finish=None)

        results = results.flatten()
        grid = np.moveaxis(grid, 0, self._num_params).reshape(-1, self._num_params)

        return results_to_df(grid, self._time_period, results, metric().name)

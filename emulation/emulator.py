from typing import Tuple, Optional

import numpy as np
import pandas
import scipy
from emukit.core import ContinuousParameter, ParameterSpace
from emukit.core.loop.user_function import UserFunctionWrapper
from emukit.examples.gp_bayesian_optimization.single_objective_bayesian_optimization import GPBayesianOptimization
from emukit.sensitivity.monte_carlo import MonteCarloSensitivity

from emulation.simulator import Simulator
from emulation.utils import results_to_df

from simulation_builder.flows import FlowStrategy
from simulation_builder.graph import Graph


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

    def bayes_opt(self, metric, interval: Tuple[float, float], iterations: int):

        print(f'\nbayesian optimisation on {metric().name}, interval {interval} for {iterations} iterations')

        np.random.seed(42)

        sim = Simulator(self._g, metric, self._strategy, self._time_period, self._sim_iterations)

        target_function = UserFunctionWrapper(sim.evaluate, extra_output_names=['raw metric'])

        x_init = np.random.uniform(*interval, size=(1, self._num_params))

        # you can't pass the UserFunctionResult straight into GPBO
        output_init = target_function(x_init)[0]

        # also the array for y is not the right shape
        y_init = np.expand_dims(output_init.Y, axis=1)

        # parameter space
        parameter_list = [ContinuousParameter(f"x{i}", *interval) for i in range(self._num_params)]

        # create the BO loop
        bo_loop = GPBayesianOptimization(variables_list=parameter_list, X=x_init, Y=y_init, noiseless=True)

        # put the inital raw metric into the bo_loop results
        bo_loop.loop_state.results[0].extra_outputs['raw metric'] = output_init.extra_outputs['raw metric']

        # run optimisation
        bo_loop.run_optimization(target_function, iterations)

        # get x and raw metric values from loop state results
        x = [step.X for step in bo_loop.loop_state.results]
        raw_metric = [step.extra_outputs['raw metric'] for step in bo_loop.loop_state.results]

        # convert into arrays
        x = np.stack(x, axis=0)
        raw_metric = np.concatenate(raw_metric)

        return results_to_df(x, self._time_period, raw_metric, metric().name), bo_loop.model

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

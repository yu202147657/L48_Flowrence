from typing import Tuple, Optional

import numpy as np
import scipy
from emukit.core import ContinuousParameter
from emukit.examples.gp_bayesian_optimization.single_objective_bayesian_optimization import GPBayesianOptimization

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
        np.random.seed(42)

        sim = Simulator(self._g, metric, self._strategy, self._time_period, self._sim_iterations)
        x_init = np.random.uniform(*interval, size=(1, self._num_params))
        y_init = sim.evaluate(x_init)

        parameter_list = [ContinuousParameter(f"p{i}", *interval) for i in range(self._num_params)]

        bo_loop = GPBayesianOptimization(variables_list=parameter_list, X=x_init, Y=y_init, noiseless=True)
        bo_loop.run_optimization(sim.evaluate, iterations)

        return results_to_df(bo_loop.model.X, bo_loop.model.Y, metric().name, self._time_period)

    def grid_search_opt(self, metric, interval: Tuple[float, float], steps_per_axis: int):
        """Evaluates target_function on all combinations of parameters taken from the same interval"""
        np.random.seed(42)

        sim = Simulator(self._g, metric, self._strategy, self._time_period, self._sim_iterations)

        x_min, f_min, grid, results = scipy.optimize.brute(func=sim.evaluate,
                                                           ranges=(interval,) * self._num_params,
                                                           Ns=steps_per_axis,
                                                           full_output=True,
                                                           finish=None)

        results = results.flatten()
        grid = np.moveaxis(grid, 0, self._num_params).reshape(-1, self._num_params)

        return results_to_df(grid, results, metric().name, self._time_period)

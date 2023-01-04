from typing import Tuple

import numpy as np
import pandas

import scipy
from emukit.core import ContinuousParameter
from emukit.examples.gp_bayesian_optimization.single_objective_bayesian_optimization import GPBayesianOptimization


def results_to_df(x, y, simulator):
    """Converts results (as np array) to dataframe"""

    metric_name = simulator.metric().name

    d = {}

    for i in range(x.shape[1]):
        d[f"x{i}"] = np.array(x[:, i])

    d[metric_name] = np.array(y).flatten()

    df = pandas.DataFrame(data=d)

    if simulator.timing_period is not None:
        # infer parameter
        df['x3'] = simulator.timing_period - df.loc[:, ['x0', 'x1', 'x2']].sum(axis=1)

        # reorder cols
        df = df[df.columns[[0, 1, 2, 4, 3]]]

    return df


def grid_search(target_function, num_parameters: int, interval: Tuple[float, float], steps_per_axis=10):
    """Evaluates target_function on all combinations of parameters taken from the same interval"""
    np.random.seed(42)

    # Reshape input to target_function, since scipy.optimize.brute expects function with 1D input
    x_min, f_min, grid, results = scipy.optimize.brute(lambda x: target_function(np.reshape(x, (1, -1))),
                                                       ranges=(interval,) * num_parameters,
                                                       Ns=steps_per_axis,
                                                       full_output=True,
                                                       finish=None)

    results = results.flatten()
    grid = np.moveaxis(grid, 0, num_parameters).reshape(-1, num_parameters)

    return grid, results


def bayesian_optimisation(target_function, num_parameters, interval, num_iterations):
    np.random.seed(42)

    # Emukit requires 2D input
    x_init = np.random.uniform(*interval, size=(1, num_parameters))
    y_init = target_function(x_init)

    parameter_list = [ContinuousParameter(f"p{i}", *interval) for i in range(num_parameters)]

    bo_loop = GPBayesianOptimization(variables_list=parameter_list, X=x_init, Y=y_init, noiseless=True)
    bo_loop.run_optimization(target_function, num_iterations)

    return bo_loop.model.X, bo_loop.model.Y


def random_sampling(target_function, num_parameters, interval, num_iterations):
    """Randomly samples num_iterations points and evaluates target function on them"""

    np.random.seed(42)

    x_list = []
    y_list = []

    for i in range(num_iterations):
        x = np.random.uniform(*interval, size=(1, num_parameters))
        x_list.append(x.tolist()[0])
        y = target_function(x)
        y_list.append(y.tolist()[0])

    return np.array(x_list), np.array(y_list)


# Test functions
def forrester(x):
    return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


def square_sum(x):
    return (x ** 2).sum(keepdims=True)

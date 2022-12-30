import json
import numpy as np
import pandas
import cityflow as cf
import itertools

from emukit.core import ContinuousParameter
from emukit.examples.gp_bayesian_optimization.single_objective_bayesian_optimization import GPBayesianOptimization

from simulation_builder.graph import Graph

from simulation_builder.roadnets import graph_to_roadnet
from simulation_builder.flows import graph_to_flow, FlowStrategy


class Simulator:
    def __init__(self, g: Graph, metric, strategy=None, x_sum_to=-1, steps=1000):

        self.g = g
        self.metric = metric
        self.steps = steps

        # flowstrategy
        if strategy is None:
            self.strategy = FlowStrategy()
        else:
            self.strategy = strategy

        # where p_sum_to != -1 infer a parameter
        self.x_sum_to = x_sum_to

    def evaluate(self, x):
        """
        Parameters
        ----------
        x: An (n x m) numpy array of traffic light timings

        Returns
        -------
        The resulting aggregate metric calculated after N simulation iterations, with traffic light timings X.
        """

        # if we need to infer parameter
        if self.x_sum_to != -1:

            # compute parameter value
            x3 = np.array([[self.x_sum_to - x.sum()]])

            # concat with x
            x = np.concatenate([x, x3], axis=1)

        traffic_light_phases = {(0, 0): x.flatten().tolist()}
        roadnet = graph_to_roadnet(self.g, traffic_light_phases, intersection_width=50, lane_width=8)

        flow = graph_to_flow(self.g, self.strategy)

        with open("cityflow_config/roadnets/auto_roadnet.json", 'w') as f:
            f.write(json.dumps(roadnet, indent=4))

        with open("cityflow_config/flows/auto_flow.json", 'w') as f:
            f.write(json.dumps(flow, indent=4))

        # TODO: where to set, save replay = False?
        eng = cf.Engine("cityflow_config/config.json", thread_num=1)

        metric = self.metric()

        for _ in range(self.steps):
            eng.next_step()
            metric.update(eng)

        aggregate, _ = metric.report()

        return np.array([[10000 - aggregate]])


def results_to_df(x, y, simulator):
    """Converts results (as np array) to dataframe"""

    metric_name = simulator.metric().name

    d = {}

    for i in range(x.shape[1]):
        d[f"x{i}"] = np.array(x[:, i])

    d[metric_name] = np.array(y).flatten()

    df = pandas.DataFrame(data=d)

    if simulator.x_sum_to != -1:
        # infer parameter
        df['x3'] = simulator.x_sum_to - df.loc[:, ['x0', 'x1', 'x2']].sum(axis=1)

        # reorder cols
        df = df[df.columns[[0, 1, 2, 4, 3]]]

    return df


def grid_search(target_function, num_parameters, interval, steps_per_axis=10):
    """Searches all traffic light phase combinations for minimum value of metric"""
    np.random.seed(42)

    # calculating all possible combinations of light phases
    # clunky at the moment (and time-consuming)
    discrete_interval = [np.linspace(*interval, steps_per_axis).tolist()] * num_parameters
    x_list = [list(tup) for tup in itertools.product(*discrete_interval)]
    y_list = []

    for x in x_list:
        y = target_function(np.asarray([x]))
        y_list.append(y.tolist()[0])

    return np.array(x_list), np.array(y_list)


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

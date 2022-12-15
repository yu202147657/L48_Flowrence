import json
import numpy as np

from metrics.useful_metrics import completed_journeys, wait_time
import cityflow as cf

from simulation_builder.flows import graph_to_flow, FlowStrategy, RandomFlowStrategy, CustomEndpointFlowStrategy
from simulation_builder.roadnets import graph_to_roadnet
from simulation_builder.graph import Graph, spiral_graph

from emukit.core import ContinuousParameter
from emukit.core.loop import UserFunctionWrapper
from emukit.core.loop import UserFunctionResult
from emukit.examples.gp_bayesian_optimization.single_objective_bayesian_optimization import GPBayesianOptimization

import matplotlib.pyplot as plt

import pandas

class Simulator:
    def __init__(self, g, metric = completed_journeys, steps = 1000):
        self.g = g
        self.metric = metric
        self.steps = steps

    def evaluate(self, X):

        # setup traffic lights (depends on input from bo_loop)
        traffic_light_phases = {(0, 0):X.flatten().tolist()} # not robust as is

        # generate roadnet
        roadnet = graph_to_roadnet(self.g, traffic_light_phases, intersection_width=50, lane_width=8)

        # default flow
        strategy = FlowStrategy() #strategy = CustomEndpointFlowStrategy({(0, 0): 1.0)

        # graph to flow
        flow = graph_to_flow(g, strategy)

        # write roadnet json
        with open("cityflow_config/roadnets/auto_roadnet.json", 'w') as f:
            f.write(json.dumps(roadnet, indent=4))

        # write flow json
        with open("cityflow_config/flows/auto_flow.json", 'w') as f:
            f.write(json.dumps(flow, indent=4))

        # setup engine
        eng = cf.Engine("cityflow_config/config.json", thread_num=1)
        # where to set, save replay = False?

        for _ in range(self.steps):

            # update engine
            eng.next_step()

            # compute metrics
            metric_val = float(self.metric(eng))

        return np.array([[metric_val]])

def results_to_df(X,Y):
    "converts results (as np array) to dataframe"

    d = {}

    for i in range(X.shape[1]):
        d[f'p{i}'] = np.array(X[:,i])

    d['completed journeys'] = np.array(Y).flatten()

    return(pandas.DataFrame(data = d))

def bayesian_optimisation(target_function, num_parameters, interval, num_iterations):
    "performs bayesian optimsation"

    # randomly initialise start points (we may want to try other init too)
    rng = np.random.default_rng(seed = 42)
    X_init = rng.uniform(*interval, size = (1, num_parameters)) # emukit require dim = 2

    # evaluate target_function at X_init
    Y_init = target_function(X_init)

    # setup emukit parameters
    parameter_list = [ContinuousParameter(f'p{i}', *interval) for i in range(num_parameters)]

    # setup bayesian optimisation loop
    bo_loop = GPBayesianOptimization(variables_list=parameter_list, X=X_init, Y=Y_init, noiseless = True)

    # run optimisation
    bo_loop.run_optimization(target_function, num_iterations)

    print(results_to_df(bo_loop.model.X, bo_loop.model.Y))

def random_sampling(target_function, num_parameters, interval, num_iterations):
    "randomly samples num_iterations points and evaluates target function on them"

    # randomly initialise start points (we may want to try other init too)
    rng = np.random.default_rng(seed = 42)

    X_list = []
    Y_list = []

    for i in range(num_iterations):
        X = rng.uniform(*interval, size = (1, num_parameters)) # emukit require dim = 2
        X_list.append(X.tolist()[0])

        # evaluate target_function at X_init
        Y = target_function(X)
        Y_list.append(Y.tolist()[0])

    print(results_to_df(np.array(X_list),np.array(Y_list)))

def forrester(x):
    return (6*x - 2)**2 * np.sin(12*x - 4)

def square_sum(x):
    return (x ** 2).sum(keepdims = True)

if __name__ == "__main__":

    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    g = Graph([(0, -400), (0, 0), (0, 400), (-400, 0), (400, 0)],
            [((0, -400), (0, 0)), ((0, 400), (0, 0)), ((-400, 0), (0, 0)), ((400, 0), (0, 0))])

    simulator = Simulator(g)

    print()
    print('RANDOM SAMPLING ON CITYFLOW, 20 ITERATIONS')
    random_sampling(simulator.evaluate, num_parameters = 4, interval = (0.1, 4), num_iterations = 20)

    print()
    print('BO ON CITYFLOW, 20 ITERATIONS')
    bayesian_optimisation(simulator.evaluate, num_parameters = 4, interval = (0.1, 4), num_iterations = 20)

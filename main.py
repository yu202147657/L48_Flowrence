import json

import numpy as np
import cityflow as cf

from simulation_builder.flows import CustomEndpointFlowStrategy, graph_to_flow
from simulation_builder.graph import Graph
from emulator.emulation import Simulator, random_sampling, bayesian_optimisation, square_sum, grid_search, results_to_df
from simulation_builder.roadnets import graph_to_roadnet

from metrics.metrics import CompletedJourneysMetric
from metrics.metrics import WaitTimeMetric


if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    g = Graph([(0, -400), (0, 0), (0, 400), (-400, 0), (400, 0)],
              [((0, -400), (0, 0)), ((0, 400), (0, 0)), ((-400, 0), (0, 0)), ((400, 0), (0, 0))])

    strategy = CustomEndpointFlowStrategy(start_flows={(0, -400): 1,
                                                       (0, 400): 240,
                                                       (-400, 0): 240,
                                                       (400, 0): 240},
                                          end_flows={(0, -400): 240,
                                                     (0, 400): 1,
                                                     (-400, 0): 240,
                                                     (400, 0): 240})

    simulator = Simulator(g, CompletedJourneysMetric, strategy=strategy, timing_period=None)

    # Number of parameters depends on whether one is inferred by a fixed total timing period.
    if simulator.timing_period is None:
        num_parameters = 4
    else:
        num_parameters = 3

    # print('\nRANDOM SAMPLING ON CITYFLOW')
    # rs_x, rs_y = random_sampling(simulator.evaluate, num_parameters, interval=(0.1, 20), num_iterations=10)
    #
    # print(results_to_df(rs_x, rs_y, simulator))
    #
    # print('\nBO ON CITYFLOW')
    # bo_x, bo_y = bayesian_optimisation(simulator.evaluate, num_parameters, interval=(0.1, 20), num_iterations=10)
    #
    # print(results_to_df(bo_x, bo_y, simulator))

    print('\nGRID SEARCH ON CITYFLOW')
    gs_x, gs_y = grid_search(simulator.evaluate, num_parameters, interval=(0.1, 20), steps_per_axis=3)

    print(results_to_df(gs_x, gs_y, simulator))

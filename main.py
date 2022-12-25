import json

import numpy as np
import cityflow as cf

from simulation_builder.flows import CustomEndpointFlowStrategy, graph_to_flow
from simulation_builder.graph import Graph
from emulator.emulation import Simulator, random_sampling, bayesian_optimisation, square_sum, grid_search
from simulation_builder.roadnets import graph_to_roadnet

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    g = Graph([(0, -400), (0, 0), (0, 400), (-400, 0), (400, 0)],
              [((0, -400), (0, 0)), ((0, 400), (0, 0)), ((-400, 0), (0, 0)), ((400, 0), (0, 0))])

    strategy = CustomEndpointFlowStrategy(start_flows={(0, -400): 2,
                                                       (0, 400): 30,
                                                       (-400, 0): 30,
                                                       (400, 0): 30},
                                          end_flows={(0, -400): 30,
                                                     (0, 400): 2,
                                                     (-400, 0): 30,
                                                     (400, 0): 30})

    roadnet = graph_to_roadnet(g, intersection_width=50, lane_width=8)
    flow = graph_to_flow(g, strategy)

    with open("cityflow_config/roadnets/auto_roadnet.json", 'w') as f:
        f.write(json.dumps(roadnet, indent=4))

    with open("cityflow_config/flows/auto_flow.json", 'w') as f:
        f.write(json.dumps(flow, indent=4))

    eng = cf.Engine("cityflow_config/config.json", thread_num=1)

    for _ in range(1000):
        eng.next_step()

    simulator = Simulator(g)
    #
    # print()
    # print('BO on squared sum, 20 iterations')
    # bayesian_optimisation(square_sum, num_parameters = 3, interval = (-4, 4), num_iterations = 20)
    #
    # print()
    # print('RANDOM SAMPLING ON CITYFLOW, 20 ITERATIONS')
    # random_sampling(simulator.evaluate, num_parameters = 4, interval = (0.1, 4), num_iterations = 20)
    #
    # print()
    # print('BO ON CITYFLOW, 20 ITERATIONS')
    # bayesian_optimisation(simulator.evaluate, num_parameters = 4, interval = (0.1, 4), num_iterations = 20)

    print('GRID SEARCH ON CITYFLOW')
    grid_search(simulator.evaluate, num_parameters = 4, interval = (0.1, 4))

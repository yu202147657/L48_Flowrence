import numpy as np

from emulation.emulator import Emulator
from simulation_builder.flows import CustomEndpointFlowStrategy
from simulation_builder.graph import Graph

from metrics.metrics import CompletedJourneysMetric


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

    e = Emulator(g, strategy)

    # print(e.bayes_opt(CompletedJourneysMetric, interval=(0.1, 20), iterations=10))
    print(e.grid_search_opt(CompletedJourneysMetric, interval=(0.1, 20), steps_per_axis=5))

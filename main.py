import numpy as np

from emulation.emulator import Emulator
from simulation_builder.flows import CustomEndpointFlowStrategy, FlowStrategy
from simulation_builder.graph import Graph, I_graph

from emulation.metrics import CompletedJourneysMetric
from emulation.metrics import WaitTimeMetric

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    # g = Graph([(0, -400), (0, 0), (0, 400), (-400, 0), (400, 0)],
    #           [((0, -400), (0, 0)), ((0, 400), (0, 0)), ((-400, 0), (0, 0)), ((400, 0), (0, 0))])
    #
    #
    #
    # strategy = CustomEndpointFlowStrategy(start_flows={(0, -400): 1,
    #                                                    (0, 400): 240,
    #                                                    (-400, 0): 240,
    #                                                    (400, 0): 240},
    #                                       end_flows={(0, -400): 240,
    #                                                  (0, 400): 1,
    #                                                  (-400, 0): 240,
    #                                                  (400, 0): 240})

    g = I_graph()
    strategy = FlowStrategy()

    e = Emulator(g, strategy, fixed_time_period=60)

    results, bo_model = e.bayes_opt(CompletedJourneysMetric, interval=(0.1, 20), iterations=5)
    print(results)
    main_effects, total_effects = e.sensitivity(bo_model, interval=(0.1, 20))
    print('\nSENSITIVITY ANALYSIS\n', 'Main Effects\n', main_effects)
    print('Total Effects\n', total_effects, '\n')

    results, bo_model = e.bayes_opt(WaitTimeMetric, interval=(0.1, 20), iterations=5)
    print(results)
    main_effects, total_effects = e.sensitivity(bo_model, interval=(0.1, 20))
    print('\nSENSITIVITY ANALYSIS\n', 'Main Effects\n', main_effects)
    print('Total Effects\n', total_effects, '\n')

    print(e.grid_search_opt(CompletedJourneysMetric, interval=(0.1, 20), steps_per_axis=2))
    print(e.grid_search_opt(WaitTimeMetric, interval=(0.1, 20), steps_per_axis=2))

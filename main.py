import json

import cityflow as cf
from matplotlib import pyplot as plt

from metrics.metrics import CompletedJourneysMetric, WaitTimeMetric
from simulation_builder.flows import graph_to_flow, FlowStrategy, RandomFlowStrategy, CustomEndpointFlowStrategy
from simulation_builder.roadnets import graph_to_roadnet
from simulation_builder.graph import Graph, spiral_graph

if __name__ == "__main__":
    g = Graph([(0, 0), (200, 0), (400, 0), (0, 400), (200, 400), (400, 400)],
              [((0, 0), (200, 0)), ((200, 0), (400, 0)), ((200, 0), (200, 400)), ((0, 400), (200, 400)),
               ((200, 400), (400, 400))])

    roadnet = graph_to_roadnet(g, intersection_width=50, lane_width=8)

    strategy = CustomEndpointFlowStrategy({
        (0, 0): 1.0,
        (400, 0): 8.0,
        (0, 400): 6.0,
        (400, 400): 7.0
    })

    flow = graph_to_flow(g, strategy)

    with open("cityflow_config/roadnets/auto_roadnet.json", 'w') as f:
        f.write(json.dumps(roadnet, indent=4))

    with open("cityflow_config/flows/auto_flow.json", 'w') as f:
        f.write(json.dumps(flow, indent=4))

    m = WaitTimeMetric()
    eng = cf.Engine("cityflow_config/config.json", thread_num=1)
    for _ in range(1000):
        eng.next_step()
        m.update(eng)

    print(m.report())
    plt.plot(m.report().data)
    plt.show()

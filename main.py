import json
import time

import cityflow as cf

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

    eng = cf.Engine("cityflow_config/config.json", thread_num=1)
    t1 = time.time()
    for _ in range(1000):
        eng.next_step()
    print(time.time() - t1)

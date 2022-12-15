import json

import cityflow as cf

from simulation_builder.flows import graph_to_flow
from simulation_builder.roadnets import graph_to_roadnet
from simulation_builder.graph import Graph, spiral_graph

from metrics.useful_metrics import completed_journeys, wait_time

if __name__ == "__main__":
    g = Graph([(0, 0), (200, 0), (400, 0), (0, 400), (200, 400), (400, 400)],
              [((0, 0), (200, 0)), ((200, 0), (400, 0)), ((200, 0), (200, 400)), ((0, 400), (200, 400)),
               ((200, 400), (400, 400))])

    roadnet = graph_to_roadnet(g, intersection_width=50, lane_width=8)
    flow = graph_to_flow(g)

    with open("cityflow_config/roadnets/auto_roadnet.json", 'w') as f:
        f.write(json.dumps(roadnet, indent=4))

    with open("cityflow_config/flows/auto_flow.json", 'w') as f:
        f.write(json.dumps(flow, indent=4))

    eng = cf.Engine("cityflow_config/config.json", thread_num=1)

    steps = 1000
    for _ in range(steps):
        eng.next_step()

        # Completed journeys at each time step
        online_cj = completed_journeys(eng, online = True)
        # Total completed journeys
        total_cj = completed_journeys(eng)

        # Avg wait at each time step
        online_avg_wait = wait_time(eng, online = True)
        # Total avg wait.
        # Doesn't print a value until last time step
        total_avg_wait = wait_time(eng, _, steps)






    #have to get metrics at each step (e.g. vehicle count varies at each step)

import json

from metrics.useful_metrics import completed_journeys, wait_time
import cityflow as cf

from simulation_builder.flows import graph_to_flow, FlowStrategy, RandomFlowStrategy, CustomEndpointFlowStrategy
from simulation_builder.roadnets import graph_to_roadnet
from simulation_builder.graph import Graph, spiral_graph

def evaluate(eng, steps, metric):

    traffic_light_phases = {(0, 0):[1,1,1,1]}

    roadnet = graph_to_roadnet(g, traffic_light_phases, intersection_width=50, lane_width=8)

    #strategy = CustomEndpointFlowStrategy({(0, 0): 1.0)

    strategy = FlowStrategy()

    flow = graph_to_flow(g, strategy)

    with open("cityflow_config/roadnets/auto_roadnet.json", 'w') as f:
        f.write(json.dumps(roadnet, indent=4))

    with open("cityflow_config/flows/auto_flow.json", 'w') as f:
        f.write(json.dumps(flow, indent=4))

    eng = cf.Engine("cityflow_config/config.json", thread_num=1)

    for _ in range(steps):

        eng.next_step()
        # Total completed journeys
        metric_val = metric(eng)

    return metric_val

if __name__ == "__main__":

    g = Graph([(0, -400), (0, 0), (0, 400), (-400, 0), (400, 0)],
            [((0, -400), (0, 0)), ((0, 400), (0, 0)), ((-400, 0), (0, 0)), ((400, 0), (0, 0))])

    steps = 1000
    metric_val = evaluate(g, steps, completed_journeys)

    print(metric_val)

from simulation_builder.graph import Graph
from simulation_builder.flows import CustomEndpointFlowStrategy


def single_intersec_bal() -> tuple:
    return single_intersec_g(), single_intersec_f_bal()


def single_intersec_g() -> Graph:

    vertices = [
            (0, -400), 
            (0, 0),
            (0, 400),
            (-400, 0),
            (400, 0),
            ]

    edges = [
            ((0, -400), (0, 0)),
            ((0, 400), (0, 0)),
            ((-400, 0), (0, 0)),
            ((400, 0), (0, 0)),
            ]

    return Graph(vertices=vertices, edges=edges)


def single_intersec_f_bal() -> CustomEndpointFlowStrategy:

    start_flows={
            (0, -400): 20,
            (0, 400): 20,
            (-400, 0): 20,
            (400, 0): 20,
            }

    end_flows={
            (0, -400): 20,
            (0, 400): 20,
            (-400, 0): 20,
            (400, 0): 20,
            }

    return CustomEndpointFlowStrategy(start_flows=start_flows, end_flows=end_flows)

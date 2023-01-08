from simulation_builder.graph import Graph
from simulation_builder.flows import CustomEndpointFlowStrategy


def single_intersec_bal() -> tuple:
    return single_intersec_g(), single_intersec_f_bal()


def single_intersec_lop() -> tuple:
    return single_intersec_g(), single_intersec_f_lop()


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
            (0, -400): 10,
            (0, 400): 10,
            (-400, 0): 10,
            (400, 0): 10,
            }

    end_flows={
            (0, -400): 10,
            (0, 400): 10,
            (-400, 0): 10,
            (400, 0): 10,
            }

    return CustomEndpointFlowStrategy(start_flows=start_flows, end_flows=end_flows)


def single_intersec_f_lop() -> CustomEndpointFlowStrategy:

    start_flows={
            (0, -400): 1,
            (0, 400): 60,
            (-400, 0): 60,
            (400, 0): 60,
            }

    end_flows={
            (0, -400): 60,
            (0, 400): 1,
            (-400, 0): 60,
            (400, 0): 60,
            }

    return CustomEndpointFlowStrategy(start_flows=start_flows, end_flows=end_flows)


def double_intersec_bal() -> tuple:
    return double_intersec_g(), double_intersec_f_bal()


def double_intersec_g() -> Graph:
    vertices = [
        (-400, 0),
        (0, 0),
        (400, 0),
        (800, 0),
        (0, -400),
        (400, -400),
        (0, 400),
        (400, 400),
        ]


    edges = [
        ((-400, 0), (0, 0)),
        ((0, 0), (400, 0)),
        ((400, 0), (800, 0)),
        ((0, 0), (0, 400)),
        ((400, 0), (400, 400)),
        ((0, 0), (0, -400)),
        ((400, 0), (400, -400))
        ]

    return Graph(vertices=vertices, edges=edges)


def double_intersec_f_bal() -> CustomEndpointFlowStrategy:

    start_flows={
            (0, 400): 20,
            (400, 400): 20,
            (800, 0): 20,
            (0, -400): 20,
            (400, -400): 20,
            (-400, 0): 20,
            }

    end_flows={
            (0, 400): 20,
            (400, 400): 20,
            (800, 0): 20,
            (0, -400): 20,
            (400, -400): 20,
            (-400, 0): 20,
            }

    return CustomEndpointFlowStrategy(start_flows=start_flows, end_flows=end_flows)

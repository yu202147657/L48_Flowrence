from typing import Tuple

from simulation_builder.graph import Graph
from simulation_builder.flows import CustomEndpointFlowStrategy, FlowStrategy, ManualFlowStrategy, UniformFlowStrategy


def single_intersec_bal() -> Tuple[Graph, FlowStrategy]:
    return single_intersec_g(), single_intersec_f_bal()


def single_intersec_lop() -> Tuple[Graph, FlowStrategy]:
    return single_intersec_g(), single_intersec_f_lop()


def single_intersec_lop_2() -> Tuple[Graph, FlowStrategy]:
    strategy = ManualFlowStrategy({
        ((0, -400), (0, 400)): 4,
        ((-400, 0), (400, 0)): 100,
        ((400, 0), (-400, 0)): 100
    })

    return single_intersec_g(), strategy


def single_intersec_bal_2() -> Tuple[Graph, FlowStrategy]:
    strategy = UniformFlowStrategy(interval=10)
    return single_intersec_g(), strategy


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
    start_flows = {
        (0, -400): 8,
        (0, 400): 7,
        (-400, 0): 6,
        (400, 0): 5,
    }

    end_flows = {
        (0, -400): 5,
        (0, 400): 10,
        (-400, 0): 8,
        (400, 0): 7,
    }

    return CustomEndpointFlowStrategy(start_flows=start_flows, end_flows=end_flows)


def single_intersec_f_lop() -> CustomEndpointFlowStrategy:
    start_flows = {
        (0, -400): 4,
        (0, 400): 200,
        (-400, 0): 250,
        (400, 0): 300,
    }

    end_flows = {
        (0, -400): 200,
        (0, 400): 1,
        (-400, 0): 200,
        (400, 0): 200,
    }

    return CustomEndpointFlowStrategy(start_flows=start_flows, end_flows=end_flows)


def double_intersec_bal() -> Tuple[Graph, FlowStrategy]:
    return double_intersec_g(), double_intersec_f_bal()


def double_intersec_lop() -> Tuple[Graph, FlowStrategy]:
    return double_intersec_g(), double_intersec_f_lop()


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
    start_flows = {
        (0, 400): 8,
        (400, 400): 7,
        (800, 0): 5,
        (400, -400): 6,
        (0, -400): 8,
        (-400, 0): 6,
    }

    end_flows = {
        (0, 400): 9,
        (400, 400): 10,
        (800, 0): 7,
        (400, -400): 5,
        (0, -400): 6,
        (-400, 0): 8,
    }

    return CustomEndpointFlowStrategy(start_flows=start_flows, end_flows=end_flows)


def double_intersec_f_lop() -> CustomEndpointFlowStrategy:
    start_flows = {
        (0, 400): 200,
        (400, 400): 250,
        (800, 0): 200,
        (400, -400): 300,
        (0, -400): 200,
        (-400, 0): 1,
    }

    end_flows = {
        (0, 400): 250,
        (400, 400): 250,
        (800, 0): 1,
        (400, -400): 300,
        (0, -400): 200,
        (-400, 0): 200,
    }

    return CustomEndpointFlowStrategy(start_flows=start_flows, end_flows=end_flows)

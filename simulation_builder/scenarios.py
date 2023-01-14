from typing import Tuple

from simulation_builder.graph import Graph
from simulation_builder.flows import CustomEndpointFlowStrategy, FlowStrategy, ManualFlowStrategy, UniformFlowStrategy


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


def double_intersec_bal_2() -> Tuple[Graph, FlowStrategy]:
    strategy = UniformFlowStrategy(interval=20)
    return double_intersec_g(), strategy


def double_intersec_lop_2() -> Tuple[Graph, FlowStrategy]:
    strategy = ManualFlowStrategy({
        ((-400, 0), (800, 0)): 4,
        ((800, 0), (-400, 0)): 4,
        ((0, -400), (0, 400)): 100,
        ((400, 400), (400, -400)): 100,
    })

    return double_intersec_g(), strategy


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

import math
from logging import warning

from numpy import random
from typing import Dict, List, Tuple

from simulation_builder.graph import Graph, Road
import heapq as hq


class Flow:
    def __init__(self, route: List[Tuple[int, int]], interval=2.0):
        # Convert list of points to list of Roads objects
        self.route = [Road(u, v).name() for (u, v) in zip(route[:-1], route[1:])]
        self._interval = interval

    def json(self) -> Dict:
        return {
            "vehicle": {
                "length": 5.0,
                "width": 2.0,
                "maxPosAcc": 2.0,
                "maxNegAcc": 4.5,
                "usualPosAcc": 2.0,
                "usualNegAcc": 4.5,
                "minGap": 2.5,
                "maxSpeed": 12.67,
                "headwayTime": 1.5
            },
            "route": self.route,
            "interval": self._interval,
            "startTime": 0,
            "endTime": -1
        }


class FlowStrategy:
    # Default flow strategy creates one flow per route.
    def gen_flows(self, route: List[Tuple[int, int]]) -> List[Flow]:
        return [Flow(route)]


class RandomFlowStrategy(FlowStrategy):
    def __init__(self, loc=2.0, scale=1.0):
        self._loc = loc
        self._scale = scale

    def gen_flows(self, route: List[Tuple[int, int]]) -> List[Flow]:
        return [Flow(route, interval=max(1.0, random.normal(loc=self._loc, scale=self._scale)))]


class CustomEndpointFlowStrategy(FlowStrategy):
    def __init__(self, endpoint_flows : Dict[Tuple[int, int], float], default=2.0):
        self._endpoint_flows = endpoint_flows
        self._default = default

    def gen_flows(self, route: List[Tuple[int, int]]) -> List[Flow]:
        start = route[0]
        if start in self._endpoint_flows:
            return [Flow(route, interval=self._endpoint_flows[start])]
        else:
            warning(f"Custom flow strategy does not define flow interval for endpoint {start}.")
            return [Flow(route, interval=self._default)]


def graph_to_flow(g: Graph, strategy: FlowStrategy = FlowStrategy()) -> List[Dict]:
    paths = all_pairs_shortest_paths(g)
    flows = []
    for start in paths:
        for end in paths[start]:
            flows += [flow.json() for flow in strategy.gen_flows(paths[start][end])]
    return flows


def all_pairs_shortest_paths(g: Graph) -> Dict:
    """
    Args:
        g: An undirected Graph

    Returns:
        A dictionary of dictionaries of paths, where each one represents the shortest path between an
        endpoint and all other endpoints.
    """

    endpoints = [v for v in g.keys() if len(g[v]) == 1]

    flows = {source: {} for source in endpoints}

    for source in endpoints:
        dist = {source: 0}
        prev = {}

        heap = [(0, source)]
        for v in g.keys():
            if v != source:
                dist[v] = math.inf
            prev[v] = None

        while len(heap) != 0:
            _, u = hq.heappop(heap)
            for v in g[u]:
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    hq.heappush(heap, (alt, v))

        routes = {}
        for v in endpoints:
            if v != source:
                route = [v]
                u = prev[v]
                while u is not None:
                    route.insert(0, u)
                    u = prev[u]
                routes[v] = route
        flows[source] = routes
    return flows

import math
from abc import ABC, abstractmethod
from logging import warning

from numpy import random
from typing import Dict, List, Tuple, Optional

from simulation_builder.graph import Graph, Road
import heapq as hq


class Flow:
    def __init__(self, route: List[Tuple[int, int]], interval=5.0):
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


class FlowStrategy(ABC):
    @abstractmethod
    def gen_flows(self, route: List[Tuple[int, int]]) -> List[Flow]:
        pass


class UniformFlowStrategy(FlowStrategy):
    """
    Creates exactly one flow per route, all initialised with the same interval
    """
    def __init__(self, interval=5.0):
        self._interval = interval

    def gen_flows(self, route: List[Tuple[int, int]]) -> List[Flow]:
        return [Flow(route, interval=self._interval)]


class RandomFlowStrategy(FlowStrategy):
    def __init__(self, loc=2.0, scale=1.0):
        self._loc = loc
        self._scale = scale

    def gen_flows(self, route: List[Tuple[int, int]]) -> List[Flow]:
        return [Flow(route, interval=max(1.0, random.normal(loc=self._loc, scale=self._scale)))]


class CustomEndpointFlowStrategy(FlowStrategy):
    """
    Defines a custom flow strategy, where the interval for a flow is determined by the maximum of the start and end
    flow.

    For example, a flow consisting of nodes [(0, 0), (0, 100), (100, 100)] with start_flows[(0, 0)] = 2 and
    end_flows[(100, 100)] = 4 would be capped at an interval of 4 - since the endpoint (100, 100) only accepts flows
    with a minimum interval of 4.

    If no endpoint interval is specified, then no limit is applied.
    """

    def __init__(self, start_flows: Dict[Tuple[int, int], float], end_flows: Dict[Tuple[int, int], float] = None,
                 default=2.0):
        self._start_flows = start_flows
        self._end_flows = end_flows if end_flows is not None else {}
        self._default = default

    def gen_flows(self, route: List[Tuple[int, int]]) -> List[Flow]:
        start = route[0]
        end = route[-1]
        if start in self._start_flows:
            start_interval = self._start_flows[start]
            if end in self._end_flows:
                end_interval = self._end_flows[end]
                return [Flow(route, interval=max(start_interval, end_interval))]
            # If no end interval specified, no lower bound is applied
            return [Flow(route, interval=start_interval)]
        else:
            warning(f"Custom flow strategy does not define flow interval for source {start}.")
            return [Flow(route, interval=self._default)]


class ManualFlowStrategy(FlowStrategy):
    """
    Takes a dictionary mapping routes defined by start/end pairs to flow intervals. Assumes flows are uniquely defined
    by their start and end points.
    """
    def __init__(self, flows: Dict[Tuple[Tuple, Tuple], float]):
        self._flows = flows

    def gen_flows(self, route: List[Tuple[int, int]]) -> List[Flow]:
        start, end = route[0], route[-1]
        if (start, end) in self._flows:
            return [Flow(route, interval=self._flows[(start, end)])]
        return []


def graph_to_flow(g: Graph, strategy: FlowStrategy = UniformFlowStrategy()) -> List[Dict]:
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

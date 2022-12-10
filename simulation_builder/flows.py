import math
from typing import Dict

from simulation_builder.graph import Graph
import heapq as hq


def all_pairs_shortest_paths(g: Graph) -> Dict[Dict]:
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


import math
from typing import Dict, List

from simulation_builder.graph import Graph, Road
import heapq as hq


# TODO: Discuss customisations - for example, we may define a vehicle type that can be customised.
def graph_to_flow(g: Graph) -> List[Dict]:
	paths = all_pairs_shortest_paths(g)
	flows = []
	for start in paths:
		for end in paths[start]:
			route = [Road(u, v).name() for (u, v) in zip(paths[start][end][:-1], paths[start][end][1:])]
			flow = {
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
				"route": route,
				"interval": 2.0,
				"startTime": 0,
				"endTime": -1
			}
			flows.append(flow)

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

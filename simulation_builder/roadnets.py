from typing import List, Dict

from simulation_builder.geometry import find_path
from simulation_builder.graph import Graph, Road


def graph_to_roadnet(g: Graph, intersection_width=10, lane_width=4, lane_speed=20) -> Dict:
	"""
	Returns:
	 	A dictionary represented the roadnet generated from g.
	"""
	roads = []

	for u in g:
		for v in g[u]:
			road = Road(u, v, lane_width, lane_speed)
			roads.append(road.json())

	intersections = gen_intersections(g, intersection_width, lane_width, lane_speed)

	return {
		"intersections": intersections,
		"roads": roads
	}


def gen_intersections(g: Graph, intersection_width=50, lane_width=4, lane_speed=20) -> List[Dict]:
	intersections = []
	for u in g:
		x, y = u
		intersection = {
			"id": f"intersection_{x}_{y}",
			"point": {"x": x, "y": y},
			"roads": [],
			"roadLinks": [],
			"trafficLight": {
				"roadLinkIndices": [],
				"lightphases": []
			}
		}

		# u is virtual if incoming roads have no choice of direction
		if len(g[u]) <= 2:
			intersection["width"] = 0

			roads = [Road(u, v, lane_width, lane_speed) for v in g[u]] + \
					[Road(v, u, lane_width, lane_speed) for v in g[u]]
			intersection["roads"] = [road.name() for road in roads]
			intersection["roadLinks"] = []
			intersection["trafficLight"]["lightphases"] = [
				{
					"time": 5,
					"availableRoadLinks": []
				},
				{
					"time": 30,
					"availableRoadLinks": []
				},
				{
					"time": 30,
					"availableRoadLinks": []
				},
				{
					"time": 30,
					"availableRoadLinks": []
				},
				{
					"time": 30,
					"availableRoadLinks": []
				},
				{
					"time": 30,
					"availableRoadLinks": []
				},
				{
					"time": 30,
					"availableRoadLinks": []
				},
				{
					"time": 30,
					"availableRoadLinks": []
				},
				{
					"time": 30,
					"availableRoadLinks": []
				}
			]
			intersection["virtual"] = True
		else:
			intersection["width"] = intersection_width
			# Store dictionary of roads indexed by direction
			incoming_roads = {}
			outgoing_roads = {}
			for v in g[u]:
				in_road = Road(v, u)
				out_road = Road(u, v)
				incoming_roads[in_road.direction] = in_road
				outgoing_roads[out_road.direction] = out_road

			intersection["roads"] = [road.name() for road in
									 list(incoming_roads.values()) + (list(outgoing_roads.values()))]

			road_links = []
			# For each incoming road, iterate over all three possible directions. If there is a matching outgoing road,
			# create a road link to it.
			for in_dir, in_road in incoming_roads.items():
				for turn_dir in [-1, 0, 1]:
					if (out_dir := (turn_dir + in_dir) % 4) in outgoing_roads:
						out_road = outgoing_roads[out_dir]
						road_link = {
							"type": "turn_left" if turn_dir == 1 else "turn_right" if turn_dir == -1 else "go_straight",
							"startRoad": in_road.name(),
							"endRoad": out_road.name(),
							"direction": in_dir,
							"laneLinks": []
						}

						for out_lane in range(3):
							# Lane 0 turns left, 1 goes straight and 2 turns right
							in_lane = 1 - turn_dir
							lane_link = {
								"startLaneIndex": in_lane,
								"endLaneIndex": out_lane,
								"points": find_path(in_road, in_lane, out_road, out_lane, 100)
							}
							road_link["laneLinks"].append(lane_link)

						road_links.append(road_link)
			intersection["roadLinks"] = road_links

			road_link_indices = list(range(len(road_links)))

			# Define predicates on road link type to determine valid traffic light phases
			left_road_links = set(filter(lambda i: road_links[i]["type"] == "turn_left", road_link_indices))
			straight_road_links = set(filter(lambda i: road_links[i]["type"] == "go_straight", road_link_indices))
			right_road_links = set(filter(lambda i: road_links[i]["type"] == "turn_right", road_link_indices))
			WE_road_links = set(filter(lambda i: road_links[i]["direction"] == 0, road_link_indices))
			SN_road_links = set(filter(lambda i: road_links[i]["direction"] == 1, road_link_indices))
			EW_road_links = set(filter(lambda i: road_links[i]["direction"] == 2, road_link_indices))
			NS_road_links = set(filter(lambda i: road_links[i]["direction"] == 3, road_link_indices))

			light_phases = [
				right_road_links,
				((EW_road_links | WE_road_links) & straight_road_links) | right_road_links,
				((NS_road_links | SN_road_links) & straight_road_links) | right_road_links,
				((EW_road_links | WE_road_links) & left_road_links) | right_road_links,
				((SN_road_links | NS_road_links) & left_road_links) | right_road_links
			]

			processed_light_phases = [{"time" : 30, "availableRoadLinks": list(phase)}
									  for phase in light_phases if len(phase) > 0]

			intersection["trafficLight"] = {
				"roadLinkIndices": road_link_indices,
				"lightphases": processed_light_phases
			}
			intersection["virtual"] = False
		intersections.append(intersection)

	return intersections

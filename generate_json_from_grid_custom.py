from typing import List, Dict

from geometry import find_path
from graph import Graph, Road


def grid_to_roadnet(g: Graph,
					intersectionWidths, laneWidth=4, laneMaxSpeed=20,
					numLeftLanes=1, numStraightLanes=1, numRightLanes=1, tlPlan=False, midPoints=10):
	roads = []

	for u in g:
		for v in g[u]:
			road = Road(u, v)
			roads.append(road.json())

	intersections = gen_intersections(g)

	return {
		"intersections": intersections,
		"roads": roads
	}


def gen_intersections(g: Graph) -> List[Dict]:
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
				"lightphases": [
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
			}
		}

		# u is virtual if incoming roads have no choice of direction
		if len(g[u]) <= 2:
			intersection["width"] = 0

			roads = [Road(u, v) for v in g[u]] + [Road(v, u) for v in g[u]]
			intersection["roads"] = [road.name() for road in roads]
			intersection["roadLinks"] = []
			intersection["lightphases"] = [
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
			intersection["width"] = 100
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
					if (out_dir := turn_dir + in_dir % 4) in outgoing_roads:
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
			intersection["virtual"] = False
		intersections.append(intersection)

	return intersections

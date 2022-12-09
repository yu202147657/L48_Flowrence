# Problem: Cityflow loops through i, j, and k to create a grid. 
# Need to convert custom graph edges into roadnet structure.
from graph import Graph


# Assume 2-way traffic along each edge
# Current loop requires a full list of edges (e.g. both 1->2 AND 2->1)

def gridToRoadnet(graph: Graph,
				  intersectionWidths, laneWidth=4, laneMaxSpeed=20,
				  numLeftLanes=1, numStraightLanes=1, numRightLanes=1, tlPlan=False, midPoints=10):
	numLanes = numLeftLanes + numStraightLanes + numRightLanes

	roads = []

	for u in graph:
		for v in graph[u]:
			x1, y1 = u
			x2, y2 = v

			if y1 == y2 and x1 < x2:
				# traveling east
				k = 0
			elif y1 == y2 and x1 > x2:
				# traveling west
				k = 2
			elif x1 == x2 and y1 < y2:
				# traveling north
				k = 1
			else:
				# traveling south
				k = 3

			road = {
				"id": f"road_{x1}_{y1}_{k}",
				"direction": k,
				"fromi": x1,
				"fromj": y1,
				"toi": x2,
				"toj": y2,
				"points": [
					{"x": x1, "y": y1},
					{"x": x2, "y": y2}
				],
				"lanes": [
							 {
								 "width": laneWidth,
								 "maxSpeed": laneMaxSpeed
							 }
						 ] * numLanes,
				"startIntersection": f"intersection_{x1}_{y1}",
				"endIntersection": f"intersection_{x2}_{y2}"
			}
			roads.append(road)

	return roads

import math

from CityFlow.tools.generator.generate_json_from_grid import pointToDict3
from simulation_builder.graph import Road

"""
All adapted from CityFlow's generate_json_from_grid.py. 

Used to generate smooth paths between lanes at intersections.
"""


def get_lane_shift(lane_index: int, lane_width: float = 4.0):
	return 2 * (lane_index + 0.5) * lane_width


def get_road_vector(road: Road):
	x1, y1 = road.start
	x2, y2 = road.end
	dx = x2 - x1
	dy = y2 - y1
	length = math.sqrt(dx * dx + dy * dy)
	return dx / length, dy / length


def get_out_point(road: Road, lane_index: int, intersection_width: int) -> (float, float):
	dx, dy = get_road_vector(road)
	lane_shift = get_lane_shift(lane_index, road.lane_width)
	x, y = road.end
	x, y = x - dx * intersection_width, y - dy * intersection_width
	x, y = x + dy * lane_shift, y - dx * lane_shift
	return x, y


def get_in_point(road: Road, lane_index: int, intersection_width: int) -> (float, float):
	dx, dy = get_road_vector(road)
	lane_shift = get_lane_shift(lane_index, road.lane_width)
	x, y = road.start
	x, y = x + dx * intersection_width, y + dy * intersection_width
	x, y = x + dy * lane_shift, y - dx * lane_shift
	return x, y


def find_path(in_road: Road, in_lane: int, out_road: Road, out_lane: int, intersection_width, midPoint=10):
	dxa, dya = get_road_vector(in_road)
	dxb, dyb = get_road_vector(out_road)
	pxa, pya = get_out_point(in_road, in_lane, intersection_width)
	pxb, pyb = get_in_point(out_road, out_lane, intersection_width)

	dxa = dxa * intersection_width
	dya = dya * intersection_width
	dxb = dxb * intersection_width
	dyb = dyb * intersection_width

	path = []
	for i in range(midPoint + 1):
		t = i / midPoint
		t3 = t * t * t
		t2 = t * t

		k1 = 2 * t3 - 3 * t2 + 1
		x1 = k1 * pxa
		y1 = k1 * pya

		k2 = t3 - 2 * t2 + t
		x2 = k2 * dxa
		y2 = k2 * dya

		k3 = -2 * t3 + 3 * t2
		x3 = k3 * pxb
		y3 = k3 * pyb

		k4 = t3 - t2
		x4 = k4 * dxb
		y4 = k4 * dyb

		path.append([x1 + x2 + x3 + x4, y1 + y2 + y3 + y4])

	return list(map(pointToDict3, path))

from typing import List, TypeVar, Tuple, Set, Iterable, Dict

T = TypeVar("T")


# Adjacency-list based Graph data structure
class Graph:
	def __init__(self, vertices: List[T], edges: List[Tuple[T, T]]):
		self.adjacency_list = {v: set() for v in vertices}
		# Graphs are undirected
		for (u, v) in edges:
			self.adjacency_list[u].add(v)
			self.adjacency_list[v].add(u)

	def __str__(self) -> str:
		return str(self.adjacency_list)

	def __getitem__(self, index: T) -> Set[T]:
		return self.adjacency_list[index]

	# Slightly buggy - doesn't take into account edges into index.
	def __setitem__(self, index: T, items: Iterable[T]) -> None:
		if index not in self.adjacency_list.keys():
			self.adjacency_list[index] = set()
		self.adjacency_list[index] = set(items)

	def __iter__(self):
		yield from self.adjacency_list.keys()

	def keys(self) -> Set[T]:
		return set(self.adjacency_list.keys())


# Data structure for storing/computing information about roads
class Road:
	def __init__(self, start: (int, int), end: (int, int)):
		self.start = start
		self.end = end

		x1, y1 = start
		x2, y2 = end

		if x1 == x2 and y1 < y2:
			self.direction = 1
			self._direction_name = "N"
		elif x1 == x2 and y1 > y2:
			self.direction = 3
			self._direction_name = "S"
		elif y1 == y2 and x1 < x2:
			self.direction = 0
			self._direction_name = "E"
		else:
			self.direction = 2
			self._direction_name = "W"

		# TODO: allow customisation of these
		self.lane_width = 4
		self.max_speed = 20
		self.num_lanes = 3

	def name(self) -> str:
		x, y = self.start
		return f"road_{x}_{y}_{self._direction_name}"

	def json(self) -> Dict:
		x1, y1 = self.start
		x2, y2 = self.end
		return {
			"id": self.name(),
			"points": [
				{"x": x1, "y": y1},
				{"x": x2, "y": y2}
			],
			"lanes": [
						 {
							 "width": self.lane_width,
							 "maxSpeed": self.max_speed
						 }
					 ] * self.num_lanes,
			"startIntersection": f"intersection_{x1}_{y1}",
			"endIntersection": f"intersection_{x2}_{y2}"
		}

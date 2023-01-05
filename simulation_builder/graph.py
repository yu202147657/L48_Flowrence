from typing import List, TypeVar, Tuple, Set, Iterable, Dict

T = TypeVar("T")


class Graph:
    """
    Data structure for undirected graph, using adjacency list representation. Will automatically generate reversed
    edges for each edge given to constructor (i.e. specifying Graph([1, 2], (1, 2)) will generate edges (1, 2)
    and (2, 1).
    """

    def __init__(self, vertices: List[T], edges: List[Tuple[T, T]]):
        self.adjacency_list = {v: set() for v in vertices}
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


# TODO: Review whether to put in separate file
class Road:
    """
    Data structure for storing/computing information about roads, such as the start/end points, direction and
    JSON representation.
    """

    def __init__(self, start: (int, int), end: (int, int), lane_width: int = 4, max_speed: int = 20):
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

        self.lane_width = lane_width
        self.max_speed = max_speed
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


def spiral_graph(n: int, width: int = 100) -> Graph:
    cur = (0, 0)
    vertices = [cur]
    for i in range(1, n):
        if i % 2 == 0:
            for j in range(i):
                cur = (cur[0] + width, cur[1])
                vertices.append(cur)
            for j in range(i):
                cur = (cur[0], cur[1] + width)
                vertices.append(cur)
        else:
            for j in range(i):
                cur = (cur[0] - width, cur[1])
                vertices.append(cur)
            for j in range(i):
                cur = (cur[0], cur[1] - width)
                vertices.append(cur)

    edges = [(u, v) for u, v in zip(vertices[:-1], vertices[1:])]
    return Graph(vertices, edges)


def I_graph() -> Graph:
    return Graph(vertices=[(-400, 0), (0, 0), (400, 0), (-400, 400), (0, 400), (400, 400)],
                 edges=[((-400, 0), (0, 0)),
                        ((0, 0), (400, 0)),
                        ((0, 0), (0, 400)),
                        ((-400, 400), (0, 400)),
                        ((0, 400), (400, 400))]
                 )

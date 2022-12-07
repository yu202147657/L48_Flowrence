from typing import List, TypeVar, Tuple, Set, Iterable

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

    # Slightly iffy
    def __setitem__(self, index: T, items: Iterable[T]) -> None:
        if index not in self.adjacency_list.keys():
            self.adjacency_list[index] = set()
        self.adjacency_list[index] = set(items)

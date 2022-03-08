from typing import List, Tuple

class Edge:
    def __init__(self, index: int, point: float, distance: float, pheromones: float = 0, ants: int = 0) -> None:
        self.point = point
        self.index = index
        self.distance = distance
        self.pheromones = pheromones
        self.ants = ants

    def __str__(self) -> str:
        return f'{self.point}'


class Point:
    def __init__(self, label: str, value: float) -> None:
        self.value = value
        self.edges = []
        self.label = label

    def get_edges(self) -> List[Edge]:
        return self.edges

    def get_edge(self, y) -> Edge:
        for c in self.edges:
            if c.point == y:
                return c
        return None

    def __str__(self) -> str:
        res = f'{self.value} -> '
        res += ','.join([str(edge) for edge in self.edges])
        return res


class Graph:
    def __init__(self, points: List[Point]) -> None:
        self.points = points if points != None else []

    def node_by_label(self, label: str) -> Point:
        for v in self.points:
            if v.label == label:
                return v

        return None

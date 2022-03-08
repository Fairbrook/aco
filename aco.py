from turtle import distance
from graph import Edge, Graph
import numpy as np
import random 
import functools

class Ant:
    def __init__(self) -> None:
        self.route = []
        self.position = None
        self.cost = 0
    def __str__(self) -> str:
        return f'Cost:{self.cost:.3f}\tRuta:{[step for step in self.route]}'

class ACO:
    def __init__(self, graph:Graph, alpha:float, beta:float, Q: float, ants: int, disipation: float, initial_point:int, final_point:int, seed = 0) -> None:
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        self.ants = [Ant() for i in range(0, ants)]
        self.ants_len = ants
        self.disipation = disipation
        self.start = initial_point
        self.end = final_point
        self.seed = seed
        random.seed(seed)
        self.new_gen()

    def get_edge(self, x:int, y:int):
        point = self.graph.get_node(x)
        return point.get_edge(y)
    

    def new_gen(self):
        self.ants = [Ant() for i in range(0, self.ants_len)]
        for ant in self.ants:
            ant.position = self.start
        
    def __a(self, edge: Edge):
        # print('a', edge.pheromones ** self.alpha * (1/(0.000001 if edge.distance==0 else edge.distance))**self.beta)
        distance = 0.000001 if edge.distance == 0 else edge.distance
        try:
            # return edge.pheromones ** self.alpha * (1/distance)**self.beta
            # print(distance)
            test= (1/distance)**self.beta
        except RuntimeWarning:
            print(distance)
        return 1

    def generate_solutions(self)->None:
        for ant in self.ants:
            while (ant.position != self.end):
                node = self.graph.points[ant.position]
                edges = node.edges
                #sumatoria
                total_strength = functools.reduce(lambda res, edge: res + self.__a(edge), edges, 0.0)
                # print('total', total_strength)
                for edge in edges:
                    r = random.uniform(0,1)
                    p = self.__a(edge)/total_strength
                    if r < p:
                        ant.position = edge.index
                        ant.route.append((node.label, self.graph.points[edge.index].label))
                        # print(edge.distance)
                        ant.cost += edge.distance
                        break

    def pheromone_update(self):
        for point in self.graph.points:
            for edge in point.edges:
                accumulator = 0
                for ant in self.ants:
                    if (point.label, self.graph.points[edge.index].label) in ant.route:
                        accumulator += self.Q/ant.cost
                edge.pheromones = (1-self.disipation)*edge.pheromones+ accumulator
    
    def __str__(self) -> str:
        res = ''
        return res

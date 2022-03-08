from aco import ACO
from graph import Edge, Graph, Point
import numpy as np

m=10
domain = (-5.0,5.0)
increment = 0.5

# ecuacion general
def F(x, i) -> float:
    return -np.sin(x)*np.power(np.sin((i*x**2)/np.pi), 2*m)

# def get_index(list, label)->int:
#     for item in enumerate(list):
#         if 

def generate_graph()->Graph:
    discrite_values = []
    i = domain[0]
    while i <= domain[1]:
        discrite_values.append(i)
        i+= increment
    nodes = []
    nodes.append(Point('Initial',None))
    initial = nodes[0]
    for v in discrite_values:
        nodes.append(Point(f'{v}_x', v))
    for v in discrite_values:
        nodes.append(Point(f'{v}_y', v))
    nodes.append(Point('Final', None))
    final_index = len(nodes)-1

    for (i,val)in enumerate(discrite_values):
        initial.edges.append(Edge(i+1,val,F(val,1),0.01))

    second_pahse_index = len(discrite_values)
    for i in range(len(discrite_values)):
        current = nodes[i+1]
        for (i,val) in enumerate(discrite_values):
            current.edges.append(Edge(i+second_pahse_index+1,val,F(val,2),0.01))

    for i in range(len(discrite_values)):
        nodes[i+second_pahse_index+1].edges.append(Edge(final_index,None,0,0.01))

    return Graph(nodes)



graph = generate_graph()
aco = ACO(graph=graph, alpha=0.5, beta=0.9, Q= 1, ants=10, disipation= 0.3, initial_point=0, final_point=len(graph.points)-1)
# for point in graph.points:
#     print(point)
# print(F(2,1)+F(-3.0,2))
for i in range(1):
    print("gen", i)
    aco.generate_solutions()
    aco.pheromone_update()
    for ant in aco.ants:
        print(ant)
    aco.new_gen()
from aco import ACO, Ant
import matplotlib.pyplot as plt
from graph import Edge, Graph, Point
import numpy as np

m = 10
domain = (0, np.pi)
increment = 0.1

# Ecuacion general
def F(x, i) -> float:
    return -np.sin(x)*np.power(np.sin((i*x**2)/np.pi), 2*m)

# Ecuación a dos dimensiones
def f(x, y): return F(x, 1)+F(y, 2)

# Punto a buscar
# print(f(2.20,1.57))


def generate_graph() -> Graph:
    # Se vuelve discreto el dominio
    discrite_values = []
    i = domain[0]
    while i <= domain[1]:
        discrite_values.append(i)
        i += increment
    
    # Se comienza la creación de nodos
    nodes = []
    # Nodo inicial
    nodes.append(Point('Initial', None))
    initial = nodes[0]
    # Nodos de la variable x
    for v in discrite_values:
        nodes.append(Point(f'{v}_x', v))

    # Nodos de la variable y
    for v in discrite_values:
        nodes.append(Point(f'{v}_y', v))

    # Nodo final
    nodes.append(Point('Final', None))
    final_index = len(nodes)-1

    # Conexión del nodo inicial con x
    for (i, val) in enumerate(discrite_values):
        distance = F(val, 1)*-1
        distance = 0.0000000001 if distance == 0 else distance
        distance = 1/distance
        initial.edges.append(Edge(i+1, val, distance, 0.01))

    # Conexión de los nodos x con los nodos y
    second_pahse_index = len(discrite_values)
    for i in range(len(discrite_values)):
        current = nodes[i+1]
        for (i, val) in enumerate(discrite_values):
            distance = F(val, 2)*-1
            distance = 0.0000000001 if distance == 0 else distance
            distance = 1/distance
            current.edges.append(
                Edge(i+second_pahse_index+1, val, distance, 0.01))

    # Conexión de los nodos y con el nodo final
    for i in range(len(discrite_values)):
        nodes[i+second_pahse_index +
              1].edges.append(Edge(final_index, None, 0, 0.01))

    return Graph(nodes)

# Inicialización del grafo
graph = generate_graph()
aco = ACO(graph=graph, alpha=0.5, beta=1, Q=0.5, ants=10,
          disipation=0.01, initial_point=0, final_point=len(graph.points)-1, )

# Ciclo principal
bests = []
averages = []
indexes = []
percentage = 0
iteration = 0
while percentage < 0.6:
    iteration += 1
    indexes.append(iteration)
    # Realiza el recorrido para cada hormiga
    aco.generate_solutions()
    # Actualiza el nivel de feromonas
    aco.pheromone_update()

    # Datos para las graficas
    avg = 0
    min = Ant()
    min.cost = 100
    for ant in aco.ants:
        if ant.cost < min.cost:
            min = ant
        avg += ant.cost
    avg /= len(aco.ants)
    bests.append(min)
    averages.append(avg)

    #Chequeo del porcentaje de hormigas dando el mismo valor
    percentage = 0
    for ant in aco.ants:
        if min.cost == ant.cost:
            percentage += 1
    percentage /= len(aco.ants)

    # Nueva generación de hormigas
    aco.new_gen()

best_route = bests[-1].route
best_x = aco.graph.node_by_label(best_route[1][0]).value
best_y = aco.graph.node_by_label(best_route[1][1]).value
best_z = f(best_x, best_y)

# Graficación del proceso
resolution = 150
fig = plt.figure(figsize=plt.figaspect(0.4))
fig.suptitle("Busqueda de solución mediante Colonia de hormigas")
fig.tight_layout(pad=10)

# Evolucion
ax = fig.add_subplot(1, 2, 2)
ax.set_title("Evolución")
ax.plot(indexes, [x.cost for x in bests], label="Mejores")
ax.plot(indexes, averages, label="Promedios")
ax.set_xlabel("Generación")
ax.set_ylabel("Evaluación")
ax.legend()

# Grafica de la función
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.set_title("Función de Michalewicz")
x = np.linspace(0, np.pi, resolution)
y = np.linspace(0, np.pi, resolution)
X, Y = np.meshgrid(x, y)
Z = F(X, 1)+F(Y, 2)
ax.contourf(X, Y, Z, resolution)
print(bests[-1])
ax.scatter(best_x, best_y, best_z, label="Mejor punto encontrado")
ax.legend()

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.85,
                    wspace=0.4,
                    hspace=0.4)
plt.figtext(0.5, 0.01, f"Mejor punto encontrado x={best_x:.3f} y={best_y:.3f} z={best_z:.3f}", ha="center",
            fontsize=10,)
plt.show()

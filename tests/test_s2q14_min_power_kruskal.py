import sys 
sys.path.append("delivery_network")
from graph import Graph, UnionFind, kruskal, graph_from_file, min_power_kruskal


g=Graph([1,2,3,4,5,6])
g.add_edge(1, 2, 3)
g.add_edge(2, 3, 4)
g.add_edge(1, 3, 4)
g.add_edge(1, 6, 7)
g.add_edge(3, 6, 1)
g.add_edge(3, 4, 9)
g.add_edge(3, 5, 9)
g.add_edge(4, 5, 5)

print(min_power_kruskal(g, 1, 5))
#c'est bien cohérent avec l'arbre de poids couvrant donné

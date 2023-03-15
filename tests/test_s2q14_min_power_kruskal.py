import sys 
sys.path.append("delivery_network")
from graph import Graph, UnionFind, graph_from_file, kruskal, min_power_kruskal, orienter_arbre
import time

g=Graph([1,2,3,4,5,6])
g.add_edge(1, 2, 3)
g.add_edge(2, 3, 4)
g.add_edge(1, 3, 4)
g.add_edge(1, 6, 7)
g.add_edge(3, 6, 1)
g.add_edge(3, 4, 9)
g.add_edge(3, 5, 9)
g.add_edge(4, 5, 5)

g1=kruskal(g)
print(g1)
h=orienter_arbre(g1)
min_pwg, traj_g=min_power_kruskal(g1, h, 4, 2)
print(min_pwg, traj_g)

#c'est bien cohérent avec l'arbre de poids couvrant donné


#test sur les grands graphes: 

g=graph_from_file("input/network.2.in")
g2=kruskal(g)
print(g2)
t_dep= time.perf_counter()
h=orienter_arbre(g2)
min_pwg, traj_g=min_power_kruskal(g2, h, 10, 1)
t_fin= time.perf_counter()
t=t_fin-t_dep
print(min_pwg, traj_g, "le temps d'éxecution est ", t , "sec")

#le temps d'éxecution est raisonnable pour la version optimisée de max power kruskal
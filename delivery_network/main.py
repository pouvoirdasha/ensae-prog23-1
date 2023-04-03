from graph import Graph, graph_from_file, get_paths_from_routes, trucks_from_file

"""
data_path = "input/"
#file_name = "network.01.in"

#g = graph_from_file(data_path + file_name)
#print(g)
#graph avec juste le noeud 1, affiche graphe
g=Graph([1])

g.add_edge(2,1,18)

print(g)
print(g.nodes)
"""

x=trucks_from_file(1)
print(x)
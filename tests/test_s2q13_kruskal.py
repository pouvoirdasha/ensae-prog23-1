import sys 
sys.path.append("delivery_network")
from graph import Graph, UnionFind, kruskal, graph_from_file

#on teste sur network.00.in
gnet1 = graph_from_file("input/network.01.in")
print(gnet1)
print(kruskal(gnet1))

#On teste sur les fichiers plus importants (avec le temps d'exceution): 


#le graph est déjà un arbre couvrant car il est d'un seul tenant donc cela renvoie la même chose
#les autres graphes de type network.0x.in sont trop simples, déjà des arbres couvrants donc on va tester sur autre chose

#on crée un graphe nous-même pour tester la fonction
g=Graph([1,2,3,4,5,6])
g.add_edge(1, 2, 3)
g.add_edge(2, 3, 4)
g.add_edge(1, 3, 4)
g.add_edge(1, 6, 7)
g.add_edge(3, 6, 1)
g.add_edge(3, 4, 9)
g.add_edge(3, 5, 9)
g.add_edge(4, 5, 5)


print(g)
print(kruskal(g))
#on voit que l'arbre que la fonction kruskal renvoie est bien un arbre couvrant de poids minimal
import networkx as nx
import matplotlib.pyplot as plt



"ce programme fonctionne, mais sans la bibliothèque graphviz"
"le code tout en bas devrait marcher avec graphviz mais il semble y avoir un problème avec la bibliothèque dot"

class GraphRepresentation:

	def __init__(self):
		self.listofedges = []

	def add_edge2(self, i, j): #fonction qui ajoute les différentes arêtes
		edge = [i, j]
		self.listofedges.append(edge) 

	def display(self):
		G = nx.Graph()
		G.add_edges_from(self.listofedges) #on ajoute toutes les arêtes
		nx.draw_networkx(G)
		plt.show()
#on crée le graphe qui correspond à network.00.in
G = GraphRepresentation()
G.add_edge2(1, 2)
G.add_edge2(1, 6)
G.add_edge2(1, 8)
G.add_edge2(2, 3)
G.add_edge2(3, 4)
G.add_edge2(4, 10)
G.add_edge2(2, 5)
G.add_edge2(5, 7)
G.add_edge2(8, 9)

G.display()

'''
import graphviz
graph = Graph('G', filename='graph', engine='neato')

#on ajoute les noeuds
graph.node('1')
graph.node('2')
graph.node('3')
graph.node('4')
graph.node('5')
graph.node('6')
graph.node('7')
graph.node('8')
graph.node('9')
graph.node('10')
graph.node('11')

#on ajoute les arêtes
graph.edge('1', '2')
graph.edge('2', '3')
graph.edge('1', '6')
graph.edge('3', '4')
graph.edge('4', '10')
graph.edge('2', '5')
graph.edge('5', '7')
graph.edge('1', '8')
graph.edge('8', '9')

#on affiche le graphe
graph.view()

'''
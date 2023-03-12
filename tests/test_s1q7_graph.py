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

#Pour faire des tests, il faut sauvegarder le doc (Ctrl+S), puis après mettre dans le terminal avec python3.exe tests/lenomdutest, on peut utiliser tab pour aller plus vite
import time
from graphviz import Graph as g

class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self): #complexité en O(nb_edges)
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
        


 #Question1   
    def add_edge(self, node1, node2, power_min, dist=1): #complexité en O(1)
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        #si le noeud n'est pas dans le dictionnaire (de la forme graph={0:[(1,3,..), (2,...)]})
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)
        #on rajoute les liens 
        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
        

#Question2

    def connected_components(self): #complexité en O(nb_nodes + nb_edges)
        licomponents = []
        visited_node = {noeud:False for noeud in self.nodes}

        def profound_path(node): #complexité en O(nb_node)
        #on initialise la liste avec uniquement le noeud de départ
            component = [node]
            for neighbor in self.graph[node]:
                neighbor=neighbor[0] #on prend le nom du noeud
                if not visited_node[neighbor]: #s'il n'est pas encore visité
                    visited_node[neighbor]=True #on change pour le mettre en mode visité
                    component += profound_path(neighbor) #récursivement, on ajoute les autres voisins
            return component #on retourne une liste qui donne tous les noeuds accessibles depuis le noeud de départ

        for node in self.nodes:
            if not visited_node[node]:
                licomponents.append(profound_path(node))
        return licomponents
#cout de la fonction exploration : O(1) + nb d'arrêtes + nb de sommets
#la complexité de la méthode est O(n+m)= O(V+E)

#frozenset : comme une liste, mais où l'ordre n'importe pas, et les répétitions non plus, c'est comme un ensemble, et supprime les redondances

    def connected_components_set(self): #comme connected_components
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))


#Question3 
    def get_path_with_power(self, src, dest, power): #complexité en O(nb_edges log(nb_edges))
        #on va faire quelque chose de récursif, on va à chaue fois regarder les voisins des voisins pour trouver le chemin
        #on va s'inspirer fortement de connected_components
        visited_node = {noeud:False for noeud in self.nodes}
        visited_node[src]=True

        def path_research(noeud, path): #on va faire une recherche de chemin en partant du noeud "noeud"
            if noeud == dest: #le chemin qui va directement à destination
                return path
            for neighbor in self.graph[noeud]: #pour chaque voisin on cherche le voisin
                neighbor, power_min, dist = neighbor
                if not visited_node[neighbor] and power_min <= power: #on ne veut pas repasser un même noeud + il faut que la puissance de la voiture soit supérieure à la puissance de la route
                    visited_node[neighbor]=True #le noeud voisin est visité
                    res=path_research(neighbor, path+[neighbor]) #on applique au voisin, avec le chemin de base + le voisin
                    if res is not None:
                        return res
            return None #on a visité tous les voisins mais on n'a rien trouvé
        return path_research(src, [src]) #on part de la source "src"

#Question5 : bonus
    def get_shorter_path_with_power(self, src, dest, power):
        #on va utiliser l'algorithme de Dijkstra avec la condition sur la puissance
        d_dist={noeud : None for noeud in self.nodes}
        d_dist[src]=0 #la distance entre src et src est 0
        d_power={noeud : None for noeud in self.nodes} #on initialise tous les noeuds à +l'infini, ou ici, None pour faciliter
        d_power[src]=0 #la puissance nécessaire pour aller de src à src est 0
        path={noeud:[] for noeud in self.nodes}
        path[src]=[src]
        #on veut créer un sous-graphe tel que la distanc entre un sommet et src soit connue et minimale
        sub_graph=[(0,src)]
        while sub_graph !=[]:
            dist_node, node = min(sub_graph)
            sub_graph.remove((dist_node, node))
            if node == dest: #si ça atteint l'arrivée
                return path[dest]
            for other_node in self.graph[node]:
                other_node, necessary_power, dist_between = other_node
                if necessary_power<= power : 
                    if d_power[other_node] is None or dist_between + d_dist[node]< d_dist[other_node]: #on veut prendre le minimum, on teste s'il y a mieux
                        d_power[other_node]=max(d_power[node], necessary_power)
                        d_dist[other_node]=dist_between + d_dist[node]
                        path[other_node]=path[node]+[other_node]
                        sub_graph.append((d_dist[other_node], other_node))
        return None


#Question6
    #on fait la même fonction en rajoutant P
    def get_path_with_power2(self, src, dest, power):
            visited_node = {noeud:False for noeud in self.nodes}
            visited_node[src]=True

            def path_research(noeud, path, P): #on va faire une recherche de chemin en partant du noeud "noeud"
                if noeud == dest: #le chemin qui va directement à destination
                    return path, P 
                for neighbor in self.graph[noeud]: #pour chaque voisin on cherche le voisin
                    neighbor, power_min, dist = neighbor
                    if not visited_node[neighbor] and power_min <= power: #on ne veut pas repasser un même noeud + il faut que la puissance de la voiture soit supérieure à la puissance de la route
                        visited_node[neighbor]=True #le noeud voisin est visité
                        res=path_research(neighbor, path+[neighbor], P) #on applique au voisin, avec le chemin de base + le voisin
                        if res is not None:
                            return res
                return None #on a visité tous les voisins mais on n'a rien trouvé
            return path_research(src, [src], 0)

    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        #calcule la puissance minimale pour couvrir le trajet
        
        a=0
        b=1
        def dichotomie(a,b):
            while b-a>0.1:
                if self.get_path_with_power2(src, dest, (a+b)/2)!=None:
                    b=(a+b)/2
                else:
                    a = (a+b)/2
                dichotomie(a,b)
            return self.get_path_with_power2(src, dest,b), b
        while self.get_path_with_power2(src, dest,b)==None:
            b=2*b
        return dichotomie(a,b)

#Question7 : bonus
"cf test_s1q7_graph"

#Question 8 : implémenter d'autres tests 

"les tests sont complétés"

#Question 9 : bonus 













#Question1 et Question4
def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
        return g
# ou sinon, ce code : 
#Question4
def graph_from_file_dist(filename):
    #n=nombre de noeud
    #m=nombre d'arêtes
    with open(filename, 'r') as file:
        ligne1=file.readline().split()
        n=int(ligne1[0])
        m=int(ligne1[1])
        nodes = [i for i in range(1, n+1)]
        G=Graph(nodes)
        for i in range(m):
            lignei=file.readline().split()
            node1=int(lignei[0])
            node2=int(lignei[1])
            power_min=int(lignei[2])
            if len(lignei)==3:
                G.add_edge(node1, node2, power_min)
            else:
                dist=int(lignei[3])
                G.add_edge(node1, node2, power_min, dist)       
    return G





#Séance2

#Question10
#on doit tester le temps sur min_power
#ce n'est pas assez optimal, donc ça motive le reste de la séance
    
'''voir test_s2q10_time.py pour l'éxecution'''
def estimated_time(nb_file): #entrer le numéro du fichier
    assert nb_file in [i for i in range(1,11)] #on vérifie qu'il est bien entre 1 et 10
    name_route_file="input/routes."+ str(nb_file) + ".in"
    f=open(name_route_file, 'r')
    ligne1 = f.readline().split()
    n = int(ligne1[0])
    sum = 0
    p1="input/network."
    p2=".in"
    for i in range(4): #on estime le temps avec les 10 premières lignes du fichier
        ligne = f.readline().split()
        node1 = int(ligne[0])
        node2 = int(ligne[1])
        t_dep = time.perf_counter()
        name_network_file=p1+str(nb_file)+p2
        res = graph_from_file(name_network_file).min_power(node1, node2)
        t_fin = time.perf_counter()
        sum = sum + t_fin - t_dep
    return (n * sum/4)

#Question11 : bonus

#Question12

#on trie les arêtes par poids croissant
#dans l'ordre on ajoute à l'arbre les arêtes si elle ne fait pas de cycle avec les arêtes déjà ajoutées
#poids de l'arbre = somme des arêtes
#si même poids d'arêtes, on refait avec un ordre différent mais revient au même
class UnionFind:
    def __init__(self, n):
        """
        Initialise la structure de données Union-Find avec n éléments,
        chacun étant initialement dans sa propre partition.
        """
        self.parent = [k for k in range(n+1)] #tableau qui contient le parent de chaque élément, initialisé à lui-même
        self.rank = [0]*n #stocke la hauteur (=le rang) de chaque arbre

    def find(self, x): #trouver l'ensemble auquel x appartient en remontant la chaine de parents
        if self.parent[x] != x: #si x n'est pas la racine, on continue 
            self.parent[x] = self.find(self.parent[x]) #récursivité + on comprime pour être plus efficace
        return self.parent[x]

    def union(self, x, y): #relier les arbres
        root_x, root_y = self.find(x), self.find(y) #on trouve les racines de x et y
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y #on relie l'arbre de hauteur inférieur à la racine de l'arbre de rang supérieur 
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x #si même rang, on les relie + on augmete le rang 
            self.rank[root_x] += 1
    
def kruskal(g):
    edges=[]
    sorted_edges=[]
    for node in g.graph:
        for connected_node, power, dist in g.graph[node]:
            edges.append((power,node,connected_node))
    sorted_edges=sorted(edges, key=lambda l: l[0]) #on trie les arêtes par poids croissant
    uf = UnionFind(g.nb_nodes + max(g.nodes)) #on crée une structure d'unionfind, on rajoute le dernier sinon on est out of range dans la suite de la fonction
    g_mst = Graph() #on va créer l'arbre couvrant de poids minimal
    for power, node1, node2 in sorted_edges:
        if uf.find(node1)!= uf.find(node2): #on vérifie si ça ne crée pas de cycle 
            g_mst.add_edge(node1, node2, power) #on l'ajoute à l'arbre couvrant 
            uf.union(node1, node2) #on les lie 
    return g_mst

#Question 13
'''voir test_s2q13_kruskal pour les tests'''


#Question14
#on observe que la fonction minpower ne fonctionne pas sur les grands fichiers avec kruskal, 
#On cherche donc une autre solution
#Pour avoir la fonction qui calcule la puissance minimale d'un camion pour un trajet t donné et le chemin,
#On peut implementer une fonction similaire à get path with power mais sur la fonction kruskal 
#D'abord on va orienter l'arbre vers le premier node, ce qui permet d'avoir le plus court chemin en remontant vers les ancetres 
def oriented_tree(g,root=1): #complexité en O(V+E)
    parent = [k for k in range(g.nb_nodes+1)] #tableau qui contient le parent de chaque élément, initialisé à lui-même
    rank = [0]*(g.nb_nodes+1)
    power = [0]*(g.nb_nodes+1)
    #on réalise un parcours en profondeur (DFS) de l'arbre, en initialisant à 1 la racine de l'arbre 
    def DFS(node, father): 
        for child, power_min, dist in g.graph[node]:
            if child!=father: #ici, le node enfant = le neoud de rang +1 de notre noeud et le noeud father est le noeud de rang-1 de notre noeud
                parent[child]=node  #on oriente l'enfant vers son parent 
                rank[child]=rank[node]+1 #le rang de l'enfant est supérieur au rang du noeud 
                power[child]=power_min #on récupere également la puissance pour notre programme 
                DFS(child, node) #on définit cette fonction par récursivité 
    
    DFS(1,1) #DFS est  une fonction récursive. On appelle DFS sur 1,1 puisque 1 est son propre parent, ce qui nous permet de la lancer sur tout l'arbre
    return parent, rank, power 
#recherche du trajet et de la puissance minimale avec la source et la destination = deux noeuds qu'on souhaite relier 
#Si le rang des deux noeuds n'est pas le meme par rapport au premier noeud
#alors on remonte l'arbre de parenté
def min_power_kruskal(g, dfs, src, dest): 
    parent=dfs[0]
    rank=dfs[1]
    power=dfs[2]
    min_pkr=0
    traj_src=[]
    traj_d=[]
    while rank[src] < rank[dest]:
        min_pkr=max(power[dest], min_pkr) #a chaque fois qu'on remonte l'arbre, on verifie qu'on a bien la puissance minimal (max parmi les arretes)
        traj_d+=[dest] #Pour faire le trajet on ajoute le noeud à chaque iteration à la liste de trajet
        dest=parent[dest] #on remonte l'arbre 
    while rank[dest] < rank[src]:  #de meme mais cette fois si le rang de la source est supérieur au rag de la destination
        min_pkr=max(power[src], min_pkr)
        traj_src+=[src]
        src=parent[src]
    while dest !=src: #une fois au meme rang, on travaille sur les deux noeuds (source et destination)
        #On remonte l'arbre tant que les deux noeuds ne sont pas égaux (auquel cas on a trouvé notre chemin)
        min_pkr=max(power[src], power[dest], min_pkr)
        traj_src+=[src]
        traj_d+=[dest]
        src=parent[src]
        dest=parent[dest]
    traj_f=traj_src+[src]+traj_d[::-1] #on ajout eles trajets depuis la source et depuis la destination ensemble 
    return min_pkr, traj_f
    

#Question15
#on estime le temps mais avec l'arbre couvrant de poids minimal

def estimated_time_kruskal(nb_file): #entrer le numéro du fichier
    assert nb_file in [i for i in range(1,11)] #on vérifie qu'il est bien entre 1 et 10
    name_route_file="input/routes."+ str(nb_file) + ".in"
    f=open(name_route_file, 'r')
    ligne1 = f.readline().split()
    n = int(ligne1[0])
    sum = 0
    p1="input/network."
    p2=".in"
    name_network_file=p1+str(nb_file)+p2
    g=graph_from_file(name_network_file)
    g_kruskal=kruskal(g)
    ot=oriented_tree(g_kruskal)
    for i in range(n): #on estime le temps avec les 5 premières lignes du fichier
        ligne = f.readline().split()
        node1 = int(ligne[0])
        node2 = int(ligne[1])
        t_dep = time.perf_counter()
        res = min_power_kruskal(g_kruskal, ot, node1, node2)
        t_fin = time.perf_counter()
        sum = sum + t_fin - t_dep
    return sum



"""def routes_from_file(nb_file_routes): 
    filename = "input/routes." + str(nb_file_routes) + ".in"
    f = open(filename, 'r')
    n =int(f.readline().rstrip())
    for i in range(n):
        line=f.readline.split()

"""









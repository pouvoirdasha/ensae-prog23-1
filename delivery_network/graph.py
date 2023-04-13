# Pour faire des tests, il faut sauvegarder le doc (Ctrl+S), puis après mettre dans le terminal avec python3.exe tests/lenomdutest, on peut utiliser tab pour aller plus vite
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
    

    def __str__(self): # Complexité en O(nb_edges)
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
        


 ### Question1   
    def add_edge(self, node1, node2, power_min, dist=1): # Complexité en O(1)
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
        # Si le noeud n'est pas dans le dictionnaire (de la forme graph={0:[(1,3,..), (2,...)]})
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)
        # On rajoute les liens 
        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
        

### Question2

    def connected_components(self): # Complexité en O(nb_nodes + nb_edges) = O(V+E)
        licomponents = []
        visited_node = {noeud:False for noeud in self.nodes}

        def profound_path(node): # Complexité en O(nb_node)
        # On initialise la liste avec uniquement le noeud de départ
            component = [node]
            for neighbor in self.graph[node]:
                neighbor = neighbor[0] # On prend le nom du noeud
                if not visited_node[neighbor]: # S'il n'est pas encore visité
                    visited_node[neighbor] = True # On change pour le mettre en mode visité
                    component += profound_path(neighbor) # Récursivement, on ajoute les autres voisins
            return component # On retourne une liste qui donne tous les noeuds accessibles depuis le noeud de départ

        for node in self.nodes:
            if not visited_node[node]:
                licomponents.append(profound_path(node))
        return licomponents
        # Cout de la fonction exploration : O(1) + nb d'arrêtes + nb de sommets
        # La complexité de la méthode est O(n+m)= O(V+E)
        # Frozenset : comme une liste, mais où l'ordre n'importe pas, et les répétitions non plus, c'est comme un ensemble, et supprime les redondances

    def connected_components_set(self): # Complexité en O(V+E) comme connected_components
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))


###Question3 
    def get_path_with_power(self, src, dest, power): # Complexité en O(V+E)
        # On va faire quelque chose de récursif, on va à chaque fois regarder les voisins des voisins pour trouver le chemin
        # On va s'inspirer fortement de connected_components
        visited_node = {noeud:False for noeud in self.nodes}
        visited_node[src] = True

        def path_research(noeud, path): # On va faire une recherche de chemin en partant du noeud "noeud"
            if noeud == dest: # Le chemin qui va directement à destination
                return path
            for neighbor in self.graph[noeud]: # Pour chaque voisin on cherche le voisin
                neighbor, power_min, dist = neighbor
                if not visited_node[neighbor] and power_min <= power: # On ne veut pas repasser un même noeud + il faut que la puissance de la voiture soit supérieure à la puissance de la route
                    visited_node[neighbor] = True # Le noeud voisin est visité
                    res = path_research(neighbor, path+[neighbor]) # On applique au voisin, avec le chemin de base + le voisin
                    if res is not None:
                        return res
            return None # On a visité tous les voisins mais on n'a rien trouvé
        return path_research(src, [src]) # On part de la source "src"

###Question5 : bonus
    def get_shorter_path_with_power(self, src, dest, power): #  Complexité en O((V+E)log(V))
        # On va utiliser l'algorithme de Dijkstra avec la condition sur la puissance
        d_dist = {noeud : None for noeud in self.nodes}
        d_dist[src] = 0 # La distance entre src et src est 0
        d_power = {noeud : None for noeud in self.nodes} # On initialise tous les noeuds à +l'infini, ou ici, None pour faciliter
        d_power[src] = 0 # La puissance nécessaire pour aller de src à src est 0
        path = {noeud:[] for noeud in self.nodes}
        path[src] = [src]
        # On veut créer un sous-graphe tel que la distance entre un sommet et src soit connue et minimale
        sub_graph = [(0,src)]
        while sub_graph != []:
            dist_node, node = min(sub_graph)
            sub_graph.remove((dist_node, node))
            if node == dest: # Si ça atteint l'arrivée
                return path[dest]
            for other_node in self.graph[node]:
                other_node, necessary_power, dist_between = other_node
                if necessary_power <= power : 
                    if d_power[other_node] is None or dist_between + d_dist[node] < d_dist[other_node]: # On veut prendre le minimum, on teste s'il y a mieux
                        d_power[other_node] = max(d_power[node], necessary_power)
                        d_dist[other_node] = dist_between + d_dist[node]
                        path[other_node] = path[node]+[other_node]
                        sub_graph.append((d_dist[other_node], other_node))
        return None


###Question6
    # On fait presque la même fonction
    def get_path_with_power2(self, src, dest, power):
            visited_node = {noeud:False for noeud in self.nodes}
            visited_node[src] = True

            def path_research(noeud, path, P): # On va faire une recherche de chemin en partant du noeud "noeud"
                if noeud == dest: # Le chemin qui va directement à destination
                    return path, P 
                for neighbor in self.graph[noeud]: # Pour chaque voisin on cherche le voisin
                    neighbor, power_min, dist = neighbor
                    if not visited_node[neighbor] and power_min <= power: # On ne veut pas repasser un même noeud + il faut que la puissance de la voiture soit supérieure à la puissance de la route
                        visited_node[neighbor] = True # Le noeud voisin est visité
                        res=path_research(neighbor, path+[neighbor], P) # On applique au voisin, avec le chemin de base + le voisin
                        if res is not None:
                            return res
                return None # On a visité tous les voisins mais on n'a rien trouvé
            return path_research(src, [src], 0)

    def min_power(self, src, dest): # Complexité en O(E(V+E)log(V))
        """
        Should return path, min_power. 
        """
        # Calcule la puissance minimale pour couvrir le trajet
        
        a = 0
        b = 1
        def dichotomie(a,b): # On fait une dichotomie 
            while b-a > 0.2:
                if self.get_path_with_power2(src, dest, (a+b)/2)!= None:
                    b = (a+b)/2
                else:
                    a = (a+b)/2
                dichotomie(a,b)
            return self.get_path_with_power2(src, dest,b), b
        while self.get_path_with_power2(src, dest,b) == None: # Si aucun trajet n'est possible, on augmente b pour majorer la puissance et appliquer la dichotomie car la puissance ne sera pas de 1, certainement
            b=2*b
        return dichotomie(a,b)

###Question7 : bonus
"cf test_s1q7_graph"

###Question 8 : implémenter d'autres tests 

"les tests sont complétés"

###Question 9 : bonus 


###Question1 et Question4
def graph_from_file(filename): # Complexité en O(E)
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
                g.add_edge(node1, node2, power_min) # Will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
        return g
# Ou sinon, ce code : 
###Question4
def graph_from_file_dist(filename):
    # n=nombre de noeud
    # m=nombre d'arêtes
    with open(filename, 'r') as file:
        ligne1 = file.readline().split()
        n = int(ligne1[0])
        m = int(ligne1[1])
        nodes = [i for i in range(1, n+1)]
        G = Graph(nodes)
        for i in range(m):
            lignei = file.readline().split()
            node1 = int(lignei[0])
            node2 = int(lignei[1])
            power_min = int(lignei[2])
            if len(lignei) == 3:
                G.add_edge(node1, node2, power_min)
            else:
                dist = int(lignei[3])
                G.add_edge(node1, node2, power_min, dist)       
    return G


###Séance2

###Question10
# On doit tester le temps sur min_power
# Ce n'est pas assez optimal, donc ça motive le reste de la séance
    
'''voir test_s2q10_time.py pour l'éxecution'''
def estimated_time(nb_file): # Entrer le numéro du fichier
    assert nb_file in [i for i in range(1,11)] # On vérifie qu'il est bien entre 1 et 10
    name_route_file = "input/routes." + str(nb_file) + ".in"
    f = open(name_route_file, 'r')
    ligne1 = f.readline().split()
    n = int(ligne1[0])
    sum = 0
    p1 = "input/network."
    p2 = ".in"
    for i in range(4): # On estime le temps avec les 10 premières lignes du fichier
        ligne = f.readline().split()
        node1 = int(ligne[0])
        node2 = int(ligne[1])
        t_dep = time.perf_counter()
        name_network_file = p1 + str(nb_file) + p2
        res = graph_from_file(name_network_file).min_power(node1, node2)
        t_fin = time.perf_counter()
        sum = sum + t_fin - t_dep
    return (n * sum/4)

###Question11 : bonus

###Question12

# On trie les arêtes par poids croissant
# Dans l'ordre on ajoute à l'arbre les arêtes si elle ne fait pas de cycle avec les arêtes déjà ajoutées
# Poids de l'arbre = somme des arêtes
# Si même poids d'arêtes, on refait avec un ordre différent mais revient au même
class UnionFind:
    def __init__(self, n):
        """
        Initialise la structure de données Union-Find avec n éléments,
        chacun étant initialement dans sa propre partition.
        """
        self.parent = [k for k in range(n+1)] # Tableau qui contient le parent de chaque élément, initialisé à lui-même
        self.rank = [0] * n # Stocke la hauteur (=le rang) de chaque arbre

    def find(self, x): # Complexité en O(log(n))
        if self.parent[x] != x: # Si x n'est pas la racine, on continue 
            self.parent[x] = self.find(self.parent[x]) # Récursivité + on comprime pour être plus efficace
        return self.parent[x]

    def union(self, x, y): # Complexité en O(1)
        root_x, root_y = self.find(x), self.find(y) # On trouve les racines de x et y
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y # On relie l'arbre de hauteur inférieur à la racine de l'arbre de rang supérieur 
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x # Si même rang, on les relie + on augmete le rang 
            self.rank[root_x] += 1
    
def kruskal(g): # Complexité de O(Elog(E))
    edges = []
    sorted_edges = []
    for node in g.graph:
        for connected_node, power, dist in g.graph[node]:
            edges.append((power,node,connected_node))
    sorted_edges = sorted(edges, key=lambda l: l[0]) # On trie les arêtes par poids croissant
    uf = UnionFind(g.nb_nodes + max(g.nodes)) # On crée une structure d'unionfind, on rajoute le dernier sinon on est out of range dans la suite de la fonction
    g_mst = Graph() # On va créer l'arbre couvrant de poids minimal
    for power, node1, node2 in sorted_edges:
        if uf.find(node1) != uf.find(node2): # On vérifie si ça ne crée pas de cycle 
            g_mst.add_edge(node1, node2, power) # On l'ajoute à l'arbre couvrant 
            uf.union(node1, node2) # On les lie 
    return g_mst

###Question 13
'''voir test_s2q13_kruskal pour les tests'''


###Question14
def oriented_tree(g,root=1): # Complexité en O(V+E)
    parent = [k for k in range(g.nb_nodes+1)] # Tableau qui contient le parent de chaque élément, initialisé à lui-même
    rank = [0] * (g.nb_nodes+1)
    power = [0] * (g.nb_nodes+1)
    # On réalise un parcours en profondeur (DFS) de l'arbre, en initialisant à 1 la racine de l'arbre 
    def DFS(node, father): 
        for child, power_min, dist in g.graph[node]:
            if child!=father: # Ici, le node enfant = le neoud de rang +1 de notre noeud et le noeud father est le noeud de rang-1 de notre noeud
                parent[child]=node  # On oriente l'enfant vers son parent 
                rank[child]=rank[node]+1 # Le rang de l'enfant est supérieur au rang du noeud 
                power[child]=power_min # On récupere également la puissance pour notre programme 
                DFS(child, node) # On définit cette fonction par récursivité 
    
    DFS(1,1) # DFS est  une fonction récursive. On appelle DFS sur 1,1 puisque 1 est son propre parent, ce qui nous permet de la lancer sur tout l'arbre
    return parent, rank, power 
# Recherche du trajet et de la puissance minimale avec la source et la destination = deux noeuds qu'on souhaite relier 
# Si le rang des deux noeuds n'est pas le meme par rapport au premier noeud
# Alors on remonte l'arbre de parenté

def min_power_kruskal(g, dfs, src, dest): # Complexité en O(Elog(E))
    parent = dfs[0]
    rank = dfs[1]
    power = dfs[2]
    min_pkr = 0
    traj_src = []
    traj_d = []
    while rank[src] < rank[dest]:
        min_pkr = max(power[dest], min_pkr) # A chaque fois qu'on remonte l'arbre, on vérifie qu'on a bien la puissance minimale (max parmi les arêtes)
        traj_d += [dest] # Pour faire le trajet on ajoute le noeud à chaque itération à la liste de trajet
        dest = parent[dest] # On remonte l'arbre 
    while rank[dest] < rank[src]:  # De même mais cette fois si le rang de la source est supérieur au rang de la destination
        min_pkr = max(power[src], min_pkr)
        traj_src += [src]
        src = parent[src]
    while dest !=src: # Une fois au même rang, on travaille sur les deux noeuds (source et destination)
        # On remonte l'arbre tant que les deux noeuds ne sont pas égaux (auquel cas on a trouvé notre chemin)
        min_pkr = max(power[src], power[dest], min_pkr)
        traj_src += [src]
        traj_d += [dest]
        src = parent[src]
        dest = parent[dest]
    traj_f = traj_src + [src] + traj_d[::-1] # On ajoute les trajets depuis la source et depuis la destination ensemble 
    return min_pkr, traj_f

'''voir test_s2q13_kruskal pour les tests'''

###Question15
# On estime le temps mais avec l'arbre couvrant de poids minimal
# La complexité est O(EVlog(V)log(E))
def estimated_time_kruskal(nb_file): # Entrer le numéro du fichier
    assert nb_file in [i for i in range(1,11)] # On vérifie qu'il est bien entre 1 et 10
    name_route_file = "input/routes." + str(nb_file) + ".in"
    f = open(name_route_file, 'r')
    ligne1 = f.readline().split()
    n = int(ligne1[0])
    sum = 0
    p1 = "input/network."
    p2 = ".in"
    name_network_file = p1 + str(nb_file) + p2
    g = graph_from_file(name_network_file)
    g_kruskal = kruskal(g)
    ot = oriented_tree(g_kruskal)
    for i in range(n): #on estime le temps avec les 5 premières lignes du fichier
        ligne = f.readline().split()
        node1 = int(ligne[0])
        node2 = int(ligne[1])
        t_dep = time.perf_counter()
        res = min_power_kruskal(g_kruskal, ot, node1, node2)
        t_fin = time.perf_counter()
        sum = sum + t_fin - t_dep
    return sum

###Séance 4
###Question 18
def routes_from_file(nb_file_routes): 
    filename = "input/routes." + str(nb_file_routes) + ".in"
    f = open(filename, 'r')
    n = int(f.readline().rstrip())
    p1="input/network."
    p2=".in"
    name_network_file=p1+str(nb_file_routes)+p2
    g=graph_from_file(name_network_file)
    g_kruskal=kruskal(g)
    ot=oriented_tree(g_kruskal)
    paths_profit = []
    for i in range(n):
        line=f.readline().split()
        node1 = int(line[0])
        node2 = int(line[1])
        profit = int(line[2])
        min_pow, path = min_power_kruskal(g_kruskal, ot, node1, node2)
        paths_profit.append([node1, node2, profit, min_pow])
    paths_profit_sorted=sorted(paths_profit , key=lambda l: -l[2])
    return paths_profit_sorted


# L'algo du sac à dos ne donne pas une solution exacte 
# Pour la méthode exacte, la complexité est exponentielle 

def trucks_from_file_dic(nb_file_trucks): 
    filename = "input/trucks." + str(nb_file_trucks) + ".in" #on crée le fichier et on l'ouvre
    f = open(filename, 'r')
    n = int(f.readline().rstrip())
    dict_trucks=dict()
    for i in range(n):
        line = f.readline().split()
        power = int(line[0])
        price = int(line[1])
        dict_trucks[power] = price
    sorted_trucks = sorted(dict_trucks.items(), key=lambda x: x[1], reverse=False)
    return sorted_trucks 

def trucks_from_file_list(nb_file_trucks): 
    filename = "input/trucks." + str(nb_file_trucks) + ".in" #on crée le fichier et on l'ouvre
    f = open(filename, 'r')
    n = int(f.readline().rstrip())
    truck_list = [] #on initialise une liste pour stocker les camions
    for i in range(n):
        line = f.readline().split()
        power = int(line[0])
        price = int(line[1])
        truck_list.append((power, price)) #on ajoute à la liste de camions
    return truck_list

'''On essaye une méthode mais elle ne marche pas sur le routes 2 donc la meilleure méthode est celle tout en bas'''

# Using greedy method
def knapsack(trucks, paths, budget):
    
    # On va initialiser nos variables 
    used_trucks = {} # Camions utilisés
    used_paths = [] # Chemins parcourus
    total_profit = 0 # Profit récupéré
    remaining_budget = budget # Budget restant 
    # Notre liste path est déjà triée par ordre decroissant en termes de profits
    # Les camions sont deja triés par ordre croissant en termes de prix 
    # On parcourt les chemins et on trouve 
    for i in range(len(paths)):
        for j in range(len(trucks)):
            if trucks[j][0] >= paths[i][3] and trucks[j][1] <= remaining_budget and paths[i] not in used_paths:
            # On pose une condition sur la puissance de camion qui doit etre supérieure au minpower du chemin, 
            # Le prix doit etre inférieur au budget restant 
            # Et le chemin ne doit pas avoir déjà été traité
                remaining_budget -= trucks[j][1] # On soustrait le prix du camion du budget
                if trucks[j][0] in used_trucks:
                    used_trucks[trucks[j][0]] += 1 
                else:
                    used_trucks[trucks[j][0]] = 1 
                used_paths.append(paths[i]) # On rajoute le chemin traité à la liste des chemins
                total_profit += paths[i][2] # On rajoute l'utilité du chemin parcouru 
    return total_profit, used_paths, used_trucks, budget-remaining_budget


'''On teste encore une autre méthode, celle qui marche pour tout'''
'''Celle-ci marche sur toutes les routes'''


def routes_from_file_simple(nb_file_routes): 
    res=[]
    filename = "input/routes." + str(nb_file_routes) + ".in"
    f = open(filename, 'r')
    n = int(f.readline().rstrip())
    for i in range(n):
        line=f.readline().split()
        src, dest, profit = map(int, line)
        res.append([(src, dest), profit])
    return res

def truck_remove(truck_list):
    truck_list = sorted(truck_list, key= lambda u: -u[0]) # On trie la liste par ordre décroissant de puissance
    validated_trucks = [truck_list[0]] # On initialise avec le premier
    price2=truck_list[0][1] # On initialise la variable de prix au premier prix 
    for i in range(1, len(truck_list)):
        # Si le prix du camion est inférieur au prix actuel, on ajoute le camion à la liste validée et on met à jour le prix actuel
        if truck_list[i][1] < price2 : 
            validated_trucks.append((truck_list[i][0], truck_list[i][1]))
            price2=truck_list[i][1]
    validated_trucks=validated_trucks[::-1] # On retourne la liste pour avoir l'ordre croissant de prix
    return validated_trucks

def truck_for_routes(network, nb_file_route, nb_file_truck):
    routes = routes_from_file_simple(nb_file_route) #on va utiliser toutes les fonctions kruskal de la séance précédente
    trucks = truck_remove(trucks_from_file_list(nb_file_truck))   
    g = graph_from_file(network)
    g2 = kruskal(g)
    h = oriented_tree(g2)
    power_mini, middle, min = 0, 0, 0
    max = len(trucks)
    power_t = int(trucks[middle][0])
    res = []
    for route in routes: # On fait une dichotomie
        a, b = min_power_kruskal(g, h, route[0][0], route[0][1])
        power_mini = int(a)
        middle = int((len(trucks)/2))
        min = 0
        max = len(trucks)
        while max - min > 1:
            power_t = int(trucks[middle][0])
            if power_t > power_mini:
                max = middle
                middle = int( (middle + min) /2)
            else:
                min = middle
                middle = int((middle+max)/2)
        res.append((route, trucks[min +1]))
    return res

def profit_best(network, nb_file_route, nb_file_trucks): # On veut trouver le profit maximal
    truck_routes = truck_for_routes(network, nb_file_route, nb_file_trucks)
    profit = 0
    B = 0
    l = 0
    profit_route = 0
    cost = 0
    powprof=[]
    truck_routes_ratio = []
    for i in range(len(truck_routes)): # On calcule profit coût et rapport pour trouver le plus intéressant
        profit_route = int(truck_routes[i][0][1])
        cost = int(truck_routes[i][1][1])
        rapport = profit_route/cost
        truck_routes_ratio.append(truck_routes[i] + (rapport,))
    truck_routes_ratio.sort(key=lambda truck_routes_ratio : truck_routes_ratio[2], reverse= True)
    while B<25*10**9 and l < len(truck_routes_ratio): 
        profit += truck_routes_ratio[l][0][1]
        B += truck_routes_ratio[l][1][1]
        powprof.append(truck_routes_ratio[l][0][0] + (truck_routes_ratio[l][1][0],))
        cost = truck_routes_ratio[l][1][0]
        profit_route = truck_routes_ratio[l][0][1]
        l += 1
    if B > 25*10**9: # Si le budget est suffisant
        powprof.pop(-1)
        B = B - cost # On retire le coût
        profit = profit - profit_route # On calcule le profit 
    powprof = [profit] + powprof
    B=str(B)
    y = "Le profit est " + B
    z = "Le budget utilisé est " + str(profit)
    return powprof, z, y
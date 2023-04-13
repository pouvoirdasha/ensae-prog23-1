import sys 
import time
sys.path.append("delivery_network")
from graph import Graph, get_paths_from_routes, trucks_from_file, knapsack
def test_q19(nbroutes, nbtrucks, b):
    t_dep = time.perf_counter()
    paths = get_paths_from_routes(nbroutes)
    truck = trucks_from_file(nbtrucks)
    total_profit, used_paths, used_trucks, used_budget=knapsack(truck, paths, b)
    t_fin= time.perf_counter()
    t=t_fin-t_dep
    
    
    print("les chemins couverts", used_paths, end='\n')
    print("les camions utilisés", used_trucks, end='\n')
    print("le profit est", total_profit, end='\n')
    print("le budget utilisé", used_budget, end='\n')
    print( "le temps d'execution est ", t, "s", end='\n ')

test_q19(1,1,100000000)
test_q19(1,2,100000000)
test_q19(3,1,100000000)
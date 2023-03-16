import sys 
import time
sys.path.append("delivery_network")
from graph import estimated_time_kruskal


print("Le temps nécessaire est :",  estimated_time_kruskal(1), "s")
print("Le temps nécessaire est :",  estimated_time_kruskal(2), "s")
print("Le temps nécessaire est :",  estimated_time_kruskal(3), "s")
print("Le temps nécessaire est :",  estimated_time_kruskal(4), "s")
print("Le temps nécessaire est :",  estimated_time_kruskal(5), "s")
print("Le temps nécessaire est :",  estimated_time_kruskal(6), "s")
print("Le temps nécessaire est :",  estimated_time_kruskal(7), "s")
print("Le temps nécessaire est :",  estimated_time_kruskal(8), "s")
print("Le temps nécessaire est :",  estimated_time_kruskal(9), "s")
# S'éxecute en moins d'une minute! 

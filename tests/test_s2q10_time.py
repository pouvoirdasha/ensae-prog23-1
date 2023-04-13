import time
import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file, estimated_time

print("Le temps nécessaire est :",  estimated_time(1), "s")

'''Les fichiers suivants mettent trop de temps à s'exécuter, on se contentera d'exécuter le 1'''
print("Le temps nécessaire est :",  estimated_time(2), "s") 
#print("Le temps nécessaire est :",  estimated_time(3), "s")
#print("Le temps nécessaire est :",  estimated_time(4), "s")


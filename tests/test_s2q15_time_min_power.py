import sys 
import time
sys.path.append("delivery_network")
from graph import estimated_time_kruskal


print("Le temps nécessaire est :",  estimated_time_kruskal(1), "s")

#il y a deux problèmes :
#1): si les graphes sont disjoints et qu'il ne peut pas y aller alors la fonction ne s'arrête pas
#2): pour x>1, trop long pour "input/network.x.in"
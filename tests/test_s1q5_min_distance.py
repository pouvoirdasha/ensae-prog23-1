# À compléter
import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file

import unittest   # The test framework

class Test_Reachability(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.04.in")
        self.assertEqual(g.get_shorter_path_with_power(1, 2, 10), [1, 2])
        self.assertEqual(g.get_shorter_path_with_power(1, 2, 11), [1, 4, 3, 2])
        

if __name__ == '__main__':
    unittest.main()
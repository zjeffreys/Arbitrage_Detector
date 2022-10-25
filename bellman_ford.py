from contextlib import nullcontext
from typing import Tuple, List
# from math import log
import sys
import math
"""
This implements a Bellman Ford Graph search to find arbitrations
between the currency markets
"""
VERTICES = ['GBP', 'JPY', 'EUR', 'CHF',
    'AUD']  # not sure if this should be hard coded??


class Graph:
    def __init__(self):
        self.V = len(VERTICES)
        self.graph = []  # [currency_A, currency_B, w] * 2n

    def addEdge(self, currency_A, currency_B, exchange_rate):
        self.graph.append([currency_A, currency_B, -math.log10(exchange_rate)])
        self.graph.append([currency_B, currency_A, math.log10(exchange_rate)])

    def printArr(self, dist):
        print("Vertex Distance from Source")
        for i in range(self.V):
            print("{0}\t\t{1}".format(i, dist[i]))

    def printGraph(self):
        for each in self.graph:
            print(each)


    def BellmanFord(self, src):
        dist = [float("Inf")] * self.V
        dist[src] = 0

        for _ in range(self.V - 1):
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w

        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                print("Graph contains negative weight cycle")
                return
 
        self.printArr(dist)

if __name__ == '__main__':
    if len(sys.argv) != 1:
        # print("Usage: python lab3.py GCDHOST GCDPORT")
        print("Usage: python3 lab3.py")
        exit(1)

    g = Graph()
    g.addEdge(0, 1, 100)
    g.addEdge(0, 2, 0.72848)
    g.addEdge(1, 2, 1.25783)
    g.addEdge(1, 3, 0.72848)
    g.addEdge(1, 4, 1.03237)
    g.addEdge(3, 2, 101.00345)
    
 
    # function call
    g.BellmanFord(0)
    g.addEdge(4, 3, 1.1159)
    g.addEdge(0, 2, 2.2848)
    g.BellmanFord(0)
    g.printGraph()
    
  


from contextlib import nullcontext
from datetime import timedelta
from datetime import datetime
import sys
import math

MAX_STEPS = 1000

"""
This implements a Bellman Ford Graph search to find arbitrations
between the currency markets
"""

class Graph:
    def __init__(self):
        self.graph = {}  # [currency_A, currency_B, w] * 2n
        self.vertices = None 

    def addEdge(self, currency_A, currency_B, quote):
        if not currency_A in self.graph:
            self.graph[currency_A] = {}        
        self.graph[currency_A][currency_B] = {"time": quote["time"], "price": -math.log10(quote["price"])}
        
        if not currency_B in self.graph:
            self.graph[currency_B] = {}
        self.graph[currency_B][currency_A] = {"time": quote["time"], "price": math.log10(quote["price"])}


    def removeStale(self, timeout = 1.5):
        stale_timeout = datetime.now() - timedelta(seconds=timeout)
        stales = 0
        for u in self.graph:
            for v in self.graph[u]:
                if(self.graph[u][v]["time"] <= stale_timeout):
                    del self.graph[u][v]
                    stales = stales + 1
        return stales

    def print_arbitrage(self, prev, src, trade_amount):
        steps = [src]
        last_step = prev[src]
		
        infiniteLoop = 0 # In case we get stuck in loop. shouldn't backtrack farther then verticies length
        while not last_step == src:
            if(infiniteLoop == MAX_STEPS): 
                return None
            steps.append(last_step)
            last_step = prev[last_step]
            infiniteLoop = infiniteLoop + 1
		
        steps.append(src)
        steps.reverse()

        print("From", trade_amount," ", src)		
        value = trade_amount
        last = src
		
        for i in range(1, len(steps)):
            curr = steps[i]
            price = math.exp(-1 * self.graph[last][curr]["price"]) 
            value *= price
            print(" = {} {}".format(value, curr))
            last = curr
			
        profit = value - trade_amount
        print(" > Profit of {} {}".format(profit, src))
            

    def bellman_ford(self, src, tolerance=0):
        self.vertices = len(self.graph)
        dist = {}
        prev = {}
        
        for vertex in self.graph:
            dist[vertex] = float("Inf")
            prev[vertex] = None
		
        dist[src] = 0

        for i in range(self.vertices - 1):
            for curr1 in self.graph:
                for curr2 in self.graph[curr1]:
                    weight = self.graph[curr1][curr2]["price"]
                    
                    # if this new path is shorter than the previous distance
                    if dist[curr1] != float("Inf") and (dist[curr1] + weight + tolerance < dist[curr2] and dist[curr1] + weight - tolerance < dist[curr2]):
                        dist[curr2] = dist[curr1] + weight
                        prev[curr2] = curr1
                        
        # negative path detection
        for curr1 in self.graph:
            for curr2 in self.graph[curr1]:
                weight = self.graph[curr1][curr2]["price"]
                
                if dist[curr1] != float("Inf") and (dist[curr1] + weight + tolerance < dist[curr2] and dist[curr1] + weight - tolerance < dist[curr2]):
                    # we found a negative path, return it
                    return dist, prev, (curr1, curr2)
                    
        return dist, prev, None
    


# if __name__ == '__main__':
#     if len(sys.argv) != 1:
#         # print("Usage: python lab3.py GCDHOST GCDPORT")
#         print("Usage: python3 lab3.py")
#         exit(1)


#     g = Graph()
#     g.addEdge('USD', "GBP", 0.7989773090444231)
#     g.addEdge('GBP', "CAD", 0.8322701347524601)
#     g.addEdge('CAD', "AUD", 3.3290805390098406)
#     g.addEdge('AUD', "USD", 0.75035)
#     print(g.BellmanFord('USD'))
    # g.printGraph()
    



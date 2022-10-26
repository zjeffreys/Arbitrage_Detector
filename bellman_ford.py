from datetime import timedelta
from datetime import datetime
import math

MAX_STEPS = 1000 
TOLERANCE = 0
"""
This implements a Bellman Ford Graph search to find arbitrations
between the currency markets
"""

class Graph:
    def __init__(self):
        """
        Construct a new graph to store V and E
        """
        self.graph = {}  
        self.vertices = None 

    def addEdge(self, currency_A, currency_B, quote):
        """
        Add edges for each quote. Adds edge for currency A to currency B, and vice versa.

        :param currency_A: Currency start
        :param currency_B: Currency to convert into 
        :param quote: the weight consiting of the time and price
        """
        if not currency_A in self.graph:
            self.graph[currency_A] = {}        
        self.graph[currency_A][currency_B] = {"time": quote["time"], "price": -math.log10(quote["price"])}
        
        if not currency_B in self.graph:
            self.graph[currency_B] = {}
        self.graph[currency_B][currency_A] = {"time": quote["time"], "price": math.log10(quote["price"])}


    def removeStale(self, timeout = 1.5):
        """
        Discard stale quotes, but leaves it in the graph if it 
        does not exceep the 1.5 second timeout

        :param timeout: time in seconds to allow quote to stay in graph
        """
        stale_timeout = datetime.now() - timedelta(seconds=timeout)
        stales = 0
        for currency_A in self.graph:
            for currency_B in self.graph[currency_A]:
                if(self.graph[currency_A][currency_B]["time"] <= stale_timeout):
                    del self.graph[currency_A][currency_B]
                    stales = stales + 1
        return stales

    def print_arbitrage(self, prev, src, trade_amount):
        """
        Prints the arbitrage that was found and the 
        conversions of currencies

        :param prev: Previous currency converted from 
        :param src: Starting currency
        :param trade_amount: Amount of src currency to start out with
        """
        
        steps = [src]
        last_step = prev[src]
        infiniteLoop = 0 

        # Backtrack to create path 
        while not last_step == src:
            # Incase of negative infinity 
            if(infiniteLoop == MAX_STEPS): 
                return None
            steps.append(last_step)
            last_step = prev[last_step]
            infiniteLoop = infiniteLoop + 1
        steps.append(src)

        # Reverse to get into correct order 
        steps.reverse()

        print("From", trade_amount," ", src)		
        value = trade_amount
        last = src

        # Convert into price and multiply together to determine currency value after arbitrage
        for i in range(1, len(steps)):
            curr = steps[i]
            price = math.exp(-1 * self.graph[last][curr]["price"]) 
            value *= price
            print(" = {} {}".format(value, curr))
            last = curr
			
        profit = value - trade_amount
        print(" > Profit of {} {}".format(profit, src))
            

    def bellman_ford(self, src, tolerance=TOLERANCE):
        """
        Runs the bellman_ford shortest path algorithem 
        
        :param src: Currency to start with
        :param tolerance: amount of tolerance thats acceptable
        """
        self.vertices = len(self.graph)
        dist = {}
        prev = {}
        
        # Set distances to infinitiy and previous to None 
        for vertex in self.graph:
            dist[vertex] = float("Inf")
            prev[vertex] = None
		
        # Relax all edges
        dist[src] = 0
        for i in range(self.vertices - 1):
            for currency_A in self.graph:
                for currency_B in self.graph[currency_A]:
                    weight = self.graph[currency_A][currency_B]["price"]
                    if dist[currency_A] != float("Inf") and (dist[currency_A] + weight + tolerance < dist[currency_B] and dist[currency_A] + weight - tolerance < dist[currency_B]):
                        dist[currency_B] = dist[currency_A] + weight
                        prev[currency_B] = currency_A
                        
        # Negative path detection
        for currency_A in self.graph:
            for currency_B in self.graph[currency_A]:
                weight = self.graph[currency_A][currency_B]["price"]
                if dist[currency_A] != float("Inf") and (dist[currency_A] + weight + tolerance < dist[currency_B] and dist[currency_A] + weight - tolerance < dist[currency_B]):
                    return prev, (currency_A, currency_B)
                    
        return prev, None
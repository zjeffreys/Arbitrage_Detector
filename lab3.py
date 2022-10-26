from base64 import decode
from datetime import datetime
from re import S
import socket
import sys
from typing import Tuple
from urllib.request import Request
from bellman_ford import Graph
import fxp_bytes
import fxp_bytes_subscriber
import ipaddress
from array import array
import threading
import time
# from bellman_ford import Graph


REQUEST_ADDRESS = ('127.0.0.1', 50403)
DEFAULT_ADDRESS = ('127.0.0.1', 0)
TEST_ADDRESS = ('127.0.0.1', 65534)
TEN_MINUTES = 10 * 60  # ten minutes
ONE_SEC = 1
BUFFER = 2048
MESSAGE_TIMEOUT = 0.1
ONE_HUNDRED_USD = 100


class Lab3(object):
    def __init__(self, publisher=REQUEST_ADDRESS):
        self.publisher_address = publisher
        self.graph = Graph()
        self.myAddr = None  # listener sets port
        self.run()

    def run(self):
        listener = threading.Thread(target=self.listen_to_publisher)
        subscriber = threading.Thread(target=self.subscribe_to_forex)
        listener.start()
        time.sleep(ONE_SEC)  # give lister time to set port dynamically
        subscriber.start()

    def subscribe_to_forex(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                timeout = datetime.now() + (datetime.utcnow() - datetime.now())
                s.sendto(fxp_bytes_subscriber.serialize_address(self.myAddr), self.publisher_address)
            time.sleep(TEN_MINUTES)

    def listen_to_publisher(self):
        print("starting listener")
        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener.bind(DEFAULT_ADDRESS)
        self.myAddr = (DEFAULT_ADDRESS[0], listener.getsockname()[1])
        timeout = datetime.now() + (datetime.utcnow() - datetime.now())
        while True:
            data, addr = listener.recvfrom(BUFFER)
            de_marshaled = fxp_bytes_subscriber.de_marshal_message(data)
            for quote in de_marshaled:
                if ((timeout - quote["time"]).total_seconds() > MESSAGE_TIMEOUT):
                    print("ignoring out-of-sequence message")
                else:
                    curA, curB = quote["cross"].split("/")
                    self.graph.addEdge(curA, curB, quote)
                    print(quote["time"], curA, curB, quote["price"])
                    timeout = quote["time"]
            stales = self.graph.removeStale()
            if (stales > 0):
                print("Removed ", stales, "stale quotes")
            dist, prev, edge = self.graph.bellman_ford('USD')
            if not edge is None:
                self.graph.print_arbitrage(prev, 'USD', ONE_HUNDRED_USD)
               


if __name__ == '__main__':
    if len(sys.argv) != 1:
        # print("Usage: python lab3.py GCDHOST GCDPORT")
        print("Usage: python3 lab3.py")
        exit(1)
    lab3 = Lab3()
    
    





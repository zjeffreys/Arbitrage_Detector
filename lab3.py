import socket
import sys

class Lab3(object):
    def __init__(self, gcd_host, gcd_port):
        print("constructor")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python lab1.py GCDHOST GCDPORT")
        exit(1)
    print("Hello from lab3.py")
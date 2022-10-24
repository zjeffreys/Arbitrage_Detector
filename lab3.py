import socket
import sys
import fxp_bytes
import fxp_bytes_subscriber
import ipaddress
from array import array


REQUEST_ADDRESS = ('127.0.0.1', 50403)
DEFAULT_ADDRESS = ('127.0.0.1', 0)
TEST_ADDRESS = ('127.0.0.1', 65534)


class Lab3(object):
    def __init__(self):
        self.subscribe_to_forex()

    def subscribe_to_forex(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(DEFAULT_ADDRESS)
            myAddr = (DEFAULT_ADDRESS[0], s.getsockname()[1])
            while True:
                s.sendto(fxp_bytes_subscriber.serialize_address(myAddr), REQUEST_ADDRESS)
                data, addr = s.recvfrom(4096)
                decoded = fxp_bytes_subscriber.de_marshal_message(data)
            # print(data)
            # continue from here 
    


if __name__ == '__main__':
    if len(sys.argv) != 1:
        # print("Usage: python lab3.py GCDHOST GCDPORT")
        print("Usage: python3 lab3.py")
        exit(1)
    lab3 = Lab3()
    
    





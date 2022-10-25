"""
This module contains marshaling functions for subscriber

"""

from calendar import day_abbr
from encodings import utf_8
import ipaddress
from array import array
from datetime import datetime, timedelta
from locale import currency
from tokenize import String
import pickle

MICROS_PER_SECOND = 1_000_000

"""
Convert a string of the combined (host, port) into a byte array.
>>> serialize_address(('127.0.0.1', 65534))
b\x7f\x00\x00\x01\xff\xfe
"""


def serialize_address(address):
    b = array('B')
    h = array('H')
    for num in address[0].split('.'):
        b.append(int(num))
    h.append(int(address[1]))
    h.byteswap()
    return (b.tobytes() + h.tobytes())


"""
Receives the byte steam and converts it to a message
"""
def de_marshal_message(datagram):
    # Datetime
    t  = array('Q', datagram[0:8])
    t.byteswap()
    second_elapsed = t[0]/MICROS_PER_SECOND
    d = datetime(1970, 1, 1) + timedelta(seconds= second_elapsed)    

    # Currencies
    c = datagram[8:14]
    cA = c[0:3]
    cB = c[3:]
    currencies = [cA.decode('UTF-8'), cB.decode('UTF-8')]

    # Exchange Rate
    exchangeArray = array('d', datagram[14: 22])
    exchangeRate = exchangeArray[0]

    print(d, " ", currencies[0], " ", currencies[1], " ", exchangeRate)

   

   

   
   
    
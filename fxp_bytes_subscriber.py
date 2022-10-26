"""
This module contains marshaling functions for subscriber
"""
from calendar import day_abbr
from encodings import utf_8
import ipaddress
from array import array
from datetime import datetime, timedelta


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
    quotes = []
    #print("Length: ",len(datagram))
    for offset in range(0, int(len(datagram)/32)):
        byte_offset = datagram[offset * 32: offset * 32 + 32]
        quote = {}
        
        # Time
        t  = array('Q', byte_offset[0:8])
        t.byteswap()
        second_elapsed = t[0]/MICROS_PER_SECOND
        d = datetime(1970, 1, 1) + timedelta(seconds= second_elapsed)    
        quote["time"] = d

        # Currencies
        c = byte_offset[8:14]
        cA = c[0:3]
        cB = c[3:]
        currencies = [cA.decode('UTF-8'), cB.decode('UTF-8')]
        quote["cross"] = currencies[0] + "/" + currencies[1]

        # Exchange Rate
        exchangeArray = array('d', byte_offset[14: 22])
        exchangeRate = exchangeArray[0]
        quote["price"] = exchangeRate

        quotes.append(quote)

    return quotes

   

   

   
   
    
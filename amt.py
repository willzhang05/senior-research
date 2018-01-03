#!/usr/bin/python3
import socket
import random
import ctypes
from bitarray import bitarray

def gen_nonce():
    return ctypes.c_uint32(random.random()).value

def send_relay_discovery(anycast_addr, anycast_port):
    protocol_version = 0
    message_type = 1
    
    message = bitarray(64)
    message.setall(0)
    message[3] = protocol_version
    message[7] = message_type
    nonce = random.random()
    print(message)
    message = message.tobytes()
    print(nonce)
    gw_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gw_out.sendto(message, (anycast_addr, anycast_port))
    gw_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gw_in.bind(("localhost", anycast_port))
    while True:
        data, addr = gw_in.recvfrom(1024)
        print("received: ", data)
    

def main():
    amt_relay_ip = "198.38.23.145"
    amt_relay_port = 2268
    send_relay_discovery(amt_relay_ip, amt_relay_port)

if __name__ == '__main__':
    main()

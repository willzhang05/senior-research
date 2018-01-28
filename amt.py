#!/usr/bin/python3
import socket
import struct
import random
import ctypes
from bitarray import bitarray
#import flask

#app = Flask(__name__)

#@app.route('/')
def index():
    return render_template("index.html")

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
    

def recv_native(anycast_addr, anycast_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((anycast_addr, anycast_port))
    mreq = struct.pack("4sl", socket.inet_aton(anycast_addr), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        print(sock.recv(10240))

def main():
#    amt_relay_ip = "198.38.23.145"
#    amt_relay_port = 2268
#    send_relay_discovery(amt_relay_ip, amt_relay_port)
    mcast_grp = "233.44.15.9"
    mcast_port = 50001
    recv_native(mcast_grp, mcast_port)

    

if __name__ == '__main__':
    main()

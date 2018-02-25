#!/usr/bin/python3
import threading
import socket
import struct
from flask import Flask, Response, render_template

app = Flask(__name__)

#buff = [None] * 188
buff = None
index = 0

@app.before_first_request
def connect():
    anycast_addr = "233.44.15.9"
    anycast_port = 50001
    def recv_native(anycast_addr, anycast_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((anycast_addr, anycast_port))
        mreq = struct.pack("=4sl", socket.inet_aton(anycast_addr), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        global buff
        global index
        while True:
            recv = sock.recv(10240)
            buff = recv
            #index = buff.index(b'G')
            #recv = recv[index:index + 188]
            #s_recv = [recv[i:i+2] for i in range(0, len(recv), 2)]
            #for i in range(len(s_recv)):
            #    buff[i] = (int(s_recv[i], base=16))[2:]
            #    print(buff[i])
            
    thread = threading.Thread(target=recv_native, args=[anycast_addr, anycast_port])
    thread.start()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video')
def video():
    print(buff)
    return Response(buff, mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(threaded=True)

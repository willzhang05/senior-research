#!/usr/bin/python3
import threading
import socket
import struct
from flask import Flask, Response, render_template

app = Flask(__name__)

buff = None

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
        while True:
            buff = sock.recv(10240)
    thread = threading.Thread(target=recv_native, args=[anycast_addr, anycast_port])
    thread.start()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video')
def video():
    return Response(buff, mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(threaded=True)

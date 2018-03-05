#!/usr/bin/env python3

# Source: https://pymotw.com/3/socket/tcp.html

import socket
import sys

def make_request(ip, port, data):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (ip, port)
    print('Connecting to tcp://{}:{}'.format(*server_address))
    sock.connect(server_address)

    resp = []
    try:
        message = str.encode(data)
        print('Sending {!r}'.format(message))
        sock.sendall(message)


        while True:
            data = sock.recv(32)
            if not data: break
            resp.extend(data.decode("utf-8"))
    finally:
        sock.close()
        return ''.join(resp)

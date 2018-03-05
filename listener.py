#!/usr/bin/env python3

import subprocess
import sys
import tcp_client


path_on_servers = '~/.algorand'
listener_py = 'tcp_listener.py'


class Listener:

    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.running = False

    def __repr__(self):
        return '{} at {}:{}'.format(self.name, self.ip, self.port)

    def __str__(self):
        return self.__repr__()

    def setup(self):
        ex = subprocess.call(["scp", listener_py,
                              "{}:{}".format(self.ip, path_on_servers)])
        if ex != 0:
            err = "Error while setting up listener on {}".format(self.ip)
            sys.exit(err)
        ex = subprocess.call(["ssh", self.ip, "-t", "chmod +x {}/{}"
                              .format(path_on_servers, listener_py)])
        if ex != 0:
            err = "Error while setting up listener on {}".format(self.ip)
            sys.exit(err)

    def run(self):
        if self.running:
            return
        command = "tmux new-session -d -s 'ar-listen' '{}/{} {}'".format(
            path_on_servers, listener_py, self.port)
        ex = subprocess.call(["ssh", self.ip, "-t", command])
        if ex != 0:
            err = "Error while running listener on {}".format(self.ip)
            sys.exit(err)
        self.running = True

    def stop(self):
        resp = tcp_client.make_request(self.ip, self.port, 'die')
        print("Stop response from {}: {}".format(self.ip, resp))
        self.running = False

    def send(self, data):
        resp = tcp_client.make_request(self.ip, self.port, data)
        print("Response from {}: {}".format(self.ip, resp))

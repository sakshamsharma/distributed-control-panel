#!/usr/bin/env python3

import sys
import pickle
import http_client
from consts import (listener_py, listener_deps, path_on_servers)


def path_to_file(x):
    y = x.split('/')
    return y[len(y)-1]


class Listener:

    def __init__(self, name, ip, port, server):
        self.name = name
        self.ip = ip
        self.port = port
        self.running = False
        self.server = server

    def __repr__(self):
        return '{} at {}:{}'.format(self.name, self.ip, self.port)

    def __str__(self):
        return self.__repr__()

    def setup(self):
        for f in listener_deps:
            ex = self.server.copy_file(f, path_on_servers, path_to_file(f))
            if ex != 0:
                err = "Error while setting up {} on {}".format(f, self.ip)
                sys.exit(err)
        ex = self.server.copy_executable(listener_py, path_on_servers,
                                         path_to_file(listener_py))
        if ex != 0:
            err = "Error while setting up listener on {}".format(self.ip)
            sys.exit(err)

    def run(self):
        if self.running:
            return
        command = ["tmux", "new-session", "-d", "-s", "dcp-listen",
                   '{}/{} {}'.format(path_on_servers,
                                     path_to_file(listener_py), self.port)]
        ex = self.server.run_proc(command)
        if ex != 0:
            err = "Error while running listener on {}".format(self.ip)
            print(err)
        else:
            self.running = True

    def stop(self):
        resp = http_client.make_get_request(self.ip, self.port, 'die')
        print("Die response from {}: {}".format(self.ip, resp))
        self.running = False

    def send(self, action, py_data):
        data = pickle.dumps(py_data)
        resp = http_client.make_post_request(self.ip, self.port, action, data)
        print("Response from {}: {}".format(self.ip, resp))

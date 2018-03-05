#!/usr/bin/env python3


import actions
import consts


class Node:

    def __init__(self, name, server, port, http_port, peers):
        self.name = name
        self.server = server
        self.port = port
        self.http_port = http_port
        self.peers = peers

    def __repr__(self):
        return '{} on server ({}) at port {}'.format(
            self.name, self.server, self.http_port)

    def __str__(self):
        return self.__repr__()

    def run_binary(self):
        action = actions.RunAction(
            ns="dcp",
            name=self.name,
            args="--testing_arg -u -v --uselessarg",
            binary=self.server.binary.path_on_server,
            logs="{}.{}.logs".format(consts.path_on_servers, self.name)
        )
        self.server.listener.send("run", action)

    def stop_binary(self):
        action = actions.StopAction(
            ns="dcp",
            name=self.name
        )
        self.server.listener.send("stop", action)

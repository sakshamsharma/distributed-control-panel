#!/usr/bin/env python3


import actions
import consts
import time


class Node:

    def __init__(self, name, server, port, http_port, peers, sleep_time=0):
        self.name = name
        self.server = server
        self.port = port
        self.http_port = http_port
        self.peers = peers
        self.logfile = "{}/.{}.logs".format(consts.path_on_servers, self.name)
        self.addr = self.server.ip + ":" + str(self.port)
        self.sleep_time = sleep_time

    def register_nodes(self, nodes, arg_gen):
        peers_with_addr = [nodes[peer] for peer in self.peers]
        self.args = eval(arg_gen)(peers_with_addr)(self)

    def __repr__(self):
        return '{} on server ({}) at port {}'.format(
            self.name, self.server, self.http_port)

    def __str__(self):
        return self.__repr__()

    def run_binary(self):
        action = actions.RunAction(
            ns="dcp",
            name=self.name,
            args=self.args,
            binary=self.server.binary.path_on_server,
            logs=self.logfile
        )
        self.server.listener.send("run", action)
        time.sleep(self.sleep_time)

    def stop_binary(self):
        action = actions.StopAction(
            ns="dcp",
            name=self.name
        )
        self.server.listener.send("stop", action)

    def logs(self):
        self.server.tail_file(self.logfile)

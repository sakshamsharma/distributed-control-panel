#!/usr/bin/env python3


class Node:

    def __init__(self, name, server, binary, port, http_port, peers):
        self.name = name
        self.server = server
        self.binary = binary
        self.port = port
        self.http_port = http_port
        self.peers = peers

    def __repr__(self):
        return '{} on server ({}) at port {}'.format(
            self.name, self.server, self.http_port)

    def __str__(self):
        return self.__repr__()

#!/usr/bin/env python3


class Node:

    def __init__(self, name, location, port, http_port, peers):
        self.name = name
        self.location = location
        self.port = port
        self.http_port = http_port
        self.peers = peers

    def __repr__(self):
        return '{} on server ({}) at port {}'.format(
            self.name, self.location, self.http_port)

    def __str__(self):
        return self.__repr__()

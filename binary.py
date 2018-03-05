#!/usr/bin/env python3


import sys
from consts import path_on_servers


class Binary:

    def __init__(self, path, server):
        self.path_local = path
        self.server = server
        self.path_on_server = "{}/binary".format(path_on_servers)

    def setup(self):
        ex = self.server.copy_executable(self.path_local, path_on_servers,
                                         "binary")
        if ex != 0:
            err = "Error while setting up binary on {}".format(self.server.ip)
            sys.exit(err)

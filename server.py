#!/usr/bin/env python3

import random
import subprocess
import sys
from listener import Listener


path_on_servers = '~/.algorand'
setup_cache = '.cache_setup'
listener_py = 'tcp_listener.py'


class Server:

    setup_cache_contents = {}

    def read_setup_cache():
        """Static function to setup cache"""
        cache_file = ''
        try:
            cache_file = open(setup_cache, 'r')
        except IOError:
            cache_file = open(setup_cache, 'w')
            cache_file.close()
            cache_file = open(setup_cache, 'r')
        contents = cache_file.readlines()
        for server in contents:
            Server.setup_cache_contents[server.strip()] = True
        cache_file.close()

    def __init__(self, ip, name="noname", port=22):
        self.name = name
        self.ip = ip
        self.port = port
        listener_port = random.randint(20000, 25000)
        self.listener = Listener(name, ip, listener_port)

    def __repr__(self):
        return '{} at {}:{}'.format(self.name, self.ip, self.port)

    def __str__(self):
        return self.__repr__()

    def setup_ssh(self):
        ex = subprocess.call(["ssh-copy-id", self.ip])
        if ex != 0:
            sys.exit("Error while setting up login on server {}"
                     .format(self.ip))

    def setup_folder(self):
        ex = subprocess.call(["ssh", self.ip, "-t",
                              "mkdir -p {}".format(path_on_servers)])
        if ex != 0:
            sys.exit("Error while setting up listener on {}"
                     .format(self.ip))

    def setup_binary(self):
        # TODO: Incomplete.
        return

    def finish_setup(self):
        with open(setup_cache, "a") as f:
            f.write("{}\n".format(self.ip))

    def setup_volatile(self):
        self.setup_binary()
        self.listener.setup()

    def setup(self, copy_anyway=False):
        if len(Server.setup_cache_contents) == 0:
            Server.read_setup_cache()
        if self.ip in Server.setup_cache_contents:
            if copy_anyway:
                self.setup_volatile()
            return

        print("Setting up server {}".format(self.ip))
        self.setup_ssh()
        self.setup_folder()
        self.finish_setup()
        self.setup_volatile()
        print("Finished setting up server {}".format(self.ip))

    def run(self):
        self.listener.run()

    def shutdown(self):
        self.listener.stop()

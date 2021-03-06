#!/usr/bin/env python3

import random
import subprocess
import sys
from listener import Listener
from binary import Binary
from consts import (path_on_servers, setup_cache)


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

    def __init__(self, ip, binary, name="noname", port=22):
        self.name = name
        self.ip = ip
        self.port = port
        listener_port = random.randint(20000, 25000)
        self.listener = Listener(name, ip, listener_port, self)
        self.binary = Binary(binary, self)

    def __repr__(self):
        return '{} at {}:{}'.format(self.name, self.ip, self.port)

    def __str__(self):
        return self.__repr__()

    def run_proc(self, args):
        if self.ip in ["127.0.0.1", "0.0.0.0", "localhost"]:
            try:
                ex = subprocess.call(["bash", "-c", " ".join(args)])
                return ex
            except KeyboardInterrupt:
                print("Process stopped by user")
                return 0
        else:
            return subprocess.call(["ssh", self.ip, "-t", " ".join(args)])

    def copy_file(self, file_path_local, file_path_server, file_name_server):
        return subprocess.call(["scp", file_path_local,
                                "{}:{}/{}".format(self.ip,
                                                  file_path_server,
                                                  file_name_server)])

    def copy_executable(self, file_path_local, file_location_server,
                        file_name_server):
        ex = self.copy_file(file_path_local, file_location_server,
                            file_name_server)
        if ex != 0:
            return ex
        return self.run_proc(["chmod", "+x", "{}/{}".format(
            file_location_server, file_name_server)])

    def tail_file(self, file_path_server):
        try:
            self.run_proc(["tail", "-f", file_path_server])
        finally:
            pass

    def setup_ssh(self):
        ex = subprocess.call(["ssh-copy-id", self.ip])
        if ex != 0:
            sys.exit("Error while setting up SSH login on server {}"
                     .format(self.ip))

    def setup_folder(self):
        ex = self.run_proc(["mkdir", "-p", path_on_servers])
        if ex != 0:
            sys.exit("Error while setting up main data folder on {}"
                     .format(self.ip))

    def clear_logs(self):
        ex = self.run_proc(["bash", "-c",
                            "'rm {}/.*logs'".format(path_on_servers)])
        if ex != 0:
            sys.exit("Error while clearing logs on {}" .format(self.ip))

    def finish_setup(self):
        with open(setup_cache, "a") as f:
            f.write("{}\n".format(self.ip))

    def setup_volatile(self):
        self.binary.setup()
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
        self.clear_logs()
        self.finish_setup()
        print("Finished setting up server {}".format(self.ip))

    def run(self):
        self.setup_volatile()
        self.listener.run()

    def shutdown(self):
        self.listener.stop()

#!/usr/bin/env python3

import subprocess


class Tmux:
    def __init__():
        pass

    def ls(server=None):
        if not server:
            subprocess.call(["tmux", "ls"])
        else:
            server.run_proc(["tmux", "ls"])

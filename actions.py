#!/usr/bin/env python3


class RunAction:

    def __init__(self, ns, name, args, binary, logs):
        self.action_type = "run"
        self.ns = ns
        self.name = name
        self.args = args
        self.binary = binary
        self.logs = logs
        self.shell_cmd = "bash -c '{} {} > {} 2>&1'".format(
            self.binary, self.args, self.logs)
        self.session_name = "{}-{}".format(ns, name)


class StopAction:

    def __init__(self, ns, name):
        self.action_type = "stop"
        self.session_name = "{}-{}".format(ns, name)

#!/usr/bin/env python3

import json
import setup_graph
import server
import math
import atexit
import argcfg
from tmux import Tmux


servers = []
nodes = []
logs = []
cfg = {}


def dummy():
    Tmux()


def shutdown_all_servers():
    print("Shutting down all servers")
    for s in servers:
        print("Shutting down", s)
        s.shutdown()


def setup_all_servers():
    shutdown_all_servers()
    for s in servers:
        s.setup(True)


def run_binaries_on_all_nodes():
    for s in servers:
        s.clear_logs()
    for n in nodes:
        n.run_binary()


def stop_binaries_on_all_nodes():
    for n in nodes:
        n.stop_binary()


def run_new_node():
    global nodes, logs
    node = setup_graph.create_new_node(servers, nodes)
    node.peers = [0]
    node.register_nodes(nodes=nodes, arg_gen=cfg["arg-gen-lambda"])
    nodes.append(node)
    logs.append(node.logs)
    node.run_binary()


def set_node_cnt(n):
    global servers, nodes, cfg, logs
    try:
        args = argcfg.get_args()
        args.digraph = True
        if not args.edges:
            args.edges = min(math.ceil(float(n) * 2.5), n*(n-1))

        with open(args.cfg) as f:
            cfg = json.loads(f.read())
            for entry in cfg["servers"]:
                s = server.Server(ip=entry["ip"],
                                  binary=cfg["binary"],
                                  name=entry["name"])
                s.setup()
                s.run()
                servers.append(s)

        nodes = setup_graph.setup_graph_return_nodes(args, servers, cfg)
        for n in nodes:
            n.register_nodes(nodes=nodes, arg_gen=cfg["arg-gen-lambda"])

        logs = [n.logs for n in nodes]

        print("\nServers available:")
        for s in servers:
            print(s)

        print("""
        Available variables/methods:
        - nodes
        - servers
        - logs
        - shutdown_all_servers()
        - setup_all_servers()
        - run_binaries_on_all_nodes()
        - stop_binaries_on_all_nodes()
        - Tmux.ls(?server)
        """)

    except SystemExit:
        shutdown_all_servers()


args = argcfg.get_args()
set_node_cnt(int(args.nodes))
atexit.register(shutdown_all_servers)

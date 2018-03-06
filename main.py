#!/usr/bin/env python3

import json
from setup_graph import setup_graph_return_nodes
import server
import math
import atexit
import argcfg


servers = []
nodes = []


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
    for n in nodes:
        n.run_binary()


def stop_binaries_on_all_nodes():
    for n in nodes:
        n.stop_binary()


try:
    args = argcfg.get_args()
    args.digraph = True
    n = int(args.nodes)
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

    nodes = setup_graph_return_nodes(args, servers)
    for n in nodes:
        n.register_nodes(nodes=nodes, arg_gen=cfg["arg-gen-lambda"])

    print("\nServers available:")
    for s in servers:
        print(s)

    print("""
    Available variables/methods:
    - nodes
    - servers
    - shutdown_all_servers()
    - setup_all_servers()
    - run_binaries_on_all_nodes()
    - stop_binaries_on_all_nodes()
    """)

except SystemExit:
    shutdown_all_servers()

atexit.register(shutdown_all_servers)

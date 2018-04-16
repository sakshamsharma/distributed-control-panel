#!/usr/bin/env python3

import math
from node import Node
import random
import random_connected_graph as rcg


def setup_graph_return_nodes(args, servers, cfg):
    graph = rcg.get_graph(args)

    node_cnt = int(args.nodes)

    peers_of = {}
    for edge in graph.edges:
        peers_of.setdefault(edge[0], []).append(edge[1])

    per_server_nodes = math.ceil(node_cnt / len(servers))

    print("Connections among nodes:")
    print(peers_of)

    nodes = []
    cnt = 0

    for server in servers:
        done = 0
        while done < per_server_nodes and cnt < node_cnt:
            node = Node(
                name="Node-" + str(cnt),
                server=server,
                port=random.randint(10000, 15000),
                http_port=random.randint(15000, 20000),
                peers=peers_of[cnt]
            )
            nodes.append(node)
            cnt += 1
            done += 1

    if cfg["has-genesis-node"]:
        node = Node(
            name="Genesis-Node",
            server=servers[0],
            port=random.randint(10000, 15000),
            http_port=random.randint(15000, 20000),
            peers=[],
            sleep_time=2
        )
        nodes.append(node)
        nodes[0].peers.append(len(nodes)-1)

    return nodes

#!/usr/bin/env python3

import math
import node
import random
import random_connected_graph as rcg


def setup_graph(args, servers):
    graph = rcg.get_graph(args)

    node_cnt = int(args.nodes)

    peers_of = {}
    for edge in graph.edges:
        peers_of.setdefault(edge[0], []).append(edge[1])

    per_server_nodes = math.ceil(node_cnt / len(servers))

    print(peers_of)

    nodes = []
    cnt = 0
    for server in servers:
        done = 0
        while done < per_server_nodes and cnt < node_cnt:
            node_ = node.Node(
                name="Node-" + str(cnt),
                location=server,
                port=random.randint(10000, 15000),
                http_port=random.randint(15000, 20000),
                peers=peers_of[cnt]
            )
            nodes.append(node_)
            cnt += 1
            done += 1

    return nodes

#!/usr/bin/env python3

import math
from node import Node
import random
import random_connected_graph as rcg


def create_new_node(servers, nodes):
    return Node(
        name="Node-" + str(len(nodes)),
        server=random.sample(servers, 1)[0],
        port=random.randint(10000, 15000),
        http_port=random.randint(15000, 20000),
        peers=nodes[0]
    )


def setup_graph_return_nodes(args, servers, cfg):
    node_cnt = int(args.nodes)

    if cfg["sequential"]:
        return create_sequential_graph(node_cnt, args, servers)
    else:
        return create_fancy_graph(node_cnt, args, servers)


def create_sequential_graph(n, args, servers):
    genesis = Node(
        name="Node-0",
        server=servers[0],
        port=random.randint(10000, 15000),
        http_port=random.randint(15000, 20000),
        peers=[],
        sleep_time=2
    )

    # What order should we allocate the servers in?
    idxs = [i for i in range(1, n+1)]
    random.shuffle(idxs)

    # Assign servers in a random order.
    nodes = [genesis]
    cnt = 1
    per_server_nodes = math.ceil(n / len(servers))
    for server in servers:
        done = 0
        while done < per_server_nodes and cnt <= n:
            node = Node(
                name="Node-" + str(cnt),
                server=server,
                port=random.randint(10000, 15000),
                http_port=random.randint(15000, 20000),
                peers=None
            )
            nodes.append(node)
            cnt += 1
            done += 1

    # Assign peers.
    if not args.edges_per_node:
        edges_per_node = 3
    else:
        edges_per_node = int(args.edges_per_node)

    available_nodes = []
    for i, node in enumerate(nodes):
        node.peers = random.sample(available_nodes, min(len(available_nodes),
                                                        edges_per_node))
        available_nodes.append(i)

    print("Connections among nodes:")
    peers_of = {}
    for i, node in enumerate(nodes):
        peers_of[i] = node.peers
    print(peers_of)

    return nodes


def create_fancy_graph(n, args, servers):
    graph = rcg.get_graph(args)

    peers_of = {}
    for edge in graph.edges:
        peers_of.setdefault(edge[0], []).append(edge[1])
    return assign_nodes_to_servers(n, peers_of, [], servers)


def assign_nodes_to_servers(n, peers_of, nodes, servers):
    per_server_nodes = math.ceil(n / len(servers))

    print("Connections among nodes:")
    print(peers_of)

    nodes = []
    cnt = 0

    for server in servers:
        done = 0
        while done < per_server_nodes and cnt < n:
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
    return nodes

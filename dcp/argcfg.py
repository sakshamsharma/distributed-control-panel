#!/usr/bin/env python3

import argparse


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cfg',
                        help='config file containing configuration',
                        required=True)
    parser.add_argument('--nodes',
                        help='filename containing node labels (one per line)'
                             'OR integer number of nodes to generate',
                        required=True)
    parser.add_argument('-e', '--edges', type=int,
                        help='number of edges (default is minimum possible)')
    parser.add_argument('-l', '--loops', action='store_true',
                        help='allow self-loop edges')
    parser.add_argument('-m', '--multigraph', action='store_true',
                        help='allow parallel edges between nodes')
    parser.add_argument('-d', '--digraph', action='store_true',
                        help='make edges unidirectional')
    parser.add_argument('-w', '--wilson', action='store_const',
                        const='wilsons_algo', dest='approach',
                        help="use wilson's generation algorithm (best)")
    parser.add_argument('-r', '--random-walk', action='store_const',
                        const='random_walk', dest='approach',
                        help='use random-walk generation algorithm (default)')
    parser.add_argument('-n', '--naive', action='store_const',
                        const='naive', dest='approach',
                        help='use a naive generation algorithm (slower)')
    parser.add_argument('-t', '--partition', action='store_const',
                        const='partition', dest='approach',
                        help='use partition-based generation algo (biased)')
    parser.add_argument('--no-output', action='store_true',
                        help='do not display any output')
    parser.add_argument('-p', '--pretty', action='store_true',
                        help='print large graphs with each edge on a new line')
    parser.add_argument('-g', '--gml',
                        help='filename to save the graph to in GML format')
    return parser


def get_args():
    return get_parser().parse_args()

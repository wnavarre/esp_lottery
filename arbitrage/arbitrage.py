"""
http://shriphani.com/blog/2010/07/02/bellman-ford-algorithms-applications-triangular-arbitrage/
"""

from bellman_ford import bellman_ford
from math import log
from collections import defaultdict
import sys

# ---------------------------------------------------------------------------- #

def find_path(predecessor,start,end):
    """ assumes path exists from start to end """
    path = []
    while True:
        path.append(end)
        if end == start:
            path.reverse()
            return path
        end = predecessor[end]

def negative_weight_cycle(predecessor,end):
    path = []
    while True:
        path.append(end)
        if path.count(end) > 1:
            path = path[path.index(end):]
            path.reverse()
            path = path[path.index(end):]
            return path 
        end = predecessor[end]


def find_cycle(graph):
    symbols = set()
    for i in graph:
        symbols.add(i)
        for j in graph[i]:
            symbols.add(j)

    for src in symbols:
        distances,predecessors,cycle_vertex = bellman_ford(graph,src)
        if cycle_vertex is not None:
            out = negative_weight_cycle(predecessors,cycle_vertex)
            return out

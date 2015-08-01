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

def find_negative_weight_cycle(graph):
    symbols = set()
    
    new_graph = {}
    #copy the references into a new dictionary.
    for k in graph:
        new_graph[k] = graph[k]
    graph = new_graph

    for src in graph:
        symbols.add(src)
        for dst in graph[src]:
            symbols.add(dst)
    

    # universal_source should have an arrow
    # going to all the other nodes in the graph. 
    universal_source = "UNIVERSAL_SOURCE"
    while universal_source in symbols: 
        universal_source = str(random.random())
    graph[universal_source] = {}
    for target in symbols:
        graph[universal_source][target] = 0
    
    try:
        distances,predecessors,cycle_vertex = bellman_ford(graph,universal_source)
        return negative_weight_cycle(predecessors,cycle_vertex)
    except NoCycle:
        pass

#!/usr/bin/env python3
import scipy

import matplotlib.pyplot as plt
"""

"""
import os
import networkx as nx
print(os.getcwd())
os.chdir("constraintProgramming_learn")

#extracting only 2000 nodes from entire metabolic stuff
def DONEnolongerneeded():
    """already generated metabolic network to search into"""
    f_ll = open("PP-Pathways_ppi.csv", "rt").readlines()
    allEdges = set()
    for line in f_ll:
        tup = tuple(int(i) for i in line.replace("\n","").split(","))
        if tup[0] > 2000 or tup[1] > 2000 : 
            continue
        else:
            allEdges.add(tup)
    ALLMETAB = nx.DiGraph()
    ALLMETAB.add_edges_from(list(allEdges))
    print(type((ALLMETAB.edges())))
    print(len(list((ALLMETAB.edges()))))
    print(len(list((ALLMETAB.nodes()))))
    #extract the nodes making part of the largest connected component:
    ho_l = max(nx.kosaraju_strongly_connected_components(ALLMETAB) ,key=len)
    print(type(ho_l))
    print(ho_l)
    SG = ALLMETAB.subgraph(ho_l)
    print(len(SG.nodes()))
    print(len(SG.edges()))
    print(nx.is_connected(SG.to_undirected()))
    return "done"

print(DONEnolongerneeded())
"""
paths_between_generator = nx.all_simple_paths(ALLMETAB,source=1, target=1500)
nodes_between_set = set()
for path in paths_between_generator:
    for node in path:
        nodes_between_set.add(node)
SG = ALLMETAB.subgraph(nodes_between_set)

print(SG.number_of_selfloops())
nx.draw(SG, node_size=1)
plt.savefig("bouh2.png")
"""
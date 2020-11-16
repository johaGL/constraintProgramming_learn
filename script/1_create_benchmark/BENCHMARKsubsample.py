#!/usr/bin/env python3
import matplotlib.pyplot as plt
"""
Generate json target-pattern files
Target  sizes : 20 30 50 100 150 .... 900 nodes
being pattern ~30%-20% of the target size
"""
import os
import networkx as nx
import json

print(os.getcwd())


#extracting only 900 nodes from entire metabolic stuff
def DONEnolongerneeded():
    """extracting a part of the metabolic network
       dataset from Stanford University
       output: a connected graph (contains loops, I verifyed)
       of 932 nodes, saved into json file. The BASE.
    """
    f_ll = open("PP-Pathways_ppi.csv", "rt").readlines()
    allEdges = set()
    for line in f_ll:
        tup = tuple(int(i) for i in line.replace("\n","").split(","))
        if tup[0] > 2500 or tup[1] > 2500 : 
            continue
        else:
            allEdges.add(tup)
    ALLMETAB = nx.DiGraph()
    ALLMETAB.add_edges_from(list(allEdges))
    print(len(list((ALLMETAB.edges()))))
    print(len(list((ALLMETAB.nodes()))))
    #extract the nodes making part of the largest connected component:
    ho_l = max(nx.kosaraju_strongly_connected_components(ALLMETAB) ,key=len)
    print(type(ho_l))
    SG = ALLMETAB.subgraph(ho_l)
    print(len(SG.nodes()))
    print(len(SG.edges()))
    print(nx.is_connected(SG.to_undirected())) #True, ok
    print(nx.is_directed(SG)) # , True ok
    EDGEStxt = ", ".join(list(str(list(tu)) for tu in SG.edges()))
    textjson = '{"nodes": '+str(len(SG.nodes()))+ ', "edges": ['+EDGEStxt+']}'
    with open("METABO.jsonlike","w") as p : 
        p.write(textjson)
        p.close()
    return "done"

# print(DONEnolongerneeded()) ## deactivated, its already done
"""
get the different json files
"""
#initial T target is 950 node sample metab:
data = "METABO.jsonlike"
with open(data) as json_data:
    data_dict = json.load(json_data)

T = nx.DiGraph()
for edge in data_dict['edges']:
        T.add_edge(edge[0],edge[1]) 
motif = nx.DiGraph()

#trick to make it work with benchmark:
Ttrans = nx.convert_node_labels_to_integers(T, first_label=0)
print(Ttrans.edges())
"""loop while:  Ttrans progressively diminishes"""
N = len(Ttrans.nodes())

#N -= 800
#tmpSUB = Ttrans.subgraph(list(Ttrans.nodes())[1:N])  #diminish size
#Ttrans = tmpSUB

while (N >= 15): 
    NBNODESMOTIF = int(len(Ttrans.nodes())*0.25)
    print(NBNODESMOTIF)
    sub_subnodes = list(Ttrans.nodes())[0:NBNODESMOTIF]
    motifo = Ttrans.subgraph(sub_subnodes)
    motif = nx.convert_node_labels_to_integers(motifo,first_label=0)
    FILENM = "Subisomorphism_METABO-"+str(len(Ttrans.nodes()))+".json"
    dico = {}
    dico["nPatternNodes"] = len(motif.nodes())
    dico["nTargetNodes"] = len(Ttrans.nodes())
    yy = [list(tu) for tu in motif.edges()]
    yy.sort()
    dico["patternEdges"] = yy
    zz = [list(tu) for tu in Ttrans.edges()]
    zz.sort()
    dico["targetEdges"] = zz
    with open("../../fichiers_json/SubisomorphismB_/"+ FILENM,"w") as p : 
        json.dump(dico,p)  
    N -= 15
    tmpSUB = Ttrans.subgraph(list(Ttrans.nodes())[1:N])  #diminish size
    Ttrans = nx.convert_node_labels_to_integers(tmpSUB,first_label=0)
   


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
#    EDGEStxt_T = ", ".join(list(str(list(tu)) for tu in Ttrans.edges()))
 #   EDGEStxt_m = ", ".join(list(str(list(tu)) for tu in motif.edges()))
    #textjson = '{"nPatternNodes": '+str(len(motif.nodes()))
    #textjson += ', "nTargetNodes": '+str(len(Ttrans.nodes()))
    #textjson += ', "patternEdges": ['+EDGEStxt_m+']'
    #textjson += ', "targetEdges": ['+EDGEStxt_T+']}'
    #print(textjson)

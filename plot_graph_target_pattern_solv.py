#!/usr/bin/env python
# coding: utf-8



import networkx as nx
import matplotlib.pyplot as plt
import json 

target=nx.Graph()
pattern=nx.Graph()


data="data/Subisomorphism_40_node_0.json"
result=""

with open(data) as json_data:
    data_dict = json.load(json_data)

pattern_label=[i for i in range(data_dict['nPatternNodes'])]  

for edge in data_dict['patternEdges']:
    pattern.add_edge(edge[0],edge[1])
pos_pattern = nx.spring_layout(pattern,k=1)

target_label=[i for i in range(data_dict['nTargetNodes'])]  

for edge in data_dict['targetEdges']:
    target.add_edge(edge[0],edge[1])
pos_target = nx.spring_layout(target,k=1)

#Liste récupérer par le solver

L="0 26 40 172 183 187 8 41 199 62 118 167 122 15 70 50 198 5 163 23 169 151 29 46 31 52 94 189 88 58 83 125 2 120 33 184 75 149 21 152"
L=L.split(" ")

subgraph_label=[i for i in range(data_dict['nTargetNodes'])]

for i in range(len(L)):
    L[i]=int(i)
print(L)    
for node in L:
    subgraph_label.remove(node)

i=0
for node in range(len(pos_pattern)):
    pos_pattern[i]=pos_target[int(L[node])]
    i=i+1


plt.figure()
plt.axis('off')

nx.draw_networkx_nodes(target, pos_target, node_color="blue",node_size=15, node_shape="o", nodelist=target_label )
#nx.draw_networkx_labels(target,pos,font_weight=800,font_color='black')
nx.draw_networkx_edges(target, pos_target, width=0.3)

plt.figure()
plt.axis('off')

nx.draw_networkx_nodes(pattern, pos_pattern, node_color="red",node_size=15, node_shape="o", nodelist=pattern_label )
#nx.draw_networkx_labels(pattern,pos,font_weight=800,font_color='black')
nx.draw_networkx_edges(pattern, pos_pattern, width=0.3)


plt.figure()
plt.axis('off')

nx.draw_networkx_nodes(target, pos_target, node_color="red",node_size=25, node_shape="o", nodelist=L )
nx.draw_networkx_nodes(target, pos_target , node_color="blue",node_size=15, node_shape="o", nodelist=subgraph_label )
#nx.draw_networkx_labels(target,pos,font_weight=800,font_color='black')
nx.draw_networkx_edges(target, pos_target, width=0.3)





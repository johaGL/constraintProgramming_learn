#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

d_stat={'nbnode_target':[],'nbnode_pattern':[],'ratioedge_target':[],'ratioedge_pattern':[]}

path="target_pattern/scalefree/"

for lettre in ["A","B","C","E","F"]:
    for i in range(1,20):
        if int(i) < 10:
            target=open(path+lettre+".0"+str(i)+"/target")
            pattern=open(path+lettre+".0"+str(i)+"/pattern")
        else:
            target=open(path+lettre+"."+str(i)+"/target")
            pattern=open(path+lettre+"."+str(i)+"/pattern")
        dico={"nPatternNodes":0,"nTargetNodes":0,"patternEdges":[],"targetEdges":[]}
        t=target.readline()
        t=t.strip()
        dico["nTargetNodes"]=int(t)
        node=0
        somme_edge_target=0
        for l in target:
            l=l.strip()
            ligne=l.split(" ")
            somme_edge_target+=int(ligne[0])
            for e in range(1,len(ligne)):
                if int(ligne[e]) > node:
                    edge=[node,int(ligne[e])]
                    dico["targetEdges"].append(edge)
            node+=1
        p=pattern.readline()
        p=p.strip()
        dico["nPatternNodes"]=int(p)
        node=0
        somme_edge_patern=0
        for l in pattern:
            l=l.strip()
            ligne=l.split(" ")
            somme_edge_patern+=int(ligne[0])
            for e in range(1,len(ligne)):
                if int(ligne[e]) > node:
                    edge=[node,int(ligne[e])]
                    dico["patternEdges"].append(edge)  
            node+=1
        d_stat["nbnode_target"].append(int(t))
        d_stat["nbnode_pattern"].append(int(p))
        d_stat["ratioedge_target"].append(somme_edge_target/int(t))
        d_stat["ratioedge_pattern"].append(somme_edge_patern/int(p))

        if int(i) < 10:
            with open('../../fichiers_json/Subisomorphism_/Subisomorphism_'+lettre+'-0'+str(i)+'.json', 'w') as outfile:
                json.dump(dico, outfile)
        else:
            with open('../../fichiers_json/Subisomorphism_/Subisomorphism_'+lettre+'-'+str(i)+'.json', 'w') as outfile:
                json.dump(dico, outfile)
path="target_pattern/si2_bvg_b03_200/si2_b03_m200.0"

for i in range(0,9):
    target=open(path+str(i)+"/target")
    pattern=open(path+str(i)+"/pattern")
    dico={"nPatternNodes":0,"nTargetNodes":0,"patternEdges":[],"targetEdges":[]}
    t=target.readline()
    t=t.strip()
    dico["nTargetNodes"]=int(t)
    node=0
    somme_edge_target=0
    for l in target:
        l=l.strip()
        ligne=l.split(" ")
        somme_edge_target+=int(ligne[0])
        for e in range(1,len(ligne)):
            if int(ligne[e]) > node:
                edge=[node,int(ligne[e])]
                dico["targetEdges"].append(edge)
        node+=1
    p=pattern.readline()
    p=p.strip()
    dico["nPatternNodes"]=int(p)
    node=0
    somme_edge_patern=0
    for l in pattern:
        l=l.strip()
        ligne=l.split(" ")
        somme_edge_patern+=int(ligne[0])
        for e in range(1,len(ligne)):
            if int(ligne[e]) > node:
                edge=[node,int(ligne[e])]
                dico["patternEdges"].append(edge)  
        node+=1
    d_stat["nbnode_target"].append(int(t))
    d_stat["nbnode_pattern"].append(int(p))
    d_stat["ratioedge_target"].append(somme_edge_target/int(t))
    d_stat["ratioedge_pattern"].append(somme_edge_patern/int(p))
    with open('../../fichiers_json/Subisomorphism_/Subisomorphism_40_node_'+str(i)+'.json', 'w') as outfile:
        json.dump(dico, outfile)
        
##make plot with stat node et edge
fig, (ax1,ax2) = plt.subplots(1,2)
params = {'legend.fontsize': 'x-large',
         'figure.figsize': (20, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
plt.suptitle('Benchmart Christine Solmon')
ax1.plot(d_stat['nbnode_target'],d_stat['nbnode_pattern'],'bo',)
ax1.set(xlabel='Number of node in target graph',ylabel='Number of node in pattern graph',)

ax2.plot(d_stat['ratioedge_target'],d_stat['ratioedge_pattern'],'bo',)
ax2.set(xlabel='Ratio number edge/number node  in target graph',ylabel='Ratio number edge/number node in pattern graph')
pylab.rcParams.update(params)

plt.savefig('../../plot/stat_benchmart1.png')
#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

import json, glob

path="../../fichiers_json/SubisomorphismB_/*"
files=glob.glob(path)
plot="../../plot/"
d_stat={'nbnode_target':[],'nbnode_pattern':[],'ratioedge_target':[],'ratioedge_pattern':[]}


for f in files:
    with open(f) as dico:
    	d=json.load(dico)
    d_stat['nbnode_target'].append(d['nTargetNodes'])
    d_stat['nbnode_pattern'].append(d['nPatternNodes'])
    c={key:0 for key in range(d['nTargetNodes']+1)}
    somme_t=0
    for edge in d['targetEdges']:
        c[edge[0]]+=1
        c[edge[1]]+=1
    for n in c:
        somme_t+=c[n]
    d_stat['ratioedge_target'].append(somme_t/d['nTargetNodes'])
    c={key:0 for key in range(d['nPatternNodes']+1) }
    somme_t=0
    for edge in d['patternEdges']:
        c[edge[0]]+=1
        c[edge[1]]+=1
    for n in c:
        somme_t+=c[n]
    d_stat['ratioedge_pattern'].append(somme_t/d['nPatternNodes'])
    
fig, (ax1,ax2) = plt.subplots(1,2)
params = {'legend.fontsize': 'x-large',
         'figure.figsize': (20, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
plt.suptitle('Benchmart Réseau Protéine-Protéine',fontsize=20)
ax1.plot(d_stat['nbnode_target'],d_stat['nbnode_pattern'],'bo',)
ax1.set(xlabel='Number of node in target graph',ylabel='Number of node in pattern graph')


ax2.plot(d_stat['ratioedge_target'],d_stat['ratioedge_pattern'],'bo',)
ax2.set(xlabel='Ratio number edge/number node  in target graph',ylabel='Ratio number edge/number node in pattern graph')
pylab.rcParams.update(params)

plt.savefig(plot+'stat_benchmart2.png')
    
        
    

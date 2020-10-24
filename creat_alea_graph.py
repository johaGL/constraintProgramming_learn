#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import string

import pygraphviz as pgv #https://bioinfo-fr.net/python-dessine-moi-un-graphe

def graph_alea(N,proba):
    N=N
    node=set()
    letters=[i for i in string.ascii_letters]
    while len(node) < N:
        l=random.sample(letters,1)
        number=str(random.randint(1,100))
        node.add(l[0]+number)
    d={}
    for i in node:
        d[i]=[]
    for n in node:
        if len(d[n])<N/4:
            nb_edge=random.randint(len(d[n]),int(N*proba))
        else:
            continue
        neighbor_l=[]
        for i in d:
            if len(d[i]) < N/4:
                neighbor_l.append(i)
        for i in range(nb_edge):
            neighbor=neighbor_l.pop(random.randint(0,len(neighbor_l)-1))
            d[n].append((n,neighbor))
            if n != neighbor:
                d[neighbor].append((n,neighbor))
    return(d)
def graph_alea_number(N,proba):
    N=N
    node=[i for i in range(0,N)]
    d={}
    for i in node:
        d[i]=[]
    for n in node:
        if len(d[n])<N/4:
            nb_edge=random.randint(len(d[n]),int(N*proba))
        else:
            continue
        neighbor_l=[]
        for i in d:
            if len(d[i]) < N/4:
                neighbor_l.append(i)
        for i in range(nb_edge):
            neighbor=neighbor_l.pop(random.randint(0,len(neighbor_l)-1))
            d[n].append((n,neighbor))
            if n != neighbor:
                d[neighbor].append((n,neighbor))
    M=[[0 for n in range(0,N+1)] for i in range(0,N+1)]
    for l in d.values():
        for t in l:
            M[t[0]][t[1]]=1
    return(M)

def write_matrix_file(M):
    f=open("data/big_graph.txt",'w')
    N=len(M[0])-1
    print(N)
    for i in range(N):
        for j in range(N-1):
            f.write(str(M[i][j])+'\t')
        f.write(str(M[i][N])+'\n')

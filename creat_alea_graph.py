#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import string
N=8
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
        nb_edge=random.randint(len(d[n]),int(N/4))
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
print(d)
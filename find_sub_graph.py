#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from creat_alea_graph import *
from Numberjack import *
import string
import numpy

#node = Variable(graph.keys())
def get_model(N, n,proba, clues):
    matrice=Matrix(N, N, 0,(N*proba))
    #print(matrice)
    sub_graph=graph_alea_number(n,1/2)
    sub_matrice=Matrix(sub_graph)
    model=Model([(x == int(v)) for x, v in zip(matrice.flat, "".join(open(clues)).split())],
                [matrice[x:x+n,y:y+n] == sub_graph
                for x in range(0,N,1)
                for y in range (0,N,1)],
                )
    return(matrice,model)

def solve(param):
    N = param['N']
    n= param['n']
    proba= param['proba']
    graph=graph_alea_number(N,proba)
    write_matrix_file(graph)
    clues=param['file']

    matrice, model = get_model(N, n ,proba, clues)

    solver = model.load(param['solver'])
    solver.setVerbosity(param['verbose'])
    solver.setTimeLimit(param['tcutoff'])

    solver.solve()
    out = ""
    if solver.is_sat():
        out = True
    else:
        out = False

    return out



default = {'N': 10, 'n' : 4,'proba': 1/4, 'solver': 'Mistral', 'verbose': 0, 'tcutoff': 30,'file': 'data/big_graph.txt'}


if __name__ == '__main__':
    param = input(default)
    print(solve(param))




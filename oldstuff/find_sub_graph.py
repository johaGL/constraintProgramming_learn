#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from creat_alea_graph import *
from Numberjack import *
import string
import numpy

#node = Variable(graph.keys())
def get_model(N, n,proba, clues):
    graph=graph_alea_number(N,proba)
    matrice=Matrix(graph)
    #print(matrice)
    sub_graph=graph_alea_number(n,1/2)
    sub_matrice=Matrix(sub_graph)
    """
    list_sum=[]
    for i in range(n):
        sum=0
        for j in range(n):
            sum+=sub_graph[i][j]
        list_sum.append(sum)
    """    
    
    solv=Matrix(n+1,n+1,0,N) # matrice resultat with ligne 0 et col 0 == node big graph,
    model=Model(solv[0][0] == -1,
                [AllDiff(row) for row in solv.row]) #all node is different
    for i in range(1,n+1):
        model.add(solv[0][i]==solv[i][0]) #node ligne 0 et col 0 equal
    for i in range(1,n):
        for j in range(2,n+1):  # Contraite des arcs , pas de contrainte en col 1 et ligne n+1
            model.add(matrice[solv[0][j]][solv[i][0]] == sub_matrice[i-1][j-1])
        

    #toujours pas bon il faut remplir solv avec les .add            

    return(solv,model)

def solve(param):
    N = param['N']
    n= param['n']
    proba= param['proba']
    graph=graph_alea_number(N,proba)
    write_matrix_file(graph)
    clues=param['file']

    solv, model = get_model(N, n ,proba, clues)

    solver = model.load(param['solver'])
    solver.setVerbosity(param['verbose'])
    solver.setTimeLimit(param['tcutoff'])

    solver.solve()
    out = ""
    if solver.is_sat():
        out = solv
    else:
        out = False

    return out



default = {'N': 10, 'n' : 4,'proba': 1/4, 'solver': 'Mistral', 'verbose': 0, 'tcutoff': 30,'file': 'data/big_graph.txt'}


if __name__ == '__main__':
    param = input(default)
    print(solve(param))




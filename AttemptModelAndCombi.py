from Numberjack import *
import itertools
import math
import os
import string
"""
les variables de classe Numberjack ont suffix 'Var'
"""
#cdir = os.getcwd()
# THE SPACE
os.chdir("constraintProgramming_learn")
filespace = open("data/big_graph2.txt", 'rt').readlines()
space = [[ int(k) for k in li.replace('\n','').strip().split('\t')] for li in filespace ]
spacex = Matrix(space)
print(f'espace de recherche, {int(math.sqrt(len(spacex.flat)))} nodes, en matadjacence')
matchesVar = VarArray([], 0, int(math.sqrt(len(spacex.flat))))

"""
ATTENTIOn on a mis cette matrice 'space' comme ça mais il faut
reflechir a une methode: existe-t-il une logique (?) qui
réglemente l'ordre des sommets pour la construction de la matrice d'adjacence ?*
( * question pour l'espace de recherche et aussi pour le motif a rechercher).
**Solution proposée ici pour le motif: toutes les possibles matrices introduites
"""
# THE MOTIF
motif = { 'nodes' : ['h', 'f', 'g'], 'arrows' : [('h','h'), ('f','h'), ('g','f'), ('f','g')]}
print(f'voici le motif à chercher{motif}')
combimotifthatmatchVar = VarArray([], motif['nodes']) #domain is nodes in query

# DECLARE COMBINATORIAL QUESTION:
#combinatorial problem: n! possible adjacency matrices for this motif graph!
def domatrixinthisorder(permnodes_l, listofarrows):
    #permnodes_l =  ['g', 'h', 'f']
    N = len(permnodes_l)
    motifmat = [[ 0 for i in range(N)]for i in range(N)]
    for i in range(N):
        for j in range(N):
            #if (permnodes_l[i],permnodes_l[j]) in motif['arrows'] :
            if (permnodes_l[i],permnodes_l[j]) in listofarrows :
                motifmat[i][j] = 1
    return motifmat
combimotifdict = { }  # stock respective matrices (one for each nodes permutation)
# mais le dictionnaire n'est pas une variable reconue par Numberjack
# on fera listes ***: 
motifpermVar = VarArray([]) # du motif
permusmotifnodes = list(itertools.permutations(motif['nodes']))
for permnodes_l in permusmotifnodes:
    tmpmatrix = domatrixinthisorder(permnodes_l, motif['arrows'])  
    combimotifdict[permnodes_l] = tmpmatrix
    motifpermVar.append([permnodes_l, Matrix(tmpmatrix)])
print(f'possibles matrices adjacence pour le motif : {len(motifpermVar)}')

# exploring all possible as said in **
# organize the search in space: slicing submatrices:
N = len(motif['nodes'])
P = len(space[0]) # 7 for this mini-exemple
listmatchesindexes = []
model = Model()
for i in range(P-N+1):
    for j in range(P-N+1):  # cette fois ci "à la volée" car en mémoire is bad
        #model.add(  # FAILED CODE STRUCTURE TO DEFINE THIS !!!
        subspace = Matrix([[space[m][n] for n in range(j,j+N)] for m in range(i,i+N)])
        for motif in motifpermVar:
            if motif[1].__repr__() == subspace.__repr__():
                print("FOUND!")
                combimotifthatmatchVar.append(motif[0])
                matchesVar.append((i,j))
                listmatchesindexes.append((i,j))
            else:
                continue

print(matchesVar)   
print(combimotifthatmatchVar)      

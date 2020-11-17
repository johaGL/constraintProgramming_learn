#!/usr/bin/env python3
# coding: utf-8
"""
code  a changé
car on va inclure pour le meme jeu donnes
des resultats avec et sans DIRECTION des arcs
"""
import os
import glob
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.express as px
import pandas as pandas
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

os.chdir(os.getcwd())

outputARC = "../../résultat/BENCHMARKoutput_arcB.txt" 
outputNOARC = "../../résultat/BENCHMARKoutputB.txt"

f_o_d = "../../plot/"

"""
2. prendre les resultats du solveur pour les 95 cas d'isomorphisme
"""
#reformatting results into dictionnary, voir en bas la forme du texte
# quelques fichiers -00.xml ont ete inclus par erreur on va les filtrer etape 3
def yieldbenchdico(filesolverstats):
    benchdico = {}
    benchlines = open(filesolverstats,'rt').readlines()
    for line in benchlines:
        if line.startswith("BENCHMARK"):
            tmp = {}
            name = line.split("/")[-1].replace("Subisomorphism-","").split(".")[0]
            tmp["file"] = name
        elif line.startswith(" s") or line.startswith("\ts"):
            tmp["SS"] = str(line.split(" ")[-1].replace("\n",""))
        elif line.startswith(" d") or line.startswith("\td"):
            if "RUNTIME" in line:
                tmp["RUNTIME"] = float(line.split(" ")[-1].replace("\n",""))
            elif "MEMORY" in line:
                tmp["MEMORY"] = float(line.split(" ")[-1].replace("\n",""))
            elif "VARIABLES" in line:
                tmp["VARIABLES"] = int(line.split(" ")[-1].replace("\n",""))
            elif "CONSTRAINTS" in line:
                tmp["CONSTRAINTS"] = int(line.split(" ")[-1].replace("\n",""))
            elif "RESTARTS" in line:
                tmp["RESTARTS"] = int(line.split(" ")[-1].replace("\n",""))
            elif "BACKTRACKS" in line:
                tmp["BACKTRACKS"] = int(line.split(" ")[-1].replace("\n",""))
            elif "PROPAGATIONS" in line:
                tmp["PROPAGATIONS"] = float(line.split(" ")[-1].replace("\n",""))
            elif "ARITY" in line:
                tmp["ARITY"] = int(line.split(" ")[-1].replace("\n",""))
        benchdico[name] = tmp
    return(benchdico)

benchdicoARC = yieldbenchdico(outputARC)
benchdicoNOARC = yieldbenchdico(outputNOARC)

print(benchdicoARC['Subisomorphism_METABO-111'])
print(benchdicoNOARC['Subisomorphism_METABO-111']) 
print("end dictionnaire benchmark")

"""
3. figures
"""
CATEGORIE = []
SATISFIABLE = []
RUNTIME = []
VARIABLES = []
CONSTRAINTS = []
MEMORY = []
RESTARTS= []
BACKTRACKS = []
PROPAGATIONS = []

CATEGORIE_arc = []
SATISFIABLE_arc = []
RUNTIME_arc = []
VARIABLES_arc = []
CONSTRAINTS_arc = []
MEMORY_arc = []
RESTARTS_arc = []
BACKTRACKS_arc = []
PROPAGATIONS_arc = []

# ON VA INCLURE SATISFIABLE ET NON SATISFIABLE ! 
#commonkeys = [key for key in benchdicoNOARC.keys() if key in benchdicoARC.keys()]

for key in benchdicoNOARC.keys():
    if len(benchdicoNOARC[key]) > 1 :
        CATEGORIE.append("NOARC") 
        SATISFIABLE.append(benchdicoNOARC[key]["SS"])
        VARIABLES.append(benchdicoNOARC[key]["VARIABLES"])
        RUNTIME.append(benchdicoNOARC[key]["RUNTIME"])
        CONSTRAINTS.append(benchdicoNOARC[key]["CONSTRAINTS"]) #is the same as EDGESMOTIF+2
        MEMORY.append(benchdicoNOARC[key]["MEMORY"])
        RESTARTS.append(benchdicoNOARC[key]["RESTARTS"])
        BACKTRACKS.append(benchdicoNOARC[key]["BACKTRACKS"])
        PROPAGATIONS.append(benchdicoNOARC[key]["PROPAGATIONS"])

for key in benchdicoARC.keys():
    if len(benchdicoARC[key]) > 1 :
        CATEGORIE_arc.append("ARC")
        SATISFIABLE_arc.append(benchdicoARC[key]["SS"])
        VARIABLES_arc.append(benchdicoARC[key]["VARIABLES"])
        RUNTIME_arc.append(benchdicoARC[key]["RUNTIME"])
        CONSTRAINTS_arc.append(benchdicoARC[key]["CONSTRAINTS"]) #is the same as EDGESMOTIF+2
        MEMORY_arc.append(benchdicoARC[key]["MEMORY"])
        RESTARTS_arc.append(benchdicoARC[key]["RESTARTS"])
        BACKTRACKS_arc.append(benchdicoARC[key]["BACKTRACKS"])
        PROPAGATIONS_arc.append(benchdicoARC[key]["PROPAGATIONS"])

print("instances 'satisfiables' selon type de contrainte (txt): ")
print("avec arc ==>" +str(len(SATISFIABLE))  + "/" +str(len(benchdicoARC)))
print("sans arc ==>" +str(len(SATISFIABLE_arc))+"/" +str(len(benchdicoNOARC)))

"""       
print(len(CATEGORIE))
print(len(SATISFIABLE))
print(len(VARIABLES))
print(len(CATEGORIE_arc))
print(len(SATISFIABLE_arc))
print(len(VARIABLES_arc))
"""
fig = plt.figure()
fig.suptitle('Temps de calcul en fonction des contraintes et Type')
plt.scatter(CONSTRAINTS_arc,RUNTIME_arc, c="tomato", label="arc_orienté")
plt.scatter(CONSTRAINTS, RUNTIME, c="lightblue", label="non_orienté")
plt.xlabel("Contraintes (n)")
plt.ylabel("Temps (s)")
plt.legend()
fig.savefig(f_o_d+'BENCHMARK_arcVSnonarc_t.jpg')

fig = plt.figure()
fig.suptitle('Ressources en fonction des contraintes et Type')
plt.scatter(CONSTRAINTS_arc, MEMORY_arc, c="tomato", label="arc_orienté")
plt.scatter(CONSTRAINTS, MEMORY, c="lightblue", label="non_orienté")
plt.xlabel("Contraintes (n)")
plt.ylabel("Ressources Mémoire (Mib)")
plt.legend()
fig.savefig(f_o_d+'BENCHMARK_arcVSnonarc_memo.jpg')

fig = plt.figure()
fig.suptitle('Ressources en fonction des variables et Type contrainte')
plt.scatter(VARIABLES_arc, MEMORY_arc, c="darkcyan", label="arc_orienté")
plt.scatter(VARIABLES, MEMORY, c="blueviolet", label="non_orienté")
plt.xlabel("Variables (n)")
plt.ylabel("Ressources Mémoire (Mib)")
plt.legend()
fig.savefig(f_o_d+'BENCHMARK_arcVSnonarc_memVAR.jpg')

fig = plt.figure()
fig.suptitle('Temps en fonction des variables et Type contrainte')
plt.scatter(VARIABLES_arc, RUNTIME_arc, c="darkcyan", label="arc_orienté")
plt.scatter(VARIABLES, RUNTIME, c="blueviolet", label="non_orienté")
plt.xlabel("Variables (n)")
plt.ylabel("Temps (s)")
plt.legend()
fig.savefig(f_o_d+'BENCHMARK_arcVSnonarc_memVt.jpg')

""" INUTILE, CEST TOUT SATISFIABLE CAR LA TAILLE DE SUBDICTIOS > 1
def getnum(mysatvector):
    tmp = []
    for elem in mysatvector:
        if elem == "SATISFIABLE":
            tmp.append(1)
        else:
            tmp.append(0)
    return tmp
print(getnum(SATISFIABLE_arc))
print(getnum(SATISFIABLE))
"""




 


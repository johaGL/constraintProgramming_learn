#!/usr/bin/env python3
# coding: utf-8
"""
code  a changé
car on va inclure pour le meme jeu donnes
des resultats avec et sans arc
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
commonkeys = [key for key in benchdicoNOARC.keys() if key in benchdicoARC.keys()]

for key in commonkeys:
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


"""
fig = plt.figure()
x = np.array(RATIO_TG)
y = np.array(RUNTIME)
fig.suptitle('Temps de calcul en fonction du ratio nbArêtes/nbNodes du Target')
plt.scatter(x,y, c="coral")
plt.xlabel("ratio nbArêtes/nbNodes in Target")
plt.ylabel("Temps (s)")
fig.savefig(f_o_d+'BENCHMARK_seulTarget.jpg')

fig = plt.figure()
x = np.divide( (np.divide(RATIO_MOTIF, RATIO_TG)) ,np.array(CONSTRAINTS))
y = np.array(MEMORY)
fig.suptitle('Ressources en fonction des tailles relatives motif/target')
plt.scatter(x,y, c="darkviolet")
plt.xlabel("NbAretes/Nbnoeuds Motif / NbAretes/Nbnoeuds Target")
plt.ylabel("Ressources Mémoire (Gb)")
fig.savefig(f_o_d+'BENCHMARKfigratioderatio.jpg')

fig = plt.figure()
x = np.array(EDGESMOTIF)
y = np.array(MEMORY)
colorcat = []
for i in range(len(EDGESMOTIF)):
    tmp = EDGESMOTIF[i] / EDGESTG[i]
    if tmp < 0.1:
        colorcat.append("black")
    elif  tmp >= 0.1 and tmp <= 0.3:
        colorcat.append("indigo")
    elif tmp > 0.3 and tmp < 0.8:
        colorcat.append("gray") #un seul point gray en tout cas
    else: colorcat.append("royalblue")
fig.suptitle('Ressources en fonction des tailles relatives motif/target')
plt.scatter(x,y, c=colorcat)
patch1 = mpatches.Patch(color="indigo", label="0.1-0.3 du target")
patch2 = mpatches.Patch(color="royalblue", label="0.8-0.9 du target")
plt.legend(handles=[patch1,patch2])
plt.xlabel("Nb arêtes du motif")
plt.ylabel("Ressources Mémoire (Mib)")
fig.savefig(f_o_d+'BENCHMARK_Var_Space.jpg')

#special color map with plotly and pandas (this shows in browser directly):
rapportNEW = list(np.divide(CONSTRAINTS, NODESMOTIF))
print(rapportNEW)
minidico = {  "nb Nodes target" : NODESTG, "runtime (s)" : RUNTIME, \
    "Rapport nb Contraintes/nb Variables" : rapportNEW,\
        "nb Nodes motif" : NODESMOTIF}
df = pandas.DataFrame(minidico, columns = ["nb Nodes target", "runtime (s)", \
    "Rapport nb Contraintes/nb Variables", "nb Nodes motif"])
fig = px.scatter(df, x="Rapport nb Contraintes/nb Variables", y="runtime (s)", color="nb Nodes target",\
     color_continuous_scale=px.colors.sequential.Inferno, size="nb Nodes motif")
fig.show() #see browser !! 

 
ratioEdgesConstraints = np.divide(EDGESMOTIF,CONSTRAINTS)
fig = plt.figure()
x = ratioEdgesConstraints
y = np.array(RUNTIME)
fig.suptitle('Temps de calcul en fonction du ratio nb Arêtes_Motif/Contraintes')
plt.scatter(x,y, c="darkgreen")
plt.xlabel("Ratio nb Arêtes_Motif/Contraintes")
plt.ylabel("Temps (s)")
fig.savefig(f_o_d+'BENCHMARK_.jpg')
"""


 


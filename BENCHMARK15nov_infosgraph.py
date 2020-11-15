#!/usr/bin/env python3
# coding: utf-8
"""
code pour 
Obtenir des infos pour creer des figures: RUNTIME vs nbcontraintes, etc 
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

os.chdir("constraintProgramming_learn/")
cwd = os.getcwd() #expected location: ~/constraintProgramming_learn
print(cwd)
dir_jsons = "Subisomorphism_/"
dir_jsons_B = "SubisomorphismB_/"
filesolverstats = "BENCHMARK_OUTPUTMERGED.txt"  #prendre les resultats du solveur pour les 95 cas d'isomorphisme
jsonfiles = glob.glob(os.path.join(dir_jsons,"*.json"))
jsonfilesB = glob.glob(os.path.join(dir_jsons_B,"*.json"))
f_o_d = "BENCHMARK15nov_Figures/"
"""
1. prendre des ratios edges/nodes target et motif
"""
# dictionnary containing as key the file name as "Subisomorphism_E-01" :no extension 
def yielddico(filespathlist):
    dico = {}
    for jsonf in filespathlist:
        tmp = []
        with open(jsonf) as json_data:
            name = jsonf.split("/")[-1].split(".")[0]
            data_dict = json.load(json_data)
            bigG_nbedges = len(data_dict['targetEdges'])
            bigG_nbnodes = data_dict['nTargetNodes']
            motifnbedges = len(data_dict['patternEdges'])
            motifnbnodes = data_dict['nPatternNodes']
        dico[name] = {"file": name,"RATIO_TG": bigG_nbedges/bigG_nbnodes, "RATIO_MOTIF": motifnbedges/motifnbnodes, \
                        "NODESTG": bigG_nbnodes, "NODESMOTIF": motifnbnodes, \
                            "EDGESTG": bigG_nbedges , "EDGESMOTIF" : motifnbedges }
    return(dico)
        #print([name, bigG_nbedges/bigG_nbnodes, motifnbedges/motifnbnodes])

dico = yielddico(jsonfiles)
dicoB = yielddico(jsonfilesB)
dico.update(dicoB)
print("end dictionnaire ratios origine. Note: dico contanins also dicoB info!")
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

benchdico = yieldbenchdico(filesolverstats)
print(benchdico['Subisomorphism_A-08']) # dictio ok : {'file': 'Subisomorphism_A-08', 'SS': 'SATISFIABLE', 'RUNTIME': '0.07', 'MEMORY': '121.74', 'RESTARTS': '1', 'BACKTRACKS': '11', 'PROPAGATIONS': '8578', 'CONSTRAINTS': '493', 'ARITY': '180'}
print(benchdico['Subisomorphism_METABO-271']) 
print("end dictionnaire benchmark")

"""
3. explorer uniquement satisfiables!  et faire figures
"""
NODESTG = []
NODESMOTIF = []
EDGESTG = []
EDGESMOTIF = []
RATIO_TG = []
RATIO_MOTIF = []
RUNTIME = []
CONSTRAINTS = []
MEMORY = []
RESTARTS= []
BACKTRACKS = []
PROPAGATIONS = []

for key in benchdico.keys():
    if key in dico.keys() and benchdico[key].get("SS") == "SATISFIABLE":
        #print(dico[key])
        #print(benchdico[key])
        #INFOS FROM DICO
        NODESTG.append(dico[key]["NODESTG"])
        NODESMOTIF.append(dico[key]["NODESMOTIF"])
        EDGESTG.append(dico[key]["EDGESTG"])
        EDGESMOTIF.append(dico[key]["EDGESMOTIF"])
        RATIO_TG.append(dico[key]["RATIO_TG"])
        RATIO_MOTIF.append(dico[key]["RATIO_MOTIF"])
        #INFOS FROM BENCHDICO
        RUNTIME.append(benchdico[key]["RUNTIME"])
        CONSTRAINTS.append(benchdico[key]["CONSTRAINTS"]) #is the same as EDGESMOTIF+2
        MEMORY.append(benchdico[key]["MEMORY"])
        RESTARTS.append(benchdico[key]["RESTARTS"])
        BACKTRACKS.append(benchdico[key]["BACKTRACKS"])
        PROPAGATIONS.append(benchdico[key]["PROPAGATIONS"])
  
"""
fig = plt.figure()
fig.suptitle('Temps de calcul en fonction nb variables et nb contraintes')
ax = fig.add_subplot(111,projection='3d')
x = np.array(NODESMOTIF)
y = np.array(CONSTRAINTS)
z = np.array(RUNTIME)
ax.scatter(x,y,z)
ax.set_xlabel("Variables (nb nodesMotif)")
ax.set_ylabel("Contraintes (n)")
ax.set_zlabel("runtime (s)")
plt.show()
#fig.savefig(f_o_d+'BENCHMARK_Var_Cnt.jpg')


fig = plt.figure()
x = np.array(RATIO_MOTIF)
y = np.array(RUNTIME)
fig.suptitle('Temps de calcul en fonction du ratio nbArêtes/nbNodes du Motif')
plt.scatter(x,y, c="coral")
plt.xlabel("ratio nbArêtes/nbNodes in Motif")
plt.ylabel("Temps (s)")
fig.savefig(f_o_d+'BENCHMARK_seulMotif.jpg')

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
plt.ylabel("Ressources Mémoire (Gb)")
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
"""
 
ratioEdgesConstraints = np.divide(EDGESMOTIF,CONSTRAINTS)
fig = plt.figure()
x = ratioEdgesConstraints
y = np.array(RUNTIME)
fig.suptitle('Temps de calcul en fonction du ratio nb Arêtes_Motif/Contraintes')
plt.scatter(x,y, c="darkgreen")
plt.xlabel("Ratio nb Arêtes_Motif/Contraintes")
plt.ylabel("Temps (s)")
fig.savefig(f_o_d+'BENCHMARK_.jpg')



 
""" forme du texte :
BENCHMARKdata/Subisomorphism-Subisomorphism_A-08.xml 
c Mistral 16062018
 c +===========================================+
 c |       12        8578     0.07 |       180 | 
 c +===========================================+
 c +========================================================================================+
 s                                                                               SATISFIABLE
 v                                                                                        1
 d  MAXDEPTH                                                                            180
 d  SUCCESS                                                                               1
 d  RUNTIME                                                                            0.07
 d  PREPROCTIME                                                                         0.1
 d  MEMORY                                                                           121.74
 d  NODES                                                                                12
 d  RESTARTS                                                                              1
 d  FAILURES                                                                             11
 d  BACKTRACKS                                                                           11
 d  PROPAGATIONS                                                                       8578
 d  VARIABLES                                                                           180
 d  CONSTRAINTS                                                                         493
 d  ARITY                                                                               180
 d  WEAKDEC                                                                               0
 c +========================================================================================+
v <instantiation type="solution">
v   <list> x[0] x[1] x[2] x[3] x[4] x[5] x[6] x[7] x[8] x[9] x[10] x[11] x[12] x[13] x[14] x[15] x[16] x[17] x[18] x[19] x[20] x[21] x[22] x[23] x[24] x[25] x[26] x[27] x[28] x[29] x[30] x[31] x[32] x[33] x[34] x[35] x[36] x[37] x[38] x[39] x[40] x[41] x[42] x[43] x[44] x[45] x[46] x[47] x[48] x[49] x[50] x[51] x[52] x[53] x[54] x[55] x[56] x[57] x[58] x[59] x[60] x[61] x[62] x[63] x[64] x[65] x[66] x[67] x[68] x[69] x[70] x[71] x[72] x[73] x[74] x[75] x[76] x[77] x[78] x[79] x[80] x[81] x[82] x[83] x[84] x[85] x[86] x[87] x[88] x[89] x[90] x[91] x[92] x[93] x[94] x[95] x[96] x[97] x[98] x[99] x[100] x[101] x[102] x[103] x[104] x[105] x[106] x[107] x[108] x[109] x[110] x[111] x[112] x[113] x[114] x[115] x[116] x[117] x[118] x[119] x[120] x[121] x[122] x[123] x[124] x[125] x[126] x[127] x[128] x[129] x[130] x[131] x[132] x[133] x[134] x[135] x[136] x[137] x[138] x[139] x[140] x[141] x[142] x[143] x[144] x[145] x[146] x[147] x[148] x[149] x[150] x[151] x[152] x[153] x[154] x[155] x[156] x[157] x[158] x[159] x[160] x[161] x[162] x[163] x[164] x[165] x[166] x[167] x[168] x[169] x[170] x[171] x[172] x[173] x[174] x[175] x[176] x[177] x[178] x[179] </list>
v   <values> 97 130 115 167 42 157 172 111 174 153 85 149 86 51 25 99 124 17 126 175 82 1 103 104 148 129 112 28 136 0 65 145 14 8 134 93 62 9 176 186 192 127 178 72 160 169 98 182 7 49 165 45 70 144 121 166 102 92 32 119 67 43 18 139 4 190 100 24 34 33 163 135 155 158 146 89 122 73 77 195 177 106 31 71 107 54 188 11 181 140 12 164 78 109 48 15 185 21 138 101 87 142 79 88 114 197 84 183 10 180 59 39 191 196 94 179 69 143 116 22 63 194 41 68 96 76 47 27 58 16 30 105 44 60 152 120 189 46 141 36 38 171 3 19 151 147 123 150 113 118 193 170 37 125 117 61 187 108 2 95 23 6 173 55 131 74 80 162 132 91 13 137 57 56 133 199 50 5 29 90 </values>
v </instantiation>
"""

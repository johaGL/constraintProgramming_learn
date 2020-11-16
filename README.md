# ISOMORPHISME DE SOUS-GRAPHE :
## Problématique :
- Trouver des sous graph (pattern) dans un graph (target)
- En Biologie par example, trouver des fonctions métaboliques connues dans un réseaux métabolique inconnus

## Benchmark :
- 1 Existant : http://perso.citi-lab.fr/csolnon/SIP.html
```
cd script/1_create_benchmark/
unzip target_pattern.zip
```
- 2 Générer : 
	- à partir d’un dataset SNAP d'interaction protéine-protéine humaine https://snap.stanford.edu/biodata/datasets/10000/10000-PP-Pathways.html (nommée PP-Pathways_ppi.csv)
	- puis Échantillonnage du dataset + création sous-graph avec networkx
	- benchmark généré dans fichiers_json/SubisomorphismB_/
```
cd script/1_create_benchmark/target_pattern.zip
./BENCHMARKsubsample.py
``` 
## Solvers :
- Mistral : https://github.com/ehebrard/Mistral-2.0/
- Abscon: https://www.cril.univ-artois.fr/~lecoutre/#/softwares

## Pipeline d'analyse :
- 1 Générer les instance du benchmarcks 1 en json 
```
cd script/1_create_benchmark/
./pattern_target_to_json.py
``` 
- 2 Générer les instances des benchmarks en XCSP3 
	- dans les dossiers BENCHMARKdata*/
- +les donners aux solveurs
	- résultats dans dossiers résultats
```
cd script/2_lancer_modelisation_solver/
./script_mistral.sh
#non effectué mais possible
./script_Abscon.sh
``` 
![pipeline_analyse]()

## Modèle :
- Générer dans script/2_lancer_modelisation_solver/Subisomorphism.py
	- modèle ici pour graph non orienté et degré des nodes targets < degré node pattern
	- pour graph orienté changé ligne 16 par : both_way_table = {(i, j) for (i, j) in t_edges} }
	- pour égalité des dégrés modifé ligne 17 par : degree_conflicts = [{j for j in range(m) if t_degrees[j] < p_degrees[i]} for i in range(n)]
* Aucune solution pour les 2 alternatives pour le Benchmark 1
* Benchmark 2 , solutions pour les graphs orientés

## Résultats / Statistique
-Résultats sous forme:
``` 
BENCHMARKdataB/Subisomorphism-Subisomorphism_METABO-111.xml
c Mistral 16062018
 c +===========================================+
 c |       37         469        0 |        27 | 
 c +===========================================+
 c +========================================================================================+
 s                                                                               SATISFIABLE
 v                                                                                        1
 d  MAXDEPTH                                                                             27
 d  SUCCESS                                                                               1
 d  RUNTIME                                                                               0
 d  PREPROCTIME                                                                           0
 d  MEMORY                                                                           18.961
 d  NODES                                                                                37
 d  RESTARTS                                                                              1
 d  FAILURES                                                                             12
 d  BACKTRACKS                                                                           36
 d  PROPAGATIONS                                                                        469
 d  VARIABLES                                                                            27
 d  CONSTRAINTS                                                                          39
 d  ARITY                                                                                27
 d  WEAKDEC                                                                              11
 c +========================================================================================+
v <instantiation type="solution">
v   <list> x[0] x[1] x[2] x[3] x[4] x[5] x[6] x[7] x[8] x[9] x[10] x[11] x[12] x[13] x[14] x[15] x[16] x[17] x[18] x[19] x[20] x[21] x[22] x[23] x[24] x[25] x[26] </list>
v   <values> 109 105 100 25 26 0 108 19 93 106 103 33 24 42 87 34 36 99 102 28 47 104 107 101 46 45 110 </values>
``` 


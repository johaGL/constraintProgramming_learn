/**
 * This piece of code(1) runs inside a cloned choco-graph repo;
 *  exact file path:
 *  src/test/java/org/chocosolver/gccprojectBIO/version1.java

 */

package org.chocosolver.gccprojectBIO;

import org.chocosolver.graphsolver.GraphModel;

import org.chocosolver.graphsolver.variables.DirectedGraphVar;
import org.chocosolver.solver.constraints.set.PropAllDiff;
import org.chocosolver.util.objects.graphs.DirectedGraph;
import org.chocosolver.util.objects.setDataStructures.SetType;


public class version1 {
	public static void main(String[] args) {
		//test premier, sur des petites instances:
		//A.  introducing instances: metabolic network and motif to search
		int M = 5;
		DirectedGraph metabonetwork = new DirectedGraph(M, SetType.BITSET, true);
		metabonetwork.addArc(0, 1);
		metabonetwork.addArc(1, 2);
		metabonetwork.addArc(2, 4);
		metabonetwork.addArc(3, 2);
		metabonetwork.addArc(4, 4);
		metabonetwork.addArc(3, 0);
		//System.out.println(metabonetwork);

		// TODO: here we have to implement a graph generator (different motif sizes to test)
		int n = 3;
		DirectedGraph motif = new DirectedGraph(n, SetType.BITSET, true);
		motif.addArc(1, 0);
		motif.addArc(2, 1);
		//System.out.println(motif);

		// B. define MODEL
		GraphModel model = new GraphModel();
		// add  initial domain
		DirectedGraph GUB = new DirectedGraph(model, M, SetType.BITSET, true);
		for (int i = 0; i < M; i++) {
			for (int j = 0; j < M; j++) {
				if (metabonetwork.arcExists(i, j)) {
					GUB.addArc(i, j);
				}
			}
		}
		DirectedGraph GLB = new DirectedGraph(model, n, SetType.BITSET, false);
		System.out.println("!!!!this print wshoud be empty graph!! : ");
		System.out.println(GLB);

		DirectedGraphVar FOUND = model.digraphVar("x", GLB, GUB);

		// C. ADDING.... THE CONSTRAINTS !!!!
		// 1st constraint: set number of nodes

		model.nbNodes(FOUND, model.intVar(n)).post();
		// 2nd constraint: set number of
		int n_edges = 0;
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				if (motif.arcExists(i, j)) {
					n_edges += 1;
				}
			}
		}
		model.nbArcs(FOUND, model.intVar(n_edges)).post();
		System.out.println(model);
	}
}



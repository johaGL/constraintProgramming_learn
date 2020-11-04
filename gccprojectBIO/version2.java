/**
 * This piece of code(1) runs inside a cloned choco-graph repo;
 *  exact file path:
 *  src/test/java/org/chocosolver/gccprojectBIO/version1.java
 */
import org.chocosolver.solver.Model;
import org.chocosolver.solver.Solver;
import org.chocosolver.solver.constraints.extension.Tuples;
import org.chocosolver.solver.variables.BoolVar;
import org.chocosolver.solver.variables.IntVar;
import org.chocosolver.util.objects.graphs.DirectedGraph;
import org.chocosolver.util.objects.setDataStructures.SetType;

//package org.chocosolver.gccprojectBIO;
/**
this is killing me. Version 2
 */
public class version2 {
    public static void main(String[] args) {
        //test premier, sur des petites instances:
        //A.  introducing instances: metabolic network and motif to search

        int M = 4;
        DirectedGraph metabonetwork = new DirectedGraph(M, SetType.BITSET, true);
        metabonetwork.addArc(0, 1);
        metabonetwork.addArc(1, 2);
        metabonetwork.addArc(2, 2);
        metabonetwork.addArc(2, 1);
        metabonetwork.addArc(2, 3);

        //System.out.println(metabonetwork);

        // TODO: here we have to implement a graph generator (different motif sizes to test)
        int n = 3;
        DirectedGraph motif = new DirectedGraph(n, SetType.BITSET, true);
        motif.addArc(0,1);
        motif.addArc(0,2);
        motif.addArc(0,0);

        Model model = new Model();
        IntVar[] SGMATCH = model.intVarArray("v", n, 0, M - 1);
        System.out.println(SGMATCH);

        //constraints
        model.allDifferent(SGMATCH).post();
        //new
        for (int k = 0; k < n; k++) {
            for (int h = 0; h < n; h++) {
                for (int i = 0; i < M; i++){
                    for (int j = 0; j < M; j++) {
                        // for k node, if loop in motif but not! in its "homolog" in network, thenexclude as i candidate
                        if ((i == j) & (k == h) ){
                            if ((motif.arcExists(k, h)) & !(metabonetwork.arcExists(i, j))) {
                                System.out.println("obligatory loop not met !");
                                model.arithm(SGMATCH[k], "!=", i).post();
                                } else {model.arithm(SGMATCH[k], "=", i).post();}
                        } //end loop constraint
                        if ((i != j) & (k !=h)) {//treat all the rest (no loops)
                            if (metabonetwork.arcExists(i, j) | metabonetwork.arcExists(j, i) ){
                                //detect conflict: a node in motif CANNOT have more suc/pred than its 'homolog' in network
                                if (motif.getPredOf(k).toArray().length < metabonetwork.getPredOf(i).toArray().length |
                                        motif.getSuccOf(k).toArray().length < metabonetwork.getSuccOf(i).toArray().length) {
                                    System.out.println("CONFLICT");
                                    model.arithm(SGMATCH[k], "!=",i).post();
                                } else {
                                    System.out.println("ALLOWED");
                                    model.arithm(SGMATCH[k], "=",i).post();
                                }
                            }
                        }
                    }//end for
                }//end for
                System.out.println("==========the unknown =====================");

            }//end for
        }//end for
        //end new
        // hey! i can use (j,i):the reverse way!

        System.out.println(model);
        Solver solver = model.getSolver();

        while (solver.solve()) {
            for (IntVar i : SGMATCH) {
                System.out.println("=== possible subgraph: ==");
                System.out.println(i);
            }

        }
        solver.printStatistics();
    }
}

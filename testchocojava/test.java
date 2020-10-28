// if automatically not set, do once : Ctr+Shift+p and set 'Configure Java Runtime: then edit.config/Code/User/settings.json'

import org.chocosolver.graphsolver.GraphModel;
import org.chocosolver.graphsolver.variables.DirectedGraphVar;
import org.chocosolver.solver.Model;
import org.chocosolver.solver.variables.IntVar;
import org.chocosolver.util.objects.graphs.DirectedGraph;
import org.chocosolver.util.objects.setDataStructures.SetType;
/**
 * each time to run do:
 * $ export CLASSPATH=$CLASSPATH:$HOME/constraintProgramming_learn/testchocojava/choco-solver-4.10.6-20201002.142745-1-jar-with-dependencies.jar
 *  and also chocograph:
 * $ export CLASSPATH=$CLASSPATH:$HOME/constraintProgramming_learn/testchocojava/choco-graph-4.2.3.jar
 */
public class test {
    public static void main(String[] args) {
        int m = 3;

        while (m > 0) {
            System.out.println("JUST PRINTING A NUMBER HERE");
            System.out.println(m);
            System.out.println("");
            m -= 1;
        }
        // model doesnt work, message error for ALL elements:
        //  cannot be resolved to a variable

        try{
            int n = 5;
            // VARIABLE COUNTING THE NUMBER OF ARCS
            GraphModel model = new GraphModel();
            IntVar nbArcs = model.intVar("arcCount", 0, n * n, true);
            // GRAPH VARIABLE : initial domain (every node belongs to the solution)
            DirectedGraph GLB = new DirectedGraph(model, n, SetType.BITSET, true);
            DirectedGraph GUB = new DirectedGraph(model, n, SetType.BITSET, true);
            GLB.addArc(0,1); // some arbitrary mandatory arcs
            GLB.addArc(1,2);
            GLB.addArc(3,1);
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    GUB.addArc(i, j);		// potential edge
                }
            }

            DirectedGraphVar dag = model.digraphVar("dag", GLB, GUB);

            // CONSTRAINTS
            model.noCircuit(dag).post();
            model.nbArcs(dag, nbArcs).post();

            model.setObjective(Model.MAXIMIZE,nbArcs);
            if (model.getSolver().solve()){
                System.out.println("solution found : "+nbArcs);
                System.out.println(dag.graphVizExport());
            }
            model.getSolver().printStatistics();

        } 
        catch (Exception e){
            System.out.println("MALDITO JAVA TE ODIO");
            System.out.println(e);
        }

    }
}



import java.util.ArrayList;
import java.util.Random;

public class Main {

    private static ArrayList<Integer> genRandomArray(int n) {
        ArrayList<Integer> arr = new ArrayList<>();
        Random rnd = new Random();
        for (int i = 0; i < n; i++) {
            int sign = rnd.nextInt(2);
            if (sign == 0) {
                sign = -1;
            }
            arr.add(sign * rnd.nextInt(100));
        }
        return arr;
    }

    private static ArrayList<Node> performBFS(Tree t, Node targetNode, boolean verbose) {
        System.out.println("\n\tBFS\n");
        System.out.println("\tTARGET:\n" + targetNode);
        ArrayList<Node> path = t.breadthFirstSearch(targetNode);
        if (path.size() == 0) {
            System.out.println("\n\tNO PATH FOUND");
        }
        else {
            System.out.println("\n\tPATH TO TARGET FOUND!");
        }
        if (verbose) {
            printPathHistory(path);
        }
        return path;
    }

    private static ArrayList<Node> performDFS(Tree t, Node targetNode, boolean verbose) {
        System.out.println("\n\tDFS\n");
        System.out.println("\tTARGET:\n" + targetNode);
        ArrayList<Node> path = t.depthFirstSearch(targetNode);
        if (path.size() == 0) {
            System.out.println("\n\tNO PATH FOUND");
        }
        else {
            System.out.println("\n\tPATH TO TARGET FOUND!");
        }
        if (verbose) {
            printPathHistory(path);
        }
        return path;
    }

    private static ArrayList<Node> performDLS(Tree t, Node targetNode, int dlsLimit, boolean verbose) {
        System.out.println("\n\tDLS\n" + "Limit:\t" + dlsLimit);
        System.out.println("\tTARGET:\n" + targetNode);
        ArrayList<Node> path = t.depthLimitedSearch(dlsLimit, targetNode);
        if (path.size() == 0) {
            System.out.println("\n\tNO PATH FOUND");
        }
        else {
            System.out.println("\n\tPATH TO TARGET FOUND!");
        }
        if (verbose) {
            printPathHistory(path);
        }
        return path;
    }

    private static ArrayList<Node> performIDS(Tree t, Node targetNode, boolean verbose) {
        System.out.println("\n\tIDS\n");
        System.out.println("\tTARGET:\n" + targetNode);
        ArrayList<Node> path = t.iterativeDepthLimitingSearch(targetNode);
        if (path.size() == 0) {
            System.out.println("\n\tNO PATH FOUND");
        }
        else {
            System.out.println("\n\tPATH TO TARGET FOUND!");
        }
        if (verbose) {
            printPathHistory(path);
        }
        return path;
    }

    private static void printPathHistory(ArrayList<Node> path) {
        if (path.size() > 0) {
            System.out.println("\n\tPATH:\n");
            for (Node visitedNode : path) {
                System.out.println(" -> " + visitedNode);
            }
                System.out.println("\n\tPATH.SIZE():\n" + path.size());
            System.out.println();
        }
    }

    private static MinMaxTree genMinMaxTree(int bF, int arrSize, int numNodes, boolean rootIsMaxNode) {
        ArrayList<Integer> arr = genRandomArray(arrSize);
        MinMaxTree t = new MinMaxTree(bF, arr, rootIsMaxNode);
        for (int i = 0; i < numNodes; i++) {
            double partA = Math.log(((bF - 1.0) * (i + 1)) + 1);
            double partB = Math.log(bF);
            double partC = ((partA - partB) / partB);
            int depth = (int) Math.ceil(partC);
//            System.out.println("A: " + partA + ", B: " + partB + ", C:" + partC + ", i: " + (i + 1) + ", depth: " + depth);
            arr = genRandomArray(arrSize);
            Node newNode;
            if (depth % 2 == 0) {
                if (rootIsMaxNode) {
                    newNode = new MaxNode(i + 2, bF, arr);
                } else {
                    newNode = new MinNode(i + 2, bF, arr);
                }
            } else {
                if (rootIsMaxNode) {
                    newNode = new MinNode(i + 2, bF, arr);
                } else {
                    newNode = new MaxNode(i + 2, bF, arr);
                }
            }
            t.addNodeToRoot(newNode);
//            arr = genRandomArray(10);
//            Node newNode = new Node(i + 1, bF, arr);
//            nodeStorage[i] = newNode;
//            addResult = t.addNodeToRoot(newNode);
//            // System.out.println("addResult:\t" + ((addResult)? "Successful" : "Failure") + "\n\n");
//            if (i == (numNodes - 2)) {
//                maxDepth = t.computeMaxDepth(newNode);
//            }
        }
        t.doMiniMax();
        t = t.pruneTree();
        return t;
    }

    // this makes one more node than i want it to
    private static MinMaxTree genMinMaxTreeFromArr(int bF, ArrayList<Integer> nums, boolean rootIsMaxNode) {
        ArrayList<ArrayList<Integer>> arr = new ArrayList<>();
        for (int num : nums) {
            ArrayList<Integer> n = new ArrayList<>();
            n.add(num);
            arr.add(n);
        }
        MinMaxTree t = new MinMaxTree(bF, arr.get(0), rootIsMaxNode);
        for (int i = 1; i < arr.size() - 1; i++) {
            double partA = Math.log(((bF - 1.0) * (i + 1)) + 1);
            double partB = Math.log(bF);
            double partC = ((partA - partB) / partB);
            int depth = (int) Math.ceil(partC);
//            System.out.println("A: " + partA + ", B: " + partB + ", C:" + partC + ", i: " + (i + 1) + ", depth: " + depth);
//            arr = genRandomArray(arrSize);
            Node newNode;
            if (depth % 2 == 0) {
                if (rootIsMaxNode) {
                    newNode = new MaxNode(i + 1, bF, arr.get(i));
                } else {
                    newNode = new MinNode(i + 1, bF, arr.get(i));
                }
            } else {
                if (rootIsMaxNode) {
                    newNode = new MinNode(i + 1, bF, arr.get(i));
                } else {
                    newNode = new MaxNode(i + 1, bF, arr.get(i));
                }
            }
            t.addNodeToRoot(newNode);
//            arr = genRandomArray(10);
//            Node newNode = new Node(i + 1, bF, arr);
//            nodeStorage[i] = newNode;
//            addResult = t.addNodeToRoot(newNode);
//            // System.out.println("addResult:\t" + ((addResult)? "Successful" : "Failure") + "\n\n");
//            if (i == (arr.size() - 2)) {
//                maxDepth = t.computeMaxDepth(newNode);
//            }
        }
        t.doMiniMax();
        t = t.pruneTree();
        return t;
    }

    private static Tree genTreeFromArr(int bF, ArrayList<Integer> nums) {
        ArrayList<ArrayList<Integer>> arr = new ArrayList<>();
        for (int num : nums) {
            ArrayList<Integer> n = new ArrayList<>();
            n.add(num);
            arr.add(n);
        }
        Tree t = new Tree(bF, arr.get(0));
        for (int i = 1; i < arr.size(); i++) {
//            arr = genRandomArray(10);
            Node newNode = new Node(i + 1, bF, arr.get(i));
            t.addNodeToRoot(newNode);
        }
        return t;
    }

    private static Tree genRandomTree(int bF, int arrSize, int numNodes) {
        ArrayList<Integer> arr = genRandomArray(arrSize);
        Tree t = new Tree(bF, arr);
        for (int i = 1; i < numNodes; i++) {
            arr = genRandomArray(10);
            Node newNode = new Node(i + 1, bF, arr);
            t.addNodeToRoot(newNode);
        }
        return t;
    }

    public static void viewPrunedTree(MinMaxTree tree) {
        System.out.println("\nPath to best value:\n" + tree.getPathToBestValue());
        System.out.println("Pruned:\n" + tree.getPrunedNodes() + "\n");
    }

    public static void main(String[] args) {

        /////////////////////////////////////////
        int branchingFactor = 2;
        int numNodes = 31; // including root
        int goalNodeId = numNodes - 1;
        int dlsLimit = 6;
        boolean verbose = true;
        ////////////////////////////////////////

        // sanity check, if these conditions weren't avoided,
        // the execution time would be very large.
        if ((numNodes >= 80000 && branchingFactor < 25) || numNodes > 90000) {
            System.out.println("\tToo many nodes.\n\t\tTry again.");
            return;
        }

        Tree t = genRandomTree(branchingFactor, 10, numNodes);

        // Print tree
//         System.out.println(t);
        System.out.println(t.printTreeTopToBottom());

        //  -- Searching --
        int indexOfChoice = t.lookupIndex(goalNodeId);
        Node targetNode;

        // x < 0        : default set to root
        // x = (0 - n)  : search for valid node
        // x > n        : default set to null (NO PATH, traverses full tree)
        if (indexOfChoice < 0) {
            targetNode = t.getRoot();
        } else {
            targetNode = ((indexOfChoice < t.getNodeStorageSize()) ?
                    t.getNodeStorage().get(indexOfChoice) : null);
        }

        ArrayList<Node> bfs = performBFS(t, targetNode, verbose);
        ArrayList<Node> dfs = performDFS(t, targetNode, verbose);
        ArrayList<Node> dls = performDLS(t, targetNode, dlsLimit, verbose);
        ArrayList<Node> ids = performIDS(t, targetNode, verbose);

        //  -- MiniMax --
        System.out.println("\n\n\tMinMax Trees\n");
        Tree minMaxTree = genMinMaxTree(branchingFactor, 1, numNodes, true);
//        System.out.println(minMaxTree);

        ArrayList<Integer> a = new ArrayList<>();
        for (int i = 1; i < (numNodes + 1) + 1; i++) {
            a.add(i);
        }
        MinMaxTree minMax1 = genMinMaxTreeFromArr(branchingFactor, genRandomArray(numNodes), true);
        MinMaxTree minMax2 = genMinMaxTreeFromArr(branchingFactor, genRandomArray(numNodes), false);
        MinMaxTree minMaxA = genMinMaxTreeFromArr(branchingFactor, a, true);
        MinMaxTree minMaxB = genMinMaxTreeFromArr(branchingFactor, a, false);

//        System.out.println(t.getNodeStorage().get(45).getChildren());
        System.out.println("\tRoot is Max node\n" + minMax1);
        System.out.println("\n\tRoot is Min node\n" + minMax2);

//        MinMaxTree maxRootPruned = minMax1.pruneTree();
//        System.out.println("\tmaxRootPruned:\n" + maxRootPruned);
//        minMax2.doMinMaxOnNode(minMax2.getNodeStorage().get(minMax2.lookupIndex(3)));
//        minMax2.doMinMaxOnNode(minMax2.getNodeStorage().get(minMax2.lookupIndex(1)));
        viewPrunedTree(minMax1);
        viewPrunedTree(minMax2);
        viewPrunedTree(minMaxA);
        viewPrunedTree(minMaxB);

        System.out.println(minMaxA.getPrunedTree().printTreeTopToBottom());
        System.out.println(minMaxB.getPrunedTree().printTreeTopToBottom());


// 		arr = genRandomArray(1);
// 		Tree minMaxTree = new MinMaxTree(branchingFactor, arr, true);
    }

}
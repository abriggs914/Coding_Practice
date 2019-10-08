import java.util.ArrayList;
import java.util.Arrays;
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

    private static MinMaxTree genMinMaxTree(String id, int bF, int arrSize, int numNodes, boolean rootIsMaxNode) {
        ArrayList<Integer> arr = genRandomArray(arrSize);
        MinMaxTree t = new MinMaxTree(id, bF, arr, rootIsMaxNode);
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
        t.pruneTree();
        t.initOriginalTree();
        t = t.getPrunedTree();
        return t;
    }

    // this makes one more node than i want it to
    private static MinMaxTree genMinMaxTreeFromArr(String id, int bF, ArrayList<Integer> nums, boolean rootIsMaxNode) {
        ArrayList<ArrayList<Integer>> arr = new ArrayList<>();
        for (int num : nums) {
            ArrayList<Integer> n = new ArrayList<>();
            n.add(num);
            arr.add(n);
        }
        MinMaxTree t = new MinMaxTree(id, bF, arr.get(0), rootIsMaxNode);
        for (int i = 1; i < arr.size(); i++) {
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
        }
        t.doMiniMax();
        t.pruneTree();
        t.initOriginalTree();
        t = t.getPrunedTree();
        return t;
    }

    private static Tree genTreeFromArr(String id, int bF, ArrayList<Integer> nums) {
        ArrayList<ArrayList<Integer>> arr = new ArrayList<>();
        for (int num : nums) {
            ArrayList<Integer> n = new ArrayList<>();
            n.add(num);
            arr.add(n);
        }
        Tree t = new Tree(id, bF, arr.get(0));
        for (int i = 1; i < arr.size(); i++) {
//            arr = genRandomArray(10);
            Node newNode = new Node(i + 1, bF, arr.get(i));
            t.addNodeToRoot(newNode);
        }
        return t;
    }

    private static Tree genRandomTree(String id, int bF, int arrSize, int numNodes) {
        ArrayList<Integer> arr = genRandomArray(arrSize);
        Tree t = new Tree(id, bF, arr);
        for (int i = 1; i < numNodes; i++) {
            arr = genRandomArray(10);
            Node newNode = new Node(i + 1, bF, arr);
            t.addNodeToRoot(newNode);
        }
        return t;
    }

    public static void viewPrunedTree(MinMaxTree tree) {
        System.out.println("\n\t" + tree.getID());
        System.out.println("Path to best value:\n" + tree.getPathToBestValue());
        System.out.println("Pruned:\n" + tree.getPrunedNodes() + "\n");
    }

    public static Node lookUpTargetNode(int indexOfChoice, Tree t) {
        System.out.println("indexOfChoice:\t" + indexOfChoice);
        Node targetNode;
        // x < 0        : default set to root
        // x = (0 - n)  : search for valid node
        // x > n        : default set to null (NO PATH, traverses full tree)
        if (indexOfChoice < 2) {
            targetNode = t.getRoot();
        }
        else {
            String index = Integer.toString(indexOfChoice);
            try {
                targetNode = t.getNodeStorage().get(index);
            }
            catch (Exception e) {
                targetNode = null;
            }
        }
        return targetNode;
    }

    public static void main(String[] args) {

        /////////////////////////////////////////
        int branchingFactor = 2;
        int numNodes = 31; // including root
        int goalNodeId = 31;
        int dlsLimit = 6;
        boolean verbose = true;
        ////////////////////////////////////////

        // sanity check, if these conditions weren't avoided,
        // the execution time would be very large.
        if ((numNodes >= 80000 && branchingFactor < 25) || numNodes > 90000) {
            System.out.println("\tToo many nodes.\n\t\tTry again.");
            return;
        }

        Tree t = genRandomTree(("random (n = " + numNodes + ", a = " + 10 + ")"), branchingFactor, 10, numNodes);

        // Print tree
//         System.out.println(t);
        System.out.println(t.printTreeTopToBottom());

        //  -- Searching --
//        int indexOfChoice = t.lookupIndex(goalNodeId);
        Node targetNode = lookUpTargetNode(goalNodeId, t);
        System.out.println("TargetNode:\t" + targetNode);

        ArrayList<Node> bfs = performBFS(t, targetNode, verbose);
        ArrayList<Node> dfs = performDFS(t, targetNode, verbose);
        ArrayList<Node> dls = performDLS(t, targetNode, dlsLimit, verbose);
        ArrayList<Node> ids = performIDS(t, targetNode, verbose);

        //  -- MiniMax --
        System.out.println("\n\n\tMinMax Trees\n");
        Tree minMaxTree = genMinMaxTree(("minmax (n = " + numNodes + ", a = " + 1 + ")"), branchingFactor, 1, numNodes, true);
//        System.out.println(minMaxTree);

        ArrayList<Integer> a = new ArrayList<>();
        for (int i = 1; i < (numNodes + 1); i++) {
            a.add(i);
        }
//        MinMaxTree minMax1 = genMinMaxTreeFromArr(branchingFactor, genRandomArray(numNodes), true);
//        MinMaxTree minMax2 = genMinMaxTreeFromArr(branchingFactor, genRandomArray(numNodes), false);
        MinMaxTree minMaxA = genMinMaxTreeFromArr(("minmaxA (n = " + numNodes + ", a = " + 1 + ")"), branchingFactor, a, true);
        MinMaxTree minMaxB = genMinMaxTreeFromArr(("minmaxB (n = " + numNodes + ", a = " + 1 + ")"), branchingFactor, a, false);

//        System.out.println("\tRoot is Max node\n" + minMax1);
//        System.out.println("\n\tRoot is Min node\n" + minMax2);

//        System.out.println("\tmaxRootPruned:\n" + maxRootPruned);
//        minMax2.doMinMaxOnNode(minMax2.getNodeStorage().get(minMax2.lookupIndex(3)));
//        minMax2.doMinMaxOnNode(minMax2.getNodeStorage().get(minMax2.lookupIndex(1)));
//        viewPrunedTree(minMax1);
//        viewPrunedTree(minMax2);
        viewPrunedTree(minMaxA);
        viewPrunedTree(minMaxB);

        System.out.println(minMaxA);
        System.out.println(minMaxB);
        System.out.println(minMaxB.getOriginalTree());
        System.out.println(minMaxA.printTreeTopToBottom());
        System.out.println(minMaxB.printTreeTopToBottom());
        System.out.println(minMaxB.getOriginalTree().printTreeTopToBottom());

        // Challenge the MinMaxTree
//        MinMaxTree bigTree = genMinMaxTree("BigTree (n = 300, a = 9)", 3,9,300,true);
//        System.out.println(bigTree);
//        viewPrunedTree(bigTree);

        int[] dChildren = {-2, 0, -4};
        int[] eChildren = {4, -3, 3};
        int[] fChildren = {-3, -2, -1};
        int[] gChildren = {1, 6, 4};

        Node nodeA = new MaxNode(1, 2, genRandomArray(1));
        Node nodeB = new MinNode(2, 2, genRandomArray(1));
        Node nodeC = new MinNode(3, 2, genRandomArray(1));
        Node nodeD = new MaxNode(4, 3, dChildren);
        Node nodeE = new MaxNode(5, 3, eChildren);
        Node nodeF = new MaxNode(6, 3, fChildren);
        Node nodeG = new MaxNode(7, 3, gChildren);

        Node nodeH = new MaxNode(8, 0, dChildren[0]);
        Node nodeI = new MaxNode(9, 0, dChildren[1]);
        Node nodeJ = new MaxNode(10, 0, dChildren[2]);
        Node nodeK = new MaxNode(11, 0, eChildren[0]);
        Node nodeL = new MaxNode(12, 0, eChildren[1]);
        Node nodeM = new MaxNode(13, 0, eChildren[2]);
        Node nodeN = new MaxNode(14, 0, fChildren[0]);
        Node nodeO = new MaxNode(15, 0, fChildren[1]);
        Node nodeP = new MaxNode(16, 0, fChildren[2]);
        Node nodeQ = new MaxNode(17, 0, gChildren[0]);
        Node nodeR = new MaxNode(18, 0, gChildren[1]);
        Node nodeS = new MaxNode(19, 0, gChildren[2]);
        MinMaxTree unEvenTree = new MinMaxTree("Uneven tree", nodeA, true);
        unEvenTree.addNodeToTree(nodeB, nodeA);
        unEvenTree.addNodeToTree(nodeC, nodeA);
        unEvenTree.addNodeToTree(nodeD, nodeB);
        unEvenTree.addNodeToTree(nodeE, nodeB);
        unEvenTree.addNodeToTree(nodeF, nodeC);
        unEvenTree.addNodeToTree(nodeG, nodeC);

        unEvenTree.addNodeToTree(nodeH, nodeD);
        unEvenTree.addNodeToTree(nodeI, nodeD);
        unEvenTree.addNodeToTree(nodeJ, nodeD);

        unEvenTree.addNodeToTree(nodeK, nodeE);
        unEvenTree.addNodeToTree(nodeL, nodeE);
        unEvenTree.addNodeToTree(nodeM, nodeE);

        unEvenTree.addNodeToTree(nodeN, nodeF);
        unEvenTree.addNodeToTree(nodeO, nodeF);
        unEvenTree.addNodeToTree(nodeP, nodeF);

        unEvenTree.addNodeToTree(nodeQ, nodeG);
        unEvenTree.addNodeToTree(nodeR, nodeG);
        unEvenTree.addNodeToTree(nodeS, nodeG);
        System.out.println("\n\t- After construction -\n" + unEvenTree);
        unEvenTree.doMiniMax();
        unEvenTree.pruneTree();
        unEvenTree.initOriginalTree();
        unEvenTree = unEvenTree.getPrunedTree();
        System.out.println("\n\t- After pruning -\n" + unEvenTree);
        viewPrunedTree(unEvenTree);


        System.out.println("____________________________________________");
        Node classEXNodeA = new MaxNode(1, 2, 1);
        MinMaxTree classEXTree = new MinMaxTree("Class Example", classEXNodeA, true);

        Node classEXNodeB = new MinNode(2, 2, 1);
        Node classEXNodeC = new MinNode(3, 2, 1);

        Node classEXNodeD = new MaxNode(4, 2, 1);
        Node classEXNodeE = new MaxNode(5, 2, 1);
        Node classEXNodeF = new MaxNode(6, 2, 1);
        Node classEXNodeG = new MaxNode(7, 2, 1);

        Node classEXNodeH = new MinNode(8, 2, 1);
        Node classEXNodeI = new MinNode(9, 2, 1);
        Node classEXNodeJ = new MinNode(10, 2, 1);
        Node classEXNodeK = new MinNode(11, 2, 1);
        Node classEXNodeL = new MinNode(12, 2, 1);
        Node classEXNodeM = new MinNode(13, 2, 1);
        Node classEXNodeN = new MinNode(14, 2, 1);
        Node classEXNodeO = new MinNode(15, 2, 1);

        Node classEXNodeP = new Node(16, 0, 8);
        Node classEXNodeQ = new Node(17, 0, 7);
        Node classEXNodeR = new Node(18, 0, 3);
        Node classEXNodeS = new Node(19, 0, 1);
        Node classEXNodeT = new Node(20, 0, 9);
        Node classEXNodeU = new Node(21, 0, 8);
        Node classEXNodeV = new Node(22, 0, 100);
        Node classEXNodeW = new Node(23, 0, -10);
        Node classEXNodeX = new Node(24, 0, 1);
        Node classEXNodeY = new Node(25, 0, -1);
        Node classEXNodeZ = new Node(26, 0, 8);
        Node classEXNodeAA = new Node(27, 0, 9);
        Node classEXNodeAB = new Node(28, 0, 9);
        Node classEXNodeAC = new Node(29, 0, 9);
        Node classEXNodeAD = new Node(30, 0, 1);
        Node classEXNodeAE = new Node(31, 0, -3);

        classEXTree.addNodeToTree(classEXNodeB, classEXNodeA);
        classEXTree.addNodeToTree(classEXNodeC, classEXNodeA);
        classEXTree.addNodeToTree(classEXNodeD, classEXNodeB);
        classEXTree.addNodeToTree(classEXNodeE, classEXNodeB);
        classEXTree.addNodeToTree(classEXNodeF, classEXNodeC);
        classEXTree.addNodeToTree(classEXNodeG, classEXNodeC);
        classEXTree.addNodeToTree(classEXNodeH, classEXNodeD);
        classEXTree.addNodeToTree(classEXNodeI, classEXNodeD);
        classEXTree.addNodeToTree(classEXNodeJ, classEXNodeE);
        classEXTree.addNodeToTree(classEXNodeK, classEXNodeE);
        classEXTree.addNodeToTree(classEXNodeL, classEXNodeF);
        classEXTree.addNodeToTree(classEXNodeM, classEXNodeF);
        classEXTree.addNodeToTree(classEXNodeN, classEXNodeG);
        classEXTree.addNodeToTree(classEXNodeO, classEXNodeG);

        classEXTree.addNodeToTree(classEXNodeP, classEXNodeH);
        classEXTree.addNodeToTree(classEXNodeQ, classEXNodeH);
        classEXTree.addNodeToTree(classEXNodeR, classEXNodeI);
        classEXTree.addNodeToTree(classEXNodeS, classEXNodeI);
        classEXTree.addNodeToTree(classEXNodeT, classEXNodeJ);
        classEXTree.addNodeToTree(classEXNodeU, classEXNodeJ);
        classEXTree.addNodeToTree(classEXNodeV, classEXNodeK);
        classEXTree.addNodeToTree(classEXNodeW, classEXNodeK);
        classEXTree.addNodeToTree(classEXNodeX, classEXNodeL);
        classEXTree.addNodeToTree(classEXNodeY, classEXNodeL);
        classEXTree.addNodeToTree(classEXNodeZ, classEXNodeM);
        classEXTree.addNodeToTree(classEXNodeAA, classEXNodeM);
        classEXTree.addNodeToTree(classEXNodeAB, classEXNodeN);
        classEXTree.addNodeToTree(classEXNodeAC, classEXNodeN);
        classEXTree.addNodeToTree(classEXNodeAD, classEXNodeO);
        classEXTree.addNodeToTree(classEXNodeAE, classEXNodeO);

        System.out.println("\n\t- After construction -\n" + classEXTree);
        classEXTree.doMiniMax();
        classEXTree.pruneTree();
        classEXTree.initOriginalTree();
        classEXTree = classEXTree.getPrunedTree();
        System.out.println("\n\t- After pruning -\n" + classEXTree);
        viewPrunedTree(classEXTree);
        System.out.println(classEXTree.printTreeTopToBottom());

//        Integer[] ad = {1, 1,1, 1,1,1,1, 1,1,1,1,1,1,1,1, 18,7,3,1,9,8,100,-10,1,-1,8,9,9,9,1,-3};
//        ArrayList<Integer> al = new ArrayList<>();
//        for (int el : ad) {
//            al.add(el);
//        }
//        MinMaxTree tree2 = genMinMaxTreeFromArr("tree 2", 2, al, true);
//        System.out.println(tree2);
//        System.out.println(tree2.printTreeTopToBottom());
//        viewPrunedTree(tree2);

//        Integer[] question6 = {1, 1,1, 1,1,1,1, 0,-4,4,-3,-3,-1,1,6};
//        ArrayList<Integer> q6A = new ArrayList<>();
//        for (int el : question6) {
//            q6A.add(el);
//        }
//        MinMaxTree questionSix = genMinMaxTreeFromArr("Question 6", 2, q6A, true);
//        System.out.println(questionSix);
//        viewPrunedTree(questionSix);
//        System.out.println(questionSix.printTreeTopToBottom());


// 		arr = genRandomArray(1);
// 		Tree minMaxTree = new MinMaxTree(branchingFactor, arr, true);
    }

}
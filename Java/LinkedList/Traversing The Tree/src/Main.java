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

    private static void performBFS(Tree t, Node targetNode) {
        System.out.println();
        System.out.println("\tBFS\n");
        ArrayList<Node> path = t.breadthFirstSearch(targetNode);
        System.out.println("\tANSWER:\n" + targetNode + "\n\tPATH:\n");
        for (Node visitedNode : path) {
            System.out.println(" -> " + visitedNode);
        }
        System.out.println("\n\tPATH.SIZE():\n" + path.size());
        System.out.println();
    }

    private static void performDFS(Tree t, Node targetNode) {
        System.out.println();
        System.out.println("\tDFS\n");
        ArrayList<Node> path = t.depthFirstSearch(targetNode);
        System.out.println("\tANSWER:\n" + targetNode + "\n\tPATH:\n");
        for (Node visitedNode : path) {
            System.out.println(" -> " + visitedNode);
        }
        System.out.println("\n\tPATH.SIZE():\n" + path.size());
        System.out.println();
    }

    private static void performDLS(Tree t, Node targetNode, int dlsLimit) {
        System.out.println();
        System.out.println("\tDLS\n" + "Limit:\t" + dlsLimit);
        ArrayList<Node> path = t.depthLimitedSearch(dlsLimit, targetNode);
        System.out.println("\tANSWER:\n" + targetNode + "\n\tPATH:\n");
        for (Node visitedNode : path) {
            System.out.println(" -> " + visitedNode);
        }
        System.out.println("\n\tPATH.SIZE():\n" + path.size());
        System.out.println();
    }

    private static void performIDS(Tree t, Node targetNode) {
        System.out.println();
        System.out.println("\tIDS\n");
        ArrayList<Node> path = t.iterativeDepthLimitingSearch(targetNode);
        System.out.println("\tANSWER:\n" + targetNode + "\n\tPATH:\n");
        for (Node visitedNode : path) {
            System.out.println(" -> " + visitedNode);
        }
        System.out.println("\n\tPATH.SIZE():\n" + path.size());
        System.out.println();
    }

    private static Tree genMinMaxTree(int bF, int arrSize, int numNodes, boolean rootIsMaxNode) {
        ArrayList<Integer> arr = genRandomArray(arrSize);
        Tree t = new MinMaxTree(bF, arr, rootIsMaxNode);
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
        return t;
    }

    private static Tree genMinMaxTreeFromArr(int bF, ArrayList<Integer> nums, boolean rootIsMaxNode) {
        ArrayList<ArrayList<Integer>> arr = new ArrayList<>();
        for (int num : nums) {
            ArrayList<Integer> n = new ArrayList<>();
            n.add(num);
            arr.add(n);
        }
        Tree t = new MinMaxTree(bF, arr.get(0), rootIsMaxNode);
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
                    newNode = new MaxNode(i + 2, bF, arr.get(i));
                } else {
                    newNode = new MinNode(i + 2, bF, arr.get(i));
                }
            } else {
                if (rootIsMaxNode) {
                    newNode = new MinNode(i + 2, bF, arr.get(i));
                } else {
                    newNode = new MaxNode(i + 2, bF, arr.get(i));
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
            // System.out.println("addResult:\t" + ((addResult)? "Successful" : "Failure") + "\n\n");
//            if (i == (arr.size() - 2)) {
//                maxDepth = t.computeMaxDepth(newNode);
//            }
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
            // System.out.println("addResult:\t" + ((addResult)? "Successful" : "Failure") + "\n\n");
//            if (i == (numNodes - 2)) {
//                maxDepth = t.computeMaxDepth(newNode);
//            }
        }
        return t;
    }

    public static void main(String[] args) {

        /////////////////////////////////////////
        int branchingFactor = 3;
        int numNodes = 33; // including root
        int goalNodeId = 13;
        int dlsLimit = 6;
        ////////////////////////////////////////

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

        performBFS(t, targetNode);
        performDFS(t, targetNode);
        performDLS(t, targetNode, dlsLimit);
        performIDS(t, targetNode);

        //  -- MiniMax --
        System.out.println("\n\n\tMinMax Trees\n");
        Tree minMaxTree = genMinMaxTree(branchingFactor, 1, numNodes, true);
//        System.out.println(minMaxTree);

        ArrayList<Integer> a = new ArrayList<>();
        for (int i = 0; i < numNodes + 1; i++) {
            a.add(i);
        }
        Tree minMax1 = genMinMaxTreeFromArr(branchingFactor, a, true);
        Tree minMax2 = genMinMaxTreeFromArr(branchingFactor, a, false);
//        System.out.println("\tRoot is Max node\n" + minMax1);
//        System.out.println("\n\tRoot is Min node\n" + minMax2);


// 		arr = genRandomArray(1);
// 		Tree minMaxTree = new MinMaxTree(branchingFactor, arr, true);
    }

}
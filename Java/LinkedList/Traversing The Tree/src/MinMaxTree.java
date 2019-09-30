import java.io.*;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Stack;

public class MinMaxTree extends Tree {

//    private Node root;
    private boolean rootIsMaxNode;
    private int maxDepth;
    private ArrayList<Node> prunedNodes;


    MinMaxTree(int branchingFactor, ArrayList<Integer> arr, boolean rootIsMaxNode) {
        super(branchingFactor, arr);
        this.rootIsMaxNode = rootIsMaxNode;
        if (rootIsMaxNode) {
            this.root = new MaxNode(1, branchingFactor, arr);
//            this.root.initValue();
        }
        else {
            this.root = new MinNode(1, branchingFactor, arr);
        }
        this.root.setParent(null);
        this.prunedNodes = new ArrayList<>();
//        this.root.initAlpha();
//        this.root.initBeta();
    }

    public void doMiniMax() {
        root.setValue(minimax(root, 0, this.rootIsMaxNode, Integer.MIN_VALUE, Integer.MAX_VALUE));
        System.out.println("\n\tMINIMAX complete:\nRoot.val:\t" + root.getValue());
    }

    public void doMinMaxOnNode(Node nodeIn) {
        boolean nodeIsMaxNode = (this.rootIsMaxNode && nodeIn.getDepth() % 2 == 0) ||
                                (!this.rootIsMaxNode && nodeIn.getDepth() % 2 == 1);
        Node parent = nodeIn.getParent();
        if (parent == null) {
            doMiniMax();
            return;
        }
        nodeIn.setValue(minimax(nodeIn, nodeIn.getDepth(), nodeIsMaxNode, parent.getAlpha(), parent.getBeta()));
//        System.out.println("\nMINIMAX on node: " + nodeIn);
//        System.out.println("\n\tMINIMAX complete:\nnode.val:\t" + nodeIn.getValue());
    }

    public int minimax(Node node, int depth, boolean isMaximizingPlayer, int alpha, int beta) {

        if (node.getLeafStatus()){
            return node.getValue();
        }
        if (isMaximizingPlayer) {
            int bestVal = Integer.MIN_VALUE;
            for (Node child : node.getChildren()) {
                int value = minimax(child, depth + 1, false, alpha, beta);
                bestVal = Math.max(bestVal, value);
                alpha = Math.max(alpha, bestVal);
                child.setAlpha(alpha);
                child.setBeta(beta);
                if (bestVal > beta) {
                    if (!prunedNodes.contains(node)) {
                        this.prunedNodes.add(node);
                    }
                }
                if (beta <= alpha) {
                    break;
                }
            }
            return bestVal;
        }
        else {
            int bestVal = Integer.MAX_VALUE;
            for (Node child : node.getChildren()) {
                int value = minimax(child, depth + 1, true, alpha, beta);
                bestVal = Math.min(bestVal, value);
                beta = Math.min(beta, bestVal);
                child.setAlpha(alpha);
                child.setBeta(beta);
                if (bestVal < alpha) {
                    if (!prunedNodes.contains(node)) {
                        this.prunedNodes.add(node);
                    }
                }
                if (beta <= alpha) {
                    break;
                }
            }
            return bestVal;
        }
    }



    public MinMaxTree pruneTree() {
        MinMaxTree prunedTree = new MinMaxTree(root.getBranchingFactor(), root.getArr(), this.rootIsMaxNode);
        ArrayList<Node> prunedNodesList = new ArrayList<>();
        pruningHelper(this.getRoot(), prunedNodesList, prunedTree);

//        this.getRoot().updateValue();

//        ArrayList<Node> children = root.getChildren();
//        Stack nodeStack = new Stack();
//        nodeStack.addAll(children);
//        while (nodeStack.size() > 0) {
//            System.out.println("\tSTACK:\n");
//            for (Iterator it = nodeStack.iterator(); it.hasNext(); ) {
//                Node stackMember = (Node) it.next();
//                System.out.println(stackMember);
//            }
//            Node child = (Node) nodeStack.pop();
//            child.updateValue();
////            prunedTree.addNodeToRoot(child);
//            System.out.println("child:\t" + child);
//            ArrayList<Node> grandChildren = child.getChildren();
//            for (Node grandChild : grandChildren){
//                nodeStack.push(grandChild);
//            }
//        }
        return this;
    }

    public void pruningHelper(Node currNode, ArrayList<Node> prunedNodes, MinMaxTree newTree) {
        ArrayList<Node> children = currNode.getChildren();
//        currNode.updateValue();
        for (Node child : children) {
//            newTree.addNodeToRoot(child);
            doMinMaxOnNode(child);
            pruningHelper(child, prunedNodes, newTree);
        }
    }

    public ArrayList<Node> getPathToBestValue() {
        ArrayList<Node> path = new ArrayList<>();
        path.add(root);
        Node currNode = root;
        int currNodeVal = currNode.getValue();
        while (currNode.hasChildren()) {
//            System.out.println("currNode:\t" + currNode);
            for (Node child : currNode.getChildren()) {
//                System.out.println("\tchild:\t" + currNode);
                if (child.getValue() == currNodeVal) {
                    path.add(child);
                    currNode = child;
                    currNodeVal = child.getValue();
                }
            }
        }
        return path;
    }

    ArrayList<Node> getPrunedNodes() {
        ArrayList<Node> nodesList = this.prunedNodes;
        ArrayList<Node> prunedPrunedList = new ArrayList<>();
        for (Node prunedNode : nodesList) {
            Node parent = prunedNode.getParent();
            while (parent != root) {
                if (nodesList.contains(parent)) {
                    // parent of prunedNode exists
                    break;
                }
                parent = parent.getParent();
            }
            if (parent == root) {
                prunedPrunedList.add(prunedNode);
            }
        }
        return prunedPrunedList;
    }

    public MinMaxTree getPrunedTree() {
        MinMaxTree newTree = null;
        ArrayList<Node> prunedNodesLst = this.getPrunedNodes();
        newTree = new MinMaxTree(root.getBranchingFactor(), root.getArr(), rootIsMaxNode);
        for (Node node : prunedNodesLst) {
            ArrayList<Node> pathToNode = this.breadthFirstSearch(node);
            Node nodeToPrune = pathToNode.get(pathToNode.size() - 1);
            nodeToPrune.pruneChildren();
            nodeToPrune.setParent(null);
        }
        //        Node currNode = root;
//        Queue<Node> queue = new LinkedList<>();
//        if (root.hasChildren()) {
//            queue.addAll(root.getChildren());
//        }
//        while (queue.size() > 0) {
////            ArrayList<Node> children = currNode.getChildren();
////            for (Node child : children) {
////                if (!prunedNodesLst.contains(child)) {
////                    queue.add(child);
////                    child.setParent(currNode);
////                }
////            }
//        }
        return this;
    }

//    public MinMaxTree copyMinMaxTree(MinMaxTree orig) {
//        ArrayList<Node> prunedNodesLst = this.getPrunedNodes();
//    }

//    boolean getRootIsNode() {
//        return this.rootIsMaxNode;
//    }
}

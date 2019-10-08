package com.example.abrig.tictactoeapp;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

/**
 *
 * MiniMaxTree is a data structure similar to a tree except a node
 * may be a min node or a max node. A min node selects the minimum
 * of its children and a max node selects the maximum of it's
 * children. This allows for the simulation of alpha-beta pruning
 * in a min vs. max game environment.
 *
 * @author Avery Briggs
 *
 * Sept. 30 / 2019
 *
 * */

class MinMaxTree extends Tree {

    /**
     * boolean value, true if root is a max node,
     * false otherwise.
     * */
    private boolean rootIsMaxNode;

    /**
     * ArrayList of nodes containing the pruned
     * nodes encountered in the tree.
     * */
    private ArrayList<Node> prunedNodes;

    /**
     * MinMaxTree contianing the original tree without pruning.
     * */
    private MinMaxTree originalTree;

    MinMaxTree(String id, int branchingFactor, ArrayList<Integer> arr, boolean rootIsMaxNode) {
        super(id, branchingFactor, arr);
        this.rootIsMaxNode = rootIsMaxNode;
        if (rootIsMaxNode) {
            this.root = new MaxNode(1, branchingFactor, arr);
        }
        else {
            this.root = new MinNode(1, branchingFactor, arr);
        }
        this.root.setParent(null);
        prunedNodes = new ArrayList<>();
    }

    MinMaxTree(String id, Node rootIn, boolean rootIsMaxNode) {
        super(id, rootIn);
        this.rootIsMaxNode = rootIsMaxNode;
        this.root = rootIn;
        this.root.setParent(null);
        prunedNodes = new ArrayList<>();
    }

    /**
     * Called from the driver class after initialization of a new MinMaxTree.
     * Maintains all original paths before any pruning is done.
     * */
    void initOriginalTree() {
        this.originalTree = new MinMaxTree(this.getID() + "\n-- ORIGINAL TREE --", root.getBranchingFactor(), root.getArr(), rootIsMaxNode);
        HashMap<String, Node> nodeStorage = getNodeStorage();
        for (int i = 1; i < nodeStorage.size(); i++) {
            Node node = nodeStorage.get(Integer.toString(i + 1));
            Node newNode = new Node(node.getNodeNum(), node.getBranchingFactor(), node.getArr());
            originalTree.addNodeToRoot(newNode);
        }
    }

    /**
     * Called on initialization of new MinMaxTree. Makes a call to minimax()
     * from the root node. This sets all alpha, beta and value data entries
     * to the corresponding output from the minimax algorithm.
     * */
    void doMiniMax() {
        root.setValue(minimax(root, 0, this.rootIsMaxNode, Integer.MIN_VALUE, Integer.MAX_VALUE));
        System.out.println("\n\tMINIMAX complete:\n\tRoot.val:\t" + root.getValue() + "\n");
    }

    /**
     * Makes a call to minimax() from the paramaterized node.
     * This sets all alpha, beta and value data entries below the
     * given node to their corresponding outputs from the
     * minimax algorithm.
     * @param nodeIn The node to perform a minimax on.
     * */
    private void doMinMaxOnNode(Node nodeIn) {
        boolean nodeIsMaxNode = (this.rootIsMaxNode && nodeIn.getDepth() % 2 == 0) ||
                                (!this.rootIsMaxNode && nodeIn.getDepth() % 2 == 1);
        Node parent = nodeIn.getParent();
        if (parent == null) {
            doMiniMax();
            return;
        }
        nodeIn.setValue(minimax(nodeIn, nodeIn.getDepth(), nodeIsMaxNode, parent.getAlpha(), parent.getBeta()));
//        System.out.println("\nMINIMAX on node: " + nodeIn);
//        System.out.println("\n\tMINIMAX complete:\tnode.val:\t" + nodeIn.getValue());
    }

    /**
     * Performs the minimax Algorithm on a given starting node.
     * Traverses every node and assigns each it's new alpha, beta,
     * and value data entries, as well as adds non-necessary nodes
     * to the prunedNodes list.
     * @param node Starting node to begin the algorithm.
     * @param depth Depth of the starting node.
     * @param isMaximizingPlayer Boolean indicating if node is a max node or not.
     * @param alpha Initially Integer.MIN_VALUE, but is adjusted to represent the
     *              best outcome for a max node (worst for min).
     * @param beta Initially Integer.MAX_VALUE, but is adjusted to represent the
     *             best outcome for the min node (worst for max).
     * @return bestVal The best outcome in the given tree if all moves are optimal.
     */
    private int minimax(Node node, int depth, boolean isMaximizingPlayer, int alpha, int beta) {
//        System.out.println("Expanding:\t" + node);
        if (node.getLeafStatus()){
            return node.getValue();
        }
        ArrayList<Node> prunedNodes = this.getPrunedNodes();
        if (isMaximizingPlayer) {
            int bestVal = Integer.MIN_VALUE;
            ArrayList<Node> children = node.getChildren();
            for (int i = 0; i < children.size(); i++) {
                Node child = children.get(i);
                int value = minimax(child, depth + 1, child.getIsMaxNode(), alpha, beta);
                bestVal = Math.max(bestVal, value);
                alpha = Math.max(alpha, bestVal);
                child.setAlpha(alpha);
                child.setBeta(beta);
                if (bestVal > beta) {
                    if (!prunedNodes.contains(node)) {
                        for (Node childNode : children) {
                            if (childNode != child) {
                                addPrunedNode(childNode);
                            }
                        }
                    }
                }
                if (beta <= alpha) {
                    break;
                }
            }
//            System.out.println("\tReturning (MAX):\t" + bestVal);
            return bestVal;
        }
        else {
            int bestVal = Integer.MAX_VALUE;
            ArrayList<Node> children = node.getChildren();
            for (int i = 0; i < children.size(); i++) {
                Node child = children.get(i);
                int value = minimax(child, depth + 1, child.getIsMaxNode(), alpha, beta);
                bestVal = Math.min(bestVal, value);
                beta = Math.min(beta, bestVal);
                child.setAlpha(alpha);
                child.setBeta(beta);
                if (bestVal < alpha) {
                    if (!prunedNodes.contains(node)) {
                        for (Node childNode : children) {
                            if (childNode != child) {
                                addPrunedNode(childNode);
                            }
                        }
                    }
                }
                if (beta <= alpha) {
                    break;
                }
            }
//            System.out.println("\tReturning (MIN):\t" + bestVal);
            return bestVal;
        }
    }

    private ArrayList<Node> getPrunedNodesList() {
        return prunedNodes;
    }

    private void addPrunedNode(Node prunedNode) {
        prunedNodes.add(prunedNode);
    }

    MinMaxTree getOriginalTree() {
        return this.originalTree;
    }


    void pruneTree() {
        pruningHelper(this.getRoot());

    }

    private void pruningHelper(Node currNode) {
        ArrayList<Node> children = currNode.getChildren();
//        currNode.updateValue();
        for (Node child : children) {
//            newTree.addNodeToRoot(child);
            doMinMaxOnNode(child);
            pruningHelper(child);
        }
    }

    ArrayList<Node> getPathToBestValue() {
        ArrayList<Node> path = new ArrayList<>();
        path.add(root);
        Node currNode = root;
        int currNodeVal = currNode.getValue();
        while (currNode.hasChildren()) {
//            System.out.println("currNode:\t" + currNode);
            for (Node child : currNode.getChildren()) {
//                System.out.println("\tchild:\t" + child);
                if (child.getValue() == currNodeVal) {
                    path.add(child);
                    currNode = child;
                    currNodeVal = child.getValue();
                }
            }
        }
        Collections.reverse(path);
        ArrayList<Node> finalPath = new ArrayList<>();
        Node tempNode = path.get(0);
        for (int i = 0; i < path.size(); i++) {
            Node lstMember = path.get(i);
            finalPath.add(lstMember);
            tempNode = lstMember.getParent();
            i++;
            while (i < path.size() && (path.get(i) != tempNode)) {
                System.out.println("path.get(" + i + "):\t" + path.get(i) + "\ttempNode:\t" + tempNode);
                i++;
            }
        }
        Collections.reverse(finalPath);
        System.out.println("finalPath:\t" + finalPath);
        return finalPath;
    }

    MinMaxTree getPrunedTree() {
        ArrayList<Node> prunedNodesLst = getPrunedNodes();
//        System.out.println("prunedNodesLst:\t" + prunedNodesLst);
        for (Node node : prunedNodesLst) {
            ArrayList<Node> pathToNode = this.breadthFirstSearch(node);
            Node nodeToPrune = pathToNode.get(pathToNode.size() - 1);
            nodeToPrune.pruneChildren();
//            nodeToPrune.setParent(null);
        }
        return this;
    }

    ArrayList<Node> getPrunedNodes() {
        ArrayList<Node> nodesList = getPrunedNodesList();
//        System.out.println("nodesList:\t" + nodesList);
        ArrayList<Node> prunedPrunedList = new ArrayList<>();
        for (Node prunedNode : nodesList) {
            Node parent = prunedNode.getParent();
//            System.out.println("check:\t" + prunedNode);
            while (parent != null) {
                if (nodesList.contains(parent)) {
                    // parent of prunedNode exists
//                    System.out.println("Break");
                    break;
                }
                parent = parent.getParent();
            }
//            System.out.println("-> parent:\t" + parent);
            if (parent == null) {
                prunedPrunedList.add(prunedNode);
            }
        }
//        System.out.println("prunedPrunedList:\t" + prunedPrunedList);
        HashSet hs = new HashSet();
        hs.addAll(prunedPrunedList);
        prunedPrunedList.clear();
        prunedPrunedList.addAll(hs);
        return prunedPrunedList;
    }

    String printTreeTopToBottom() {
        int borderWidth = 1;
        int charSize = 3;
        int spaceSize = 2;
        double bfToMaxDepth = Math.pow(root.getBranchingFactor(), maxDepth);
        int maxWidth = (2 * borderWidth) +
                (int) (charSize * bfToMaxDepth) +
                (int) ((spaceSize * bfToMaxDepth) - 1);

//        System.out.println("maxDepth:\t" + maxDepth +
//                "\nborderWidth:\t" + borderWidth +
//                "\nbranchingFactor:\t" + root.getBranchingFactor() +
//                "\nbfToMaxDepth:\t" + bfToMaxDepth +
//                "\nmaxWidth:\t" + maxWidth);

        if (maxWidth < 500) {
            ArrayList<String> pruneIds = new ArrayList<>();
            for (Node prune : getPrunedNodes()) {
                pruneIds.add(Integer.toString(prune.getNodeNum()));
            }
//            System.out.println("prunedNodes:\t" + this.getPrunedNodes());
            System.out.println("prunedIds:\t" + pruneIds);
            StringBuilder tree = new StringBuilder("\t" + this.getID() + "\n");
            tree.append("\n");
            int currNode = 1;
            int divisor;
//            System.out.println("nodestorage.size():\t" + nodeStorage.size() + "\tmaxdepth:\t" + maxDepth);
            for (int d = 0; d < maxDepth + 1; d++) {
                Node workingNode = nodeStorage.get(Integer.toString(currNode));
                int baseBF = workingNode.getBranchingFactor();
                if (baseBF == 0) {
                    if (!workingNode.getIsMiniMaxNode()) {
                        baseBF = workingNode.getParent().getBranchingFactor();
                    }
                    else {
                        baseBF = 1;
                    }
                }
                divisor = (int) Math.pow(baseBF, d);
                int numNodesOnRow = divisor;
                int spacer = maxWidth / Math.max(2, divisor);
                StringBuilder row = new StringBuilder();
                int i = 0;
//                System.out.println("spacer:\t" + spacer + "\tdivisor:\t" + divisor);
                while (i < maxWidth) {
                    workingNode = nodeStorage.get(Integer.toString(currNode));
                    if (i > 0 && i % spacer == 0) {
                        if ((currNode - 1) < nodeStorage.size() && numNodesOnRow > 0){//&&
                              if(!workingNode.isDecendantOfNodeInList(getPrunedNodes())) {
                                  if (!pruneIds.contains(Integer.toString(workingNode.getNodeNum()))) {
                                      numNodesOnRow--;
                                      String num = Integer.toString(workingNode.getNodeNum());
                                      currNode++;
                                      StringBuilder pad = new StringBuilder();
                                      for (int j = 0; j < (charSize - num.length()); j++) {
                                          pad.append(" ");
                                      }
                                      num = pad + num + "|";
                                      row.append(num);
                                      i += (charSize);
                                  }
                                  else {
                                      currNode++;
                                  }
                              }
                              else {
                                  currNode++;
                              }
                        }
                    }
                    else {
                        row.append(" ");
                    }
                    i++;
                }
                row.append("\n");
                tree.append(row);
            }
            return "\n{ " + tree + " }\n";
        }
        else  {
            return "Tree width is too wide...";
        }
    }

//    public MinMaxTree copyMinMaxTree(MinMaxTree orig) {
//        ArrayList<Node> prunedNodesLst = this.getPrunedNodes();
//    }

//    boolean getRootIsNode() {
//        return this.rootIsMaxNode;
//    }

//    public MinMaxTree copyTree(MinMaxTree tree) {
////        Node newRoot = new Node(root.getNodeNum(), root.getBranchingFactor(), root.getArr());
//        MinMaxTree newTree = new MinMaxTree(root.getBranchingFactor(), root.getArr(), rootIsMaxNode);
//        for (Node node : getNodeStorage()) {
//            Node newNode = new Node(node.getNodeNum(), node.getBranchingFactor(), node.getArr());
//            newTree.addNodeToRoot(newNode);
//        }
//        return newTree;
//    }
}

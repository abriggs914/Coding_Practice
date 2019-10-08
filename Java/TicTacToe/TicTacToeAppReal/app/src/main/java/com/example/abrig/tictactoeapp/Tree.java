package com.example.abrig.tictactoeapp;/*package whatever //do not write package name here */

import java.util.ArrayList;
import java.util.Queue;
import java.util.LinkedList;
import java.util.HashMap;
import java.util.Map;
import java.util.Iterator;
import java.util.Set;

public class Tree {

    private String id;
    Node root;
    int maxDepth;
    HashMap<String,Node> nodeStorage;

    Tree(String id, int branchingFactor, ArrayList<Integer> arr) {
        this.id = id;
        this.root = new Node(1, branchingFactor, arr);
        this.root.setParent(null);
        this.nodeStorage = new HashMap<>();
        nodeStorage.put(Integer.toString(root.getNodeNum()), root);
    }

    Tree(String id, Node rootIn) {
        this.id = id;
        this.root = rootIn;
        this.root.setParent(null);
        this.nodeStorage = new HashMap<>();
        nodeStorage.put(Integer.toString(root.getNodeNum()), root);
    }

    // Returns an ArrayList containing visited nodes on the way to
    // the target node.
    ArrayList<Node> depthFirstSearch(Node target) {
        return depthFirstSearchHelper(root, target, new ArrayList<Node>());
    }

    private ArrayList<Node> depthFirstSearchHelper(Node start, Node target, ArrayList<Node> visited) {
        visited.add(start);
        if (start.equals(target)) {
            return visited;
        }
        for (Node child : start.getChildren()) {
            if (countNodes(child, visited) == 0) {
                ArrayList<Node> path = depthFirstSearchHelper(child, target, visited);
                if (path.size() > 0) {
                    return path;
                }
            }
        }
        return new ArrayList<>();
        // path.clear();
        // return path;
    }

    Node getRoot() {
        return this.root;
    }

    int getNodeStorageSize() {
        return nodeStorage.size();
    }

    HashMap<String, Node> getNodeStorage() {
        return nodeStorage;
    }

    String getID() {
        return this.id;
    }

    // Returns an ArrayList containing visited nodes on the way to
    // the target node.

    ArrayList<Node> breadthFirstSearch(Node target) {
        ArrayList<Node> path = new ArrayList<>();
        path.add(root);
        if (root == target) {
            return path;
        }
        HashMap<Node, ArrayList<Node>> vertexPath = new HashMap<>();
        Queue<HashMap<Node, ArrayList<Node>>> bfsQ = new LinkedList<>();
        vertexPath.put(root, root.getChildren());
        bfsQ.add(vertexPath);
        ArrayList<Node> visited = new ArrayList<>();
        while (bfsQ.size() > 0) {
            // System.out.println("bfsQ.size:\t" + bfsQ.size());
            HashMap<Node, ArrayList<Node>> qFront;
            qFront = bfsQ.remove();
            Set set = qFront.entrySet();
            Iterator iterator = set.iterator();
            Node node = null;  // = qFront.getKey();
            while(iterator.hasNext()) {
                Map.Entry mEntry = (Map.Entry)iterator.next();
                node = (Node) mEntry.getKey();
            }
            // System.out.println("at:\t" + node + "Children.size():\t" + children.size());
            visited.add(node);
            for (Node child : node.getChildren()) {
                if (countNodes(child, visited) == 0) {
                    path.add(child);
                    if (child.equals(target)) {
                        return path;
                    }
                    else {
                        HashMap<Node, ArrayList<Node>> newBranch = new HashMap<>();
                        newBranch.put(child, path);
                        bfsQ.add(newBranch);
                    }
                }
            }
        }
//        System.out.println("REACHED END - NO PATH");
        path.clear();
        return path;
    }

    ArrayList<Node> iterativeDepthLimitingSearch(Node target) {
        boolean keepSearching = true;
        ArrayList<Node> path = new ArrayList<>();
        if (root != target) {
            for (int i = 0; keepSearching; i++) {
                System.out.println("\tchecking level: " + i);
                path = depthLimitedSearch(i, target);
                if (i > maxDepth || path.size() > 0) {
                    keepSearching = false;
                }
            }
        }
        else {
            path.add(root);
        }
        return path;
    }

    ArrayList<Node> depthLimitedSearch(int limit, Node target) {
        ArrayList<Node> dfsRes = depthLimitedSearchHelper(limit, root, target, new ArrayList<Node>());
//        if (dfsRes.size() == 0) {
//            System.out.println("REACHED END - NO PATH");
//
//        }
        return dfsRes;
    }

    private ArrayList<Node> depthLimitedSearchHelper(int limit, Node start, Node target, ArrayList<Node> visited) {
        visited.add(start);
        if (start.equals(target)) {
            return visited;
        }
        if (start.getDepth() < limit) {
            for (Node child : start.getChildren()) {
                if (countNodes(child, visited) == 0) {
                    ArrayList<Node> path = depthLimitedSearchHelper(limit, child, target, visited);
                    if (path.size() > 0) {
                        return path;
                    }
                }
            }
        }
        return new ArrayList<>();
        // path.clear();
        // return path;
    }

    private int countNodes(Node targetNode, ArrayList<Node> arr) {
        int count = 0;
        for (Node node : arr) {
            if (node.equals(targetNode)) {
                count++;
            }
        }
        return count;
    }

    /**
     * Adds a new node to the root of the tree in BFS order.
     * While the branch factor of a node is not met, it will
     * continue to collect child nodes until it is full. A queue
     * keeps track of the order of nodes to visit.
     * @param newNode the node to be added to the tree.
     * @return booleanValue, really not used for anything since
     *                       there is no case where a node can't
     *                       be added to a parent node somewhere
     *                       in the tree.
     */
    boolean addNodeToRoot(Node newNode) {
        ArrayList<Node> path = new ArrayList<>();
        path.add(root);
        HashMap<Node, ArrayList<Node>> vertexPath = new HashMap<>();
        Queue<HashMap<Node, ArrayList<Node>>> bfsQ = new LinkedList<>();
        vertexPath.put(root, root.getChildren());
        bfsQ.add(vertexPath);
        while (bfsQ.size() > 0) {
            HashMap<Node, ArrayList<Node>> qFront;
            qFront = bfsQ.remove();
            Set set = qFront.entrySet();
            Iterator iterator = set.iterator();
            Node node = null;  // = qFront.getKey();
            while(iterator.hasNext()) {
                Map.Entry mentry = (Map.Entry)iterator.next();
                node = (Node) mentry.getKey();
            }
            int branchFactor = node.getBranchingFactor();
            //System.out.println("node.getChildren():\t" + node.getChildren());
            if (node.getChildren().size() < branchFactor) {
//                node.getChildren().add(newNode);
                node.addChild(newNode);
                newNode.setParent(node);
                checkMaxDepth(newNode);
                nodeStorage.put(Integer.toString(newNode.getNodeNum()), newNode);
//                System.out.println("inserting newNode.d = " + newNode.getDepth());
                // System.out.println("\tCREATING NODE:\n" + node + " -> " + newNode);
                return true;
            }
            else {
                for (Node child : node.getChildren()) {
                    path.add(child);
                    // System.out.println("child:\t" + child);
                    // System.out.println("newNode:\t" + newNode);
                    if (child.getNumImmediateChildren() < branchFactor) {
//                        child.getChildren().add(newNode);
                        child.addChild(newNode);
                        newNode.setParent(child);
                        nodeStorage.put(Integer.toString(newNode.getNodeNum()), newNode);
//                        System.out.println("inserting newNode.d = " + newNode.getDepth());
                        // System.out.println("\tCREATING NODE:\n" + child + " -> " + newNode);
                        checkMaxDepth(newNode);
                        return true;
                    }
                    else {
                        HashMap<Node, ArrayList<Node>> newBranch = new HashMap<>();
                        newBranch.put(child, path);
                        bfsQ.add(newBranch);
                    }
                }
            }
        }
        return false;
    }

    void addNodeToTree(Node newNode, Node parent) {
        String numID = Integer.toString(parent.getNodeNum());
        parent = nodeStorage.get(numID);
//        System.out.println("numID:\t" + numID + parent);
        boolean addResult = tryToAdd(newNode, parent);
        String extra = "";
        if (!addResult) {
//            System.out.println("\t\tnumIMMC < BF: { " + parent.getNumImmediateChildren() + " < " + parent.getBranchingFactor() + " }");
//            if (root.getNumImmediateChildren() >= root.getBranchingFactor()){
//                root.incrementBF();
//            }
            addResult = tryToAdd(newNode, root);
            extra = "\nInstead allocated to " + root;
        }
        String result = ((addResult)? "Successfully" : "Failure");
//        System.out.println(result + " placing " + newNode + " @ " + parent + extra);
        checkMaxDepth(newNode);
        this.nodeStorage.put(Integer.toString(newNode.getNodeNum()), newNode);
    }

    private boolean tryToAdd(Node newNode, Node parent) {
//        System.out.println("numIMMC < BF: { " + parent.getNumImmediateChildren() + " < " + parent.getBranchingFactor() + " }");
        if (parent.getNumImmediateChildren() <= parent.getBranchingFactor()) {
//            System.out.println("SUCCESS");
            parent.addChild(newNode);
            newNode.setParent(parent);
//            System.out.println("\tCHECK\n" + this);
            return true;
        }
        else {
//            System.out.println("FAILURE");
            return false;
        }
    }

    private void checkMaxDepth(Node newNode) {
        int d = newNode.getDepth();
        if (this.maxDepth < d) {
            this.maxDepth = d;
            System.out.println("New max depth:\t" + maxDepth);
        }
    }

    private int calcMaxDepth(int bF, int numNodes) {
        double partA = Math.log(((bF - 1.0) * (numNodes + 1)) + 1);
        double partB = Math.log(bF);
        double partC = ((partA - partB) / partB);
        return (int) Math.ceil(partC);
    }

    String printTreeTopToBottom() {
        int borderWidth = 1;
        int charSize = 3;
        int spaceSize = 2;
        double bfToMaxDepth = Math.pow(root.getBranchingFactor(), maxDepth);
        int maxWidth = (2 * borderWidth) +
                (int) (charSize * bfToMaxDepth) +
                (int) ((spaceSize * bfToMaxDepth) - 1);
        if (maxWidth < 500) {
            StringBuilder tree = new StringBuilder("\t" + this.getID() + "\n");
            tree.append("\n");
            int currNode = 1;
            int divisor;
            for (int d = 0; d < maxDepth + 1; d++) {
//                System.out.println("nodestorage.size():\t" + nodeStorage.toString());
                divisor = (int) Math.pow(nodeStorage.get(Integer.toString(currNode)).getBranchingFactor(), d);
                int numNodesOnRow = divisor;
                int spacer = maxWidth / Math.max(2, divisor);
                StringBuilder row = new StringBuilder();
                int i = 0;
                while (i < maxWidth) {
                    if (i > 0 && i % spacer == 0) {
                        if ((currNode - 1) < nodeStorage.size() && numNodesOnRow > 0) {
                            numNodesOnRow--;
                            String num = Integer.toString(nodeStorage.get(Integer.toString(currNode)).getNodeNum());
                            currNode++;
                            StringBuilder pad = new StringBuilder();
                            for (int j = 0; j < (charSize - num.length()); j++) {
                                pad.append(" ");
                            }
                            num = pad + num + "|";
                            row.append(num);
                            i += (charSize);
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
            System.out.println("{ " + tree + " }");
        }
        else {
            System.out.println("Tree width is too wide...");
        }
//        for (int i = 0; i < 49; i++) {
//            System.out.print("0");
//        }
//        System.out.print("\n");
//        for (int i = 0; i < 6145; i++) {
//            System.out.print("0");
//        }
        return Integer.toString(maxWidth);
    }

    private String nodeToString(Node node, String res) {
        res += "\n\tCHILD" + node.toString();
        res += "\tchildren: " + node.hasChildren() + ",\tNum children:\t" + node.getNumChildren(node) + "\n";
        res += node.getChildren() + "\n";
        if (node.hasChildren()) {
            ArrayList<Node> children = node.getChildren();
            for (Node child : children) {
                res = nodeToString(child, res);
            }
        }
        return res;
    }

    private String treeToString() {
        String res = "\n\t" + this.getID() + "\n";
        res += "\n\tROOT" + root.toString();
        res += "\tRoot children: " + root.hasChildren() + ",\tNum children:\t" + root.getNumChildren(root) + "\n";
        res += root.getChildren() + "\n";
        if (root.hasChildren()) {
            ArrayList<Node> children = root.getChildren();
            for (Node child : children) {
                res = "\n"+ nodeToString(child, res) +"\n";
            }
        }
        return res;
    }

    public String toString() {
        return treeToString();
    }
}
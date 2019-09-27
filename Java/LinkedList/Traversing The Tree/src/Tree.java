/*package whatever //do not write package name here */

import java.util.ArrayList;
import java.util.Queue;
import java.util.LinkedList;
import java.util.HashMap;
import java.util.Map;
import java.util.Iterator;
import java.util.Set;

public class Tree {

    private Node root;
    private int maxDepth;
    private ArrayList<Node> nodeStorage;

    Tree(int branchingFactor, ArrayList<Integer> arr) {
        this.root = new Node(1, branchingFactor, arr);
        this.root.setParent(null);
        this.nodeStorage = new ArrayList<>();
        nodeStorage.add(this.root);
    }

    // Returns an ArrayList containing visited nodes on the way to
    // the target node.
    ArrayList<Node> depthFirstSearch(Node target) {
        ArrayList<Node> dfsRes = depthFirstSearchHelper(root, target, new ArrayList<>());
        if (dfsRes.size() == 0) {
            System.out.println("REACHED END - NO PATH");

        }
        return dfsRes;
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

    public Node getRoot() {
        return this.root;
    }

    int getNodeStorageSize() {
        return nodeStorage.size();
    }

    ArrayList<Node> getNodeStorage() {
        return nodeStorage;
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
        System.out.println("REACHED END - NO PATH");
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
        ArrayList<Node> dfsRes = depthLimitedSearchHelper(limit, root, target, new ArrayList<>());
        if (dfsRes.size() == 0) {
            System.out.println("REACHED END - NO PATH");

        }
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
                node.getChildren().add(newNode);
                newNode.setParent(node);
                checkMaxDepth(newNode);
                nodeStorage.add(newNode);
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
                        child.getChildren().add(newNode);
                        newNode.setParent(child);
                        nodeStorage.add(newNode);
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

    private void checkMaxDepth(Node newNode) {
        int d = newNode.getDepth();
        if (this.maxDepth < d) {
            this.maxDepth = d;
        }
    }

    int lookupIndex(int goalNodeId) {
        if (goalNodeId == 2) {
            goalNodeId = 1;
        }
        else if (goalNodeId == 1) {
            goalNodeId = 0;
        }
        else if (goalNodeId < 1) {
            goalNodeId = -1;
        }
        else {
            goalNodeId -= 2;
        }
        return goalNodeId;
    }

    int computeMaxDepth(Node node) {
        return node.getDepth();
    }

    String printTreeTopToBottom() {
        int borderWidth = 1;
        int charSize = 3;
        double bfToMaxDepth = Math.pow(root.getBranchingFactor(), maxDepth);
        int maxWidth = (2 * borderWidth) +
                (int) (charSize * bfToMaxDepth) +
                (int) (bfToMaxDepth - 1);

        System.out.println("maxDepth:\t" + maxDepth +
                "\nborderWidth:\t" + borderWidth +
                "\nbranchingFactor:\t" + root.getBranchingFactor() +
                "\nbfToMaxDepth:\t" + bfToMaxDepth +
                "\nmaxWidth:\t" + maxWidth);

        StringBuilder tree = new StringBuilder();
        int currNode = 0;
        int divisor;
        for (int d = 0; d < maxDepth + 1; d++) {
            divisor = (int) Math.pow(nodeStorage.get(currNode).getBranchingFactor(), d);
            int numNodesOnRow = divisor;
            int spacer = maxWidth / Math.max(2, divisor);
            double overFlowCheck = (double) maxWidth / Math.max(2, divisor);
            System.out.println("spacer:\t" + spacer + "\toverflow:\t" + overFlowCheck + "\tdivisor:\t" + Math.max(2, divisor));
            StringBuilder row = new StringBuilder();
            for (int i = 0; i < maxWidth; i++) {
                if (i > 0 && i % spacer == 0) {
                    System.out.println("i:\t" + i);
                    if (currNode < nodeStorage.size() && numNodesOnRow > 0) {
                        numNodesOnRow--;
                        String num = Integer.toString(nodeStorage.get(currNode).getNodeNum());
                        currNode++;
                        StringBuilder pad = new StringBuilder();
                        for (int j = 0; j < (charSize - num.length()); j++) {
                            pad.append(" ");
                        }
                        num = pad + num;
                        row.append(num);
//                        double x = (overFlowCheck * (i / Math.max(2, divisor)));
//                        if (x >= maxWidth) {
//                            System.out.println("X:\t" + x);
//                            break;
//                        }
                    }

                }
                else {
                    row.append(" ");
                }
            }
            row.append("\n");
            tree.append(row);
        }
        System.out.println("{ " + tree + " }");
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
        String res = "";
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
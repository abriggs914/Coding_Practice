/*package whatever //do not write package name here */

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.util.Queue;
import java.util.LinkedList; 
import java.util.HashMap; 
import java.util.Map;
import java.util.Iterator;
import java.util.Set;

public class Tree {
    
    public static int numNodes = 0;
    
    private static class Node{
        
        ArrayList<Integer> arr;
        ArrayList<Node> children;
        int depth;
        int arrSum;
        int nodeNum;
        int branchFactor;
        Node parent;
        
        public Node(int branchingFactor, ArrayList<Integer> arr) {
            this.arr = arr;
            this.parent = null;
            this.arrSum = sum(arr);
            this.branchFactor = branchingFactor;
            this.children = new ArrayList<Node>();
            numNodes++;
            this.nodeNum = numNodes;
        }
        
        public void setParent(Node parent) {
            this.parent = parent;
            if (parent == null) {
                this.depth = 0;
            }
            else {
                this.depth = parent.depth + 1;
            }
        }
        
        public int sum(ArrayList<Integer> arr) {
            int sum = 0;
            for (int el : arr) {
                sum += el;
            }
            return sum;
        }
        
        public int getNumImmediateChildren() {
            return this.getChildren().size();
        }
        
        public int getNumChildren(Node node) {
            if (node == null) {
                return 0;
            }
            else{
                int numChildren = 0;
                for(int i = 0; i < node.getChildren().size(); i++) {
                    numChildren += 1 + getNumChildren(node.getChildren().get(i));
                }
                return numChildren;
            }
        }
        
        public ArrayList<Node> getChildren() {
            return this.children;
        }
        
        public int getBranchingFactor() {
            return this.branchFactor;
        }
        
        public int getDepth() {
            return this.depth;
        }
        
        public void setDepth(int d) {
            this.depth = d;
        }
        
        public int getArrSum() {
            return this.arrSum;
        }
        
        public boolean hasChildren() {
            return this.getArr().size() != 0;
        }
        
        public ArrayList<Integer> getArr() {
            return this.arr;
        }
        
        public String toString() {
            String res = "  { NodeNumber: " + this.nodeNum +
                         ",\tDepth: " + this.getDepth() + 
                         ",\t#immC: " + this.getNumImmediateChildren() +
                         ",\t#children: " + this.getNumChildren(this) + "} "; // +
                        //  "\nARR\n" + this.getArr().toString() +
                        //  "sum:\t" + this.getArrSum() + "\n";
            return res;
        }
    }
    
    public static Node root;
    public static int branchingFactor;
    
    // public static int getBranchingFactor() {
    //     return this.branchingFactor;
    // }
    
    public Tree(int branchingFactor, ArrayList<Integer> arr) {
        this.branchingFactor = branchingFactor;
        this.root = new Node(branchingFactor, arr);
        this.root.setParent(null);
	}
	
	// Returns an ArrayList contianing visited nodes on the way to
	// the target node.
	
	public ArrayList<Node> depthFirstSearch(Node target) {
	    ArrayList<Node> dfsRes = depthFirstSearchHelper(root, target, new ArrayList<Node>());
	    if (dfsRes.size() == 0) {
	        System.out.println("REACHED END - NO PATH");
	        
	    }
	    return dfsRes;
	}
	
	public ArrayList<Node> depthFirstSearchHelper(Node start, Node target, ArrayList<Node> visited) {
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
	     return new ArrayList<Node>();
	       // path.clear();
	       // return path;
	}
	
	// Returns an ArrayList contianing visited nodes on the way to
	// the target node.
	
	public ArrayList<Node> breadthFirstSearch(Node target) {
	    ArrayList<Node> path = new ArrayList<Node>();
	    path.add(root);
	    if (root == target) {
	        return path;
	    }
	    HashMap<Node, ArrayList<Node>> vertexPath = new HashMap<>(); 
	    Queue<HashMap<Node, ArrayList<Node>>> bfsQ = new LinkedList<>();
	    vertexPath.put(root, root.getChildren());
	    bfsQ.add(vertexPath);
	    ArrayList<Node> visited = new ArrayList<Node>();
	    while (bfsQ.size() > 0) {
	       // System.out.println("bfsQ.size:\t" + bfsQ.size());
	        HashMap<Node, ArrayList<Node>> qFront;
	        qFront = bfsQ.remove();
	        Set set = qFront.entrySet();
	        Iterator iterator = set.iterator();
	        Node node = null;  // = qFront.getKey();
	        while(iterator.hasNext()) {
	            Map.Entry mentry = (Map.Entry)iterator.next();
	            node = (Node) mentry.getKey();
	        }
	       // System.out.println("at:\t" + node + "Children.size():\t" + children.size());
	        visited.add(node);
	       // Iterator<Node> iter = children.iterator();
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
	
	public static int countNodes(Node targetNode, ArrayList<Node> arr) {
	    int count = 0;
	    for (Node node : arr) {
	        if (node.equals(targetNode)) {
	            count++;
	        }
	    }
	    return count;
	}
	
	public static boolean addNodeToRoot(Node newNode) {
	    ArrayList<Node> path = new ArrayList<Node>();
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
	                   // System.out.println("\tCREATING NODE:\n" + child + " -> " + newNode);
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
	
	public static ArrayList<Integer> genRandomArray(int n) {
	    ArrayList<Integer> arr = new ArrayList<Integer>();
	    Random rnd = new Random();
	    for (int i = 0; i < n; i++) {
	        arr.add(rnd.nextInt(100));
	    }
	    return arr;
	}
	
	public static int lookupIndex(int goalNodeId) {
	    if (goalNodeId == 2) {
	        goalNodeId = 0;
	    }
	    else if (goalNodeId <= 1) {
	        goalNodeId = -1;
	    }
	    else if (goalNodeId > 2) {
	        goalNodeId -= 2;
	    }
	    return goalNodeId;
	}
	
	public static int computeMaxDepth(Node node) {
	    return node.getDepth();
	}
	
	public static String printTreeTopToBottom(int maxDepth) {
	    int borderWidth = 1; 
	    double bfToMaxDepth = Math.pow(root.getBranchingFactor(), maxDepth);
	    int maxWidth = (2 * borderWidth) +
	                   (int) (2 * bfToMaxDepth) +
	                   (int) (bfToMaxDepth - 1);
	    System.out.println("maxDepth:\t" + maxDepth +
	                       "\nborderWidth:\t" + borderWidth +
	                       "\nbranchingFactor:\t" + root.getBranchingFactor() + 
	                       "\nbfToMaxDepth:\t" + bfToMaxDepth + 
	                       "\nmaxWidth:\t" + maxWidth);
	    return Integer.toString(maxWidth);
	}
    
	public static void main (String[] args) {
	    
	    /////////////////////////////////////////
	    int branchingFactor = 2;
	    int numNodes = 25; // including root
	    int goalNodeId = 25;
	    ////////////////////////////////////////
	    
	    Node[] nodeStorage = new Node[numNodes];
	    ArrayList<Integer> arr = genRandomArray(10);
	    Tree t = new Tree(branchingFactor, arr);
	    int maxDepth = 0;
	    boolean addResult;
	    for (int i = 0; i < numNodes - 1; i++) {
	        arr = genRandomArray(10);
	        Node newNode = new Node(branchingFactor, arr);
	        nodeStorage[i] = newNode;
	        addResult = t.addNodeToRoot(newNode);
	       // System.out.println("addResult:\t" + ((addResult)? "Successful" : "Failure") + "\n\n");
	        if (i == (numNodes - 2)) {
	            maxDepth = computeMaxDepth(newNode);
	        }
	    }
	   // Print tree
	   // System.out.println(t);
	   
	   // System.out.println(nodeStorage[nodeStorage.length- 1]);
	   // int maxDepth = computeMaxDepth(nodeStorage[nodeStorage.length - 1]);
	    System.out.println(t.printTreeTopToBottom(maxDepth));
	    
	    // Searching:
	    int indexOfChoice = lookupIndex(goalNodeId);
	    Node targetNode;
	    if (indexOfChoice < 0) {
	        targetNode = root;
	    }
	    else {
	        targetNode = ((indexOfChoice < nodeStorage.length)? 
	                            nodeStorage[indexOfChoice] :
	                            null);
	    }
	   // System.out.println(Arrays.toString(nodeStorage));
	    
	    System.out.println();
	    System.out.println("\tBFS\n");
	    ArrayList<Node> path = t.breadthFirstSearch(targetNode);
	    System.out.println("\tANSWER:\n" + targetNode + "\n\tPATH:\n");
	    for (Node visitedNode : path) {
	        System.out.println(" -> " + visitedNode);
	    }
	    System.out.println("\n\tPATH.SIZE():\n" + path.size());
	    System.out.println();
	    
	    System.out.println("\tDFS\n");
	    path = t.depthFirstSearch(targetNode);
	    System.out.println("\tANSWER:\n" + targetNode + "\n\tPATH:\n");
	    for (Node visitedNode : path) {
	        System.out.println(" -> " + visitedNode);
	    }
	    System.out.println("\n\tPATH.SIZE():\n" + path.size());
	    System.out.println();
	    
// 		System.out.println("GfG!");
	}
	
	public String nodeToString(Node node, String res) {
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
	
	public String treeToString() {
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
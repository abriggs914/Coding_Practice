import java.util.ArrayList;
import java.util.HashMap;
import java.util.Queue;
import java.util.LinkedList;
import java.util.Set;
import java.util.Map;
import java.util.Iterator;
import java.util.Random;

/**
 * 
 * Java project to create a binary search tree and
 * perform bread-first and depth-first searches.
 * 
 * Sept. 25 / 2019
 * Avery Briggs
 * 
*/

class BSTTraversals {
    
    public static Node root;
    
    public static Random rnd = new Random();
    
    public static class Node {
        Node left; 
        Node right;
        Node parent;
        int data;
        int iD;
        int depth;
        public Node(Node left, Node right, Node parent, int val, int id) {
            this.iD = id;
            this.parent = parent;
            this.left = left;
            this.right = right;
            this.data = val;
        }
        
        public void adjustDepth() {
            Node parent = this.parent;
            if (parent == null) {
                this.depth = 0;
            }
            else {
                this.depth = parent.depth + 1;
            }
        }
        
        public ArrayList<Node> getChildren() {
            ArrayList<Node> arr = new ArrayList<Node>();
            Node left = this.getLeft();
            Node right = this.getRight();
            if (left != null) {
                arr.add(left);
            }
            if (right != null) {
                arr.add(right);
            }
            return arr;
        }
        
        public Node getRight() {
            return this.right;
        }
        
        public Node getLeft() {
            return this.left;
        }
        
        public String toString() {
            String res = "node:\t" + this.iD + ", data:\t" + this.data;
            Node left = this.getLeft();
            Node right = this.getRight();
            String depthSpace = "\t";
            for (int i = 0; i < this.depth; i++) {
                depthSpace += "\t";
            }
            res += "\n" + depthSpace + "left: ";
            if (left != null) {
                res += "{ " + left + " }";
            }
            else {
                res += "empty";
            }
            res += "\n" + depthSpace + "right: ";
            if (right != null) {
                res +="{ " + right + " }";
            }
            else {
                res += "empty";
            }
            return res;
        }
    }
    
    public static ArrayList<Node> depthFirstSearch(Node target) {
        ArrayList<Node> path = depthFirstSearchHelper(root, target, new ArrayList<Node>());
	    if (path.size() == 0) {
	     System.out.println("REACHED END - NO PATH");
	    }
	    return path;
	}
	
	public static ArrayList<Node> depthFirstSearchHelper(Node start, Node target, ArrayList<Node> visited) {
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
	
	public static ArrayList<Node> breadthFirstSearch(Node target) {
	    ArrayList<Node> path = new ArrayList<Node>();
	    path.add(root);
	    HashMap<Node, ArrayList<Node>> vertexPath = new HashMap<>(); 
	    Queue<HashMap<Node, ArrayList<Node>>> bfsQ = new LinkedList<>();
	   // ArrayList<Node> children = new ArrayList<Node>();
	   // children.add(root.getLeft());
	   // children.add(root.getRight());
	    vertexPath.put(root, root.getChildren());
	    bfsQ.add(vertexPath);
	    ArrayList<Node> visited = new ArrayList<Node>();
	    while (bfsQ.size() > 0) {
	        System.out.println("bfsQ.size:\t" + bfsQ.size());
	        HashMap<Node, ArrayList<Node>> qFront;
	        qFront = bfsQ.remove();
	        Set set = qFront.entrySet();
	        Iterator iterator = set.iterator();
	        Node node = null;  // = qFront.getKey();
	        while(iterator.hasNext()) {
	            Map.Entry mentry = (Map.Entry)iterator.next();
	            node = (Node) mentry.getKey();
	           // System.out.println(mentry.getValue());
	        }
	       // ArrayList<Node> childrenO = (ArrayList<Node>) qFront.get(node);
	       // ArrayList<Node> children = new ArrayList<Node>();
	       // children.addAll(childrenO);
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
	
    public static void bstInsertRecurs(Node rt, Node node){
        if(node.data <= rt.data){
            if(rt.left == null){
                rt.left = node;
                node.parent = rt;
                node.adjustDepth();
            }
            else{
                bstInsertRecurs(rt.left, node);
            }
        }
        else{
            if(rt.right == null){
                rt.right = node;
                node.parent = rt;
                node.adjustDepth();
            }
            else{
                bstInsertRecurs(rt.right, node);
            }
        }
    }

    public static Node bstInsert(Node rt, Node node){
        int i;
        if(rt == null){
            root = node;
            root.adjustDepth();
            return node;
        }
        bstInsertRecurs(rt, node);
        // for(i = 0; i < n; i++){
        //     System.out.println("i: " + i);
        //     node.data = arr[i];
        //     tree[i] = node;
        //     if(i == 0){
        //         root = node;
        //         root.left = root.right = null;
        //     }
        // }
        return node;
    }
    
	public static void main (String[] args) {
		root = null;
		int v = 0;
		int[] arr = {6,4,8,3,5,7,9};
		
		
		int numNodes = arr.length;
		Node[] nodeStorage = new Node[numNodes];
		for (int i = 0; i < numNodes; i++) {
		  //  v = rnd.nextInt(1000);
		  //  Node newNode = new Node(null, null, null, v, i);
		    Node newNode = new Node(null, null, null, arr[i], i);
		    nodeStorage[i] = newNode;
		    bstInsert(root, newNode);
		}
    
	    // Searching:
	    
	    Node targetNode = nodeStorage[5];
	    
	    System.out.println();
	    System.out.println("\n\tBFS\n");
	    ArrayList<Node> path = breadthFirstSearch(targetNode);
	    System.out.println("\tANSWER:\n" + targetNode + "\n\tPATH:\n");
	    for (Node nodeVisited : path) {
	        System.out.println("\t" + nodeVisited);
	    }
	    System.out.println("\n\tPATH.SIZE():\n");
	    System.out.println(path.size());
	    
	    System.out.println("\n\tDFS\n");
	    path = depthFirstSearch(targetNode);
	    System.out.println("\tANSWER:\n" + targetNode + "\n\tPATH:\n");
	    System.out.println(path + "\n\tPATH.SIZE():\n");
	    System.out.println(path.size());

	}
}
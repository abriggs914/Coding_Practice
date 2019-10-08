package com.example.abrig.tictactoeapp;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;

public class Node {
    private ArrayList<Integer> arr;
    private ArrayList<Node> children;
    private int depth;
    private int arrSum;
    private int nodeNum;
    private int branchFactor;
    private boolean isLeafNode;
    private boolean isMaxNode;
    private boolean isMiniMaxNode;
    private Node parent;
    private String letterID;

    private int alpha;
    private int beta;
    private int value;

    Node(int nodeNum, int branchingFactor, ArrayList<Integer> arr) {
        this.arr = arr;
        this.parent = null;
        this.arrSum = sum(arr);
        this.branchFactor = branchingFactor;
        this.children = new ArrayList<>();
        this.nodeNum = nodeNum;
        this.isLeafNode = true;
        this.isMaxNode = true;
        this.letterID = genLetterID();
        initValue();
    }

    Node (int nodeNum, int branchingFactor, int[] arrIn) {
        ArrayList<Integer> arr = new ArrayList<>();
        for (int i = 0; i < arrIn.length; i++) {
            arr.add(arrIn[i]);
        }
        this.arr = arr;
        this.parent = null;
        this.arrSum = sum(arr);
        this.branchFactor = branchingFactor;
        this.children = new ArrayList<>();
        this.nodeNum = nodeNum;
        this.isLeafNode = true;
        this.isMaxNode = true;
        this.letterID = genLetterID();
        initValue();
    }

    Node (int nodeNum, int branchingFactor, int val) {
        ArrayList<Integer> arr = new ArrayList<>();
        arr.add(val);
        this.arr = arr;
        this.parent = null;
        this.arrSum = sum(arr);
        this.branchFactor = branchingFactor;
        this.children = new ArrayList<>();
        this.nodeNum = nodeNum;
        this.isLeafNode = true;
        this.isMaxNode = true;
        this.letterID = genLetterID();
        initValue();
    }

    void setParent(Node parent) {
        this.parent = parent;
        if (parent == null) {
            this.depth = 0;
        }
        else {
            this.depth = parent.depth + 1;
            parent.setNonLeaf();
//            parent.getChildren().add(this);
        }
        this.initAlpha();
        this.initBeta();
    }

    private int sum(ArrayList<Integer> arr) {
        int sum = 0;
        for (int el : arr) {
            sum += el;
        }
        return sum;
    }

    int getNumImmediateChildren() {
        return this.getChildren().size();
    }

    int getNumChildren(Node node) {
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

    ArrayList<Node> getChildren() {
        return this.children;
    }

    void addChild(Node child) {
        if (getNumImmediateChildren() < getBranchingFactor()) {
            this.getChildren().add(child);
        }
        else {
            incrementBF();
            this.getChildren().add(child);
        }
    }

    int getBranchingFactor() {
        return this.branchFactor;
    }

    void incrementBF() {
        this.branchFactor += 1;
    }

    int getDepth() {
        return this.depth;
    }

    public void setDepth(int d) {
        this.depth = d;
    }

    int getArrSum() {
        return this.arrSum;
    }

    int getNodeNum() {
        return nodeNum;
    }

    boolean hasChildren() {
        return this.getChildren().size() != 0;
    }

    void pruneChildren() {
        this.children.clear();
    }

    ArrayList<Integer> getArr() {
        return this.arr;
    }

    public String toString() {
        String res = "";
//        if (this.parent != null) {
//            res = " { Parent#: " + this.parent.nodeNum +
//                    ",  pDepth: " + this.parent.getDepth() +
//                    ",  #PimmC: " + this.parent.getNumImmediateChildren() +
//                    ",  #Pchildren: " + this.parent.getNumChildren(this.parent) + "} ->";
//        }
        res += " { Node#: " + this.nodeNum + "( " + this.getLetterID() + " )" +
                ",  D: " + this.getDepth() +
                ",  BF: " + this.getBranchingFactor() +
                ",  #immC: " + this.getNumImmediateChildren() +
                ",  #kids: " + this.getNumChildren(this) +
                ",  Arr: " + this.getArr() +
                ", value: " + this.getValue();
//        if (this.hasChildren()) {
//            res += ",  favChild.id: " + this.getFavouriteChild().getNodeNum() +
//                   ",  score: " + this.getFavouriteChild().getArrSum();
//        }
        res += " } ";
        //  "\nARR\n" + this.getArr().toString() +
//          "sum:\t" + this.getArrSum() + "\n";
        return res;
    }

    // returns its eldest (furthest left) child
     Node getFavouriteChild() {
        return this.getChildren().get(0);
    }

    void initAlpha() {
        this.alpha = Integer.MIN_VALUE;
    }

    void initBeta() {
        this.beta = Integer.MAX_VALUE;
    }

    void initValue() {
        this.value = sum(this.getArr());
    }

//    void updateValue() {
//        this.value = sum(arr);
//    }

    void setValue(int value) {
        this.value = value;
    }

    void setAlpha(int value) {
        this.alpha = value;
    }

    void setBeta(int value) {
        this.beta = value;
    }

    int getValue() {
        return this.value;
    }

    int getAlpha() {
        return this.alpha;
    }

    int getBeta() {
        return this.beta;
    }

    // parent node will call this
    private void setNonLeaf() {
        this.isLeafNode = false;
//        this.getParent().
        this.initValue();
    }

    boolean getLeafStatus() {
        return this.isLeafNode;
    }

    Node getParent() {
        return this.parent;
    }

    boolean isDecendantOf(Node ancestor) {
        Node currNode = this;
        while (currNode.getParent() != null) {
            if (currNode.getNodeNum() == ancestor.getNodeNum()) {
                return true;
            }
            currNode = currNode.getParent();
        }
        return false;
    }

    boolean isDecendantOfNodeInList(ArrayList<Node> possibleAncestors) {
        boolean isAncestor = false;
        for (Node ancestor : possibleAncestors) {
            isAncestor = this.isDecendantOf(ancestor);
            if (isAncestor) {
//                System.out.println(this + " is a decendant of " + ancestor);
                return true;
            }
        }
        return isAncestor;
    }

    boolean getIsMaxNode() {
        return this.isMaxNode;
    }

    boolean getIsMiniMaxNode() {
        return this.isMiniMaxNode;
    }

    void setIsMinNode() {
        this.isMaxNode = false;
    }

    void setIsMiniMaxNode() {
        this.isMiniMaxNode = true;
    }

    String getLetterID() {
        return this.letterID;
    }

    public String genLetterID() {
        int getNodeNum = this.getNodeNum();
        int p;
        int divides26 = getNodeNum;
        ArrayList<Integer> digits = new ArrayList<>();
        if (getNodeNum > 0 && getNodeNum < 27) {
            digits.add(divides26);
        }
        else {
            while (divides26 > 1) {
                p = divides26 % 26;
                if (p == 0) {
                    digits.add(26);
                }
                else {
                    digits.add(p);
                }
                divides26 /= 26;
            }
            if (divides26 < 27 && divides26 > 0) {
                digits.add(divides26);
            }
        }
        String letter = "";
        for (int alphabetIdx : digits) {
            letter = (char)  (alphabetIdx + 64) + letter;
        }
        return letter;
    }
}

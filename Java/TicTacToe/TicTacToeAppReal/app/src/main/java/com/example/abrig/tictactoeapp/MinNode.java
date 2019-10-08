package com.example.abrig.tictactoeapp;

import java.util.ArrayList;

class MinNode extends Node {

    MinNode(int nodeNum, int branchingFactor, ArrayList<Integer> arr) {
        super(nodeNum, branchingFactor, arr);
        this.initValue();
        this.setIsMinNode();
    }

    MinNode(int nodeNum, int branchingFactor, int[] arrIn) {
        super(nodeNum, branchingFactor, arrIn);
        this.initValue();
        this.setIsMinNode();
    }

    MinNode(int nodeNum, int branchingFactor, int val) {
        super(nodeNum, branchingFactor, val);
        this.initValue();
        this.setIsMinNode();
    }

    void initValue() {
        if (this.getLeafStatus()) {
            this.setValue(this.getArrSum());
        }
        else {
            this.setValue(Integer.MAX_VALUE);
        }
        this.setIsMiniMaxNode();
    }

//    void updateValue() {
//        ArrayList<Node> children = this.getChildren();
//        System.out.print("updating:\t" + this);
//        int thisValue = this.getValue();
//        for (Node child : children) {
//            if (child.hasChildren()) {
//                child.updateValue();
//            }
//            else {
//                int childValue = child.getValue();
//                System.out.println("thisVal: " + thisValue + ", childVal: " + childValue);
//                if (childValue < thisValue) {
//                    this.setValue(childValue);
//                    thisValue = this.getValue();
//                }
//                if (thisValue <= this.getAlpha()) {
//                    break;
//                } else if (thisValue < this.getBeta()) {
//                    this.setBeta(thisValue);
//                }
//            }
////            child.updateValue();
//        }
//        System.out.println("\n\t->\t" + this);
//    }

    // returns min of children
    Node getFavouriteChild() {
        ArrayList<Node> children = this.getChildren();
        int minNodeVal = Integer.MAX_VALUE;
        Node minChild = null;
        for (Node child : children) {
            if (child.getArrSum() < minNodeVal) {
                minNodeVal = child.getArrSum();
                minChild = child;
            }
        }
        if (minChild == null) {
            return this;
        }
        else {
            return minChild;
        }
    }

    public String toString() {
        String res = "";
        res += " (Min) { Node#: " + this.getNodeNum() + ", ( " + this.getLetterID()  + " )" +
                ",  D: " + this.getDepth() +
                ",  #immC: " + this.getNumImmediateChildren() +
                ",  BF: " + this.getBranchingFactor() +
                ",  val: " + this.getValue() +
                ",  alpha: " + this.getAlpha() +
                ",  beta: " + this.getBeta();
//                ",  Arr: " + this.getArrSum();
        res += " } ";
        return res;
    }
}

package com.example.abrig.tictactoeapp;

import java.util.ArrayList;

class MaxNode extends Node {

    MaxNode(int nodeNum, int branchingFactor, ArrayList<Integer> arr) {
        super(nodeNum, branchingFactor, arr);
        this.initValue();
    }

    MaxNode(int nodeNum, int branchingFactor, int[] arrIn) {
        super(nodeNum, branchingFactor, arrIn);
        this.initValue();
    }

    MaxNode(int nodeNum, int branchingFactor, int val) {
        super(nodeNum, branchingFactor, val);
        this.initValue();
    }

    void initValue() {
        if (this.getLeafStatus()) {
            this.setValue(this.getArrSum());
        }
        else {
            this.setValue(Integer.MIN_VALUE);
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
//                if (childValue > thisValue) {
//                    this.setValue(childValue);
//                    thisValue = this.getValue();
//                }
//                if (thisValue >= this.getBeta()) {
//                    break;
//                } else if (thisValue > this.getAlpha()) {
//                    this.setAlpha(thisValue);
//                }
//            }
////            child.updateValue();
//        }
//        System.out.println("\n\t->\t" + this);
//    }

    // returns max of children
    Node getFavouriteChild() {
        ArrayList<Node> children = this.getChildren();
        int maxNodeVal = Integer.MIN_VALUE;
        Node maxChild = null;
        for (Node child : children) {
            if (child.getArrSum() > maxNodeVal) {
                maxNodeVal = child.getArrSum();
                maxChild = child;
            }
        }
        if (maxChild == null) {
            return this;
        }
        else {
            return maxChild;
        }
    }

    public String toString() {
        String res = "";
        res += " (Max) { Node#: " + this.getNodeNum() + ", ( " + this.getLetterID()  + " )" +
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

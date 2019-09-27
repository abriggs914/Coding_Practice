import java.util.ArrayList;

public class MaxNode extends Node {
    MaxNode(int nodeNum, int branchingFactor, ArrayList<Integer> arr) {
        super(nodeNum, branchingFactor, arr);
    }

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

//    public String toString() {
//        String res = "root ->";
////            if (this.parent != null) {
////                res = " { Parent#: " + this.parent.nodeNum +
////                        ",  pDepth: " + this.parent.getDepth() +
////                        ",  #PimmC: " + this.parent.getNumImmediateChildren() +
////                        ",  #Pchildren: " + this.parent.getNumChildren(this.parent) + "} ->";
////            }
//        res += " { NodeNumber: " + this.getNodeNum() +
//                ",  Depth: " + this.getDepth() +
//                ",  #immC: " + this.getNumImmediateChildren() +
//                ",  #children: " + this.getNumChildren(this);
//        if (this.hasChildren()) {
//            res += ",  favChild: " + this.getFavouriteChild();
//        }
//        res += " } ";
//        //  "\nARR\n" + this.getArr().toString() +
//        //  "sum:\t" + this.getArrSum() + "\n";
//        return res;
//    }
}

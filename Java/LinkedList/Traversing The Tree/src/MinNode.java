import java.util.ArrayList;

public class MinNode extends Node {

    MinNode(int nodeNum, int branchingFactor, ArrayList<Integer> arr) {
        super(nodeNum, branchingFactor, arr);
    }

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

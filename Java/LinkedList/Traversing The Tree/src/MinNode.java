import java.util.ArrayList;

class MinNode extends Node {

    MinNode(int nodeNum, int branchingFactor, ArrayList<Integer> arr) {
        super(nodeNum, branchingFactor, arr);
        this.initValue();
    }

    void initValue() {
        if (this.getLeafStatus()) {
            this.setValue(this.getArrSum());
        }
        else {
            this.setValue(Integer.MAX_VALUE);
        }
    }

    void updateValue() {
        ArrayList<Node> children = this.getChildren();
        System.out.print("updating:\t" + this);
        int thisValue = this.getValue();
        for (Node child : children) {
            if (child.hasChildren()) {
                child.updateValue();
            }
            else {
                int childValue = child.getValue();
                System.out.println("thisVal: " + thisValue + ", childVal: " + childValue);
                if (childValue < thisValue) {
                    this.setValue(childValue);
                    thisValue = this.getValue();
                }
                if (thisValue <= this.getAlpha()) {
                    break;
                } else if (thisValue < this.getBeta()) {
                    this.setBeta(thisValue);
                }
            }
//            child.updateValue();
        }
        System.out.println("\n\t->\t" + this);
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

    public String toString() {
        String res = "";
//        if (this.parent != null) {
//            res = " { Parent#: " + this.parent.nodeNum +
//                    ",  pDepth: " + this.parent.getDepth() +
//                    ",  #PimmC: " + this.parent.getNumImmediateChildren() +
//                    ",  #Pchildren: " + this.parent.getNumChildren(this.parent) + "} ->";
//        }
        res += " (Min) { Node#: " + this.getNodeNum() +
                ",  D: " + this.getDepth() +
                ",  #immC: " + this.getNumImmediateChildren() +
                ",  val: " + this.getValue() +
                ",  alpha: " + this.getAlpha() +
                ",  beta: " + this.getBeta();
//                ",  #kids: " + this.getNumChildren(this) +
//                ",  Arr: " + this.getArrSum();
//        if (this.hasChildren()) {
//            res += ",  favChild.id: " + this.getFavouriteChild().getNodeNum() +
//                    ",  score: " + this.getFavouriteChild().getArrSum();
//        }
        res += " } ";
        //  "\nARR\n" + this.getArr().toString() +
//          "sum:\t" + this.getArrSum() + "\n";
        return res;
    }
}

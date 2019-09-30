import java.util.ArrayList;

class MaxNode extends Node {

    MaxNode(int nodeNum, int branchingFactor, ArrayList<Integer> arr) {
        super(nodeNum, branchingFactor, arr);
        this.initValue();
    }

    void initValue() {
        if (this.getLeafStatus()) {
            this.setValue(this.getArrSum());
        }
        else {
            this.setValue(Integer.MIN_VALUE);
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
                if (childValue > thisValue) {
                    this.setValue(childValue);
                    thisValue = this.getValue();
                }
                if (thisValue >= this.getBeta()) {
                    break;
                } else if (thisValue > this.getAlpha()) {
                    this.setAlpha(thisValue);
                }
            }
//            child.updateValue();
        }
        System.out.println("\n\t->\t" + this);
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

    public String toString() {
        String res = "";
//        if (this.parent != null) {
//            res = " { Parent#: " + this.parent.nodeNum +
//                    ",  pDepth: " + this.parent.getDepth() +
//                    ",  #PimmC: " + this.parent.getNumImmediateChildren() +
//                    ",  #Pchildren: " + this.parent.getNumChildren(this.parent) + "} ->";
//        }
        res += " (Max) { Node#: " + this.getNodeNum() +
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

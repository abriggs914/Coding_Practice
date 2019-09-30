import java.util.ArrayList;

public class Node {
    private ArrayList<Integer> arr;
    private ArrayList<Node> children;
    private int depth;
    private int arrSum;
    private int nodeNum;
    private int branchFactor;
    private boolean isLeafNode;
    private Node parent;

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
    }

    void setParent(Node parent) {
        this.parent = parent;
        if (parent == null) {
            this.depth = 0;
        }
        else {
            this.depth = parent.depth + 1;
            parent.setNonLeaf();
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

    int getBranchingFactor() {
        return this.branchFactor;
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
        res += " { Node#: " + this.nodeNum +
                ",  D: " + this.getDepth() +
                ",  #immC: " + this.getNumImmediateChildren() +
                ",  #kids: " + this.getNumChildren(this) +
                ",  Arr: " + this.getArrSum();
        if (this.hasChildren()) {
            res += ",  favChild.id: " + this.getFavouriteChild().getNodeNum() +
                   ",  score: " + this.getFavouriteChild().getArrSum();
        }
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
        this.value = -99;
    }

    void updateValue() {

    }

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
            if (currNode == ancestor) {
                return true;
            }
            currNode = currNode.getParent();
        }
        return false;
    }
}

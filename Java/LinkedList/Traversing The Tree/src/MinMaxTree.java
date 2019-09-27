import java.util.*;

public class MinMaxTree extends Tree {

    private Node root;
    private boolean rootIsMaxNode;
    private int maxDepth;


    MinMaxTree(int branchingFactor, ArrayList<Integer> arr, boolean rootIsMaxNode) {
        super(branchingFactor, arr);
        this.rootIsMaxNode = rootIsMaxNode;
        if (rootIsMaxNode) {
            this.root = new MaxNode(1, branchingFactor, arr);
        }
        else {
            this.root = new MinNode(1, branchingFactor, arr);
        }
        this.root.setParent(null);
    }
}

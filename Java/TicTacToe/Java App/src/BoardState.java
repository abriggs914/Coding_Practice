import java.util.ArrayList;
import java.util.List;

public class BoardState {

//    private int numBoardStatesCreated = 0;

    public int[][] boardState;
    public ArrayList<BoardState> childStates;
    public TicTacToe tttObject;
    public int depth;
    public boolean leafBoard;

    // TicTacToe object passed in is the parent to the
    // one being created currently.
    public BoardState(TicTacToe ttt, int[][] state) {
        this.boardState = state;
        this.childStates = new ArrayList<BoardState>();
        this.depth = ttt.gameTurnNum;
        this.tttObject = ttt;
        if (this.getCurrDepth() < 10 && this.getCurrDepth() > 0) {
            this.leafBoard = false;
        }
        else {
            this.leafBoard = true;
            System.out.println("LEAF BOARD NODE");
        }
//        System.out.println("numBoardStatesCreated:\t" + numBoardStatesCreated);
    }

    public String toString() {
        String res = this.tttObject.getPrintBoardString(this.getBoardState());
        return res;
    }

    public int[][] getBoardState() {
        return this.boardState;
    }

    public int getCurrDepth() {
        return this.depth;
    }

    public boolean getLeafStatus() {
        return this.leafBoard;
    }

    public ArrayList<BoardState> getChildStates() {
        return this.childStates;
    }

    public void addChildState(TicTacToe ttt, int[][] state) {
        BoardState childState = new BoardState(ttt, state);
        this.childStates.add(childState);
    }

}
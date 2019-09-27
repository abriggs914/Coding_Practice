import java.util.ArrayList;
import java.util.Arrays;

public class TicTacToe {

    final private boolean PRINT_STATEMENTS = false;

    public int playerSymbol; // stores 1 or 3 meaning player is 'X' or 'O'.
    public int aiSymbol; // stores 1 or 3 meaning computer is 'X' or 'O'.
    public int gameTurnNum; // keeps track of the games turn number.
    public int numBoardStatesCreated = 0;
    public BoardState boardTree; // a node that stores the current TicTacToe
                                 // board and which squares are marked.

    // Starts tree after first move to cut computation 9! -> 8!
    public TicTacToe(boolean playerWentFirst, int symbol, int firstMoveLocation) {
        int[][] initialBoard = getInitialBoardState();
        this.playerSymbol = ((playerWentFirst)? symbol : ((symbol == 1)? 3 : 1));
        this.aiSymbol = getAISymbol();
        this.gameTurnNum = 0;
        resetTurnNumber();
        initialBoard = handleFirstMove(symbol, firstMoveLocation, initialBoard);
        this.boardTree = new BoardState(this, initialBoard);
//        numBoardStatesCreated++;
//        System.out.println("\t# BoardStatesCreated\t" + numBoardStatesCreated);
//        printBoard(initialBoard);

//        expandTree(playerWentFirst, symbol, getBoardTree());

        int resultCode = checkBoardForWinner(initialBoard);
        if (PRINT_STATEMENTS) {
            System.out.println("\tResultCode:\t" + resultCode);
            System.out.println("\n\tConstructor TTT\n");
        }
    }

    // .
    // Accepts pre-determined moves on the board when it is created.
    public TicTacToe(boolean playerWentFirst, int symbol, int firstMoveLocation, int[][] postitionSymbol) {
        int[][] initialBoard = getInitialBoardState();
        this.playerSymbol = ((playerWentFirst)? symbol : ((symbol == 1)? 3 : 1));
        this.aiSymbol = getAISymbol();
        this.gameTurnNum = 0;
        resetTurnNumber();
        initialBoard = handleTestMoves(symbol, firstMoveLocation, initialBoard, postitionSymbol);
        // initialBoard can be empty, partially filled, or completely filled

        // Create a parent state
        this.boardTree = new BoardState(this, initialBoard);
//        numBoardStatesCreated++;
//        System.out.println("\t# BoardStatesCreated\t" + numBoardStatesCreated);
        if (PRINT_STATEMENTS) {
            System.out.println("\n\tConstructor TTT\n");
        }
//        printBoard(initialBoard);

//        expandTree(playerWentFirst, symbol, getBoardTree());

        int resultCode = checkBoardForWinner(initialBoard);
        if (PRINT_STATEMENTS) {
            System.out.println("\tResultCode:\t" + resultCode);
            System.out.println("\t^Constructor^\n");
        }
    }

    // Creates a string representation of
    // the board with integer marks (1,2,3).
    public String toString() {
        String res = "\n\n";
        int[][] board = this.getBoardTree().getBoardState();
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++)  {
                res += ((board[i][j] == 2)? " " : ((board[i][j] == 1)? "X" : "O"));;
            }
            res += "\n";
        }
        res += "\n\n";
        return res;
    }

    public void expandTree(boolean playerWentFirst, int symbol, int turnNumber, BoardState rootBoardState) {
        int[][] board = rootBoardState.getBoardState();
//        int firstSymbol = symbol;

        if (turnNumber >= 10) {
            return;
        }

        int turnParam = turnNumber;
        int diff = 8 - turnNumber;
        while(diff >= 0 && !rootBoardState.getLeafStatus()) {
            if (diff % 2 == 1) {
                symbol = ((symbol == 2)? 2 : ((symbol == 1)? 3 : 1));
            }
            ArrayList<Integer> availSquares = collectAvailableSquares(board);
            for (int i = 0; i < availSquares.size(); i++) {
                int idx = availSquares.get(i);
                int r = idx / 3;
                int c = idx % 3;
                int[][] markedBoard = markBoardWithMove(symbol, idx, deepCopyBoard(board));
                int[][] positionSymbol = getMarksAndIndicies(markedBoard);
                if (PRINT_STATEMENTS) {
                    System.out.println("mm");
                }
                if (PRINT_STATEMENTS){
                    printBoard(markedBoard);
                }
                TicTacToe newTTT = new TicTacToe(playerWentFirst, symbol, -1, positionSymbol);
                rootBoardState.addChildState(newTTT, markedBoard);
//            System.out.println(newTTT);
            }
            turnNumber++;
            diff = 8 - turnNumber;
        }
        ArrayList<BoardState> childStates = rootBoardState.getChildStates();
        if (PRINT_STATEMENTS) {
            System.out.println("\n\tturnParam + 1:\t" + (turnParam + 1) +"\n");
        }
        for (BoardState childState : childStates) {
            if (PRINT_STATEMENTS) {
                System.out.println(childState.toString());
            }
            expandTree(playerWentFirst, playerSymbol,turnParam + 1, childState);
        }
    }

    public int[][] deepCopyBoard(int[][] board) {
        if (board.length == 0) {
            return board;
        }
        int[][] newBoard = new int[board.length][board[0].length];
        for (int i = 0; i < board.length; i++) {
            newBoard[i] = Arrays.copyOf(board[i], board[i].length);
        }
        return newBoard;
    }

    public int[][] getMarksAndIndicies(int[][] board) {
        ArrayList<Integer> lst = new ArrayList<Integer>();
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                int square = get1DIndexFrom2DArray(i, j);
                char symbol = getCharFromInt(board[i][j]);
                int idx = get1DIndexFrom2DArray(i, j);
                if (symbol != ' ') {
                    lst.add((int) idx);
                    lst.add((int) symbol);
                }
            }
        }
        int[][] positionSymbol = new int[lst.size()][2];
        for (int i = 0; i < lst.size(); i += 2) {
            positionSymbol[i][0] = lst.get(i); // pos
            positionSymbol[i][1] = lst.get(i + 1); // symbol
        }
        return positionSymbol;
    }

    // serves a testing method.
    // if a int n > -1 is passed in it will mark the board.
    public int[][] handleFirstMove(int symbol, int firstMoveLocation, int[][] initialBoard) {
        if (firstMoveLocation < 0 || firstMoveLocation > 8) {
            return initialBoard;
        }
        incrementTurnNumber();
        return markBoardWithMove(symbol, firstMoveLocation, initialBoard);
    }

    public int[][] handleTestMoves(int symbol, int firstMoveLocation, int[][] initialBoard, int[][] positionSymbol) {
        for (int i = 0; i < positionSymbol.length; i++) {
            for (int j = 0; j < 2; j += 2) {
                firstMoveLocation = positionSymbol[i][0];
                symbol = positionSymbol[i][1];
                initialBoard = handleFirstMove(symbol, firstMoveLocation, initialBoard);
            }
        }
        return initialBoard;
    }

    public BoardState getBoardTree() {
        return this.boardTree;
    }

    public int getGameTurnNumber() {
        return this.gameTurnNum;
    }

    public void resetTurnNumber() {
        this.gameTurnNum = 1;
    }

    public void incrementTurnNumber() {
        this.gameTurnNum++;
    }

    public void printBoard(int[][] board) {
        boolean symbolPrint = false; // Test variable
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                String val;
                if (symbolPrint){
                    val = ((board[i][j] == 2)? " " : ((board[i][j] == 1)? "X" : "O"));
                }
                else {
                    val = Integer.toString(board[i][j]);
                }
                System.out.print(val + " ");
            }
            System.out.println();
        }
    }

    public void printBoard(int[] board) {
        for (int i = 0; i < 3; i++) {
            String val = ((board[i] == 2)? " " : ((board[i] == 1)? "X" : "O"));
            System.out.print(val + " ");
        }
        System.out.println();
    }

    public String getPrintBoardString(int[][] board) {
        String res = "\n\tBoardState\n";
        boolean symbolPrint = false; // Test variable
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                String val;
                if (symbolPrint){
                    val = ((board[i][j] == 2)? " " : ((board[i][j] == 1)? "X" : "O"));
                }
                else {
                    val = Integer.toString(board[i][j]);
                }
                res += val + " ";
//                System.out.print(val + " ");
            }
            res += " ";
//            System.out.println();
        }
        return res;
    }

    public int[][] markBoardWithMove(int symbol, int location, int[][] board) {
        int[] r_c = get2DIndexFrom1DArray(location);
        int r = r_c[0];
        int c = r_c[1];
        board[r][c] = symbol;
        return board;
    }

    public int getAISymbol() {
        return ((this.getPLayerSymbol() == 1)? 3 : 1);
    }

    public int getPLayerSymbol() {
        return this.playerSymbol;
    }

    public char getCharFromInt(int num) {
        switch (num) {
            case    1   :   return 'X';
            case    2   :   return ' ';
            case    3   :   return 'O';
            default     :   return ' ';
        }
    }

    public int[] get2DIndexFrom1DArray(int index) {
        int[] res = {index / 3, index % 3};
        return res;
    }

    public int get1DIndexFrom2DArray(int r, int c) {
        return (r * 3) + (c % 3);
    }

    public int[][] getInitialBoardState() {
        int[][] res = {{2, 2, 2}, {2, 2, 2}, {2, 2, 2}};
        return res;
    }

    public int[] flattenBoard(int[][] board) {
        int[] flatBoard = new int[9];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                flatBoard[get1DIndexFrom2DArray(i, j)] = board[i][j];
            }
        }
        return flatBoard;
    }

    public ArrayList<Integer> collectAvailableSquares(int[][] board) {
        ArrayList<Integer> availSquares = new ArrayList<Integer>();
        int[] flatBoard = flattenBoard(board);
        for (int i = 0; i < 9; i++) {
            if (flatBoard[i] == 2) {
                availSquares.add(i);
            }
        }
        return availSquares;
    }

    public int checkHorizontal(int[][] board) {
        boolean winnerFound = false;
        boolean xIsWinner = false;
        // Check rows (horizontal)
        for (int r = 0; r < board.length; r++) {
            int xInRow = 0;
            int oInRow = 0;
            for (int c = 0; c < board[r].length; c++) {
                // Check x's
                if (board[r][c] == 1) {
                    xInRow++;
                }
                // Check o's
                else if (board[r][c] == 3) {
                    oInRow++;
                }
            }
            if (xInRow == 3) {
                xIsWinner = true;
                winnerFound = true;
            }
            else if (oInRow == 3) {
                winnerFound = true;
            }
        }
        if (winnerFound) {
            if (xIsWinner) {
                return 1;
            }
            else {
                return 0;
            }
        }
        // keep playing
        return 2;
    }

    public int checkVertical(int[][] board) {
        // Check columns (vertical)
        boolean winnerFound = false;
        boolean xIsWinner = false;
        for (int c = 0; c < board.length; c++) {
            // Check x's
            if (board[0][c] == 1 && board[1][c] == 1 && board[2][c] == 1) {
                xIsWinner = true;
                winnerFound = true;
            }
            // Check o's
            else if (board[0][c] == 3 && board[1][c] == 3 && board[2][c] == 3) {
                winnerFound = true;
            }
        }
        if (winnerFound) {
            if (xIsWinner) {
                return 1;
            }
            else {
                return 0;
            }
        }
        // keep playing
        return 2;
    }

    public boolean diagonalHelper(int r,int c, int symbol, int[][] board) {
        if (board[r][c] == symbol) {
            return true;
        }
        return false;
    }

    public int checkDiagonal(int[][] board) {
        int[][] coordinates = {{0, 0, 1, 1, 2, 2},{0, 2, 1, 1, 2, 0}}; // left and right diagonals
        int x = 1;
        int o = 3;
        for (int s = 0; s < 2; s++) {
            int sq = ((s == 0)? 1 : 3);
            for (int i = 0; i < 2; i++) {
                boolean coordinateCheck = true;
                for (int j = 0; j < 6; j += 2) {
                    int r = coordinates[i][j];
                    int c = coordinates[i][j + 1];
                    coordinateCheck &= diagonalHelper(r, c, sq, board);
//                    System.out.println("s: " + sq + " i: " + i + " j: " + j + " coor.: " +
//                            coordinateCheck + " r: " + r + " c: " + c + " b[r][c]: " + board[r][c]);
                    if (!coordinateCheck) {
                        break;
                    }
                }
                if (coordinateCheck) {
                    return sq;
                }
            }
        }
        return 2;
    }

    public int checkBoardStatus(int[][] board) {
        boolean newBoard = true; // assume new board (empty)
        boolean boardFull = true;
        for (int r = 0; r < 3; r++){
            for (int c = 0; c < 3; c++){
                // newBoard check if all squares == 2
                if (newBoard && board[r][c] != 2) {
                    newBoard = false;
                }
                if (boardFull && board[r][c] == 2) {
                    boardFull = false;
                }
            }
        }
        if (boardFull) {
            return 4;
        }
        else {
            return 2;
        }
    }

    // -2 -  boardStatus error
    // -1 -  logicCheck error
    // 1  -  x wins
    // 2  -  keep playing
    // 3  -  O wins
    // 4  -  draw / board full
    public int checkBoardForWinner(int[][] board) {
        int boardStatus = checkBoardStatus(board);
        // keep playing
        if (boardStatus == 2) {
            ArrayList<Integer> availSquares = collectAvailableSquares(board);
            int numEmptySquares = availSquares.size();
            if (numEmptySquares > 6) {
                return 2;
            }
        }
        // draw
        else if (boardStatus == 4) {
            return 4;
        }
        // error...
        else if (boardStatus < 1 || boardStatus > 3) {
            return -2;
        }

        // now only values 1, 2, and 3 can get this far
        int hCheck = checkHorizontal(board);
        int vCheck = checkVertical(board);
        int dCheck = checkDiagonal(board);
        boolean logicChecks = true;
        int winnerStatus = 2;

        // all checks are equal
        if ((hCheck == vCheck) && (hCheck == dCheck)) {
            // x wins
            if (hCheck == 1) {
                return 1;
            }
            // o wins
            else if (hCheck == 3) {
                return 3;
            }
            else {
                return 2;
            }
        }

        if (PRINT_STATEMENTS) {
            System.out.println("hcheck:\t" + hCheck + "\tvCheck:\t" + vCheck + "\tdCheck:\t" + dCheck);
        }
        if (hCheck == 1 || vCheck == 1 || dCheck == 1) {
            winnerStatus = 1;
        }
        if (hCheck == 3 || vCheck == 3 || dCheck == 3) {
            if (winnerStatus == 1) {
                logicChecks = false;
            }
            winnerStatus = 3;
        }

        if (logicChecks) {
            return winnerStatus;
        }
        else {
            return -1;
        }
    }

}
package com.example.abrig.tictactoeapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class MainActivity extends AppCompatActivity {

    public ImageView topLeftSquare;
    public ImageView topSquare;
    public ImageView topRightSquare;
    public ImageView leftSquare;
    public ImageView centerSquare;
    public ImageView rightSquare;
    public ImageView bottomLeftSquare;
    public ImageView bottomSquare;
    public ImageView bottomRightSquare;

    public ImageView topLeftX;
    public ImageView topX;
    public ImageView topRightX;
    public ImageView leftX;
    public ImageView centerX;
    public ImageView rightX;
    public ImageView bottomLeftX;
    public ImageView bottomX;
    public ImageView bottomRightX;

    public ImageView topLeftO;
    public ImageView topO;
    public ImageView topRightO;
    public ImageView leftO;
    public ImageView centerO;
    public ImageView rightO;
    public ImageView bottomLeftO;
    public ImageView bottomO;
    public ImageView bottomRightO;

    public ImageButton oSelectButton;
    public ImageButton xSelectButton;

    public boolean topLeftSquareShowing;
    public boolean topSquareShowing;
    public boolean topRightSquareShowing;
    public boolean leftSquareShowing;
    public boolean centerSquareShowing;
    public boolean rightSquareShowing;
    public boolean bottomLeftSquareShowing;
    public boolean bottomSquareShowing;
    public boolean bottomRightSquareShowing;

    public boolean playerChoseSymbol;
    public boolean playerSymbolIsX;
    public boolean gameWinnerFound;
    public boolean xPlayerIsWinner;
    public boolean oPlayerIsWinner;
    public int[][] boardStatus;
    public int gameNumber;
    public int playerWins;
    public int draws;
    public int playerLosses;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initViews();
        newGameBoard();
        playerChoseSymbol = false;
        getPlayerToChooseSymbol();
    }

    public void getPlayerToChooseSymbol() {
        String text = "Choose a symbol to play with first!";
        Toast.makeText(MainActivity.this, text, Toast.LENGTH_LONG).show();
    }

    public void selectSymbolX(View view) {
        if (!playerChoseSymbol) {
            gameNumber++;
            playerSymbolIsX = true;
            playerChoseSymbol = true;
            xSelectButton.setImageResource(R.drawable.red_selected_x_24dp);
        }
        else {
            String playerSymbol = ((playerSymbolIsX) ? "X" : "O");
            String text = "You have already chosen a symbol [ " + playerSymbol + " ]";
            Toast.makeText(MainActivity.this, text, Toast.LENGTH_LONG).show();
        }
    }

    public void selectSymbolO(View view) {
        if (!playerChoseSymbol) {
            gameNumber++;
            playerSymbolIsX = false;
            playerChoseSymbol = true;
            oSelectButton.setImageResource(R.drawable.red_selected_o_24dp);
        }
        else {
            String playerSymbol = ((playerSymbolIsX) ? "X" : "O");
            String text = "You have already chosen a symbol [ " + playerSymbol + " ]";
            Toast.makeText(MainActivity.this, text, Toast.LENGTH_LONG).show();
        }
    }

    public void printBoardResult(int[][] board) {
        int[] flatBoard = new int[9];
        int t = 0;
        System.out.println("\n\tBOARD\n");
        for (int r = 0; r < board.length; r++) {
            for (int c = 0; c < board[r].length; c++) {
                flatBoard[t++] = board[r][c];
//                System.out.println(flatBoard[t-1] + " ");
            }
//            System.out.println();
        }
        for (int square : flatBoard) {
            System.out.print(square + " ");
        }
        System.out.println();
    }

    public void tieMatch() {
        String text = "draw game";
        Toast.makeText(MainActivity.this, text, Toast.LENGTH_LONG).show();
        newGameBoard();
    }

    // Checks that booleans for PCX == XW
    // Checks that booleans for PCO == OW
    // else cpu wins
    public void winnerFound() {
        String text;
        if (playerSymbolIsX && xPlayerIsWinner) {
            playerWins++;
            text = "You Win!";
        }
        else if (!playerSymbolIsX && oPlayerIsWinner) {
            playerWins++;
            text = "You Win!";
        }
        else {
            playerLosses++;
            text = "You Lose :(";
        }
        int playerScore = playerWins;
        int cpuScore = playerLosses;
        int playerDraws = draws;
        String results = "\n{ " + playerWins + " , " + playerDraws + " , " + playerLosses + " }";
        text += results;
        Toast.makeText(MainActivity.this, text, Toast.LENGTH_LONG).show();
        printBoardResult(boardStatus);
    }

    public void checkForWinner() {
        int winnerFound = checkBoardForWinner(boardStatus);
        int keepPlaying = 0;
        // no winner      -1, new board found
        // draw            4, full board found
        // winnerFound ==  1, X won
        // winnerFound ==  2, no winner
        // winnerFound ==  3, O won
        switch (winnerFound) {
            case    1   :   xPlayerIsWinner = true;
                            gameWinnerFound = true;
                            winnerFound();
                            break;
            case    2   :   draws++;
                            tieMatch();
                            break;
            case    3   :   oPlayerIsWinner = true;
                            gameWinnerFound = true;
                            winnerFound();
                            break;
            case    4   :   return;
//                            keepPlaying++;
//                            break;
            case    -1  :   return;
//                            keepPlaying++;
//                            break;
            default     :   System.out.println("ERROR DEFAULT CASE USED");
        }
    }

    public int checkBoardForWinner(int[][] currBoardStatus) {
        boolean winnerFound = false;
        boolean xIsWinner = false;
        boolean oIsWinner = false;

        // Check rows (horizontal)
        for (int r = 0; r < currBoardStatus.length; r++) {
            int xInRow = 0;
            int oInRow = 0;
            for (int c = 0; c < currBoardStatus[r].length; c++) {
                // Check x's
                if (currBoardStatus[r][c] == 1) {
                    xInRow++;
                }
                // Check o's
                else if (currBoardStatus[r][c] == 3) {
                    oInRow++;
                }
            }
            if (xInRow == 3) {
                xIsWinner = true;
                winnerFound = true;
            }
            else if (oInRow == 3) {
                oIsWinner = true;
                winnerFound = true;
            }
        }
        if (!winnerFound) {
            // Check columns (vertical)
            for (int c = 0; c < currBoardStatus.length; c++) {
                // Check x's
                if (currBoardStatus[0][c] == 1 && currBoardStatus[1][c] == 1 && currBoardStatus[2][c] == 1) {
                    xIsWinner = true;
                    winnerFound = true;
                }
                // Check o's
                else if (currBoardStatus[0][c] == 3 && currBoardStatus[1][c] == 3 && currBoardStatus[2][c] == 3) {
                    oIsWinner = true;
                    winnerFound = true;
                }
            }
        }
        if (!winnerFound) {
            // Check diagonals
            int xFound = 0;
            int oFound = 0;
            // Check topLeft to bottomRight
            for (int r = 0, c = 0; c < currBoardStatus.length; r++, c++) {
                // Check x's
                if (currBoardStatus[r][c] == 1) {
                    xFound++;
                }
                // Check o's
                else if (currBoardStatus[r][c] == 3) {
                    oFound++;
                }
            }
            if (xFound == 3) {
                xIsWinner = true;
                winnerFound = true;
            }
            else if (oFound == 3) {
                oIsWinner = true;
                winnerFound = true;
            }
            xFound = 0;
            oFound = 0;
            if (!winnerFound) {
                for (int r = 2, c = 0; c < currBoardStatus.length; r--, c++) {
                    // Check x's
                    if (currBoardStatus[r][c] == 1) {
                        xFound++;
                    }
                    // Check o's
                    else if (currBoardStatus[r][c] == 3) {
                        oFound++;
                    }
                }
                if (xFound == 3) {
                    xIsWinner = true;
                    winnerFound = true;
                }
                else if (oFound == 3) {
                    oIsWinner = true;
                    winnerFound = true;
                }
            }
        }
        boolean newBoard = true;
        boolean draw = false;
        boolean boardStillPlayable = false;
        for (int r = 0; r < currBoardStatus.length; r++){
            for (int c = 0; c < currBoardStatus[r].length; c++){
                // newBoard check if all squares == 2
                if (newBoard && currBoardStatus[r][c] != 2) {
                    newBoard = false;
                }
                if (!boardStillPlayable && currBoardStatus[r][c] == 2) {
                    boardStillPlayable = true;
                }
            }
        }

        if (!boardStillPlayable) {
            draw = true;
        }

        if (winnerFound) {
            if (xIsWinner) {
                return 1;
            }
            else {
                return 3;
            }
        }
        else if (newBoard){
            return -1;
        }
        else if (draw) {
            return 2;
        }
        else {
            return 4;
        }
    }

    public void computerAIMove() {
        int computerSymbol = ((playerSymbolIsX)? 3 : 1);
        int keepPlaying = checkBoardForWinner(boardStatus);
        if (keepPlaying == -1 || keepPlaying == 4){
            int[] flattenedBoard = new int[9];
            int t = 0;
            for (int r = 0; r < boardStatus.length; r++) {
                for (int c = 0; c < boardStatus[r].length; c++) {
                    flattenedBoard[t] = boardStatus[r][c];
                    System.out.println("r:\t" + r + "\tc:\t" + c + "\t[r][c]:\t" + boardStatus[r][c]);
                    t++;
                }
            }
            naiveMove(flattenedBoard);
//            minimaxMove(flattenedBoard);
            checkForWinner();
        }
//
    }

//    public void minimaxMove(int[] flattenedBoard) {
//
//        int computerSymbol = ((playerSymbolIsX)? 3 : 1);
//        ArrayList<Integer> availableSquares = collectAvailableSquares(flattenedBoard);
//        ArrayList<Integer> availableSquaresParam = copyArrayList(availableSquares);
//        System.out.println("\n\nAVAILABLE SQUARES\n" + availableSquares);
//        int[] scoresArray = new int[availableSquares.size()];
//        int moveChoice = pickMinimaxMove(computerSymbol, flattenedBoard, boardStatus, scoresArray, availableSquaresParam);
//        System.out.println("\n\nMOVE CHOICE\n" + moveChoice);
//        if (moveChoice < 0 || moveChoice > 8) {
//            Random rnd = new Random();
//            int rndNum = rnd.nextInt(availableSquares.size());
//            moveChoice = rndNum;
//        }
//        int squareSelected = availableSquares.get(moveChoice);
//        aiMoveChoice(squareSelected, flattenedBoard.length);
//    }

    public ArrayList<Integer> copyArrayList(ArrayList<Integer> arr) {
        ArrayList<Integer> copy = new ArrayList<Integer>();
        copy.addAll(arr);
        return copy;
    }

//    public int pickMinimaxMove(int cpuSymbol, int[] flatBoard, int[][] currBoardStatus, int[] scores, ArrayList<Integer> availSquares) {
//        // cpu wins
//        System.out.println("\n\nSIZE:\t" + availSquares.size());
//        int playerSymbol = ((playerSymbolIsX)? 1 : 3);
////        int[] scores = new int[availSquares.size()];
//        for (int i = 0; i < availSquares.size(); i++) {
//            int r = i / 3;
//            int c = i % 3;
//            int val = 0;
////            boardStatus[r][c] = cpuSymbol;
//            System.out.print("\tin\n");
//            for (Integer in : availSquares) {
//                System.out.print(in + " ");
//            }
//            currBoardStatus[r][c] = cpuSymbol;
//            printBoardResult(currBoardStatus);
//            int winnerStatus = checkBoardForWinner(currBoardStatus);
//            System.out.println("\ti:\t" + i + "\tWinnerStatus:\t" + winnerStatus);
//            int moveSelected = availSquares.get(i);
//            if (winnerStatus == cpuSymbol) {
//                if (playerSymbolIsX) {
//                    oPlayerIsWinner = true;
//                }
//                else {
//                    xPlayerIsWinner = true;
//                }
//                gameWinnerFound = true;
//                winnerFound();
//                val = 10;
//                break;
//            }
//            // loss condition
//            else if (winnerStatus == playerSymbol) {
////                boardStatus[r][c] = 2;
//                if (playerSymbolIsX) {
//                    xPlayerIsWinner = true;
//                }
//                else {
//                    oPlayerIsWinner = true;
//                }
//                gameWinnerFound = true;
//                winnerFound();
//                val = -10;
//                break;
//            }
//            // draw condition
//            else if (winnerStatus == 2) {
//                // draw
////                tieMatch();
////                val = 0;
//                break;
//            }
//            // keep playing condition
//            else if (winnerStatus == 4) {
//                // sim player move too
//                int[] adjFlatBoard = new int[9]; //int[flatBoard.length - 1];
//                int t = 0;
//                for (int j = 0; j < flatBoard.length; j++) {
//                    if (j != i) {
//                        adjFlatBoard[t] = flatBoard[j];
//                        t++;
//                    }
//                }
//                availSquares.remove(i);
////                currBoardStatus[r][c] = 2; // reset for next iteration
////                printBoardResult(currBoardStatus);
//                System.out.println("\n\nSIZE: ->\t" + availSquares.size());
//                val = pickMinimaxMove(cpuSymbol, adjFlatBoard, currBoardStatus, scores, availSquares);
//            }
//            scores[i] = val;
//            for(int p : scores) {
//                System.out.print(p + " ");
//            }
//        }
////        System.out.println("\n\tERROR RETURNING 0\n");
////        return -1;
//        return availSquares.get(indexOfMaximumElement(scores));
//    }
//
//    public int minMax() {
//
//    }

    public int indexOfMaximumElement(int[] arr){
        int maxIdx = -1;
        int maxVal = Integer.MIN_VALUE;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] > maxVal) {
                maxVal = arr[i];
                maxIdx = i;
            }
        }
        return maxIdx;
    }

    public void naiveMove(int[] flattenedBoard) {
        // Randomly returning one of the remaining squares
        Random rnd = new Random();
        ArrayList<Integer> availableSquares = collectAvailableSquares(flattenedBoard);
        System.out.println("\nflattenedBoard nums");
        for (int v : flattenedBoard) {
            System.out.print(v + " ");
        }
        System.out.println("\navailableSquares nums");
        int rndNum = rnd.nextInt(availableSquares.size());
        for (int v : availableSquares) {
            System.out.print(v + " ");
        }
        System.out.println();
        System.out.println("rndNum:\t" + rndNum + "\tavailableSquares.get(rndNum):\t" + availableSquares.get(rndNum));
        int squareSelected = availableSquares.get(rndNum);
        while (validateSquare(squareSelected) <= 0) {
            squareSelected = rnd.nextInt(availableSquares.size());
            if (squareSelected == -1) {
                break;
            }
        }
        System.out.println("VALIDATED RETURN:\t" + squareSelected);
        aiMoveChoice(squareSelected, flattenedBoard.length);
//        for (int n : flattenedBoard) {
//            System.out.println(n + " ");
//        }
    }

    // Handles the final selection for an ai move, selects
    // the ai symbol and marks the board.
    public void aiMoveChoice(int square, int flatLength) {
        int computerSymbol = ((playerSymbolIsX) ? 3 : 1);
        int r_offset = square / 3;
        int c_offset = square % 3;
        System.out.println("before\t[ " +  square + " ] " + "[ r : " + r_offset + " ] [ c : " + c_offset + " ]\n");
        for (int r = 0; r < boardStatus.length; r++) {
            for (int c = 0; c < boardStatus[r].length; c++) {
                System.out.print(boardStatus[r][c] + " ");
            }
        }
        System.out.println("after\n");
        System.out.println("roff:\t" + r_offset + "\tcoff:\t" + c_offset + "\n");
        boardStatus[r_offset][c_offset] = computerSymbol;
        for (int r = 0; r < boardStatus.length; r++) {
            for (int c = 0; c < boardStatus[r].length; c++) {
                System.out.print(boardStatus[r][c] + " ");
            }
        }
        System.out.println();
        System.out.println("CPU CHOSE SQUARE:\t" + square);
//        int validated = validateSquare(square);
//        System.out.println("validatedReturn:\t" + validated);
        boolean c = false;
//        while (validated != -1 && validated == 0) {
        switch (square) {
            case 0:
                if (computerSymbol == 1) {
                    topLeftX.setVisibility(View.VISIBLE);
                } else {
                    topLeftO.setVisibility(View.VISIBLE);
                }
                topLeftSquareShowing = true;
                c = true;
                break;
            case 1:
                if (computerSymbol == 1) {
                    topX.setVisibility(View.VISIBLE);
                } else {
                    topO.setVisibility(View.VISIBLE);
                }
                topSquareShowing = true;
                c = true;
                break;
            case 2:
                if (computerSymbol == 1) {
                    topRightX.setVisibility(View.VISIBLE);
                } else {
                    topRightO.setVisibility(View.VISIBLE);
                }
                topRightSquareShowing = true;
                c = true;
                break;
            case 3:
                if (computerSymbol == 1) {
                    leftX.setVisibility(View.VISIBLE);
                } else {
                    leftO.setVisibility(View.VISIBLE);
                }
                leftSquareShowing = true;
                c = true;
                break;
            case 4:
                if (computerSymbol == 1) {
                    centerX.setVisibility(View.VISIBLE);
                } else {
                    centerO.setVisibility(View.VISIBLE);
                }
                centerSquareShowing = true;
                c = true;
                break;
            case 5:
                if (computerSymbol == 1) {
                    rightX.setVisibility(View.VISIBLE);
                } else {
                    rightO.setVisibility(View.VISIBLE);
                }
                rightSquareShowing = true;
                c = true;
                break;
            case 6:
                if (computerSymbol == 1) {
                    bottomLeftX.setVisibility(View.VISIBLE);
                } else {
                    bottomLeftO.setVisibility(View.VISIBLE);
                }
                bottomLeftSquareShowing = true;
                c = true;
                break;
            case 7:
                if (computerSymbol == 1) {
                    bottomX.setVisibility(View.VISIBLE);
                } else {
                    bottomO.setVisibility(View.VISIBLE);
                }
                bottomSquareShowing = true;
                c = true;
                break;
            case 8:
                if (computerSymbol == 1) {
                    bottomRightX.setVisibility(View.VISIBLE);
                } else {
                    bottomRightO.setVisibility(View.VISIBLE);
                }
                bottomRightSquareShowing = true;
                c = true;
                break;
//            Random rnd = new Random();
//            int newSquare = rnd.nextInt(flatLength);
//            validated = validateSquare(newSquare);
        }
        System.out.println("EXITED SAFELY\t" + c);
    }

    public int validateSquare(int square) {
        int[] flatboard = new int[9];
        System.out.println("square ^ :\t" + square);
        for (int r = 0; r < boardStatus.length; r++){
            for (int c = 0; c < boardStatus[r].length; c++) {
                flatboard[(r * 3) + c] = boardStatus[r][c];
                System.out.print(flatboard[(r*3) + c] + " ");
            }
        }
        System.out.println();
        for (int n = 0; n < flatboard.length; n++) {
            System.out.print(n + "\t");
            if (flatboard[n] == 2 && n == square){
                return 1;
            }
            if (n == square && flatboard[n] != 2) {
                return 0;
            }
        }
        System.out.println();
        return -1;
    }

    public ArrayList<Integer> collectAvailableSquares(int[] flattenedBoard) {
        ArrayList<Integer> availableIndexes = new ArrayList<>();
        for (int i = 0; i < flattenedBoard.length; i++) {
            int n = flattenedBoard[i];
            if (n == 2) {
                availableIndexes.add(i);
            }
        }
        return availableIndexes;
    }

//    public int minmax(int[] newBoard, int computerSymbol) {
//        int playerSymbol = ((playerSymbolIsX) ? 1 : 3);
//        ArrayList<Integer> availableIndexes = new ArrayList<>();
//        for (int n : newBoard) {
//            if (n != computerSymbol && n != playerSymbol) {
//                availableIndexes.add(n);
//            }
//        }
//        if (availableIndexes.isEmpty()) {
//            return -1;
//        }
//        else {
//            ArrayList<Integer> availIndexesScores = new ArrayList<>();
//            for (int availIndex : availableIndexes) {
//                int [] moveOnBoard = newBoard.clone();
//                moveOnBoard[availIndex] = computerSymbol;
//                availIndexesScores.add(minmax(moveOnBoard, computerSymbol));
//            }
//            int bestIndexForMove;
//            int maxScore = Integer.MIN_VALUE;
//            int maxScoreIndex = -1;
//            for (int i = 0; i < availIndexesScores.size(); i++) {
//                if (availIndexesScores.indexOf(i) > maxScore) {
//                    maxScore = availIndexesScores.indexOf(i);
//                    maxScoreIndex = i;
//                }
//            }
//            return
//        }
//    }

    public void resetGameBoard(View view) {
        if (!gameWinnerFound) {
            playerLosses++;
        }
        gameWinnerFound = false;
        xPlayerIsWinner = false;
        oPlayerIsWinner = false;
        newGameBoard();
    }

    public void newGameBoard() {
        topLeftX.setVisibility(View.INVISIBLE);
        topX.setVisibility(View.INVISIBLE);
        topRightX.setVisibility(View.INVISIBLE);
        leftX.setVisibility(View.INVISIBLE);
        centerX.setVisibility(View.INVISIBLE);
        rightX.setVisibility(View.INVISIBLE);
        bottomLeftX.setVisibility(View.INVISIBLE);
        bottomX.setVisibility(View.INVISIBLE);
        bottomRightX.setVisibility(View.INVISIBLE);

        topLeftO.setVisibility(View.INVISIBLE);
        topO.setVisibility(View.INVISIBLE);
        topRightO.setVisibility(View.INVISIBLE);
        leftO.setVisibility(View.INVISIBLE);
        centerO.setVisibility(View.INVISIBLE);
        rightO.setVisibility(View.INVISIBLE);
        bottomLeftO.setVisibility(View.INVISIBLE);
        bottomO.setVisibility(View.INVISIBLE);
        bottomRightO.setVisibility(View.INVISIBLE);

        xSelectButton.setImageResource(R.drawable.ic_black_x_24dp);
        oSelectButton.setImageResource(R.drawable.ic_black_o_24dp);

        topLeftSquareShowing = false;
        topSquareShowing = false;
        topRightSquareShowing = false;
        leftSquareShowing = false;
        centerSquareShowing = false;
        rightSquareShowing = false;
        bottomLeftSquareShowing = false;
        bottomSquareShowing = false;
        bottomRightSquareShowing = false;

//        playerLosses = 0;
//        playerWins = 0;
//        gameNumber = 0;
        gameWinnerFound = false;
        xPlayerIsWinner = false;
        oPlayerIsWinner = false;
        playerChoseSymbol = false;
        boardStatus = new int[][]{{2, 2, 2}, {2, 2, 2}, {2, 2, 2}};
    }

    public void initViews() {
        topLeftSquare = findViewById(R.id.top_left_square);
        topSquare = findViewById(R.id.top_square);
        topRightSquare = findViewById(R.id.top_right_square);
        leftSquare = findViewById(R.id.left_square);
        centerSquare = findViewById(R.id.center_square);
        rightSquare = findViewById(R.id.right_square);
        bottomLeftSquare = findViewById(R.id.bottom_left_square);
        bottomSquare = findViewById(R.id.bottom_square);
        bottomRightSquare = findViewById(R.id.bottom_right_square);

        topLeftX = findViewById(R.id.top_left_x);
        topX = findViewById(R.id.top_x);
        topRightX = findViewById(R.id.top_right_x);
        leftX = findViewById(R.id.left_x);
        centerX = findViewById(R.id.center_x);
        rightX = findViewById(R.id.right_x);
        bottomLeftX = findViewById(R.id.bottom_left_x);
        bottomX = findViewById(R.id.bottom_x);
        bottomRightX = findViewById(R.id.bottom_right_x);

        topLeftO = findViewById(R.id.top_left_o);
        topO = findViewById(R.id.top_o);
        topRightO = findViewById(R.id.top_right_o);
        leftO = findViewById(R.id.left_o);
        centerO = findViewById(R.id.center_o);
        rightO = findViewById(R.id.right_o);
        bottomLeftO = findViewById(R.id.bottom_left_o);
        bottomO = findViewById(R.id.bottom_o);
        bottomRightO = findViewById(R.id.bottom_right_o);

        oSelectButton = findViewById(R.id.select_o_button);
        xSelectButton = findViewById(R.id.select_x_button);
    }

    public void topLeftSquareClick(View view) {
        if (playerChoseSymbol && !gameWinnerFound) {
            if (!topLeftSquareShowing) {
                if (playerSymbolIsX) {
                    topLeftX.setVisibility(View.VISIBLE);
                    boardStatus[0][0] = 1;
                }
                else {
                    topLeftO.setVisibility(View.VISIBLE);
                    boardStatus[0][0] = 3;
                }
                topLeftSquareShowing = true;
                computerAIMove();
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }

    public void topSquareClick(View view) {
        if (playerChoseSymbol && !gameWinnerFound) {
            if (!topSquareShowing) {
                if (playerSymbolIsX) {
                    topX.setVisibility(View.VISIBLE);
                    boardStatus[0][1] = 1;
                }
                else {
                    topO.setVisibility(View.VISIBLE);
                    boardStatus[0][1] = 3;
                }
                topSquareShowing = true;
                computerAIMove();
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }

    public void topRightSquareClick(View view) {
        if (playerChoseSymbol && !gameWinnerFound) {
            if (!topRightSquareShowing) {
                if (playerSymbolIsX) {
                    topRightX.setVisibility(View.VISIBLE);
                    boardStatus[0][2] = 1;
                }
                else {
                    topRightO.setVisibility(View.VISIBLE);
                    boardStatus[0][2] = 3;
                }
                topRightSquareShowing = true;
                computerAIMove();
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }

    public void leftSquareClick(View view) {
        if (playerChoseSymbol && !gameWinnerFound) {
            if (!leftSquareShowing) {
                if (playerSymbolIsX) {
                    leftX.setVisibility(View.VISIBLE);
                    boardStatus[1][0] = 1;
                }
                else {
                    leftO.setVisibility(View.VISIBLE);
                    boardStatus[1][0] = 3;
                }
                leftSquareShowing = true;
                computerAIMove();
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }

    public void centerSquareClick(View view) {
        if (playerChoseSymbol && !gameWinnerFound) {
            if (!centerSquareShowing) {
                if (playerSymbolIsX) {
                    centerX.setVisibility(View.VISIBLE);
                    boardStatus[1][1] = 1;
                }
                else {
                    centerO.setVisibility(View.VISIBLE);
                    boardStatus[1][1] = 3;
                }
                centerSquareShowing = true;
                computerAIMove();
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }

    public void rightSquareClick(View view) {
        if (playerChoseSymbol && !gameWinnerFound) {
            if (!rightSquareShowing) {
                if (playerSymbolIsX) {
                    rightX.setVisibility(View.VISIBLE);
                    boardStatus[1][2] = 1;
                }
                else {
                    rightO.setVisibility(View.VISIBLE);
                    boardStatus[1][2] = 3;
                }
                rightSquareShowing = true;
                computerAIMove();
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }

    public void bottomLeftSquareClick(View view) {
        if (playerChoseSymbol && !gameWinnerFound) {
            if (!bottomLeftSquareShowing) {
                if (playerSymbolIsX) {
                    bottomLeftX.setVisibility(View.VISIBLE);
                    boardStatus[2][0] = 1;
                }
                else {
                    bottomLeftO.setVisibility(View.VISIBLE);
                    boardStatus[2][0] = 3;
                }
                bottomLeftSquareShowing = true;
                computerAIMove();
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }

    public void bottomSquareClick(View view) {
        if (playerChoseSymbol && !gameWinnerFound) {
            if (!bottomSquareShowing) {
                if (playerSymbolIsX) {
                    bottomX.setVisibility(View.VISIBLE);
                    boardStatus[2][1] = 1;
                }
                else {
                    bottomO.setVisibility(View.VISIBLE);
                    boardStatus[2][1] = 3;
                }
                bottomSquareShowing = true;
                computerAIMove();
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }

    public void bottomRightSquareClick(View view) {
        if (playerChoseSymbol && !gameWinnerFound) {
            if (!bottomRightSquareShowing) {
                if (playerSymbolIsX) {
                    bottomRightX.setVisibility(View.VISIBLE);
                    boardStatus[2][2] = 1;
                }
                else {
                    bottomRightO.setVisibility(View.VISIBLE);
                    boardStatus[2][2] = 3;
                }
                bottomRightSquareShowing = true;
                computerAIMove();
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }
}

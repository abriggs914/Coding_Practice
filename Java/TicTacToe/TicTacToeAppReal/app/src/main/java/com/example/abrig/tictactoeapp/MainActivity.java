package com.example.abrig.tictactoeapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

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
        }
        else {
            String playerSymbol = ((playerSymbolIsX) ? "X" : "O");
            String text = "You have already chosen a symbol [ " + playerSymbol + " ]";
            Toast.makeText(MainActivity.this, text, Toast.LENGTH_LONG).show();
        }
    }

    public void checkForWinner() {
        boolean winnerFound = false;
        boolean xIsWinner = false;
        boolean oIsWinner = false;

        // Check rows (horizontal)
        for (int r = 0; r < boardStatus.length; r++) {
            int xInRow = 0;
            int oInRow = 0;
            for (int c = 0; c < boardStatus[r].length; c++) {
                // Check x's
                if (boardStatus[r][c] == 1) {
                    xInRow++;
                }
                // Check o's
                else if (boardStatus[r][c] == 3) {
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
            for (int c = 0; c < boardStatus.length; c++) {
                // Check x's
                if (boardStatus[0][c] == 1 && boardStatus[1][c] == 1 && boardStatus[2][c] == 1) {
                    xIsWinner = true;
                    winnerFound = true;
                }
                // Check o's
                else if (boardStatus[0][c] == 3 && boardStatus[1][c] == 3 && boardStatus[2][c] == 3) {
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
            for (int r = 0, c = 0; c < boardStatus.length; r++, c++) {
                // Check x's
                if (boardStatus[r][c] == 1) {
                    xFound++;
                }
                // Check o's
                else if (boardStatus[r][c] == 3) {
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
                for (int r = 2, c = 0; c < boardStatus.length; r--, c++) {
                    // Check x's
                    if (boardStatus[r][c] == 1) {
                        xFound++;
                    }
                    // Check o's
                    else if (boardStatus[r][c] == 3) {
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
        if (winnerFound) {
            if (xIsWinner) {
                xPlayerIsWinner = true;
            }
            else{
                oPlayerIsWinner = true;
            }
            gameWinnerFound = true;
            winnerFound();
        }
    }

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
        Toast.makeText(MainActivity.this, text, Toast.LENGTH_LONG).show();
    }

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

        topLeftSquareShowing = false;
        topSquareShowing = false;
        topRightSquareShowing = false;
        leftSquareShowing = false;
        centerSquareShowing = false;
        rightSquareShowing = false;
        bottomLeftSquareShowing = false;
        bottomSquareShowing = false;
        bottomRightSquareShowing = false;

        playerLosses = 0;
        playerWins = 0;
        gameNumber = 0;
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
                checkForWinner();
            }
        }
        else {
            getPlayerToChooseSymbol();
        }
    }
}

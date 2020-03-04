package com.example.abrig.minesweeper;

public class MineSweeperException extends Throwable {

    private MineSweeper mineSweeper;

    public MineSweeperException(MineSweeper mineSweeper, int code) {
        this.mineSweeper = mineSweeper;
        switch (code) {
            case 0 :
                gameOverException();
                break;
            case 1 :
                invalidSubGridIndicies();
                break;
            case 2 :
                failedToClearSurrounding();
                break;
            case 3 :
                timesUpException();
                break;
            case 4 :
                youWinException();
                break;
            default :
                gameOverException();
        }
    }

    private void youWinException() {
        System.out.println("You win!");
        gameOverException();
    }

    private void invalidSubGridIndicies() {
        System.out.println("Invalid grid indicies.");
        gameOverException();
    }

    private void failedToClearSurrounding() {
        System.out.println("Not all surrounding squares were marked correctly.");
        gameOverException();
    }

    private void timesUpException() {
        System.out.println("Time\'s up!");
        gameOverException();
    }

    public void gameOverException() {
//        this.printStackTrace();
        System.out.println("GAME OVER");
        mineSweeper.setGameOver(true);
    }
}

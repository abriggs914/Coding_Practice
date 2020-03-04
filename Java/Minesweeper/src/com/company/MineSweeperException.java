package com.company;

public class MineSweeperException extends Throwable {
    public MineSweeperException(int code) {
        switch (code) {
            case 0 :
                gameOverException();
                break;
            case 1 :
                invalidSubGridIndicies();
                break;
            default :
                gameOverException();
        }
    }

    private void invalidSubGridIndicies() {
        System.out.println("Invalid grid indicies.");
        gameOverException();
    }

    public void gameOverException() {
        this.printStackTrace();
        System.out.println("GAME OVER");
    }
}

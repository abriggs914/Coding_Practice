package com.example.abrig.minesweeper;

public class Game {

    private int gameNum, time, score, searched;
    private boolean win;
    private Grid grid, gridSoln;

    public Game(int gameNum, boolean win, int time, int score, int searched, Grid grid, Grid gridSoln) {
        this.gameNum = gameNum;
        this.win = win;
        this.time = time;
        this.score = score;
        this.searched = searched;
        this.grid = grid;
        this.gridSoln = gridSoln;
    }

    @Override
    public String toString() {
        return "Game #" + String.format("%03d", gameNum)
                + ((win)? " win" : " loss") + ", time: "
                + Utilities.parseTime(time)
                + ", score: " + score
//                + "\n\nGrid:\n" + gridSoln
                ;
    }
}

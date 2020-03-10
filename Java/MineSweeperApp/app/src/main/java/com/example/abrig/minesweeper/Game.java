package com.example.abrig.minesweeper;

import java.util.ArrayList;
import java.util.Comparator;

public class Game {

    private int gameNum, time, score, searched;
    private boolean win;
    private Grid grid, gridSoln;
    private int difficulty;
    private MineSweeper mineSweeper;

    public Game(int gameNum, boolean win, int time, int score, int searched, MineSweeper mineSweeper) {
        this.gameNum = gameNum;
        this.win = win;
        this.time = time;
        this.score = score;
        this.searched = searched;
//        System.out.println("Game creation:\n\tminesweeper: " + mineSweeper + "\n\tgrid: " + mineSweeper.getGameGrid() + "\n\tgridSoln: " + mineSweeper.getSolnGrid());
        this.mineSweeper = mineSweeper;
        this.grid = mineSweeper.getGameGrid();
        this.gridSoln = mineSweeper.getSolnGrid();
        this.difficulty = mineSweeper.getDifficulty();
    }

    @Override
    public String toString() {
        return "Game #" + String.format("%05d", gameNum)
                + ((win)? " win" : " loss") + ", time: "
                + Utilities.parseTime(time)
                + ", score: " + score
                + ", difficulty: " + difficulty //Utilities.twoDecimal(difficulty)
//                + "\n\nGrid:\n" + gridSoln
                ;
    }

    public Grid getGridSoln() {
        return gridSoln;
    }

    public Grid getNoCluesGrid() {
        int r = grid.getNRows();
        int c = grid.getNCols();
        String[][] stringGrid = new String[r][c];
        ArrayList<ArrayList<String>> stringVals = grid.getStringValues();
        for (int i = 0; i < r; i++) {
            for (int j = 0; j < c; j++) {
                int val = grid.getValueAt(i, j);
                if (val < 9) {
                    stringGrid[i][j] = "0";
                }
                else {
                    stringGrid[i][j] = stringVals.get(i).get(j);
                }
            }
        }
        return new Grid(stringGrid);
    }

    static class GameNumberComparator implements Comparator<Game> {
        public int compare(Game game1, Game game2) {
            Integer g1 = game1.gameNum;
            Integer g2 = game2.gameNum;
            return g1.compareTo(g2);
        }
    }

    static class GameTimeComparator implements Comparator<Game> {
        public int compare(Game game1, Game game2) {
            Integer g1 = game1.time;
            Integer g2 = game2.time;
            return g1.compareTo(g2);
        }
    }

    static class GameScoreComparator implements Comparator<Game> {
        public int compare(Game game1, Game game2) {
            Integer g1 = game1.score;
            Integer g2 = game2.score;
            return g1.compareTo(g2);
        }
    }

    public int getGameNum() {
        return gameNum;
    }

    public int getDifficulty() {
        return difficulty;
    }

    public int getSecondsPast() {
        return time;
    }
}

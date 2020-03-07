package com.example.abrig.minesweeper;

import java.util.ArrayList;

public class MineSweeper {

    private Grid originalGrid;
    private Grid grid;
    private Grid grid_soln;
    private boolean gameOver;

    public MineSweeper(Grid soln) {
        this.grid_soln = soln;
        init();
    }

    public MineSweeper(String[][] arr) {
        this.grid_soln = Grid.parseGrid(arr);
        init();
    }

    public void init() {
        this.gameOver = false;
        this.grid_soln.addClues();
        this.grid_soln.setCheckedAll();
        this.grid = Grid.parseGrid(grid_soln.getGameGrid());
        this.originalGrid = Grid.parseGrid(grid_soln.getGameGrid());
    }

    public Grid getOriginalGrid() {
        return originalGrid;
    }

    public Grid getGameGrid() {
        return grid;
    }

    public Grid getSolnGrid() {
        return grid_soln;
    }

    public boolean isGameOver() {
        return gameOver;
    }

    public void setGameOver(boolean gameOver) {
        this.gameOver = gameOver;
//        this.grid.setCheckedAll();
    }

    public int getNumSquares() { return this.grid.getNumSquares(); }

    public int getNumMines() {
        return this.grid_soln.count(Main.MINE);
    }

    public int getNumCheckedSquares() { return this.grid.countCheckedSquares(); }

    public int getNumUnCheckedSquares() { return this.grid.countUnCheckedSquares(); }

    public boolean selectSquare(int r, int c) throws MineSweeperException {
        boolean success = false;
        if (!gameOver) {
            success = this.grid.selectSquare(r, c, grid_soln);
            if (success) {
//            int val = this.grid_soln.getValueAt(r, c);
//            if (0 < val && val < 10) {
//                this.grid.putValueAt(r, c, val);
//            }
                System.out.println("Square selection at (" + r + ", " + c + ") was successful!");
            } else {
                this.gameOver = true;
                System.out.println("Square selection at (" + r + ", " + c + ") FAILED");
                throw new MineSweeperException(this, 0);
            }
        }
        else {
            throw new MineSweeperException(this, 0);
        }
        return success;
    }

    public void setPossibleMine(int r, int c) {
        this.grid.setCheckStatusAt(r, c, true);
        this.grid.putValueAt(r, c, Main.POSSIBLE);
    }

    public void resetPossibleMine(int r, int c) throws MineSweeperException{
        boolean status = grid.getCheckStatusAt(r, c);
        int val = grid.getValueAt(r, c);
        if (status) {
            if (val == Main.POSSIBLE.charAt(0)) {
                this.grid.putValueAt(r, c, this.grid_soln.getValueAt(r, c));
                this.grid.setCheckStatusAt(r, c, false);
                return;
            }
        }
        throw new MineSweeperException(this, 0);
    }

    public void setSurroundingChecked(int r, int c) throws MineSweeperException{
        ArrayList<String> surroundingKeys = grid.getSurroundingSquaresKeys(r, c);
        for (String key : surroundingKeys) {
            int currVal = grid.getValueAt(key);
            int val = grid_soln.getValueAt(key);
            grid.setCheckStatusAt(key, true);
            if (currVal == Main.MINE.charAt(0) && val == Main.MINE.charAt(0)) {
                throw new MineSweeperException(this, 2);
            }
        }
    }

    public int count(String s) {
        System.out.println("Grid counting: " + s);
        return this.grid.count(s);
    }

    public int countSoln(String s) {
        System.out.println("GridSoln counting: " + s);
        return this.grid_soln.count(s);
    }

    public boolean guessedAll() {
        return countSoln(Main.MINE) == count(Main.POSSIBLE);
    }

    public boolean checkSolution() {
        boolean valid = true;
//        boolean gameOver = count(Main.MINE) > 0;
//        if (gameOver) {
//            throw new MineSweeperException(this, 0);
//        }
        boolean guessAll = guessedAll();
        if (guessAll) {
            ArrayList<String> markedIndexes = grid.getAllKeys(Main.POSSIBLE);
            int mineVal = Main.MINE.charAt(0);
            for (String key : markedIndexes) {
                boolean status = grid.getCheckStatusAt(key);
                int val = grid_soln.getValueAt(key);
                if (!status || val != mineVal) {
                    valid = false;
                    break;
                }
            }
        }
        return guessAll && valid;
    }

    public void printSoln() {
        System.out.println("\n\tSOLUTION\n" + grid_soln.toGameView(true));
    }

    public String toString() {
        return grid.toGameView(true);//_soln.toGameView(false);
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////

    public Grid subGrid(Grid gridIn, int startRow, int stopRow, int startCol, int stopCol) throws MineSweeperException{
        // logic
        int rows = gridIn.getNRows();
        int cols = gridIn.getNCols();
        boolean valid = false;
        startRow = Math.max(0, startRow);
        stopRow = Math.min(gridIn.getNRows() - 1, stopRow);
        startCol = Math.max(0, startCol);
        stopCol = Math.min(gridIn.getNCols() - 1, stopCol);
        if (Utilities.inRange(0, startRow, stopRow)) {
            if (Utilities.inRange(startRow, stopRow, rows)) {
                if (Utilities.inRange(0, startCol, stopCol)) {
                    if (Utilities.inRange(startCol, stopCol, cols)) {
                        valid = true;
                    }
                }
            }
        }
        if (!valid) {
            throw new MineSweeperException(this, 1);
        }

        int newRows = 1 + stopRow - startRow;
        int newCols = 1 + stopCol - startCol;
        int r = 0, c;
        String[][] res = new String[newRows][newCols];
//        System.out.println("startRow: " + startRow + ", stopRow: " + stopRow + ", startCol: " + startCol + ", stopCol: " + stopCol + ", newRows: " + newRows + ", newCols: " + newCols);
        for (int i = startRow; i <= stopRow; i++) {
            c = 0;
            for (int j = startCol; j <= stopCol; j++) {
                int intVal = gridIn.getValueAt(i, j);
                boolean status = gridIn.getCheckStatusAt(i, j);
                String val = Integer.toString(intVal);
//                System.out.println("i: " + i + ", j: " + j + ", r: " + r + ", c: " + c + ", intVal: " + intVal + ", val: " + val);
                if (status) {
                    res[r][c] = val;
                }
                else {
                    res[r][c] = Main.UNCHECKED;
                }
                c++;
            }
            r++;
        }
//        for (String[] s : res) {
//            System.out.println(Arrays.toString(s));
//        }
        Grid g = new Grid(res);
//        g.setCheckedAllSpacesAndHints();
//        System.out.println(g.toGameView(true));
        return g;
    }
}

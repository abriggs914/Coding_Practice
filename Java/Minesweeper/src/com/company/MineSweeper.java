package com.company;

public class MineSweeper {

    private Grid grid;
    private Grid grid_soln;

    public MineSweeper(Grid soln) {
//        this.grid = grid;
        this.grid_soln = soln;
        init();
    }

    public MineSweeper(String[][] arr) {
        this.grid_soln = Grid.parseGrid(arr);
        init();
    }

    public void init() {
        this.grid_soln.addClues();
        this.grid_soln.setCheckedAll();
        this.grid = Grid.parseGrid(grid_soln.getGameGrid());
    }

    public Grid getGameGrid() {
        return grid;
    }

    public int getNumMines() {
        return this.grid_soln.count(Main.MINE);
    }

    public boolean selectSquare(int r, int c) throws MineSweeperException {
        boolean success = this.grid.selectSquare(r, c, grid_soln);
        if (success) {
//            int val = this.grid_soln.getValueAt(r, c);
//            if (0 < val && val < 10) {
//                this.grid.putValueAt(r, c, val);
//            }
            System.out.println("Square selection at (" + r + ", " + c + ") was successful!");
        }
        else {
            System.out.println("Square selection at (" + r + ", " + c + ") FAILED");
        }
        return success;
    }

    public void printSoln() {
        System.out.println("\n\tSOLUTION\n" + grid_soln.toGameView(true));
    }

    public String toString() {
        return grid.toGameView(true);//_soln.toGameView(false);
    }
}

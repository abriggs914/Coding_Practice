package com.company;

import java.util.ArrayList;
import java.util.Arrays;

public class Main {

    final static String BORDER = "#";
    final static String MINE = "M";
    final static String POSSIBLE = "P";
    final static String CHECKED = " ";
    final static String UNCHECKED = "0";

    public static void main(String[] args) {

	// write your code here
        String[][] grid_1 = {
                {"0","0","0","0","0"},
                {"0","0","0","0","0"},
                {"0","0","0","0","0"},
                {"0","0","0","0","0"},
                {"0","0","0","0","0"}};

        String[][] grid_1_soln = {
                {"M"," "," "," "," "},
                {" "," "," "," "," "},
                {" "," "," "," "," "},
                {" "," "," "," "," "},
                {" ","M"," ","M"," "}};

        String[][] grid_2 = {
                {"0","0","0","0","0"},
                {"0","0","0","0","0"},
                {"0","0","0","0","0"},
                {"0","0","0","0","0"},
                {"0","0","0","0","0"}};

        String[][] grid_2_soln = {
                {" "," "," "," "," ","M"," "," "," ","M"," "," ","M"," "},
                {" "," "," ","M"," "," "," "," "," "," "," "," "," ","M"},
                {" ","M"," "," "," "," "," ","M"," ","M"," "," "," "," "},
                {" "," "," "," "," "," "," "," "," "," "," "," "," "," "},
                {" "," "," "," "," "," "," "," "," "," "," ","M"," "," "},
                {" "," "," "," "," "," "," ","M"," "," "," ","M"," "," "},
                {" ","M"," "," "," "," "," "," "," "," "," "," "," "," "},
                {" "," "," "," "," "," "," "," "," "," "," "," "," ","M"},
                {" "," "," ","M"," "," ","M"," "," "," "," "," "," "," "},
                {" ","M"," "," "," "," ","M"," "," "," "," "," "," "," "},
                {" ","M","M"," "," "," "," "," "," "," "," "," ","M"," "},
                {"M","M"," "," "," "," "," "," ","M"," "," "," "," ","M"},
                {" "," "," "," "," "," "," "," "," "," "," "," "," "," "},
                {"M"," "," "," "," ","M"," "," "," "," "," "," "," "," "},
                {" ","M"," "," "," "," "," "," ","M"," "," "," "," "," "},
                {"M"," "," ","M"," "," "," "," "," "," "," "," "," "," "},
                {" "," ","M","M"," "," "," "," ","M"," ","M"," "," "," "},
                {" "," "," "," "," "," "," "," "," "," ","M"," "," "," "},
                {" "," "," "," ","M"," "," "," "," "," "," ","M"," ","M"},
                {" "," "," "," "," "," "," "," "," "," "," "," ","M"," "}};

//        String[][] grid_2_soln = {
//                {" "," ","1","1","2","M","1"," ","1","M","1","1","M","2"},
//                {"1","1","2"," "," "},
//                {" "," "," "," "," "},
//                {" "," "," "," "," "},
//                {" ","M"," ","M"," "}};


//        Grid grid = new Grid(grid_1);
//        Grid grid_soln = new Grid(grid_1_soln);
//        System.out.println(grid);
//        System.out.println("available: " + grid.getAvailableSquaresKeys(0,0));
//        System.out.println("available: " + grid.getAvailableSquaresKeys(0,1));
//        System.out.println("soln: " + grid_soln);
        MineSweeper ms = new MineSweeper(grid_2_soln);
        System.out.println(ms);
        try {
//            ms.selectSquare(0, 1);
//            ms.selectSquare(1, 1); // works 9:29
            ms.selectSquare(7, 8);
            System.out.println(ms);
            ms.selectSquare(4, 0);
            ms.selectSquare(0, 7);
            System.out.println(ms);
            System.out.println(ms.getGameGrid().getSurroundingSquaresKeys(8, 3));
            System.out.println(ms.getGameGrid().getUncheckedSurrounding(8, 3));
//            Grid g = Grid.subGrid(ms.getGameGrid(), 10, 19, 0, 10);
//            System.out.println(ms);
//            System.out.println(ms);
//            ms.printSoln();
        }
        catch (Exception | MineSweeperException e) {
            e.printStackTrace();
        }
    }

    public static ArrayList<String> getAcceptedInput() {
        return new ArrayList<>(
                Arrays.asList(
                        BORDER,
                        MINE,
                        CHECKED,
                        UNCHECKED,
                        POSSIBLE,
                        Integer.toString(BORDER.charAt(0)),
                        Integer.toString(MINE.charAt(0)),
                        Integer.toString(CHECKED.charAt(0)),
                        Integer.toString(POSSIBLE.charAt(0)),
                        Integer.toString(UNCHECKED.charAt(0)),
                        "1", "2", "3", "4", "5", "6", "7", "8"));
    }
}

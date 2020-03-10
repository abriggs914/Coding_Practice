package com.example.abrig.minesweeper;

import android.content.Context;

import java.util.ArrayList;
import java.util.Arrays;

public class GameHistoryParser {

    public GameHistoryParser() {

    }

    public static Game getGameFromString(Context context, String gameString) throws MineSweeperException {
//        System.out.println("gameString: " + gameString);
        String[] gridSplit = gameString.split("\\[\\[");
        String[] statsSplit = gridSplit[0].split(",");
//        System.out.println("gridSplit: " + Arrays.toString(gridSplit));
//        System.out.println("statsSplit: " + Arrays.toString(statsSplit));
        int gameNum = Integer.parseInt(statsSplit[0].trim());
        boolean win = Integer.parseInt(statsSplit[1].trim()) != 0;
        int time = Integer.parseInt(statsSplit[2].trim());
        int score = Integer.parseInt(statsSplit[3].trim());
        int searched = Integer.parseInt(statsSplit[4].trim());
        String[][] arr = Utilities.arrify("[[" + gridSplit[2].trim());
//        String message = "\n\tARR:\n";
        for (int i = 0; i < arr.length; i++) {
            String[] row = arr[i];
//            message += Arrays.toString(row);
            for (int j = 0; j < row.length; j++) {
                String str = row[j];
                if (!Main.getAcceptedInput().contains(str)) {
                    arr[i][j] = Main.UNCHECKED;
                }
                else if (Integer.parseInt(str) < 9) {
                    arr[i][j] = Main.UNCHECKED;
                }
            }
//            row = arr[i];
//            message += Arrays.toString(row);
//            message += "\t contains weird char: " + weirdChar + "\n";
        }
//        System.out.println(message + "DONE");
        MineSweeper mineSweeper = new MineSweeper(arr, context);
//        System.out.println("minesweeper: " + mineSweeper);
        return new Game(gameNum, win, time, score, searched, mineSweeper);
    }

    public static String genHistoryString(MineSweeper mineSweeper, int... values) {
        StringBuilder label = new StringBuilder();
        Grid grid = mineSweeper.getGameGrid();
        Grid gridSoln = mineSweeper.getSolnGrid();
        String[][] gridString = grid.getGameGrid(); //.getStringGrid();
        String[][] gridSolnString = gridSoln.getGameGrid(); //.getStringGrid();
        // game_num, win/loss(1/0), time, score, searched
        for (int i : values) {
            label.append(i).append(", ");
        }
        label.append("[");
        for(String[] arr : gridString) {
            label.append(Arrays.toString(arr));
        }
        label.append("]");

        label.append("[");
        for(String[] arr : gridSolnString) {
            label.append(Arrays.toString(arr));
        }
        label.append("]");
//        System.out.println("generated string: " + label);
        return label.toString();
    }
}

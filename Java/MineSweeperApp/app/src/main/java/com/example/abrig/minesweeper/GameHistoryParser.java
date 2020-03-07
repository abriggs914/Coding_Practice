package com.example.abrig.minesweeper;

import java.util.Arrays;

public class GameHistoryParser {

    public GameHistoryParser() {

    }

    public static Game getGameFromString(String gameString) {
        // TODO:
        System.out.println("gameString: " + gameString);
        String[] gridSplit = gameString.split("\\[\\[");
        String[] statsSplit = gridSplit[0].split(",");
        System.out.println("gridSplit: " + Arrays.toString(gridSplit));
        System.out.println("statsSplit: " + Arrays.toString(statsSplit));
        int gameNum = Integer.parseInt(statsSplit[0].trim());
        boolean win = Boolean.parseBoolean(statsSplit[1].trim());
        int time = Integer.parseInt(statsSplit[2].trim());
        int score = Integer.parseInt(statsSplit[3].trim());
        int searched = Integer.parseInt(statsSplit[4].trim());
        Grid grid = new Grid(Utilities.arrify(gridSplit[1].trim()));
        Grid gridSoln = new Grid(Utilities.arrify(gridSplit[2].trim()));
        return new Game(gameNum, win, time, score, searched, grid, gridSoln);
    }

    public static String genHistoryString(Grid grid, Grid gridSoln, int... values) {
        StringBuilder label = new StringBuilder();
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
        System.out.println("generated string: " + label);
        Game game = getGameFromString(label.toString());
        System.out.println("generated game: " + game);
        return label.toString();
    }
}

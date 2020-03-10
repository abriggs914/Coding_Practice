package com.example.abrig.minesweeper;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class Grid {

    private final String BORDER = "#";

    private int n_cols;
    private int n_rows;
    private HashMap<String, HashMap<String, String>> grid;

    public Grid(String[][] gridIn) {
        this.n_rows = gridIn.length;
        this.n_cols = gridIn[0].length;
        this.grid = initializeGrid(gridIn);
    }

    public int getNRows() {
        return n_rows;
    }

    public int getNCols() {
        return n_cols;
    }

    private HashMap<String, HashMap<String, String>> initializeGrid(String[][] gridIn) {
        HashMap<String, HashMap<String, String>> res = new HashMap<>();
        for (int r = 0; r < n_rows; r++) {
            String[] row = gridIn[r];
            for (int c = 0; c < n_cols; c++) {
                String key = keyify(r, c);
                String val = String.valueOf(gridIn[r][c]);
                HashMap<String, String> attrs = new HashMap<>();
                boolean checked = val.equals(Main.CHECKED); // could be a clue, so not a safe check
                boolean unChecked = val.equals(Main.UNCHECKED) || val.equals(Main.MINE);
                // bad naming, but checked WITH "ed" marks whether the square is marked with a mine
                // WITHOUT "ed" marks the in game status of whether the square has been revealed
                attrs.put("checked_status", Boolean.toString(!unChecked));
                attrs.put("current_value", String.valueOf(val));

                res.put(key, attrs);
            }
        }
//        for (String key : res.keySet()) {
//            System.out.println("\tATTRS @ " + key + ": " + res.get(key));
//        }
//        System.out.println("initGrid results: " + res);
        return res;
    }

    public String keyify(int r, int c) {
        return "(" + r + ", " + c + ")";
    }

    public static boolean validateRectangle(String[][] gridIn){
        int r = gridIn.length;
        int total = 0;
        for (String[] row : gridIn) {
            total += row.length;
        }
        int x = total / r;
        return (x * r) == total;
    }

    public ArrayList<String> getAvailableSquaresKeys(int row, int col) {
        ArrayList<String> res = new ArrayList<>();
        int val = getValueAt(row, col);
//        System.out.println("row: " + row + ", col: " + col + " , val: " + val);
//        if (val != 77) {
//            return res;
//        }
        if (row < 0 || row  >= n_rows) {
            return res;
        }
        if (col < 0 || col >= n_cols) {
            return res;
        }
        if (row > 0) {
            if (col > 0) {
                if (!getCheckStatusAt(row - 1 , col - 1)) {
                    res.add(keyify(row - 1, col - 1));
                }
            }
            if (!getCheckStatusAt(row - 1, col)) {
                res.add(keyify(row - 1, col));
            }
            if (col < (n_cols - 1)) {
                if (!getCheckStatusAt(row - 1, col + 1)) {
                    res.add(keyify(row - 1, col + 1));
                }
            }
        }
        if (row < (n_rows - 1)) {
            if (col > 0) {
                if (!getCheckStatusAt(row + 1, col - 1)) {
                    res.add(keyify(row + 1, col - 1));
                }
            }
            if (!getCheckStatusAt(row + 1, col)) {
                res.add(keyify(row + 1, col));
            }
            if (col < (n_cols - 1)) {
                if (!getCheckStatusAt(row + 1, col + 1)) {
                    res.add(keyify(row + 1, col + 1));
                }
            }
        }
        if (col > 0) {
            if (!getCheckStatusAt(row, col - 1)) {
                res.add(keyify(row, col - 1));
            }
        }
        if (col < (n_cols - 1)) {
            if (!getCheckStatusAt(row, col + 1)) {
                res.add(keyify(row, col + 1));
            }
        }

//        res.forEach(System.out::println);
        return res;
    }

    public void addClues() {
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
//                String key = keyify(r, c);
                ArrayList<String> availableSquares = getAvailableSquaresKeys(r, c);
                if (getValueAt(r, c) == Main.MINE.charAt(0)) {
//                    System.out.println("keys: " + availableSquares);
                    for (String key : availableSquares) {
//                        System.out.println("key: " + key);
                        if (getValueAt(key) != Main.MINE.charAt(0)) {
                            putValueAt(key, getValueAt(key) + 1);
                        }
                    }
                }
            }
        }
    }

    public int getValueAt(int r, int c) {
        String curr = String.valueOf(this.grid.get(keyify(r, c)).get("current_value"));
        int res;
        try {
            res = Integer.parseInt(curr);
        }
        catch (Exception e) {
            if (curr.equals(Main.CHECKED)) {
                res = 0;
            }
            else {
                res = (int) curr.charAt(0);
//                System.out.println("\tcurr: (" + curr + "), is not a number. From key: " + keyify(r, c) + "\treturning: " + res);
            }
        }
//        System.out.println("fetchedA (" + res + ") from " + Utilities.keyify(r, c));
        return res;
    }

    public int getValueAt(String key) {
        String curr = String.valueOf(this.grid.get(key).get("current_value"));
        int res;
        try {
            res = Integer.parseInt(curr);
        }
        catch (Exception e) {
            if (curr.equals(Main.CHECKED)) {
                res = 0;
            }
            else {
                res = (int) curr.charAt(0);
//                System.out.println("\tcurr: (" + curr + "), is not a number. From key: " + key + "\treturning: " + res);
            }
        }
//        System.out.println("fetchedB (" + res + ") from " + key);
        return res;
    }

    public boolean getCheckStatusAt(int r, int c) {
        return getCheckStatusAt(keyify(r, c));
    }

    public boolean getCheckStatusAt(String key) {
        return Boolean.parseBoolean(this.grid.get(key).get("check_status"));
    }

    public boolean isMine(int r, int c) {
        return getValueAt(r, c) == Main.MINE.charAt(0);
    }

    public void setCheckStatusAt(String key, boolean checked) {
        this.grid.get(key).put("check_status", Boolean.toString(checked));
    }

    public void setCheckStatusAt(int r, int c, boolean checked) {
        setCheckStatusAt(keyify(r, c), checked);
    }

    public void putValueAt(int r, int c, String val) {
        this.grid.get(keyify(r, c)).put("current_value", val);
    }

    public void putValueAt(int r, int c, int val) {
        putValueAt(r, c, Integer.toString(val));
    }

    public void putValueAt(String key, int val) {
        this.grid.get(key).put("current_value", Integer.toString(val));
    }

    public HashMap<String, HashMap<String, String>> getMap() {
        return new HashMap<>(grid);
    }

    public int getNumSquares() {
        return n_rows * n_cols;
    }

    public int countCheckedSquares() {
        int res = 0;
        ArrayList<String> keys = getAllKeys();
        for (String key : keys) {
            if (getCheckStatusAt(key)) {
                res++;
            }
        }
        return res;
    }

    public int countUnCheckedSquares() {
        return getNumSquares() - countCheckedSquares();
    }

    public boolean selectSquare(int r, int c, boolean doCascade, Grid soln) {
        boolean stop = false;
//        System.out.println("\n\tSelecting: " + keyify(r, c) + ", which is valued at: " + getValueAt(r, c));
        if (r < 0 || r  >= n_rows) {
//            System.out.println("Row out of range (" + r + ") out of (0, " + n_rows + ")");
            stop = true;
        }
        if (c < 0 || c >= n_cols) {
//            System.out.println("Col out of range (" + c + ") out of (0, " + n_cols + ")");
            stop = true;
        }
        if (stop) {
            return false;
        }
        int val = getValueAt(r, c);
        if (val == Main.MINE.charAt(0)) {
            setCheckStatusAt(r, c, true);
            return false;
        }
        else {
//            boolean lastPlacedZero = true;
//            if (val == 0) {
//                lastPlacedZero = true;
//            }
            if (doCascade) {
                cascadeSelection(r, c, soln, true);
            }
            setCheckStatusAt(r, c, true);
            return true;
        }
    }

    private void cascadeSelection(int r, int c, Grid soln, boolean lastPlacedSpace) {
//        System.out.println("centered on: (" + r + ", " + c + ")");
        for (int i = -1; i < 2; i++) {
            for (int j = -1; j < 2; j++) {
                int x = r + i;
                int y = c + j;
                if (0 <= x && x < n_rows) {
                    if (0 <= y && y < n_cols) {
                        int solVal = soln.getValueAt(x, y);
                        boolean status = getCheckStatusAt(x, y);
//                        System.out.println("\t\tsolVal: " + solVal + ", status: " + status + " @ (" + x + ", " + y + ")");
                        if (!status && solVal == 0) {
                            this.putValueAt(x, y, solVal);
                            this.setCheckStatusAt(x, y, true);
                            cascadeSelection(x, y, soln, true);
                        }
                        else if (!status && lastPlacedSpace && (solVal < 9)) {
                            this.putValueAt(x, y, solVal);
                            this.setCheckStatusAt(x, y, true);
//                             TODO: check this
                            cascadeSelection(x, y, soln, false);
                        }
                    }
                }
            }
        }
    }

    public String[][] getStringGrid() {
        String[][] res = new String[n_rows][n_cols];
        for (int r = 0; r < n_rows; r++) {
            for(int c = 0; c < n_cols; c++) {
                int val = getValueAt(r, c);
                String stringVal;
                if (val < 9) {
                    stringVal = "0"; //Integer.toString(val);
                }
                else {
                    stringVal = Character.toString((char) val);
                }
                res[r][c] = stringVal;
            }
        }
        return res;
    }

    public ArrayList<ArrayList<String>> getStringValues() {
        ArrayList<ArrayList<String>> res = new ArrayList<>();
        for(int i = 0; i < n_rows; i++) {
            ArrayList<String> row = new ArrayList<>();
            for (int j = 0; j < n_cols; j++) {
                String val = Character.toString((char) getValueAt(i, j));
                row.add(val);
            }
            res.add(row);
        }
        return res;
    }

    public ArrayList<ArrayList<Integer>> getIntValues() {
        ArrayList<ArrayList<Integer>> res = new ArrayList<>();
        for(int i = 0; i < n_rows; i++) {
            ArrayList<Integer> row = new ArrayList<>();
            for (int j = 0; j < n_cols; j++) {
                int val = getValueAt(i, j);
                row.add(val);
            }
            res.add(row);
        }
        return res;
    }

    public ArrayList<String> getSurroundingSquaresKeys(int r, int c) {
        ArrayList<String> res = new ArrayList<>();
        if (Utilities.inRange(0, r, n_rows - 1) && Utilities.inRange(0, c, n_cols - 1)) {
            for (int i = -1; i < 2; i++) {
                for (int j = -1; j < 2; j++) {
                    int x = r + i;
                    int y = c + j;
//                    System.out.println("r: " + r + ", c: " + c + ", i: " + i + ", j: " + j + ", x: " + x + ", y: " + y);
                    if (Utilities.inRange(0, x, n_rows - 1)) {
                        if (Utilities.inRange(0, y, n_cols - 1)) {
                            if (x != r || y != c) {
                                res.add(keyify(x, y));
                            }
                        }
                    }
                }
            }
        }
//        System.out.println("Squares surrounding: " + keyify(r, c) + ": " + res);
        return res;
    }

    public ArrayList<String> getUncheckedSurrounding(int r, int c) {
        ArrayList<String> strings = getSurroundingSquaresKeys(r, c);
        ArrayList<String> res = new ArrayList<>();
//        System.out.println("getUncheckedSurrounding: " + strings + "\nr: " + r + ", c: " + c);
        for (String s : strings) {
            boolean status = getCheckStatusAt(s);
//            System.out.println("s: " + s + ", status: " + status + "\n");
            if (!status){
                res.add(s);
            }
        }
        return res;
    }

    public ArrayList<String> getAllKeys() {
        ArrayList<String> res = new ArrayList<>();
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
                res.add(keyify(r, c));
            }
        }
        return res;
    }

    public ArrayList<String> getAllKeys(String val) {
        int intVal = val.charAt(0);
        ArrayList<String> res = new ArrayList<>();
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
                int gridVal = getValueAt(r, c);
                if (gridVal == intVal) {
                    res.add(keyify(r, c));
                }
            }
        }
        return res;
    }

    public int count(String s) {
        int res = 0;
        int checkVal = s.charAt(0);
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
//                boolean status = getCheckStatusAt(r, c);
                int val = getValueAt(r, c);
//                System.out.println("key: " + keyify(r, c) + ", comparing: " + val + " to " + checkVal + ", curr res: " + res);
                if (val == checkVal) {
                    res++;
                }
            }
        }
        return res;
    }

    public void setCheckedAll() {
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
                setCheckStatusAt(r, c, true);
            }
        }
    }

    public String[][] getGameGrid() {
//        System.out.println("Get game grid");
        String[][] res = new String[n_rows][n_cols];
        for (int r = 0; r < n_rows; r++) {
            String[] row = new String[n_cols];
            for (int c = 0; c < n_cols; c++) {
                int val = getValueAt(r, c);
                boolean status = getCheckStatusAt(r, c);
                if (status) {
                    row[c] = val + "";
                }
                else {
                    row[c] = Main.UNCHECKED;
                }
            }
            res[r] = row;
        }
        return res;
    }

    private String genHorizontalBorder() {
        StringBuilder res = new StringBuilder();
        String border = Main.BORDER;
        for (int c = 0; c < n_cols + 2; c++) {
            res.append(border);
        }
        return res.toString();
    }

    public String toString() {
        StringBuilder res = new StringBuilder("\n");
        String borderString = genHorizontalBorder();
        res.append(borderString + "\n");
        for (int r = 0; r < n_rows; r++) {
            res.append(Main.BORDER);
            for (int c = 0; c < n_cols; c++) {
                int val = getValueAt(r, c);
                if (val < 10) {
                    if (val == 0) {
                        res.append(Main.CHECKED);
                    }
                    else {
                        res.append(val);
                    }
                }
                else {
//                    System.out.println("Mine: " + val);
                    res.append(Main.MINE);
                }
            }
            res.append(Main.BORDER + "\n");
        }
        res.append(borderString).append("\n");
        return res.toString();
    }

    public String toGameView(boolean showBlanks) {
        StringBuilder res = new StringBuilder("\n");
        String borderString = genHorizontalBorder();
        res.append(borderString + "\n");
        for (int r = 0; r < n_rows; r++) {
            res.append(Main.BORDER);
            for (int c = 0; c < n_cols; c++) {
                int val = getValueAt(r, c);
                boolean status = getCheckStatusAt(r, c);
                if (status) {
                    if (showBlanks && val == 0) {
                        res.append(" ");
                    }
                    else if (val == Main.MINE.charAt(0)) {
                        res.append(Main.MINE);
                    }
                    else {
                        res.append(val);
                    }
                }
                else {
                    res.append(Main.UNCHECKED);
                }
            }
            res.append(Main.BORDER + "\n");
        }
        res.append(borderString).append("\n");
        return res.toString();
    }

    public static Grid parseGrid(String[][] gridIn) {
//        System.out.println("IN -> gridIn: ");
//        for (String[] arr : gridIn) {
//            System.out.println(Arrays.toString(arr));
//        }
        int n_rows = gridIn.length;
        if (n_rows == 0 || !validateRectangle(gridIn)) {
//            System.out.println("EARLY");
            return null;
        }
        int n_cols = gridIn[0].length;
        ArrayList<String> acceptedInput = Main.getAcceptedInput();
//        System.out.println("ACCEPTED INPUT: " + acceptedInput);
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
                String val = String.valueOf(gridIn[r][c]);
                if (!acceptedInput.contains(val)) {
                    System.out.println("Invalid symbol encountered: {" + val + "}");
//                      TODO: this line is broken.
                    return null;
                }
            }
        }
//        System.out.println("OUT -> gridIn: ");
//        for (String[] arr : gridIn) {
//            System.out.println(Arrays.toString(arr));
//        }
        return new Grid(gridIn);
    }
}

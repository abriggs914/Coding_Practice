package com.company;

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

    private int getNRows() {
        return n_rows;
    }

    private int getNCols() {
        return n_cols;
    }

    private HashMap<String, HashMap<String, String>> initializeGrid(String[][] gridIn) {
        HashMap<String, HashMap<String, String>> res = new HashMap<>();
        for (int r = 0; r < n_rows; r++) {
            String[] row = gridIn[r];
            for (int c = 0; c < n_cols; c++) {
                String key = keyify(r, c);
                String val = gridIn[r][c];
                HashMap<String, String> attrs = new HashMap<>();
                boolean checked = val.equals(Main.CHECKED); // could be a clue, so not a safe check
                boolean unChecked = val.equals(Main.UNCHECKED) || val.equals(Main.MINE);
                attrs.put("checked_status", Boolean.toString(!unChecked));
                attrs.put("current_value", val);

                res.put(key, attrs);
            }
        }
        System.out.println("initGrid results: " + res);
        return res;
    }

    public String keyify(int r, int c) {
        return "(" + r + ", " + c + ")";
    }

    public static Grid parseGrid(String[][] gridIn) {
        System.out.println("IN -> gridIn: ");
        for (String[] arr : gridIn) {
            System.out.println(Arrays.toString(arr));
        }
        int n_rows = gridIn.length;
        if (n_rows == 0 || !validateRectangle(gridIn)) {
            System.out.println("EARLY");
            return null;
        }
        int n_cols = gridIn[0].length;
        ArrayList<String> acceptedInput = Main.getAcceptedInput();
        System.out.println("ACCEPTED INPUT: " + acceptedInput);
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
                String val = gridIn[r][c];
                if (!acceptedInput.contains(val)) {
                    System.out.println("Invalid symbol encountered: {" + val + "}");
                    return null;
                }
            }
        }
        System.out.println("OUT -> gridIn: ");
        for (String[] arr : gridIn) {
            System.out.println(Arrays.toString(arr));
        }
        return new Grid(gridIn);
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

    public static Grid subGrid(Grid gridIn, int startRow, int stopRow, int startCol, int stopCol) throws MineSweeperException{
        // logic
        int rows = gridIn.getNRows();
        int cols = gridIn.getNCols();
        boolean valid = false;
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
            throw new MineSweeperException(1);
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
                String val = Integer.toString(intVal);
//                System.out.println("i: " + i + ", j: " + j + ", r: " + r + ", c: " + c + ", intVal: " + intVal + ", val: " + val);
                res[r][c] = val;
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
        String curr = this.grid.get(keyify(r, c)).get("current_value");
        int res;
        try {
            res = Integer.parseInt(curr);
        }
        catch (Exception e) {
            if (curr.equals(Main.CHECKED)) {
                res = 0;
            }
            else {
                System.out.println("\tcurr: (" + curr + "), is not a number. From key: " + keyify(r, c));
                res = 77;
            }
        }
        return res;
    }

    public int getValueAt(String key) {
        String curr = this.grid.get(key).get("current_value");
        int res;
        try {
            res = Integer.parseInt(curr);
        }
        catch (Exception e) {
            if (curr.equals(Main.CHECKED)) {
                res = 0;
            }
            else {
                System.out.println("\t\tcurr: (" + curr + "), is not a number. From key: " + key);
                res = 77;
            }
        }
        return res;
    }

    public boolean getCheckStatusAt(int r, int c) {
        return getCheckStatusAt(keyify(r, c));
    }

    public boolean getCheckStatusAt(String key) {
        return Boolean.parseBoolean(this.grid.get(key).get("check_status"));
    }

    public void setCheckStatusAt(int r, int c, boolean checked) {
        this.grid.get(keyify(r, c)).put("check_status", Boolean.toString(checked));
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

    public boolean selectSquare(int r, int c, Grid soln) throws MineSweeperException {
        boolean stop = false;
        System.out.println("\n\tSelecting: " + keyify(r, c) + ", which is valued at: " + getValueAt(r, c));
        if (r < 0 || r  >= n_rows) {
            System.out.println("Row out of range (" + r + ") out of (0, " + n_rows + ")");
            stop = true;
        }
        if (c < 0 || c >= n_cols) {
            System.out.println("Col out of range (" + c + ") out of (0, " + n_cols + ")");
            stop = true;
        }
        if (stop) {
            return false;
        }
//        setCheckStatusAt(r, c, true);
//        putValueAt(r, c, soln.getValueAt(r, c));
        int val = getValueAt(r, c);
        if (val == Main.MINE.charAt(0)) {
            throw new MineSweeperException(0);
        }
        else {
            boolean lastPlacedZero = false;
            if (val == 0) {
                lastPlacedZero = true;
            }
            cascadeSelection(r, c, soln, lastPlacedZero);
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
                        }
                    }
                }
            }
        }
    }

    public ArrayList<ArrayList<String>> getValues() {
        ArrayList<ArrayList<String>> res = new ArrayList<>();
        for(int i = 0; i < n_rows; i++) {
            ArrayList<String> row = new ArrayList<>();
            for (int j = 0; j < n_cols; j++) {
                String val = grid.get(keyify(i, j)).get("current_value");
                row.add(val);
            }
            res.add(row);
        }
        return res;
    }

    public ArrayList<String> getSurroundingSquaresKeys(int r, int c) {
        ArrayList<String> res = new ArrayList<>();
        if (Utilities.inRange(0, r, n_rows) && Utilities.inRange(0, c, n_cols)) {
            for (int i = -1; i < 2; i++) {
                for (int j = -1; j < 2; j++) {
                    int x = r + i;
                    int y = c + j;
//                    System.out.println("r: " + r + ", c: " + c + ", i: " + i + ", j: " + j + ", x: " + x + ", y: " + y);
                    if (Utilities.inRange(0, x, n_rows)) {
                        if (Utilities.inRange(0, y, n_cols)) {
                            if (x != r || y != c) {
                                res.add(keyify(x, y));
                            }
                        }
                    }
                }
            }
        }
        System.out.println("Squares surrounding: " + keyify(r, c) + ": " + res);
        return res;
    }

    public ArrayList<String> getUncheckedSurrounding(int r, int c) {
        ArrayList<String> strings = getSurroundingSquaresKeys(r, c);
        ArrayList<String> res = new ArrayList<>();
        for (String s : strings) {
            boolean status = getCheckStatusAt(s);
            if (!status){
                res.add(s);
            }
        }
        return res;
    }

    public int count(String s) {
        final int[] res = {0};
        ArrayList<ArrayList<String>> stringsLists = getValues();
        stringsLists.forEach((l) -> l.forEach((str) -> res[0] += ((str.equals(s))? 1 : 0)));
        return res[0];
    }

    public void setCheckedAll() {
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
                setCheckStatusAt(r, c, true);
            }
        }
    }

    public void setCheckedAllSpaces() {
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
                int val = getValueAt(r, c);
                if (val == 0) {
                    setCheckStatusAt(r, c, true);
                }
            }
        }
    }

    public void setCheckedAllSpacesAndHints() {
        for (int r = 0; r < n_rows; r++) {
            for (int c = 0; c < n_cols; c++) {
                int val = getValueAt(r, c);
                if (val < 9) {
                    setCheckStatusAt(r, c, true);
                }
            }
        }
    }

    public String[][] getGameGrid() {
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
                    row[c] = "0";
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
                        res.append(" ");
                    }
                    else {
                        res.append(val);
                    }
                }
                else {
//                    System.out.println("Mine: " + val);
                    res.append("M");
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
                    res.append("0");
                }

//                if (val < 10) {
//                    if (showBlanks && val == 0) {
//                        res.append(" ");
//                    }
//                    else {
//                        res.append(val);
//                    }
//                }
//                else {
////                    System.out.println("Mine: " + val);
//                    res.append("M");
//                }
            }
            res.append(Main.BORDER + "\n");
        }
        res.append(borderString).append("\n");
        return res.toString();
    }
}

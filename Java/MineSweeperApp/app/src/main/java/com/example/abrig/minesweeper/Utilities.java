package com.example.abrig.minesweeper;

import java.util.ArrayList;
import java.util.Arrays;

public class Utilities {
    // Inclusive
    public static boolean inRange(int start, int x, int end) {
        return start <= x && x <= end;
    }

    // Inclusive
    public static boolean inRange(double start, double x, double end) {
//        System.out.println(start + " <= " + x + " <= " + end + " -> " + (start <= x && x <= end));
        return start <= x && x <= end;
    }

    public static String keyify(int r, int c) {
        return "(" + r + ", " + c + ")";
    }

    public static String keyify(float r, float c) {
        return "(" + (int)r + ", " + (int)c + ")";
    }

    public static String parseTime(int secondsPast) {
        String res = "";
        int mins = -1, seconds = 0;
        for (int x = secondsPast; x >= 0; x -= 60) {
            mins += 1;
            seconds = x;
            if (mins >= 60) {
                mins = 59;
                seconds = 59;
                break;
            }
//            System.out.println("x: " + x + ", mins: " + mins + ", seconds: " + seconds);
        }
        if (mins < 0) {
            mins = 0;
        }
        res = mins + "";
        String secondsString = seconds + "";
        if (res.length() != 2) {
            res = "0" + res;
        }
        res += ":";
        if (secondsString.length() != 2) {
            secondsString = "0" + secondsString;
        }
        res += secondsString;
        return res;
    }

    public static String[][] arrify(String s) {
//        System.out.println("in: " + s);
        String[] leftSplit = s.split("]\\[");
//        System.out.println("leftSplit: " + Arrays.toString(leftSplit));
        ArrayList<ArrayList<String>> list = new ArrayList<>();
        for (String possibleRow : leftSplit) {
            String[] commaSplit = possibleRow.split(",");
            ArrayList<String> rowList = new ArrayList<>();
            for (String entry : commaSplit) {
//                System.out.print("\tbefore: {" + entry);
                entry = entry.replaceAll("\\[", "");
                entry = entry.replaceAll("]", "");
                entry = entry.trim();
                rowList.add(entry);
//                System.out.println("}\tafter: {" + entry + "}");
            }
//            System.out.println("rowList: " + rowList);
            list.add(rowList);
        }
        int x = 1, y = 1;
        if (list.size() > 0) {
            y = list.get(0).size();
            x = list.size();
        }
        String[][] res = new String[x][y];
        for (int r = 0; r < x; r++) {
            ArrayList<String> row = list.get(r);
//            System.out.println("row ("+row.size()+"): " + row);
            for (int c = 0; c < y; c++) {
                res[r][c] = row.get(c);
            }
        }
        return res;
    }
}

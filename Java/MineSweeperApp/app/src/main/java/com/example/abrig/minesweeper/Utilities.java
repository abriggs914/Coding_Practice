package com.example.abrig.minesweeper;

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
}

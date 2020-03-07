package com.example.abrig.minesweeper;

import android.content.SharedPreferences;

import java.util.ArrayList;
import java.util.Map;
import java.util.Set;

public class SharedPreferencesHandler {

    public SharedPreferencesHandler() {

    }

    public static void printPrefs() {
        String line = "-----------------------------------------------------------------------";
        for (int i = 0; i < 3; i++) {
            System.out.println(line);
            line += "*";
        }
        for (String key : MainActivity.preferences.getAll().keySet()) {
            String entry = MainActivity.preferences.getAll().get(key).toString();
            System.out.println("    key: " + key + " -> " + entry);
        }
        for (int i = 0; i < 3; i++) {
            System.out.println(line);
            line += "*";
        }
    }

    public static int getIntVal(String label) {
        System.out.println("label: " + label);
        Map<String, ?> keyVals = MainActivity.preferences.getAll();
        Class clazz = keyVals.get(label).getClass();
        int val = 0;
        if (clazz == int.class) {
            val = (Integer) keyVals.get(label);
        }
        else if (clazz == String.class) {
            val = Integer.parseInt((String) keyVals.get(label));
        }
        return val;
    }

    public static String getStringVal(String label) {
        System.out.println("label: " + label);
        Map<String, ?> keyVals = MainActivity.preferences.getAll();
        Class clazz = keyVals.get(label).getClass();
        String val = "0";
        if (clazz == int.class) {
            val = Integer.toString((Integer) keyVals.get(label));
        }
        else if (clazz == String.class) {
            val = (String) keyVals.get(label);
        }
        return val;
    }

    public static void increment(String label) {
        int val = getIntVal(label);
        write(label, Integer.toString(val + 1));
    }

    public static void add(String label, int value) {
        int curr = getIntVal(label);
        write(label, Integer.toString(curr + value));
    }

    public static void write(String label, String value) {
        MainActivity.preferences.edit().putString(label, value).apply();
    }

    public static void write(String label, int value) {
        write(label, Integer.toString(value));
    }

    public static void write(String label,  boolean value) {
        MainActivity.preferences.edit().putBoolean(label, value).apply();
    }

    public static String getTopFiveString() {
        return "Top 5 games:";
    }

    public static String getLastFiveString() {
        return "Last 5 games:";
    }

    public static int getLostGames() {
        return getIntVal("games_lost");
    }

    public static int getWonGames() {
        return getIntVal("games_won");
    }

    public static int getNumGames() {
        return getIntVal("games_num");
    }

    public static int getBestScore() {
        return getIntVal("score_best");
    }

    public static int getBestTime() {
        return getIntVal("time_best");
    }

    public static int getWorstScore() {
        return getIntVal("score_worst");
    }

    public static int getWorstTime() {
        return getIntVal("time_worst");
    }

    public static int getAverageScore() {
        return getIntVal("score_average");
    }

    public static int getAverageTime() {
        return getIntVal("time_average");
    }

    public static int getAverageDifficulty() { return getIntVal("difficulty_average"); }

    public static int getTotalScore() { return getIntVal("score_total"); }

    public static int getTotalTime() { return getIntVal("time_total"); }

    public static int getTotalDifficulty() { return getIntVal("difficulty_total"); }

    public static ArrayList<String> getGamesStringList() {
        ArrayList<String> res = new ArrayList<>();
        Map<String, ?> keyVals = MainActivity.preferences.getAll();
        for (String key : keyVals.keySet()) {
            if (key.contains("game #")) {
                String val = (String) keyVals.get(key);
                res.add(val);
            }
        }
        return res;
    }
}

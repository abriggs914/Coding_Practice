package com.example.abrig.spendinglog;

import android.content.SharedPreferences;

import java.util.ArrayList;
import java.util.Map;
import java.util.Set;

public class SharedPreferencesWriter {

    public SharedPreferencesWriter() {

    }

    public static void printPrefs() {
        String line = "-----------------------------------------------------------------------";
        for (int i = 0; i < 3; i++) {
            System.out.println(line);
            line += "*";
        }
        for (String key : MainActivity.prefs.getAll().keySet()) {
            String entry = MainActivity.prefs.getAll().get(key).toString();
            if (key.contains("entity_entry_")) {
                System.out.println("            entity key: " + key + " -> " + entry);
            }
            else {
                System.out.println("    regular key: " + key + " -> " + entry);
            }
        }
        for (int i = 0; i < 3; i++) {
            System.out.println(line);
            line += "*";
        }
    }

    public static void write(String label, String value) {
        MainActivity.prefs.edit().putString(label, value).apply();
    }

    public static void write(String label, int value) {
        MainActivity.prefs.edit().putInt(label, value).apply();
    }

    public static void write(String label, float value) {
        MainActivity.prefs.edit().putFloat(label, value).apply();
    }

    public static void write(String label, boolean value) {
        MainActivity.prefs.edit().putBoolean(label, value).apply();
    }

    public static void deleteEntityEntry(Entity e) {
        String key = Utilities.getKey(e);
        MainActivity.prefs.edit().remove(key).apply();
    }

    public static void re_writePrefs() {
        Map<String, ?> prefs = MainActivity.prefs.getAll();
        Set<String> keys = prefs.keySet();
        ArrayList<String> keysToRemove = new ArrayList<>();
        for (String key : keys) {
            if (key.contains("entity_entry_")) {
                keysToRemove.add(key);
            }
        }
        for (String key : keysToRemove) {
            MainActivity.prefs.edit().remove(key).apply();
        }
        ArrayList<Entity> entities = MainActivity.TH.getEntities();
        for (Entity e : entities) {
            if (!e.getName().equals(prefs.get("user_name"))) {
                write("entity_entry_" + e.getName(), e.serializeEntry());
            }
            else {
                write("entity_entry_User", e.serializeEntry());
            }
        }

//        MainActivity.prefs.edit().apply();
    }
}

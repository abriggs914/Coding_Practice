package com.example.abrig.spendinglog;

public enum CustomOccurringOptions {
    HOUR("hour", 8760),
    DAY("day", 365),
    NIGHT("night", 365),
    WEEK("week", 52),
    MONTH("month", 12),
    YEAR("year", 1);

    public String name;
    public double annualRef;

    CustomOccurringOptions(String name, double annualRef){
        this.name = name;
        this.annualRef = annualRef;
    }

    public static String[] getValues() {
        CustomOccurringOptions[] vals = CustomOccurringOptions.values();
        int len = vals.length;
        String[] res = new String[len];
        for (int i = 0; i < len; i++) {
            res[i] = vals[i].name;
        }
        return res;
    }
}

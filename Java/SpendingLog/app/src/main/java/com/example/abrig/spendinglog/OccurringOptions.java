package com.example.abrig.spendinglog;

public enum OccurringOptions {
    HOURLY("hourly"),
    DAILY("daily"),
    NIGHTLY("nightly"),
    WEEKLY("weekly"),
    BI_WEEKLY("bi-weekly"),
    MONTHLY("monthly"),
    BI_MONTHLY("bi-monthly"),
    YEARLY("yearly"),
    BI_YEARLY("bi-yearly"),
    CUSTOM("custom");

    public String name;

    OccurringOptions(String name){
        this.name = name;
    }

    public static String[] getValues() {
        OccurringOptions[] vals = OccurringOptions.values();
        int len = vals.length;
        String[] res = new String[len];
        for (int i = 0; i < len; i++) {
            res[i] = vals[i].name;
        }
        return res;
    }

    @Override
    public String toString() {
        return name;
    }
}

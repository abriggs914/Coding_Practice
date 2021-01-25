package com.example.cluenotebook.ui.main;

public class Utility {

    public static String join(String delim, Object[] objs) {
        StringBuilder res = new StringBuilder();
        for (int i = 0; i < objs.length; i++) {
            res.append(objs[i]);
            if (i < objs.length - 1) {
                res.append(delim);
            }
        }
        return res.toString();
    }
}

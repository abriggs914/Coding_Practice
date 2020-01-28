package com.example.abrig.spendinglog;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class CSVWriter {

    public CSVWriter() {

    }

    public void writeFile(ArrayList<String> header, ArrayList<Transaction> transactions) {
        List<String[]> data = new ArrayList<String[]>();
        String[] h = new String[header.size()];
        for (int i = 0; i < header.size(); i++) {
            String title = header.get(i);
            h[i] = title;
        }
        data.add(h);
        for (Transaction t : transactions) {
            data.add(new String[]{
                    t.getTransactionDate().toString(),
                    t.getSender().getName(),
                    t.getReceiver().getName(),
                    Integer.toString(t.getTransactionAmount())});
        }
        for (String[] s : data) {
            System.out.println(Arrays.toString(s));
        }
    }
}

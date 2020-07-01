package com.example.abrig.spendinglog;
import android.support.annotation.NonNull;

import java.util.ArrayList;

public class TransactionType {

    private static ArrayList<TransactionType> listOfTypes = new ArrayList<>();

    private String name;

    public TransactionType(String name) {
        this.name = name.substring(0, 1).toUpperCase() + name.substring(1).toLowerCase();
        if (!listOfTypes.contains(this)) {
            listOfTypes.add(this);
        }
    }

    public static ArrayList<TransactionType> getTypes() {
        return listOfTypes;
    }

    public String getName() {
        return name;
    }

    @Override
    public String toString() {
        return this.name;
    }
}

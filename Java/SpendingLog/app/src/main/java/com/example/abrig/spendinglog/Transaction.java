package com.example.abrig.spendinglog;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

public class Transaction {

    private Date transactionDate;
    private Entity sender;
    private Entity receiver;
    private int transactionAmount;
    private boolean reoccurring;
    private String occurring;

    public Transaction(Entity sender, Entity receiver, int transactionAmount, boolean oneTime, String occurring) {
        this.transactionDate = new Date();
        this.sender = sender;
        this.receiver = receiver;
        this.transactionAmount = transactionAmount;
        this.reoccurring = oneTime;
        this.occurring = parseOccurring(occurring);
    }

    private String parseOccurring(String occurring) {
        ArrayList<String> accepted = new ArrayList<>(Arrays.asList(
                "hourly",
                "daily",
                "nightly",
                "weekly",
                "bi-weekly",
                "monthly",
                "bi-monthly",
                "yearly",
                "bi-yearly"));
        if (!accepted.contains(occurring)) {
            return "NA";
        }
        else {
            return occurring;
        }
    }

    private void setTransactionDate(Date d) {
        this.transactionDate = d;
    }

    public Date getTransactionDate() {
        return transactionDate;
    }

    public Entity getSender() {
        return sender;
    }

    public Entity getReceiver() {
        return receiver;
    }

    public int getTransactionAmount() {
        return transactionAmount;
    }

    public boolean getOneTimeStatus() {
        return reoccurring;
    }

    public void setReoccurring(boolean b) {
        this.reoccurring = b;
    }

    public String getOccurringStatus() {
        return occurring;
    }

    public String toString() {
        String s = sender + " sent " + Utilities.dollarify(transactionAmount) + " to " + receiver + " at: " + transactionDate;
        if (reoccurring) {
            s += ", re-occurring " + occurring;
        }
        return s;
    }

    public String serializeEntry() {
        return ">>" + transactionDate + ">>" + sender + ">>" + receiver + ">>" + transactionAmount + ">>" + reoccurring + ">>" + occurring + ">>";
    }

    public static Transaction re_initTransaction(Date date, Entity sender, Entity receiver, int amount, boolean reoccurring, String occurring) {
        Transaction t = new Transaction(sender, receiver, amount, reoccurring, occurring);
        t.setTransactionDate(date);
        return t;
    }
}

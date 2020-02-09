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
    private double annualOccurringRate;

    public Transaction(Entity sender, Entity receiver, int transactionAmount, boolean reoccurring, String occurring) {
        this.transactionDate = new Date();
        this.sender = sender;
        this.receiver = receiver;
        this.transactionAmount = transactionAmount;
        this.reoccurring = reoccurring;
        if (!reoccurring) {
            this.occurring = "NA";
            this.annualOccurringRate = 0;
        }
        else {
            this.occurring = parseOccurring(occurring);
            this.annualOccurringRate = determineAnnualOccurrence();
        }
    }

    private ArrayList<String> acceptedOccurringInput = new ArrayList<>(Arrays.asList(
            "custom",
            "hourly",
            "daily",
            "nightly",
            "weekly",
            "bi-weekly",
            "monthly",
            "bi-monthly",
            "yearly",
            "bi-yearly"));

    private double determineAnnualOccurrence() {
        int idx = acceptedOccurringInput.indexOf(this.occurring);
        double res = 0.0;
        switch (idx) {
            case    0   :   res = parseCustomInput();
                            break;
            case    1   :   res = 8760;
                            break;
            case    2   :   res = 365;
                            break;
            case    3   :   res = 365;
                            break;
            case    4   :   res = 52;
                            break;
            case    5   :   res = 26;
                            break;
            case    6   :   res = 12;
                            break;
            case    7   :   res = 6;
                            break;
            case    8   :   res = 1;
                            break;
            case    9   :   res = 0.5;
                            break;
            default     :   break;
        }
        return res;
    }

    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    private double parseCustomInput() {
        return 0.0;
    }
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////

    private String parseOccurring(String occurring) {
        if (!acceptedOccurringInput.contains(occurring)) {
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

    public void setSender(Entity e) {
        this.sender = e;
    }

    public Entity getReceiver() {
        return receiver;
    }

    public void setReceiver(Entity e) {
        this.receiver = e;
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
        String s = sender + " sent " + Utilities.dollarify(transactionAmount) + " to " + receiver + " on " + transactionDate;
        if (reoccurring) {
            s += ", re-occurring " + occurring;
        }
        s += ", rate: {" + annualOccurringRate + "}";
        return s;
    }

    public String serializeEntry() {
        return ">>" + transactionDate + ">>" + sender.getName() + ">>" + receiver.getName() + ">>" + transactionAmount + ">>" + reoccurring + ">>" + occurring + ">>";
    }

    public static Transaction re_initTransaction(Date date, Entity sender, Entity receiver, int amount, boolean reoccurring, String occurring) {
        Transaction t = new Transaction(sender, receiver, amount, reoccurring, occurring);
        t.setTransactionDate(date);
        return t;
    }
}

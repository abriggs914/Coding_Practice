package com.example.abrig.spendinglog;

import android.text.format.DateUtils;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;

public class Transaction {

    private Date transactionDate;
    private Date firstTransactionDate;
//    private Date nextTransactionDate;
    private Entity sender;
    private Entity receiver;
    private int transactionAmount;
    private boolean reoccurring;
    private String occurring;
    private double annualOccurringRate;
    private ArrayList<Date> oneYearTransactions;
    private TransactionType transactionType;

    private final double SECONDS_PER_YEAR = 31536000.0;

    public Transaction(Entity sender, Entity receiver, int transactionAmount, boolean reoccurring, String occurring, TransactionType transactionType) {
        this.transactionDate = new Date();
        this.firstTransactionDate = this.transactionDate;
        this.sender = sender;
        this.receiver = receiver;
        this.transactionAmount = transactionAmount;
        this.reoccurring = reoccurring;
        this.transactionType = transactionType;
        this.oneYearTransactions = new ArrayList<>();
        if (!reoccurring) {
            this.occurring = "NA";
            this.annualOccurringRate = 0;
        }
        else {
            this.occurring = occurring;
            this.annualOccurringRate = determineAnnualOccurrence();
            this.oneYearTransactions.addAll(calculateOneYearTransactions());
        }
//        this.nextTransactionDate = calculateNextTransactionDate(this.transactionDate, this.annualOccurringRate);
    }

    private ArrayList<Date> calculateOneYearTransactions() {
        ArrayList<Date> res = new ArrayList<>();
        return res;
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
        double res;
        switch (idx) {
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
            default     :   res = parseCustomInput();
                            break;
        }
        return res;
    }

    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    private double parseCustomInput() {
        String[] spl = this.occurring.split(" ");
        boolean isNum = Utilities.checkDec(spl[0]);
        double d = 1;
        double m = 1;
        if (isNum) {
            d = Double.parseDouble(spl[0]);
        }
        if (spl[0].equals("twice")) {
            d = 2;
        }
        CustomOccurringOptions[] options = CustomOccurringOptions.values();
        for (int i = 0; i < options.length; i++) {
            if (spl[2].equals(options[i].name)) {
                m = options[i].annualRef;
            }
        }
        System.out.println("D: " + d + ", M: " + m + " D x M = " + (d * m));
        return d * m;
    }
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////

//    private String parseOccurring(String occurring) {
//        if (!acceptedOccurringInput.contains(occurring)) {
//            return "NA";
//        }
//        else {
//            return occurring;
//        }
//    }

    private void setTransactionDate(Date d) {
        this.transactionDate = d;
    }

    public Date getTransactionDate() {
        return transactionDate;
    }

    public TransactionType getTransactionType() {
        return this.transactionType;
    }

    public void setFirstTransactionDate(Date d) {
        this.firstTransactionDate = d;
    }

    public Date getFirstTransactionDate() {
        return firstTransactionDate;
    }

    public ArrayList<Transaction> setUpcomingTransactionDates(ArrayList<Date> d) {
        ArrayList<Transaction> upcomingTransactions = new ArrayList<>();
        Date today = new Date();
        ArrayList<Date> leftOver = new ArrayList<>();
        for (Date date : d) {
            if (date.before(today)) {
                // update list from last start-up
                Transaction newT = re_initTransaction(date, sender, receiver, transactionAmount, reoccurring, occurring, transactionType);
                System.out.println("TransactionHandler: " + MainActivity.TH);
                System.out.println("newTransaction: " + newT);
//                MainActivity.TH.addTransaction(newT);
                upcomingTransactions.add(newT);
                sender.addTransaction(newT);
                receiver.addTransaction(newT);
            }
            else {
                leftOver.add(date);
            }
        }
        this.oneYearTransactions.addAll(leftOver);
        return upcomingTransactions;
    }

    public Date getNextTransactionDate() {
        return oneYearTransactions.get(0);
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

    public double getAnnualOccurringRate() { return this.annualOccurringRate; }

    public ArrayList<Date> calculateNextTransactionDate(Date tDate, double annualRate) {
        ArrayList<Date> res = new ArrayList<>();
        if (annualRate <= 0) {
            return res;
        }
        double secondsPerAttempt;
        if (annualRate >= 1) {
            secondsPerAttempt = SECONDS_PER_YEAR / annualRate;
        }
        else {
            secondsPerAttempt = SECONDS_PER_YEAR * annualRate;
        }
//        Calendar cal = Calendar.getInstance(); // creates calendar
//        cal.setTime(tDate); // sets calendar time/date
//        cal.add(Calendar.SECOND, (int) secondsPerAttempt);
//        Date nextDate = cal.getTime();
//        System.out.println("secondsPerAttempt: " + secondsPerAttempt + ", next date calculated: " + nextDate);
        Calendar c = Calendar.getInstance();
        c.setTime(tDate);
//        System.out.println("                   DATES: ");
        for (int count = 0, i = 0; i < SECONDS_PER_YEAR; count += 1, i += secondsPerAttempt) {
            c.add(Calendar.SECOND, (int)secondsPerAttempt);
            Date currDate = c.getTime();
            res.add(currDate);
//            System.out.println("count. " + count + ":      next date: " + currDate + " from beginning: " + i);
        }
        return res;
    }

    public String toString() {
        String s = sender + " sent " + Utilities.dollarify(transactionAmount) + " to " + receiver + " on " + transactionDate;
        if (reoccurring) {
            s += ", re-occurring " + occurring;
        }
        s += ", rate: {" + annualOccurringRate + "}";
//        s += " next: {" + nextTransactionDate +"}";
        s += ", purpose {" + transactionType + "}";
        return s;
    }

    public String serializeEntry() {
        return ">>" + transactionDate + ">>" + sender.getName() + ">>" + receiver.getName() + ">>" + transactionAmount + ">>" + transactionType + ">>" + reoccurring + ">>" + occurring + ">>";
    }

    public static Transaction re_initTransaction(Date date, Entity sender, Entity receiver, int amount, boolean reoccurring, String occurring, TransactionType transactionType) {
        Transaction t = new Transaction(sender, receiver, amount, reoccurring, occurring, transactionType);
        t.setTransactionDate(date);
        t.setFirstTransactionDate(date);
        ArrayList<Transaction> upcomingTransactions =
                t.setUpcomingTransactionDates(
                        t.calculateNextTransactionDate(
                                t.getTransactionDate(), t.getAnnualOccurringRate()
                        )
                );
        System.out.println("UPCOMING: " + upcomingTransactions);
        System.out.println("newT: " + t);
        return t;
    }
}

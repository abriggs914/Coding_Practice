package sample;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

public class Transaction {

    private Date transactionDate;
    private Entity sender;
    private Entity receiver;
    private int transactionAmount;
    private boolean oneTime;
    private String occuring;

    public Transaction(Entity sender, Entity receiver, int transactionAmount, boolean oneTime, String occurring) {
        this.transactionDate = new Date();
        this.sender = sender;
        this.receiver = receiver;
        this.transactionAmount = transactionAmount;
        this.oneTime = oneTime;
        this.occuring = parseOccurring(occurring);
    }

    private String parseOccurring(String occurring) {
        String[] perSplit = occurring.split("per", 2);
        String[] slashSplit = occurring.split("/", 2);
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
        System.out.println("perSplit: " + Arrays.toString(perSplit));
        System.out.println("slashSplit: " + Arrays.toString(slashSplit));
        return "";
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

    public String toString() {
        String s = sender + " is sending " + Main.dollarify(transactionAmount) + " to " + receiver + " at: " + transactionDate;
        if (!oneTime) {
            s += " reoccuring every " + occuring;
        }
        return s;
    }
}

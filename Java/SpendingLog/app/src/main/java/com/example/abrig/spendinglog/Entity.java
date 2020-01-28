package com.example.abrig.spendinglog;

import java.util.ArrayList;

public class Entity {

    private String name;
    private int bankedMoney;
    private int moneySent;
    private int moneyReceived;
    private boolean allowedOverdraft;
    private ArrayList<Transaction> transactions;

    public Entity(String name) {
        this.name = name;
        this.bankedMoney = 0;
        this.moneySent = 0;
        this.moneyReceived = 0;
        this.transactions = new ArrayList<>();
        this.allowedOverdraft = false;
    }

    public Entity(String name, int estimatedBank, boolean... allowedOverdraft) {
        this.name = name;
        this.bankedMoney = estimatedBank;
        this.moneySent = 0;
        this.moneyReceived = 0;
        this.transactions = new ArrayList<>();
        if (allowedOverdraft.length > 0) {
            this.allowedOverdraft = allowedOverdraft[0];
        }
        else {
            this.allowedOverdraft = false;
        }
    }

    public boolean sendMoney(Transaction t) {
        int amount = t.getTransactionAmount();
        if (this.bankedMoney >= amount || allowedOverdraft) {
            Entity receiver = t.getReceiver();
            boolean oneTime = t.getOneTimeStatus();
            String occuring = t.getOccurringStatus();
            this.transactions.add(t);
            this.bankedMoney -= amount;
            this.moneySent += amount;
            return true;
        }
        else {
            return false;
        }
    }

    public void receiveMoney(Transaction t) {
        Entity receiver = t.getReceiver();
        int amount = t.getTransactionAmount();
        boolean oneTime = t.getOneTimeStatus();
        String occuring = t.getOccurringStatus();
        this.transactions.add(t);
        this.bankedMoney += amount;
        this.moneyReceived += amount;
//        System.out.println(name + " is receiving money.");
    }

    public String getCustomerStats() {
        String n = name.substring(0, 1).toUpperCase() + name.substring(1);
        return "\n\tCustomer:\t" + n + "\n\tMoney banked:\t" + Utilities.dollarify(bankedMoney)
                + "\n\tMoney sent:\t\t" + Utilities.dollarify(moneySent)
                + "\n\tMoney received:\t" + Utilities.dollarify(moneyReceived);
    }

    public String getName() {
        return Utilities.title(name);
    }

    public String toString() {
        return getName();
    }

    public int getBankedMoney(){
        return bankedMoney;
    }

    public int getSentMoney() {
        return moneySent;
    }

    public int getReceivedMoney() {
        return moneyReceived;
    }

    public boolean isAllowedOverdraft() {
        return allowedOverdraft;
    }

    public void setAllowedOverdraft(boolean od) {
        this.allowedOverdraft = od;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setBankedMoney(int bankedMoney) {
        this.bankedMoney = bankedMoney;
    }

    public ArrayList<Transaction> getTransactions() {
        return transactions;
    }

    public void addTransaction(Transaction t) {
        this.transactions.add(t);
    }

    public String serializeEntry() {
        String res = "<<" + name + "<<" + bankedMoney + "<<" + moneySent + "<<" + moneyReceived + "<<" + allowedOverdraft + "<<";
        for (Transaction t : transactions) {
            res += t.serializeEntry(); // +"<<";
        }
        return res;
    }

    public static Entity re_initEntity(String name, int balance, int moneySent, int moneyReceived, boolean overdraft) {
        Entity e = new Entity(name, balance);
        e.moneySent = moneySent;
        e.moneyReceived = moneyReceived;
        e.allowedOverdraft = overdraft;
        return e;
    }
}

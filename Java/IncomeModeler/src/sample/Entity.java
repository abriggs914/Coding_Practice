package sample;

import java.util.ArrayList;

/**
 * Entities create Transactions and stores them into its transactions list.
 */

public class Entity {

    private String name;
    private int bankedMoney;
    private int moneySent;
    private int moneyReceived;
    private ArrayList<Transaction> transactions;

    public Entity(String name) {
        this.name = name;
        this.bankedMoney = 0;
        this.moneySent = 0;
        this.moneyReceived = 0;
        this.transactions = new ArrayList<>();
    }

    public void sendMoney(Entity receiver, int amount, boolean oneTime, String occuring) {
        Transaction t = new Transaction(this, receiver, amount, oneTime, occuring);
        this.transactions.add(t);
        this.bankedMoney -= amount;
        this.moneySent += amount;
        System.out.println(name + " is sending money.");
    }

    public void receiveMoney(Entity sender, int amount, boolean oneTime, String occuring) {
        Transaction t = new Transaction(sender, this, amount, oneTime, occuring);
        this.transactions.add(t);
        this.bankedMoney += amount;
        this.moneyReceived += amount;
        System.out.println(name + " is receiving money.");
    }

    public String getCustomerStats() {
        String n = name.substring(0, 1).toUpperCase() + name.substring(1);
        return "\n\tCustomer:\t" + n + "\n\tMoney banked:\t" + Main.dollarify(bankedMoney)
                + "\n\tMoney sent:\t\t" + Main.dollarify(moneySent)
                + "\n\tMoney received:\t" + Main.dollarify(moneyReceived);
    }

    public String getName() {
        return name.substring(0, 1).toUpperCase() + name.substring(1);
    }

    public String toString() {
        return name.substring(0, 1).toUpperCase() + name.substring(1);
    }

    public ArrayList<Transaction> getTransactions() {
        return transactions;
    }
}

package com.example.abrig.spendinglog;

import android.content.SharedPreferences;

import java.util.ArrayList;
import java.util.Map;
import java.util.Set;

public class TransactionHandler {

    private ArrayList<Entity> entities;
    private ArrayList<Transaction> transactions;

    public TransactionHandler() {
        entities = new ArrayList<>();
        transactions = new ArrayList<>();
        loadEntities();
    }

    private void loadEntities() {
        SharedPreferences prefs = MainActivity.prefs;
        Map<String, ?> keyVals = prefs.getAll();
        Set<String> keys = keyVals.keySet();
        for (String str : keys) {
//            /////////////// Using this as a clean up line for sharedprefernces
//            if (str.contains("entry_User")) {
//                MainActivity.prefs.edit().remove(str).commit();
//            }
//            //////////////
            if (str.contains("entity_entry_")) {
                String entityString = (String)keyVals.get(str);
                Entity e = Utilities.parseEntity(entityString);
                addUser(e); // string -> entity
                ArrayList<Transaction> transactions = Utilities.parseTransactions(entityString);
                for (Transaction t : transactions) {
                    e.addTransaction(t);
                }
                addTransactions(transactions);
            }
        }
//        if (prefs.contains("entities_list")) {
//            ArrayList<Entity> entries = (ArrayList<Entity>) prefs.getAll().get("entries_list");
//            for (Entity e : entries) {
//                addUser(e);
//            }
//        }
//        else {
//            MainActivity.prefs.edit().putString()
//        }
    }

    public boolean tryTransaction(Entity sender,
                                  Entity receiver,
                                  int amount,
                                  boolean oneTime,
                                  String occurring) {
        Transaction t = new Transaction(sender, receiver, amount, oneTime, occurring);

//        checkUser(sender);
//        checkUser(receiver);
        boolean validFunds = sender.sendMoney(t);
        if (validFunds) {
            receiver.receiveMoney(t);
            transactions.add(t);
            System.out.println(t);
            return true;
        }
        else {
            System.out.print("Insufficient funds.");
            return false;
        }

    }

    // starts numbering at 1
    public void addUser(Entity user) {
        if (!entities.contains(user)) {
            entities.add(user);
        }
        System.out.println("Adding user: " + user);
        MainActivity.prefs.edit().putString("entity_entry_" + user.getName(), user.serializeEntry());
    }

    public void removeUser(String user) {
        Entity e = getEntityEntry(user);
        if (entities.contains(e)) {
            entities.remove(e);
        }
    }

    public ArrayList<Entity> getEntities() {
        return entities;
    }

    public ArrayList<Transaction> getTransactions() {
        return transactions;
    }

    public int getNumEntities() {
        return entities.size();
    }

    public Entity getEntityEntry(String name) {
        for (Entity e : entities) {
            System.out.println("Entity {" + e.getName() +  "}.");
            if (e.getName().equals(name)) {
                return e;
            }
        }
        System.out.println("Entity {" + name +  "} not found.");
        return null;
    }

    public void addTransaction(Transaction t) {
        this.transactions.add(t);
    }

    public void addTransactions(ArrayList<Transaction> t) {
        this.transactions.addAll(t);
    }
}

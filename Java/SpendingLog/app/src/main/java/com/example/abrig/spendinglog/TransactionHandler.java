package com.example.abrig.spendinglog;

import android.content.Context;
import android.content.SharedPreferences;
import android.widget.Toast;

import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;
import java.util.Set;

public class TransactionHandler {

    private Context context;
    private ArrayList<Entity> entities;
    private ArrayList<Transaction> transactions;
    private TransactionType transactionType;
    private static int entityNumber;

    private String currentFilterString;

    public TransactionHandler(Context context) {
        this.currentFilterString = "00000000";
        this.context = context;
        this.transactionType = new TransactionType("No selection");
        this.transactionType = new TransactionType("Custom");
        this.entities = new ArrayList<>();
        this.transactions = new ArrayList<>();
        entityNumber = 0;
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
            if (str.contains("entity_entry_") && !str.equals("entity_entry_User")) {
                String entityString = (String)keyVals.get(str);
                Entity e = Utilities.parseEntity(entityString);
//                e.setIdString(genEntityID(e));
                addUser(e); // string -> entity
                ArrayList<Transaction> transactionsList = Utilities.parseTransactions(entityString);
                for (Transaction t : transactionsList) {
                    e.addTransaction(t);
                }
                addTransactions(transactionsList);
            }
            else if (str.equals("entity_entry_User")) {
                String entityString = (String)keyVals.get(str);
                Entity e = Utilities.parseEntity(entityString);
                entities.add(e);
                ArrayList<Transaction> transactionsList = Utilities.parseTransactions(entityString);
                for (Transaction t : transactionsList) {
                    e.addTransaction(t);
                }
                addTransactions(transactionsList);
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
                                  String occurring,
                                  TransactionType transactionType) {
        Transaction t = new Transaction(sender, receiver, amount, oneTime, occurring, transactionType);

//        checkUser(sender);
//        checkUser(receiver);
        try {
            boolean validFunds = sender.sendMoney(t);
            boolean differentPeople = sender != receiver;
            if (validFunds && differentPeople) {
                receiver.receiveMoney(t);
                addTransaction(t);
                return true;
            } else {
                System.out.print("Insufficient funds.");
                return false;
            }
        }
        catch (Exception e) {
            Toast.makeText(context, "Invalid transaction", Toast.LENGTH_LONG).show();
            return false;
        }
    }

    // starts numbering at 1
    public void addUser(Entity user) {
        if (!entities.contains(user)) {
            entities.add(user);
//            if (user.getIdString() == null){
//                user.setIdString(genEntityID(user.getName()));
//            }
        }
        System.out.println("Adding user: " + user);
        String storedName = (String) MainActivity.prefs.getAll().get("user_name");
        if (storedName.equals(user.getName())) {
            SharedPreferencesWriter.write("entity_entry_User", user.serializeEntry());
        }
        else {
            SharedPreferencesWriter.write("entity_entry_" + user.getName(), user.serializeEntry());
        }
    }

//    public String genEntityID(Entity e) {
//        String id = "";
//        String name = e.getName();
//        String[] splitName = name.split("[ ;'!@#$%^&*(),./?|`~+={}]");
//        System.out.println("splitName: " + Arrays.toString(splitName));
//        System.out.println("User: " + e + " ID: \"" + id + "\"");
//        return id;
//    }

    public static String genEntityID(String name) {
        String id = "";
        String[] splitName = name.split("[ ;'!@#$%^&*(),./?|`~+={}<>]");
        System.out.println("splitName: " + Arrays.toString(splitName));
        entityNumber += 1;
        if (splitName.length > 1) {
            id += splitName[1].substring(0, Math.min(3, splitName[1].length())).toUpperCase();
            id += splitName[0].toUpperCase();
        } else if (splitName.length == 1) {
            id += splitName[0].toUpperCase();
        }
        id += String.format("|%05d|", entityNumber);
        System.out.println("ENTITY NUMBER: " + entityNumber);
        System.out.println("User: " + name + " ID: \"" + id + "\"");
        return id;
    }

    public void removeUser(String user) {
        Entity e = getEntityEntry(user);
        entities.remove(e);
        SharedPreferencesWriter.deleteEntityEntry(e);
    }

    public void removeUser(Entity user) {
        entities.remove(user);
        SharedPreferencesWriter.deleteEntityEntry(user);
    }

    public ArrayList<Entity> getEntities() {
        return entities;
    }

    public ArrayList<String> getEntitiesIds() {
        ArrayList<String> ids = new ArrayList<>();
        for (Entity e : entities) {
            ids.add(e.getIdString());
        }
        return ids;
    }

    public ArrayList<String> getEntitiesNames() {
        ArrayList<String> names = new ArrayList<>();
        for (Entity e : entities) {
            names.add(e.getName());
        }
        return names;
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

//    public TransactionType getTransactionTypeEntry(String transactionTypeString) {
//        ArrayList<TransactionType> types = TransactionType.getTypes();
//        for (TransactionType t : types) {
//            if (t.getName().equals(transactionTypeString)) {
//                return t;
//            }
//        }
//        return null;
//    }

    public void addTransaction(Transaction t) {
//        Toast.makeText(this.context, "Editing profile information...", Toast.LENGTH_SHORT).show();
        System.out.println("trying to insert transaction {" + transactions + "}");
        if (!this.transactions.contains(t)) {
            this.transactions.add(t);
        }
        System.out.println("transactions after insertion: " + transactions);
    }

    public void addTransactions(ArrayList<Transaction> tList) {
        for (Transaction t : tList) {
            addTransaction(t);
        }
    }

    public void addEntity(Entity e) {
        if (!this.entities.contains(e)) {
            this.entities.add(e);
        }
    }

    public boolean ensureValidDelete(Entity e) {
        for (Transaction t : transactions) {
            Entity sender = t.getSender();
            Entity receiver = t.getReceiver();
            String senderID = sender.getIdString();
            String receiverID = receiver.getIdString();
//            if (senderID == null) {
//                sender.setIdString(genEntityID(sender.getName()));
//            }
//            if (receiverID == null) {
//                receiver.setIdString(genEntityID(receiver.getName()));
//            }
            System.out.println("transaction: " + t);
            System.out.println("comparing: " + e.getIdString() + " vs. ( " + sender.getIdString() + " and " + receiver.getIdString() + " )");
            if (e.getIdString().equals(sender.getIdString()) || e.getIdString().equals(receiver.getIdString())) {
                return false;
            }
        }
        return true;
    }

    public void resetTransactionHandler() {
        this.transactions.clear();
        this.entities.clear();
        this.entityNumber = 0;
    }

    public void updateTransactions(Entity oldE, Entity newE) {
        System.out.println("Updating transactions from old: " + oldE + " to new: " + newE + ", with transactions: " + transactions);
        ArrayList<Transaction> arr = new ArrayList<>();
        for (Transaction t : transactions) {
            Entity sender = t.getSender();
            Entity receiver = t.getReceiver();
//            updateTransactions(sender.getTransactions(), oldE, newE);
//            updateTransactions(receiver.getTransactions(), oldE, newE);
            System.out.println("PRE-editing: " + t);
            if (sender.getIdString().equals(oldE.getIdString())) {
                t.setSender(newE);
            }
            if (receiver.getIdString().equals(oldE.getIdString())) {
                t.setReceiver(newE);
            }
            System.out.println("POST-editing: " + t);
            arr.add(t);
        }
        transactions.clear();
        addTransactions(arr);
        SharedPreferencesWriter.re_writePrefs();
    }

    public void updateUserEntity(Entity oldE, Entity newE) {
        boolean handled = false;
        ArrayList<Entity> arr = new ArrayList<>();
        for (Entity en : entities) {
            if (en.getIdString().equals(oldE.getIdString())) {
                for (Transaction t : en.getTransactions()) {
                    Entity sender = t.getSender();
                    Entity receiver = t.getReceiver();
                    if (sender.getIdString().equals(en.getIdString())) {
                        t.setSender(newE);
                    }
                    if (receiver.getIdString().equals(en.getIdString())) {
                        t.setReceiver(newE);
                    }
                    newE.addTransaction(t);
                }
                arr.add(newE);
                handled = true;
            }
            else {
                arr.add(en);
            }
        }
        if (!handled) {
            arr.add(newE);
        }
        entities.clear();
        entities.addAll(arr);
        SharedPreferencesWriter.write("entity_entry_User", newE.serializeEntry());
        SharedPreferencesWriter.re_writePrefs();
    }

    public TransactionType getTransactionTypeEntry(String transactionTypeString) {
        transactionTypeString = transactionTypeString.substring(0, 1).toUpperCase() + transactionTypeString.substring(1);
        ArrayList<TransactionType> types = TransactionType.getTypes();
        for(TransactionType t : types) {
            if (t.getName().equals(transactionTypeString)) {
                return t;
            }
        }
        return new TransactionType(transactionTypeString);
    }

    // Sets the currentFilterString to the parsed value
    // of the parameter string.
    // 0    -   null
    // 1    -   set
    // 9    -   reset
    public void setInDepthFilters(String filterString) {
        char[] arr = this.currentFilterString.toCharArray();
        for (int i = 0; i < filterString.length(); i++) {
            char currChar = filterString.charAt(i);
            if (currChar == '1') {
                arr[i] = '1';
            }
            if (currChar == '9') {
                arr[i] = '0';
            }
        }
        this.currentFilterString = new String(arr);
    }

    public String getCurrentFilterString() {
        return this.currentFilterString;
    }
}
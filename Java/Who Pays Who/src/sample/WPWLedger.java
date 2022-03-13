package sample;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Set;

import static java.lang.Math.*;

public class WPWLedger {

    private ArrayList<WPWTransaction> transactions;
    private boolean hasProcessed;

    public WPWLedger() {
        this.init();
    }

    private void init() {
        this.transactions = new ArrayList<>();
        this.hasProcessed = false;
    }

    /**
     * Calculate the value that each entity should have chipped into the overall pot.
     * @return double value representing how much each entity should contribute.
     */
    public double calcEqualShare() {
        double share = 0;
        for (WPWTransaction transaction : this.transactions) {
            HashMap<WPWEntity, Double> fromData = transaction.getFromData();
            WPWEntity toEntity = transaction.getToEntity();
            double amount;
            if (toEntity == WPWEntity.POT) {
                for (WPWEntity entity : fromData.keySet()) {
                    if (entity != WPWEntity.POT) {
                        amount = fromData.get(entity);
                        share += amount;
                    }
                }
            }
        }
        int n = this.getAllEntities(false).size();
        n = ((n == 0)? 1 : n);
        return share / n;
    }

    /**
     * Get a list of all unique entities from the transactions list.
     * @return ArrayList of WPWEntity objects.
     */
    public ArrayList<WPWEntity> getAllEntities() {
        ArrayList<WPWEntity> entities = new ArrayList<>();
        for (WPWTransaction transaction : this.transactions) {
            ArrayList<WPWEntity> entity_list = transaction.getEntities();
            for (WPWEntity entity : entity_list) {
                if (!entities.contains(entity)) {
                    entities.add(entity);
                }
            }
        }
        return entities;
    }

    /**
     * Get a list of all unique entities from the transactions list.
     * @return ArrayList of WPWEntity objects.
     */
    public ArrayList<WPWEntity> getAllEntities(boolean includePot) {
        ArrayList<WPWEntity> entities = new ArrayList<>();
        for (WPWTransaction transaction : this.transactions) {
            ArrayList<WPWEntity> entity_list = transaction.getEntities(includePot);
            for (WPWEntity entity : entity_list) {
                if (!entities.contains(entity)) {
                    entities.add(entity);
                }
            }
        }
        return entities;
    }

    public WPWTransaction createNewTransaction(String entityName, double amount) {
        WPWEntity entity = this.lookUpEntity(entityName);
        if (entity == null) {
            entity = new WPWEntity(entityName);
        }
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);
        WPWTransaction transaction = new WPWTransaction(new Date(), h, WPWEntity.POT);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(String entityName, double amount, String entityToName) {
        WPWEntity entity = this.lookUpEntity(entityName);
        if (entity == null) {
            entity = new WPWEntity(entityName);
        }
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);

        WPWEntity entityTo = this.lookUpEntity(entityToName);
        if (entityTo == null) {
            entityTo = new WPWEntity(entityToName);
        }
        WPWTransaction transaction = new WPWTransaction(new Date(), h, entityTo);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(String entityName, double amount, Date dateIn) {
        WPWEntity entity = this.lookUpEntity(entityName);
        if (entity == null) {
            entity = new WPWEntity(entityName);
        }
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);
        WPWTransaction transaction = new WPWTransaction(dateIn, h, WPWEntity.POT);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(String entityName, double amount, WPWEntity toEntity) {
        WPWEntity entity = this.lookUpEntity(entityName);
        if (entity == null) {
            entity = new WPWEntity(entityName);
        }
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);
        WPWTransaction transaction = new WPWTransaction(new Date(), h, toEntity);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(String entityName, double amount, WPWEntity toEntity, Date dateIn) {
        WPWEntity entity = this.lookUpEntity(entityName);
        if (entity == null) {
            entity = new WPWEntity(entityName);
        }
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);
        WPWTransaction transaction = new WPWTransaction(dateIn, h, toEntity);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(WPWEntity entity, double amount) {
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);
        WPWTransaction transaction = new WPWTransaction(new Date(), h, WPWEntity.POT);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(WPWEntity entity, double amount, Date dateIn) {
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);
        WPWTransaction transaction = new WPWTransaction(dateIn, h, WPWEntity.POT);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(WPWEntity entity, double amount, WPWEntity toEntity) {
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);
        WPWTransaction transaction = new WPWTransaction(new Date(), h, toEntity);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(WPWEntity entity, double amount, WPWEntity toEntity, Date dateIn) {
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);
        WPWTransaction transaction = new WPWTransaction(dateIn, h, toEntity);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(String entityName, double amount, String entityToName, Date dateIn) {
        WPWEntity entity = this.lookUpEntity(entityName);
        if (entity == null) {
            entity = new WPWEntity(entityName);
        }
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);

        WPWEntity entityTo = this.lookUpEntity(entityToName);
        if (entityTo == null) {
            entityTo = new WPWEntity(entityToName);
        }
        WPWTransaction transaction = new WPWTransaction(dateIn, h, entityTo);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(WPWEntity entity, double amount, String entityToName) {
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);

        WPWEntity entityTo = this.lookUpEntity(entityToName);
        if (entityTo == null) {
            entityTo = new WPWEntity(entityToName);
        }
        WPWTransaction transaction = new WPWTransaction(new Date(), h, entityTo);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(WPWEntity entity, double amount, String entityToName, Date dateIn) {
        HashMap<WPWEntity, Double> h = new HashMap<>();
        h.put(entity, amount);

        WPWEntity entityTo = this.lookUpEntity(entityToName);
        if (entityTo == null) {
            entityTo = new WPWEntity(entityToName);
        }
        WPWTransaction transaction = new WPWTransaction(dateIn, h, entityTo);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(HashMap<WPWEntity, Double> fromEntities) {
        WPWTransaction transaction = new WPWTransaction(new Date(), fromEntities, WPWEntity.POT);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(HashMap<WPWEntity, Double> fromEntities, Date dateIn) {
        WPWTransaction transaction = new WPWTransaction(dateIn, fromEntities, WPWEntity.POT);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    public WPWTransaction createNewTransaction(HashMap<WPWEntity, Double> fromEntities, Date dateIn, WPWEntity toEntity) {
        WPWTransaction transaction = new WPWTransaction(dateIn, fromEntities, toEntity);

        boolean logSuccess = this.logTransaction(transaction);
        if (!logSuccess) {
            System.out.println("Failed to log transaction: {" + transaction + "}");
        }
        return transaction;
    }

    /**
     * Look up an entity based on a given name.
     * @param name String value representing the name of an entity.
     * @return WPWEntity object if matching name found else null.
     */
    public WPWEntity lookUpEntity(String name) {
        ArrayList<WPWEntity> entities = this.getAllEntities();
        for (WPWEntity entity : entities) {
            if (entity.getName() == name) {
                return entity;
            }
        }
        return null;
    }

    private boolean logTransaction(WPWTransaction transaction) {
        boolean success = false;
        // TODO this should accurately reject / grant
        success = transaction != null;
        this.transactions.add(transaction);
        return success;
    }

    public void setTransactions(ArrayList<WPWTransaction> transactions) {
        this.transactions = transactions;
    }

    public void setHasProcessed(boolean hasProcessed) {
        this.hasProcessed = hasProcessed;
    }

    public ArrayList<WPWTransaction> getTransactions() {
        return this.transactions;
    }

    public boolean hasProcessed() {
        return hasProcessed;
    }

    /**
     * Call this after all transactions have been finalized.
     * This does a pass of all entities and updates their balances.
     */
    public void processTransaction() {
        HashMap<WPWEntity, Double> fromData;
        double amount;
        for (WPWTransaction transaction : this.transactions) {
            fromData = transaction.getFromData();
            for (WPWEntity entity : fromData.keySet()) {
                amount = fromData.get(entity);
                entity.addFromBalance(amount);
            }
            transaction.getToEntity().addToBalance(transaction.calcFromTotal());
        }
        this.setHasProcessed(true);
    }

    public HashMap<WPWEntity, Double> getOwingEntities(boolean getCopies) {
        HashMap<WPWEntity, Double> owingEntities = new HashMap<>();
        if (!this.hasProcessed) {
            System.out.println("This ledger has not processed it's transactions yet.\nUnable to return owing entities.");
            return owingEntities;
        }
        double eqShare = this.calcEqualShare();
        double balance;
        double diff;
        for (WPWEntity entity : this.getAllEntities(false)) {
            balance = entity.getBalance();
            diff = balance + eqShare;
            if (diff > 0) {
                if (getCopies) {
                    owingEntities.put(new WPWEntity(entity.getName(), entity.getBalance()), diff);
                }
                else {
                    owingEntities.put(entity, diff);
                }
            }
        }
        return owingEntities;
    }

    public HashMap<WPWEntity, Double> getOwedEntities(boolean getCopies) {
        HashMap<WPWEntity, Double> owedEntities = new HashMap<>();
        if (!this.hasProcessed) {
            System.out.println("This ledger has not processed it's transactions yet.\nUnable to return owing entities.");
            return owedEntities;
        }
        double eqShare = this.calcEqualShare();
        double balance;
        double diff;
        for (WPWEntity entity : this.getAllEntities(false)) {
            balance = entity.getBalance();
            diff = balance + eqShare;
            if (diff < 0) {
                if (getCopies) {
                    owedEntities.put(new WPWEntity(entity.getName(), entity.getBalance()), diff);
                }
                else {
                    owedEntities.put(entity, diff);
                }
            }
        }
        return owedEntities;
    }

    // h -> a 20 arraylist<hashmap<WPWEntity, hashmap<WPWEntity, Double>>>
    // e -> k 15
    public ArrayList<HashMap<WPWEntity, HashMap<WPWEntity, Double>>> whoPaysWho(boolean useCopies) {
        ArrayList<HashMap<WPWEntity, HashMap<WPWEntity, Double>>> payers = new ArrayList<>();
        if (!this.hasProcessed) {
            System.out.println("This ledger has not processed it's transactions yet.\nUnable to calculate who should pay who yet.");
            return payers;
        }
        HashMap<WPWEntity, Double> owingEntities = this.getOwingEntities(useCopies);
        HashMap<WPWEntity, Double> owedEntities = this.getOwedEntities(useCopies);
        int ogn = owingEntities.size();
        int odn = owedEntities.size();
        if (ogn == 0) {
            System.out.println("There are no entities who currently owe money");
        }
        if (odn == 0) {
            System.out.println("There are no entities who are currently owed money");
        }
        if (odn == 0 || ogn == 0) {
            System.out.println("Error not enough entities owing {" + ogn + "} compared to owed: {" + odn + "}");
            return payers;
        }

        double eqShare = this.calcEqualShare();
        double owingD;
        double owedD;
        double diff;
        int i, j, x;
//        for (WPWEntity owingE : owingEntities.keySet()) {
//            for (WPWEntity owedE : owedEntities.keySet()) {

        Object[] owingEntitiesA = owingEntities.keySet().toArray();
        Object[] owedEntitiesA = owedEntities.keySet().toArray();

        i = 0;
//        x = 5;
        while (i < owingEntitiesA.length) {
            System.out.println("owing: " + owingEntities);
            System.out.println("owed: " + owedEntities);
            j = 0;
            WPWEntity owingE = (WPWEntity) owingEntitiesA[i];
            while (j < owedEntitiesA.length) {
                WPWEntity owedE = (WPWEntity) owedEntitiesA[j];

//        for (int i = 0; i < owingEntities.size(); i++) {
//            WPWEntity owingE = owingEntities.get()
//            for (WPWEntity owedE : owedEntities.keySet()) {


                owingD = owingEntities.get(owingE);
                owedD = owedEntities.get(owedE);
                diff = owingD + owedD;
//                diff = ((abs(diff) < abs(owingD))? diff : abs(owingD));
//                diff = ((abs(diff) < abs(owedD))? diff : abs(owedD));

//                System.out.println("DIFF: " + diff + ", owingD: " + owingD + ", owedD: " + owedD);
                diff = ((abs(diff) < min(abs(owingD), abs(owedD)))? diff : ((abs(owedD) < abs(owingD))? owedD : owingD));
                diff = owingD;


                System.out.println("\tdiff: {" + diff + "}, owingD: {" + owingD + "}, owedD: {" + owedD + "}, OWING: {" + owingE + "}, OWED: {" + owedE + "}");
                if (owedE.getBalance() != 0 && owingE.getBalance() != 0 && owingE.getBalance() != -eqShare) {
                    if (diff == 0) {
                        // square payment, remove both entities from their HashMaps
                        System.out.println("square");
                        HashMap<WPWEntity, HashMap<WPWEntity, Double>> owingH = new HashMap<>();
                        HashMap<WPWEntity, Double> owedH = new HashMap<>();
                        owedH.put(owedE, owingD);
                        owingH.put(owingE, owedH);
                        payers.add(owingH);
                        owedE.addToBalance(owingD);
                        owingE.addFromBalance(owedD);
//                        owingEntities.remove(owingE);
//                        owedEntities.remove(owedE);
                    } else if (diff > 0) {
                        System.out.println("A diff > 0: {" + diff + "}");
                        HashMap<WPWEntity, HashMap<WPWEntity, Double>> owingH = new HashMap<>();
                        HashMap<WPWEntity, Double> owedH = new HashMap<>();
                        owedH.put(owedE, diff);

                        owedE.addToBalance(diff);
                        owingE.addFromBalance(diff);
                        owedEntities.put(owedE, owedE.getBalance() + eqShare);
                        owingEntities.put(owingE, owingE.getBalance() + eqShare);

                        owingH.put(owingE, owedH);
                        payers.add(owingH);
                    } else {
                        System.out.println("B diff < 0: {" + diff + "}");
                        HashMap<WPWEntity, HashMap<WPWEntity, Double>> owingH = new HashMap<>();
                        HashMap<WPWEntity, Double> owedH = new HashMap<>();
                        owedH.put(owedE, diff);

                        owedE.addToBalance(-diff);
                        owingE.addFromBalance(-diff);
                        owedEntities.put(owedE, owedE.getBalance() + eqShare);
                        owingEntities.put(owingE, owingE.getBalance() + eqShare);

                        owingH.put(owingE, owedH);
                        payers.add(owingH);
                    }
                }
                if (owedE.getBalance() + eqShare > 0) {
                    // this entity has received too much.
//                    System.out.println("RECEIVED");
                    i = owingEntitiesA.length;
                    j = owedEntitiesA.length;
                    owedEntities.remove(owedE);
                    owedEntitiesA = owedEntities.keySet().toArray();
                    owingEntities.put(owedE, owedE.getBalance() + eqShare);
                    owingEntitiesA = owingEntities.keySet().toArray();
                }
                if (owingE.getBalance() + eqShare < 0) {
                    // this entity has given too much.
//                    System.out.println("GIVEN");
                    i = owingEntitiesA.length;
                    j = owedEntitiesA.length;
                    owingEntities.remove(owingE);
                    owingEntitiesA = owingEntities.keySet().toArray();
                    owedEntities.put(owingE, owingE.getBalance() + eqShare);
                    owedEntitiesA = owedEntities.keySet().toArray();
                }
                if (i == owingEntitiesA.length && j == owedEntitiesA.length) {
                    break;
                }
                j++;
            }
            i++;
//            System.out.println("(i, j): (" + i + "," + j + "), owingEntitiesA.length - 1: " + (owingEntitiesA.length - 1) + ", owedEntitiesA.length - 1: " + (owedEntitiesA.length - 1));
            if (i >= owingEntitiesA.length) {
                if (!WPWLedger.isSquare(WPWLedger.collectEntities(payers), -eqShare)) {
                    System.out.println("reset");
                    i = 0;
//                    x--;
                }
            }
//            if (x == 0) {
//                i = owingEntitiesA.length;
//            }
        }
        return payers;
    }

    @Override
    public String toString() {
        return "<WPWLedger nTransactions: {" + transactions.size() + "}, involving nEntities: {" + this.getAllEntities().size() + "}>";
    }

    /**
     * Double check that all entities in a list have the same balance.
     * @param entities ArrayList of WPWEntities.
     * @param eqShare Double value that all entites should have as a balance.
     * @return T if all balances match, else F.
     */
    private static boolean isSquare(ArrayList<WPWEntity> entities, double eqShare) {
        for (WPWEntity entity : entities) {
            if (entity.getBalance() != eqShare) {
                return false;
            }
        }
        return true;
    }


    /**
     * Used to pull a unique entity list from the result of a call to owingEntities or OwedEntities
     * @param hMap return value from either of the collection list methods.
     * @return a list of unique entites.
     */
    public static ArrayList<WPWEntity> collectEntities(HashMap<WPWEntity, Double> hMap) {
        ArrayList<WPWEntity> entities = new ArrayList<>();
        for (WPWEntity entity : hMap.keySet()) {
            if (!entities.contains(entity)) {
                entities.add(entity);
            }
        }
        return entities;
    }

    /**
     * Used to pull a unique entity list from the result of a call to whoPaysWho.
     * @param list return value from WPWLedger.whoPaysWho.
     * @return a list of unique entites.
     */
    public static ArrayList<WPWEntity> collectEntities(ArrayList<HashMap<WPWEntity, HashMap<WPWEntity, Double>>> list) {
        ArrayList<WPWEntity> entities = new ArrayList<>();
        for (HashMap<WPWEntity, HashMap<WPWEntity, Double>> fromMap : list) {
            for(WPWEntity fromEntity : fromMap.keySet()) {
                HashMap<WPWEntity, Double> toMap = fromMap.get(fromEntity);
                for (WPWEntity entity : toMap.keySet()) {
                    if (!entities.contains(entity)) {
                        entities.add(entity);
                    }
                }
                if (!entities.contains(fromEntity)) {
                    entities.add(fromEntity);
                }
            }
        }
        return entities;
    }
}

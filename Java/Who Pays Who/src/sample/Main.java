package sample;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;

public class Main {

    private static void runTest1() {
        ArrayList<WPWEntity> entities = new ArrayList<>();
        entities.add(new WPWEntity("Avery"));

        String a = "this is a string 1";
        String b = "this is a string 2";
        String c;
        c = a;
        a = "This is a String 3";

        System.out.println("a: {" + a + "}, b: {" + b + "}, c: {" + c + "}");

        entities.get(0).setBalance(14.5);
        System.out.println("Balance: " + entities.get(0).getBalance());
        System.out.println("entities: " + entities);
    }

    private static void runTest2() {
        WPWEntity e1 = new WPWEntity("Avery");
        WPWEntity e2 = new WPWEntity("Kristen");
        WPWEntity e3 = new WPWEntity("Emily");
        WPWEntity e4 = new WPWEntity("Hayley");

        HashMap<WPWEntity, Double> h1 = new HashMap<>();
        h1.put(e1, 45.0);
        WPWTransaction t1 = new WPWTransaction(DateHandler.createDateAndTime("11/03/2022 23:28:00"), h1, WPWEntity.POT);

        HashMap<WPWEntity, Double> h2 = new HashMap<>();
        h2.put(e2, 25.0);
        WPWTransaction t2 = new WPWTransaction(DateHandler.createDateAndTime("11/03/2022 23:28:00"), h2, WPWEntity.POT);

        HashMap<WPWEntity, Double> h3 = new HashMap<>();
        h3.put(e3, 25.0);
        WPWTransaction t3 = new WPWTransaction(DateHandler.createDateAndTime("11/03/2022 23:28:00"), h3, WPWEntity.POT);

        HashMap<WPWEntity, Double> h4 = new HashMap<>();
        h4.put(e4, 5.0);
        WPWTransaction t4 = new WPWTransaction(DateHandler.createDateAndTime("11/03/2022 23:28:00"), h4, WPWEntity.POT);

        ArrayList<WPWTransaction> ts1 = new ArrayList<>();
        ts1.add(t1);
        ts1.add(t2);
        ts1.add(t3);
        ts1.add(t4);
        WPWLedger ledger = new WPWLedger();
        ledger.setTransactions(ts1);

        System.out.println("Equal Share {" + ledger.calcEqualShare() + "}");
    }

    private static void runTest3() {
        WPWLedger ledger = new WPWLedger();
        ledger.createNewTransaction("Avery", 47.5);
        ledger.createNewTransaction("Kristen", 27.5);
        ledger.createNewTransaction("Emily", 20);
        ledger.createNewTransaction("Hayley", 5);
//        ledger.createNewTransaction("Hayley", 20, "Avery");
        System.out.println("Equal Share {" + ledger.calcEqualShare() + "}");
        System.out.println(ledger);
        System.out.println(ledger.getAllEntities(true));
        System.out.println(ledger.getTransactions());

        ledger.processTransaction();

        System.out.println("\n\tledger\n" + ledger);
        System.out.println("\n\tledger.getAllEntities(true)\n" + ledger.getAllEntities(true));
        System.out.println("\n\tledger.getTransactions()\n" + ledger.getTransactions());

        System.out.println("\n\tledger.getOwingEntities()\n" + ledger.getOwingEntities(true));
        System.out.println("\n\tledger.getOwedEntities()\n" + ledger.getOwedEntities(true));

        ArrayList<HashMap<WPWEntity, HashMap<WPWEntity, Double>>> whoPaysWho = ledger.whoPaysWho(false);
        String whoPaysWhoS = "";
        for (HashMap<WPWEntity, HashMap<WPWEntity, Double>> fromMap : whoPaysWho) {
            for (WPWEntity fromEntity : fromMap.keySet()) {
                whoPaysWhoS += "\tFrom: " + fromEntity;
                HashMap<WPWEntity, Double> toMap = fromMap.get(fromEntity);
                for (WPWEntity toPay : toMap.keySet()) {
                    whoPaysWhoS += "\n\t\tTo: " + toPay + "\t\t$" + toMap.get(toPay);
                }
            }
            whoPaysWhoS += "\n";
        }
        System.out.println("\n\tledger.whoPaysWho()\n" + whoPaysWhoS);
//        System.out.println(ledger.getAllEntities(true));
    }

    private static void runTest4() {
        WPWLedger ledger = new WPWLedger();


//        ledger.createNewTransaction("Avery", 47.5);
//        ledger.createNewTransaction("Kristen", 27.5);
//        ledger.createNewTransaction("Emily", 20);
//        ledger.createNewTransaction("Hayley", 5);
////        ledger.createNewTransaction("Hayley", 20, "Avery");


//        ledger.createNewTransaction("Avery", 45);
//        ledger.createNewTransaction("Kristen", 25);
//        ledger.createNewTransaction("Emily", 25);
//        ledger.createNewTransaction("Hayley", 5);
////        ledger.createNewTransaction("Hayley", 20, "Avery");


//        ledger.createNewTransaction("Avery", 25);
//        ledger.createNewTransaction("Kristen", 75);
//        ledger.createNewTransaction("Emily", 25, "Hayley");
//        ledger.createNewTransaction("Hayley", 50, "Kristen");
////        ledger.createNewTransaction("Hayley", 20, "Avery");


        ledger.createNewTransaction("Avery", 25);
        ledger.createNewTransaction("Kristen", 75);
        ledger.createNewTransaction("Emily", 25, "Hayley");
        ledger.createNewTransaction("Hayley", 50, "Kristen");
        ledger.createNewTransaction("Avery", 100);
        ledger.createNewTransaction("Kristen", 75);
        ledger.createNewTransaction("Emily", 50);
        ledger.createNewTransaction("Hayley", 100);
        ledger.createNewTransaction("Emily", 20, "Hayley");


        ledger.processTransaction();
        System.out.println("Equal Share {" + ledger.calcEqualShare() + "}");

        ArrayList<HashMap<WPWEntity, HashMap<WPWEntity, Double>>> whoPaysWho = ledger.whoPaysWho(false);
        StringBuilder whoPaysWhoS = new StringBuilder();
        for (HashMap<WPWEntity, HashMap<WPWEntity, Double>> fromMap : whoPaysWho) {
            for (WPWEntity fromEntity : fromMap.keySet()) {
                whoPaysWhoS.append("\tFrom: ").append(fromEntity);
                HashMap<WPWEntity, Double> toMap = fromMap.get(fromEntity);
                for (WPWEntity toPay : toMap.keySet()) {
                    whoPaysWhoS.append("\n\t\tTo: ").append(toPay).append("\t\t$").append(toMap.get(toPay));
                }
            }
            whoPaysWhoS.append("\n");
        }
        System.out.println("\n\tledger.whoPaysWho()\n" + whoPaysWhoS);
        System.out.println("\n\tEntities:\n" + WPWLedger.collectEntities(whoPaysWho));
        System.out.println("\n\tEntities:\n" + ledger.getAllEntities());
//        System.out.println(ledger.getAllEntities(true));
    }

    public static void main(String[] args) {
//        runTest1();
//        runTest2();
//        runTest3();
        runTest4();
    }
}

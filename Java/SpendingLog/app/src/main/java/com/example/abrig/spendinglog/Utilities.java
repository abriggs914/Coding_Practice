package com.example.abrig.spendinglog;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.text.DecimalFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

public class Utilities {

    public static String dollarify(int transactionAmount) {
        double m = transactionAmount / 100.0;
        return "$ " + String.format("% .2f", m);
    }

    public static void createCSV(ArrayList<Transaction> transactions) {
        CSVWriter writer = new CSVWriter();
        ArrayList<String> header = new ArrayList<>(Arrays.asList("Date", "Sender", "Receiver", "Amount"));
        writer.writeFile(header, transactions);
    }

    public static boolean checkInt(String n) {
        try {
            BigInteger i = new BigInteger(n.trim());
            return true;
        }
        catch (Exception e) {
            return false;
        }
    }
    public static boolean checkDec(String n) {
        try {
            BigDecimal i = new BigDecimal(n.trim());
            return true;
        }
        catch (Exception e) {
            return false;
        }
    }

    public static String removeCommas(String str) {
        String[] noCommas = str.split(",");
        String res = "";
        for (String s : noCommas) {
            res += s;
        }
        return res;
    }

    public static String removeMoneySymbols(String str) {
        String[] noCommas = str.split("[$]");
        String res = "";
        for (String s : noCommas) {
            res += s;
        }
        return res;
    }

    public static int parseMoney(String moneyString) {
        moneyString = removeCommas(moneyString);
        moneyString = removeMoneySymbols(moneyString);
        moneyString = moneyString.trim();
        System.out.println("moneyString for parsing: " + moneyString);
        boolean isInt = checkInt(moneyString);
        boolean isDec = checkDec(moneyString);
        int idx = moneyString.indexOf("$");
        if (idx >= 0 && (!isInt && !isDec)) {
            isInt = checkInt(moneyString.substring(idx));
            isDec = checkDec(moneyString.substring(idx));
        }

        if (isInt) {
            return Integer.parseInt(moneyString) * 100;
        }
        else if (isDec) {
            return (int) Math.round(Double.parseDouble(moneyString) * 100);
        }
        return 0;
    }

    public static String title(String s) {
        s = s.trim();
        if (s.length() == 0) {
            return "";
        }
        else {
            return s.substring(0,1).toUpperCase() + s.substring(1);
        }
    }

    public static String titlifyName(String name) {
        String[] splitName = name.split(" ");
        String res = "";
        for (String s : splitName) {
            res += title(s) + " ";
        }
        return res;
    }

    // |*| Entity
    // name, balance, sentTotal, receivedTotal, overdraft
    // |^| Transactions list
    // date, sender, receiver, amount, oneTime, occurring
    public static Entity parseEntity(String entry) {
        System.out.println("parsing entry: " + entry);
        int idx = entry.indexOf(">>");
        idx = ((idx < 0)? entry.length() : idx);

        String[] entityParse = entry.split("<<");
        String[] transactionParse = entry.substring(idx).split(">>");
        System.out.println("entityParse: " + Arrays.toString(entityParse));
        System.out.println("transactionParse: " + Arrays.toString(transactionParse));

        String name = entityParse[1];
        int balance = Integer.parseInt(entityParse[2]);
        int moneySent = Integer.parseInt(entityParse[3]);
        int moneyReceived = Integer.parseInt(entityParse[4]);
        boolean overdraft = Boolean.parseBoolean(entityParse[5]);
        Entity e = Entity.re_initEntity(name, balance, moneySent, moneyReceived, overdraft);
//        System.out.println("ENTITY PARSED: " + e);
        return e;
    }

    public static ArrayList<Transaction> parseTransactions(String str) {
        ArrayList<Transaction> transactions = new ArrayList<>();
        System.out.println("parsing entry: " + str);
        int idx = str.indexOf(">>");
        idx = ((idx < 0)? str.length() : idx);

        String[] entityParse = str.split("<<");
        String[] transactionParse = str.substring(idx).split(">>");

        for (int i = 1; i < transactionParse.length; i += 6) {
            Date date = parseDate(transactionParse[i]);
            Entity sender = getEntity(transactionParse[i + 1]);
            Entity receiver = getEntity(transactionParse[i + 2]);
            int amount = Integer.parseInt(transactionParse[i + 3]);
            boolean reoccurring = Boolean.parseBoolean(transactionParse[i + 4]);
            String occurring = "NA";
            if (reoccurring) {
                occurring = transactionParse[i + 5];
            }
            else {
                i -= 1;
            }

            System.out.println("date: " + date);
            System.out.println("sender: " + sender);
            System.out.println("receiver: " + receiver);
            System.out.println("amount: " + amount);
            System.out.println("reoccurring: " + reoccurring);
            System.out.println("occurring: " + occurring);
            Transaction t = Transaction.re_initTransaction(
                    date, sender, receiver, amount, reoccurring, occurring
            );
            transactions.add(t);
        }

//        if (transactionParse.length <= 1) {
//            return transactions;
//        }
        System.out.println("Returning transactions: " + transactions);
        return transactions;
    }

    public static Date parseDate(String dateString) {
        SimpleDateFormat ft = new SimpleDateFormat("EEE MMM dd hh:mm:ss zzz yyyy"); //"d m dd hh:mm:ss z yyyy"); //"a b d H:M:S Z Y");

        System.out.print("\"" + dateString + "\" Parses as ");
        Date t;
        try {
            t = ft.parse(dateString);
            System.out.println(t);
        } catch (ParseException e) {
            t = null;
            System.out.println("Unparseable using " + ft);
        }
        return t;
    }

    public static String getKey(Entity e) {
        for (String key : MainActivity.prefs.getAll().keySet()) {
            System.out.println("key: " + key + " vs. " + e);
            if (key.contains("entity_entry_")) {
                if (key.contains(e.getName())) {
                    System.out.println("returning key: " + key);
                    return key;
                }
            }
        }
        String userName = MainActivity.prefs.getString("user_name", "User");
        if (e.getName().equals(userName)) {
            return "entity_entry_User";
        }
        System.out.println("key for entity e: " + e + ", not found, returning null.");
        return null;
    }

    public static String getKey(String name) {
        if (name.contains("<<")) {
            // is a serialized entity string.
            String[] spl = name.split("<<");
            name = spl[1];
        }
        for (String key : MainActivity.prefs.getAll().keySet()) {
            System.out.println("key: " + key + " vs. " + name);
            if (key.contains("entity_entry_")) {
                if (key.contains(name)) {
                    System.out.println("returning key: " + key);
                    return key;
                }
            }
        }
        String userName = MainActivity.prefs.getString("user_name", "User");
        if (name.equals(userName)) {
            return "entity_entry_User";
        }
        System.out.println("key for name n: " + name + ", not found, returning null.");
        return null;
    }

    public static Entity getEntity(String name) {
        String key = getKey(name);
        return parseEntity(MainActivity.prefs.getString(key, null));
    }
}

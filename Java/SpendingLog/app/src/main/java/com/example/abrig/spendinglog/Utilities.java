package com.example.abrig.spendinglog;

import android.graphics.Color;
import android.text.Spannable;
import android.text.SpannableString;
import android.text.style.ForegroundColorSpan;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

public class Utilities {

    public static CharSequence[] possibleFilters = new CharSequence[] {
            "By Entity",
            "By Sender",
            "By Recipient",
            "By Transaction Type",
            "Start Date",
            "Current Date",
            "End Date",
            "By Amount Range"
    };

//    public static String dollarify(int transactionAmount) {
//        double m = transactionAmount / 100.0;
//        return "$ " + String.format("% .2f", m);
//    }

    // Inclusive
    public static boolean inRange(int start, int x, int end) {
        return start <= x && x <= end;
    }

    // Inclusive
    public static boolean inRange(double start, double x, double end) {
//        System.out.println(start + " <= " + x + " <= " + end + " -> " + (start <= x && x <= end));
        return start <= x && x <= end;
    }



    public static String keyify(int r, int c) {
        return "(" + r + ", " + c + ")";
    }

    public static String keyify(float r, float c) {
        return "(" + (int)r + ", " + (int)c + ")";
    }

    public static int[] unkeyify(String key) {
        String keys = key.replaceAll("\\(", "").replaceAll("\\)" , "").replaceAll(",", "");
        String[] splitString = keys.split(" ");
        return new int[] {Integer.parseInt(splitString[0]), Integer.parseInt(splitString[1])};
    }

    public static Spannable dollarify(int transactionAmount) {

        String moneyString = "$ " + twoDecimals(transactionAmount / 100.0);
        Spannable wordToSpan = new SpannableString(moneyString);
        if (transactionAmount < 0) {
            wordToSpan.setSpan(new ForegroundColorSpan(Color.RED), 0, wordToSpan.length(), Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);
        }
        return wordToSpan;
    }

    public static String twoDecimals(double d) {
        NumberFormat nf = NumberFormat.getInstance();
        nf.setMaximumFractionDigits(2);
        nf.setMinimumFractionDigits(2);
        return nf.format(d);
    }

    public static void createCSV(ArrayList<Transaction> transactions) {
        CSVWriter writer = new CSVWriter();
        ArrayList<String> header = new ArrayList<>(Arrays.asList("Date", "Sender", "Receiver", "Amount", "Purpose"));
        writer.writeFile(header, transactions);
    }

    public static boolean checkInt(String n) {
        try {
            int i = Integer.parseInt(n.trim());
            return true;
        }
        catch (Exception e) {
            return false;
        }
    }
    public static boolean checkDec(String n) {
        try {
            double d = Double.parseDouble(n.trim());
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
        return res.trim();
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

        String name = entityParse[1].trim();
        String idString = entityParse[2].trim();
        int balance = Integer.parseInt(entityParse[3].trim());
        int moneySent = Integer.parseInt(entityParse[4].trim());
        int moneyReceived = Integer.parseInt(entityParse[5].trim());
        boolean overdraft = Boolean.parseBoolean(entityParse[6].trim());
        Entity e = Entity.re_initEntity(name, idString, balance, moneySent, moneyReceived, overdraft);
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

        System.out.println("entityParse: " + Arrays.toString(entityParse));
        System.out.println("transactionParse: " + Arrays.toString(transactionParse));

        for (int i = 1; i < transactionParse.length; i += 7) {
            Date date = parseDate(transactionParse[i].trim());
            // date is null only if entities are not found in the transaction.
            // then just skip the transactions
            if (date == null) {
                continue;
            }
            Entity sender = getEntity(transactionParse[i + 1].trim());
            Entity receiver = getEntity(transactionParse[i + 2].trim());
            int amount = Integer.parseInt(transactionParse[i + 3].trim());
            TransactionType transactionType = getTransactionType(transactionParse[i + 4].trim());
            boolean reoccurring = Boolean.parseBoolean(transactionParse[i + 5].trim());
            String occurring = "NA";
            if (reoccurring) {
                occurring = transactionParse[i + 6].trim();
            }
            else {
                i -= 1;
            }

            System.out.println("date: " + date);
            System.out.println("sender: " + sender);
            System.out.println("receiver: " + receiver);
            System.out.println("amount: " + amount);
            System.out.println("transactionType: " + transactionType);
            System.out.println("reoccurring: " + reoccurring);
            System.out.println("occurring: " + occurring);
            Transaction t = Transaction.re_initTransaction(
                    date, sender, receiver, amount, reoccurring, occurring, transactionType
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
            String k = key.toUpperCase();
            String n = e.getName().toUpperCase();
            if (k.contains("ENTITY_ENTRY_")) {
                if (k.contains(n)) {
                    System.out.println("returning key: " + key);
                    return key;
                }
            }
        }
        String userName = MainActivity.prefs.getString("user_name", "User");
        String oldName = MainActivity.prefs.getString("user_old_name", "User");
        if (e.getName().equals(userName) || e.getName().equals(oldName)) {
            System.out.println("returning user key");
            return "entity_entry_User";
        }
        System.out.println("key for entity e: " + e + ", not found, returning null.");
        return null;
    }

    public static String getKey(String name) {
        String userName = MainActivity.prefs.getString("user_name", "User");
        String oldName = MainActivity.prefs.getString("user_old_name", "User");
        System.out.println("Comparing {" + name + "} to userName {" + userName + "}");
        if (name.contains("<<")) {
            // is a serialized entity string.
            String[] spl = name.split("<<");
            name = spl[1];
        }
        name = name.trim();
        for (String key : MainActivity.prefs.getAll().keySet()) {
            System.out.println("key: " + key + " vs. " + name);
            String k = key.toUpperCase();
            String n = name.toUpperCase();
            if (k.contains("ENTITY_ENTRY_")) {
                if (k.contains(n)) {
                    System.out.println("returning key: " + key);
                    return key;
                }
            }
        }
        if (name.equals(userName) || name.equals(oldName)) {
            System.out.println("returning user key");
            return "entity_entry_User";
        }
        System.out.println("key for name n: " + name + ", not found, returning null.");
        return null;
    }

    public static Entity getEntity(String name) {
        String key = getKey(name);
        return parseEntity(MainActivity.prefs.getString(key, null));
    }

    public static TransactionType getTransactionType(String transactionTypeIn) {
        ArrayList<TransactionType> transactionTypes = TransactionType.getTypes();
        for (TransactionType t : transactionTypes) {
            if (t.getName().equals(transactionTypeIn)) {
                return t;
            }
        }
        return null;
    }
}

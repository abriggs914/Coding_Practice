/*package whatever //do not write package name here */

import java.io.*;
import java.util.Date;
import java.util.Arrays;
import java.util.ArrayList;
import java.math.BigDecimal;
import java.math.BigInteger;

class GFG {
	public static void main (String[] args) {
// 		System.out.println("GfG!" + dollarify(1222));
// 		String moneyString = "$ 4.99";
	
//         // String[] dollarSplit = moneyString.split("/d");
//         // System.out.println(Arrays.toString(dollarSplit));
//         String a = "20";
//         String b = "20.0";
//         String c = "20.00";
//         String d = "2000";
//         // String e = "20";
//         System.out.println("A:" + a + " -> " + parseMoney(a));
//         System.out.println("B:" + b + " -> " + parseMoney(b));
//         System.out.println("C:" + c + " -> " + parseMoney(c));
//         System.out.println("D:" + d + " -> " + parseMoney(d));
        
//         ArrayList<String> arr = new ArrayList<>();
//         arr.add("hello");
//         arr.add("there");
//         arr.add("general");
//         arr.add("kenobi");
//         System.out.println("arr: " + arr);
//         arr.remove("this one");
//         System.out.println("arr: " + arr);

        // String key = "entity_entry_Rent";
        // String name = "Rent "; 
        // System.out.println("key.contains(name): " + key.contains(name));
        
        // if (key.contains("entity_entry_")) {
        //     if (key.contains(name)) {
        //         System.out.println("returning key: " + key);
        //         // return key;
        //     }
        // }
        // double a = 12.0;
        // double b = 23.99;
        // double c = 24;
        // String timeA = parseTime(a, false);
        // String timeB = parseTime(b, false);
        // String timeC = parseTime(c, false);
        // System.out.println("parsing a {" + a + "}: " + timeA);
        // System.out.println("parsing a {" + b + "}: " + timeB);
        // System.out.println("parsing a {" + c + "}: " + timeC);
        
        // System.out.println("Add one to {" + timeA + "}: " + parseTime(getTimeValue(timeA, true, true), true));
        // System.out.println("Subtract one from {" + timeA + "}: " + parseTime(getTimeValue(timeA, true, false), true));
        
        // System.out.println("Add one to {" + timeB + "}: " + parseTime(getTimeValue(timeB, true, true), true));
        // System.out.println("Subtract one from {" + timeB + "}: " + parseTime(getTimeValue(timeB, true, false), true));
        
        // System.out.println("Add one to {" + timeC + "}: " + parseTime(getTimeValue(timeC, true, true), true));
        // System.out.println("Subtract one from {" + timeC + "}: " + parseTime(getTimeValue(timeC, true, false), true));
        
        // Date date1 = new Date();
        // Date date2 = new Date();
        // System.out.println("sameDay (" + date1 + ", " + date2 + "): " + sameDay(date1, date2));
        // System.out.println("sameTime (" + date1 + ", " + date2 + "): " + sameTime(date1, date2, 0.5, true));
        
        double x = 0.2646;
        String s = String.format("%f.02", x);
        System.out.println("s: " + s);
		
		
// 		System.out.println("GfG!" + dollarify(1222));
// 		String moneyString = "$ 4.99";
	
//         // String[] dollarSplit = moneyString.split("/d");
//         // System.out.println(Arrays.toString(dollarSplit));
//         String a = "20";
//         String b = "20.0";
//         String c = "20.00";
//         String d = "2000";
//         // String e = "20";
//         System.out.println("A:" + a + " -> " + parseMoney(a));
//         System.out.println("B:" + b + " -> " + parseMoney(b));
//         System.out.println("C:" + c + " -> " + parseMoney(c));
//         System.out.println("D:" + d + " -> " + parseMoney(d));
        
//         ArrayList<String> arr = new ArrayList<>();
//         arr.add("hello");
//         arr.add("there");
//         arr.add("general");
//         arr.add("kenobi");
//         System.out.println("arr: " + arr);
//         arr.remove("this one");
//         System.out.println("arr: " + arr);

        // String key = "entity_entry_Rent";
        // String name = "Rent "; 
        // System.out.println("key.contains(name): " + key.contains(name));
        
        // if (key.contains("entity_entry_")) {
        //     if (key.contains(name)) {
        //         System.out.println("returning key: " + key);
        //         // return key;
        //     }
        // }
        // Date d = new Date();
        
        // Random rand = new Random();
        // double a = rand.nextDouble();
        // double b = rand.nextDouble();
        int a = 54281;
        int b = 181;
        String valA = parseTime(a);
        String valB = parseTime(b);
        System.out.println("String a: " + valA);
        System.out.println("String b: " + valB);
        System.out.println("a: " + a + ", int a: " + parseTime(valA));
        System.out.println("b: " + b + ", int b: " + parseTime(valB));
        
        // String a = "[[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]]";
        // String[][] x = arrify(a);
        // System.out.println("\n\n\nRES\n\n");
        // for (String[] arr : x) {
        //     System.out.println(Arrays.toString(arr));
        // }
        
        // System.out.println(85000 >> 4);
        
        // int i = 7;
        // int j = 8;
        // System.out.println((i+0.0) / (j+0.0));
        
        // String s = "1, 1, 20, 100, 18, [[80, 80, 80, 80, 80][80, 0, 80, 0, 80][80, 80, 80, 0, 80][0, 0, 80, 0, 80][0, 0, 80, 0, 0][80, 80, 80, 0, 0]][[77, 77, 77, 77, 77][77, 8, 77, 7, 77][77, 77, 77, 6, 77][2, 5, 77, 5, 77][2, 5, 77, 4, 1][77, 77, 77, 2, 0]]";
        // getGameFromString(s);
        
        // HashMap<String, HashMap<String, String>> a = new HashMap<>();
        // HashMap<String, String> a1 = new HashMap<>();
        // a1.put("current_value", "0");
        // a1.put("check_status", "false");
        // a.put("(1, 1)", a1);
        
        // HashMap<String, String> b1 = new HashMap<>();
        // b1.put("current_value", "1");
        // b1.put("check_status", "true");
        // a.put("(0, 1)", b1);
        // // a.put("second addition", new HashMap<>());
        // // a.put("third addition", new HashMap<>());
        // // a.put("fourth addition", new HashMap<>());
        // HashMap<String, HashMap<String, String>> b = new HashMap<>(a);
        // System.out.println("a: " + a);
        // System.out.println("b: " + b);
        // System.out.println();
        
        // HashMap<String, HashMap<String, String>> c = mapify(a.toString());
        // System.out.println("c: " + c);
        // System.out.println();
        
        // int a = 49;
        // int b = -4;
        // String s = keyify(a, b);
        // int[] i = unkeyify(s);
        // System.out.println("a: " + a + ", b: " + b + ", s: " + s + ", i: " + Arrays.toString(i));
        
        // String stringVal = "{(2, 1)={checked_status=true, check_status=true, current_value=1}, (2, 3)={checked_status=false, check_status=true, current_value=0}, (2, 5)={checked_status=true, check_status=true, current_value=1}, (4, 2)={checked_status=false, check_status=true, current_value=0}, (4, 4)={checked_status=true, check_status=true, current_value=2}, (0, 2)={checked_status=true, current_value=77}, (4, 0)={checked_status=true, check_status=true, current_value=1}, (0, 4)={checked_status=false, check_status=true, current_value=0}, (0, 0)={checked_status=true, current_value=1}, (3, 4)={checked_status=true, check_status=true, current_value=2}, (3, 2)={checked_status=false, check_status=true, current_value=0}, (5, 5)={checked_status=true, current_value=1}, (5, 3)={checked_status=false, check_status=true, current_value=0}, (5, 1)={checked_status=true, check_status=true, current_value=1}, (1, 5)={checked_status=false, check_status=true, current_value=0}, (1, 3)={checked_status=true, check_status=true, current_value=1}, (1, 1)={checked_status=true, check_status=true, current_value=2}, (3, 0)={checked_status=false, check_status=true, current_value=0}, (2, 0)={checked_status=true, check_status=true, current_value=1}, (2, 2)={checked_status=false, check_status=true, current_value=0}, (2, 4)={checked_status=true, check_status=true, current_value=1}, (4, 3)={checked_status=false, check_status=true, current_value=0}, (4, 5)={checked_status=true, current_value=77}, (0, 3)={checked_status=true, check_status=true, current_value=1}, (0, 5)={checked_status=false, check_status=true, current_value=0}, (4, 1)={checked_status=true, check_status=true, current_value=1}, (0, 1)={checked_status=true, current_value=2}, (3, 3)={checked_status=false, check_status=true, current_value=0}, (3, 1)={checked_status=false, check_status=true, current_value=0}, (3, 5)={checked_status=true, check_status=true, current_value=P}, (5, 4)={checked_status=true, check_status=true, current_value=1}, (5, 2)={checked_status=false, check_status=true, current_value=0}, (1, 4)={checked_status=false, check_status=true, current_value=0}, (5, 0)={checked_status=true, current_value=77}, (1, 2)={checked_status=true, check_status=true, current_value=1}, (1, 0)={checked_status=true, current_value=77}}}";
        // System.out.println("map: " + mapify(stringVal));
    }
    

    public static boolean sameTime(Date a, Date b, double window, boolean isHours) {
        String aString = a.toString();
        String bString = b.toString();
        // "EEE MMM dd hh:mm:ss zzz yyyy"
        double upWindow = window * 1; // (0 <= x <= 1)
        double downWindow = -1 * (window * 1); // (-1 <= x <= 0)
        String[] aSpaceSplit = aString.split(" ");
        String[] bSpaceSplit = bString.split(" ");
        String[] aTimeSplit = aSpaceSplit[3].split(":");
        String[] bTimeSplit = bSpaceSplit[3].split(":");
        double aHour = Double.parseDouble(aTimeSplit[0]);
        double aMinute = Double.parseDouble(aTimeSplit[1]);
        double bHour = Double.parseDouble(bTimeSplit[0]);
        double bMinute = Double.parseDouble(bTimeSplit[1]);
        System.out.print( "Bupwindow: " + upWindow + 
                            "\nBdownWindow: " + downWindow);
        
        boolean bool = false; // clean up
        if (isHours) {
            upWindow += aHour;
            downWindow += aHour;
            if (downWindow <= bHour && bHour <= upWindow) {
                bool = true;
            }
        }
        else {
            upWindow += aMinute;
            downWindow += aMinute;
            if (downWindow <= bMinute && bMinute <= upWindow) {
                bool = true;
            }
        }
        System.out.println( "\nAupwindow: " + upWindow +
                            "\nAdownWindow: " + downWindow +
                            "\naString: " + aString + 
                            "\nbString: " + bString + 
                            "\naSpaceSplit: " + Arrays.toString(aSpaceSplit) +
                            "\nbSpaceSplit: " + Arrays.toString(bSpaceSplit) +
                            "\naTimeSplit: " + Arrays.toString(aTimeSplit) +
                            "\nbTimeSplit: " + Arrays.toString(bTimeSplit) +
                            "\naHour: " + aHour +
                            "\naMinute: " + aMinute +
                            "\nbHour: " + bHour +
                            "\nbMinute: " + bMinute +
                            "\nbool: " + bool +
                            "\ndateA: " + a + 
                            "\ndateB: " + b +
                            "\nwindow: " + window +
                            "\nisHours: " + isHours);
        return bool;
    }

    public static boolean sameDay(Date a, Date b) {
        long aTime = a.getTime();
        long bTime = b.getTime();
        long diff;
        if (a.before(b)) {
            diff = bTime - aTime;
            System.out.println("IF comparing: " + a.toInstant().compareTo(b.toInstant()));
        }
        else {
            diff = aTime - bTime;
            System.out.println("ELSE comparing: " + a.toInstant().compareTo(b.toInstant()));
        }
        System.out.println("aTime: " + aTime + ", bTime: " + bTime + ", diff: " + diff);
        return diff < 86400000;
    }
    

    public static String parseTime(double value, boolean exact) {
        String res = "";
        boolean am = false;
        int valueInt = (int) value;
        int off = 0;
        if (value < 12 || valueInt == 24) {
            am = true;
        }
        else {
            valueInt -= 12;
            off = 12;
        }
        if (valueInt == 24 || valueInt == 0) {
            res += "12";
        }
        else {
            res += String.format("%02d", valueInt);
        }
        double minutes = (Math.round((value - (valueInt + off)) * 100)) / 100.0;
//        System.out.println("Math.round(value - (valueInt + off): " + (value - (valueInt + off)));
//        System.out.println("((value - (valueInt + off)) * 100): " + ((value - (valueInt + off)) * 100));
//        System.out.println("(Math.round((value - (valueInt + off)) * 100)): " + (Math.round((value - (valueInt + off)) * 100)));
//        System.out.println("(Math.round((value - (valueInt + off)) * 100)) / 100.0: " + (Math.round((value - (valueInt + off)) * 100)) / 100.0);
        int minutesInt = (int) ((exact)? Math.round(100 * minutes) : Math.round(60 * minutes));
        res += ":" + String.format("%02d", minutesInt);
        res += ((am)? " AM" : " PM");
        System.out.println("PARSE TIME res: " + res + ", exact: " + exact + ", am: " + am + ", value: " + value + ", valueInt: " + valueInt + ", off: " + off + ", minutes: " + minutes + ", minutesInt: " + minutesInt);
        return res;
    }
    
    public static double getTimeValue(String timeText, boolean doIncrement, boolean increment) {
        String[] colonSplit = timeText.split(":");
        int hours = Integer.parseInt(colonSplit[0]);
        int minutes = Integer.parseInt(colonSplit[1].substring(0, 2));
        String am_pm = colonSplit[1].split(" ")[1];
        boolean increase = doIncrement && increment;
        boolean decrease = doIncrement && !increment;
        
        if (am_pm.equals("PM")) {
            if (hours != 12) {
                hours += 12;
            }
        }
        else if (am_pm.equals("AM") && hours == 12) {
            hours -= 12;
        }
        
        if (increase) {
            minutes += 1;
        }
        else if (decrease) {
            minutes -= 1;
        }
        
        if (minutes < 0) {
            System.out.print("\nmins < 0");
            if (increase) {
                System.out.println(", increase (impossible..?)");
                // impossible..?
            }
            else if (decrease) {
                System.out.println(", decrease");
                minutes = 59;
                if (hours == 12) {
                    am_pm = "AM";
                }
                else if (hours == 0) {
                    hours = 24;
                    am_pm = "PM";
                }
                hours -= 1;
            }
            else {
                System.out.println(", else");
            }
        }
        else if (minutes >= 60) {
            System.out.print("\nmins >= 0");
            if (increase) {
                System.out.println(", increase");
                minutes = 0;
                if (hours == 11 ) {
                    if (am_pm.equals("AM")) {
                        am_pm = "PM";
                    }
                    else {
                        am_pm = "AM";
                    }
                }
                else if (hours == 23) {
                    // hours = 11;
                    am_pm = "AM";
                }
                hours += 1;
            }
            else if (decrease) {
                System.out.println(", decrease (impossible..?)");
                // impossible..?
            }
            else {
                System.out.println(", else");
            }
        }
        else {
            System.out.println("\ndefault");
        }
        
        double hoursMins = ((hours * 100) + minutes) / 100.0;
        System.out.println("TIMEVALUE colonSplit: " + Arrays.toString(colonSplit) + ", hours: " + hours + ", minutes: " + minutes + ", am_pm: " + am_pm + ", hoursMins: " + hoursMins + ", doIncrement: " + doIncrement + ", increment: " + increment);
        return hoursMins;
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

    public static String dollarify(int transactionAmount) {
        double m = transactionAmount / 100.0;
        return "$" + String.format("%2.2f", m);
    }
    
    public static int parseMoney(String moneyString) {
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
    
    public static String keyify(int r, int c) {
        return "(" + r + ", " + c + ")";
    }
    
    
    public static int parseTime(String timeString) {
        String[] colonSplit = timeString.split(":");
        int mins = Integer.parseInt(colonSplit[0]);
        int seconds = Integer.parseInt(colonSplit[1]);
        return (mins * 60) + seconds;
    }
    

    public static int[] unkeyify(String key) {
        String keys = key.replaceAll("\\(", "").replaceAll("\\)" , "").replaceAll(",", "");
        String[] splitString = keys.split(" ");
        return new int[] {Integer.parseInt(splitString[0]), Integer.parseInt(splitString[1])};
    }

     public static HashMap<String,HashMap<String,String>> mapify(String stringVal) {
        HashMap<String,HashMap<String, String>> res = new HashMap<>();
        String[] split = stringVal.split("\\(");
//        System.out.println("split: " + Arrays.toString(split));
        for (String s : split) {
            if (s.length() > 1) {
                s.replaceAll("\\{", "");
                s.replaceAll("\\}", "");
                s.trim();
                System.out.println("\ts: <" + s + ">");
                String[] spaceSplit = s.split(" ");
                String rowString = spaceSplit[0].replaceAll(",", "").trim();
                String colString = spaceSplit[1].trim();
                String cols = colString.split("\\)")[0].replaceAll(",", "").trim();
                int r = Integer.parseInt(rowString);
                int c = Integer.parseInt(cols);
                String key = keyify(r, c);
                
                String statusString = "check_status=";
                String valueString = "current_value=";
                int statusIdx = s.indexOf(statusString);
                int valueIdx = s.indexOf(valueString);
                String equalsSplit1 = s.substring(statusIdx + statusString.length());
                String equalsSplit2 = s.substring(valueIdx + valueString.length());
                if (statusIdx < 0) {
                    equalsSplit1 = "false";
                }
                        
                equalsSplit1 = equalsSplit1.split(" ")[0]
                        .replaceAll(",", "")
                        .replaceAll("\\{", "")
                        .replaceAll("\\}", "")
                        .trim();
                equalsSplit2 = equalsSplit2.split(" ")[0]
                        .replaceAll(",", "")
                        .replaceAll("\\{", "")
                        .replaceAll("\\}", "")
                        .trim();

                System.out.println("\trowString: " + rowString + "\n\tcols: " + cols + "\n\tspaceSplit[1]: " + spaceSplit[1] + "\n\tspaceSplit[2]: " + spaceSplit[2] + "\n\tequalsSplit1: " + equalsSplit1 + "\n\tequalsSplit2: " + equalsSplit2 + "\n\tspaceSplit: " + Arrays.toString(spaceSplit));
                HashMap<String, String> keyVal = new HashMap<>();
                keyVal.put("current_value", equalsSplit2);
                keyVal.put("check_status", equalsSplit1);
                res.put(key, keyVal);
            }
        }
        return res;
    }
    
    public static void getGameFromString(String gameString) {
        // TODO:
        System.out.println("gameString: " + gameString);
        String[] gridSplit = gameString.split("\\[\\[");
        String[] statsSplit = gridSplit[0].split(",");
        System.out.println("gridSplit: " + Arrays.toString(gridSplit));
        System.out.println("statsSplit: " + Arrays.toString(statsSplit));
        int gameNum = Integer.parseInt(statsSplit[0].trim());
        boolean win = Integer.parseInt(statsSplit[1].trim()) != 0;
        int time = Integer.parseInt(statsSplit[2].trim());
        int score = Integer.parseInt(statsSplit[3].trim());
        int searched = Integer.parseInt(statsSplit[4].trim());
        String[][] grid = arrify("[[" + gridSplit[1].trim());
        String[][] gridSoln = arrify("[[" + gridSplit[2].trim());
    }
    
    public static String[][] arrify(String s) {
        // System.out.println("in: " + s);
        String[] leftSplit = s.split("]\\[");
//        System.out.println("leftSplit: " + Arrays.toString(leftSplit));
        ArrayList<ArrayList<String>> list = new ArrayList<>();
        for (String possibleRow : leftSplit) {
            String[] commaSplit = possibleRow.split(",");
            ArrayList<String> rowList = new ArrayList<>();
            for (int i = 0; i < commaSplit.length; i++) {
                String entry = String.valueOf(commaSplit[i]);
//                System.out.print("\tbefore: {" + entry);
                entry = entry.replaceAll("\\[", "");
                entry = entry.replaceAll("]", "");
                entry = entry.trim();
                rowList.add(entry);
//                System.out.println("}\tafter: {" + entry + "}");
            }
//            System.out.println("rowList: " + rowList);
            list.add(rowList);
        }
        int x = 1, y = 1;
        if (list.size() > 0) {
            y = list.get(0).size();
            x = list.size();
        }
        String[][] res = new String[x][y];
        for (int r = 0; r < x; r++) {
            ArrayList<String> row = list.get(r);
            System.out.println("\t\trow ("+row.size()+"): " + row);
            for (int c = 0; c < y; c++) {
                res[r][c] = row.get(c);
            }
        }
        return res;
    }

    public static String parseTime(int secondsPast) {
        String res = "";
        int mins = -1, seconds = 0;
        for (int x = secondsPast; x >= 0; x -= 60) {
            mins += 1;
            seconds = x;
            if (mins >= 60) {
                mins = 59;
                seconds = 59;
                break;
            }
//            System.out.println("x: " + x + ", mins: " + mins + ", seconds: " + seconds);
        }
        if (mins < 0) {
            mins = 0;
        }
        res = mins + "";
        String secondsString = seconds + "";
        if (res.length() != 2) {
            res = "0" + res;
        }
        res += ":";
        if (secondsString.length() != 2) {
            secondsString = "0" + secondsString;
        }
        res += secondsString;
        return res;
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

    public static String dollarify(int transactionAmount) {
        double m = transactionAmount / 100.0;
        return "$" + String.format("%2.2f", m);
    }
    
    public static int parseMoney(String moneyString) {
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
}
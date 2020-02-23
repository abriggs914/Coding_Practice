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
}
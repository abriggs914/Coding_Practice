package sample;

import java.text.NumberFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

public class Utilities {

    public static final long NUM_MILLIS_PER_DAY = 86400000;

    public static String twoDecimals(double d) {
        NumberFormat nf = NumberFormat.getInstance();
        nf.setMaximumFractionDigits(2);
        nf.setMinimumFractionDigits(2);
        return nf.format(d);
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
        int minutesInt = (int) ((exact)? Math.round(100 * minutes) : Math.round(60 * minutes));
        res += ":" + String.format("%02d", minutesInt);
        res += ((am)? " AM" : " PM");
//        System.out.println("PARSE TIME res: " + res + ", exact: " + exact + ", am: " + am + ", value: " + value + ", valueInt: " + valueInt + ", off: " + off + ", minutes: " + minutes + ", minutesInt: " + minutesInt);
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
//            System.out.print("\nmins < 0");
            if (decrease) {
//                System.out.println(", decrease");
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
        }
        else if (minutes >= 60) {
//            System.out.print("\nmins >= 0");
            if (increase) {
//                System.out.println(", increase");
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
        }

        double hoursMins = ((hours * 100) + minutes) / 100.0;
//        System.out.println("TIMEVALUE colonSplit: " + Arrays.toString(colonSplit) + ", hours: " + hours + ", minutes: " + minutes + ", am_pm: " + am_pm + ", hoursMins: " + hoursMins + ", doIncrement: " + doIncrement + ", increment: " + increment);
        return hoursMins;
    }

    public static String addOneMinute(String timeText) {
//        System.out.println("timeIn: " + timeText);
        double hoursMins = getTimeValue(timeText, true, true);
        return parseTime(hoursMins, true);
    }

    public static String subtractOneMinute(String timeText) {
//        System.out.println("timeIn: " + timeText);
        double hoursMins = getTimeValue(timeText, true, false);
        return parseTime(hoursMins, true);
    }

    public static double getTimeSliderValue(String newTime) {
        double timeValue = getTimeValue(newTime, false, true);
        int num = (int) timeValue * 100;
        int fractional = ((int) (timeValue * 100)) - num;
        int intValue = (int) ((fractional / 60.0) * 100);
        double resValue = (num + intValue) / 100.0;
//        System.out.println( "\tnewTime: " + newTime +
//                            "\n\ttimeValue: " + timeValue +
//                            "\n\tnum: " + num +
//                            "\n\tfractional: " + fractional +
//                            "\n\tintValue: " + intValue +
//                            "\n\tresValue: " + resValue);
        return resValue;
    }

    public static boolean sameDay(Date a, Date b) {
        long aTime = a.getTime();
        long bTime = b.getTime();
        long diff;
        if (a.before(b)) {
            diff = bTime - aTime;
//            System.out.println("IF comparing: " + a.toInstant().compareTo(b.toInstant()));
        }
        else {
            diff = aTime - bTime;
//            System.out.println("ELSE comparing: " + a.toInstant().compareTo(b.toInstant()));
        }
//        System.out.println("aTime: " + aTime + ", bTime: " + bTime + ", diff: " + diff);
        boolean lessThanOneDay = diff < NUM_MILLIS_PER_DAY;
        String aString = a.toString();
        String bString = b.toString();
        String[] aSplit = aString.split(" ");
        String[] bSplit = bString.split(" ");
        int aDate = Integer.parseInt(aSplit[2]);
        int bDate = Integer.parseInt(bSplit[2]);
//        System.out.println("aSplit: " + Arrays.toString(aSplit) +
//                "\nbSplit: " + Arrays.toString(bSplit) +
//                "\naDate: " + aDate +
//                "\nbDate: " + bDate);
        return lessThanOneDay && aDate == bDate;
    }

    public static String getTimeFromDate(Date d) {
        return d.toString().split(" ")[3];
    }

    public static boolean sameTime(Date a, Date b, double window) {
        //, boolean isHours) {
//        String aString = a.toString();
//        String bString = b.toString();
//        // "EEE MMM dd hh:mm:ss zzz yyyy"
////        double mult = ((isHours)? 60 : 1);
//        double upWindow = window * 1; // (0 <= x <= 1)
//        double downWindow = -1 * (window * 1); // (-1 <= x <= 0)
//        String[] aSpaceSplit = aString.split(" ");
//        String[] bSpaceSplit = bString.split(" ");
//        String[] aTimeSplit = aSpaceSplit[3].split(":");
//        String[] bTimeSplit = bSpaceSplit[3].split(":");
//        double aHour = Double.parseDouble(aTimeSplit[0]);
//        double aMinute = Double.parseDouble(aTimeSplit[1]);
//        double bHour = Double.parseDouble(bTimeSplit[0]);
//        double bMinute = Double.parseDouble(bTimeSplit[1]);
//        System.out.print( "\nBupwindow: " + upWindow + "\nBdownWindow: " + downWindow);
//
//        boolean bool = false;
//        upWindow += (aMinute / 100.0);
//        downWindow += (aMinute / 100.0);
//        boolean upWindowFractional = (upWindow - (int)upWindow)  >= 0.6;
//        boolean upWindowLessThanOne = upWindow < 1 && upWindow >= 0.6;
//        boolean downWindowFractional = (downWindow - (int)downWindow)  >= 0.6;
//        boolean downWindowLessThanOne = Math.abs(downWindow) < 1 && Math.abs(downWindow) >= 0.6;
//        if (upWindowFractional || upWindowLessThanOne) {
//            System.out.print("\n\tupFractional: " + upWindowFractional + ", upLessThan1: " + upWindowLessThanOne + ", upwindow: (" + upWindow + " -> (");
//            upWindow = (upWindow + 1) - ((upWindowLessThanOne)? 0.6 : 0); //(0.6 * ((upWindow - (int)upWindow) * 100));
//            System.out.print(upWindow + ")");
//        }
//        if (downWindowFractional || downWindowLessThanOne) {
//            System.out.print("\n\tdownFractional: " + downWindowFractional + ", downLessThan1: " + downWindowLessThanOne + ", downwindow: (" + downWindow + " -> (");
//            downWindow = (downWindow - 1) + ((downWindowLessThanOne)? 0.6 : 0); //(0.6 * ((downWindow - (int)downWindow) * 100));
//            System.out.print(downWindow + ")");
//        }
////        if (isHours) {
//        upWindow += aHour;
//        downWindow += aHour;
//
//        System.out.print( "\nDupwindow: " + upWindow + "\nDdownWindow: " + downWindow);
//
////        }
//        if (upWindow >= 24) {
//            System.out.print("\n\tupWindow(" + upWindow + ") -> (");
//            upWindow -= 24;
//            System.out.print(upWindow + ")");
//        }
//        boolean downWindowExact = true;
//        if (downWindow < 0) {
//            System.out.print("\n\tdownWindow(" + downWindow + ") -> (");
////            downWindowExact = false;
//            downWindow += 23.6;
//            System.out.print(downWindow + ")");
//        }
//        if ((downWindow - (int)downWindow) >= 0.6) {
//            downWindow = getTimeValue(parseTime(downWindow, false), false, false);
//        }
//
//        double bHourMinute = ((100 * bHour) + bMinute) / 100.0;
//        String bTimeString = parseTime(bHourMinute, true);
////        String upWindowString = parseTime(upWindow, true);
////        String downWindowString = parseTime(downWindow, true);
//        double bValue = getTimeSliderValue(bTimeString);
////        double upWindowValue = getTimeSliderValue(upWindowString);
////        double downWindowValue = getTimeSliderValue(downWindowString);
////        String upWindowString2 = parseTime(upWindowValue, false);
////        String downWindowString2 = parseTime(downWindowValue, false);
//        double upWindowValue = upWindow;
//        double downWindowValue = downWindow;
//        String upWindowString2 = parseTime(upWindowValue, true);
//        String downWindowString2 = parseTime(downWindowValue, downWindowExact);
//
//        if (downWindowValue <= bValue && bValue <= upWindowValue) {
//            bool = true;
//        }
//
//        System.out.println(
//                "\nAupwindow: " + upWindow +
//                "\nAdownWindow: " + downWindow +
//                "\naString: " + aString +
//                "\nbString: " + bString +
////                "\naSpaceSplit: " + Arrays.toString(aSpaceSplit) +
////                "\nbSpaceSplit: " + Arrays.toString(bSpaceSplit) +
////                "\naTimeSplit: " + Arrays.toString(aTimeSplit) +
////                "\nbTimeSplit: " + Arrays.toString(bTimeSplit) +
//                "\naHour: " + aHour +
//                "\taMinute: " + aMinute +
//                "\nbHour: " + bHour +
//                "\tbMinute: " + bMinute +
////                "\nupWindowString: " + upWindowString +
////                "\ndownWindowString: " + downWindowString +
//                "\nupWindowString2: " + upWindowString2 +
//                "\ndownWindowString2: " + downWindowString2 +
//                "\nbValue: " + bValue +
//                "\nupWindowValue: " + upWindowValue +
//                "\ndownWindowValue: " + downWindowValue +
////                "\ndateA: " + a +
////                "\ndateB: " + b +
//                "\nwindow: " + window +
////                "\nisHours: " + isHours +
//                "\nbool: " + bool);
////        return bool;

        int minutes = (int) (window * 100);
        double selectedBound, upperBound = 0.0, lowerBound = 0.0;
        String selectedTime = getTimeString(a);
        String dateInString = getTimeString(b);
        selectedBound = getTimeValue(dateInString, false, false);
        String upperBoundString = String.copyValueOf(selectedTime.toCharArray());
        String lowerBoundString = String.copyValueOf(selectedTime.toCharArray());
        for (int i = 0; i < minutes; i++) {
            upperBound = getTimeValue(upperBoundString, true, true);
            upperBoundString = parseTime(upperBound, true);
        }
        for (int i = 0; i < minutes; i++) {
            lowerBound = getTimeValue(lowerBoundString, true, false);
            lowerBoundString = parseTime(lowerBound, true);
        }
        boolean res = lowerBound <= selectedBound && selectedBound <= upperBound;
//        System.out.println(
//                "selectedTime: " + selectedTime +
//                "\ndate in question: " + dateInString +
//                "\nvalue: " + selectedBound +
//                "\nlowerBoundString: " + lowerBoundString +
//                "\nupperBoundString: " + upperBoundString +
//                "\n(" + lowerBound + " <= X <= + " + upperBound + ")\nres: " + res);
        return res;
    }

    public static String getTimeString(Date date) {
        String dateString = date.toString();
        String[] dateSpaceSplit = dateString.split(" ");
        String[] dateTimeSplit = dateSpaceSplit[3].split(":");
        int dateHour = Integer.parseInt(dateTimeSplit[0]);
        int dateMinute = Integer.parseInt(dateTimeSplit[1]);
        String am_pm = "AM";
        if (dateHour > 11) {
            if (dateHour != 12) {
                dateHour -= 12;
            }
            am_pm = "PM";
        }
        String timeText = String.format("%02d", dateHour) + ":" + String.format("%02d", dateMinute) + " " + am_pm;
//        System.out.println("Utilities.getTimeString, date: " + date + ", dateString: " + dateString + ", timeText: " + timeText);
        return timeText;
    }

    public static String getDateString(Date date) {
        String dateString = date.toString();
        String[] dateSplit = dateString.split(" ");
        return dateSplit[1] + " " + dateSplit[2] + ", " + dateSplit[5];
    }

    public static Date parseDate(String s) {
//        System.out.print(" date: " + s);
        SimpleDateFormat sdf = new SimpleDateFormat("EEE, MMM dd, yyyy hh:mm aa");//"EEE MMM dd hh:mm:ss zzz yyyy");
        Date date = null;
        try {
            date = sdf.parse(s);
        } catch (ParseException e) {
            e.printStackTrace();
        }
//        System.out.println("Utilities.parseDate - date parsed" + date);
        return date;
    }

    public static int min(int a, int b){
        return ((a <= b)? a : b);
    }

    public static int min(int x, int y, int z) {
        if (x <= y && x <= z) {
            return x;
        }
        if (y <= x && y <= z) {
            return y;
        }
        else {
            return z;
        }
    }

    public static int max(int a, int b){
        return ((a >= b)? a : b);
    }

    public static void show(int[][] arr){
        System.out.print("{");
        for(int i = 0; i < arr.length; i++){
            System.out.print("{");
            if(i > 0)
                System.out.print(" ");
            for(int j = 0; j < arr[i].length; j++){
                if(j < arr[i].length-1){
                    if(i == 0 || j == 0)
                        System.out.print((char)arr[i][j] + ", ");
                    else
                        System.out.print(arr[i][j] + ", ");
                }
                else{
                    if(i == 0 || j == 0)
                        System.out.print((char)arr[i][j]);
                    else
                        System.out.print(arr[i][j]);
                }
            }
            if(i < arr.length-1)
                System.out.println("},");
            else
                System.out.print("}");
        }
        System.out.println("}");
    }

    public static int computeMinEditDistance(String a, String b) {
        int lenA = a.length();
        int lenB = b.length();
        int x = max(lenA, lenB);
        String p = ((x == lenA)? a : b);
        String q = ((x == lenA)? b : a);
//        ArrayList<String> instructions =
        return minEditDistance(p, q);
    }

    public static int minEditDistance(String a, String b) {
        a = a.toUpperCase();
        b = b.toUpperCase();
        System.out.print("Minimum edit Distance to convert \"" + a + "\" to \"" + b + "\"\t->\t");
        int n = a.length() + 2;
        int m = b.length() + 2;
        int[][] table = new int[m][n];
        for(int i = 2; i < max(n, m); i++){
            if(i < n){
                table[0][i] = a.charAt(i - 2);
                table[1][i] = i - 1;
            }
            if(i < m){
                table[i][0] = b.charAt(i - 2);
                table[i][1] = i - 1;
            }
        }
        for(int i = 2; i < m; i++){
            for(int j = 2; j < n; j++){
                int x = table[i][j-1];
                int y = table[i-1][j-1];
                int z = table[i-1][j];
                int mini = min(x, min(y, z));
                int u = table[0][j];
                int v = table[i][0];
                if(u == v){
                    table[i][j] = table[i-1][j-1];
                }
                else{
                    // System.out.println("x: " + x + ", y: " + y + ", z: " + z + ", min(x, min(y, z): " + mini);
                    // able[i][j] = mini + 1;
                }
            }
        }
        int minimumDistance = table[table.length-1][table[table.length-1].length-1];
        System.out.println(minimumDistance);
        show(table);
        return minimumDistance;
    }

    public static int getMinEditDist(String a, String b) {
        return editDistDP(a, b, a.length(), b.length());
    }

    public static int editDistDP(String str1, String str2, int m, int n) {
        // Create a table to store results of subproblems
        int dp[][] = new int[m + 1][n + 1];

        // Fill d[][] in bottom up manner
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                // If first string is empty, only option is to
                // insert all characters of second string
                if (i == 0)
                    dp[i][j] = j; // Min. operations = j

                    // If second string is empty, only option is to
                    // remove all characters of second string
                else if (j == 0)
                    dp[i][j] = i; // Min. operations = i

                    // If last characters are same, ignore last char
                    // and recur for remaining string
                else if (str1.charAt(i - 1) == str2.charAt(j - 1))
                    dp[i][j] = dp[i - 1][j - 1];

                    // If the last character is different, consider all
                    // possibilities and find the minimum
                else
                    dp[i][j] = 1 + min(dp[i][j - 1], // Insert
                            dp[i - 1][j], // Remove
                            dp[i - 1][j - 1]); // Replace
            }
        }

        return dp[m][n];
    }

    public static int getYear(Date firstDate) {
        String dateString = firstDate.toString();
        String[] dateSplit = dateString.split(" ");
        return Integer.parseInt(dateSplit[5]);
    }

    public static int getMonth(Date firstDate) {
        SimpleDateFormat sdf = new SimpleDateFormat("MM");
        return Integer.parseInt(sdf.format(firstDate));
    }

    public static int getDay(Date firstDate) {
        String dateString = firstDate.toString();
        String[] dateSplit = dateString.split(" ");
        return Integer.parseInt(dateSplit[2]);
    }

    public static Date getFirstDate(ArrayList<Game> games) {
        Date firstDate = null;
        if (games.size() > 0) {
            firstDate = games.get(0).getDate();
        }
        for (int i = 0; i < games.size(); i++) {
            Game g = games.get(i);
            Date d = g.getDate();
            if (d.before(firstDate)) {
                firstDate = d;
            }
        }
        System.out.println("returning firstDate: " + firstDate);
        return firstDate;
    }

    public static Date getLastDate(ArrayList<Game> games) {
        Date lastDate = null;
        if (games.size() > 0) {
            lastDate = games.get(0).getDate();
        }
        for (int i = 0; i < games.size(); i++) {
            Game g = games.get(i);
            Date d = g.getDate();
            if (d.after(lastDate)) {
                lastDate = d;
            }
        }
        System.out.println("returning lastDate: " + lastDate);
        return lastDate;
    }
}

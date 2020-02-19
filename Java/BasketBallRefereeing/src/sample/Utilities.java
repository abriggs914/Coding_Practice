package sample;

import java.util.Arrays;

public class Utilities {

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
        if (doIncrement) {
            if (increment) {
                minutes += 1;
            }
            else {
                minutes -= 1;
            }
        }
        if (minutes >= 60) {
            hours += 1;
            minutes = 0;
            if (am_pm.equals("AM")) {
                if (hours == 12) {
                    am_pm = "PM";
                }
                else if (hours == 13) {
                    hours -= 12;
                }
            }
            else {
                if (hours == 12) {
                    hours -= 12;
                    am_pm = "AM";
                }
            }
            if (hours == 24) {
                hours = 0;
//                am_pm = "AM";
            }
        }
        ///////////////////////////////////////////////
        // backwards needs to be fixed
        else if (minutes < 0) {
            hours -= 1;
            minutes = 59;
            if (hours < 13 || hours == 24) {
                am_pm = "AM";
            }
            else {
//                hours = 0;
                am_pm = "PM";
            }
        }
        //////////////////////////////////////////////////
        if (hours == 12 && am_pm.equals("AM")) {
            hours -= 12;
        }
        if (am_pm.equals("PM")) {
            if (hours < 12) {
                hours += 12;
            }
        }
//        if (am_pm.equals("PM")) {
//            if (hours != 12){
//                hours += 12;
//            }
//        }
//        else {
//            if (hours == 13){
//                hours -= 12;
//            }
//        }
//        if (hours < 0) {
//            hours = 23;
//        }
//        if (hours >= 24) {
//            hours = 0;
//        }
        double hoursMins = ((hours * 100) + minutes) / 100.0;
        System.out.println("\nTIMEVALUE colonSplit: " + Arrays.toString(colonSplit) + ", hours: " + hours + ", minutes: " + minutes + ", am_pm: " + am_pm + ", hoursMins: " + hoursMins + ", doIncrement: " + doIncrement + ", increment: " + increment);
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
}

package sample;

import java.text.NumberFormat;
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
            System.out.println("IF comparing: " + a.toInstant().compareTo(b.toInstant()));
        }
        else {
            diff = aTime - bTime;
            System.out.println("ELSE comparing: " + a.toInstant().compareTo(b.toInstant()));
        }
        System.out.println("aTime: " + aTime + ", bTime: " + bTime + ", diff: " + diff);
        return diff < NUM_MILLIS_PER_DAY;
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
//        System.out.print( "Bupwindow: " + upWindow + "\nBdownWindow: " + downWindow);

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
//        System.out.println( "\nAupwindow: " + upWindow +
//                "\nAdownWindow: " + downWindow +
//                "\naString: " + aString +
//                "\nbString: " + bString +
//                "\naSpaceSplit: " + Arrays.toString(aSpaceSplit) +
//                "\nbSpaceSplit: " + Arrays.toString(bSpaceSplit) +
//                "\naTimeSplit: " + Arrays.toString(aTimeSplit) +
//                "\nbTimeSplit: " + Arrays.toString(bTimeSplit) +
//                "\naHour: " + aHour +
//                "\naMinute: " + aMinute +
//                "\nbHour: " + bHour +
//                "\nbMinute: " + bMinute +
//                "\nbool: " + bool +
//                "\ndateA: " + a +
//                "\ndateB: " + b +
//                "\nwindow: " + window +
//                "\nisHours: " + isHours);
        return bool;
    }

    public static String getTimeString(Date date) {
        String dateString = date.toString();
        String[] dateSpaceSplit = dateString.split(" ");
        String[] dateTimeSplit = dateSpaceSplit[3].split(":");
        int dateHour = Integer.parseInt(dateTimeSplit[0]);
        int dateMinute = Integer.parseInt(dateTimeSplit[1]);
        String am_pm = "AM";
        if (dateHour > 12) {
            dateHour -= 12;
            am_pm = "PM";
        }
        String timeText = String.format("%02d", dateHour) + ":" + String.format("%02d", dateMinute) + " " + am_pm;
        System.out.println("date: " + date + ", timeText: " + timeText);
        return timeText;
    }
}

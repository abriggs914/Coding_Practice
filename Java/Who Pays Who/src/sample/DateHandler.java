package sample;/*package whatever //do not write package name here */

import java.io.*;
import java.util.Random;
import java.util.Date;
import java.util.Calendar;
import java.text.SimpleDateFormat;
import java.text.ParseException;

class DateHandler {
	public static void main (String[] args) {
		System.out.println("");
		Date today = DateHandler.getToday();
		System.out.println("today: " + today);
		System.out.println("timeString: " + DateHandler.getTimeString(today));
		System.out.println("dateString: " + DateHandler.getDateString(today));
		Date now = new Date();
		System.out.println("parseDate: " + DateHandler.parseDate(now.toString()));
		String a = "03/08/2020";
		String b = "03/08/2020 12:35:15";
		System.out.println("createDate("+a+"): " + DateHandler.createDate(a));
		System.out.println("createDateAndTime("+b+"): " + DateHandler.createDateAndTime(b));
		double a1 = 2.59;
		double b1 = 14.59;
		double c1 = 14.99;
		double window = 0.05;
		System.out.println("parseTime("+a1+", true): " + DateHandler.parseTime(a1, true)); 
		System.out.println("parseTime("+a1+", false): " + DateHandler.parseTime(a1, false)); 
		System.out.println("parseTime("+b1+", true): " + DateHandler.parseTime(b1, true)); 
		System.out.println("parseTime("+b1+", false): " + DateHandler.parseTime(b1, false)); 
		System.out.println("parseTime("+c1+", true): " + DateHandler.parseTime(c1, true)); 
		System.out.println("parseTime("+c1+", false): " + DateHandler.parseTime(c1, false)); 
		System.out.println("getTimeValue("+a1+", true, true): " + DateHandler.getTimeValue(DateHandler.getTimeString(today), true, true));
		System.out.println("getTimeValue("+a1+", true, false): " + DateHandler.getTimeValue(DateHandler.getTimeString(today), true, false));
		System.out.println("sameDay("+today+", "+now+"): " + DateHandler.sameDay(today, now));
		System.out.println("sameTime("+today+", "+now+", "+window+"): " + DateHandler.sameTime(today, now, window));
		System.out.println("getDay("+today+"): " + DateHandler.getDay(today));
		System.out.println("getMonth("+today+"): " + DateHandler.getMonth(today));
		System.out.println("getYear("+today+"): " + DateHandler.getYear(today));
		System.out.println("nextDate("+today+"): " + DateHandler.nextDate(today));

	}

    /**
     * Hard coded value for number of milli-seconds in
     * one day. (1000 * 60 * 60 * 24)
     */
    public static final long NUM_MILLIS_PER_DAY = 86400000;


    /**
     * Hard coded value for number of minutes
     * one day. (60 * 24)
     */
    public static final long NUM_MINUTES_PER_DAY = 1440;


    /**
     * Get today's date object.
     * @return today's date at 12 AM.
     */
    public static Date getToday() {
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
        String dateString = sdf.format(new Date());
        try {
            return sdf.parse(dateString);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return null;
    }


    /**
     * Get the time string from a date formatted to (HH:MM AM/PM).
     * @param date Given date object.
     * @return The formatted time string.
     */
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
        return String.format("%02d", dateHour) + ":" + String.format("%02d", dateMinute) + " " + am_pm;
    }


    /**
     * Get the date string from a date formatted to (MMM DD, YYYY).
     * @param date Given date object.
     * @return The formatted date string.
     */
    public static String getDateString(Date date) {
        String dateString = date.toString();
        String[] dateSplit = dateString.split(" ");
        return dateSplit[1] + " " + dateSplit[2] + ", " + dateSplit[5];
    }


    /**
     * Get a date object representing the given string.
     * @param s Should be the toString of another date object.
     * @return new Date.
     */
    public static Date parseDate(String s) {
        SimpleDateFormat sdf = new SimpleDateFormat("EEE MMM dd hh:mm:ss zzz yyyy");
        Date date = null;
        try {
            date = sdf.parse(s);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return date;
    }


    /**
     * Get a date object representing the given string.
     * @param s Should be of the format (DD/MM/YYYY).
     * @return new Date.
     */
    public static Date createDate(String s) {
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy");
        Date date = null;
        try {
            date = sdf.parse(s);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return date;
    }


    /**
     * Get a date object representing the given string.
     * @param s Should be of the format (DD/MM/YYYY).
     * @return new Date.
     */
    public static Date createDateAndTime(String s) {
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy hh:mm:ss");
        Date date = null;
        try {
            date = sdf.parse(s);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return date;
    }


    /**
     * Generate a time of day from a double value.
     * Can be an one of:
     *      exact time            in-exact time
     *    2.59 -> 02:59 AM       2.59 -> 02:35 AM
     *   14.59 -> 02:59 PM      14.99 -> 02:59 PM
     * @param value The double value to be parsed.
     * @param exact Whether to convert minutes or not.
     * @return
     */
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
        return res;
    }


    /**
     * Return a double value representing time, parsed from
     * the given timeText string. Also may choose to increment
     * or decrement the time value.
     * @param timeText String of the getTimeString() format.
     * @param doIncrement If true, value is incremented or decremented.
     * @param increment If doIncrement and this is true, increment,
     *                 else decrement.
     * @return New time as a double value.
     */
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
            if (decrease) {
                minutes = 59;
                if (hours == 0) {
                    hours = 24;
                }
                hours -= 1;
            }
        }
        else if (minutes >= 60) {
            if (increase) {
                minutes = 0;
                hours += 1;
            }
        }

        return ((hours * 100) + minutes) / 100.0;
    }


    /**
     * Add one minute to a time string.
     * @param timeText Time string of getTimeString() format.
     * @return Incremented time string.
     */
    public static String addOneMinute(String timeText) {
        double hoursMins = getTimeValue(timeText, true, true);
        return parseTime(hoursMins, true);
    }


    /**
     * Add one minute to a time string.
     * @param timeText Time string of getTimeString() format.
     * @return Incremented time string.
     */
    public static String subtractOneMinute(String timeText) {
        double hoursMins = getTimeValue(timeText, true, false);
        return parseTime(hoursMins, true);
    }


    /**
     * Determine if two dates fall on the same day.
     * @param a Date A.
     * @param b Date B.
     * @return True if same day else false.
     */
    public static boolean sameDay(Date a, Date b) {
        long aTime = a.getTime();
        long bTime = b.getTime();
        long diff;
        if (a.before(b)) {
            diff = bTime - aTime;
        }
        else {
            diff = aTime - bTime;
        }
        boolean lessThanOneDay = diff < NUM_MILLIS_PER_DAY;
        String aString = a.toString();
        String bString = b.toString();
        String[] aSplit = aString.split(" ");
        String[] bSplit = bString.split(" ");
        int aDate = Integer.parseInt(aSplit[2]);
        int bDate = Integer.parseInt(bSplit[2]);
        return lessThanOneDay && aDate == bDate && getDay(a) == getDay(b);
    }


    /**
     * Returns the a string containing only time values.
     * @param d Date.
     * @return Time string of format (HH:MM:SS).
     */
    public static String getTimeFromDate(Date d) {
        return d.toString().split(" ")[3].trim();
    }





    /**
     * Determine if two dates fall on the same HOUR interval.
     * Can be a different day, only scans the hours and minutes.
     * @param a Date A.
     * @param b Date B.
     * @param window a value between 0 and 1 representing how much
     *               much of the day to stretch (Up to one full day).
     * @return True if dates fall on the same interval, else otherwise.
     */
    public static boolean sameTime(Date a, Date b, double window) {
        if (window < 0 || window > 1) {
            window = 1;
        }
        int minutes = (int) (window * (NUM_MINUTES_PER_DAY / 2));
        double selectedBound, upperBound = 0.0, lowerBound = 0.0;
        String selectedTime = getTimeString(a);
        String dateInString = getTimeString(b);
        selectedBound = getTimeValue(dateInString, false, false);
        String upperBoundString = String.copyValueOf(selectedTime.toCharArray());
        String lowerBoundString = String.copyValueOf(selectedTime.toCharArray());
        boolean addADay = false, subADay = false;
        for (int i = 0; i < minutes; i++) {
            double prevVal = getTimeValue(upperBoundString, false, false);
            upperBound = getTimeValue(upperBoundString, true, true);
            if (prevVal == 0) {
                addADay = true;
            }
            upperBoundString = parseTime(upperBound, true);
        }
        for (int i = 0; i < minutes; i++) {
            double prevVal = getTimeValue(lowerBoundString, false, false);
            lowerBound = getTimeValue(lowerBoundString, true, false);
            if (prevVal < lowerBound) {
                subADay = true;
            }
            lowerBoundString = parseTime(lowerBound, true);
        }
        if (addADay) {
            lowerBound -= 24;
        }
        if (subADay) {
            upperBound += 24;
        }
//        System.out.println("lowerBoundString: " + lowerBoundString + ", lowerBound: " + lowerBound + "\nupperBoundString: " + upperBoundString + ", upperBound: " + upperBound + "\nselectedBound: " + selectedBound + "\naddADay: " + addADay + ", subADay: " + subADay);
        return lowerBound <= selectedBound && selectedBound <= upperBound;
    }

    /**
     * Get the year as an integer from a date object.
     * @param date Date object.
     * @return year as an int.
     */
    public static int getYear(Date date) {
        String dateString = date.toString();
        String[] dateSplit = dateString.split(" ");
        return Integer.parseInt(dateSplit[5]);
    }


    /**
     * Get the month as an integer from a date object.
     * @param date Date object.
     * @return month as an int.
     */
    public static int getMonth(Date date) {
        SimpleDateFormat sdf = new SimpleDateFormat("MM");
        return Integer.parseInt(sdf.format(date));
    }


    /**
     * Get the day as an integer from a date object.
     * @param date Date object.
     * @return day as an int.
     */
    public static int getDay(Date date) {
        String dateString = date.toString();
        String[] dateSplit = dateString.split(" ");
        return Integer.parseInt(dateSplit[2]);
    }


    /**
     * Get the day after the given day.
     * @param date Date object.
     * @return date object for the day after.
     */
    public static Date nextDate(Date date) {
        Calendar c = Calendar.getInstance();
        c.setTime(date);
        c.add(Calendar.DAY_OF_WEEK, 1);
        return c.getTime();
    }

}
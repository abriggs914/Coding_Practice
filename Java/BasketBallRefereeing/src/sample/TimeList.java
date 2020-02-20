package sample;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

import static java.util.Arrays.asList;

public enum TimeList {
    _12_00_AM("12:00 AM", 0, 0, true),
    _12_15_AM("12:15 AM", 0, 15, true),
    _12_30_AM("12:30 AM", 0, 30, true),
    _12_45_AM("12:45 AM", 0, 45, true),
    _01_00_AM("01:00 AM", 1, 0, true),
    _01_15_AM("01:15 AM", 1, 15, true),
    _01_30_AM("01:30 AM", 1, 30, true),
    _01_45_AM("01:45 AM", 1, 45, true),
    _02_00_AM("02:00 AM", 2, 0, true),
    _02_15_AM("02:15 AM", 2, 15, true),
    _02_30_AM("02:30 AM", 2, 30, true),
    _02_45_AM("02:45 AM", 2, 45, true),
    _03_00_AM("03:00 AM", 3, 0, true),
    _03_15_AM("03:15 AM", 3, 15, true),
    _03_30_AM("03:30 AM", 3, 30, true),
    _03_45_AM("03:45 AM", 3, 45, true),
    _04_00_AM("04:00 AM", 4, 0, true),
    _04_15_AM("04:15 AM", 4, 15, true),
    _04_30_AM("04:30 AM", 4, 30, true),
    _04_45_AM("04:45 AM", 4, 45, true),
    _05_00_AM("05:00 AM", 5, 0, true),
    _05_15_AM("05:15 AM", 5, 15, true),
    _05_30_AM("05:30 AM", 5, 30, true),
    _05_45_AM("05:45 AM", 5, 45, true),
    _06_00_AM("06:00 AM", 6, 0, true),
    _06_15_AM("06:15 AM", 6, 15, true),
    _06_30_AM("06:30 AM", 6, 30, true),
    _06_45_AM("06:45 AM", 6, 45, true),
    _07_00_AM("07:00 AM", 7, 0, true),
    _07_15_AM("07:15 AM", 7, 15, true),
    _07_30_AM("07:30 AM", 7, 30, true),
    _07_45_AM("07:45 AM", 7, 45, true),
    _08_00_AM("08:00 AM", 8, 0, true),
    _08_15_AM("08:15 AM", 8, 15, true),
    _08_30_AM("08:30 AM", 8, 30, true),
    _08_45_AM("08:45 AM", 8, 45, true),
    _09_00_AM("09:00 AM", 9, 0, true),
    _09_15_AM("09:15 AM", 9, 15, true),
    _09_30_AM("09:30 AM", 9, 30, true),
    _09_45_AM("09:45 AM", 9, 45, true),
    _10_00_AM("10:00 AM", 10, 0, true),
    _10_15_AM("10:15 AM", 10, 15, true),
    _10_30_AM("10:30 AM", 10, 30, true),
    _10_45_AM("10:45 AM", 10, 45, true),
    _11_00_AM("11:00 AM", 11, 0, true),
    _11_15_AM("11:15 AM", 11, 15, true),
    _11_30_AM("11:30 AM", 11, 30, true),
    _11_45_AM("11:45 AM", 11, 45, true),

    _12_00_PM("12:00 PM", 0, 0, false),
    _12_15_PM("12:15 PM", 0, 15, false),
    _12_30_PM("12:30 PM", 0, 30, false),
    _12_45_PM("12:45 PM", 0, 45, false),
    _01_00_PM("01:00 PM", 1, 0, false),
    _01_15_PM("01:15 PM", 1, 15, false),
    _01_30_PM("01:30 PM", 1, 30, false),
    _01_45_PM("01:45 PM", 1, 45, false),
    _02_00_PM("02:00 PM", 2, 0, false),
    _02_15_PM("02:15 PM", 2, 15, false),
    _02_30_PM("02:30 PM", 2, 30, false),
    _02_45_PM("02:45 PM", 2, 45, false),
    _03_00_PM("03:00 PM", 3, 0, false),
    _03_15_PM("03:15 PM", 3, 15, false),
    _03_30_PM("03:30 PM", 3, 30, false),
    _03_45_PM("03:45 PM", 3, 45, false),
    _04_00_PM("04:00 PM", 4, 0, false),
    _04_15_PM("04:15 PM", 4, 15, false),
    _04_30_PM("04:30 PM", 4, 30, false),
    _04_45_PM("04:45 PM", 4, 45, false),
    _05_00_PM("05:00 PM", 5, 0, false),
    _05_15_PM("05:15 PM", 5, 15, false),
    _05_30_PM("05:30 PM", 5, 30, false),
    _05_45_PM("05:45 PM", 5, 45, false),
    _06_00_PM("06:00 PM", 6, 0, false),
    _06_15_PM("06:15 PM", 6, 15, false),
    _06_30_PM("06:30 PM", 6, 30, false),
    _06_45_PM("06:45 PM", 6, 45, false),
    _07_00_PM("07:00 PM", 7, 0, false),
    _07_15_PM("07:15 PM", 7, 15, false),
    _07_30_PM("07:30 PM", 7, 30, false),
    _07_45_PM("07:45 PM", 7, 45, false),
    _08_00_PM("08:00 PM", 8, 0, false),
    _08_15_PM("08:15 PM", 8, 15, false),
    _08_30_PM("08:30 PM", 8, 30, false),
    _08_45_PM("08:45 PM", 8, 45, false),
    _09_00_PM("09:00 PM", 9, 0, false),
    _09_15_PM("09:15 PM", 9, 15, false),
    _09_30_PM("09:30 PM", 9, 30, false),
    _09_45_PM("09:45 PM", 9, 45, false),
    _10_00_PM("10:00 PM", 10, 0, false),
    _10_15_PM("10:15 PM", 10, 15, false),
    _10_30_PM("10:30 PM", 10, 30, false),
    _10_45_PM("10:45 PM", 10, 45, false),
    _11_00_PM("11:00 PM", 11, 0, false),
    _11_15_PM("11:15 PM", 11, 15, false),
    _11_30_PM("11:30 PM", 11, 30, false),
    _11_45_PM("11:45 PM", 11, 45, false);

    private String name;
    private int hour, minute;
    private boolean isAM;

    TimeList(String name, int hour, int minute, boolean isAM){
        this.name = name;
        this.hour = hour;
        this.minute = minute;
        this.isAM = isAM;
    }

    public String getName() {
        return name;
    }

    public int getHour() {
        if (isAM) {
            return hour;
        }
        return hour + 12;
    }

    public int getMinute() {
        return minute;
    }

    public boolean isAM() {
        return isAM;
    }

    //    public ArrayList<String> getValues() {
//        ArrayList<String> res = new ArrayList<>();
//    }

    public static ArrayList<TimeList> getValues() {
        return new ArrayList<>(Arrays.asList(TimeList.values()));
    }

    public static Comparator<TimeList> compareHours() {
        return Comparator.comparing(TimeList::getHour);
    }

    public String toString() {
        return name;
    }
}

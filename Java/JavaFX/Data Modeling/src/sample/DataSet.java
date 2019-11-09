package sample;

import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;

import java.util.*;

public class DataSet{

    private String name;
    private Color color;
    private HashMap<String, Double> dataPoints;
    private ArrayList<String> sortedDates;
    private ArrayList<Double> sortedPoints;
//    private ArrayList<String> rows;
//    private ArrayList<String> cols;
//    private HashMap<String, HashMap<String, Double>> dataPoints;
//    private HashMap<ArrayList<String>, HashMap<String, HashMap<String, Double>>> data;

    DataSet(String name, Color color) {
        this.name = name;
        this.color = color;
        this.dataPoints = new HashMap<>();
        this.sortedDates = new ArrayList<>();
        this.sortedPoints = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public HashMap<String, Double> getDataPoints() {
        return dataPoints;
    }

    public void put(String date, Double point) {
        if (valid(date)) {
            if (validPoint(point)) {
                this.dataPoints.put(date, point);
                this.sortedDates = getSortedDates();
                this.sortedPoints = getSortedPoints();
            }
        }
    }

    private boolean validPoint(Double point) {
        return true; // can't think of a reason to return false here yet...
    }

    private boolean valid(String date) {
        try {
            String[] identifiers = date.split("-", 3);
            int year = Integer.parseInt(identifiers[0]);
            int month = Integer.parseInt(identifiers[1]);
            int day = Integer.parseInt(identifiers[2]);
            if (year < 0 || year > 2099) {
                throw new Exception("Year out of range:\t" + year);
            }
            if (month < 0 || month > 12) {
                throw new Exception("Month out of range:\t" + month);
            }
            if (day < 0 || day > 31) {
                throw new Exception("Day out of range:\t" + day);
            }
            ArrayList<Integer> shortMonths = new ArrayList<>(Arrays.asList(2, 4, 6, 9, 11));
            if (shortMonths.contains(month)) {
                if (day > 30 || (month == 2 && day > 29)) {
                    throw new Exception("Day doesn't logically make sense:\t" + day);
                }
            }
            return true;
        } catch (Exception e) {
            System.out.println("Date:\t" + date);
            e.printStackTrace();
            return false;
        }
    }

    public ArrayList<String> getSortedDates() {
        Set<String> keys = dataPoints.keySet();
        String[] keysArr = keys.toArray(new String[0]);
        ArrayList<String> res = new ArrayList<>(Arrays.asList(keysArr));
        Collections.sort(res);
        return res;
    }

    public ArrayList<Double> getSortedPoints() {
        ArrayList<String> keys = getSortedDates();
        ArrayList<Double> res = new ArrayList<>();
        for (String key : keys) {
            res.add(this.dataPoints.get(key));
        }
        return res;
    }

    public Paint getColor() {
        return this.color;
    }
}

//    private HashMap<String, ArrayList<Double>> processData(HashMap<String, Double> dataPoints) {
//        if (validData(dataPoints)) {
//
//        }
//    }
//
//    private boolean validData(HashMap<String, Double> dataPoints) {
//
//    }
//
//    public void setDataPoints(HashMap<String, HashMap<String, Double>> dataPoints) {
//        boolean validSet = true;
//        if (this.rows.containsAll(dataPoints.keySet())) {
//            Set<Entry<String, HashMap<String, Double>>> set = dataPoints.entrySet();
//            for (Object o : set) {
//                Map.Entry entry = (Map.Entry) o;
//                String rowName = (String) entry.getKey();
//                HashMap<String, Double> colNames = (HashMap<String, Double>) entry.getValue();
//                if (!this.cols.containsAll(colNames.keySet())) {
//                    validSet = false;
//                }
//            }
//        }
//        this.dataPoints = dataPoints;
//    }
//
//    public void initializeDataSet(HashMap<String, Double> dataPoints) {
//        this.dataPoints = processData(dataPoints);
//    }
//}

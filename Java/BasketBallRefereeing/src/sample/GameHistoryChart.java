package sample;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.collections.ObservableList;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.chart.XYChart.Data;
import javafx.scene.control.Tooltip;
import javafx.util.Duration;

import java.lang.reflect.Field;
import java.util.*;

public class GameHistoryChart {

//    private LineChart<Number, Number> sampleChart;
    private GameHistoryForm ghf;
    private LineChart<Number, Number> lineChart;

    public GameHistoryChart(GameHistoryForm ghf, LineChart<Number, Number> lineChart) {
//        this.sampleChart = genSampleChart();
        this.ghf = ghf;
        this.lineChart = lineChart;
    }

    public LineChart<Number, Number> drawLineChart(boolean resetChart) {
        ArrayList<Game> filteredGames = this.ghf.getFilteredGames();
        if (resetChart) {
            this.lineChart.getData().clear();
        }
        boolean none = ghf.isNoFilterSelected();
        if (!none) {
            if (ghf.isFilterDate()) {
                return drawLineChartDateVSNumGames(filteredGames);
            }
            else {
                if (ghf.isFilterGym()) {
                    return drawLineChartGymVSNumGames(filteredGames);
                }
            }
        }
        return drawLineChartDateVSNumGames(filteredGames);
    }

    /**
     * graphs the given games against date on the x-axis
     * and numGames on the Y-axis.
     * @param games
     * @return
     */
    public LineChart<Number, Number> drawLineChartDateVSNumGames(ArrayList<Game> games) {
        System.out.println("games: " + games);

        ArrayList<String> datesList = genDatesAxisLabels(games);
        HashMap<String, Integer> datesValues = genStringIntHashMap(datesList);

        // if date in games list, increment value
        System.out.println("datesValues != null: " + (datesValues != null) + ", size: " + datesList.size());
        for (Game g : games) {
            System.out.println("\tChecking on date: " + Utilities.getDateString(g.getDate()));
            String dateString = Utilities.getDateString(g.getDate());
            int curr = datesValues.get(dateString);
            datesValues.put(dateString, curr + 1);
        }

        System.out.println("hashmap: " + datesValues);
        XYChart.Series dataSeries = genXYDataSeries("Games per day", datesValues, datesList);
        this.lineChart.getData().add(dataSeries);
        addToolTips(dataSeries);
        return lineChart;
    }

    public LineChart<Number, Number> drawLineChartGymVSNumGames(ArrayList<Game> games) {
        ArrayList<String> gymsList = Gym.getStringValues();
        HashMap<String, Integer> gymValues = genStringIntHashMap(gymsList);

        for (Game game : games) {
            String gym = game.getGym().getName();
            int val = gymValues.get(gym);
            gymValues.put(gym, val + 1);
        }

        XYChart.Series dataSeries = genXYDataSeries("Times in gym", gymValues, gymsList);
        this.lineChart.getData().add(dataSeries);
        addToolTips(dataSeries);
        return lineChart;
    }

    private void addToolTips(XYChart.Series series) {
        for (Data<Number, Number> entry : (ObservableList<Data<Number, Number>>) series.getData()) {
//            System.out.print("Entered! entry: " + entry + ", Y: " + entry.getYValue() + ", X: " + entry.getXValue());
            String message = "(" + entry.getXValue() + ", " + entry.getYValue().toString() + ")";
            Tooltip t = new Tooltip(message);
            hackTooltipStartTiming(t);
//            System.out.println(", message: " + t.getText());
            Tooltip.install(entry.getNode(), t);
        }
    }

    public static void hackTooltipStartTiming(Tooltip tooltip) {
        try {
            Field fieldBehavior = tooltip.getClass().getDeclaredField("BEHAVIOR");
            fieldBehavior.setAccessible(true);
            Object objBehavior = fieldBehavior.get(tooltip);

            Field fieldTimer = objBehavior.getClass().getDeclaredField("activationTimer");
            fieldTimer.setAccessible(true);
            Timeline objTimer = (Timeline) fieldTimer.get(objBehavior);

            objTimer.getKeyFrames().clear();
            objTimer.getKeyFrames().add(new KeyFrame(new Duration(150)));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private XYChart.Series genXYDataSeries(String label, HashMap<String, Integer> values, ArrayList<String> keys) {
        XYChart.Series dataSeries = new XYChart.Series();
        dataSeries.setName(label);
        for (String key : keys) {
            int val = values.get(key);
//            System.out.println("\tadding " + key + " : " + val);
            dataSeries.getData().add(new XYChart.Data(key, val));
        }
        return dataSeries;
    }

    private HashMap<String, Integer> genStringIntHashMap(ArrayList<String> keys) {
        HashMap<String, Integer> res = new HashMap<>();
        for (String str : keys) {
            if (!res.keySet().contains(str)) {
                res.put(str, 0);
            }
        }
//        System.out.println("\ndates hashMap:");
//        res.forEach((k, v) -> System.out.println("\tk: " + k + ", v: " + v));
        return res;
    }

    public LineChart<Number, Number> setSampleChart(LineChart<Number, Number> lineChart) {
//        NumberAxis xAxis = new NumberAxis();
//        xAxis.setLabel("No of employees");
//
//        NumberAxis yAxis = new NumberAxis();
//        yAxis.setLabel("Revenue per employee");

//        lineChart = new LineChart(xAxis, yAxis);

        XYChart.Series dataSeries1 = new XYChart.Series();
        dataSeries1.setName("2014");

        dataSeries1.getData().add(new XYChart.Data( "0", 567));
        dataSeries1.getData().add(new XYChart.Data( "1", 567));
        dataSeries1.getData().add(new XYChart.Data( "2", 567));
        dataSeries1.getData().add(new XYChart.Data( "3", 567));
        dataSeries1.getData().add(new XYChart.Data( "4", 567));
        dataSeries1.getData().add(new XYChart.Data( "5", 612));
        dataSeries1.getData().add(new XYChart.Data("6", 800));
        dataSeries1.getData().add(new XYChart.Data("7", 780));
        dataSeries1.getData().add(new XYChart.Data( "8", 567));
        dataSeries1.getData().add(new XYChart.Data("9", 810));
        dataSeries1.getData().add(new XYChart.Data("10", 850));

        lineChart.getData().add(dataSeries1);
        ArrayList<String> s = genDatesAxisLabels(Main.gameManager.getGames());

        return lineChart;
    }

    private ArrayList<String> genDatesAxisLabels(ArrayList<Game> arr) {
        ArrayList<String> res = new ArrayList<>();
        ArrayList<Date> datesList = Main.gameManager.getGameDates(arr);
        Calendar calendar = Calendar.getInstance();
        Date firstDate = Utilities.getFirstDate(arr);
        Date lastDate = Utilities.getLastDate(arr);
        firstDate = ((ghf.isStartFromBeginning())? firstDate : Controller.gameHistory_getStartDate());
        lastDate = ((ghf.isGraphToEnd())? lastDate : Controller.gameHistory_getEndDate());
        System.out.println("ghf.isStartFromBeginning(): " + ghf.isStartFromBeginning() + ", ghf.isGraphToEnd(): " + ghf.isGraphToEnd());
        System.out.println("Graphing games from: " + firstDate + " -> " + lastDate);
        if (firstDate != null && lastDate != null) {
            calendar.setTime(firstDate);
            Date temp = firstDate;
            while (temp.before(lastDate) && !Utilities.sameDay(temp, lastDate)) {
                temp = calendar.getTime();
//                System.out.println("\tToday is: " + temp);
                String s = Utilities.getDateString(temp);
                res.add(s);
                calendar.add(Calendar.DAY_OF_YEAR, 1);
            }
            if (res.size() == 0) {
                res.add(Utilities.getDateString(firstDate));
            }
        }
        System.out.println("dates labels: " + res);
        return res;
    }
}

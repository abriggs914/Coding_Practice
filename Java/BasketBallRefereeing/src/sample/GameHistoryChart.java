package sample;

import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;

public class GameHistoryChart {

//    private LineChart<Number, Number> sampleChart;
    private GameHistoryForm ghf;
    private LineChart<Number, Number> lineChart;

    public GameHistoryChart(GameHistoryForm ghf, LineChart<Number, Number> lineChart) {
//        this.sampleChart = genSampleChart();
        this.ghf = ghf;
        this.lineChart = lineChart;
    }

    public LineChart<Number, Number> drawLineChart() {
        ArrayList<Game> filteredGames = this.ghf.getFilteredGames();
        boolean none = ghf.isNoFilterSelected();
        if (!none) {
            if (ghf.isFilterDate()) {
                return drawLineChartDateVSNumGames(filteredGames);
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
        ArrayList<String> datesList = genDatesAxisLabels(games);
        HashMap<String, Integer> datesValues = new HashMap<>();
        XYChart.Series dataSeries1 = new XYChart.Series();
        dataSeries1.setName("Games per day");
        for (String dateString : datesList) {
            if (!datesValues.keySet().contains(dateString)) {
                datesValues.put(dateString, 0);
            }
        }
        for (Game g : games) {
            String dateString = Utilities.getDateString(g.getDate());
                int curr = datesValues.get(dateString);
//                System.out.println("\tgame " + dateString + " -> " + curr);
                datesValues.put(dateString, curr + 1);
        }
        System.out.println("hashmap: " + datesValues);
        for (String key : datesList) {
            int val = datesValues.get(key);
//            System.out.println("\tadding " + key + " : " + val);
            dataSeries1.getData().add(new XYChart.Data( key, val));
        }
        this.lineChart.getData().add(dataSeries1);
        return lineChart;
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
        Date firstDate = null, lastDate = null;
        for (int i = 0; i < datesList.size(); i++) {
            Date d = datesList.get(i);
            if (i == 0) {
                firstDate = d;
            }
            if (i == datesList.size() - 1) {
                lastDate = d;
            }
        }
        firstDate = ((ghf.isStartFromBeginning())? Controller.gameHistory_getStartDate() : firstDate);
        lastDate = ((ghf.isGraphToEnd())? Controller.gameHistory_getEndDate() : lastDate);
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
//            System.out.println("dates labels: " + res);
        }
        return res;
    }
}

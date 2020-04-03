package sample;

import javafx.scene.chart.XYChart;

import java.util.ArrayList;
import java.util.Date;

public class PandemicHistory {

    private ArrayList<HistoryPoint> history;
    private Date startDate;
    private ArrayList<Person> startPopulation;
    private ArrayList<Person> infectedStartPopulation;
//    private ArrayList<Person> infectedCountPopulation;
//    private ArrayList<Person> passedCountPopulation;
//    private ArrayList<Person> curedCountPopulation;
    private Disease disease;

    PandemicHistory(Date startDate, ArrayList<Person> startPopulation, ArrayList<Person> infectedStartPopulation, Disease disease) {
        this.history = new ArrayList<>();
        this.startDate = startDate;
        this.startPopulation = startPopulation;
        this.infectedStartPopulation = infectedStartPopulation;
        this.disease = disease;
//        passedCountPopulation = new ArrayList<>();
//        infectedCountPopulation = new ArrayList<>();
//        curedCountPopulation = new ArrayList<>();
    }

    public void addHistoryPoint(HistoryPoint hp) {
        history.add(hp);
//        passedCountPopulation.addAll(hp.getPassedTodayPopulation());
//        curedCountPopulation.addAll(hp.getCuredTodayPopulation());
//        infectedCountPopulation.addAll(hp.getInfectedTodayPopulation());
    }

    public Disease getDisease() {
        return disease;
    }

    public void setDisease(Disease disease) {
        this.disease = disease;
    }

    public XYChart.Series<String, Double> getPopulationTotalSeries() {
        XYChart.Series<String, Double> series = new XYChart.Series<>();
        for (HistoryPoint hp : history) {
            System.out.println("TOTAL_POP\tday: " + hp.getDay() + "\t" + (double) startPopulation.size() + "\t" + startPopulation.size());
            series.getData().add(new XYChart.Data<>(DateHandler.getFormattedString(hp.getDay()), (double) startPopulation.size()));
        }
        return series;
    }

    public XYChart.Series<String, Double> getPassedTotalSeries() {
        XYChart.Series<String, Double> series = new XYChart.Series<>();
        for (HistoryPoint hp : history) {
            System.out.println("PASST_POP\tday: " + hp.getDay() + "\t" + (double) hp.getPassedPopulation().size() + "\t" + hp.getPassedPopulation());
            series.getData().add(new XYChart.Data<>(DateHandler.getFormattedString(hp.getDay()), (double) hp.getPassedPopulation().size()));
        }
        return series;
    }

    public XYChart.Series<String, Double> getInfectedTotalSeries() {
        XYChart.Series<String, Double> series = new XYChart.Series<>();
        for (HistoryPoint hp : history) {
            System.out.println("INFTO_POP\tday: " + hp.getDay() + "\t" + (double) hp.getInfectedPopulation().size() + "\t" + hp.getInfectedPopulation());
            series.getData().add(new XYChart.Data<>(DateHandler.getFormattedString(hp.getDay()), (double) hp.getInfectedPopulation().size()));
        }
        return series;
    }

    public XYChart.Series<String, Double> getCuredTotalSeries() {
        XYChart.Series<String, Double> series = new XYChart.Series<>();
        for (HistoryPoint hp : history) {
            System.out.println("CURTO_POP\tday: " + hp.getDay() + "\t" + (double) hp.getCuredPopulation().size() + "\t" + hp.getCuredPopulation());
            series.getData().add(new XYChart.Data<>(DateHandler.getFormattedString(hp.getDay()), (double) hp.getCuredPopulation().size()));
        }
        return series;
    }

    public XYChart.Series<String, Double> getPassedDailySeries() {
        XYChart.Series<String, Double> series = new XYChart.Series<>();
        for (HistoryPoint hp : history) {
            System.out.println("PASSD_POP\tday: " + hp.getDay() + "\t" + (double) hp.getPassedTodayPopulation().size() + "\t" + hp.getPassedTodayPopulation());
            series.getData().add(new XYChart.Data<>(DateHandler.getFormattedString(hp.getDay()), (double) hp.getPassedTodayPopulation().size()));
        }
        return series;
    }

    public XYChart.Series<String, Double> getInfectedDailySeries() {
        XYChart.Series<String, Double> series = new XYChart.Series<>();
        for (HistoryPoint hp : history) {
            System.out.println("INFDA_POP\tday: " + hp.getDay() + "\t" + (double) hp.getInfectedTodayPopulation().size() + "\t" + hp.getInfectedTodayPopulation());
            series.getData().add(new XYChart.Data<>(DateHandler.getFormattedString(hp.getDay()), (double) hp.getInfectedTodayPopulation().size()));
        }
        return series;
    }

    public XYChart.Series<String, Double> getCuredDailySeries() {
        XYChart.Series<String, Double> series = new XYChart.Series<>();
        for (HistoryPoint hp : history) {
            System.out.println("CURDA_POP\tday: " + hp.getDay() + "\t" + (double) hp.getCuredTodayPopulation().size() + "\t" + hp.getCuredTodayPopulation());
            series.getData().add(new XYChart.Data<>(DateHandler.getFormattedString(hp.getDay()), (double) hp.getCuredTodayPopulation().size()));
        }
        return series;
    }
}

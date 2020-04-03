package sample;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Date;

public class HistoryPoint {

    private Date day;
    private ArrayList<Person> infectedPopulation;
    private ArrayList<Person> curedPopulation;
    private ArrayList<Person> passedPopulation;
    private ArrayList<Person> infectedTodayPopulation;
    private ArrayList<Person> curedTodayPopulation;
    private ArrayList<Person> passedTodayPopulation;

    public HistoryPoint(
            Date day,
            ArrayList<Person> infectedPopulation,
            ArrayList<Person> curedPopulation,
            ArrayList<Person> passedPopulation,
            ArrayList<Person> infectedTodayPopulation,
            ArrayList<Person> curedTodayPopulation,
            ArrayList<Person> passedTodayPopulation) {
        this.day = day;
        this.infectedPopulation = new ArrayList<>(infectedPopulation);
        this.curedPopulation = new ArrayList<>(curedPopulation);
        this.passedPopulation = new ArrayList<>(passedPopulation);
        this.infectedTodayPopulation = new ArrayList<>(infectedTodayPopulation);
        this.curedTodayPopulation = new ArrayList<>(curedTodayPopulation);
        this.passedTodayPopulation = new ArrayList<>(passedTodayPopulation);
    }

    public Date getDay() {
        return day;
    }

    public void setDay(Date day) {
        this.day = day;
    }

    public ArrayList<Person> getInfectedPopulation() {
        return infectedPopulation;
    }

    public void setInfectedPopulation(ArrayList<Person> infectedPopulation) {
        this.infectedPopulation = infectedPopulation;
    }

    public ArrayList<Person> getCuredPopulation() {
        return curedPopulation;
    }

    public void setCuredPopulation(ArrayList<Person> curedPopulation) {
        this.curedPopulation = curedPopulation;
    }

    public ArrayList<Person> getInfectedTodayPopulation() {
        return infectedTodayPopulation;
    }

    public void setInfectedTodayPopulation(ArrayList<Person> infectedTodayPopulation) {
        this.infectedTodayPopulation = infectedTodayPopulation;
    }

    public ArrayList<Person> getCuredTodayPopulation() {
        return curedTodayPopulation;
    }

    public void setCuredTodayPopulation(ArrayList<Person> curedTodayPopulation) {
        this.curedTodayPopulation = curedTodayPopulation;
    }

    public ArrayList<Person> getPassedPopulation() {
        return passedPopulation;
    }

    public void setPassedPopulation(ArrayList<Person> passedPopulation) {
        this.passedPopulation = passedPopulation;
    }

    public ArrayList<Person> getPassedTodayPopulation() {
        return passedTodayPopulation;
    }

    public void setPassedTodayPopulation(ArrayList<Person> passedTodayPopulation) {
        this.passedTodayPopulation = passedTodayPopulation;
    }
}

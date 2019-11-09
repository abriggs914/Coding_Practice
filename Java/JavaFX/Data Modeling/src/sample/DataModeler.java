package sample;

import javafx.scene.layout.BorderPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;

import java.util.ArrayList;

public class DataModeler {

    private ArrayList<DataSet> dataSets;
    private String currDate;

    DataModeler(ArrayList<DataSet> dataSets) {
        this.dataSets = dataSets;
        if (dataSets.size() > 0) {
            this.currDate = dataSets.get(0).getSortedDates().get(0);
        }
//        currDate.
    }

    public ArrayList<DataSet> getDataSets() {
        return dataSets;
    }

    public void setCurrDate(String date) {
        this.currDate = date;
//        Main.dataViewer.layoutChildren();
    }

    public String getCurrDate() {
        return currDate;
    }
}

package sample;

import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.MenuBar;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;

import java.util.ArrayList;

public class ViewableDataSet extends Pane {

    private DataSet dataSet;
    private int idNum;
    private ArrayList<String> sortedDates;
    private ArrayList<Double> sortedPoints;
    private Scene scene;

    ViewableDataSet(int idNum, DataSet  dataSet) {
        this.idNum = idNum;
        this.dataSet = dataSet;
        this.sortedDates = dataSet.getSortedDates();
        this.sortedPoints = dataSet.getSortedPoints();
        this.scene = Main.getScene();
        System.out.println("NEW VIEWABLEDATASET");
    }

    @Override
    public void layoutChildren() {
        draw();
    }

    private void draw() {
        this.getChildren().clear();

        Rectangle r = new Rectangle(200.0, 25.0, Color.GREENYELLOW);
//        this.getChildren().add(r);

        Canvas canvas = new Canvas();
        MenuBar menu = Main.getMenu();
        GraphicsContext gc = canvas.getGraphicsContext2D();
        double showSpace = scene.getHeight() - menu.getPrefHeight();
        gc.setFill(dataSet.getColor());
        String currDate = Main.dataModeler.getCurrDate();
//        double height = ;
        double width = (Math.max(0, sortedPoints.get(sortedDates.indexOf(currDate))) * Main.SCALAR);
        double y = showSpace / (Main.getMaxSataSetsPerScreen() + 1);
        double x = 100;
        System.out.println("showSpace: " + showSpace + ", Main.getMaxSataSetsPerScreen(): " + Main.getMaxSataSetsPerScreen());
        System.out.println("1\twidth:\t" + width + "\tx:\t" + x + "\ty:\t" + y);
        y = (scene.getHeight() - (showSpace - (idNum * y))); // where rows start
//        gc.fillRect();
        gc.setStroke(Color.BLACK);
        gc.strokeRect(x, y, width, 25);
        gc.strokeText(dataSet.getName(), (x + width + 50), y);

        this.setHeight(showSpace / (Main.getMaxSataSetsPerScreen() + 1));
        this.setWidth(width);
        this.setLayoutX(x);
        this.setLayoutY(y);
        this.getChildren().add(canvas);
        this.setStyle("-fx-border-color: black");
        System.out.println("2\twidth:\t" + width + "\tx:\t" + x + "\ty:\t" + y);
    }

    @Override
    public String toString() { return "VIEWABLEDATASET: #" + idNum; }
}

package sample;

import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;

//import java.lang.reflect.Array;
import java.util.ArrayList;

public class DataViewer extends BorderPane {

    private ArrayList<ViewableDataSet> viewableDataSets;

    public Label dateLabel;
    public Rectangle RECTANGLE = new Rectangle(500, 50, Color.RED);

    DataViewer() {
        this.viewableDataSets = new ArrayList<>();
        this.setHeight(Main.getScene().getHeight() - Main.getMenu().getPrefHeight());
    }

    @Override
    public void layoutChildren() {
        draw();
    }

    public void draw() {
        System.out.println("DRAWING 1");
        System.out.println("children: " + this.getChildren());
//        this.getChildren().clear(); // <--
        System.out.println("cleared children: " + this.getChildren());
        System.out.println("DRAWING 2");
//        viewableDataSets.clear();
        if (this.getChildren().size() == 0) {
            ArrayList<DataSet> dataSets = Main.dataModeler.getDataSets();
            for (int i = 0; i < dataSets.size(); i++) {
                DataSet set = dataSets.get(i);
                System.out.println("\tkeys:\n" + set.getSortedDates());
                System.out.println("\tvals:\n" + set.getSortedPoints());
                viewableDataSets.add(new ViewableDataSet(i, set));
            }
            this.setTop(RECTANGLE);
            System.out.println("DRAWING 3");
            HBox hBox = new HBox();
            Scene scene = Main.getScene();
            hBox.setLayoutX(0);
            hBox.setLayoutY(scene.getHeight() -
                ((scene.getHeight() - Main.getMenu().getPrefHeight())));
            GridPane gridPane = new GridPane();
            int i = 0;
            for (ViewableDataSet viewableDataSet : viewableDataSets) {
                gridPane.addRow(i++, viewableDataSet);
            }
            dateLabel = new Label("I AM A DATE LABEL");
            dateLabel.setPrefSize(200,25);
            dateLabel.setMinSize(200,25);
            dateLabel.setStyle("-fx-border-color: green");
            hBox.getChildren().add(gridPane);
            hBox.getChildren().add(dateLabel);
            Pane pane_new = new Pane();
            pane_new.setPrefSize(100,100);
            hBox.getChildren().add(pane_new);
            hBox.setStyle("-fx-border-color: purple");
//            hBox.getChildren().addAll(gridPane, dateLabel);
            this.setCenter(hBox); // <--
            System.out.println("DRAWING 4");
            Pane leftPane = new Pane();
            Pane rightPane = new Pane();
            leftPane.setPrefWidth(100);
            leftPane.setPrefHeight(550);
            rightPane.setPrefWidth(100);
            rightPane.setPrefHeight(550);
            System.out.println("DRAWING 5");
            this.setLeft(leftPane);
            System.out.println("DRAWING 6");
            this.setRight(rightPane);

            for (ViewableDataSet viewableDataSet : viewableDataSets) {
//            gridPane.addRow(i++, viewableDataSet);
                viewableDataSet.layoutChildren();
            }

            this.setLayoutX(0);
            this.setLayoutY(scene.getHeight() - (scene.getHeight() - Main.getMenu().getPrefHeight()));
        }
        System.out.println("DRAWING 2.5");
//        GridPane gridPane = new GridPane();
        System.out.println("DRAWING 2.75");
//        gridPane.setLayoutX(0);
//        gridPane.setLayoutY(scene.getHeight() -
//                ((scene.getHeight() - Main.getMenu().getPrefHeight())));
//        int i = 0;
        synchronized (this) {
            for (ViewableDataSet viewableDataSet : viewableDataSets) {
                //            gridPane.addRow(i++, viewableDataSet);
                viewableDataSet.layoutChildren();
            }
        }
        System.out.println("DRAWING 2.85");

        System.out.println("DRAWING 7");
    }
}

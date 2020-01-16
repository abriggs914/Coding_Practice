package sample;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Spinner;
import javafx.scene.layout.HBox;
import javafx.scene.text.Font;

import java.util.ArrayList;
import java.util.Arrays;

public class SimToolBar extends HBox {

    private ArrayList<String> speedStrings = new ArrayList<>(Arrays.asList("0.5", "1", "1.25", "1.5", "2"));
    private ObservableList<String> speedList = FXCollections.observableArrayList(speedStrings);
    private Label speedLabel = new Label("sim speed:");
    private Spinner speedSpinner = new Spinner<>(speedList);
    private Button playButton = new Button("PLAY");
    private Button stopButton = new Button("STOP");
    private Font helvetica = new Font("Helvetica", 15);

    public SimToolBar() {
        speedLabel.setFont(helvetica);

        playButton.setOnAction(event -> {
            System.out.println("simulating...");
        });

        stopButton.setOnAction(event -> {
            System.out.println("stopping...");
        });

        this.setSpacing(15);
        this.setPadding(new Insets(10,10,10,10));
        this.getChildren().addAll(speedLabel, speedSpinner, playButton, stopButton);
    }

}

package sample;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import javafx.util.Duration;

import java.util.ArrayList;
import java.util.Random;

public class View extends BorderPane {

    public static Button roll;
    public static TextField sidesOnDieTextField;
    public static Label sidesOnDieLabel;
    public static VBox centerVBox;
    public static Rectangle rectangleColor;
    public static Label rectangleLabel;
    public static TextField numberRolledTextField;
    public static Label numberRolledLabel;

    public static int numSidesOnDie;
    public static int rollNumber;
    public static Color selectedColor;
    public static ArrayList<Color> colors;

    public View() {
        init();

        roll.setOnMouseClicked(event -> {

            Timeline timeline = new Timeline(new KeyFrame(Duration.seconds(0.1), new EventHandler<ActionEvent>() {

                private int i = 0;

                @Override
                public void handle(ActionEvent event) {
                    numSidesOnDie = getNumberSidesOnDie();
//            System.out.println("rolling");
                    int rndNumber = generateRollNumber();
                    selectedColor = generateRollColor();
                    rectangleColor.setFill(selectedColor);
                    numberRolledTextField.setText(Integer.toString(rndNumber));
                    i++;
                }
            }));
            timeline.setCycleCount(10);
            timeline.play();


//            this.numSidesOnDie = getNumberSidesOnDie();
////            System.out.println("rolling");
//            int rndNumber = generateRollNumber();
//            this.selectedColor = generateRollColor();
//            rectangleColor.setFill(selectedColor);
//            numberRolledTextField.setText(Integer.toString(rndNumber));
        });
    }

    private int getNumberSidesOnDie() {
        String txt = sidesOnDieTextField.getText();
        if (checkInt(txt)) {
            return Integer.parseInt(txt);
        }
        return 1;
    }

    private boolean checkInt(String txt) {
        try {
            Integer.parseInt(txt);
            return true;
        }
        catch (Exception e) {
            return false;
        }
    }

    private Color generateRollColor() {
        Random r = new Random();
        return colors.get(r.nextInt(colors.size()));
    }

    private int generateRollNumber() {
        Random r = new Random();
        return r.nextInt(numSidesOnDie) + 1;
    }

    public void init() {
        initCenterComponents();
//        initRightComponents();
        initLeftComponents();
        setCenterComponents();
//        setRightComponents();
        setLeftComponents();

        rollNumber = 0;
        numSidesOnDie = 1;
    }

    private void initCenterComponents() {
        colors = new ArrayList<>();
        colors.add(Color.RED);
        colors.add(Color.BLUE);
        colors.add(Color.GREEN);
        colors.add(Color.HOTPINK);
        colors.add(Color.YELLOW);
        colors.add(Color.ORANGE);
        Random r = new Random();
        selectedColor = colors.get(r.nextInt(colors.size()));

        centerVBox = new VBox();
        rectangleColor = new Rectangle();
        rectangleLabel = new Label("Color rolled:");
        numberRolledTextField = new TextField();
        numberRolledLabel = new Label("Number rolled:");

        centerVBox.setPadding(new Insets(10,10,10,10));
        centerVBox.setMinSize(200, 200);
        centerVBox.setStyle("-fx-border-color: black;");
        rectangleLabel.setMinSize(80, 30);
        rectangleColor.setWidth(90);
        rectangleColor.setHeight(90);

        numberRolledTextField.setMinSize(80, 30);
        numberRolledTextField.setFont(new Font("times", 28));
        numberRolledLabel.setMinSize(80, 30);

        VBox vBox = new VBox();
        roll = new Button("ROLL");
        roll.setMinSize(80, 50);
        vBox.getChildren().add(roll);
        vBox.setPadding(new Insets(10,10,10,10));
    }

    private void setCenterComponents() {
        VBox vboxColor = new VBox();
        VBox vboxNumber = new VBox();
        VBox vboxButton = new VBox();

        vboxColor.getChildren().addAll(rectangleLabel, rectangleColor);
        vboxNumber.getChildren().addAll(numberRolledLabel, numberRolledTextField);

        vboxButton.getChildren().add(roll);
        centerVBox.getChildren().addAll(vboxNumber, vboxColor, vboxButton);

        this.setCenter(centerVBox);
    }

    public void initLeftComponents() {
        sidesOnDieTextField = new TextField();
        sidesOnDieLabel = new Label("Enter number of sides:");

        sidesOnDieLabel.setMinSize(80, 30);
        sidesOnDieTextField.setMinSize(80, 30);
    }

    public void setLeftComponents() {
        VBox vBox = new VBox();
        vBox.getChildren().addAll(sidesOnDieLabel, sidesOnDieTextField);
        vBox.setPadding(new Insets(10,10,10,10));
        this.setLeft(vBox);
    }

    public void initRightComponents() {
        VBox vBox = new VBox();
        roll = new Button("ROLL");
        vBox.getChildren().add(roll);
        vBox.setPadding(new Insets(10,10,10,10));
    }

    public void setRightComponents() {
        this.setRight(roll);
    }

}

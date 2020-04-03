package sample;

import javafx.animation.Animation;
import javafx.event.ActionEvent;
import javafx.event.Event;
import javafx.event.EventHandler;
import javafx.event.EventTarget;
import javafx.scene.chart.AreaChart;
import javafx.scene.chart.LineChart;
import javafx.scene.control.*;
import javafx.scene.input.KeyEvent;
import javafx.scene.input.MouseButton;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.Pane;

import java.util.Date;
import java.util.Random;

public class Controller {

    private static Pane interactionView;
    private static Button simulateButton;
    private static Button clearButton;
    private static Button stopButton;
    private static TextField numStartPeopleTextField;
    private static TextField numInfectedPeopleTextField;
    private static Slider simulationSpeedSlider;
    private static ListView<String> interactionsHistoryListView;
    private static AreaChart<String, Double> interactionsLineChart;
    private static CheckBox graphPopulationCheckBox;
    private static CheckBox passedTotalCheckBox;
    private static CheckBox infectedTotalCheckBox;
    private static CheckBox curedTotalCheckBox;
    private static CheckBox passedDailyCheckBox;
    private static CheckBox infectedDailyCheckBox;
    private static CheckBox curedDailyCheckBox;

    public static void init() {

        interactionView = View.getInteractionView();
        simulateButton = View.getSimulateButton();
        clearButton = View.getClearButton();
        stopButton = View.getStopButton();
        numStartPeopleTextField = View.getNumStartPeopleTextField();
        numInfectedPeopleTextField = View.getNumInfectedPeopleTextField();
        simulationSpeedSlider = View.getSimulationSpeedSlider();
        interactionsHistoryListView = View.getInteractionsHistoryListView();
        interactionsLineChart = View.getInteractionsLineChart();

        graphPopulationCheckBox = View.getPopulationCheckBox();
        passedTotalCheckBox = View.getPassedTotalCheckBox();
        infectedTotalCheckBox = View.getInfectedTotalCheckBox();
        curedTotalCheckBox = View.getCuredTotalCheckBox();
        passedDailyCheckBox = View.getPassedDailyCheckBox();
        infectedDailyCheckBox = View.getInfectedDailyCheckBox();
        curedDailyCheckBox = View.getCuredDailyCheckBox();

        numInfectedPeopleTextField.setOnKeyReleased(new EventHandler<KeyEvent>() {
            @Override
            public void handle(KeyEvent event) {
                String n = numInfectedPeopleTextField.getText();
                boolean isInt = Utilities.isInt(n);
                if (n.length() == 0 || isInt) {
                    numInfectedPeopleTextField.setStyle("-fx-text-inner-color: black;");
                }
                else {
                    numInfectedPeopleTextField.setStyle("-fx-text-inner-color: red;");
                }
            }
        });

        numStartPeopleTextField.setOnKeyReleased(new EventHandler<KeyEvent>() {
            @Override
            public void handle(KeyEvent event) {
                String n = numStartPeopleTextField.getText();
                boolean isInt = Utilities.isInt(n);
                if (n.length() == 0 || isInt) {
                    numStartPeopleTextField.setStyle("-fx-text-inner-color: black;");
                }
                else {
                    numStartPeopleTextField.setStyle("-fx-text-inner-color: red;");
                }
//                System.out.println("interactionView: " + interactionView + "\ninteractionView.getWidth(): " + interactionView.getWidth() + "\ninteractionView.getHeight(): " + interactionView.getHeight());
            }
        });

        simulateButton.setOnMouseClicked(event -> {
            System.out.println("sim button clicked");
            boolean validSim = checkValidSim();
            System.out.println("validSim: " + validSim);
//            System.out.println("Model's population:\n" + Model.getPopulation());
            if (validSim) {
                Model.setNumInfectedStart(getNumStartInfectedPeople());
                Model.setNumPeopleStart(getNumStartPeople());
                if (Model.getPopulation().size() == 0) {
//                    System.out.println("Model.getPopulation().size() == 0");
                    Model.createPopulation();
                }
                if (Model.getTimeLine().getStatus() == Animation.Status.STOPPED) {
//                    System.out.println("Model.getTimeLine().getStatus() == Animation.Status.STOPPED");
                    View.drawPopulation();
                }
                if (Model.getTimeLine().getStatus() != Animation.Status.RUNNING) {
//                    System.out.println("Model.getTimeLine().getStatus() != Animation.Status.RUNNING");
                    Model.playSim();
                }
            }
        });

        stopButton.setOnMouseClicked(event -> {
            System.out.println("stop button clicked");
            Model.stopSim();
        });

        clearButton.setOnMouseClicked(event -> {
            System.out.println("clear button clicked");
            Model.clearSim();
            interactionView.getChildren().clear();
            View.clearInteractionView();
            View.clearNewsList();
            View.clearStatsPane();
            View.clearLineChart();
            Model.setCurrentDate(DateHandler.getToday());
        });

        simulationSpeedSlider.setOnMouseClicked(event -> {
            Model.setDaysPerSecond(simulationSpeedSlider.getValue());
        });

        simulationSpeedSlider.setOnMouseDragged(event -> {
            Model.setDaysPerSecond(simulationSpeedSlider.getValue());
        });

        graphPopulationCheckBox.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                View.updateChart();
            }
        });

        passedTotalCheckBox.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                View.updateChart();
            }
        });

        passedDailyCheckBox.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                View.updateChart();
            }
        });

        curedTotalCheckBox.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                View.updateChart();
            }
        });

        curedDailyCheckBox.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                View.updateChart();
            }
        });

        infectedTotalCheckBox.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                View.updateChart();
            }
        });

        infectedDailyCheckBox.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                View.updateChart();
            }
        });
    }

    private static boolean checkValidSim() {
        if (Utilities.isInt(numStartPeopleTextField.getText())) {
            if (Utilities.isInt(numInfectedPeopleTextField.getText())) {
                int startPeople = getNumStartPeople();
                int startInfected = getNumStartInfectedPeople();
                if (startPeople > startInfected) {
                    return true;
                }
            }
        }
        return false;
    }

    public static int getNumStartPeople() {
        return Integer.parseInt(numStartPeopleTextField.getText());
    }

    public static int getNumStartInfectedPeople() {
        return Integer.parseInt(numInfectedPeopleTextField.getText());
    }

    public static void clickClearButton() {
        Event.fireEvent(
                clearButton,
                new MouseEvent(
                        MouseEvent.MOUSE_CLICKED,
                        clearButton.getLayoutX(), //sceneCoords.getX(),
                        clearButton.getLayoutY(), //sceneCoords.getY(),
                        0, //screenCoords.getX(),
                        0, //screenCoords.getY(),
                        MouseButton.PRIMARY,
                        1,
                        true,
                        true,
                        true,
                        true,
                        true,
                        true,
                        true,
                        true,
                        true,
                        true,
                        null));
    }
}

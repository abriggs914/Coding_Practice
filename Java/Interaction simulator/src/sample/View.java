package sample;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Bounds;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.geometry.Side;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.chart.AreaChart;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.*;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Line;

import java.util.ArrayList;
import java.util.Date;

public class View {

    private static Parent root;

    private static BorderPane borderPane;
    private static TextField timeView;
    private static Pane interactionView;
    private static Button simulateButton;
    private static Button clearButton;
    private static Button stopButton;
    private static TextField numStartPeopleTextField;
    private static TextField numInfectedPeopleTextField;
    private static Slider simulationSpeedSlider;
    private static ListView<String> interactionsHistoryListView;
    private static AreaChart<String, Double> interactionsLineChart;
    private static ScrollPane simSummaryPane;
    private static CheckBox stepSimCheckBox;
    private static CheckBox showPathsCheckBox;
    private static VBox graphButtonsVBox;
    private static CheckBox graphPopulationCheckBox;
    private static CheckBox passedTotalCheckBox;
    private static CheckBox infectedTotalCheckBox;
    private static CheckBox curedTotalCheckBox;
    private static CheckBox passedDailyCheckBox;
    private static CheckBox infectedDailyCheckBox;
    private static CheckBox curedDailyCheckBox;

    public View(Parent rootIn) {
        root = rootIn;

        borderPane = (BorderPane) root.lookup("#borderPane");
        double width = borderPane.getWidth();
        double height = borderPane.getHeight();
        interactionView = (Pane) root.lookup("#interaction_pane");
        timeView = (TextField) root.lookup("#time_view_pane");
        simulateButton = (Button) root.lookup("#simulate_button");
        clearButton = (Button) root.lookup("#clear_button");
        stopButton = (Button) root.lookup("#stop_button");
        numStartPeopleTextField = (TextField) root.lookup("#number_people_textField");
        numInfectedPeopleTextField = (TextField) root.lookup("#number_infected_textField");
        simulationSpeedSlider = (Slider) root.lookup("#speed_slider");
        interactionsHistoryListView = (ListView<String>) root.lookup("#interaction_listView");
        interactionsLineChart = (AreaChart<String, Double>) root.lookup("#interaction_lineChart");
        stepSimCheckBox = (CheckBox) root.lookup("#step_sim_checkBox");
        showPathsCheckBox = (CheckBox) root.lookup("#show_paths_checkBox");
        simSummaryPane = (ScrollPane) root.lookup("#sim_summary_scrollPane");
        graphButtonsVBox = (VBox) root.lookup("#graph_button_vBox");

        interactionView.setPrefSize(width * (2.0/3), height * (1.0/2));
        interactionView.setMaxSize(width * (2.0/3), height * (1.0/2));
        interactionView.setMinSize(width * (2.0/3), height * (1.0/2));
        interactionView.setStyle("-fx-border-color: black");

        interactionsHistoryListView.setPrefSize(width * (1.0/5), height * (1.0/3));
        interactionsHistoryListView.setMinSize(width * (1.0/5), height * (1.0/3));
        interactionsHistoryListView.setMaxSize(width * (1.0/5), height * (1.0/3));

        simSummaryPane.setPrefSize(width * (1.0/4), height * (1.0/3));
        simSummaryPane.setMinSize(width * (1.0/4), height * (1.0/3));
        simSummaryPane.setMaxSize(width * (1.0/4), height * (1.0/3));

        interactionsLineChart.setPrefSize(width * (3.0 / 4), height * (4.0 / 9));
        interactionsLineChart.setMinSize(width * (3.0 / 4), height * (4.0 / 9));
        interactionsLineChart.setMaxSize(width * (3.0 / 4), height * (4.0 / 9));
        interactionsLineChart.setAnimated(true);
        interactionsLineChart.setLegendSide(Side.TOP);

//        setTimeView();
        timeView.setStyle("-fx-background-color: black; -fx-text-inner-color: red;");

        clearStatsPane();
        initGraphButtons();
    }

    public static void initGraphButtons() {
        graphPopulationCheckBox = new CheckBox("Population");
        infectedDailyCheckBox = new CheckBox("Infected");
        infectedTotalCheckBox = new CheckBox("Infected");
        curedDailyCheckBox = new CheckBox("Cured");
        curedTotalCheckBox = new CheckBox("Cured");
        passedDailyCheckBox = new CheckBox("Passed");
        passedTotalCheckBox = new CheckBox("Passed");
        HBox dailyHBox = new HBox(curedDailyCheckBox, infectedDailyCheckBox, passedDailyCheckBox);
        HBox totalHBox = new HBox(graphPopulationCheckBox, curedTotalCheckBox, infectedTotalCheckBox, passedTotalCheckBox);
        Label dailyLabel = new Label("Daily");
        Label totalLabel = new Label("Total");
        VBox dailyVBox = new VBox(dailyLabel, dailyHBox);
        VBox totalVBox = new VBox(totalLabel, totalHBox);

        graphPopulationCheckBox.setPadding(new Insets(0, 10, 0, 10));
        curedDailyCheckBox.setPadding(new Insets(0, 10, 0, 10));
        curedTotalCheckBox.setPadding(new Insets(0, 10, 0, 10));
        infectedDailyCheckBox.setPadding(new Insets(0, 10, 0, 10));
        infectedTotalCheckBox.setPadding(new Insets(0, 10, 0, 10));
        passedDailyCheckBox.setPadding(new Insets(0, 10, 0, 10));
        passedTotalCheckBox.setPadding(new Insets(0, 10, 0, 10));

        dailyHBox.setPadding(new Insets(10,10,10,10));
        totalHBox.setPadding(new Insets(10,10,10,10));
        dailyVBox.setPadding(new Insets(10,10,10,10));
        totalVBox.setPadding(new Insets(10,10,10,10));
        dailyVBox.setAlignment(Pos.CENTER);
        totalVBox.setAlignment(Pos.CENTER);

        graphButtonsVBox.getChildren().addAll(totalVBox, dailyVBox);
    }

    public static void drawInteractionViewHitBounds() {
        Bounds bounds = interactionView.getLayoutBounds();
        double x1 = bounds.getMinX();
        double y1 = bounds.getMinY();
        double x2 = bounds.getWidth();
        double y2 = bounds.getHeight();
        Line east = new Line(x1, y1, x1, y2);
        Line north = new Line(x1, y1, x2, y1);
        Line west = new Line(x2, y1, x2, y2);
        Line south = new Line(x1, y2, x2, y2);
        Color lineColor = Color.YELLOW;
        east.setFill(lineColor);
        east.setStroke(lineColor);
        west.setFill(lineColor);
        west.setStroke(lineColor);
        south.setFill(lineColor);
        south.setStroke(lineColor);
        north.setFill(lineColor);
        north.setStroke(lineColor);
        interactionView.getChildren().addAll(north, west, south, east);
    }


    public static void setTimeView(Date date) {
        String dateString = DateHandler.getDateString(date);
        String timeString = DateHandler.getTimeString(date);
        timeView.setText(dateString + " - " + timeString);
    }

    public static Pane getInteractionView() {
        return interactionView;
    }

    public static Button getSimulateButton() {
        return simulateButton;
    }

    public static Button getClearButton() {
        return clearButton;
    }

    public static Button getStopButton() {
        return stopButton;
    }

    public static TextField getNumStartPeopleTextField() {
        return numStartPeopleTextField;
    }

    public static TextField getNumInfectedPeopleTextField() {
        return numInfectedPeopleTextField;
    }

    public static Slider getSimulationSpeedSlider() {
        return simulationSpeedSlider;
    }

    public static ListView<String> getInteractionsHistoryListView() {
        return interactionsHistoryListView;
    }

    public static AreaChart<String, Double> getInteractionsLineChart() {
        return interactionsLineChart;
    }

    public static CheckBox getPopulationCheckBox() {
        return graphPopulationCheckBox;
    }

    public static CheckBox getPassedTotalCheckBox() {
        return passedTotalCheckBox;
    }

    public static CheckBox getInfectedTotalCheckBox() {
        return infectedTotalCheckBox;
    }

    public static CheckBox getCuredTotalCheckBox() {
        return curedTotalCheckBox;
    }

    public static CheckBox getPassedDailyCheckBox() {
        return passedDailyCheckBox;
    }

    public static CheckBox getInfectedDailyCheckBox() {
        return infectedDailyCheckBox;
    }

    public static CheckBox getCuredDailyCheckBox() {
        return curedDailyCheckBox;
    }

    public static boolean isGraphingPopulation() {
        return graphPopulationCheckBox.isSelected();
    }

    public static boolean isGraphingCuredDaily() { return curedDailyCheckBox.isSelected(); }

    public static boolean isGraphingCuredTotal() { return curedTotalCheckBox.isSelected(); }

    public static boolean isGraphingPassedDaily() { return passedDailyCheckBox.isSelected(); }

    public static boolean isGraphingPassedTotal() { return passedTotalCheckBox.isSelected(); }

    public static boolean isGraphingInfectedDaily() { return infectedDailyCheckBox.isSelected(); }

    public static boolean isGraphingInfectedTotal() { return infectedTotalCheckBox.isSelected(); }

    public static boolean isSteppingSim() {
        return stepSimCheckBox.isSelected();
    }

    public static boolean isShowingPaths() {
        return showPathsCheckBox.isSelected();
    }

    public static void drawPopulation() {
        clearInteractionView();
        for (Person person : Model.getPopulation()) {
            Group circle = person.getCircleStack();
//            Label label = new Label(person.getIdString());
//            label.setLayoutX(circle.getLayoutX());
//            label.setLayoutY(circle.getLayoutY());
            interactionView.getChildren().add(circle);
        }
    }

    public static void clearInteractionView() {
        interactionView.getChildren().clear();
    }

    public static void clearNewsList() {
        interactionsHistoryListView.getItems().clear();
    }

    public static void clearStatsPane() {
        simSummaryPane.setContent(new Label("Run a simulation first."));
    }

    public static void clearLineChart() {
        interactionsLineChart.getData().clear();
    }

    public static void updateNewsList() {
        ArrayList<String> casePopulation = new ArrayList<>();
        Model.getCaseHistoryPopulation().forEach((p) -> casePopulation.add(p.toString() + " - " + p.getCauseOfDeath()));
        ObservableList<String> newsItems = FXCollections.observableArrayList(casePopulation);
        interactionsHistoryListView.setItems(newsItems);
    }

    public static void updateStatsPane() {
        int populationSize = Model.getNumPeopleStart();
        int infectedCount = Model.getNumInfectedCount();
        int curedCount = Model.getNumCuredCount();
        int deathCount = Model.getNumDeathCount();
        Date startDay = Model.getStartDate();
        Date today = Model.getCurrentDate();

        Label title = new Label("- Statistics -");

        Label firstDateTitleLabel = new Label("First date:");
        Label lastDateTitleLabel = new Label("Current date:");
        Label durationTitleLabel = new Label("Duration:");
        Label populationTitleLabel = new Label("Population:");
        Label infectedTitleLabel = new Label("Number infected:");
        Label curedTitleLabel = new Label("Number cured:");
        Label deathTitleLabel = new Label("Number deaths:");

        Label firstDateValueLabel = new Label(DateHandler.getFormattedString(startDay));
        Label lastDateValueLabel = new Label(DateHandler.getFormattedString(today));
        int duration = DateHandler.daysBetween(startDay, today);
        String daysString = ((duration != 1)? " days" : " day");
        Label durationValueLabel = new Label(duration + daysString);
        Label populationValueLabel = new Label(Integer.toString(populationSize));
        Label infectedValueLabel = new Label(Integer.toString(infectedCount));
        Label curedValueLabel = new Label(Integer.toString(curedCount));
        Label deathValueLabel = new Label(Integer.toString(deathCount));

        HBox startDateBox = new HBox(firstDateTitleLabel, firstDateValueLabel);
        HBox endDateBox = new HBox(lastDateTitleLabel, lastDateValueLabel);
        HBox durationDateBox = new HBox(durationTitleLabel, durationValueLabel);
        HBox populationBox = new HBox(populationTitleLabel, populationValueLabel);
        HBox infectedBox = new HBox(infectedTitleLabel, infectedValueLabel);
        HBox deathBox = new HBox(deathTitleLabel, deathValueLabel);
        HBox cureBox = new HBox(curedTitleLabel, curedValueLabel);
        VBox vBox = new VBox(title, startDateBox, endDateBox, durationDateBox, populationBox, infectedBox, deathBox, cureBox);
        vBox.setAlignment(Pos.TOP_CENTER);


        simSummaryPane.setContent(vBox);
        simSummaryPane.fitToWidthProperty().set(true);
        simSummaryPane.fitToHeightProperty().set(true);

        for (int j = 1; j < vBox.getChildren().size(); j++) {
            Node node = vBox.getChildren().get(j);
            HBox hBox = (HBox) node;
            hBox.setPrefWidth(simSummaryPane.getWidth());
            hBox.setMaxWidth(simSummaryPane.getWidth());
            hBox.setMinWidth(simSummaryPane.getWidth());
            hBox.setSpacing(10);
            hBox.setPadding(new Insets(5,25,5,25));
            ObservableList<Node> children = hBox.getChildren();
            for (int i = 0; i < children.size(); i += 2) {
                Label titleLabel = (Label) children.get(i);
                Label valueLabel = (Label) children.get(i + 1);
                titleLabel.setAlignment(Pos.CENTER_LEFT);
                valueLabel.setAlignment(Pos.CENTER_RIGHT);
            }
        }

    }

//    public static void drawPaths() {
////        clearInteractionView();
//        int numPathsToColor = 5;
//        for (Person person : Model.getPopulation()) {
//            ArrayList<Line> personPath = person.getPath();
//            for (int i = personPath.size() - 1; i >= 0; i--) {
//                Line path = personPath.get(i);
//                double red = (Math.max(0, numPathsToColor - i) * 0.2);
//                double green = 1 - (Math.max(0, numPathsToColor - i) * 0.2);
//                double blue = 0.03;
//                if (i >= numPathsToColor) {
//                    red = 0;
//                    green = 0;
//                    blue = 0;
//                }
//                Color lineColor = new Color(red, green, blue, 1.0);
//                path.setStroke(lineColor);
//                path.setStrokeWidth(3);
//                path.setFill(lineColor);
//                if (!interactionView.getChildren().contains(path)) {
//                    System.out.println("line: " + path);
//                    interactionView.getChildren().add(path);
//                }
//                else{
//                    System.out.println("duplicate: " + path);
//                }
//            }
//        }
//    }

    public static void drawPaths() {
        for (Person p : Model.getPopulation()) {
            drawPath(p);
        }
    }

    public static void drawPath(Person person){
        int numPathsToColor = 10;
        ArrayList<Line> personPath = person.getPath();
        int length = personPath.size() - 1;
//        System.out.println("personPath: " + personPath.size());
        for (int i = length; i >= Math.max(0, length - numPathsToColor); i--) {
            Line path = personPath.get(i);

            if (interactionView.getChildren().contains(path)) {
//                System.out.println("grabbing a line " + path);
                path = (Line) interactionView.getChildren().get(interactionView.getChildren().indexOf(path));
            }

//            System.out.println("\t\ti: " + i + "\tline: " + path);
            Color lineColor = calcLineColor(i, length, numPathsToColor, path);
            path.setStroke(lineColor);
            path.setFill(lineColor);
//                System.out.println("line: " + path);
            if (!interactionView.getChildren().contains(path)) {
                interactionView.getChildren().add(path);
            }
            //                System.out.println("duplicate: " + path);

        }
    }

    private static Color calcLineColor(int i, int length, int numPathsToColor, Line path) {
        length += 1;// Math.max(1, length);
        double red = (Math.max(0, i - (length - 1) + numPathsToColor) * (1.0 / numPathsToColor));
        double green = 1 - (Math.max(0, i - (length - 1) + numPathsToColor) * (1.0 / numPathsToColor));
        double blue = 0.03;
        path.setStrokeWidth(2);
        if (i < (length - numPathsToColor)) {
            red = 0;
            green = 0;
            blue = 0;
            path.setStrokeWidth(1);
        }
//        System.out.println("i: " + i + ", length: " + length + ", numPathsToColor: " + numPathsToColor + "\nred: " + red + ", green: " + green + ", blue: " + blue);
        Color lineColor = new Color(red, green, blue, 1.0);
        return lineColor;
    }

    public static void updateChart() {
        interactionsLineChart.getData().clear();
        PandemicHistory history = Model.getHistory();
        boolean graphPopulation = isGraphingPopulation();
        boolean graphTotalInfected = isGraphingInfectedTotal();
        boolean graphTotalCured = isGraphingCuredTotal();
        boolean graphTotalPassed = isGraphingPassedTotal();
        boolean graphDailyInfected = isGraphingInfectedDaily();
        boolean graphDailyCured = isGraphingCuredDaily();
        boolean graphDailyPassed = isGraphingPassedDaily();
        if (history == null) {
            System.out.println("History is NULL");
        }
        else {
            if (graphPopulation) {
                XYChart.Series<String, Double> population = history.getPopulationTotalSeries();
                population.setName("Population total");
                interactionsLineChart.getData().add(population);
            }
            if (graphTotalPassed) {
                XYChart.Series<String, Double> passed = history.getPassedTotalSeries();
                passed.setName("Passed total");
                interactionsLineChart.getData().add(passed);
            }
            if (graphDailyPassed) {
                XYChart.Series<String, Double> passed = history.getPassedDailySeries();
                passed.setName("Passed daily");
                interactionsLineChart.getData().add(passed);
            }
            if (graphTotalInfected) {
                XYChart.Series<String, Double> infected = history.getInfectedTotalSeries();
                infected.setName("Infected total");
                interactionsLineChart.getData().add(infected);
            }
            if (graphDailyInfected) {
                XYChart.Series<String, Double> infected = history.getInfectedDailySeries();
                infected.setName("Infected daily");
                interactionsLineChart.getData().add(infected);
            }
            if (graphTotalCured) {
                XYChart.Series<String, Double> cured = history.getCuredTotalSeries();
                cured.setName("Cured total");
                interactionsLineChart.getData().add(cured);
            }
            if (graphDailyCured) {
                XYChart.Series<String, Double> cured = history.getCuredDailySeries();
                cured.setName("Cured daily");
                interactionsLineChart.getData().add(cured);
            }
        }
    }
}

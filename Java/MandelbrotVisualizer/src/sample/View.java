package sample;

import javafx.geometry.Insets;
import javafx.geometry.Point2D;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.scene.shape.Polygon;

import java.util.ArrayList;

public class View extends BorderPane {

    public static final int TOP_HEIGHT = 80;
    public static final int TOP_WIDTH = 300;

    private Controller controller;
    private Model model;

    private Button visualize;
    private Button reset;

    private TextField multiplierTextfield;
    private TextField diameterTextfield;
    private TextField pointsOnCircleTextfield;

    private Label multiplierLabel;
    private Label diameterLabel;
    private Label pointsOnCircleLabel;
    private Label equationLabel;

    public View(int width, int height) {

        init(width, height);

        // force the field to be numeric only
        multiplierTextfield.textProperty().addListener((observable, oldValue, newValue) -> {
            if (!newValue.matches("\\d*")) {
                multiplierTextfield.setText(newValue.replaceAll("[^\\d]", ""));
            }
        });

        // force the field to be numeric only
        diameterTextfield.textProperty().addListener((observable, oldValue, newValue) -> {
            if (!newValue.matches("\\d*")) {
                diameterTextfield.setText(newValue.replaceAll("[^\\d]", ""));
            }
        });

        // force the field to be numeric only
        pointsOnCircleTextfield.textProperty().addListener((observable, oldValue, newValue) -> {
            if (!newValue.matches("\\d*")) {
                pointsOnCircleTextfield.setText(newValue.replaceAll("[^\\d]", ""));
            }
        });

        visualize.setOnMouseClicked(event -> controller.visualize(getValues()));
        reset.setOnMouseClicked(event -> controller.reset());
    }

    private void init(int width, int height) {
        this.setWidth(width);
        this.setHeight(height);

        this.controller = Main.controller;
        this.model = Main.model;

        initTopPanel();
        initCenterPanel();
    }

    private void initTopPanel() {
        visualize = new Button("SIM");
        reset = new Button("RESET");

        multiplierTextfield = new TextField();
        diameterTextfield = new TextField();
        pointsOnCircleTextfield = new TextField();

        multiplierLabel = new Label("Multiplier:");
        diameterLabel = new Label("Circle diameter:");
        pointsOnCircleLabel = new Label("# points on circle:");

        visualize.setMinWidth(50);
        reset.setMinWidth(50);

        multiplierTextfield.setMinWidth(60);
        diameterTextfield.setMinWidth(60);
        pointsOnCircleTextfield.setMinWidth(60);

        multiplierLabel.setMinWidth(65);
        diameterLabel.setMinWidth(85);
        pointsOnCircleLabel.setMinWidth(100);
    }

    private void initCenterPanel() {
        equationLabel = new Label("");
    }

    private int[] getValues() {
        String multiplierText = multiplierTextfield.getText();
        String diameterText = diameterTextfield.getText();
        String pointsText = pointsOnCircleTextfield.getText();
        return new int[] {
                validateInt(multiplierText),
                validateInt(diameterText),
                validateInt(pointsText)
        };
    }

    private int validateInt(String text) {
        return (checkInt(text)? Integer.parseInt(text) : 1);
    }

    private boolean checkInt(String text) {
        try {
            int i = Integer.parseInt(text);
            if (i <= 0) {
                throw new Exception("Integer value must be greater than 0.");
            }
            return true;
        }
        catch(Exception e) {
            return false;
        }
    }

    @Override
    public void layoutChildren() {
        layoutTopPanel();
        layoutCenterPanel();
    }

    public void layoutTopPanel() {
        HBox topPanel = new HBox();
        HBox multiplierHBox = new HBox();
        HBox diameterHBox = new HBox();
        HBox pointsHBox = new HBox();
        HBox simHBox = new HBox();

        multiplierHBox.getChildren().addAll(multiplierLabel, multiplierTextfield);
        multiplierHBox.setSpacing(5);

        diameterHBox.getChildren().addAll(diameterLabel, diameterTextfield);
        diameterHBox.setSpacing(5);

        pointsHBox.getChildren().addAll(pointsOnCircleLabel, pointsOnCircleTextfield);
        pointsHBox.setSpacing(5);

        simHBox.getChildren().addAll(visualize, reset);
        simHBox.setSpacing(5);

        topPanel.getChildren().addAll(multiplierHBox, diameterHBox, pointsHBox, simHBox);

        topPanel.setMinWidth(TOP_WIDTH);
        topPanel.setMinHeight(TOP_HEIGHT);
        topPanel.setMaxWidth(TOP_WIDTH);
        topPanel.setMaxHeight(TOP_HEIGHT);
        topPanel.setPrefWidth(TOP_WIDTH);
        topPanel.setPrefHeight(TOP_HEIGHT);

        topPanel.setSpacing(10);
        topPanel.setPadding(new Insets(15,5,15,5));

        this.setTop(topPanel);
    }

    private void layoutCenterPanel() {
        AnchorPane centerPanel = new AnchorPane();
        centerPanel.getChildren().add(equationLabel);

        //Circle circle = new Circle(model.getCircleDiameter() / 2);

        Polygon circle = model.getCircle();
        circle.setFill(Color.BLACK);
        circle.setStrokeWidth(1);
        circle.setStroke(Color.BLACK);

        centerPanel.getChildren().add(circle);
        centerPanel.setMinWidth(300);
        this.setCenter(centerPanel);
        this.getCenter().setLayoutX(100);
        this.getCenter().setLayoutY(TOP_HEIGHT);

        System.out.println("diameter: " + model.getCircleDiameter());
        System.out.println("CENTER: x: " + centerPanel.getLayoutX() + ", y: " + centerPanel.getLayoutY());
        System.out.println("border center x: " + this.getCenter().getLayoutX());
        System.out.println("border center y: " + this.getCenter().getLayoutY());

        Point2D[] pts = model.getPoints();
        AnchorPane a = (AnchorPane) this.getCenter();
        Circle back = new Circle(model.getOrigin().getX(), model.getOrigin().getY(), model.getCircleDiameter() / 2, Color.GREEN);
        back.setOpacity(0.4);
        a.getChildren().add(back);
        for (int i = 0; i < pts.length; i++) {
            Point2D p = pts[i];
            System.out.println("\t\tadding point: " + p);
            Circle c = new Circle(p.getX(), p.getY(), 5);
            c.setFill(Color.RED);
            a.getChildren().add(c);
        }

        ArrayList<Line> lines = model.genlinePoints();
        for (Line l : lines) {
            l.setStroke(Color.WHITE);
            l.setStrokeWidth(1);
            a.getChildren().add(l);
        }
        this.setCenter(a);
    }

    public void drawPoints(Point2D[] pts) {
    }

    public void setEquation(String equation) {
        equationLabel.setText(equation);
    }
}

package sample;

import javafx.geometry.Point2D;

public class Controller {

    private Model model;
    private View view;

    Controller() {
        model = Main.model;
        view = Main.view;
    }

    void visualize(int[] values) {
        System.out.println("VISUALIZE");
        int multiplier = values[0];
        int diameter = values[1];
        int pointsOnCircle = values[2];
        model.setMultiplier(multiplier);
        model.setCircleDiameter(diameter);
        model.setPointsOnCircle(pointsOnCircle);

        Point2D origin = model.getOrigin();
        Point2D[] points = model.genPoints(diameter, pointsOnCircle, origin);
        model.setCircle(points);

        generateEquation();
//        view.drawPoints(points);
//        Double[] linePoints = model.genlinePoints();
    }

    void reset() {
        System.out.println("RESET");
        model.setMultiplier(1);
        model.setCircleDiameter(1);
        model.setPointsOnCircle(1);

        Point2D origin = model.getOrigin();
        Point2D[] points = model.genPoints(model.getCircleDiameter(), model.getPointsOnCircle(), origin);
        model.setCircle(points);

        generateEquation();
//        view.drawPoints(points);
    }

    private void generateEquation() {
        String equation = "z^" + model.getMultiplier() + " + C";
        if (view == null) {
            System.out.println("view is null");
            view = Main.view;
        }
        else {
            view.setEquation(equation);
        }
    }
}

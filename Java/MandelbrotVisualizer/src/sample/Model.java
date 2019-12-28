package sample;

import javafx.geometry.Point2D;
import javafx.scene.shape.Line;
import javafx.scene.shape.Polygon;

import java.util.ArrayList;


public class Model {

    private int multiplier;
    private int pointsOnCircle;

    private int circleDiameter;
    private double spaceBetweenPoints;

    private Polygon circle;
    private Point2D origin;

    public Model() {
        this.circle = new Polygon();

        this.origin = new Point2D(175, View.TOP_HEIGHT + 90);
    }

    /**
     * Calculate the space between each point of the circle.
     * @param diameter diameter of the given circle
     * @param numPoints number of desired points
     * @return distance between each point
     */
    private double computeSpaceBetweenPoints(int diameter, int numPoints) {
        double circumference = diameter * Math.PI; // 2*pi*r
        return circumference / numPoints;
    }

    private double anglePerSlice(int numSlices) {
        return ((numSlices == 0)? 360 : 360.0 / numSlices);
    }

    public Point2D[] genPoints(int diameter, int numPoints, Point2D origin) {
        Point2D[] res = new Point2D[numPoints];
        double degrees = 0;
        double degreesPerSlice = Math.round(anglePerSlice(numPoints));
        double oX = origin.getX(), oY = origin.getY(), x, y;
        double r = diameter / 2;
        for(int i = 0; i < numPoints; i++) {
            System.out.println("\tdegreesPerSlice:" + degreesPerSlice + ", degrees: " + degrees);
            x = (-1 * r * Math.cos(Math.toRadians(degrees))) + oX;
            y = (-1 * r * Math.sin(Math.toRadians(degrees))) + oY;
            res[i] = new Point2D(x, y);
            System.out.println("\tpoint: " + i + ": " + res[i]);
            degrees += degreesPerSlice;
        }
//        System.out.println(Arrays.toString(res));
//        System.out.println(res.length);
        return res;
    }

    public ArrayList<Line> genlinePoints() {
        ArrayList<Line> lines = new ArrayList<>();
        ArrayList<Integer> valuesChecked = new ArrayList<>();
        double x1, y1, x2, y2;
        Point2D[] pts = getPoints();
        for (int i = 0; i < pointsOnCircle; i++) {
            int rem = (i * multiplier) % pointsOnCircle;
            Point2D p1 = pts[i];
            Point2D p2 = pts[rem];
            x1 = p1.getX();
            y1 = p1.getY();
            x2 = p2.getX();
            y2 = p2.getY();
            Line line1 = new Line(x1, y1, x2, y2);
            Line line2 = new Line(x2, y2, x1, y1);
            while (!lines.contains(line1) && !lines.contains(line2)) {
                System.out.println("\tCONNECTING " + i + " to " + rem + ".");
                lines.add(line1);
                System.out.println("rem: " + rem);
                valuesChecked.add(rem);
                if (!valuesChecked.contains(i)) {
                    valuesChecked.add(i);
                }
            }
        }
//        System.out.println("\n\n\t\tRES points for lines:\n" + Arrays.toString(res));
        return lines;
    }

    public Point2D[] getPoints() {
        return genPoints(circleDiameter, pointsOnCircle, origin);
    }

    public int getMultiplier() {
        return multiplier;
    }

    public void setMultiplier(int multiplier) {
        this.multiplier = multiplier;
    }

    public int getPointsOnCircle() {
        return pointsOnCircle;
    }

    public void setPointsOnCircle(int pointsOnCircle) {
        this.pointsOnCircle = pointsOnCircle;
    }

    public int getCircleDiameter() {
        return circleDiameter;
    }

    public void setCircleDiameter(int circleDiameter) {
        this.circleDiameter = circleDiameter;
    }

    public double getSpaceBetweenPoints() {
        return spaceBetweenPoints;
    }

    public void setSpaceBetweenPoints(double spaceBetweenPoints) {
        this.spaceBetweenPoints = spaceBetweenPoints;
    }

    public void setCircle(Point2D[] points) {
        Double[] pts = new Double[points.length * 2];
        int i = 0;
        for (Point2D p : points) {
            pts[i++] = p.getX();
            pts[i++] = p.getY();
        }
        this.circle.getPoints().clear();
        this.circle.getPoints().addAll(pts);
    }

    public Polygon getCircle() {
        return circle;
    }

    public void setOrigin(Point2D pt) {
        this.origin = pt;
    }

    public Point2D getOrigin() {
        return origin;
    }
}

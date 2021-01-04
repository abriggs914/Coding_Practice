package sample;

import javafx.scene.canvas.Canvas;
import javafx.scene.shape.Rectangle;

import java.math.BigDecimal;
import java.math.MathContext;
import java.util.ArrayList;

public class Curve {

    private final double GRAVITY = 9.8;

    private double x1;
    private double y1;
    private double x2;
    private double y2;
    private double duration;
    private MathContext mathContext;

    private int segments;
    private ArrayList<BigDecimal[]> points;

    public Curve(double x1, double y1, double x2, double y2, int segments, boolean downHill) {

        // Ensures that the slope of the curve will be negative.
        // A ball shouldn't roll up-hill.
        if (downHill) {
            double ym = ((Math.max(y1, y2) == y1)? y1 : y2);
            double xm = ((Math.max(y1, y2) == y1)? x1 : x2);
            x2 = ((Math.max(y1, y2) == y1)? x2 : x1);
            y2 = ((Math.max(y1, y2) == y1)? y2 : y1);
            x1 = xm;
            y1 = ym;
        }

        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
        this.segments = segments;
        this.mathContext = new MathContext(100);
    }

    public void draw(Canvas canvas) {
        System.out.println("Please overwrite this method in the subclass");
    }

    public String getEquation() {
        return "Please overwrite this method in the subclass";
    }

    public ArrayList<BigDecimal[]> getPoints() {
        return points;
    }

    public int getSegments() {
        return segments;
    }

    public double getX1() {
        return x1;
    }

    public double getY1() {
        return y1;
    }

    public double getX2() {
        return x2;
    }

    public double getY2() {
        return y2;
    }

    public double getXSpan() {
        return Math.abs(x2 - x1);
    }

    public double getYSpan() {
        return Math.abs(y2 - y1);
    }

    public Rectangle getBounds() {
        double x = Math.min(x1, x2);
        double y = Math.max(y1, y2);
        return new Rectangle(x, y, getXSpan(), getYSpan());
    }

    public double getDuration() {
        return duration;
    }

    public double getGravity() {
        return GRAVITY;
    }

    public MathContext getMathContext() {
        return mathContext;
    }

    public BigDecimal[] getPointAtT(double t) {
        return new BigDecimal[] {BigDecimal.ZERO, BigDecimal.ZERO};
    }

    public void setPoints(ArrayList<BigDecimal[]> points) {
        this.points = new ArrayList<>(points);
    }

    public void setDuration(double d) {
        this.duration = d;
    }

//    public void setSegments(int segments) {
//        this.segments = segments;
//    }
//
//    public void setX1(double x1) {
//        this.x1 = x1;
//    }
//
//    public void setY1(double y1) {
//        this.y1 = y1;
//    }
//
//    public void setX2(double x2) {
//        this.x2 = x2;
//    }
//
//    public void setY2(double y2) {
//        this.y2 = y2;
//    }

//    public ArrayList<Double[]> getBrachistochronePoints() {
//        ArrayList<Double[]> points = new ArrayList<>();
//        for (Double theta : thetas) {
//            points.add(brachistochrone(theta));
//        }
//        return points;
//    }

//    public Double[] brachistochrone(double theta) {
//        //x = a(θ − sinθ) + x0
//        //y = −a(1 − cosθ) + y0
//        double x = (wheelRadius * (Math.toRadians(theta) - (Math.sin(Math.toRadians(theta))))) + x1;// + circle.getMidX();
//        double y = ((1 * wheelRadius) * (1 - (Math.cos(Math.toRadians(theta))))) + y1; //+ circle.getMidY();
////        return rotatePoint(circle.getMidX(), circle.getMidY(), x, y, 180);
//        return new Double[] {x, y};
//    }

//    public ArrayList<Double> getThetas() {
//        return thetas;
//    }

    // Rotate a 2D point about the origin a given amount of degrees
//    public Double[] rotateOnOrigin(double px, double py, double theta) {
//        // x′ = x * cos(θ) - y * sin(θ)
//        // y′ = x * sin(θ) + y * cos(θ)
//        double t = Math.toRadians(theta);
//        double x = (px * Math.cos(t)) - (py * Math.sin(t));
//        double y = (px * Math.sin(t)) + (py * Math.cos(t));
//        return new Double[]{x, y};
//    }
//
//    public Double[] rotatePoint(double cx, double cy, double px, double py, double theta) {
//        double xd = 0 - cx;
//        double yd = 0 - cy;
//        Double[] rxry = rotateOnOrigin(px + xd, py + yd, theta);
////        System.out.println("cx: " + cx + ", cy: " + cy);
////        System.out.println("px: " + px + ", py: " + py);
////        System.out.println("px - xd:" + (px - xd) + ", py - yd:" + (py - yd));
////        System.out.println("xd: " + xd + ", yd: " + yd);
////        System.out.println("rx: " + rxry[0] + ", ry: " + rxry[1]);
////        System.out.println("rx - xd: " + (rxry[0] - xd) + ", ry - yd: " + (rxry[1] - yd));
////        System.out.println("theta: " + theta);
//        return new Double []{rxry[0] - xd, rxry[1] - yd};
//    }
//
//    public Circle getCircle() {
//        return circle;
//    }
}

package sample;

import javafx.geometry.Point2D;

public class Vector {

    private double x1;
    private double y1;
    private double x2;
    private double y2;
    private double angle;
    private double magnitude;

    // Given angle and size
    public Vector(double angle, double magnitude) {
        this.angle = angle;
        this.magnitude = magnitude;

        this.x1 = 0;
        this.y1 = 0;
        reCalcPoint2();
    }

    // Given 2 points
    public Vector(double x1, double y1, double x2, double y2) {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;

        reCalcAngle();
        reCalcMagnitude();
    }

    // Re-calculators for when an attribute is adjusted

    public void reCalcAngle() {
        this.angle = Math.atan(Math.abs(y2 - y1) / Math.abs(x2 - x1));
    }

    public void reCalcMagnitude() {
        this.magnitude = Math.sqrt(Math.pow((x2 - x1), 2) + Math.pow((y2 - y1), 2));
    }

    public void reCalcPoint2() {
        this.x2 = x1 + (Math.cos(Math.toRadians(angle)) * magnitude);
        this.y2 = y1 + (Math.sin(Math.toRadians(angle)) * magnitude);
    }

    // Setters

    public void setX1(double x1) {
        this.x1 = x1;
        reCalcAngle();
        reCalcMagnitude();
//        reCalcPoint2();
    }

    public void setY1(double y1) {
        this.y1 = y1;
        reCalcAngle();
        reCalcMagnitude();
//        reCalcPoint2();
    }

    public void setX2(double x2) {
        this.x2 = x2;
        reCalcAngle();
        reCalcMagnitude();
    }

    public void setY2(double y2) {
        this.y2 = y2;
        reCalcAngle();
        reCalcMagnitude();
    }

    public void setAngle(double angle) {
        this.angle = angle;
        reCalcPoint2();
    }

    public void setMagnitude(double magnitude) {
        this.magnitude = magnitude;
        reCalcPoint2();
    }

    // Getters

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

    public double getAngle() {
        return angle;
    }

    public double getMagnitude() {
        return magnitude;
    }

    public double getXComponent() {
        return Math.abs(x2 - x1);
    }

    public double getYComponent() {
        return Math.abs(y2 - y1);
    }

    public Point2D getPoint1() {
        return new Point2D(x1, y1);
    }

    public Point2D getPoint2() {
        return new Point2D(x2, y2);
    }

    // Mathematical operations

    public void add(Vector v) {
        this.x2 += v.getXComponent();
        this.y2 += v.getYComponent();
        reCalcAngle();
        reCalcMagnitude();
    }

    public String toString() {
        return "Vector (" + x1 + ", " + y1 +") -> (" + x2 + ", " + y2 + ") angle: " + angle + ", magnitude: " + magnitude;
    }
}

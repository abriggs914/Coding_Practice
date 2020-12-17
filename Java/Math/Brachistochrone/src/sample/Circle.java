package sample;

import javafx.geometry.Point2D;

public class Circle {

    private double x1;
    private double y1;
    private double x2;
    private double y2;

    private double h; // midpoint x
    private double k; // midpoint y
    private double r; // radius
    private double a; // interior angle
    private double s; // arc length

    public Circle(double x1, double y1, double x2, double y2) {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;

        this.h = (x1 + x2) / 2;
        this.k = (y1 + y2) / 2;
        this.a = this.calcAngle();

        // r^2 = (x - h)^2 + (y - k)^2
        this.r = distance(x2, y2, h, k); // Math.sqrt(((x2 - h) * (x2 - h)) + ((y2 - k) * (y2 - k)));

        // L = r * θ
        this.s = r * a;
    }

    public double calcAngle() {
        // t = cos^-1(a / h)
        double hypotenuse1 = distance(x1, y1, 0, 0);
        double adjacent1 = distance(0, 0, x1, 0);
        double theta1 = Math.acos((adjacent1 / hypotenuse1)) * (180 / Math.PI);

        // t = cos^-1(a / h)
        double hypotenuse2 = distance(x2, y2, 0, 0);
        double adjacent2 = distance(0, 0, x2, 0);
        double theta2 = Math.acos((adjacent2 / hypotenuse2)) * (180 / Math.PI);

//        if (x1 == 0) {
//            theta1 = 90;
//        }
//        if (y1 == 0) {
//            theta1 = 0;
//        }
//        if (x2 == 0) {
//            theta2 = 90;
//        }
//        if (y2 == 0) {
//            theta2 = 0;
//        }

        double angle = Math.abs(theta2 - theta1);

        System.out.println("x1: " + x1 + ", y1: " + y1 + ", x2: " + x2 + ", y2: " + y2 + "\nhypoteneuse1: " + hypotenuse1 + ", adjacent1: " + adjacent1 + ", theta1: " + theta1 + "\nhypoteneuse2: " + hypotenuse2 + ", adjacent2: " + adjacent2 + ", theta2: " + theta2 + "\nangle: " + angle);


        if (angle == 0) {
            if (x1 != x2 || y1 != y2) {
                angle = 180;
            }
        }
        return angle;
    }

    public static double distance(double x1, double y1, double x2, double y2) {
        return Math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)));
    }

    public double getMidX() {
        return h;
    }

    public double getMidY() {
        return k;
    }

    public Point2D getMidPoint() {
        return new Point2D(this.getMidX(), this.getMidY());
    }

    public double getRadius() {
        return r;
    }

    public double getArcLength() {
        return s;
    }

    public double getAngle() {
        return a;
    }

    public double getChord() {
        return this.distance(x1, y1, x2, y2);
    }

    public String toString() {
        return "<Circle: (x - " + h + ")^2 + (y - " + k + ")^2 = " + r +"^2, a=" + a + ", s=" + s + ", M=(" + h + ", " + k + ")>";
    }
}

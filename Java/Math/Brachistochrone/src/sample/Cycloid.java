package sample;

import javafx.geometry.Point2D;

import java.math.BigDecimal;
import java.util.ArrayList;

public class Cycloid extends Curve implements CurveCreator{

    public Cycloid(double x1, double y1, double x2, double y2, int segments, boolean downHill) {
        super(x1, y1, x2, y2, segments, downHill);

        init();
    }

    public void init() {
        this.setPoints(calcPoints());
    }

    // Return the h, k, and r values of the circle formula
    public BigDecimal[] calcCirclePoints(double x, double y, double hypotenuse) {
        double r = Math.acos(Math.toRadians(45)) * hypotenuse;
//        BigDecimal[] points = new BigDecimal[3];
        return new BigDecimal[] {BigDecimal.valueOf(-x), BigDecimal.valueOf(-y), BigDecimal.valueOf(r)};
    }

    public int numIntersections() {
        double hypotenuse = Math.sqrt(Math.pow((this.getY2() - this.getY1()), 2) + Math.pow((this.getX2() - this.getX1()), 2));
        double r0 = Math.sin(Math.toRadians(45)) * hypotenuse;
        double r1 = Math.cos(Math.toRadians(45)) * hypotenuse;
        double sumR0R1 = r0 + r1;
        boolean tooFar = hypotenuse > sumR0R1; // No intersection - Too far away.
        boolean contains = hypotenuse < Math.abs(r0 - r1); // No intersection - Inside one another.
        boolean equal = hypotenuse == 0 && r0 == r1; // Circles are the same.
        // No intersection - Too far away.
        if (tooFar || contains || equal) {
            return 0;
        }
        // 1 intersection
        else if (hypotenuse == (r0 + r1)) {
            return 1;
        }
        // 2 intersections
        else {
            return 2;
        }
    }

    @Override
    // With use of the formula described here:
    // http://csharphelper.com/blog/2014/09/determine-where-two-circles-intersect-in-c/
    public ArrayList<BigDecimal[]> calcPoints() {
        ArrayList<BigDecimal[]> points = new ArrayList<>();
        double distance = Math.sqrt(Math.pow((this.getY2() - this.getY1()), 2) + Math.pow((this.getX2() - this.getX1()), 2));
        double r0 = Math.sin(Math.toRadians(45)) * distance;
        double r1 = Math.cos(Math.toRadians(45)) * distance;
        int intersections = numIntersections();
        System.out.println("\n\n(" + this.getX1() + ", " + this.getY1() + "), (" + this.getX2() + ", " + this.getY2() + "), ");
        System.out.println("distance: " + distance + "\nr0: " + r0 + "\nr1: " + r1 + "\nintersections: " + intersections);

        BigDecimal[] p1Circle = calcCirclePoints(this.getX1(), this.getY1(), distance);
        BigDecimal[] p2Circle = calcCirclePoints(this.getX2(), this.getY2(), distance);

        if (intersections > 0) {
            double a = (Math.pow(r0, 2) + Math.pow(distance, 2) - Math.pow(r1, 2)) / (2 * distance);
            double h = Math.sqrt(Math.pow(r0, 2) - Math.pow(a, 2));
            double centerX = this.getX1() + a * (this.getX2() - this.getX1()) / distance;
            double centerY = this.getY1() + a * (this.getY2() - this.getY1()) / distance;

            double p3X = centerX - h * (this.getY2() - this.getY1()) / distance;
            double p3Y = this.getY1() - (centerY + h * (this.getX2() - this.getX1()) / distance) + this.getY2();
            System.out.println("P3: " + new Point2D(p3X, p3Y));

            int s = this.getSegments();
            double angleRange = 90;
            double angleSegments = angleRange / s;
            double opp = (this.getY1() - ((this.getY1() + this.getY2()) - p3Y));
            double adj = Math.abs(p3X - this.getX1());
            double start = Math.toDegrees(Math.atan(opp / adj));
            double startAngle = 180 - start;
            double endAngle = (startAngle + angleRange) % 360;


//            double angle = (360 - startAngle) % 360;
            double angle = (360 - endAngle) % 360;
            System.out.println("start: " + start + ", angle: " + angle + "\ns: " + s + "\nangleSegments: " + angleSegments);
            for (int i = 0; i <= s; i += 1) {
//                System.out.println("\tangle: " + angle + "\nMath.cos(Math.toRadians(angle)): " + Math.cos(Math.toRadians(angle)) + "\nMath.sin(Math.toRadians(angle)): " + Math.sin(Math.toRadians(angle)));
                BigDecimal x = BigDecimal.valueOf((r0 * Math.cos(Math.toRadians(angle))) + p3X);
                BigDecimal y = BigDecimal.valueOf((r0 * Math.sin(Math.toRadians(angle))) + p3Y);
                points.add(new BigDecimal[] {x, y});
                angle += angleSegments;
            }
            System.out.println("opp: " + opp + ", adj: " + adj + "\n\tstart: " + startAngle + " -> end: " + endAngle);
//            points = new ArrayList<>(Collections.singletonList(new BigDecimal[] {BigDecimal.valueOf(p3X), BigDecimal.valueOf(p3Y)}));
//            points.add(new BigDecimal[] {BigDecimal.valueOf(p3X), BigDecimal.valueOf(p3Y)});
        }
        return points;
    }

    @Override
    public double calcDuration() {
        //TODO non 0
        return 0;
    }

    @Override
    public String toString() {
        return "Cycloid";
    }

    @Override
    public String getEquation() {
        double distance = Math.sqrt(Math.pow((this.getY2() - this.getY1()), 2) + Math.pow((this.getX2() - this.getX1()), 2));
        double r0 = Math.sin(Math.toRadians(45)) * distance;
        double r1 = Math.cos(Math.toRadians(45)) * distance;
        double a = (Math.pow(r0, 2) + Math.pow(distance, 2) - Math.pow(r1, 2)) / (2 * distance);
        double h = Math.sqrt(Math.pow(r0, 2) - Math.pow(a, 2));
        double centerX = this.getX1() + a * (this.getX2() - this.getX1()) / distance;
        double centerY = this.getY1() + a * (this.getY2() - this.getY1()) / distance;
        double p3X = centerX - h * (this.getY2() - this.getY1()) / distance;
        double p3Y = this.getY1() - (centerY + h * (this.getX2() - this.getX1()) / distance) + this.getY2();
        double opp = (this.getY1() - ((this.getY1() + this.getY2()) - p3Y));
        double adj = Math.abs(p3X - this.getX1());
        double start = Math.toDegrees(Math.atan(opp / adj));
        double startAngle = 180 - start;
        double angleRange = 90;
        double endAngle = (startAngle + angleRange) % 360;
        double angle = (360 - endAngle) % 360;
        String xEquation = "(" + r0 + " * cos(" + angle + ") + " + p3X;
        String yEquation = "(" + r0 + " * sin(" + angle + ") + " + p3Y;
        return xEquation + "\n" + yEquation;
    }

    @Override
    public BigDecimal[] getPointAtT(double t) {
        return new BigDecimal[] {
                BigDecimal.valueOf(XPointAtT(t)),
                BigDecimal.valueOf(YPointAtT(t))
        };
    }

    @Override
    public double XPointAtT(double t) {
        //TODO non 0
        return 0;
    }

    @Override
    public double YPointAtT(double t) {
        //TODO non 0
        return 0;
    }
}

package sample;

import java.math.BigDecimal;
import java.util.ArrayList;

public class Parabolic extends Curve implements CurveCreator{

    public Parabolic(double x1, double y1, double x2, double y2, int segments, boolean downHill) {
        super(x1, y1, x2, y2, segments, downHill);

        init();
    }

    public void init() {
        this.setPoints(calcPoints());
    }

    public BigDecimal equation(double x) {
        // Set point2 as the vertex and calculate on e arm of the parabola.
        double deltaY = Math.abs(this.getY1() - this.getY2());
        double h = this.getX2();
        double k = this.getY2();
        double a = deltaY / (Math.pow(this.getX1(), 2) - (2 * this.getX1() * h) + Math.pow(h, 2));
        System.out.println("h: " + h + ", k: " + k + ", a: " + a + ", y: " + ((a * Math.pow((x - h), 2)) + k));
        return BigDecimal.valueOf((-a * Math.pow((x - h), 2)) + this.getY1());
//        double deltaX = 0 - this.getX1();
//        System.out.println("this.getY1(): " + this.getY1());
//        System.out.println("this.getY2(): " + this.getY2());
//        System.out.println("this.getX2(): " + this.getX2());
//        System.out.println("deltaX: " + deltaX);
//        System.out.println("this.getX2() + this.getX2() + deltaX: " + (this.getX2() + this.getX2() + deltaX));
//        System.out.println("Math.pow((this.getX2() + deltaX), 2): " + Math.pow((this.getX2() + deltaX), 2));
//        System.out.println("this.getY1() / Math.pow((this.getX2() + deltaX), 2): " + (this.getY1() / Math.pow((this.getX2() + deltaX), 2)));
//        System.out.println("(Math.pow(x, 2): " + Math.pow(x, 2));
//        System.out.println("(Math.pow(x, 2) * (this.getY1() / Math.pow((this.getX2() + deltaX), 2)): " + (Math.pow(x, 2) * (this.getY1() / Math.pow((this.getX2() + deltaX), 2))));
//        System.out.println("this.getY2() + (Math.pow(x, 2) * Math.abs(this.getY1() / Math.pow((this.getX2() + deltaX), 2))): " + (this.getY2() + (Math.pow(x, 2) * Math.abs(this.getY1() / Math.pow((this.getX2() + deltaX), 2)))));
//        System.out.println("y = x^2 * " + this.getY2() + " / (" + this.getX2() + ")^2" );
////        System.out.println(this.getY2() + (Math.pow(x, 2) * Math.abs(this.getY1() / Math.pow((this.getX2() + deltaX), 2))));
//        return BigDecimal.valueOf(this.getY2() + (Math.pow(x, 2) * Math.abs(this.getY1() / Math.pow((this.getX2() + deltaX), 2))));
    }

    @Override
    public String getEquation() {
        double deltaY = Math.abs(this.getY1() - this.getY2());
        double h = this.getX2();
        double k = this.getY2();
        double a = -deltaY / (Math.pow(this.getX1(), 2) - (2 * this.getX1() * h) + Math.pow(h, 2));
        return "y = " + a + "(x - " + h + ")^2 + " + k;
    }

    @Override
    public ArrayList<BigDecimal[]> calcPoints() {
        ArrayList<BigDecimal[]> points = new ArrayList<>();
        int s = this.getSegments();
        double xRange = this.getX2() - this.getX1();
        double xIncrement = xRange / s;

        for (double x = this.getX1(); x <= this.getX2(); x += xIncrement) {
            BigDecimal yV = equation(x);
            BigDecimal xV = BigDecimal.valueOf(x);
            System.out.println("(xV, yV): (" + xV + ", " + yV + ")");
            points.add(new BigDecimal[] {xV, yV});
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
        return "Parabolic";
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

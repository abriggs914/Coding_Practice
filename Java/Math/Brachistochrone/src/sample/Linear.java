package sample;

import java.math.BigDecimal;
import java.util.ArrayList;

public class Linear extends Curve implements CurveCreator{

    public Linear(double x1, double y1, double x2, double y2, int segments, boolean downHill) {
        super(x1, y1, x2, y2, segments, downHill);

        init();
    }

    public void init() {
        setPoints(calcPoints());
        setDuration(calcDuration());
    }

    @Override
    public ArrayList<BigDecimal[]> calcPoints() {
        double xd = this.getX2() - this.getX1();
        double yd = this.getY2() - this.getY1();
        ArrayList<BigDecimal[]> points = new ArrayList<>();
        if (xd == 0) {
            // vertical line
        }
        else {
            double m = -(this.getY2() - this.getY1()) / xd;
            double b = this.getY1() - (this.getX2() * m);
            int s = this.getSegments();
            double xRange = this.getX2() - this.getX1();
            double xIncrement = xRange / s;
            for (double x = this.getX1(); x < this.getX2(); x += xIncrement) {
                points.add(new BigDecimal[] {BigDecimal.valueOf(x), BigDecimal.valueOf((m * x) + b)});
            }
        }
        return points;
    }

    @Override
    public double calcDuration() {
        double dx = Math.abs(this.getX2() - this.getX1());
        double dy = Math.abs(this.getY2() - this.getY1());
        double d = Math.sqrt(Math.pow(dy, 2) + Math.pow(dx, 2));
        return Math.sqrt(2 / getGravity()) * (d / Math.sqrt(dy));
    }

    @Override
    public String getEquation() {
        double xd = this.getX2() - this.getX1();
        double m = (this.getY2() - this.getY1()) / xd;
        double b = this.getY1() - (this.getX2() * m);
        return "y = " + m + "x + " + b;
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
        double h = (t / Math.sqrt(2 / getGravity())) * Math.sqrt(getYSpan());
        double a = Math.toDegrees(Math.atan(getXSpan() / getYSpan()));
        return (Math.sin(Math.toRadians(a)) * h) + this.getX1();
    }

    @Override
    public double YPointAtT(double t) {
        double h = (t / Math.sqrt(2 / getGravity())) * Math.sqrt(getYSpan());
        double a = Math.toDegrees(Math.atan(getXSpan() / getYSpan()));
        return (Math.cos(Math.toRadians(a)) * h) + this.getY1();
    }

    @Override
    public String toString() {
        return "Linear";
    }
}

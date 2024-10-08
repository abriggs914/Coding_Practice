package sample;

import BigMath.BigDecimalMath;

import java.math.BigDecimal;
import java.math.MathContext;
import java.util.ArrayList;
import java.util.Arrays;

public class Brachistochrone extends Curve implements CurveCreator{

    private BigDecimal xVal;
    private BigDecimal yVal;
    private BigDecimal radius;
    private BigDecimal theta;

    public Brachistochrone(double x1, double y1, double x2, double y2, int segments, boolean downHill) {
        super(x1, y1, x2, y2, segments, downHill);

        init();
    }

    public void init() {
        this.xVal = calXVal();
        this.yVal = calYVal();
        this.theta = calcTheta(getXVal(), getYVal());
        System.out.println("calculated theta: " + theta);
        this.radius = calcRadius();
        System.out.println("calculated radius: " + radius);
        this.setPoints(calcPoints());
        this.setDuration(calcDuration());
    }

    public BigDecimal calcRadius() {
        System.out.println("THETA: " + getTheta());
        MathContext mathContext = getMathContext();
//        BigDecimal deltaY = new BigDecimal(0 - this.getY1());
//        BigDecimal yVal = new BigDecimal(this.getY2());
//        yVal = yVal.abs().add(deltaY);
        BigDecimal yVal = getYVal();
        System.out.println("yVal: " + yVal);
        return (yVal.divide(BigDecimal.ONE.subtract(BigDecimalMath.cos(this.getTheta(), mathContext)), BigDecimal.ROUND_HALF_DOWN)).abs();
    }

    public BigDecimal calcTheta(BigDecimal xVal, BigDecimal yVal) {
//        System.out.println("non_zero: " + nonZeroBisectionOnT(new BigDecimal(-360), new BigDecimal(360), xVal, yVal, 25));

        return nonZeroBisectionOnT(BigDecimal.valueOf(-360), BigDecimal.valueOf(360), xVal, yVal, 25);
    }

    public BigDecimal nonZeroBisectionOnT(BigDecimal low, BigDecimal high, BigDecimal xVal, BigDecimal yVal, int times) {
        if (bigDecimalInRange(low, BigDecimal.ZERO, high)) {
            BigDecimal error = (((high.subtract(low)).divide(BigDecimal.valueOf(2).pow(times + 1), getMathContext()))).abs();
            BigDecimal negative = bisectionOnT(low, BigDecimal.ZERO.subtract(error), xVal, yVal, times, true);
            BigDecimal positive = bisectionOnT(BigDecimal.ZERO.add(error), high, xVal, yVal, times, false);
            boolean includeNegative = false;
            boolean includePositive = false;
            // negative root falls within the error regions, method converged on possible root.
            if (bigDecimalInRange(low.add(error), negative, BigDecimal.ZERO.subtract(error))) {
                includeNegative = true;
            }
            // positive root falls within the error regions, method converged on possible root.
            if (bigDecimalInRange(BigDecimal.ZERO.add(error), positive, high.subtract(error))) {
                includePositive = true;
            }

            System.out.println("error: " + error);
            System.out.println("negative: " + negative);
            System.out.println("positive: " + positive);
            System.out.println("bigDecimalInRange(low.add(error), negative, BigDecimal.ZERO.subtract(error)): " + bigDecimalInRange(low.add(error), negative, BigDecimal.ZERO.subtract(error)));
            System.out.println("bigDecimalInRange(BigDecimal.ZERO.add(error), positive, high.subtract(error)): " + bigDecimalInRange(BigDecimal.ZERO.add(error), positive, high.subtract(error)));
            BigDecimal root = null;
            if (includeNegative) {
                root = negative;
            }
            if (includePositive) {
                if (root != null) {
                    root = ((negative.abs().compareTo(positive.abs()) < 0)? negative : positive);
                }
                else {
                    root = positive;
                }
            }
            return root;
        }
        else {
            return bisectionOnT(low, high, xVal, yVal, times, false);
        }
    }

    public BigDecimal bisectionOnT(BigDecimal low, BigDecimal high, BigDecimal xVal, BigDecimal yVal, int times, boolean negative) {
        BigDecimal c = (low.add(high)).divide(new BigDecimal(2), BigDecimal.ROUND_HALF_DOWN);
        BigDecimal v;
        BigDecimal f1 = tEquation(xVal, yVal, low);
        BigDecimal f2 = tEquation(xVal, yVal, high);
        if (f1.compareTo(BigDecimal.ZERO) < 0 ^ f2.compareTo(BigDecimal.ZERO) < 0) {
            System.out.println("DIVERGING");
        }
        if (times > 1) {
            v = tEquation(xVal, yVal, c);
            if (v.compareTo(BigDecimal.ZERO) < 0) {
                if (negative) {
                    high = c;
                }
                else {
                    low = c;
                }
            }
            else if (v.compareTo(BigDecimal.ZERO) == 0) {
                System.out.println("Exact root found.");
                return c;
            }
            else {
                if (negative) {
                    low = c;
                }
                else {
                    high = c;
                }
            }

            return bisectionOnT(low, high, xVal, yVal, times - 1, negative);
        }
        return c;
    }

    public BigDecimal tEquation(BigDecimal x, BigDecimal y, BigDecimal t) {
        MathContext mc = getMathContext();
        return (y.multiply(t.subtract(BigDecimalMath.sin(t, mc)))).subtract(x.multiply(BigDecimal.ONE.subtract(BigDecimalMath.cos(t, mc))));
    }

    @Override
    public ArrayList<BigDecimal[]> calcPoints() {
        ArrayList<BigDecimal[]> points = new ArrayList<>();
        BigDecimal s = BigDecimal.valueOf(this.getSegments());
        BigDecimal i = BigDecimal.ZERO;
        BigDecimal t = getTheta();
        BigDecimal r = getRadius();
        BigDecimal d = (t.divide(s, getMathContext())).abs();
        BigDecimal x = BigDecimal.ZERO;//new BigDecimal(this.getX1());
        BigDecimal y = BigDecimal.ZERO;//new BigDecimal(this.getY1());
        System.out.println("r: " + r + "\nd: " + d + "\ni: " + i);
        while (i.compareTo(t.abs()) <= 0) {
            BigDecimal bx = brachistochroneX(r, i, x);
            BigDecimal by = brachistochroneY(r, i, y);
            points.add(new BigDecimal[] {bx, by});
            i = i.add(d);
        }
        System.out.println("xVal: " + getXVal() + ", yVal: " + getYVal());
        System.out.println("AFTER CALCULATION BEFORE ADJUSTING");
        for (BigDecimal[] point : points) {
            System.out.println("\tpoint: " + Arrays.toString(point));
        }

        if (this.getX2() != getXVal().doubleValue() || this.getY2() != getYVal().doubleValue()) {
            BigDecimal xd = ((BigDecimal.valueOf(this.getX2() - this.getX1())).divide(getXVal(), getMathContext())).abs();
            BigDecimal yd = (BigDecimal.valueOf(this.getY2() - this.getY1()).divide(getYVal(), getMathContext())).abs();
            System.out.println("xd: " + xd + ", yd: " + yd);
            for (int j = 0; j < points.size(); j++) {
                BigDecimal[] point = points.get(j);
                BigDecimal[] p = new BigDecimal[] {
                        (xd.multiply(point[0])).add(BigDecimal.valueOf(this.getX1())),
                        (yd.multiply(point[1])).abs().add(BigDecimal.valueOf(this.getY2()))
                };
                points.set(j, p);
            }
        }
        System.out.println("After calcPoints:\bx1: " + getX1() + ", y1: " + getY1() + ", x2: " + getX2() + ", y2: " + getY2());
        return points;
    }

    @Override
    public double calcDuration() {
        BigDecimal r = getRadius().multiply(BigDecimal.valueOf(Math.PI)).divide(BigDecimal.valueOf(180), getMathContext());
        BigDecimal g = BigDecimal.valueOf(getGravity());
        BigDecimal dx = BigDecimal.valueOf(Math.abs(this.getX2() - this.getX1()));
        return (r.divide(g, getMathContext()).multiply(dx)).sqrt(getMathContext()).doubleValue();
    }

    public BigDecimal brachistochroneX(BigDecimal r, BigDecimal t, BigDecimal x0) {
        return x0.add(r.multiply(t.subtract(BigDecimalMath.sin(t, getMathContext()))));
    }

    public BigDecimal brachistochroneY(BigDecimal r, BigDecimal t, BigDecimal y0) {
        return y0.add(r.multiply(BigDecimal.valueOf(-1).add(BigDecimalMath.cos(t, getMathContext()))));
    }

    public boolean bigDecimalInRange(BigDecimal low, BigDecimal x, BigDecimal high) {
        return x.compareTo(low) >= 0 && x.compareTo(high) <= 0;
    }

    public BigDecimal calXVal() {
        BigDecimal deltaX = BigDecimal.valueOf(0 - this.getX1());
        BigDecimal xVal = BigDecimal.valueOf(this.getX2());
        System.out.println("calcXVal: x1: " + getX1() + ", x2: " + getX2());
        return xVal.abs().add(deltaX);
    }

    public BigDecimal calYVal() {
        BigDecimal deltaY = BigDecimal.valueOf(0 - this.getY1());
        BigDecimal yVal = BigDecimal.valueOf(this.getY2());
        System.out.println("calcYVal: y1: " + getY1() + ", y2: " + getY2());
        return yVal.abs().add(deltaY);
//        System.out.println("xVal: " + xVal + ", yVal: " + yVal + ", deltaX: " + deltaX + ", deltaY: " + deltaY);
    }

    public BigDecimal getRadius() {
        return radius;
    }

    public BigDecimal getTheta() {
        return theta;
    }

    public BigDecimal getXVal() {
        return xVal;
    }

    public BigDecimal getYVal() {
        return yVal;
    }

    @Override
    public String toString() {
        return "Brachistochrone";
    }

    @Override
    public String getEquation() {
        BigDecimal s = BigDecimal.valueOf(this.getSegments());
        BigDecimal i = BigDecimal.ZERO;
        BigDecimal t = getTheta();
        BigDecimal r = getRadius();
        BigDecimal d = (t.divide(s, getMathContext())).abs();
        BigDecimal x = BigDecimal.ZERO;//new BigDecimal(this.getX1());
        BigDecimal y = BigDecimal.ZERO;//new BigDecimal(this.getY1());
        String xEquation = x + " + " + r + "(" + t + " - sin(" + t + ")";
        String yEquation = y + " + " + r + "(" + -1 + " + cos(" + t + ")";
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

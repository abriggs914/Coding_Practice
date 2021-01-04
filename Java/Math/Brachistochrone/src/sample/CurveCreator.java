package sample;

import java.math.BigDecimal;
import java.util.ArrayList;

public interface CurveCreator {

    ArrayList<BigDecimal[]> calcPoints();

    double calcDuration();

    String getEquation();

    double XPointAtT(double t);

    double YPointAtT(double t);
}

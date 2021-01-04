package sample;

import javafx.scene.canvas.Canvas;
import javafx.scene.paint.Paint;

import java.math.BigDecimal;
import java.util.ArrayList;

public class GraphingCurve {

    private Paint paint;
    private Curve curve;
    private int markerRadius;

    public GraphingCurve(Curve curve, Paint curveColour) {
        this.curve = curve;
        this.paint = curveColour;
        this.markerRadius = 4;
    }

    public void draw(Canvas canvas) {
        double width = canvas.getWidth();
        double height = canvas.getHeight();
        if (curve.getBounds().getWidth() > width ||
                curve.getBounds().getHeight() > height) {
            System.out.println("OUT OF BOUNDS: " + curve.getBounds().getWidth() + " x " + curve.getBounds().getHeight() +  " VS. " + width + " x " + height);
            return;
        }
        Main.changeCanvasColour(canvas, paint);
        ArrayList<BigDecimal[]> points = curve.getPoints();

        for (BigDecimal[] point : points) {
            BigDecimal dX = point[0];
            BigDecimal dY = point[1];
            double x = dX.doubleValue();
            double y = dY.doubleValue();
            System.out.println("x: " + x + ", y: " + y);
            canvas.getGraphicsContext2D().strokeOval(x, y, markerRadius, markerRadius);
        }
    }

    public String toString() {
        return curve.toString();
    }

    public String getEquation() {
        return curve.getEquation();
    }

    public double getDuration() {
        return curve.getDuration();
    }

    public BigDecimal[] getPointAtT(double t) {
        return curve.getPointAtT(t);
    }

    public Paint getColour() {
        return paint;
    }
}

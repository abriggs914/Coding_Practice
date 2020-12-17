package sample.Version_4;

import javafx.geometry.Point2D;
import javafx.scene.paint.Color;
import javafx.scene.shape.Line;
import javafx.scene.shape.Polygon;

public class Testing {

    public static Polygon createPolygon(Line a, Line b, Line c, Color col) {
        Point2D intersectionAB = intersectionPoint(a, b);
        Point2D intersectionAC = intersectionPoint(a, c);
        Point2D intersectionBC = intersectionPoint(b, c);

        System.out.println("a: " + a);
        System.out.println("b: " + b);
        System.out.println("c: " + c);
        assert intersectionAB != null : "AB is NULL {" + intersectionAB + "}";
        assert intersectionAC != null : "AC is NULL {" + intersectionAC + "}";
        assert intersectionBC != null : "BC is NULL {" + intersectionBC + "}";
        Polygon p = new Polygon(intersectionAB.getX(), intersectionAB.getY(), intersectionAC.getX(), intersectionAC.getY(), intersectionBC.getX(), intersectionBC.getY());
        p.setFill(col);
        return p;
    }

    public static Point2D intersectionPoint(Line a, Line b) {
        double x1a = a.getStartX();
        double y1a = a.getStartY();
        double x2a = a.getEndX();
        double y2a = a.getEndY();

        double x1b = b.getStartX();
        double y1b = b.getStartY();
        double x2b = b.getEndX();
        double y2b = b.getEndY();

        double xda = x2a - x1a;
        double xdb = x2b - x1b;
//         x difference is 0 for 1 or both lines.
        if (xda == 0 || xdb == 0) {
            return null;
        }
        double ma = (y2a - y1a) / xda;
        double mb = (y2b - y1b) / xdb;

        double ba = y1a - (x1a * ma);
        double bb = y1b - (x1b * mb);

        double x = (bb - ba) / (ma - mb);
        double y = (ma * x) + ba;
        System.out.println(
                "x1a: " + x1a +
                "\ny1a: " + y1a +
                "\nx2a: " + x2a +
                "\ny2a: " + y2a +
                "\nx1b: " + x1b +
                "\ny1b: " + y1b +
                "\nx2b: " + x2b +
                "\ny2b: " + y2b +
                "\n y = " + ma + "x + " + ba +
                "\n y = " + mb + "x + " + bb +
                "\n x = " + x +
                "\n y = " + y
        );
//        TODO: sometimes produces NaN
        Point2D p = new Point2D(x, y);
        if (!a.contains(p) || !b.contains(p)) {
            return null;
        }
        return p;
    }

    public static void main(String[] args) {
        Line a = new Line(449.41592263397604, 115.64685700527684, 449.41592263397604, 115.64685700527684);
        Line b = new Line(449.41592263397604, 115.64685700527684, 409.6,119.4202614379085);
        Line c = new Line(409.6, 119.4202614379085, 449.41592263397604, 115.64685700527684);
        Polygon p = createPolygon(a, b, c, Color.WHITE);

    }
}

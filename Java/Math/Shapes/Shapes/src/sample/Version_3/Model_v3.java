package sample;

import javafx.collections.ObservableList;
import javafx.geometry.Point2D;
import javafx.scene.paint.Color;
import javafx.scene.shape.Line;
import javafx.scene.shape.Polygon;
import sample.Version_3.Triangle_v3;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class Model_v3 {

    private static double whiteBoardMarkerRedVal;
    private static double whiteBoardMarkerGreenVal;
    private static double whiteBoardMarkerBlueVal;
    private static double[] whiteBoardMarkerColour;
    private static double opacity = 1;

    private static ArrayList<Line> whiteBoardLines;
    private static HashMap<Polygon, Triangle_v3> whiteBoardTriangles;
    private static int triangleNumber;

    public Model_v3() {
        whiteBoardMarkerRedVal = 1;
        whiteBoardMarkerGreenVal = 1;
        whiteBoardMarkerBlueVal = 1;
        updateWhiteBoardMarkerColour();

        whiteBoardLines = new ArrayList<>();
        whiteBoardTriangles = new HashMap<>();
        triangleNumber = 0;
    }

    public static void updateWhiteBoardRed(double value) {
        whiteBoardMarkerRedVal = value;
        updateWhiteBoardMarkerColour();
    }

    public static void updateWhiteBoardGreen(double value) {
        whiteBoardMarkerGreenVal = value;
        updateWhiteBoardMarkerColour();
    }

    public static void updateWhiteBoardBlue(double value) {
        whiteBoardMarkerBlueVal = value;
        updateWhiteBoardMarkerColour();
    }

    private static void updateWhiteBoardMarkerColour() {
        whiteBoardMarkerColour = new double[] {
                whiteBoardMarkerRedVal,
                whiteBoardMarkerGreenVal,
                whiteBoardMarkerBlueVal,
                1.0
        };
    }

    public static void addTriangle(Polygon p, Triangle_v3 t) {
        for (Polygon triangle : whiteBoardTriangles.keySet()) {
            if (matchingPolygons(p, triangle)) {
                return;
            }
        }
//        Triangle triangle = createTriangle(p);
//        whiteBoardTriangles.put(p, triangle);
        whiteBoardTriangles.put(p, t);
    }

    public static double[] getWhiteBoardMarkerColour() {
        return whiteBoardMarkerColour;
    }

    public static Color getWhiteBoardColour() {
        double[] markerColour = getWhiteBoardMarkerColour();
        double r = markerColour[0];
        double g = markerColour[1];
        double b = markerColour[2];
        double a = markerColour[3];
        return new Color(r, g, b, a);
    }

    public static void addLine(Line l) {
        whiteBoardLines.add(l);
    }

    public static void addLines(Line... l) {
        whiteBoardLines.addAll(Arrays.asList(l));
    }

    public static void removeLines(Line... lines) {
        int s = whiteBoardLines.size();
        whiteBoardLines.removeAll(Arrays.asList(lines));
        int a = whiteBoardLines.size();
        if (s - lines.length != a) {
            ArrayList<Line> wbLines = new ArrayList<>();
            for (Line wbLine : whiteBoardLines) {
                boolean include = true;
                for (Line l : lines) {
                    if (matchingLines(wbLine, l)) {
                        include = false;
                        break;
                    }
                }
                if (include) {
                    wbLines.add(wbLine);
                }
            }
            whiteBoardLines.clear();
            whiteBoardLines.addAll(wbLines);
        }
    }

    public static ArrayList<Line> getWhiteBoardLines() {
        return whiteBoardLines;
    }

    public static void clearWhiteBoardLines() {
        whiteBoardLines.clear();
    }

    public static void clearWhiteBoardTriangles() {
        whiteBoardTriangles.clear();
    }

    public static HashMap<Line, ArrayList<Line>> getIntersectingWhiteBoardLines() {
        HashMap<Line, ArrayList<Line>> intersections = new HashMap<>();
        for (Line a : whiteBoardLines) {
            ArrayList<Line> crosses = new ArrayList<>();
            for (Line b : whiteBoardLines) {
                if (a != b) {
                    if (intersectionPoint(a, b) != null) {
                        if (intersections.containsKey(b)) {
                            if (!intersections.get(b).contains(a)) {
                                crosses.add(b);
//                                System.out.println("if if intersection point: " + WhiteBoardModel.intersectionPoint(a, b));
                            }
                        } else {
                            crosses.add(b);
//                            System.out.println("if else intersection point: " + WhiteBoardModel.intersectionPoint(a, b));
                        }
                    }
                }
            }
            if (crosses.size() > 0) {
                intersections.put(a, crosses);
            }
        }
        return intersections;
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
//        System.out.println(
//                "x1a: " + x1a +
//                "\ny1a: " + y1a +
//                "\nx2a: " + x2a +
//                "\ny2a: " + y2a +
//                "\nx1b: " + x1b +
//                "\ny1b: " + y1b +
//                "\nx2b: " + x2b +
//                "\ny2b: " + y2b +
//                "\n y = " + ma + "x + " + ba +
//                "\n y = " + mb + "x + " + bb
//        );
//        TODO: sometimes produces NaN
        Point2D p = new Point2D(x, y);
        if (!a.contains(p) || !b.contains(p)) {
            return null;
        }
        return p;
    }

    public static HashMap<Polygon, Triangle_v3> getWhiteBoardTriangles() {
        return whiteBoardTriangles;
    }

    public static ArrayList<Triangle_v3> checkWhiteBoardTriangles() {
        ArrayList<Triangle_v3> triangles = new ArrayList<>();
        HashMap<Line, ArrayList<Line>> intersections = getIntersectingWhiteBoardLines();
        for (Line a : intersections.keySet()) {
            for (Line b : intersections.get(a)){
                if (intersections.containsKey(b)) {
//                    System.out.println("a: " + a + "\nb: " + b);
                    ArrayList<Line> bsToCs = intersections.get(b);
                    for (Line c : bsToCs) {
                        if (intersections.get(a).contains(c)) {
//                            System.out.println("\tc: " + c);
//                            Triangle t = new Triangle("", a, b, c);
                            Triangle_v3 t = createTriangle(genTriangleName(), a, b, c);
//                                Intersection i = new Intersection(a, b, c);
                            triangles.add(t);
//                            }
                        }
                    }
                }
            }
        }
        return triangles;
    }

    public static boolean matchingPolygons(Polygon a, Polygon b) {
        ObservableList<Double> aPoints = a.getPoints().sorted();
        ObservableList<Double> bPoints = b.getPoints().sorted();
        if (aPoints.size() == bPoints.size() && aPoints.size() == 6) {
            for (int i = 0; i < aPoints.size(); i++) {
                if (!aPoints.get(i).equals(bPoints.get(i))) {
                    return false;
                }
            }
        }
        return true;
    }

    /**
     * Checks if two given lines cover the same region.
     * @param a First line.
     * @param b Second line.
     * @return True if they cover the same region.
     */
    public static boolean matchingLines(Line a, Line b) {
        double aXS = a.getStartX();
        double aYS = a.getStartY();
        double aXE = a.getEndX();
        double aYE = a.getEndY();
        double bXS = b.getStartX();
        double bYS = b.getStartY();
        double bXE = b.getEndX();
        double bYE = b.getEndY();
        return (aXS == bXS && aXE == bXE && aYS == bYS && aYE == bYE) || (aXS == bXE && aXE == bXS && aYS == bYE && aYE == bYS);
    }

    public static Triangle_v3 createTriangle(String name, Line a, Line b, Line c) {
        Triangle_v3 t = new Triangle_v3(name, a, b, c);
        System.out.println("\n\tNew triangle:\n" + t);
        return t;
    }

    public static sample.AdjustableTriangle_v3 createAdjustableTriangle(String name, Line a, Line b, Line c) {
        sample.AdjustableTriangle_v3 t = new sample.AdjustableTriangle_v3(name, a, b, c);
        System.out.println("\n\tNew triangle:\n" + t);
        return t;
    }

    public static Triangle_v3 createTriangle(Polygon triangle) {
        ObservableList<Double> points = triangle.getPoints();
        Point2D ab = new Point2D(points.get(0), points.get(1));
        Point2D ac = new Point2D(points.get(2), points.get(3));
        Point2D bc = new Point2D(points.get(4), points.get(5));
        double a = ab.distance(ac);
        double b = ab.distance(bc);
        double c = ac.distance(bc);
        sample.Side_v3 sideA = new sample.Side_v3("side a", a);
        sample.Side_v3 sideB = new sample.Side_v3("side b", b);
        sample.Side_v3 sideC = new sample.Side_v3("side c", c);
        Triangle_v3 t = new Triangle_v3(genTriangleName(), sideA, sideB, sideC, null, null, null);
        t.solveRemainingTriangle();
        System.out.println("\n\tNew triangle:\n" + t);
//        for (int i = 0; i < points.size(); i+=2) {
//            Double x = points.get(i);
//            Double y = points.get(i + 1);
//            Point2D p = new Point2D(x, y);
//            if (i < 2) {
//                sideA = p.;
//            }
//            else if (i < 4) {
//                sideB = ;
//            }
//            else {
//                sideC = ;
//            }
//        }
        return t;
    }

    public static String genTriangleName() {
        triangleNumber++;
        return "Triangle " + triangleNumber;
    }

    public static void resetTriangleNumber() {
        triangleNumber = 0;
    }

}

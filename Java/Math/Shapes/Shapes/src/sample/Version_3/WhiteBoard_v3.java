package sample;

import com.sun.org.apache.xpath.internal.operations.Mod;
import javafx.geometry.Point2D;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.Slider;
import javafx.scene.control.Tooltip;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.scene.shape.*;
import sample.Version_3.Triangle_v3;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class WhiteBoard_v3 {

    // Default design and style variables
    private boolean check_drawGrid = true;
    private int CELL_WIDTH = 10;
    private int CELL_HEIGHT = 10;
    private Color GRID_LINE_COLOUR = Color.color(0.55, 0.55, 0.55, 0.7);
    private boolean check_drawIntersectionsInterior = false;
    private boolean check_drawIntersectionsSupplementA = false;
    private boolean check_drawIntersectionsSupplementB = false;
    private boolean check_drawIntersectionsOpposite = false;

    private Parent root;
    private Paint BACKGROUND;
    private Point2D markerPointFirst;
    private Point2D markerPointLast;

    public VBox vbox_whiteBoard_backdrop;
    public HBox hbox_whiteBoard_buttons;
    public Pane pane_whiteBoard_drawing;
    public Button button_whiteBoard_clear;
    public Slider slider_whiteBoard_red_colour;
    public Slider slider_whiteBoard_green_colour;
    public Slider slider_whiteBoard_blue_colour;
    public Rectangle rectangle_whiteBoard_marker_colour;
    public Rectangle rectangle_whiteBoard_drawing;

    public WhiteBoard_v3() {
//        root = rootIn;
        BACKGROUND = Color.WHITE;
    }

    public void setDims(double x, double y, double w, double h) {
        pane_whiteBoard_drawing.setPrefSize(w, h);
        pane_whiteBoard_drawing.setMaxSize(w, h);
        pane_whiteBoard_drawing.setMinSize(w, h);
        pane_whiteBoard_drawing.setLayoutX(x);
        pane_whiteBoard_drawing.setLayoutY(y);
        this.drawGridBackground();
    }

    private void clearWhiteBoard() {
        rectangle_whiteBoard_drawing.setFill(BACKGROUND);
    }

    public void initFields(Parent rootIn) {
        root = rootIn;
        vbox_whiteBoard_backdrop = (VBox) root.lookup("#vbox_whiteBoard_backdrop");
        hbox_whiteBoard_buttons = (HBox) root.lookup("#hbox_whiteBoard_buttons");
        pane_whiteBoard_drawing = (Pane) root.lookup("#pane_whiteBoard_drawing");

        button_whiteBoard_clear = (Button) root.lookup("#button_whiteBoard_clear");
        slider_whiteBoard_red_colour = (Slider) root.lookup("#slider_whiteBoard_red_colour");
        slider_whiteBoard_green_colour = (Slider) root.lookup("#slider_whiteBoard_green_colour");
        slider_whiteBoard_blue_colour = (Slider) root.lookup("#slider_whiteBoard_blue_colour");
        rectangle_whiteBoard_marker_colour = (Rectangle) root.lookup("#rectangle_whiteBoard_marker_colour");
        rectangle_whiteBoard_drawing = (Rectangle) root.lookup("#rectangle_whiteBoard_drawing");

        this.drawGridBackground();
//        addTestLines();
        addTestAdjustable();

        this.addListeners();

        sample.Model_v3.updateWhiteBoardRed(slider_whiteBoard_red_colour.getValue());
        sample.Model_v3.updateWhiteBoardGreen(slider_whiteBoard_green_colour.getValue());
        sample.Model_v3.updateWhiteBoardBlue(slider_whiteBoard_blue_colour.getValue());

    }

    public void drawGridBackground() {
        if (!check_drawGrid) {
            return;
        }
        double width = pane_whiteBoard_drawing.getWidth();
        double height = pane_whiteBoard_drawing.getHeight();
        double top = pane_whiteBoard_drawing.getLayoutBounds().getMinY();
        double bottom = top + height; //pane_whiteBoard_drawing.getLayoutBounds().getMaxY();
        double left = pane_whiteBoard_drawing.getLayoutBounds().getMinX();
        double right = left + width; //pane_whiteBoard_drawing.getLayoutBounds().getMaxX();
        Line lt = new Line(left, top, right, bottom);
        lt.setStroke(Color.ORANGE);
        lt.setStrokeWidth(5);
        pane_whiteBoard_drawing.getChildren().add(lt);
        int cols = (int) width / CELL_WIDTH;
        int rows = (int) height / CELL_HEIGHT;
        for (int i = 0; i < rows + 1; i++) {
            double y1 = (i * CELL_HEIGHT) + top;
            Line l = new Line(left, y1, right, y1);
            l.setStroke(GRID_LINE_COLOUR);
            pane_whiteBoard_drawing.getChildren().add(l);
        }
        for (int j = 0; j < cols + 1; j++) {
            double x1 = (j * CELL_WIDTH) + left;
            Line l = new Line(x1, top, x1, bottom);
            l.setStroke(GRID_LINE_COLOUR);
            pane_whiteBoard_drawing.getChildren().add(l);
        }
    }

    public void addTestAdjustable() {
        System.out.println("Adding adjustable");
        Line a = new Line(60, 100, 160, 125);
        Line b = new Line(75, 81, 130, 225);
        Line c = new Line(145, 71, 100, 205);
        sample.AdjustableTriangle_v3 t = new sample.AdjustableTriangle_v3("T", a, b, c);
//        t.markerAListener();

//        t.markerA.setOnMousePressed(event -> {
//            double x = event.getX();
//            double y = event.getY();
//            t.translateCornerA(x, y);
//            t.markerA.setCenterX(x);
//            t.markerA.setCenterY(y);
//            this.drawTriangles();
//        });
//
//        t.markerA.setOnMouseDragged(event -> {
//            double x = event.getX();
//            double y = event.getY();
//            t.translateCornerA(x, y);
//            t.markerA.setCenterX(x);
//            t.markerA.setCenterY(y);
//            this.drawLines();
//        });

        Polygon p = t.polygon;
        sample.Model_v3.addTriangle(p, t);
        this.draw();
    }

    /**
     * Draw 8 test intersection points of 16 unique lines.
     */
    public void addTestLines() {
        // horizontal lines row 1
        Line a1 = new Line(60, 100, 61, 20);
        Line b1 = new Line(180, 100, 181, 20);
        Line c1 = new Line(300, 20, 301, 100);
        Line d1 = new Line(420, 20, 421, 100);

        // vertical lines row 1
        Line a2 = new Line(20, 60, 100, 61);
        Line b2 = new Line(220, 60, 140, 61);
        Line c2 = new Line(260, 60, 340, 61);
        Line d2 = new Line(460, 60, 380, 61);

        // vertical lines row 2
        Line e1 = new Line(20, 180, 100, 181);
        Line f1 = new Line(220, 180, 140, 181);
        Line g1 = new Line(260, 180, 340, 181);
        Line h1 = new Line(460, 180, 380, 181);

        // horizontal lines row 2
        Line e2 = new Line(60, 220, 61, 140);
        Line f2 = new Line(180, 220, 181, 140);
        Line g2 = new Line(300, 140, 301, 220);
        Line h2 = new Line(420, 140, 421, 220);

        ArrayList<Line> lines = new ArrayList<>(Arrays.asList(a1, a2, b1, b2, c1, c2, d1, d2, e1, e2, f1, f2, g1, g2, h1, h2));
        for (Line l : lines) {
            l.setStroke(Color.GREEN);
            l.setStrokeWidth(3);
            sample.Model_v3.addLine(l);
        }
        this.checkTriangles();
//        this.drawLines();
        this.draw();
    }

    private void addListeners() {
        slider_whiteBoard_red_colour.setOnMouseDragged(event -> {
            sample.Model_v3.updateWhiteBoardRed(slider_whiteBoard_red_colour.getValue());
            this.updateMarkerColour();
        });

        slider_whiteBoard_green_colour.setOnMouseDragged(event -> {
            sample.Model_v3.updateWhiteBoardGreen(slider_whiteBoard_green_colour.getValue());
            this.updateMarkerColour();
        });

        slider_whiteBoard_blue_colour.setOnMouseDragged(event -> {
            sample.Model_v3.updateWhiteBoardBlue(slider_whiteBoard_blue_colour.getValue());
            this.updateMarkerColour();
        });
        slider_whiteBoard_red_colour.setOnMouseClicked(event -> {
            sample.Model_v3.updateWhiteBoardRed(slider_whiteBoard_red_colour.getValue());
            this.updateMarkerColour();
        });

        slider_whiteBoard_green_colour.setOnMouseClicked(event -> {
            sample.Model_v3.updateWhiteBoardGreen(slider_whiteBoard_green_colour.getValue());
            this.updateMarkerColour();
        });

        slider_whiteBoard_blue_colour.setOnMouseClicked(event -> {
            sample.Model_v3.updateWhiteBoardBlue(slider_whiteBoard_blue_colour.getValue());
            this.updateMarkerColour();
        });

//        pane_whiteBoard_drawing.setOnMousePressed(event -> {
//            System.out.println("Mouse pressed on white board");
////          System.out.println("Top node: " + pane_whiteBoard_drawing.g);
//            System.out.println("clicked: " + clickedNothing(event.getX(), event.getY()));
//            System.out.println("children\n" + pane_whiteBoard_drawing.getChildren());
//            markerPointFirst = new Point2D(event.getX(), event.getY());
//        });
//
//        pane_whiteBoard_drawing.setOnMouseDragged(event -> {
//            markerPointLast = new Point2D(event.getX(), event.getY());
//            this.drawLines();
//        });
//
//        pane_whiteBoard_drawing.setOnMouseReleased(event -> {
//            System.out.println("Mouse released on white board");
//            markerPointLast = new Point2D(event.getX(), event.getY());
//            Line l = createMarkedLine();
//            WhiteBoardModel.addLine(l);
//            this.checkTriangles();
//            this.drawLines();
//            markerPointFirst = null;
//            markerPointLast = null;
//        });

        button_whiteBoard_clear.setOnMouseClicked(event -> {
            pane_whiteBoard_drawing.getChildren().clear();
            sample.Model_v3.clearWhiteBoardLines();
            sample.Model_v3.clearWhiteBoardTriangles();
            sample.Model_v3.resetTriangleNumber();
            this.drawGridBackground();
            this.addTestAdjustable();
        });
    }

    public boolean clickedNothing(double mouseX, double mouseY) {
        for (Node child : pane_whiteBoard_drawing.getChildren()) {
            if (child.getLayoutBounds().contains(mouseX, mouseY)) {
                System.out.println("child: " + child);
                return false;
            }
        }
        return true;
    }

    /**
     * Check WhiteBoard for all triangles.
     */
    public void checkTriangles() {
//        ArrayList<Triangle> triangles = WhiteBoardModel.getWhiteBoardTriangles();
        ArrayList<Triangle_v3> triangles = sample.Model_v3.checkWhiteBoardTriangles();
        if (triangles.size() > 0) {
            for (Triangle_v3 t : triangles) {
//                Triangle t =
                sample.Model_v3.removeLines(t.lineA, t.lineB, t.lineC);
                sample.Model_v3.addTriangle(t.polygon, t);
            }
        }
    }

    public Line createMarkedLine() {
        Line l = new Line(markerPointFirst.getX(), markerPointFirst.getY(), markerPointLast.getX(), markerPointLast.getY());
        Color paint = sample.Model_v3.getWhiteBoardColour();
        l.setFill(paint);
        l.setStroke(paint);
        l.setStrokeWidth(5);
        return l;
    }

    private void updateMarkerColour() {
        double[] vals = sample.Model_v3.getWhiteBoardMarkerColour();
        double r = vals[0], g = vals[1], b = vals[2], a = vals[3];
        rectangle_whiteBoard_marker_colour.setFill(new Color(r, g, b, a));
    }

    public ArrayList<Node> drawLines() {
        ArrayList<Line> lines = sample.Model_v3.getWhiteBoardLines();
//        pane_whiteBoard_drawing.getChildren().clear();
        //            pane_whiteBoard_drawing.getChildren().add(line);
        ArrayList<Node> nodes = new ArrayList<>(lines);
        if (markerPointFirst != null && markerPointLast != null) {
            Line l = createMarkedLine();
            if (!pane_whiteBoard_drawing.getChildren().contains(l)) {
//                pane_whiteBoard_drawing.getChildren().add(l);
                nodes.add(l);
            }
        }

        HashMap<Line, ArrayList<Line>> intersectingLines = sample.Model_v3.getIntersectingWhiteBoardLines();
        for (Line a : intersectingLines.keySet()) {
            ArrayList<Line> intersections = intersectingLines.get(a);
            for (Line b : intersections) {
                ArrayList<Node> markers = this.drawIntersections(a, b);
//                pane_whiteBoard_drawing.getChildren().addAll(markers);
                nodes.addAll(markers);
            }
        }
        this.drawTriangles();
        return nodes;
    }

    public ArrayList<Node> drawTriangles() {
        ArrayList<Node> nodes = new ArrayList<>();
//        ArrayList<Triangle> triangles = WhiteBoardModel.getWhiteBoardTriangles();
        HashMap<Polygon, Triangle_v3> triangles = sample.Model_v3.getWhiteBoardTriangles();
        for (Polygon p : triangles.keySet()) {
            Triangle_v3 t = triangles.get(p);
            Line a = t.lineA;
            Line b = t.lineB;
            Line c = t.lineC;
            sample.Model_v3.removeLines(a, b, c);
            nodes.addAll(drawIntersectionsSupplementA(a, b));
            nodes.addAll(drawIntersectionsSupplementB(a, c));
            nodes.addAll(drawIntersectionsSupplementA(b, c));
            Point2D center = t.centroid();
            Circle circle = new Circle(center.getX(), center.getY(), 3, Color.DODGERBLUE);
//            System.out.println("t: " + t + "\ncentroid: " + center);
//            pane_whiteBoard_drawing.getChildren().add(circle);
            if (t.getClass() == sample.AdjustableTriangle_v3.class) {
//                System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\tAdjustable Triangle\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
                sample.AdjustableTriangle_v3 at = (sample.AdjustableTriangle_v3) t;
                Circle circleA = at.getMarkerA();
                Circle circleB = at.getMarkerB();
                Circle circleC = at.getMarkerC();

                circleA.setOnMousePressed(event -> {
//                    System.out.println("markerA OnMousePressed");
                    double x = event.getX();
                    double y = event.getY();
                    at.translateCornerA(x, y);
                    at.markerA.setCenterX(x);
                    at.markerA.setCenterY(y);
//                    this.drawLines();
                });

                circleA.setOnMouseDragged(event -> {
//                    System.out.println("markerA OnMouseDragged");
                    double x = event.getX();
                    double y = event.getY();
                    at.translateCornerA(x, y);
                    at.markerA.setCenterX(x);
                    at.markerA.setCenterY(y);
//                    this.drawLines();
                });

//                pane_whiteBoard_drawing.getChildren().addAll(circleA, circleB, circleC);
                nodes.addAll(Arrays.asList(circle, circleA, circleB, circleC));
            }
            sample.Model_v3.addLines(t.lineA, t.lineB, t.lineC);
        }
        return nodes;
    }

    // Main drawing method.
    // Draws all lines and triangles to the WhiteBoard.
    public void draw() {
        pane_whiteBoard_drawing.getChildren().clear();
        this.drawGridBackground();
        pane_whiteBoard_drawing.getChildren().addAll(this.drawLines());
        pane_whiteBoard_drawing.getChildren().addAll(this.drawTriangles());
    }

    /**
     * Draw an arc between the two angles, and add a tooltip indicating the interior angle, start angle. and arc length.
     *
     * @param t      Triangle object required for arc length.
     * @param p      Point2d object marking the intersection point.
     * @param angleA double value indicating the starting angle for arc placement.
     * @param angleB double value indicating the ending angle for arc placement.
     * @return List of all markers.
     */
    public ArrayList<Node> drawAngleArc(Triangle_v3 t, Point2D p, double angleA, double angleB) {
        double radius = 22;
        double angle = t.C.angle;
        double delta = Math.abs(angleA - angleB);
        double startAngle = (((angleA / 360) <= (angleB / 360)) ? angleA : angleB); // choose lesser value then check orientation

        if (delta >= 180) {
            startAngle = ((startAngle == angleB) ? angleA : angleB);
        }

        Color color = new Color(0, 0, 0, 0); // transparent

        Arc arc = new Arc(p.getX(), p.getY(), radius, radius, startAngle, angle);
//        arc.setType(ArcType.ROUND);
        arc.setFill(color);
        arc.setStroke(Color.DARKGRAY);
        arc.setStrokeWidth(4);

        Tooltip toolTipAngle = new Tooltip("Angle:\t\t" + angle + "\nStart Angle:\t" + startAngle + "\nArc Length:\t" + angle); // + "\nv:\t\t" + Vector.computeAngle(p.getX(), p.getY(), lb.getEndX(), lb.getEndY()));
        Tooltip.install(arc, toolTipAngle);

        return new ArrayList<>(Arrays.asList(arc));
    }

    /**
     * Calculate triangle encompassing interior angle of intersection. Mark angle with Line and circle objects, with tooltips,
     *
     * @param a Line object representing the first of the two intersecting lines drawn.
     * @param b Line object representing the second of the two intersecting lines drawn.
     * @return List of all markers.
     */
    public ArrayList<Node> drawIntersectionsInterior(Line a, Line b) {
        Point2D p = sample.Model_v3.intersectionPoint(a, b);
        Point2D ptA = new Point2D(a.getEndX(), a.getEndY());
        Point2D ptB = new Point2D(b.getEndX(), b.getEndY());

        Line la = new Line(p.getX(), p.getY(), a.getEndX(), a.getEndY());
        Line lb = new Line(p.getX(), p.getY(), b.getEndX(), b.getEndY());
        Line lc = new Line(a.getEndX(), a.getEndY(), b.getEndX(), b.getEndY());

        double lenA = p.distance(ptA);
        double lenB = p.distance(ptB);
        double lenC = ptB.distance(ptA);
        sample.Side_v3 sideA = new sample.Side_v3("", lenA);
        sample.Side_v3 sideB = new sample.Side_v3("", lenB);
        sample.Side_v3 sideC = new sample.Side_v3("", lenC);
        Triangle_v3 t = new Triangle_v3("", sideA, sideB, sideC, null, null, null);

        double angleB = 360 - sample.Vector_v3.computeAngle(p.getX(), p.getY(), b.getEndX(), b.getEndY());
        double angleA = 360 - sample.Vector_v3.computeAngle(p.getX(), p.getY(), a.getEndX(), a.getEndY());

        double halfX = (ptB.getX() + ptA.getX()) / 2;
        double halfY = (ptB.getY() + ptA.getY()) / 2;
        Circle mark = new Circle(halfX, halfY, 5, Color.ORANGE);

        Tooltip toolTipSideA = new Tooltip("side a: " + sideA);
        Tooltip.install(la, toolTipSideA);
        Tooltip toolTipSideB = new Tooltip("side b: " + sideB);
        Tooltip.install(lb, toolTipSideB);
        Tooltip toolTipSideC = new Tooltip("side c: " + sideC);
        Tooltip.install(lc, toolTipSideC);
        la.setStroke(Color.RED);
        lb.setStroke(Color.YELLOW);
        lc.setStroke(Color.BLUE);
        la.setStrokeWidth(3);
        lb.setStrokeWidth(3);
        lc.setStrokeWidth(3);

        ArrayList<Node> markers = new ArrayList<>(drawAngleArc(t, p, angleA, angleB));
        markers.addAll(Arrays.asList(la, lb, lc, mark));
        return markers;
    }

    /**
     * Calculate triangle encompassing supplement angle of line a. Mark angle with Line and circle objects, with tooltips,
     *
     * @param a Line object representing the first of the two intersecting lines drawn.
     * @param b Line object representing the second of the two intersecting lines drawn.
     * @return List of all markers.
     */
    public ArrayList<Node> drawIntersectionsSupplementA(Line a, Line b) {
        double xa = a.getStartX();
        double ya = a.getStartY();
        double xb = b.getEndX();
        double yb = b.getEndY();
        Point2D p = sample.Model_v3.intersectionPoint(a, b);
        Point2D ptA = new Point2D(xa, ya);
        Point2D ptB = new Point2D(xb, yb);

        Line la = new Line(p.getX(), p.getY(), xa, ya);
        Line lb = new Line(p.getX(), p.getY(), xb, yb);
        Line lc = new Line(xa, ya, xb, yb);

        double lenA = p.distance(ptA);
        double lenB = p.distance(ptB);
        double lenC = ptB.distance(ptA);
        sample.Side_v3 sideA = new sample.Side_v3("", lenA);
        sample.Side_v3 sideB = new sample.Side_v3("", lenB);
        sample.Side_v3 sideC = new sample.Side_v3("", lenC);
        Triangle_v3 t = new Triangle_v3("", sideA, sideB, sideC, null, null, null);

        double angleB = 360 - sample.Vector_v3.computeAngle(p.getX(), p.getY(), xb, yb);
        double angleA = 360 - sample.Vector_v3.computeAngle(p.getX(), p.getY(), xa, ya);

        double halfX = (ptB.getX() + ptA.getX()) / 2;
        double halfY = (ptB.getY() + ptA.getY()) / 2;
        Circle mark = new Circle(halfX, halfY, 5, Color.ORANGE);

        ArrayList<Node> markers = new ArrayList<>(drawAngleArc(t, p, angleA, angleB));
        markers.addAll(Arrays.asList(la, lb, lc, mark));
        return markers;
    }

    /**
     * Calculate triangle encompassing supplement angle of line b. Mark angle with Line and circle objects, with tooltips,
     *
     * @param a Line object representing the first of the two intersecting lines drawn.
     * @param b Line object representing the second of the two intersecting lines drawn.
     * @return List of all markers.
     */
    public ArrayList<Node> drawIntersectionsSupplementB(Line a, Line b) {
        double xa = a.getEndX();
        double ya = a.getEndY();
        double xb = b.getStartX();
        double yb = b.getStartY();
        Point2D p = sample.Model_v3.intersectionPoint(a, b);
        Point2D ptA = new Point2D(xa, ya);
        Point2D ptB = new Point2D(xb, yb);

        Line la = new Line(p.getX(), p.getY(), xa, ya);
        Line lb = new Line(p.getX(), p.getY(), xb, yb);
        Line lc = new Line(xa, ya, xb, yb);

        double lenA = p.distance(ptA);
        double lenB = p.distance(ptB);
        double lenC = ptB.distance(ptA);
        sample.Side_v3 sideA = new sample.Side_v3("", lenA);
        sample.Side_v3 sideB = new sample.Side_v3("", lenB);
        sample.Side_v3 sideC = new sample.Side_v3("", lenC);
        Triangle_v3 t = new Triangle_v3("", sideA, sideB, sideC, null, null, null);

        double angleB = 360 - sample.Vector_v3.computeAngle(p.getX(), p.getY(), xb, yb);
        double angleA = 360 - sample.Vector_v3.computeAngle(p.getX(), p.getY(), xa, ya);

        double halfX = (ptB.getX() + ptA.getX()) / 2;
        double halfY = (ptB.getY() + ptA.getY()) / 2;
        Circle mark = new Circle(halfX, halfY, 5, Color.ORANGE);

        ArrayList<Node> markers = new ArrayList<>(drawAngleArc(t, p, angleA, angleB));
        markers.addAll(Arrays.asList(la, lb, lc, mark));
        return markers;
    }

    /**
     * Calculate triangle encompassing the opposite angle. Mark angle with Line and circle objects, with tooltips,
     *
     * @param a Line object representing the first of the two intersecting lines drawn.
     * @param b Line object representing the second of the two intersecting lines drawn.
     * @return List of all markers.
     */
    public ArrayList<Node> drawIntersectionsOpposite(Line a, Line b) {
        double xa = a.getStartX();
        double ya = a.getStartY();
        double xb = b.getStartX();
        double yb = b.getStartY();
        Point2D p = sample.Model_v3.intersectionPoint(a, b);
        Point2D ptA = new Point2D(xa, ya);
        Point2D ptB = new Point2D(xb, yb);

        Line la = new Line(p.getX(), p.getY(), xa, ya);
        Line lb = new Line(p.getX(), p.getY(), xb, yb);
        Line lc = new Line(xa, ya, xb, yb);

        double lenA = p.distance(ptA);
        double lenB = p.distance(ptB);
        double lenC = ptB.distance(ptA);
        sample.Side_v3 sideA = new sample.Side_v3("", lenA);
        sample.Side_v3 sideB = new sample.Side_v3("", lenB);
        sample.Side_v3 sideC = new sample.Side_v3("", lenC);
        Triangle_v3 t = new Triangle_v3("", sideA, sideB, sideC, null, null, null);

        double angleB = 360 - sample.Vector_v3.computeAngle(p.getX(), p.getY(), xb, yb);
        double angleA = 360 - sample.Vector_v3.computeAngle(p.getX(), p.getY(), xa, ya);

        double halfX = (ptB.getX() + ptA.getX()) / 2;
        double halfY = (ptB.getY() + ptA.getY()) / 2;
        Circle mark = new Circle(halfX, halfY, 5, Color.ORANGE);

        ArrayList<Node> markers = new ArrayList<>(drawAngleArc(t, p, angleA, angleB));
        markers.addAll(Arrays.asList(la, lb, lc, mark));
        return markers;
    }

    /**
     * Draw markers around an intersection, indicating the intersection point and creating tooltips to showcase calculations.
     *
     * @param a Line object, chronologically first of the two lines drawn.
     * @param b Line object, chronologically second of the two lines drawn.
     * @return List of all markers.
     */
    public ArrayList<Node> drawIntersections(Line a, Line b) {
        ArrayList<Node> markers = new ArrayList<>();
        if (check_drawIntersectionsInterior) {
            markers.addAll(this.drawIntersectionsInterior(a, b));
        }
        if (check_drawIntersectionsSupplementA) {
            markers.addAll(this.drawIntersectionsSupplementA(a, b));
        }
        if (check_drawIntersectionsSupplementB) {
            markers.addAll(this.drawIntersectionsSupplementB(a, b));
        }
        if (check_drawIntersectionsOpposite) {
            markers.addAll(this.drawIntersectionsOpposite(a, b));
        }
        return markers;
    }
}

package sample.Version_4;

import javafx.geometry.Bounds;
import javafx.geometry.Insets;
import javafx.geometry.Point2D;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.Slider;
import javafx.scene.control.Tooltip;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.scene.shape.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class WhiteBoard {

    public VBox vbox_whiteBoard_backdrop;
    public HBox hbox_whiteBoard_buttons;
    public Pane pane_whiteBoard_drawing;
    public Pane pane_whiteBoard_drawing_container;
    public Pane pane_whiteBoard_container;
    public Button button_whiteBoard_clear;
    public Slider slider_whiteBoard_red_colour;
    public Slider slider_whiteBoard_green_colour;
    public Slider slider_whiteBoard_blue_colour;
    public Rectangle rectangle_whiteBoard_marker_colour;

    public WhiteBoard() {
//        root = rootIn;
    }

    /**
     * Update dimensions for container, pane, and background of the WhiteBoard drawing region.
     * @param x starting x.
     * @param y starting y.
     * @param w width.
     * @param h height.
     */
    public void setDims(double x, double y, double w, double h) {
        pane_whiteBoard_drawing_container.getChildren().clear();
        addListeners();

        pane_whiteBoard_drawing_container.setBackground(null);

        // Update sizies for container and pane.
        pane_whiteBoard_drawing_container.setLayoutX(x);
        pane_whiteBoard_drawing_container.setLayoutY(y);
        pane_whiteBoard_drawing_container.setPrefSize(w, h);
        pane_whiteBoard_drawing_container.setMaxSize(w, h);
        pane_whiteBoard_drawing_container.setMinSize(w, h);

        pane_whiteBoard_drawing.setLayoutX(x);
        pane_whiteBoard_drawing.setLayoutY(y);
        pane_whiteBoard_drawing.setPrefSize(w, h);
        pane_whiteBoard_drawing.setMaxSize(w, h);
        pane_whiteBoard_drawing.setMinSize(w, h);

        pane_whiteBoard_drawing_container.getChildren().add(pane_whiteBoard_drawing);

        // Set the background.
        BackgroundFill backgroundFill = new BackgroundFill(
                WhiteBoardModel.getBackgroundColour(),
                CornerRadii.EMPTY,
                Insets.EMPTY
        );
//        BackgroundFill bf = new BackgroundFill();
        Background background = new Background(backgroundFill);
        pane_whiteBoard_drawing_container.setBackground(background);

        // redraw gird lines.
        drawGridBackground();
    }

//    private void clearWhiteBoard() {
//        rectangle_whiteBoard_drawing.setFill(BACKGROUND);
//    }

    public void initFields(Parent root) {
        WhiteBoardModel.setParent(root);
        vbox_whiteBoard_backdrop = (VBox) root.lookup("#vbox_whiteBoard_backdrop");
        hbox_whiteBoard_buttons = (HBox) root.lookup("#hbox_whiteBoard_buttons");
        pane_whiteBoard_drawing = (Pane) root.lookup("#pane_whiteBoard_drawing");
        pane_whiteBoard_drawing_container = (Pane) root.lookup("#pane_whiteBoard_drawing_container");
        pane_whiteBoard_container = (Pane) root.lookup("#pane_whiteBoard_container");

        button_whiteBoard_clear = (Button) root.lookup("#button_whiteBoard_clear");
        slider_whiteBoard_red_colour = (Slider) root.lookup("#slider_whiteBoard_red_colour");
        slider_whiteBoard_green_colour = (Slider) root.lookup("#slider_whiteBoard_green_colour");
        slider_whiteBoard_blue_colour = (Slider) root.lookup("#slider_whiteBoard_blue_colour");
        rectangle_whiteBoard_marker_colour = (Rectangle) root.lookup("#rectangle_whiteBoard_marker_colour");
//        rectangle_whiteBoard_drawing = (Rectangle) root.lookup("#rectangle_whiteBoard_drawing");

        drawGridBackground();
//        addTestLines();
        addTestAdjustable();

        addListeners();

        WhiteBoardModel.updateWhiteBoardRed(slider_whiteBoard_red_colour.getValue());
        WhiteBoardModel.updateWhiteBoardGreen(slider_whiteBoard_green_colour.getValue());
        WhiteBoardModel.updateWhiteBoardBlue(slider_whiteBoard_blue_colour.getValue());

    }

    /**
     * Create a grid pattern within the drawing container pane.
     * Goes underneath the drawing pane. Grid lines are visible
     * through the transparent pane.
     */
    public void drawGridBackground() {
        System.err.println("DRAWING BACKGROUND");
        if (!WhiteBoardModel.check_drawGrid) {
            return;
        }
        System.out.println("containerX: " + pane_whiteBoard_drawing_container.getLayoutX());
        System.out.println("containerY: " + pane_whiteBoard_drawing_container.getLayoutY());
        System.out.println("paneX: " + pane_whiteBoard_drawing.getLayoutX());
        System.out.println("paneY: " + pane_whiteBoard_drawing.getLayoutY());
        System.out.println("pane_whiteBoard_drawing_container.getWidth(): " + pane_whiteBoard_drawing_container.getWidth());
        System.out.println("pane_whiteBoard_drawing_container.getMaxWidth(): " + pane_whiteBoard_drawing_container.getMaxWidth());
        System.out.println("pane_whiteBoard_drawing_container.getMinWidth(): " + pane_whiteBoard_drawing_container.getMinWidth());
        System.out.println("pane_whiteBoard_drawing_container.getPrefWidth(): " + pane_whiteBoard_drawing_container.getPrefWidth());
        System.out.println("pane_whiteBoard_drawing_container.getBoundsInLocal(): " + pane_whiteBoard_drawing_container.getBoundsInLocal());
        System.out.println("pane_whiteBoard_drawing_container.getLayoutBounds(): " + pane_whiteBoard_drawing_container.getLayoutBounds());
        System.out.println("pane_whiteBoard_drawing_container.getBoundsInParent(): " + pane_whiteBoard_drawing_container.getBoundsInParent());
        double width = pane_whiteBoard_drawing_container.getPrefWidth();
        double height = pane_whiteBoard_drawing_container.getPrefHeight();
        double top = pane_whiteBoard_drawing_container.getLayoutY();
        top = 0;
        double bottom = top + height;
        double left = pane_whiteBoard_drawing_container.getLayoutX();
        left = 0;
        double right = left + width;

//        double width = pane_whiteBoard_drawing_container.getBoundsInParent().getWidth();
//        double height = pane_whiteBoard_drawing_container.getBoundsInParent().getHeight();
//        double top = pane_whiteBoard_drawing_container.getBoundsInParent().getMinY();
//        double bottom = pane_whiteBoard_drawing_container.getBoundsInParent().getMaxY();
//        double left = pane_whiteBoard_drawing_container.getBoundsInParent().getMinX();
//        double right = pane_whiteBoard_drawing_container.getBoundsInParent().getMaxX();
        // Draws diagonal line for dimensions
//        Line lt = new Line(left, top, right, bottom);
//        lt.setStroke(Color.ORANGE);
//        lt.setStrokeWidth(5);
//        pane_whiteBoard_drawing_container.getChildren().add(lt);

        int cellWidth = WhiteBoardModel.CELL_WIDTH;
        int cellHeight = WhiteBoardModel.CELL_HEIGHT;
        Paint lineColour = WhiteBoardModel.GRID_LINE_COLOUR;

        int cols = (int) width / cellWidth;
        int rows = (int) height / cellHeight;
//        System.out.println("rows: " + rows + "\ncols: " + cols + "\nleft: " + left + "\ntop: " + top + "\nright: " + right + "\nbottom: " + bottom + "\nwidth: " + width + "\nheight: " + height + "\ncellWidth: " + cellWidth + "\ncellHeight: " + cellHeight);
        for (int i = 0; i < rows + 1; i++) {
            double y1 = (i * cellHeight) + top;
            Line l = new Line(left, y1, right, y1);
            l.setStroke(lineColour);
            pane_whiteBoard_drawing_container.getChildren().add(l);
        }
        for (int j = 0; j < cols + 1; j++) {
            double x1 = (j * cellWidth) + left;
            Line l = new Line(x1, top, x1, bottom);
            l.setStroke(lineColour);
            pane_whiteBoard_drawing_container.getChildren().add(l);
        }
        pane_whiteBoard_drawing.toFront();
    }

    /**
     * Create a test AdjustableTriangle.
     */
    public void addTestAdjustable() {
        System.out.println("Adding Test Adjustable");
        Line a = new Line(60, 100, 160, 125);
        Line b = new Line(75, 81, 130, 225);
        Line c = new Line(145, 71, 100, 205);
        AdjustableTriangle t = new AdjustableTriangle("T", a, b, c);

//        WhiteBoardModel.addTriangle(t);
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

        ArrayList<Line> lines = new ArrayList<>(
                Arrays.asList(
                        a1, a2, b1, b2, c1, c2, d1, d2,
                        e1, e2, f1, f2, g1, g2, h1, h2
                )
        );

        for (Line l : lines) {
            l.setStroke(Color.GREEN);
            l.setStrokeWidth(3);
//            WhiteBoardModel.addLine(l);
        }
        pane_whiteBoard_drawing.getChildren().addAll(lines);

//        this.checkTriangles();
        this.draw();
    }

    /**
     * After all fields are initialized add listeners;
     *     - mouse pressed:
     *          drawing pane
     *     - mouse draggeed:
     *          drawing pane
     *          red slider
     *          green slider
     *          blue slider
     *     - mouse clicked:
     *          clear button
     *          red slider
     *          green slider
     *          blue slider
     */
    private void addListeners() {

        //          -   Marker colour sliders  -

        slider_whiteBoard_red_colour.setOnMouseDragged(event -> {
            WhiteBoardModel.updateWhiteBoardRed(slider_whiteBoard_red_colour.getValue());
            this.updateMarkerColour();
        });

        slider_whiteBoard_green_colour.setOnMouseDragged(event -> {
            WhiteBoardModel.updateWhiteBoardGreen(slider_whiteBoard_green_colour.getValue());
            this.updateMarkerColour();
        });

        slider_whiteBoard_blue_colour.setOnMouseDragged(event -> {
            WhiteBoardModel.updateWhiteBoardBlue(slider_whiteBoard_blue_colour.getValue());
            this.updateMarkerColour();
        });

        slider_whiteBoard_red_colour.setOnMouseClicked(event -> {
            WhiteBoardModel.updateWhiteBoardRed(slider_whiteBoard_red_colour.getValue());
            this.updateMarkerColour();
        });

        slider_whiteBoard_green_colour.setOnMouseClicked(event -> {
            WhiteBoardModel.updateWhiteBoardGreen(slider_whiteBoard_green_colour.getValue());
            this.updateMarkerColour();
        });

        slider_whiteBoard_blue_colour.setOnMouseClicked(event -> {
            WhiteBoardModel.updateWhiteBoardBlue(slider_whiteBoard_blue_colour.getValue());
            this.updateMarkerColour();
        });


        //          -   Clear button  -

        button_whiteBoard_clear.setOnMouseClicked(event -> {
            pane_whiteBoard_drawing.getChildren().clear();
//            WhiteBoardModel.clearWhiteBoardLines();
//            WhiteBoardModel.clearWhiteBoardTriangles();
            WhiteBoardModel.resetTriangleNumber();
            drawGridBackground();
//            this.addTestAdjustable();
        });


        //          -   Drawing pane  -

        pane_whiteBoard_drawing.setOnMousePressed(event -> {
            double x = event.getX();
            double y = event.getY();
            if (!inBounds(x, y)) {
                WhiteBoardModel.setPointFirst(null);
                WhiteBoardModel.setPointLast(null);
                return;
            }
            boolean markerClicked = false;
            System.out.println("CURRENT TRIANGLES:\n" + WhiteBoardModel.getWhiteBoardTriangles());
            for (Triangle t : WhiteBoardModel.getWhiteBoardTriangles()) {
                if (t.getClass() == AdjustableTriangle.class) {
                    System.out.println("CLICKED A MARKER:\n" + t);
                    AdjustableTriangle at = (AdjustableTriangle) t;
                    markerClicked = at.selectMarker(x, y);
//                    draw();
                }
            }
            System.out.println("Mouse pressed on white board");

            System.out.println("markerClicked: " + markerClicked);
            if (!markerClicked) {
//          System.out.println("Top node: " + pane_whiteBoard_drawing.g);
//                System.out.println("clicked: " + clickedNothing(x, y));
                System.out.println("mouse pressed\nchildren (" + pane_whiteBoard_drawing.getChildren().size() + ")\n" + pane_whiteBoard_drawing.getChildren());
                WhiteBoardModel.setPointFirst(new Point2D(x, y));
                WhiteBoardModel.setPointLast(new Point2D(x, y));
            }
        });

        pane_whiteBoard_drawing.setOnMouseDragged(event -> {
            double x = event.getX();
            double y = event.getY();
            boolean markerClicked = false;
            if (WhiteBoardModel.getAdjustingShape() != null) {
                for (Triangle t : WhiteBoardModel.getWhiteBoardTriangles()) {
                    if (t.getClass() == AdjustableTriangle.class) {
                        AdjustableTriangle at = (AdjustableTriangle) t;
                        markerClicked = at.translateMarker(x, y);
//                    draw();
                    }
                }
            }
//            System.out.println("markerClicked: " + markerClicked);
            if (!markerClicked) {
                Line drawingLine = WhiteBoardModel.getDrawingLine();
                pane_whiteBoard_drawing.getChildren().remove(drawingLine);
                WhiteBoardModel.setPointLast(new Point2D(x, y));
                drawingLine = WhiteBoardModel.getDrawingLine();
                pane_whiteBoard_drawing.getChildren().add(drawingLine);
            }
        });

        pane_whiteBoard_drawing.setOnMouseReleased(event -> {
            double x = event.getX();
            double y = event.getY();
            if (!inBounds(x, y)) {
                Line drawingLine = WhiteBoardModel.getDrawingLine();
                pane_whiteBoard_drawing.getChildren().remove(drawingLine);
                WhiteBoardModel.setPointFirst(null);
                WhiteBoardModel.setPointLast(null);
                return;
            }
            boolean markerClicked = false;
            ArrayList<Triangle> triangles = WhiteBoardModel.getWhiteBoardTriangles();
//            ArrayList<Triangle> triangles = WhiteBoardModel.getWhiteBoardTriangles(pane_whiteBoard_drawing.getChildren());
//            for (Triangle t : triangles) {
//
//
//                Polygon poly = t.getPolygon();
//                if (!pane_whiteBoard_drawing.getChildren().contains(poly)) {
//                    pane_whiteBoard_drawing.getChildren().add(poly);
//                }
//
//
//                if (t.getClass() == AdjustableTriangle.class) {
//                    AdjustableTriangle at = (AdjustableTriangle) t;
//                    markerClicked = at.deselectMarker(x, y);
////                    draw();
//                }
//            }
            System.out.println("Mouse released on white board");
            System.out.println("markerClicked: " + markerClicked);
            if (!markerClicked) {
                Line drawingLine = WhiteBoardModel.getDrawingLine();
                pane_whiteBoard_drawing.getChildren().remove(drawingLine);
                WhiteBoardModel.setPointLast(new Point2D(x, y));
//                Line l = WhiteBoardModel.getDrawingLine();
                drawingLine = WhiteBoardModel.getDrawingLine();
                pane_whiteBoard_drawing.getChildren().add(drawingLine);
//                triangles.removeAll(WhiteBoardModel.getWhiteBoardTriangles());
                for (Triangle t : triangles) {
                    WhiteBoardModel.addTriangle(t);
                }
//                WhiteBoardModel.addLine(l);
//                this.checkTriangles();
//                this.drawLines();
                WhiteBoardModel.setPointFirst(null);
                WhiteBoardModel.setPointLast(null);
            }
            System.out.println("mouse pressed\nchildren (" + pane_whiteBoard_drawing.getChildren().size() + ")\n" + pane_whiteBoard_drawing.getChildren());

            draw();
        });
    }

    public boolean inBounds(double x, double y) {
//        System.out.println("x, y: " + x + ", " + y);
//        System.out.println("pane_whiteBoard_drawing.getLayoutBounds(): " + pane_whiteBoard_drawing.getLayoutBounds());
//        System.out.println("pane_whiteBoard_drawing.getBoundsInLocal(): " + pane_whiteBoard_drawing.getBoundsInLocal());
//        System.out.println("pane_whiteBoard_drawing.getBoundsInParent(): " + pane_whiteBoard_drawing.getBoundsInParent());
        return pane_whiteBoard_drawing.getLayoutBounds().contains(x, y);
    }

//    public boolean clickedNothing(double mouseX, double mouseY) {
//        for (Node child : pane_whiteBoard_drawing.getChildren()) {
//            if (child.getLayoutBounds().contains(mouseX, mouseY)) {
//                System.out.println("child: " + child);
//                return false;
//            }
//        }
//        return true;
//    }

//    /**
//     * Check WhiteBoard for all triangles.
//     */
//    public void checkTriangles() {
////        ArrayList<Triangle> triangles = WhiteBoardModel.getWhiteBoardTriangles();
//        ArrayList<Triangle> triangles = WhiteBoardModel.checkWhiteBoardTriangles();
//        if (triangles.size() > 0) {
//            for (Triangle t : triangles) {
////                Triangle t =
//                WhiteBoardModel.removeLines(t.a.getLine(), t.b.getLine(), t.c.getLine());
//                WhiteBoardModel.addTriangle(t.polygon, t);
//            }
//        }
//    }

//    public Line createMarkedLine() {
////        Point2D first = WhiteBoardModel.getPointFirst();
////        Point2D last = WhiteBoardModel.getPointLast();
////        Line l = new Line(first.getX(), first.getY(), last.getX(), last.getY());
//        Line l = WhiteBoardModel.getDrawingLine(); //(first.getX(), first.getY(), last.getX(), last.getY());
//        Color paint = WhiteBoardModel.getWhiteBoardColour();
//        l.setFill(paint);
//        l.setStroke(paint);
//        l.setStrokeWidth(5);
//        return l;
//    }

    private void updateMarkerColour() {
        double[] vals = WhiteBoardModel.getWhiteBoardMarkerColour();
        double r = vals[0], g = vals[1], b = vals[2], a = vals[3];
        rectangle_whiteBoard_marker_colour.setFill(new Color(r, g, b, a));
    }

//    public ArrayList<Node> drawLines() {
//        Point2D first = WhiteBoardModel.getPointFirst();
//        Point2D last = WhiteBoardModel.getPointLast();
//        ArrayList<Line> lines = WhiteBoardModel.getWhiteBoardLines(pane_whiteBoard_drawing.getChildren());
////        pane_whiteBoard_drawing.getChildren().clear();
//        //            pane_whiteBoard_drawing.getChildren().add(line);
//        ArrayList<Node> nodes = new ArrayList<>(lines);
//        if (first != null && last != null) {
//            Line l = createMarkedLine();
//            if (!pane_whiteBoard_drawing.getChildren().contains(l)) {
////                pane_whiteBoard_drawing.getChildren().add(l);
//                nodes.add(l);
//            }
//        }
//
//        HashMap<Line, ArrayList<Line>> intersectingLines = WhiteBoardModel.getIntersectingWhiteBoardLines(pane_whiteBoard_drawing.getChildren());
//        for (Line a : intersectingLines.keySet()) {
//            ArrayList<Line> intersections = intersectingLines.get(a);
//            for (Line b : intersections) {
//                ArrayList<Node> markers = this.drawIntersections(a, b);
////                pane_whiteBoard_drawing.getChildren().addAll(markers);
//                nodes.addAll(markers);
//            }
//        }
//        this.drawTriangles();
//        return nodes;
//    }

    public ArrayList<Node> drawTriangles() {
        ArrayList<Node> nodes = new ArrayList<>();
//        ArrayList<Triangle> triangles = WhiteBoardModel.getWhiteBoardTriangles();
        ArrayList<Triangle> triangles = WhiteBoardModel.getWhiteBoardTriangles();
        for (Triangle t : triangles) {
            Line a = t.getSideA().getLine();
            Line b = t.getSideB().getLine();
            Line c = t.getSideC().getLine();
//            WhiteBoardModel.removeLines(a, b, c);
            nodes.addAll(drawIntersectionsSupplementA(a, b));
            nodes.addAll(drawIntersectionsSupplementB(a, c));
            nodes.addAll(drawIntersectionsSupplementA(b, c));
//            nodes.add(t.getPolygon());
            Point2D center = t.centroid();
            Circle circle = new Circle(center.getX(), center.getY(), 3, Color.DODGERBLUE);
//            System.out.println("t: " + t + "\ncentroid: " + center);
//            pane_whiteBoard_drawing.getChildren().add(circle);
            if (t.getClass() == AdjustableTriangle.class) {
//                System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\tAdjustable Triangle\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
                AdjustableTriangle at = (AdjustableTriangle) t;
                ArrayList<Circle> corners = at.getCornerMarkers();
                Circle circleA = corners.get(0);
                Circle circleB = corners.get(1);
                Circle circleC = corners.get(2);

//                circleA.setOnMousePressed(event -> {
////                    System.out.println("markerA OnMousePressed");
//                    double x = event.getX();
//                    double y = event.getY();
//                    at.translateCornerA(x, y);
////                    at.markerA.setCenterX(x);
////                    at.markerA.setCenterY(y);
////                    this.drawLines();
//                });
//
//                circleA.setOnMouseDragged(event -> {
////                    System.out.println("markerA OnMouseDragged");
//                    double x = event.getX();
//                    double y = event.getY();
//                    at.translateCornerA(x, y);
////                    at.markerA.setCenterX(x);
////                    at.markerA.setCenterY(y);
////                    this.drawLines();
//                });

//                pane_whiteBoard_drawing.getChildren().addAll(circleA, circleB, circleC);
                nodes.addAll(Arrays.asList(circle, circleA, circleB, circleC));
            }
//            WhiteBoardModel.addLines(t.getSideA().getLine(), t.getSideB().getLine(), t.getSideC().getLine());
//            pane_whiteBoard_drawing.getChildren().addAll(t.getSideA().getLine(), t.getSideB().getLine(), t.getSideC().getLine());
            nodes.addAll(Arrays.asList(t.getSideA().getLine(), t.getSideB().getLine(), t.getSideC().getLine()));
        }
        return nodes;
    }

    // Main drawing method.
    // Draws all lines and triangles to the WhiteBoard.
    public void draw() {
//        pane_whiteBoard_drawing.getChildren().clear();
//        drawGridBackground();
//        pane_whiteBoard_drawing.getChildren().addAll(this.drawLines());
        ArrayList<Node> triangleData = drawTriangles();
        for (Node n : triangleData) {
            if (!pane_whiteBoard_drawing.getChildren().contains(n)) {
                pane_whiteBoard_drawing.getChildren().addAll(n);
            }
        }
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
    public ArrayList<Node> drawAngleArc(Triangle t, Point2D p, double angleA, double angleB) {
        double radius = 22;
        double angle = t.getAngleC().getAngle();
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
        Point2D p = WhiteBoardModel.intersectionPoint(a, b);
        Point2D ptA = new Point2D(a.getEndX(), a.getEndY());
        Point2D ptB = new Point2D(b.getEndX(), b.getEndY());

        Line la = new Line(p.getX(), p.getY(), a.getEndX(), a.getEndY());
        Line lb = new Line(p.getX(), p.getY(), b.getEndX(), b.getEndY());
        Line lc = new Line(a.getEndX(), a.getEndY(), b.getEndX(), b.getEndY());

//        double lenA = p.distance(ptA);
//        double lenB = p.distance(ptB);
//        double lenC = ptB.distance(ptA);
        Edge edgeA = new Edge("edge a", la.getStartX(), la.getStartY(), la.getEndX(), la.getEndY());
        Edge edgeB = new Edge("edge b", lb.getStartX(), lb.getStartY(), lb.getEndX(), lb.getEndY());
        Edge edgeC = new Edge("edge c", lc.getStartX(), lc.getStartY(), lc.getEndX(), lc.getEndY());
        Triangle t = new Triangle("", edgeA, edgeB, edgeC, null, null, null);

        double angleB = 360 - Vector.computeAngle(p.getX(), p.getY(), b.getEndX(), b.getEndY());
        double angleA = 360 - Vector.computeAngle(p.getX(), p.getY(), a.getEndX(), a.getEndY());

        double halfX = (ptB.getX() + ptA.getX()) / 2;
        double halfY = (ptB.getY() + ptA.getY()) / 2;
        Circle mark = new Circle(halfX, halfY, 5, Color.ORANGE);

        Tooltip toolTipSideA = new Tooltip("side a: " + edgeA);
        Tooltip.install(la, toolTipSideA);
        Tooltip toolTipSideB = new Tooltip("side b: " + edgeB);
        Tooltip.install(lb, toolTipSideB);
        Tooltip toolTipSideC = new Tooltip("side c: " + edgeC);
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
        Point2D p = WhiteBoardModel.intersectionPoint(a, b);
        Point2D ptA = new Point2D(xa, ya);
        Point2D ptB = new Point2D(xb, yb);

        Line la = new Line(p.getX(), p.getY(), xa, ya);
        Line lb = new Line(p.getX(), p.getY(), xb, yb);
        Line lc = new Line(xa, ya, xb, yb);

//        double lenA = p.distance(ptA);
//        double lenB = p.distance(ptB);
//        double lenC = ptB.distance(ptA);
        Edge edgeA = new Edge("edge a", la.getStartX(), la.getStartY(), la.getEndX(), la.getEndY());
        Edge edgeB = new Edge("edge b", lb.getStartX(), lb.getStartY(), lb.getEndX(), lb.getEndY());
        Edge edgeC = new Edge("edge c", lc.getStartX(), lc.getStartY(), lc.getEndX(), lc.getEndY());
        Triangle t = new Triangle("", edgeA, edgeB, edgeC, null, null, null);

        double angleB = 360 - Vector.computeAngle(p.getX(), p.getY(), xb, yb);
        double angleA = 360 - Vector.computeAngle(p.getX(), p.getY(), xa, ya);

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
        Point2D p = WhiteBoardModel.intersectionPoint(a, b);
        Point2D ptA = new Point2D(xa, ya);
        Point2D ptB = new Point2D(xb, yb);

        Line la = new Line(p.getX(), p.getY(), xa, ya);
        Line lb = new Line(p.getX(), p.getY(), xb, yb);
        Line lc = new Line(xa, ya, xb, yb);

//        double lenA = p.distance(ptA);
//        double lenB = p.distance(ptB);
//        double lenC = ptB.distance(ptA);
        Edge edgeA = new Edge("edge a", la.getStartX(), la.getStartY(), la.getEndX(), la.getEndY());
        Edge edgeB = new Edge("edge b", lb.getStartX(), lb.getStartY(), lb.getEndX(), lb.getEndY());
        Edge edgeC = new Edge("edge c", lc.getStartX(), lc.getStartY(), lc.getEndX(), lc.getEndY());
        Triangle t = new Triangle("", edgeA, edgeB, edgeC, null, null, null);

        double angleB = 360 - Vector.computeAngle(p.getX(), p.getY(), xb, yb);
        double angleA = 360 - Vector.computeAngle(p.getX(), p.getY(), xa, ya);

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
        Point2D p = WhiteBoardModel.intersectionPoint(a, b);
        Point2D ptA = new Point2D(xa, ya);
        Point2D ptB = new Point2D(xb, yb);

        Line la = new Line(p.getX(), p.getY(), xa, ya);
        Line lb = new Line(p.getX(), p.getY(), xb, yb);
        Line lc = new Line(xa, ya, xb, yb);

        double lenA = p.distance(ptA);
        double lenB = p.distance(ptB);
        double lenC = ptB.distance(ptA);
        Edge edgeA = new Edge("edge a", la.getStartX(), la.getStartY(), la.getEndX(), la.getEndY());
        Edge edgeB = new Edge("edge b", lb.getStartX(), lb.getStartY(), lb.getEndX(), lb.getEndY());
        Edge edgeC = new Edge("edge c", lc.getStartX(), lc.getStartY(), lc.getEndX(), lc.getEndY());
        Triangle t = new Triangle("", edgeA, edgeB, edgeC, null, null, null);

        double angleB = 360 - Vector.computeAngle(p.getX(), p.getY(), xb, yb);
        double angleA = 360 - Vector.computeAngle(p.getX(), p.getY(), xa, ya);

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
        if (WhiteBoardModel.check_drawIntersectionsInterior) {
            markers.addAll(this.drawIntersectionsInterior(a, b));
        }
        if (WhiteBoardModel.check_drawIntersectionsSupplementA) {
            markers.addAll(this.drawIntersectionsSupplementA(a, b));
        }
        if (WhiteBoardModel.check_drawIntersectionsSupplementB) {
            markers.addAll(this.drawIntersectionsSupplementB(a, b));
        }
        if (WhiteBoardModel.check_drawIntersectionsOpposite) {
            markers.addAll(this.drawIntersectionsOpposite(a, b));
        }
        return markers;
    }
}

package sample.Version_4;

import javafx.geometry.Point2D;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;

public class Edge {

    private String name;
    private Line line;
    private double halfMarkCircleRadius;
    private Color halfMarkCircleColour;

    /*////////////////////
    //   Constructors   //
    ////////////////////*/

    public Edge(String name, double x1, double y1, double x2, double y2) {
        this.name = name;
        initHalfMarkDefaults();

        Line line = initLine(x1, y1, x2, y2);
        setLine(line);
    }

    public Edge(String name, double x1, double y1, double x2, double y2, Color color) {
        this.name = name;
        initHalfMarkDefaults();

        Line line = initLine(x1, y1, x2, y2);
        line.setFill(color);
        line.setStroke(color);
        setLine(line);
    }

    public Edge(String name, double x1, double y1, double x2, double y2, Color color, double strokeWidth) {
        this.name = name;
        initHalfMarkDefaults();

        Line line = initLine(x1, y1, x2, y2);
        line.setFill(color);
        line.setStroke(color);
        line.setStrokeWidth(strokeWidth);
        setLine(line);
    }

    public Edge(String name, Line line) {
        this.name = name;
        this.line = line;
        initHalfMarkDefaults();
    }

    /*////////////////////
    //      Getters     //
    ////////////////////*/

    public String getName() {
        return name;
    }

    public double getLength() {
        return getX1Y1().distance(getX2Y2());
    }

    public Line getLine() {
        return line;
    }

    public double getX1() {
        return line.getStartX();
    }

    public double getX2() {
        return line.getEndX();
    }

    public double getY1() {
        return line.getStartY();
    }

    public double getY2() {
        return line.getEndY();
    }

    public Point2D getX1Y1() {
        return new Point2D(getX1(), getY1());
    }

    public Point2D getX2Y2() {
        return new Point2D(getX2(), getY2());
    }

    public double getHalfX() {
        return (getX1() + getX2()) / 2;
    }

    public double getHalfY() {
        return (getY1() + getY2()) / 2;
    }

    public Point2D getHalfPoint() {
        return new Point2D(getHalfX(), getHalfY());
    }

    public double getHalfMarkCircleRadius() {
        return halfMarkCircleRadius;
    }

    public Color getHalfMarkCircleColour() {
        return halfMarkCircleColour;
    }

    public Circle getHalfMarkCircle() {
        return new Circle(getHalfX(), getHalfY(), getHalfMarkCircleRadius(), getHalfMarkCircleColour());
    }

    /*////////////////////
    //      Setters     //
    ////////////////////*/

    public void setName(String name) {
        this.name = name;
    }

    public void setLine(Line line) {
        this.line = line;
    }

    public void setX1(double x1) {
        this.line.setStartX(x1);
    }

    public void setX2(double x2) {
        this.line.setEndX(x2);
    }

    public void setY1(double y1) {
        this.line.setStartY(y1);
    }

    public void setY2(double y2) {
        this.line.setEndY(y2);
    }

    public void setX1Y1(double x1, double y1) {
        setX1(x1);
        setY1(y1);
    }

    public void setX2Y2(double x2, double y2) {
        setX2(x2);
        setY2(y2);
    }

    public void setHalfMarkCircleRadius(double r) {
        this.halfMarkCircleRadius = r;
    }

    public void setHalfMarkCircleColour(Color halfMarkCircleColour) {
        this.halfMarkCircleColour = halfMarkCircleColour;
    }





    public boolean known() {
        return getLength() != 0;
    }

    public void initHalfMarkDefaults() {
        this.halfMarkCircleRadius = 3;
        this.halfMarkCircleColour = Color.ORANGE;
//        getHalfPoint().angle(getHalfPoint());
    }

    public Line initLine(double x1, double y1, double x2, double y2) {
        return new Line(x1, y1, x2, y2);
    }

    public String toString() {
        return "<Edge " + this.name + ", line: " + line + ", (" + getLength() + ")>";
    }
}
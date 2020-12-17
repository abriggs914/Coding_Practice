package sample.Version_4;

import javafx.geometry.Point2D;
import javafx.scene.Node;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;

import java.util.ArrayList;
import java.util.Arrays;

public class AdjustableTriangle extends Triangle{

    private double radius;

//    public Circle markerA;
//    private Circle markerB;
//    private Circle markerC;

    private Color markerAColour;
    private Color markerBColour;
    private Color markerCColour;

    private boolean selectedCornerA;
    private boolean selectedCornerB;
    private boolean selectedCornerC;

    public AdjustableTriangle(String name, Line a, Line b, Line c) {
        super(name, a, b, c);

        this.radius = 8;
        this.markerAColour = new Color(1, 0.55, 0.55, 0.7);
        this.markerBColour = new Color(0.55, 1, 0.55, 0.7);
        this.markerCColour = new Color(0.55, 0.55, 1, 0.7);
//        this.addCornerMarkers();
    }

//    private void addCornerMarkers() {
//        Point2D C = c.getX1Y1(); //this.intersectionAB;
//        Point2D B = b.getX1Y1(); //this.intersectionAC;
//        Point2D A = a.getX1Y1(); //this.intersectionBC;
//
//        this.markerA = new Circle(A.getX(), A.getY(), this.radius, this.markerAColour);
//        this.markerB = new Circle(B.getX(), B.getY(), this.radius, this.markerBColour);
//        this.markerC = new Circle(C.getX(), C.getY(), this.radius, this.markerCColour);
//    }

    public Circle getCornerMarkerA() {
        Point2D A = getSideA().getX1Y1();
        return new Circle(A.getX(), A.getY(), radius, markerAColour);
    }

    public Circle getCornerMarkerB() {
        Point2D B = getSideB().getX1Y1();
        return new Circle(B.getX(), B.getY(), radius, markerBColour);
    }

    public Circle getCornerMarkerC() {
        Point2D C = getSideC().getX1Y1();
        return new Circle(C.getX(), C.getY(), radius, markerCColour);
    }

    public ArrayList<Circle> getCornerMarkers() {
        return new ArrayList<>(Arrays.asList(getCornerMarkerA(), getCornerMarkerB(), getCornerMarkerC()));
    }

//    public void markerAListener() {
//        this.markerA.setOnMousePressed(event -> {
//            System.out.println("markerA OnMousePressed");
//            double x = event.getX();
//            double y = event.getY();
//            this.translateCornerA(x, y);
//            this.markerA.setCenterX(x);
//            this.markerA.setCenterY(y);
//        });
//
//        this.markerA.setOnMouseDragged(event -> {
//            System.out.println("markerA OnMouseDragged");
//            double x = event.getX();
//            double y = event.getY();
//            this.translateCornerA(x, y);
//            this.markerA.setCenterX(x);
//            this.markerA.setCenterY(y);
//        });
//    }

//    public Circle getMarkerA() {
//        return markerA;
//    }

//    public void setMarkerA(Circle markerA) {
//        this.markerA = markerA;
//    }

//    public Circle getMarkerB() {
//        return markerB;
//    }

//    public void setMarkerB(Circle markerB) {
//        this.markerB = markerB;
//    }

//    public Circle getMarkerC() {
//        return markerC;
//    }

//    public void setMarkerC(Circle markerC) {
//        this.markerC = markerC;
//    }

    public Color getMarkerAColour() {
        return markerAColour;
    }

    public void setMarkerAColour(Color markerAColour) {
        this.markerAColour = markerAColour;
    }

    public Color getMarkerBColour() {
        return markerBColour;
    }

    public void setMarkerBColour(Color markerBColour) {
        this.markerBColour = markerBColour;
    }

    public Color getMarkerCColour() {
        return markerCColour;
    }

    public void setMarkerCColour(Color markerCColour) {
        this.markerCColour = markerCColour;
    }

    public void selectCornerA() {
        this.selectedCornerA = true;
        this.markerAColour = markerAColour.darker();
    }

    public void selectCornerB() {
        this.selectedCornerB = true;
        this.markerBColour = markerBColour.darker();
    }

    public void selectCornerC() {
        this.selectedCornerC = true;
        this.markerCColour = markerCColour.darker();
    }

    public void deselectCornerA() {
        this.selectedCornerA = false;
        this.markerAColour = markerAColour.brighter();
    }

    public void deselectCornerB() {
        this.selectedCornerB = false;
        this.markerBColour = markerBColour.brighter();
    }

    public void deselectCornerC() {
        this.selectedCornerC = false;
        this.markerCColour = markerCColour.brighter();
    }

    // Set the corner marker located at mouse coordinates x and y, to be selected
    public boolean selectMarker(double x, double y) {
        Point2D mouse = new Point2D(x, y);
        if (getCornerMarkerA().contains(mouse)){
            System.out.println("Selecting corner A");
            selectCornerA();
        }
        else if (getCornerMarkerB().contains(mouse)){
            System.out.println("Selecting corner B");
            selectCornerB();
        }
        else if (getCornerMarkerC().contains(mouse)){
            System.out.println("Selecting corner C");
            selectCornerC();
        }
        else {
            return false;
        }
        return true;
    }

    // Set the corner marker located at mouse coordinates x and y, to be unselected
    public boolean deselectMarker(double x, double y) {
        Point2D mouse = new Point2D(x, y);
        if (getCornerMarkerA().contains(mouse)){
            deselectCornerA();
        }
        else if (getCornerMarkerB().contains(mouse)){
            deselectCornerB();
        }
        else if (getCornerMarkerC().contains(mouse)){
            deselectCornerC();
        }
        else {
            return false;
        }
        return true;
    }

    // Set the corner marker located at mouse coordinates x and y, to be selected
    public boolean translateMarker(double x, double y) {
        Point2D mouse = new Point2D(x, y);
        if (getCornerMarkerA().contains(mouse)){
            translateCornerA(x, y);
        }
        else if (getCornerMarkerA().contains(mouse)){
            translateCornerB(x, y);
        }
        else if (getCornerMarkerA().contains(mouse)){
            translateCornerC(x, y);
        }
        else {
            return false;
        }
        return true;
    }
}

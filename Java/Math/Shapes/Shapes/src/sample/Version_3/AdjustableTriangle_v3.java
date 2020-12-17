package sample;

import javafx.geometry.Point2D;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import sample.Version_3.Triangle_v3;

public class AdjustableTriangle_v3 extends Triangle_v3 {

    private double radius;

    public Circle markerA;
    private Circle markerB;
    private Circle markerC;

    private Color markerAColour;
    private Color markerBColour;
    private Color markerCColour;

    public AdjustableTriangle_v3(String name, Line a, Line b, Line c) {
        super(name, a, b, c);

        this.radius = 8;
        this.markerAColour = new Color(1, 0.55, 0.55, 0.7);
        this.markerBColour = new Color(0.55, 1, 0.55, 0.7);
        this.markerCColour = new Color(0.55, 0.55, 1, 0.7);
        this.addCornerMarkers();
    }

    private void addCornerMarkers() {
        Point2D C = this.intersectionAB;
        Point2D B = this.intersectionAC;
        Point2D A = this.intersectionBC;

        this.markerA = new Circle(A.getX(), A.getY(), this.radius, this.markerAColour);
        this.markerB = new Circle(B.getX(), B.getY(), this.radius, this.markerBColour);
        this.markerC = new Circle(C.getX(), C.getY(), this.radius, this.markerCColour);
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

    public Circle getMarkerA() {
        return markerA;
    }

    public void setMarkerA(Circle markerA) {
        this.markerA = markerA;
    }

    public Circle getMarkerB() {
        return markerB;
    }

    public void setMarkerB(Circle markerB) {
        this.markerB = markerB;
    }

    public Circle getMarkerC() {
        return markerC;
    }

    public void setMarkerC(Circle markerC) {
        this.markerC = markerC;
    }

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
}

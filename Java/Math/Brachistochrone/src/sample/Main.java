package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.control.Label;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.scene.text.Font;
import javafx.stage.Stage;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception{
        double WIDTH = 900;
        double HEIGHT = 600;
        // small test
//        double x1 = 4;
//        double y1 = 2;
//        double x2 = 4;
//        double y2 = 4;

        // large test
//        double x1 = 60;
//        double y1 = 200;
//        double x2 = 220;
//        double y2 = 80;

//        double x1 = 20;
//        double y1 = 200;
//        double x2 = 100;
//        double y2 = 25;

//        double x2 = 20;
//        double y2 = 40;
//        double x1 = 40;
//        double y1 = 20;

        // very large test
        double x1 = 20;
        double y1 = 540;
        double x2 = 890;
        double y2 = 88;

//        double x1 = 20;
//        double y1 = 80;
//        double x2 = 140;
//        double y2 = 20;
        int segments = 150;
        double duration = 3.5;
        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));

        Label label = new Label("TOP LABEL");
        label.setFont(new Font(15));
        label.setStyle("-fx-border-color: orange");
        HBox hBox = new HBox(label);
        hBox.setStyle("-fx-border-color: blue");
        Canvas canvas = new Canvas(WIDTH, HEIGHT);//300, 275, Color.color(0.45, 0.85, 0.45, 0.67));
        canvas.setWidth(WIDTH);
        canvas.maxWidth(WIDTH);
        canvas.minWidth(WIDTH);
        canvas.prefWidth(WIDTH);
        canvas.setHeight(HEIGHT);
        canvas.maxHeight(HEIGHT);
        canvas.minHeight(HEIGHT);
        canvas.prefHeight(HEIGHT);
        VBox vBox = new VBox(hBox, canvas);
        vBox.setStyle("-fx-border-color: green");
//        Curve curve = new Curve(x1, y1, x2, y2, 15, 5);
//
//        ArrayList<Double[]> pts = curve.getBrachistochronePoints();
//        int nPoints = pts.size();
//        double[] xs = new double[nPoints];
//        double[] ys = new double[nPoints];
//        double w = 1;
//        double h = 1;

//        canvas.setStyle("-fx-border-color: black");
//        changeCanvasColour(canvas, Color.color(0.86, 0.21, 0.35, 0.85));

//        double s = y1 + y2;
//        double xA = x1;
//        double yA = Math.min(y1, y2);
//        double xB = x2;
//        double yB = Math.max(y1, y2);
//        System.out.println("s: " + s + ", xA: " + xA + ", yA: " + yA + ", xB; " + xB + ", yB: " + yB);
//        canvas.getGraphicsContext2D().strokeLine(x1, yA, x2, yB);

        //////////////////////////////////////////////////////////////////////////

//        changeCanvasColour(canvas, Color.color(0.35, 0.21, 0.86, 0.85));
//        Curve brachistochrone = new Brachistochrone(x1, y1, x2, y2, segments, true);
//        ArrayList<BigDecimal[]> bPoints = brachistochrone.getPoints();
//
//        for (BigDecimal[] point : bPoints) {
//            BigDecimal bdX = point[0];
//            BigDecimal bdY = point[1];
//            double x = bdX.doubleValue();
//            double y = bdY.doubleValue();
//            System.out.println("x: " + x + ", y: " + y);
//            canvas.getGraphicsContext2D().strokeOval(x, y, w, h);
//        }
//
//        // Finding the right-angled triangle to the two given points
//
//        Curve cycloid = new Cycloid(x1, y1, x2, y2, segments, true);
//        System.out.println("Circular points: " + cycloid.getPoints());
//        ArrayList<BigDecimal[]> cPoints = cycloid.getPoints();
//
//        changeCanvasColour(canvas, Color.color(0.4, 0.0, 0.3, 1));
//        for (BigDecimal[] point : cPoints) {
//            BigDecimal cdX = point[0];
//            BigDecimal cdY = point[1];
//            double x = cdX.doubleValue();
//            double y = cdY.doubleValue();
//            System.out.println("x: " + x + ", y: " + y);
//            canvas.getGraphicsContext2D().strokeOval(x, y, w, h);
//        }
//
//
//        Curve parabola = new Parabolic(x1, y1, x2, y2, segments, true);
//        System.out.println("Parabolic points: " + parabola.getPoints());
//        ArrayList<BigDecimal[]> pPoints = parabola.getPoints();
//
//        changeCanvasColour(canvas, Color.color(0.0, 0.45, 0.0, 1));
//        for (BigDecimal[] point : pPoints) {
//            BigDecimal pdX = point[0];
//            BigDecimal pdY = point[1];
//            double x = pdX.doubleValue();
//            double y = pdY.doubleValue();
//            System.out.println("x: " + x + ", y: " + y);
//            canvas.getGraphicsContext2D().strokeOval(x, y, w, h);
//        }

//        Color.color(0.8, 0.6, 0.3, 1);


        //////////////////////////////////////////////////////////////////////////




//        sample.Circle cObject = curve.getCircle();
//        canvas.getGraphicsContext2D().strokeOval(cObject.getMidX() - (15 / 2.), cObject.getMidY() - (15 / 2.), 15, 15);
//
//        double halfX = 0;//Math.abs(x2 - x1) / 2;
//        double halfY = 0;//Math.abs(y2 - y1) / 2;
//        ArrayList<Paint> colours = new ArrayList<>(Arrays.asList(Color.DODGERBLUE, Color.MAGENTA, Color.AQUA, Color.CRIMSON));
//        for (int i = 0; i < pts.size(); i++) {
//            Double[] xyOrig = pts.get(i);
//            Paint col = colours.get(0);
//            canvas.getGraphicsContext2D().setStroke(col);
//            canvas.getGraphicsContext2D().setFill(col);
//            Double[] xy = pts.get(i);
////            Double[] xy = curve.rotatePoint(curve.getCircle().getMidX(), curve.getCircle().getMidY(), xyOrig[0], xyOrig[1], );
////            Double[] xy = new Double[]{xyOrig[0], Math.abs( linear(xyOrig[0], x1, y1, x2, y2) - xyOrig[1]) + linear(xyOrig[0], x1, y1, x2, y2)};
//
//            xs[i] = xy[0] - halfX; //rotatePoint(circle.getMidX(), circle.getMidY(), x, y, 180);
//            ys[i] = xy[1] - halfY;
//            if (0 == 0) {
//                System.out.println("(" + xs[i] + ", -" + ys[i] + ")");
//            }
//
//            canvas.getGraphicsContext2D().strokeOval(xs[i] - (w / 2), ys[i] - (h / 2), w, h);
//            canvas.getGraphicsContext2D().strokeLine(cObject.getMidX() + (w / 2), cObject.getMidY() + (h / 2), xs[i], ys[i]);
//
//
//            // For N, E, S, and W viewa
////            for (int j = 0; j < 360; j += 90) {
////                Paint col = colours.get(j / 90);
////                canvas.getGraphicsContext2D().setStroke(col);
////                canvas.getGraphicsContext2D().setFill(col);
////                Double[] xy = curve.rotatePoint(curve.getCircle().getMidX(), curve.getCircle().getMidY(), xyOrig[0], xyOrig[1], j);
////
////                xs[i] = xy[0] - halfX; //rotatePoint(circle.getMidX(), circle.getMidY(), x, y, 180);
////                ys[i] = xy[1] - halfY;
////                if (j == 0) {
////                    System.out.println("(" + xy[0] + ", -" + xy[1] + ")");
////                }
////
////                canvas.getGraphicsContext2D().strokeOval(xs[i] - (w / 2), ys[i] - (h / 2), w, h);
////                canvas.getGraphicsContext2D().strokeLine(cObject.getMidX() + (w / 2), cObject.getMidY() + (h / 2), xs[i], ys[i]);
////            }
//        }
//        canvas.getGraphicsContext2D().strokePolyline(xs, ys, nPoints);

        root = vBox;
        primaryStage.setTitle("Hello World");
        primaryStage.setScene(new Scene(root, 300, 275));
        primaryStage.show();
        vBox.resize(WIDTH, HEIGHT);
//        vBox.setPrefWidth(300);
//        vBox.setPrefHeight(275);
        BallSimulation ballSimulation = new BallSimulation(x1, y1, x2, y2, segments, duration, Brachistochrone.class, Parabolic.class, Cycloid.class, Linear.class);
//        BallSimulation ballSimulation = new BallSimulation(x1, y1, x2, y2, segments, duration, Brachistochrone.class);
        ballSimulation.draw(canvas);
    }

    public static double linear(double x, double x1, double y1, double x2, double y2) {
        double m = (y2 - y1) / (x2 - x1);
        double b = y1 - (m * x1);
        return (m * x) + b;
//        return 0;
    }

    public static void changeCanvasColour(Canvas c, Color paint) {
        c.getGraphicsContext2D().setStroke(paint);
        c.getGraphicsContext2D().setFill(paint);
    }

    public static void changeCanvasColour(Canvas c, Paint paint) {
        c.getGraphicsContext2D().setStroke(paint);
        c.getGraphicsContext2D().setFill(paint);
    }


    public static void main(String[] args) {
        launch(args);
    }
}

package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Point2D;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.scene.shape.Line;
import sample.Version_3.Triangle_v3;

import java.util.ArrayList;
import java.util.Arrays;

public class Main_v3 extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception{

        sample.Model_v3 model = new sample.Model_v3();

        Parent root;
//        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        primaryStage.setTitle("Hello World");

        root = FXMLLoader.load(getClass().getResource("whiteBoard.fxml"));
        sample.WhiteBoard_v3 whiteBoard = new sample.WhiteBoard_v3();
        whiteBoard.initFields(root);
        primaryStage.setScene(new Scene(root, 900, 575));
        primaryStage.show();
        whiteBoard.setDims(0, 0, primaryStage.getWidth(), primaryStage.getHeight());
        primaryStage.show();


        try {

            sample.Side_v3 side1 = new sample.Side_v3("a", 48);
            sample.Side_v3 side2 = new sample.Side_v3("b", 36);
            sample.Side_v3 side3 = new sample.Side_v3("c", 60);

            sample.Angle_v3 angle1 = new sample.Angle_v3("A", side1, side2, 36);
            sample.Angle_v3 angle2 = new sample.Angle_v3("B", side2, side3, 34);
            sample.Angle_v3 angle3 = new sample.Angle_v3("C", side1, side3, 110);

            Triangle_v3 t1 = new Triangle_v3("t1", side1, side2, side3, null, null, null);
            Triangle_v3 t2 = new Triangle_v3("t2", side1, side2, null, angle1, null, null);
            Triangle_v3 t3 = new Triangle_v3("t3", null, side2, side3, null, angle2, null);
            Triangle_v3 t4 = new Triangle_v3("t4", side1, null, side3, null, null, angle3);
            Triangle_v3 t5 = new Triangle_v3("t5", side1, side2, null, null, null, angle3);

            System.out.println("\nt1: " + t1);
            System.out.println("\nt2: " + t2);
            System.out.println("\nt3: " + t3);
            System.out.println("\nt4: " + t4);
            System.out.println("\nt5: " + t5);

            ArrayList<Triangle_v3> triangles = new ArrayList<>(Arrays.asList(
                    t1, t2, t3, t4, t5
            ));
            System.out.println("Finding sides and angles:");
            for (int i = 0; i < triangles.size(); i++) {
                Triangle_v3 t = triangles.get(i);
                System.out.println("\n" + t);
                t.solveRemainingTriangle();
                System.out.println("\n" + t);
                // System.out.println("a: " + lawOfCosines(t, SIDE_A));
                // System.out.println("b: " + lawOfCosines(t, SIDE_B));
                // System.out.println("c: " + lawOfCosines(t, SIDE_C));
                // System.out.println("A: " + lawOfCosines(t, ANGLE_A));
                // System.out.println("B: " + lawOfCosines(t, ANGLE_B));
                // System.out.println("C: " + lawOfCosines(t, ANGLE_C));
            }
            System.out.println();
            System.out.println();
            Point2D p1a = new Point2D(-1, -1);
            Point2D p1b = new Point2D(4, 14);
            Point2D p2a = new Point2D(-2, -9);
            Point2D p2b = new Point2D(6, 23);
            Line a = new Line(p1a.getX(), p1a.getY(), p1b.getX(), p1b.getY());
            Line b = new Line(p2a.getX(), p2a.getY(), p2b.getX(), p2b.getY());
            Point2D i = sample.Model_v3.intersectionPoint(a, b);
            System.out.println("p1a: " + p1a);
            System.out.println("p1b: " + p1b);
            System.out.println("p2a: " + p2a);
            System.out.println("p2b: " + p2b);
            System.out.println("line a: " + a);
            System.out.println("line b: " + b);
            System.out.println("i: " + i);
            System.out.println("check x:\n" + (i.getX() == 3) + "\ny:" + (i.getY() == 11));
            System.out.println();
            throw new sample.InvalidTriangleCreation_v3(1, "THIS IS JUST A TEST\n\"a\".equals(\"a\"): " + ("a".equals("a")) + "\n\"a\".equals(\"A\"): " + ("a".equals("A")) + "\n\"A\".equals(\"A\"): " + ("A".equals("A")) + "\n\"A\".equals(\"a\"): " + ("A".equals("a")));
        }
        catch(sample.InvalidTriangleCreation_v3 e) {
            System.out.println("CAUGHT");
        }
    }


    public static void main(String[] args) {
        launch(args);
    }
}

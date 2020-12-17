package sample.Version_4;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Polygon;
import javafx.stage.Stage;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception{
//
//        Polygon p1 = new Polygon();
//        p1.getPoints().addAll(10d, 20d, 30d, 10d, 20d, 30d);
//        Polygon p2 = new Polygon();
//        p2.getPoints().addAll(30d, 20d, 10d, 30d, 20d, 10d);
//        System.out.println("match: " + WhiteBoardModel.matchingPolygons(p1, p2));

        WhiteBoardModel whiteBoardModel = new WhiteBoardModel();

        Parent root;
//        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        primaryStage.setTitle("Hello World");

        root = FXMLLoader.load(getClass().getResource("whiteBoard.fxml"));
        WhiteBoard whiteBoard = new WhiteBoard();
        whiteBoard.initFields(root);
        primaryStage.setScene(new Scene(root, 900, 575));
        primaryStage.show();
        whiteBoard.setDims(30, 30, 600, 300);
        primaryStage.show();

        /////////////////////////////////////////////////////////

//        try {
//
//            // set title for the stage
//            primaryStage.setTitle("creating Background");
//
//            // create a label
//            Label label = new Label("Name : ");
//
//            // create a text field
//            TextField textfield = new TextField();
//
//            // set preferred column count
//            textfield.setPrefColumnCount(10);
//
//            // create a button
//            Button button = new Button("OK");
//
//            // add the label, text field and button
//            HBox hbox = new HBox(label, textfield, button);
//
//            // set spacing
//            hbox.setSpacing(10);
//
//            // set alignment for the HBox
//            hbox.setAlignment(Pos.CENTER);
//
//            VBox vBox = new VBox();
//            Label a = new Label("LABEL A");
//            vBox.getChildren().addAll(a, hbox);
//            // create a scene
//            Scene scene = new Scene(vBox, 280, 280);
//
//            // create a background fill
//            BackgroundFill background_fill = new BackgroundFill(Color.PINK,
//                    new CornerRadii(180), Insets.EMPTY);
//
//            // create Background
//            Background background = new Background(background_fill);
//
//            // set background
//            hbox.setBackground(background);
//
//            // set the scene
//            primaryStage.setScene(scene);
//
//            primaryStage.show();
//        }
//
//        catch (Exception e) {
//
//            System.out.println(e.getMessage());
//        }
////    }

    /////////////////////////////////////////////////////////

//        try {
//
//            Side side1 = new Side("a", 48);
//            Side side2 = new Side("b", 36);
//            Side side3 = new Side("c", 60);
//
//            Angle angle1 = new Angle("A", side1, side2, 36);
//            Angle angle2 = new Angle("B", side2, side3, 34);
//            Angle angle3 = new Angle("C", side1, side3, 110);
//
//            Triangle t1 = new Triangle("t1", side1, side2, side3, null, null, null);
//            Triangle t2 = new Triangle("t2", side1, side2, null, angle1, null, null);
//            Triangle t3 = new Triangle("t3", null, side2, side3, null, angle2, null);
//            Triangle t4 = new Triangle("t4", side1, null, side3, null, null, angle3);
//            Triangle t5 = new Triangle("t5", side1, side2, null, null, null, angle3);
//
//            System.out.println("\nt1: " + t1);
//            System.out.println("\nt2: " + t2);
//            System.out.println("\nt3: " + t3);
//            System.out.println("\nt4: " + t4);
//            System.out.println("\nt5: " + t5);
//
//            ArrayList<Triangle> triangles = new ArrayList<>(Arrays.asList(
//                    t1, t2, t3, t4, t5
//            ));
//            System.out.println("Finding sides and angles:");
//            for (int i = 0; i < triangles.size(); i++) {
//                Triangle t = triangles.get(i);
//                System.out.println("\n" + t);
//                t.solveRemainingTriangle();
//                System.out.println("\n" + t);
//                // System.out.println("a: " + lawOfCosines(t, SIDE_A));
//                // System.out.println("b: " + lawOfCosines(t, SIDE_B));
//                // System.out.println("c: " + lawOfCosines(t, SIDE_C));
//                // System.out.println("A: " + lawOfCosines(t, ANGLE_A));
//                // System.out.println("B: " + lawOfCosines(t, ANGLE_B));
//                // System.out.println("C: " + lawOfCosines(t, ANGLE_C));
//            }
//            System.out.println();
//            System.out.println();
//            Point2D p1a = new Point2D(-1, -1);
//            Point2D p1b = new Point2D(4, 14);
//            Point2D p2a = new Point2D(-2, -9);
//            Point2D p2b = new Point2D(6, 23);
//            Line a = new Line(p1a.getX(), p1a.getY(), p1b.getX(), p1b.getY());
//            Line b = new Line(p2a.getX(), p2a.getY(), p2b.getX(), p2b.getY());
//            Point2D i = WhiteBoardModel.intersectionPoint(a, b);
//            System.out.println("p1a: " + p1a);
//            System.out.println("p1b: " + p1b);
//            System.out.println("p2a: " + p2a);
//            System.out.println("p2b: " + p2b);
//            System.out.println("line a: " + a);
//            System.out.println("line b: " + b);
//            System.out.println("i: " + i);
//            System.out.println("check x:\n" + (i.getX() == 3) + "\ny:" + (i.getY() == 11));
//            System.out.println();
//            throw new InvalidTriangleCreation(1, "THIS IS JUST A TEST\n\"a\".equals(\"a\"): " + ("a".equals("a")) + "\n\"a\".equals(\"A\"): " + ("a".equals("A")) + "\n\"A\".equals(\"A\"): " + ("A".equals("A")) + "\n\"A\".equals(\"a\"): " + ("A".equals("a")));
//        }
//        catch(InvalidTriangleCreation e) {
//            System.out.println("CAUGHT");
//        }
    }


    public static void main(String[] args) {
        launch(args);
    }
}

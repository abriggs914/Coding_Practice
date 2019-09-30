package sample;
import javafx.application.Application;
import javafx.geometry.*;
import javafx.scene.Scene;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

// Java 8 code
public class Main extends Application {

    @Override
    public void start(final Stage stage) {
        Axes axes = new Axes(
                400, 300,
                -8, 8, 1,
                -6, 6, 1
        );

        Plot plot = new Plot(
                x -> x * (x + 2),
                -10,10,0.1,
                axes

                // original
                // x -> .25 * (x + 4) * (x + 1) * (x - 2),
                //-8, 8, 0.1,
                //axes
        );

        StackPane layout = new StackPane(
                plot
        );
        layout.setPadding(new Insets(20));
        layout.setStyle("-fx-background-color: rgb(35, 39, 50);");

        stage.setTitle("y = \u00BC(x+4)(x+1)(x-2)");
        stage.setScene(new Scene(layout, Color.rgb(35, 39, 50)));
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
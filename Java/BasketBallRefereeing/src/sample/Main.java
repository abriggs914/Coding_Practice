package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.util.Date;

import static sample.Gym.*;
import static sample.Referee.*;
import static sample.Team.*;

public class Main extends Application {

    public static GameManager gameManager = new GameManager();

    @Override
    public void start(Stage primaryStage) throws Exception{
        SampleGames sg = new SampleGames();
        sg.load_Fall_2019();
        gameManager.addGameObjectsArrayList(sg.getGames());

        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        primaryStage.setTitle("Basketball game entry form.");
        primaryStage.setScene(new Scene(root, 800, 800));
        primaryStage.setMaximized(true);
        primaryStage.show();

//        root.lookup("");

        Controller controller = new Controller();
        controller.init(root);
        System.out.println("gameManager: " + gameManager);
    }


    public static void main(String[] args) {
        launch(args);
    }
}

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
        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        primaryStage.setTitle("Basketball game entry form.");
        primaryStage.setScene(new Scene(root, 600, 600));
        primaryStage.show();

//        root.lookup("");

        Controller controller = new Controller();
        controller.init(root);

        Team homeTeam = FREDERICTON_HIGH_SCHOOL_SR_AAA_BOYS;
        Team awayTeam = LEO_HAYES_HIGH_SCHOOL_SR_AAA_BOYS;
        Referee refA = AVERY_BRIGGS;
        Referee refB = TERRY_DOLAN;
        Gym gym = FREDERICTON_HIGH_SCHOOL_MAIN_GYM;
        Date day = new Date();
        gameManager.createNewGame(day, gym, refA, refB, homeTeam, awayTeam);
        System.out.println("gameManager: " + gameManager);
    }


    public static void main(String[] args) {
        launch(args);
    }
}

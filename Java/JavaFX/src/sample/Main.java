package sample;

import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Group;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseEvent;
import javafx.scene.text.Text;
import javafx.scene.text.TextFlow;
import javafx.stage.Stage;

public class Main extends Application {

//    @FXML private TextField tf = fx:id="id";

    public static String pResultCurrText;
    public static String qResultCurrText;
    public static String cResultCurrText;
    public static String m2ResultCurrText;
    public static String m1ResultCurrText;
    public static String dResultCurrText;
    public static String nResultCurrText;
    public static String eResultCurrText;

    @Override
    public void start(Stage primaryStage) throws Exception{
        primaryStage.setTitle("RSA Encryption/Decryption");

        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        Scene scene = new Scene(root, 500, 375);

        // Buttons initialization
        Button genPrimesButton = (Button) scene.lookup("#generatePrimesButton");
        Button computeNButton = (Button) scene.lookup("#computeNButton");
        Button calculateDButton = (Button) scene.lookup("#calculateDButton");
        Button encryptButton = (Button) scene.lookup("#encryptButton");
        Button decryptButton = (Button) scene.lookup("#decryptButton");

        // TextFields initialization
        TextField pEqualsResultTextField = (TextField) scene.lookup("#pEqualsResultTextField");
        pResultCurrText = "";
        TextField qEqualsResultTextField = (TextField) scene.lookup("#qEqualsResultTextField");
        qResultCurrText = "";
        TextField cEqualsResultTextField = (TextField) scene.lookup("#cEqualsResultTextField");
        cResultCurrText = "";
        TextField mEqualsResultTextField1 = (TextField) scene.lookup("#mEqualsResultTextField1");
        m1ResultCurrText = "";
        TextField mEqualsResultTextField2 = (TextField) scene.lookup("#mEqualsResultTextField2");
        m2ResultCurrText = "";
        TextField dEqualsResultTextField = (TextField) scene.lookup("#dEqualsResultTextField");
        dResultCurrText = "";
        TextField nEqualsResultTextField = (TextField) scene.lookup("#nEqualsResultTextField");
        nResultCurrText = "";
        TextField eEqualsResultTextField = (TextField) scene.lookup("#eEqualsResultTextField");
        eResultCurrText = "";

        RSAEncryption rsa = new RSAEncryption();

        genPrimesButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                System.out.println("gen primes clicked");
                Main.pResultCurrText = Integer.toString(rsa.generatePrimeNumber());
                Main.qResultCurrText = Integer.toString(rsa.generatePrimeNumber());
                pEqualsResultTextField.setText(pResultCurrText);
                qEqualsResultTextField.setText(qResultCurrText);
            }
        });

        computeNButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                System.out.println("compute n button clicked");
                Main.nResultCurrText = "n";
                nEqualsResultTextField.setText(nResultCurrText);
            }
        });

        calculateDButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                System.out.println("calculate d button clicked");
                Main.dResultCurrText = "d";
                dEqualsResultTextField.setText(dResultCurrText);
            }
        });

        encryptButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                System.out.println("encrypt message button clicked");
                Main.m2ResultCurrText = "encrypted";
                mEqualsResultTextField2.setText(m2ResultCurrText);
            }
        });

        decryptButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                System.out.println("decrypt message button clicked");
                Main.m1ResultCurrText = "decrypted";
                mEqualsResultTextField1.setText(m1ResultCurrText);
            }
        });

        primaryStage.setScene(scene); // background
        primaryStage.show();
    }



    public static void main(String[] args) {
        launch(args);
    }
}

/*
*
* package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Group;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.text.Text;
import javafx.scene.text.TextFlow;
import javafx.stage.Stage;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception{
        //Creating a Text object
        Text text = new Text();

        //Setting the text to be added.
        text.setText("Hello how are you");

        //setting the position of the text
        text.setX(50);
        text.setY(50);

        //Creating a Group object
        Group grp = new Group(text);

        //Creating a scene object
//        Scene scene = new Scene(root, 600, 300);

        //Setting title to the Stage
        primaryStage.setTitle("RSA Encryption/Decryption");

        //Adding scene to the stage
//        primaryStage.setScene(root);

        //Displaying the contents of the stage
//        primaryStage.show();


        TextFlow tf = new TextFlow();


        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        primaryStage.setScene(new Scene(root, 500, 375)); // backgground
//        primaryStage.setScene(new Scene(grp, 150, 150)); // text and buttons
//        primaryStage.setTitle("Hello World");
        primaryStage.show();
    }



    public static void main(String[] args) {
        launch(args);
    }
}
*
* */

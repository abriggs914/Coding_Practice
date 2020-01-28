package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.Arrays;

public class Main extends Application {

    public static String dollarify(int transactionAmount) {
        double m = transactionAmount / 100.0;
        return "$ " + String.format("% .2f", m);
    }

    public void createCSV(ArrayList<Transaction> transactions) {
        CSVWriter writer = new CSVWriter();
        ArrayList<String> header = new ArrayList<>(Arrays.asList("Date", "Sender", "Receiver", "Amount"));
        writer.writeFile(header, transactions);
    }

    @Override
    public void start(Stage primaryStage) throws Exception{
        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        primaryStage.setTitle("Hello World");
        primaryStage.setScene(new Scene(root, 300, 275));
        primaryStage.show();

        Entity me = new Entity("avery");
        Entity power = new Entity("Power");
        Entity rent = new Entity("rent");
        Entity gst = new Entity("GST");
        me.sendMoney(power, 10005, true, "");
        me.sendMoney(rent, 37550, true, "");
        me.sendMoney(power, 10005, true, "");
        me.sendMoney(rent, 37550, true, "");
        me.receiveMoney(gst, 14700, true, "");

//        System.out.println("Transactions: \n" + t1 + "\n" + t2 + "\n" + t3 + "\n" + t4);
        System.out.println(me.getTransactions());
        System.out.println(me.getCustomerStats());
        createCSV(me.getTransactions());
    }


    public static void main(String[] args) {
        launch(args);
    }
}

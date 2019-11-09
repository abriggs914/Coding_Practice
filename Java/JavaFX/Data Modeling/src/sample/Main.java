package sample;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.concurrent.Service;
import javafx.concurrent.Task;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.MenuBar;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Main extends Application {

    public static final int SCALAR = 200;

    private static Scene scene;
    private static MenuBar menu;
    private static BorderPane borderPane;

    static DataModeler dataModeler;
    static DataViewer dataViewer;

    private static int maxSataSetsPerScreen = 7;

    @Override
    public void start(Stage primaryStage) {

//        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));

        try {
//            synchronized (this) {
                borderPane = new BorderPane();
                scene = new Scene(borderPane, 800, 550);
                menu = new GenMenuBar(getMenuContents()).getMenuBar();
                dataModeler = new DataModeler(getDataToModel());
                dataViewer = new DataViewer();
//            }

            borderPane.setTop(menu);
//            HBox hbox = new HBox();
//
//            hbox.getChildren().addAll(dateLabel, dataViewer);
//            borderPane.setCenter(hbox);
            borderPane.setCenter(dataViewer);

            primaryStage.setTitle("Data Modeling");
            primaryStage.setScene(scene);
            primaryStage.setResizable(false);
            primaryStage.show();

            ArrayList<String> days = Main.dataModeler.getDataSets().get(0).getSortedDates();

            Service<Void> service = new Service<Void>() {
                @Override
                protected Task<Void> createTask() {
                    return new Task<Void>() {
                        @Override
                        protected Void call() throws Exception {
                            //Background work
                            final CountDownLatch latch = new CountDownLatch(1);
                            Platform.runLater(new Runnable() {
                                @Override
                                public void run() {
                                    try{
                                        //FX Stuff done here
                                        dataViewer.dateLabel.setText("I HAVE BEEN CHANGED");
                                    }finally{
                                        latch.countDown();
                                    }
                                }
                            });
                            latch.await();
                            //Keep with the background work
                            return null;
                        }
                    };
                }
            };
            service.start();



//            final ScheduledExecutorService executorService = Executors.newSingleThreadScheduledExecutor();
//            executorService.scheduleAtFixedRate(new Runnable() {
//                public int i = 0;
//                @Override
//                public void run() {
//                    if (i < days.size()){
//                        System.out.print("i: " +  i + "\t");
//                        myTask(i);
////                        executorService.wait();
//                        synchronized (this) {
//                            dataViewer.layoutChildren();
//                        }
//                        i++;
//                    }
//                }
//                }, 0, 1, TimeUnit.SECONDS);
//                String day = days.get(0);
//                dataModeler.setCurrDate(day);
//                dataViewer.layoutChildren();
//                TimeUnit.SECONDS.sleep(1);
//                day = days.get(1);
//                dataModeler.setCurrDate(day);
//                dataViewer.layoutChildren();
//                TimeUnit.SECONDS.sleep(1);
//                day = days.get(2);
//                dataModeler.setCurrDate(day);
//                dataViewer.layoutChildren();
//            int i = 0;
//            while (i < days.size()) {
//                String day = days.get(i);
//                System.out.println("CURRDATE:\t" + day);
//                dataModeler.setCurrDate(day);
//                dataViewer.layoutChildren();
//                i++;
//                System.out.println("FINISHED UPDATING!");
//                TimeUnit.SECONDS.sleep(1);
//            }

//            Driver d = new Driver();
//            Thread t = new Thread(new Cddd());
//            t.run();
//            ArrayList<String> days = Main.dataModeler.getDataSets().get(0).getSortedDates();
//            final ScheduledExecutorService executorService = Executors.newSingleThreadScheduledExecutor();
//            executorService.scheduleAtFixedRate(new Runnable() {
//                public int i = 0;
//                @Override
//                public void run() {
//                    if (i < days.size()){
//                        System.out.print("i: " +  i + "\t");
//                        myTask(i);
////                        executorService.wait();
//                        dataViewer.layoutChildren();
//                        i++;
//                    }
//                }
//            }, 0, 1, TimeUnit.SECONDS);
        }
        catch (Exception e) {
            System.out.println("MAIN EXCEPTION");
            e.printStackTrace();
        }
    }

    public static void myTask(int i) {
        ArrayList<String> days = Main.dataModeler.getDataSets().get(0).getSortedDates();
//        for (int i = 0; i < days.size(); i++) {
            String day = days.get(i);
            System.out.println("CURRDATE:\t" + day);
//            try {
//                TimeUnit.SECONDS.sleep(2);
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            }
            dataModeler.setCurrDate(day);
//        dataViewer.draw();
            System.out.println("FINISHED UPDATING!");
//        }
    }

    public class Cddd implements Runnable{

        @Override
        public void run() {
            ArrayList<String> days = Main.dataModeler.getDataSets().get(0).getSortedDates();
            for (int i = 0; i < days.size(); i++) {
                String day = days.get(i);
                System.out.println("CURRDATE:\t" + day);
                try {
                    TimeUnit.SECONDS.sleep(2);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                Main.dataModeler.setCurrDate(day);
//                Main.dataViewer.layoutChildren();
            }
        }
    }

    private ArrayList<DataSet> getDataToModel() {
        ArrayList<DataSet> dataToModel = new ArrayList<>();
        DataSet carbonLevelData = new CarbonLevelData();
        dataToModel.add(carbonLevelData);
        dataToModel.add(carbonLevelData);
        dataToModel.add(carbonLevelData);
        dataToModel.add(carbonLevelData);
        dataToModel.add(carbonLevelData);
        dataToModel.add(carbonLevelData);
        dataToModel.add(carbonLevelData);
        return dataToModel;
    }

    private HashMap<String, ArrayList<String>> getMenuContents() {
        HashMap<String, ArrayList<String>> menu = new HashMap<>();
        String[] fileItemNames = {"new", "open", "save", "close"};
        ArrayList<String> fileItems = new ArrayList<>(Arrays.asList(fileItemNames));
        menu.put("File", fileItems);
        return menu;
    }

    public static Scene getScene() {
        return scene;
    }

    public static MenuBar getMenu() {
        return menu;
    }

    public static double getMaxSataSetsPerScreen() {
        return maxSataSetsPerScreen;
    }


    public static void main(String[] args) {
        launch(args);
    }
}

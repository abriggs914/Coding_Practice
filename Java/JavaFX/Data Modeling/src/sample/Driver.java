package sample;

import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import javafx.application.Platform;
import javafx.concurrent.*;

public class Driver {
    Driver() {
        ArrayList<String> days = Main.dataModeler.getDataSets().get(0).getSortedDates();
//        Runnable r = () -> {
//            for (int i = 0; i < days.size(); i++) {
//                String day = days.get(i);
//                System.out.println("CURRDATE:\t" + day);
//                try {
//                    TimeUnit.SECONDS.sleep(2);
//                } catch (InterruptedException e) {
//                    e.printStackTrace();
//                }
//                Main.dataModeler.setCurrDate(day);
//                Main.dataViewer.layoutChildren();
//            }
//        };

//        Thread t = new Thread(r);
//        t.run();

        Platform.runLater(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < days.size(); i++) {
                    String day = days.get(i);
                    System.out.println("CURRDATE:\t" + day);
                    try {
                        TimeUnit.SECONDS.sleep(2);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    Main.dataModeler.setCurrDate(day);
                    Main.dataViewer.layoutChildren();
                }
            }
        });
    }
}

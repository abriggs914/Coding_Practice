package com.company;
import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {
        ArrayList<WPWEntity> entities = new ArrayList<>();
        entities.add(new WPWEntity("Avery"));

        entities.get(0).balance = 14.5;
        System.out.println("Balance: " + entities.get(0).balance);
        System.out.println("entities: " + entities);
    }
}

package sample;

import javafx.scene.paint.Color;

import java.util.HashMap;
import java.util.Set;

public enum Disease {
    CORONAVIRUS(
            "Coronavirus",
            "COVID-19",
            new HashMap<Integer, Double>() {{
                put(0, 8.1);
                put(10, 11.5);
                put(20, 22.1);
                put(30, 28.5);
                put(40, 29.6);
                put(50, 31.0);
                put(60, 35.6);
                put(70, 32.2);
                put(80, 26.6);
                put(90, 25.7);
                put(100, 19.9);
                put(110, 10.0);
                put(120, 7.4);
            }},
            new HashMap<Integer, Double>() {{
                put(0, 0.0);
                put(10, 0.0);
                put(20, 0.15);
                put(30, 0.18);
                put(40, 0.2);
                put(50, 0.3);
                put(60, 1.3);
                put(70, 3.6);
                put(80, 8.0);
                put(90, 14.8);
                put(100, 25.0);
                put(110, 55.0);
                put(120, 79.8);
            }},
            18,
            false,
            Color.RED);

    private String name;
    private String idString;
    private HashMap<Integer, Double> infectionRate;
    private HashMap<Integer, Double> mortalityRate;
    private double infectiousPeriod;
    private boolean transmittableAfterDeath;
    private Color color;

    Disease(String name, String idString, HashMap<Integer, Double> infectionRate, HashMap<Integer, Double> mortalityRate, double infectiousPeriod, boolean transmittableAfterDeath, Color color) {
        this.name = name;
        this.idString = idString;
        this.infectionRate = infectionRate;
        this.mortalityRate = mortalityRate;
        this.infectiousPeriod = infectiousPeriod;
        this.transmittableAfterDeath = transmittableAfterDeath;
        this.color = color;
    }

    public String getName() {
        return name;
    }

    public String getIdString() {
        return idString;
    }

    public double getInfectionRate(int age) {
        for (int i = 0; i < 130; i += 10) {
            if (i > age) {
//                System.out.println("\t\tInfection Returning (" + i + "): " + mortalityRate.get(i));
                return infectionRate.get(i);
            }
        }
//        System.out.println("\t\tInfection Returning (" + 0 + ")");
        return 0.0;
    }

    public HashMap<Integer, Double> getInfectionRateMap() {
        return infectionRate;
    }

    public double getMortalityRate(int age) {
        for (int i = 0; i < 130; i += 10) {
            if (i > age) {
//                System.out.println("\t\tMortality Returning (" + i + "): " + mortalityRate.get(i));
                return mortalityRate.get(i);
            }
        }
//        System.out.println("\t\tMortality Returning (" + 0 + ")");
        return 0.0;
    }

    public HashMap<Integer, Double> getMortalityRateMap() { return mortalityRate; }

    public boolean isTransmittableAfterDeath() {
        return transmittableAfterDeath;
    }

    public double getInfectiousPeriod() {
        return infectiousPeriod;
    }

    public Color getColor() {
        return color;
    }
}

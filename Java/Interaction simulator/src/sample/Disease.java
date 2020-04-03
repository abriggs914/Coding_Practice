package sample;

import javafx.scene.paint.Color;

public enum Disease {
    CORONAVIRUS("Coronavirus", "COVID-19",35.6, 7.8, 18, false, Color.RED);

    private String name;
    private String idString;
    private double infectionRate;
    private double mortalityRate;
    private double infectiousPeriod;
    private boolean transmittableAfterDeath;
    private Color color;

    Disease(String name, String idString, double infectionRate, double mortalityRate, double infectiousPeriod, boolean transmittableAfterDeath, Color color) {
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

    public double getInfectionRate() {
        return infectionRate;
    }

    public double getMortalityRate() { return mortalityRate; }

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

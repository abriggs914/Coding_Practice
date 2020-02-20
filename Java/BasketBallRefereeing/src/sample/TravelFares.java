package sample;

import java.util.Comparator;

public enum TravelFares {
    OUT_OF_ZONE("Out of zone", 0,0),
    FREDERICTON("Fredericton",0, 0),
    STANLEY("Stanley",38,42.6),
    CAMBRIDGE_NARROWS("Cambridge Narrows",53,68.8),
    BOIESTOWN("Boiestown",60,76.9),
    HARVEY("Harvey",35,49.2),
    OROMOCTO("Oromocto",15,21.5),
    BASE_GAGETOWN("Base Gagetown", 15, 25.8),
    GAGETOWN("Gagetown",45,58.2),
    KESWICK_VALLEY("Keswick Valley",22,29.5),
    KESWICK_RIDGE("Keswick Ridge",19,23.2),
    CHIPMAN("Chipman",57,91.7),
    MINTO("Minto",38,65.3),
    MCADAM("McAdam",60,80.7),
    NACKAWICK("Nackawick",48,63.9),
    FREDERICTON_JUNCTION("Fredericton Junction",30,36.6);
    private String locationName;
    private double travelFare, distance;

    TravelFares(String locationName, double travelFare, double distance) {
        this.locationName = locationName;
        this.travelFare = travelFare;
        this.distance = distance;
    }

    public String getLocationName() {
        return this.locationName;
    }

    public double getDollarPerKM() {
        return this.travelFare / this.distance;
    }

    public static Comparator<TravelFares> compareTravelFareNames() {
        return Comparator.comparing(TravelFares::getLocationName);
    }

    public String toString() {
        return locationName + ", distance: " + distance + ", travel fare: $ " + travelFare + ".";
    }
}

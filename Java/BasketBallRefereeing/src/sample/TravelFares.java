package sample;

import java.util.Comparator;

public enum TravelFares {
    OUT_OF_ZONE("Out of zone", 0,0),
    FREDERICTON("Fredericton",0, 0),
    STANLEY("Stanley",0,0),
    CAMBRIDGE_NARROWS("Cambridge Narrows",0,0),
    BOIESTOWN("Boiestown",0,0),
    HARVEY("Harvey",0,0),
    OROMOCTO("Oromocto",0,0),
    GAGETOWN("Gagetown",0,0),
    KESWICK_VALLEY("Keswick Valley",0,0),
    KESWICK_RIDGE("Keswick Ridge",0,0),
    CHIPMAN("Chipman",0,0),
    MINTO("Minto",0,0),
    MCADAM("McAdam",0,0),
    NACKAWICK("Nackawick",0,0),
    FREDERICTON_JUNCTION("Fredericton Junction",0,0);

    private String locationName;
    private double travelFare, distance;

    TravelFares(String locationName, double travelFare, double distance) {
        this.locationName = locationName;
        this.travelFare = travelFare;
        this.distance = distance;
    }

    public String getLocationName() {
        return locationName;
    }

    public static Comparator<TravelFares> compareTravelFareNames() {
        return Comparator.comparing(TravelFares::getLocationName);
    }

    public String toString() {
        return locationName + ", distance: " + distance + ", travel fare: $ " + travelFare + ".";
    }
}

package sample;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

import static sample.TravelFares.*;

public enum Gym {
    CURRIE_CENTRE_PERFORMANCE("Currie centre performance gym", "RJC_PG", "Fredericton - south", true, FREDERICTON),
    CURRIE_CENTRE_REC_1("Currie centre rec gym 1", "RJC_RG1", "Fredericton - south", true, FREDERICTON),
    CURRIE_CENTRE_REC_2("Currie centre rec gym 2", "RJC_RG2", "Fredericton - south", true, FREDERICTON),
    BLISS_CARMEN_MIDDLE_SCHOOL("Bliss carmen middle school", "BCMS", "Fredericton - south", true, FREDERICTON),
    FREDERICTON_HIGH_SCHOOL_MAIN_GYM("Fredericton high school main gym", "FHS_MG", "Fredericton - south", true, FREDERICTON),
    FREDERICTON_HIGH_SCHOOL_SIDE_GYM_1("Fredericton high school side gym 1", "FHS_SG1", "Fredericton - south", true, FREDERICTON),
    FREDERICTON_HIGH_SCHOOL_SIDE_GYM_2("Fredericton high school side gym 2", "FHS_SG2", "Fredericton - south", true, FREDERICTON),
    LEO_HAYES_HIGH_SCHOOL("Leo hayes high school", "LHHS", "Fredericton - north", true, FREDERICTON),
    ECOLE_LES_ECLAIEURS_COURT_1("Ecole les eclaieurs court 1", "ELE_C1", "Fredericton - north", true, FREDERICTON),
    ECOLE_LES_ECLAIEURS_COURT_2("Ecole les eclaieurs court 2", "ELE_C2", "Fredericton - north", true, FREDERICTON),
    ECOLE_SAINTE_ANNE_MAIN_COURT("Ecole saint-anne main court", "ESA_MC", "Fredericton - south", true, FREDERICTON),
    ECOLE_SAINTE_ANNE_COURT_1("Ecole saint-anne court 1", "ESA_C1", "Fredericton - south", true, FREDERICTON),
    ECOLE_SAINTE_ANNE_COURT_2("Ecole saint-anne court 2", "ESA_C2", "Fredericton - south", true, FREDERICTON),
    GEORGE_STREET_MIDDLE_SCHOOL("George street middle school", "GSMS", "Fredericton - north", true, FREDERICTON),
    DEVON_MIDDLE_SCHOOL("Devon middle school", "DMS", "Fredericton - north", true, FREDERICTON),
    DEVON_PARK_MIDDLE_SCHOOL("Devon park christian school", "DPCS", "Fredericton - north", true, FREDERICTON),
    PARK_ST_ELEMENTARY("Park street elementary school", "PSES", "Fredericton - north", true, FREDERICTON),
    PRIESTMAN_STREET_SCHOOL("Priestman street school", "PSS", "Fredericton - south", true, FREDERICTON),
    NASHWAKSIS_MIDDLE_SCHOOL_MAIN_COURT("Nashwaksis middle school main court", "NMS_MC", "Fredericton - north", true, FREDERICTON),
    NASHWAKSIS_MIDDLE_SCHOOL_COURT_1("Nashwaksis middle school court 1", "NMS_C1", "Fredericton - north", true, FREDERICTON),
    NASHWAKSIS_MIDDLE_SCHOOL_COURT_2("Nashwaksis middle school court 2", "NMS_C2", "Fredericton - north", true, FREDERICTON),
    NASHWAKSIS_MIDDLE_SCHOOL_COURT_3("Nashwaksis middle school court 3", "NMS_C3", "Fredericton - north", true, FREDERICTON),
    BARKERS_POINT_ELEMENTARY_SCHOOL("Barkers point elementary school","BPES","Fredericton - north",true,FREDERICTON),
    GIBSON_NEIL_ELEMENTARY_SCHOOL("Gibson-neil elementary school", "GNES", "Fredericton - north", true, FREDERICTON),

    STANLEY_HIGH_SCHOOL("Stanley high school", "SHS", "Stanley", false, STANLEY),
    CAMBRIDGE_NARROWS_HIGH_SCHOOL("Cambridge narrows high school", "CNHS", "Cambridge-Narrows", false, CAMBRIDGE_NARROWS),
    CENTRAL_NEW_BRUNSWICK_ACADEMY("Central new brunswick academy", "CNBA", "Boiestown", false, BOIESTOWN),
    HARVEY_HIGH_SCHOOL("Harvey high school", "HHS", "Harvey", false, HARVEY),
    FREDERICTON_JUNCTION_SCHOOL("Fredericton junction school", "FJS", "Fredericton Junction", false, FREDERICTON_JUNCTION),
    OROMOCTO_HIGH_SCHOOL("Oromocto High School", "OHS", "Oromocto", false, OROMOCTO),
    HAROLD_PETERSON_MIDDLE_SCHOOL("Harold peterson middle school", "", "Oromocto", false, OROMOCTO),
    RIDGEVIEW_MIDDLE_SCHOOL("Ridgeview middle school", "", "Oromocto", false, OROMOCTO),
    GAGETOWN_SCHOOL("Gagetown school", "GES", "Gagetown", false, GAGETOWN),
    GAGETOWN_BASE("Base gagetown", "CBF", "Gagetown", false, BASE_GAGETOWN),
    BURTS_CORNER("Burt\'s corner school", "KVS", "Keswick valley", false, KESWICK_VALLEY),
    KESWICK_RIDGE_SCHOOL("Keswick ridge school", "KRS", "Keswick ridge", false, KESWICK_RIDGE),
    CHIPMAN_HIGH_SCHOOL("Chipman high school", "CHS", "Chipman", false, CHIPMAN),
    MINTO_HIGH_SCHOOL("Minto high school", "MHS", "Minto", false, MINTO),
    MINTO_MIDDLE_SCHOOL("Minto middle school", "MMS", "Minto", false, MINTO),
    MCADAM_HIGH_SCHOOL("McAdam high school", "MHS", "McAdam", false, MCADAM),
    NACKAWICK_MIDDLE_SCHOOL("Nackawick middle school", "NMS", "Nackawick", false, NACKAWICK),
    NACKAWICK_HIGH_SCHOOL("Nackawick high school", "NHS", "Nackawick", false, NACKAWICK);

    private String name, acronym, locationString;
    boolean inTown;
    TravelFares travelFare;

    Gym(String name, String acronym, String locationString, boolean inTown, TravelFares travelFare) {
        this.name = name;
        this.acronym = acronym;
        this.locationString = locationString;
        this.inTown = inTown;
        this.travelFare = travelFare;
    }

    public String getName() {
        return name;
    }

    public String getAcronym() {
        return acronym;
    }

    public String getLocationString() {
        return locationString;
    }

    public boolean isInTown() {
        return inTown;
    }

    public TravelFares getTravelFare() {
        return travelFare;
    }

    public static ArrayList<Gym> getValues() {
        return new ArrayList<>(Arrays.asList(Gym.values()));
    }

    public static Comparator<Gym> compareGymNames() {
        return Comparator.comparing(Gym::getName);
    }

    public String toString() {
        return Utilities.titlifyName(name);
    }
}

package sample;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;

import static sample.TravelFares.*;

public enum Gym {
    UNKNOWN_GYM("UNKNOWN", new ArrayList<>(Collections.emptyList()), "NA", "UNKNOWN", true, OUT_OF_ZONE),
    CURRIE_CENTRE_PERFORMANCE("Currie centre performance gym", new ArrayList<>(Collections.singletonList("Currie centre_perf")),"RJC_PG", "Fredericton - south", true, FREDERICTON),
    CURRIE_CENTRE_REC_1("Currie centre recreation gym 1", new ArrayList<>(Collections.singletonList("Currie centre_rec 1")), "RJC_RG1", "Fredericton - south", true, FREDERICTON),
    CURRIE_CENTRE_REC_2("Currie centre recreation gym 2", new ArrayList<>(Collections.singletonList("Currie centre_rec 2")), "RJC_RG2", "Fredericton - south", true, FREDERICTON),
    BLISS_CARMEN_MIDDLE_SCHOOL("Bliss carmen middle school", new ArrayList<>(Collections.emptyList()), "BCMS", "Fredericton - south", true, FREDERICTON),
    FREDERICTON_HIGH_SCHOOL_MAIN_GYM("Fredericton high school main gym", new ArrayList<>(Collections.emptyList()), "FHS_MG", "Fredericton - south", true, FREDERICTON),
    FREDERICTON_HIGH_SCHOOL_SIDE_GYM_1("Fredericton high school side gym 1", new ArrayList<>(Collections.singletonList("FHS-side")), "FHS_SG1", "Fredericton - south", true, FREDERICTON),
    FREDERICTON_HIGH_SCHOOL_SIDE_GYM_2("Fredericton high school side gym 2", new ArrayList<>(Collections.singletonList("FHS-side")), "FHS_SG2", "Fredericton - south", true, FREDERICTON),
    LEO_HAYES_HIGH_SCHOOL("Leo hayes high school", new ArrayList<>(Collections.emptyList()), "LHHS", "Fredericton - north", true, FREDERICTON),
    ECOLE_LES_ECLAIREURS_COURT_1("Ecole les eclaireurs court 1", new ArrayList<>(Collections.singletonList("Eclaireurs - Gym 1")), "ELE_C1", "Fredericton - north", true, FREDERICTON),
    ECOLE_LES_ECLAIREURS_COURT_2("Ecole les eclaireurs court 2", new ArrayList<>(Collections.singletonList("Eclaireurs - Gym 2")), "ELE_C2", "Fredericton - north", true, FREDERICTON),
    ECOLE_SAINTE_ANNE_MAIN_COURT("Ecole saint-anne main court", new ArrayList<>(Collections.emptyList()), "ESA_MC", "Fredericton - south", true, FREDERICTON),
    ECOLE_SAINTE_ANNE_COURT_1("Ecole saint-anne court 1", new ArrayList<>(Collections.singletonList("Esa - Ct1")), "ESA_C1", "Fredericton - south", true, FREDERICTON),
    ECOLE_SAINTE_ANNE_COURT_2("Ecole saint-anne court 2", new ArrayList<>(Collections.singletonList("Esa - Ct2")), "ESA_C2", "Fredericton - south", true, FREDERICTON),
    GEORGE_STREET_MIDDLE_SCHOOL("George street middle school", new ArrayList<>(Collections.emptyList()), "GSMS", "Fredericton - north", true, FREDERICTON),
    DEVON_MIDDLE_SCHOOL("Devon middle school", new ArrayList<>(Collections.emptyList()), "DMS", "Fredericton - north", true, FREDERICTON),
    DEVON_PARK_MIDDLE_SCHOOL("Devon park christian school", new ArrayList<>(Collections.emptyList()), "DPCS", "Fredericton - north", true, FREDERICTON),
    PARK_ST_ELEMENTARY("Park street elementary school", new ArrayList<>(Collections.singletonList("Park st.")), "PSES", "Fredericton - north", true, FREDERICTON),
    PRIESTMAN_STREET_SCHOOL("Priestman street school", new ArrayList<>(Collections.emptyList()), "PSS", "Fredericton - south", true, FREDERICTON),
    NASHWAKSIS_MIDDLE_SCHOOL_MAIN_COURT("Nashwaksis middle school main court", new ArrayList<>(Collections.singletonList("Naasis")), "NMS_MC", "Fredericton - north", true, FREDERICTON),
    NASHWAKSIS_MIDDLE_SCHOOL_COURT_1("Nashwaksis middle school court 1", new ArrayList<>(Collections.singletonList("Naasis - Ct1")), "NMS_C1", "Fredericton - north", true, FREDERICTON),
    NASHWAKSIS_MIDDLE_SCHOOL_COURT_2("Nashwaksis middle school court 2", new ArrayList<>(Collections.singletonList("Naasis - Ct2")), "NMS_C2", "Fredericton - north", true, FREDERICTON),
    NASHWAKSIS_MIDDLE_SCHOOL_COURT_3("Nashwaksis middle school court 3", new ArrayList<>(Collections.singletonList("Naasis - Ct3")), "NMS_C3", "Fredericton - north", true, FREDERICTON),
    BARKERS_POINT_ELEMENTARY_SCHOOL("Barkers point elementary school", new ArrayList<>(Collections.emptyList()),"BPES","Fredericton - north",true,FREDERICTON),
    GIBSON_NEILL_ELEMENTARY_SCHOOL("Gibson-neill elementary school", new ArrayList<>(Collections.emptyList()), "GNES", "Fredericton - north", true, FREDERICTON),
    GARDEN_CREEK_ELEMENTARY_SCHOOL("Garden creek elementary school", new ArrayList<>(Collections.emptyList()), "GCES", "Fredericton - south", true, FREDERICTON),

    STANLEY_HIGH_SCHOOL("Stanley high school", new ArrayList<>(Collections.emptyList()), "SHS", "Stanley", false, STANLEY),
    CAMBRIDGE_NARROWS_HIGH_SCHOOL("Cambridge-narrows high school", new ArrayList<>(Collections.emptyList()), "CNHS", "Cambridge-Narrows", false, CAMBRIDGE_NARROWS),
    CENTRAL_NEW_BRUNSWICK_ACADEMY("Central new brunswick academy", new ArrayList<>(Collections.singletonList("CNBA")), "CNBA", "Boiestown", false, BOIESTOWN),
    HARVEY_HIGH_SCHOOL("Harvey high school", new ArrayList<>(Collections.emptyList()), "HHS", "Harvey", false, HARVEY),
    FREDERICTON_JUNCTION_SCHOOL("Fredericton junction school", new ArrayList<>(Collections.singletonList("F\'ton Junction")), "FJS", "Fredericton Junction", false, FREDERICTON_JUNCTION),
    OROMOCTO_HIGH_SCHOOL("Oromocto High School", new ArrayList<>(Collections.emptyList()), "OHS", "Oromocto", false, OROMOCTO),
    HAROLD_PETERSON_MIDDLE_SCHOOL("Harold peterson middle school", new ArrayList<>(Collections.emptyList()), "HPMS", "Oromocto", false, OROMOCTO),
    RIDGEVIEW_MIDDLE_SCHOOL("Ridgeview middle school", new ArrayList<>(Collections.emptyList()), "RMS", "Oromocto", false, OROMOCTO),
    GAGETOWN_SCHOOL("Gagetown school", new ArrayList<>(Collections.emptyList()), "GES", "Gagetown", false, GAGETOWN),
    GAGETOWN_BASE("Base gagetown", new ArrayList<>(Collections.emptyList()), "CBF", "Gagetown", false, BASE_GAGETOWN),
    BURTS_CORNER("Burt\'s corner school", new ArrayList<>(Collections.singletonList("Keswick valley")), "KVS", "Keswick valley", false, KESWICK_VALLEY),
    KESWICK_RIDGE_SCHOOL("Keswick ridge school", new ArrayList<>(Collections.emptyList()), "KRS", "Keswick ridge", false, KESWICK_RIDGE),
    CHIPMAN_HIGH_SCHOOL("Chipman high school", new ArrayList<>(Collections.emptyList()), "CHS", "Chipman", false, CHIPMAN),
    MINTO_HIGH_SCHOOL("Minto high school", new ArrayList<>(Collections.emptyList()), "MHS", "Minto", false, MINTO),
    MINTO_MIDDLE_SCHOOL("Minto middle school", new ArrayList<>(Collections.emptyList()), "MMS", "Minto", false, MINTO),
    MCADAM_HIGH_SCHOOL("McAdam high school", new ArrayList<>(Collections.emptyList()), "MHS", "McAdam", false, MCADAM),
    NACKAWICK_MIDDLE_SCHOOL("Nackawick middle school", new ArrayList<>(Collections.emptyList()), "NMS", "Nackawick", false, NACKAWICK),
    NACKAWICK_HIGH_SCHOOL("Nackawick high school", new ArrayList<>(Collections.emptyList()), "NHS", "Nackawick", false, NACKAWICK);

    private String name, acronym, locationString;
    private ArrayList<String> nickNames;
    boolean inTown;
    TravelFares travelFare;

    Gym(String name, ArrayList<String> nickNames, String acronym, String locationString, boolean inTown, TravelFares travelFare) {
        this.name = name;
        this.nickNames = new ArrayList<>(nickNames);
        this.acronym = acronym;
        this.locationString = locationString;
        this.inTown = inTown;
        this.travelFare = travelFare;
    }

    public String getName() {
        return name;
    }

    public ArrayList<String> getNickNames() {
        return nickNames;
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

    public static ArrayList<String> getStringValues() {
        ArrayList<String> res = new ArrayList<>();
        getValues().forEach((g) -> res.add(g.getName()));
        return res;
    }

    public static Comparator<Gym> compareGymNames() {
        return Comparator.comparing(Gym::getName);
    }

//    public static Gym parseGym(String s) {
//        System.out.println("parsing gym: " + s);
//        Gym bestPick = null;
//        if (s.equals("") || s.equals(" ")) {
//            return null;
//        }
//        for (Gym g : getValues()) {
//            if (g.getName().toUpperCase().equals(s.toUpperCase())){
//                bestPick = g;
//                break;
//            }
//            else if (g.getName().toUpperCase().contains(s.toUpperCase())) {
//                bestPick = g;
//            }
//        }
//        return bestPick;
//    }


//    public static Gym parseGym(String s) {
//        System.out.println("parsing gym: " + s);
//        Gym bestPick = null;
//        int minimumEditDistance = Integer.MAX_VALUE;
//        if (s.equals("") || s.equals(" ")) {
//            return null;
//        }
//        for (Gym g : getValues()) {
//            String name = g.getName().toUpperCase();
//            String temp = s.toUpperCase();
//            if (name.equals(temp)){
//                bestPick = g;
//                break;
//            }
//            else if (name.contains(temp)) {
//                int distance = Utilities.minEditDistance(name, temp);
//                if (distance < minimumEditDistance) {
//                    minimumEditDistance = distance;
//                    bestPick = g;
//                }
//            }
//        }
//        return bestPick;
//    }

    public static Gym parseGym(String s) {
//        System.out.print(", gym: " + s);
        Gym bestPick = UNKNOWN_GYM;
        int minimumEditDistance = Integer.MAX_VALUE;
        if (s.equals("") || s.equals(" ")) {
            return bestPick;
        }
        for (Gym gym : getValues()) {
            String gymName = gym.getName().toUpperCase();
            String stringIn = s.toUpperCase();
            ArrayList<String> toCheck = new ArrayList<>(Arrays.asList(gymName, gym.getAcronym()));
            toCheck.addAll(gym.getNickNames());
//            System.out.println("name: " + gymName + ", temp: " + stringIn);
            if (toCheck.contains(stringIn)) {
                bestPick = gym;
//                System.out.println("FOUND EXACT " + bestPick + "\n\n\ttoCheck:\n" + toCheck);
                break;
            }
            else {
                for (String str : toCheck) {
//                    System.out.println("BEFORE\tstr: " + str + ", stringIn: " + stringIn);
                    if (str.contains(stringIn)) {
                        int u = str.indexOf(stringIn);
                        int v = stringIn.length();
                        str = str.substring(u, (u + v));
                    }
                    else if (stringIn.contains(str)) {
                        int u = stringIn.indexOf(str);
                        int v = str.length();
//                        System.out.println("\t\t\tstringIn: " + stringIn + ", str: " + str + ", u: " + u + ", v: " + v);
                        stringIn = stringIn.substring(u,(u + v));
                    }
                    int distance = Utilities.getMinEditDist(str, stringIn);
//                    System.out.println("AFTER\tstr: " + str + ", stringIn: " + stringIn + ", distance: " + distance);
                    if (distance < minimumEditDistance) {
                        minimumEditDistance = distance;
                        bestPick = gym;
                    }
                }
            }
        }
        return bestPick;
    }

    public String toString() {
        return Utilities.titlifyName(name);
    }
}

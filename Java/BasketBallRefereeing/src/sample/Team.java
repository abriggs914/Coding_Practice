package sample;

import javafx.scene.paint.Color;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;

import static sample.Gym.*;
import static sample.Level.*;

public enum Team {
    UNKNOWN_TEAM(
            "UNKNOWN",
            "UNKNOWN",
            true,
            "UNKNOWN",
            UNKNOWN_GYM,
            UNKNOWN_LEVEL,
            Color.BLACK,
            Color.WHITE
    ),
    FREDERICTON_HIGH_SCHOOL_SR_AAA_BOYS(
            "Fredericton high school senior boys",
            "Black Kats",
            true,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            AAA,
            Color.BLACK,
            Color.GOLD),

    LEO_HAYES_HIGH_SCHOOL_SR_AAA_BOYS(
            "Leo hayes high school senior boys",
            "Lions",
            true,
            "Fredericton - north",
            LEO_HAYES_HIGH_SCHOOL,
            AAA,
            Color.WHITE,
            Color.BLUE),

    FREDERICTON_HIGH_SCHOOL_SR_AAA_GIRLS(
            "Fredericton high school senior girls",
            "Black Kats",
            false,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            AAA,
            Color.BLACK,
            Color.GOLD),

    FREDERICTON_HIGH_SCHOOL_X_AAA_GIRLS(
            "Fredericton high school exhibition girls",
            "Black Kats",
            false,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            EXHIBITION,
            Color.BLACK,
            Color.GOLD),

    LEO_HAYES_HIGH_SCHOOL_SR_AAA_GIRLS(
            "Leo hayes high school senior girls",
            "Lions",
            false,
            "Fredericton - north",
            LEO_HAYES_HIGH_SCHOOL,
            AAA,
            Color.WHITE,
            Color.BLUE),

    KENTUCKY_SR_EDP_BOYS(
            "Kentucky Sr. EDP boys",
            "UNKNOWN",
            true,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            SR_EDP,
            Color.BLACK,
            Color.WHITE),

    MICHIGAN_SR_EDP_BOYS(
            "Michigan Sr. EDP boys",
            "UNKNOWN",
            true,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            SR_EDP,
            Color.BLACK,
            Color.WHITE),

    LOUSVILLE_SR_EDP_BOYS(
            "Lousville Sr. EDP boys",
            "UNKNOWN",
            true,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            SR_EDP,
            Color.BLACK,
            Color.WHITE),

    SYRACUSE_SR_EDP_BOYS(
            "Syracuse Sr. EDP boys",
            "UNKNOWN",
            true,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            SR_EDP,
            Color.BLACK,
            Color.WHITE),

    RIVERVIEW_A_U_14_GIRLS(
            "Riverview \'A\' u14 girls",
            "Royals",
            false,
            "Riverview",
            UNKNOWN_GYM,
            U_14,
            Color.WHITE,
            Color.RED),

    RIVERVIEW_A_U_14_BOYS(
            "Riverview \'A\' u14 boys",
            "Royals",
            true,
            "Riverview",
            UNKNOWN_GYM,
            U_14,
            Color.WHITE,
            Color.RED),

    RIVERVIEW_B_U_12_BOYS(
            "Riverview \'B\' u12 boys",
            "Royals",
            true,
            "Riverview",
            UNKNOWN_GYM,
            U_12,
            Color.WHITE,
            Color.RED),

    NMBA_TIER_1_U_14_GIRLS(
            "NMBA tier 1 u14 girls",
            "Lions",
            false,
            "Fredericton - north",
            LEO_HAYES_HIGH_SCHOOL,
            U_14,
            Color.WHITE,
            Color.BLUE),

    NMBA_TIER_2_U_14_BOYS(
            "NMBA tier 2 u14 boys",
            "Lions",
            false,
            "Fredericton - north",
            LEO_HAYES_HIGH_SCHOOL,
            U_14,
            Color.WHITE,
            Color.BLUE),

    KVBA_A_U_14_GIRLS(
            "KVBA \'A\' u14 girls",
            "Crusaders",
            false,
            "Kennebacasis Valley",
            UNKNOWN_GYM,
            U_14,
            Color.WHITE,
            Color.BLUE),

    KVBA_A_U_14_BOYS(
            "KVBA \'A\' u14 boys",
            "Crusaders",
            true,
            "Kennebacasis Valley",
            UNKNOWN_GYM,
            U_14,
            Color.WHITE,
            Color.BLUE),

    MONCTON_A_U_14_GIRLS(
            "Moncton \'A\' u14 girls",
            "Hawks",
            false,
            "Moncton",
            UNKNOWN_GYM,
            U_14,
            Color.BLACK,
            Color.GOLD),

    MONCTON_B_U_14_BOYS(
            "Moncton \'B\' u14 boys",
            "Hawks",
            true,
            "Moncton",
            UNKNOWN_GYM,
            U_14,
            Color.BLACK,
            Color.GOLD),

    GRAND_MANAN_HIGH_SCHOOL_SR_A_GIRLS(
            "Grand manan high school senior girls",
            "Breakers",
            false,
            "Grand manan",
            UNKNOWN_GYM,
            A,
            Color.BLUE,
            Color.GOLD),

    GRAND_MANAN_U_12_BOYS(
            "Grand manan u12 boys",
            "Breakers",
            true,
            "Grand manan",
            UNKNOWN_GYM,
            U_12,
            Color.BLUE,
            Color.GOLD),

    HARTLAND_HIGH_SCHOOL_SR_A_GIRLS(
            "Hartland high school senior girls",
            "Huskies",
            false,
            "Hartland",
            UNKNOWN_GYM,
            A,
            Color.DARKRED,
            Color.GOLD),

    HARVEY_HIGH_SCHOOL_SR_A_GIRLS(
            "Harvey high school senior girls",
            "Lakers",
            false,
            "Harvey",
            HARVEY_HIGH_SCHOOL,
            A,
            Color.GREEN,
            Color.GOLD),

    HARVEY_HIGH_SCHOOL_JR_A_GIRLS(
            "Harvey high school junior girls",
            "Lakers",
            false,
            "Harvey",
            HARVEY_HIGH_SCHOOL,
            JV_A,
            Color.GREEN,
            Color.GOLD),

    CALEDONIA_HIGH_SCHOOL_SR_A_GIRLS(
            "Caledonia high school senior girls",
            "Tigers",
            false,
            "Caledonia",
            UNKNOWN_GYM,
            A,
            Color.PURPLE,
            Color.GOLD),

    CALEDONIA_HIGH_SCHOOL_SR_A_BOYS(
            "Caledonia high school senior boys",
            "Tigers",
            true,
            "Caledonia",
            UNKNOWN_GYM,
            A,
            Color.PURPLE,
            Color.GOLD),

    YCBC_Tier_1_U_14_BOYS(
            "YCBC tier 1 u14 boys",
            "Caps",
            true,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            U_14,
            Color.RED,
            Color.BLACK),

    YCBC_Tier_2_U_14_BOYS(
            "YCBC tier 2 u14 boys",
            "Caps",
            true,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            U_14,
            Color.RED,
            Color.BLACK),

    YCBC_Tier_1_U_10_BOYS(
            "YCBC u10 tier 1 boys",
            "Caps",
            true,
            "Fredericton - south",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            U_12,
            Color.RED,
            Color.BLACK),

    CARLETON_NORTH_U_14_BOYS(
            "Carleton north u14 boys",
            "Start",
            true,
            "Bristol",
            UNKNOWN_GYM,
            U_14,
            Color.WHITE,
            Color.ROYALBLUE),

    EAST_SAINT_JOHN_U_14_BOYS(
            "East saint john u14 boys",
            "Thunder",
            true,
            "Saint John",
            UNKNOWN_GYM,
            U_14,
            Color.RED,
            Color.WHITE),

    LANCASTER_B_U_14_BOYS(
            "Lancaster \'B\' u14 boys",
            "Lynx",
            true,
            "Lancaster",
            UNKNOWN_GYM,
            U_14,
            Color.BLUE,
            Color.GOLD),

    WESTERN_VALLEY_B_U_14_BOYS(
            "Western valley u14 boys",
            "Thunder",
            true,
            "Woodstock",
            UNKNOWN_GYM,
            U_14,
            Color.RED,
            Color.WHITE),

    ST_STEPHEN_U_14_BOYS(
            "St. Stephen u14 boys",
            "Spartans",
            true,
            "St. Stephen",
            UNKNOWN_GYM,
            U_14,
            Color.WHITE,
            Color.GREEN),

    MIRAMICHI_A_U_12_BOYS(
            "Miramichi \'A\' u12 boys",
            "Tommies",
            true,
            "Miramichi",
            UNKNOWN_GYM,
            U_12,
            Color.GREEN,
            Color.GOLD),

    BATHURST_U_12_BOYS(
            "Bathurst u12 boys",
            "Phantoms",
            true,
            "Bathurst",
            UNKNOWN_GYM,
            U_12,
            Color.WHITE,
            Color.RED),

    SUSSEX_U_14_GIRLS(
            "Sussex u14 girls",
            "Classic",
            false,
            "Sussex",
            UNKNOWN_GYM,
            U_14,
            Color.RED,
            Color.WHITE),

    SUSSEX_A_U_12_BOYS(
            "Sussex \'A\' u12 boys",
            "Classic",
            true,
            "Sussex",
            UNKNOWN_GYM,
            U_12,
            Color.RED,
            Color.WHITE),

    WOODSTOCK_U_14_GIRLS(
            "Woodstock u14 girls",
            "Thunder",
            false,
            "Woodstock",
            UNKNOWN_GYM,
            U_14,
            Color.WHITE,
            Color.DARKRED),

    CHIPMAN_HIGH_SCHOOL_SENIOR_A_GIRLS(
            "Chipman high school senior girls",
            "Crusaders",
            false,
            "Chipman",
            CHIPMAN_HIGH_SCHOOL,
            A,
            Color.WHITE,
            Color.RED),

    CHIPMAN_HIGH_SCHOOL_SENIOR_A_BOYS(
            "Chipman high school senior boys",
            "Crusaders",
            true,
            "Chipman",
            CHIPMAN_HIGH_SCHOOL,
            A,
            Color.WHITE,
            Color.RED),

    BELLEISLE_HIGH_SCHOOL_SENIOR_A_GIRLS(
            "Belleisle high school senior girls",
            "Bears",
            false,
            "Belleisle",
            UNKNOWN_GYM,
            A,
            Color.BLUE,
            Color.GOLD),

    BELLEISLE_HIGH_SCHOOL_SENIOR_A_BOYS(
            "Belleisle high school senior boys",
            "Bears",
            true,
            "Belleisle",
            UNKNOWN_GYM,
            A,
            Color.BLUE,
            Color.GOLD)
    ;

    private String name, homeTown, mascot;
    private boolean isMale;
    private Gym homeGym;
    private Level level;
    private Color mainColour, secondaryColour;

    Team(String name, String mascot, boolean isMale, String homeTown, Gym homeGym, Level level, Color mainColour, Color secondaryColor) {
        this.name = name;
        this.mascot = mascot;
        this.isMale = isMale;
        this.homeTown = homeTown;
        this.homeGym = homeGym;
        this.level = level;
        this.mainColour = mainColour;
        this.secondaryColour = secondaryColor;
    }

    public String getName() {
        return name;
    }

    public String getHomeTown() {
        return homeTown;
    }

    public Gym getHomeGym() {
        return homeGym;
    }

    public Color getMainColour() {
        return mainColour;
    }

    public Color getSecondaryColour() {
        return secondaryColour;
    }

    public boolean isMale() {
        return isMale;
    }

    public Level getLevel() {
        return level;
    }

    public static ArrayList<Team> getValues() {
        return new ArrayList<>(Arrays.asList(Team.values()));
    }

    public static Comparator<Team> compareTeamNames() {
        return Comparator.comparing(Team::getName);
    }

    public static Team parseTeam(String s) {
//        System.out.print(", team: " + s);
        Team bestPick = UNKNOWN_TEAM;
        int minimumEditDistance = Integer.MAX_VALUE;
        if (s.equals("") || s.equals(" ")) {
            return bestPick;
        }
        else if (s.toUpperCase().contains("FINAL") ||
                 s.toUpperCase().contains("CHAMPION") ||
                 s.toUpperCase().contains("PLACE")) {
            return bestPick;
        }
        for (Team team : getValues()) {
            String teamName = team.getName().toUpperCase();
            String stringIn = s.toUpperCase();
            ArrayList<String> toCheck = new ArrayList<>(Collections.singletonList(teamName));
//            toCheck.addAll(team.getNickNames());
//            System.out.println("name: " + refereeName + ", stringIn: " + stringIn);
            if (toCheck.contains(stringIn)) {
                bestPick = team;
//                System.out.println("FOUND EXACT " + bestPick + "\n\n\ttoCheck:\n" + toCheck);
                break;
            }
            else {
                for (String str : toCheck) {
//                    System.out.println("BEFORE\tstr: " + str + ", stringIn: " + stringIn);
                    if (str.contains(stringIn)) {
                        int u = str.indexOf(stringIn);
                        int v = stringIn.length();
//                        System.out.println("\t\t\tif stringIn: " + stringIn + ", str: " + str + ", u: " + u + ", v: " + v);
                        str = str.substring(u, (u + v));
                    }
                    else if (stringIn.contains(str)) {
                        int u = stringIn.indexOf(str);
                        int v = str.length();
//                        System.out.println("\t\t\telse if stringIn: " + stringIn + ", str: " + str + ", u: " + u + ", v: " + v);
                        stringIn = stringIn.substring(u, (v + v));
                    }
                    int distance = Utilities.getMinEditDist(str, stringIn);
//                    System.out.println("AFTER\tstr: " + str + ", stringIn: " + stringIn + ", distance: " + distance);
                    if (distance < minimumEditDistance) {
                        minimumEditDistance = distance;
                        bestPick = team;
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

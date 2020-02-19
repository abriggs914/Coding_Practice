package sample;

import javafx.scene.paint.Color;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

import static sample.Gym.*;
import static sample.Level.*;

public enum Team {
    FREDERICTON_HIGH_SCHOOL_SR_AAA_BOYS(
            "Fredericton high school senior boys",
            "Black Kats",
            true,
            "Fredericton",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            AAA,
            Color.BLACK,
            Color.GOLD),

    LEO_HAYES_HIGH_SCHOOL_SR_AAA_BOYS(
            "Leo hayes high school senior boys",
            "Lions",
            true,
            "Fredericton",
            LEO_HAYES_HIGH_SCHOOL,
            AAA,
            Color.WHITE,
            Color.BLUE),

    FREDERICTON_HIGH_SCHOOL_SR_AAA_GIRLS(
            "Fredericton high school senior girls",
            "Black Kats",
            false,
            "Fredericton",
            FREDERICTON_HIGH_SCHOOL_MAIN_GYM,
            AAA,
            Color.BLACK,
            Color.GOLD),

    LEO_HAYES_HIGH_SCHOOL_SR_AAA_GIRLS(
            "Leo hayes high school senior girls",
            "Lions",
            false,
            "Fredericton",
            LEO_HAYES_HIGH_SCHOOL,
            AAA,
            Color.WHITE,
            Color.BLUE);

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

    public String toString() {
        return Utilities.titlifyName(name);
    }
}

package sample;

import java.util.Comparator;

public enum Level {
    U_12("u-12"),
    U_14("u-14"),
    MINI("mini"),
    GRADE_6("grade 6"),
    MS_7("grade 7"),
    MS_8("grade 8"),
    A("A"),
    AA("AA"),
    AAA("AAA"),
    JV_A("JV_A"),
    JV_AA("JV_AA"),
    JV_AAA("JV_AAA"),
    SR_EDP("Sr. EDP"),
    JR_EDP("Jr. EDP");

    private String name;

    Level(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public static Comparator<Level> compareLevelNames() {
        return Comparator.comparing(Level::getName);
    }

    public String toString() {
        return name;
    }
}

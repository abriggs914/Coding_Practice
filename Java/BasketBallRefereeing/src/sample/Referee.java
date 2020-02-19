package sample;

import java.sql.Ref;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

public enum Referee {
    AVERY_BRIGGS("Avery Briggs"),
    BEV_AMOS("Bev Amos"),
    KEN_ANDERSON("Ken Anderson"),
    ROD_AUBE("Rod Aube"),
    OLIVIA_BLIZZARD("Olivia Blizzard"),
    PATRICK_BOYD("Patrick Boyd"),
    CRAIG_CLARKSON("Craig Clarkson"),
    TRENT_COLLIER("Trent Collier"),
    MARC_COLWELL("Marc Colwell"),
    JAN_COPELAND("Jan Copeland"),
    STEVE_DEWOLFE("Steve DeWolfe"),
    STEVE_DICKINSON("Steve Dickinson"),
    COLIN_DOLAN("Colin Dolan"),
    TERRY_DOLAN("Terry Dolan"),
    MARCUS_DOLLIVER("Marcus Dolliver"),
    MIKE_DORAN("Mike Doran"),
    MARC_DUGAS("Marc Dugas"),
    DONNIE_FORSYTHE("Donnie Forsythe"),
    GEOFF_HOLLOWAY("Geoff Holloway"),
    PAUL_HORNIBROOK("Paul Hornibrook"),
    ADAM_HUMPHREY("Adam Humphrey"),
    SEAMUS_KELLY("Seamus Kelly"),
    PAUL_LAROCQUE("Paul Larocque"),
    MICHAEL_MACDONALD("Michael MacDonald"),
    DAVE_MACMULLIN("Dave MacMullin"),
    ARTHUR_MCCARTHY("Arthur McCarthy"),
    SHANE_MCCULLUM("Shane McCullum"),
    TODD_MESSER("Todd Messer"),
    MIKE_MURRAY("Mike Murray"),
    HEATHER_OLMSTEAD("Heather Olmstead"),
    IVAN_ROBICHAUD("Ivan Robichaud"),
    MITCHELL_SCEVIOUR("Mitchell Sceviour"),
    ANDREW_SULLIVAN("Andrew Sullivan"),
    MATT_TWEEDIE("Matt Tweedie"),
    MATT_WHIPPLE("Matt Whipple"),
    DAN_WHIPPLE("Dan Wilton"),
    KYLE_WOODWORTH("Kyle Woodworth"),
    KEVIN_ZHOU("Kevin Zhou"),
    EMILIO_ANCHETA("Emilio Ancheta"),
    DAN_BANQUICIO("Dan Banquicio"),
    DEREK_BLACK("Derek Black"),
    JUSTIN_EAGLES("Justin Eagles"),
    MORGAN_GALLANT("Morgan Gallant"),
    MARK_HILLINGHAM("Mark Gillingham"),
    iAN_HUMPHREY("Ian Humphrey"),
    PETER_LINTON("Peter Linton"),
    PAUL_MCCARTHY("Paul McCarthy"),
    JAMIE_MOORE("Jamie Moore"),
    MICHAEL_OBLEUNES("Michael O\'Bleunes"),
    JUSTIN_RIOUX("Justin Rioux");

    private String name;

    Referee(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public static ArrayList<Referee> getValues() {
        return new ArrayList<>(Arrays.asList(Referee.values()));
    }

    public static Comparator<Referee> compareRefereeNames() {
        return Comparator.comparing(Referee::getName);
    }

    public String toString() {
        return name;
    }
}

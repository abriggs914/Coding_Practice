package sample;

import org.omg.CORBA.UNKNOWN;

import java.sql.Ref;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;

public enum Referee {
    UNKNOWN_REFEREE("UNKNOWN", new ArrayList<>(Collections.emptyList())),
    AVERY_BRIGGS("Avery Briggs", new ArrayList<>(Collections.emptyList())),
    BEV_AMOS("Bev Amos", new ArrayList<>(Collections.emptyList())),
    KEN_ANDERSON("Ken Anderson", new ArrayList<>(Collections.emptyList())),
    ROD_AUBE("Rod Aube", new ArrayList<>(Collections.emptyList())),
    OLIVIA_BLIZZARD("Olivia Blizzard", new ArrayList<>(Collections.emptyList())),
    PATRICK_BOYD("Patrick Boyd", new ArrayList<>(Collections.emptyList())),
    CRAIG_CLARKSON("Craig Clarkson", new ArrayList<>(Collections.emptyList())),
    TRENT_COLLIER("Trent Collier", new ArrayList<>(Collections.emptyList())),
    MARC_COLWELL("Marc Colwell", new ArrayList<>(Collections.emptyList())),
    JAN_COPELAND("Jan Copeland", new ArrayList<>(Collections.emptyList())),
    STEVE_DEWOLFE("Steve DeWolfe", new ArrayList<>(Collections.emptyList())),
    STEVE_DICKINSON("Steve Dickinson", new ArrayList<>(Collections.emptyList())),
    COLIN_DOLAN("Colin Dolan", new ArrayList<String>(Collections.singletonList("C.Dolan"))),
    TERRY_DOLAN("Terry Dolan", new ArrayList<String>(Collections.singletonList("T.Dolan"))),
    MARCUS_DOLLIVER("Marcus Dolliver", new ArrayList<>(Collections.emptyList())),
    MIKE_DORAN("Mike Doran", new ArrayList<>(Collections.emptyList())),
    MARC_DUGAS("Marc Dugas", new ArrayList<>(Collections.emptyList())),
    DONNIE_FORSYTHE("Donnie Forsythe", new ArrayList<>(Collections.emptyList())),
    GEOFF_HOLLOWAY("Geoff Holloway", new ArrayList<>(Collections.emptyList())),
    PAUL_HORNIBROOK("Paul Hornibrook", new ArrayList<>(Collections.emptyList())),
    ADAM_HUMPHREY("Adam Humphrey", new ArrayList<String>(Collections.singletonList("A.Humphrey"))),
    SEAMUS_KELLY("Seamus Kelly", new ArrayList<>(Collections.emptyList())),
    PAUL_LAROCQUE("Paul Larocque", new ArrayList<>(Collections.emptyList())),
    MICHAEL_MACDONALD("Michael MacDonald", new ArrayList<>(Collections.emptyList())),
    DAVE_MACMULLIN("Dave MacMullin", new ArrayList<>(Collections.emptyList())),
    ARTHUR_MCCARTHY("Arthur McCarthy", new ArrayList<String>(Collections.singletonList("A.McCarthy"))),
    SHANE_MCCULLUM("Shane McCullum", new ArrayList<>(Collections.emptyList())),
    TODD_MESSER("Todd Messer", new ArrayList<>(Collections.emptyList())),
    MIKE_MURRAY("Mike Murray", new ArrayList<>(Collections.emptyList())),
    HEATHER_OLMSTEAD("Heather Olmstead", new ArrayList<>(Collections.emptyList())),
    IVAN_ROBICHAUD("Ivan Robichaud", new ArrayList<>(Collections.emptyList())),
    MITCHELL_SCEVIOUR("Mitchell Sceviour", new ArrayList<>(Collections.emptyList())),
    ANDREW_SULLIVAN("Andrew Sullivan", new ArrayList<>(Collections.emptyList())),
    MATT_TWEEDIE("Matt Tweedie", new ArrayList<>(Collections.emptyList())),
    MATT_WHIPPLE("Matt Whipple", new ArrayList<>(Collections.emptyList())),
    DAN_WILTON("Dan Wilton", new ArrayList<>(Collections.emptyList())),
    KYLE_WOODWORTH("Kyle Woodworth", new ArrayList<>(Collections.emptyList())),
    KEVIN_ZHOU("Kevin Zhou", new ArrayList<>(Collections.emptyList())),
    EMILIO_ANCHETA("Emilio Ancheta", new ArrayList<>(Collections.emptyList())),
    DAN_BANQUICIO("Dan Banquicio", new ArrayList<>(Collections.emptyList())),
    DEREK_BLACK("Derek Black", new ArrayList<>(Collections.emptyList())),
    JUSTIN_EAGLES("Justin Eagles", new ArrayList<>(Collections.emptyList())),
    MORGAN_GALLANT("Morgan Gallant", new ArrayList<>(Collections.emptyList())),
    MARK_HILLINGHAM("Mark Gillingham", new ArrayList<>(Collections.emptyList())),
    IAN_HUMPHREY("Ian Humphrey", new ArrayList<String>(Collections.singletonList("I.Humphrey"))),
    PETER_LINTON("Peter Linton", new ArrayList<>(Collections.emptyList())),
    PAUL_MCCARTHY("Paul McCarthy", new ArrayList<String>(Collections.singletonList("P.McCarthy"))),
    JAMIE_MOORE("Jamie Moore", new ArrayList<>(Collections.emptyList())),
    MICHAEL_OBLEUNES("Michael O\'Bleunes", new ArrayList<>(Collections.emptyList())),
    JUSTIN_RIOUX("Justin Rioux", new ArrayList<>(Collections.emptyList()));

    private String name;
    private ArrayList<String> nickNames;

    Referee(String name, ArrayList<String> nickNames) {
        this.name = name;
        this.nickNames = new ArrayList<>(nickNames);
    }

    public String getName() {
        return name;
    }

    public ArrayList<String> getNickNames() {
        return nickNames;
    }

    public static ArrayList<Referee> getValues() {
        return new ArrayList<>(Arrays.asList(Referee.values()));
    }

    public static Comparator<Referee> compareRefereeNames() {
        return Comparator.comparing(Referee::getName);
    }

    public static Referee parseReferee(String s) {
//        System.out.print(", referee: " + s);
        Referee bestPick = UNKNOWN_REFEREE;
        int minimumEditDistance = Integer.MAX_VALUE;
        if (s.equals("") || s.equals(" ")) {
            return bestPick;
        }
        for (Referee referee : getValues()) {
            String refereeName = referee.getName().toUpperCase();
            String stringIn = s.toUpperCase();
            ArrayList<String> toCheck = new ArrayList<>(Collections.singletonList(refereeName));
            toCheck.addAll(referee.getNickNames());
//            System.out.println("name: " + refereeName + ", stringIn: " + stringIn);
            if (toCheck.contains(stringIn)) {
                bestPick = referee;
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
                        bestPick = referee;
                    }
                }
            }
        }
        return bestPick;
    }

    public String toString() {
        return name;
    }
}

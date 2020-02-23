package sample;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

import static sample.Gym.*;
import static sample.Referee.*;
import static sample.Team.*;

public class SampleGames {

    private ArrayList<Game> gamesList;

    public SampleGames() {
        this.gamesList = new ArrayList<>();
    }

    public ArrayList<Game> getGames() {
        return this.gamesList;
    }

    public void load_Fall_2019() {

        GameManager gameManager = Main.gameManager;

//        Team homeTeam = FREDERICTON_HIGH_SCHOOL_SR_AAA_BOYS;
//        Team awayTeam = LEO_HAYES_HIGH_SCHOOL_SR_AAA_BOYS;
//        Referee refA = AVERY_BRIGGS;
//        Referee refB = TERRY_DOLAN;
//        Gym gym = FREDERICTON_HIGH_SCHOOL_MAIN_GYM;
//        Date day = new Date();
//        gameManager.createNewGame(day, gym, refA, refB, homeTeam, awayTeam);
        ArrayList<String> gameStrings = new ArrayList<>(Arrays.asList(
                "Sat, Sep 14, 2019 1:10 PM###Currie Center_Perf###Jr EDP###F### ### ###MacDonald###Briggs###$20### ",
                "Sat, Sep 14, 2019 2:15 PM###Currie Center_Perf###Jr EDP###M### ### ###MacDonald###Briggs###$20### ",
                "Thu, Sep 19, 2019 5:30 PM###FHS###FHSSP###M###Kentucky###Michigan###Hornibrook###Briggs###$20### ",
                "Thu, Sep 19, 2019 6:30 PM###FHS###FHSSP###M###Lousville###Syracuse###Hornibrook###Briggs###$20### ",
                "Sun, Oct 20, 2019 12:30 PM###Currie Ctr_Rec2_2###Jr EDP### |## ###|Briggs###cancel### ",
                "Sun, Oct 20, 2019 1:30 PM###Currie Ctr_Rec2_2###Jr EDP### ### ###Briggs###cancel### ",
                "Sun, Oct 20, 2019 2:30 PM###Currie Ctr_Rec2_2###Jr EDP### ### ###Briggs###cancel### ",
                "Sun, Oct 20, 2019 3:30 PM###Currie Ctr_Rec2_2###Jr EDP### ### ###Briggs###cancel### ",
                "Sat, Nov 02, 2019 9:00 AM###Leo Hayes###U14###F###Riverview 'A'###NMBA tier 1###Briggs###Dugas###$34### ",
                "Sat, Nov 02, 2019 10:30 AM###Leo Hayes###U14###F###KVBA 'A'###Moncton 'A'###Briggs###Dugas###$34### ",
                "Sun, Nov 03, 2019 4:00 PM###Eclaireurs - Gym 1###U14###F###Championship [Tier 1]### ###Briggs###Robichaud###$34### ",
                "Sat, Nov 09, 2019 1:00 PM###Harvey###A###F###Harvey###Grand Manan###Briggs###Aube###$44###$35",
                "Sat, Nov 09, 2019 2:45 PM###Harvey###A###F###Caledonia###Hartland###Briggs###Aube###$44### ",
                "Sun, Nov 10, 2019 9:15 AM###FHS-side###U14###M###YCBC Tier 1### ###Briggs###Anderson###$34### ",
                "Sun, Nov 10, 2019 10:30 AM###FHS-side###U14###M###YCBC Tier 1### ###Briggs###Linton###$34### ",
                "Wed, Nov 13, 2019 5:00 PM###Harvey###JV-A###F###Harvey###Fredericton Exhibition###Briggs###MacMullin###$44###$35",
                "Sat, Nov 16, 2019 9:00 AM###Naasis - Ct3###U14###M###YCBC Tier 2###Carleton North###Briggs###I.Humphrey###$34### ",
                "Sat, Nov 16, 2019 10:30 AM###Naasis - Ct3###U14###M###East Saint John###Moncton 'B'###Briggs###I.Humphrey###$34### ",
                "Sat, Nov 16, 2019 12:00 PM###Naasis - Ct3###U14###M###Riverview###KVBA 'A'###Briggs###I.Humphrey###$34### ",
                "Sun, Nov 17, 2019 8:30 AM###Naasis - Ct2###U14###M###Lancaster 'B'###NMBA Tier 2###Dugas###Briggs###$34### ",
                "Sun, Nov 17, 2019 10:00 AM###Naasis - Ct2###U14###M###Western Valley 'B'###St. Stephen###Dugas###Briggs###$34### ",
                "Sat, Nov 23, 2019 11:00 AM###Cambridge-Narrows###A###F###Cambridge-Narrows###Caledonia###Colwell###Briggs###cancel### ",
                "Sat, Nov 23, 2019 12:45 PM###Cambridge-Narrows###A###M###Cambridge-Narrows###Caledonia###Colwell###Briggs###cancel### ",
                "Sun, Nov 24, 2019 10:30 AM###Gibson-Neill###U12###M###NMBA Tier 2### ###Moore###Briggs###$29### ",
                "Mon, Nov 25, 2019 5:30 PM###Harvey###JV-A###F###Harvey###St. Stephen###Briggs###MacMullin###cancel### ",
                "Sat, Dec 07, 2019 1:30 PM###Garden Creek###U12-T3###M###Riverview 'B'###Grand Manan###Rioux###Briggs###$29### ",
                "Sat, Dec 07, 2019 3:00 PM###Garden Creek###U12-T3###M###YCBC U10 Tier 1###Miramichi 'A'###Rioux###Briggs###$29### ",

                "Sat, Dec 07, 2019 4:30 PM###Garden Creek###U12-T3###M###Bathurst###Grand Manan###Hornibrook###Briggs###$29### ",
                "Sat, Dec 07, 2019 7:30 PM###Devon Middle###U12-T2###M###Sussex 'A'###Miramichi 'A'###Briggs###Gallant###$29### ",
                "Sun, Dec 08, 2019 9:00 AM###Priestman St###U12-T4###M###Semi-final### ###Sceviour###Briggs###$29### ",
                "Sun, Dec 08, 2019 10:30 AM###Priestman St###U12-T4###M###Semi-final### ###Sceviour###Briggs###$29### ",
                "Sun, Dec 08, 2019 1:30 PM###Leo Hayes###U14-T2###F###3rd Place### ###Briggs###Dolliver###$34### ",
                "Sun, Dec 08, 2019 3:00 PM###Leo Hayes###U14-T2###F###Championship### ###Briggs###Dolliver###$34### ",
                "Sun, Dec 15, 2019 10:30 AM###Currie Centre_Rec###U14###F###NMBA Tier 1###Woodstock###Robichaud###Briggs###$34### ",
                "Sun, Dec 15, 2019 12:00 PM###Currie Centre_Rec###U14###F###Woodstock###Sussex###Rioux###Briggs###$34### ",
                "Mon, Dec 16, 2019 6:00 PM###Chipman###A###M###Chipman###Caledonia###Amos###Briggs###$44### ",
                "Mon, Dec 16, 2019 7:45 PM###Chipman###A###F###Chipman###Caledonia###Amos###Briggs###$44### ",
                "Thu, Dec 19, 2019 6:00 PM###Chipman###A###F###Chipman###Belleisle###Briggs###Dickinson###$44###$57",
                "Thu, Dec 19, 2019 7:45 PM###Chipman###A###M###Chipman###Belleisle###Briggs###Dickinson###$44### "));
        this.gamesList = new ArrayList<>(parseGameStrings(gameStrings));
    }

    private ArrayList<Game> parseGameStrings(ArrayList<String> gameStrings) {
        ArrayList<Game> res = new ArrayList<>();
        for (String s : gameStrings) {
            if (s.contains("cancel")) {
//                System.out.println("CANCELLED: " + s);
            }
            else {
                String[] stringSplit = s.split("###");
//                System.out.println("\n\n\tPARSING: " + s + "\n\t\t(" + stringSplit.length + ")->:\t" + Arrays.toString(stringSplit));

//                System.out.print("\tPARSING: ");
                Date day = Utilities.parseDate(stringSplit[0]);
                Gym gym = Gym.parseGym(stringSplit[1]);
                Referee refereeA = Referee.parseReferee(stringSplit[6]);
                Referee refereeB = Referee.parseReferee(stringSplit[7]);

                String homeString = prepTeamString(stringSplit, true);
                String awayString = prepTeamString(stringSplit, false);

                Team homeTeam = Team.parseTeam(homeString);
                Team awayTeam = Team.parseTeam(awayString);
//                System.out.println();
//                System.out.println( "\t\tPARSED:\n\tDate:\t\t" + day +
//                                    "\n\tGym:\t\t" + gym +
//                                    "\n\tRefereeA:\t" + refereeA +
//                                    "\n\tRefereeB:\t" + refereeB +
//                                    "\n\tHomeTeam:\t" + homeTeam +
//                                    "\n\tAwayTeam:\t" + awayTeam);
                Game g = Main.gameManager.createGameObject(day, gym, refereeA, refereeB, homeTeam, awayTeam);
                res.add(g);
            }
        }
        return res;
    }

    public String prepTeamString(String[] stringSplit, boolean forTeam1) {
        String level = stringSplit[2].trim().toUpperCase();
        String gender = stringSplit[3].trim().toUpperCase();
        String team1 = stringSplit[4].trim().toUpperCase();
        String team2 = stringSplit[5].trim().toUpperCase();

        String genderString = ((gender.equals("M"))? " boys" : " girls");

        String levelString = ((level.contains("A"))? " high school" : "");
        levelString += ((level.contains("JV"))? " junior" : "");
        levelString += ((level.contains("A") && !level.contains("JV"))? " senior" : "");

        String genderLevelString = levelString + genderString;
        StringBuilder res = new StringBuilder();

        String x = ((forTeam1)? team1 : team2);
        String[] xSplit = x.split(" ");
        for (int i = 0; i < xSplit.length; i++) {
            String str = xSplit[i];
//            System.out.println("\ni: (" + i + " of " + xSplit.length + "), str: " + str + "res: {" + res + "}\n");
            if (str.length() == 0) {
                return res.toString();
            }
            if (i == 0) {
                res.append(str).append(levelString);
            }
            else {
                res.append(" ").append(str);
            }
        }
        res.append(genderString);
        return res.toString();
    }
}

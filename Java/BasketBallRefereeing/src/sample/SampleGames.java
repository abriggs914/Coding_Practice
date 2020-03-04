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
                /////
                "Sun, Oct 20, 2019 12:30 PM###Currie Ctr_Rec2_2###Jr EDP### |## ###|Briggs###cancel### ",
                "Sun, Oct 20, 2019 1:30 PM###Currie Ctr_Rec2_2###Jr EDP### ### ###Briggs###cancel### ",
                "Sun, Oct 20, 2019 2:30 PM###Currie Ctr_Rec2_2###Jr EDP### ### ###Briggs###cancel### ",
                "Sun, Oct 20, 2019 3:30 PM###Currie Ctr_Rec2_2###Jr EDP### ### ###Briggs###cancel### ",
                /////
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
                /////
                "Sat, Nov 23, 2019 11:00 AM###Cambridge-Narrows###A###F###Cambridge-Narrows###Caledonia###Colwell###Briggs###cancel### ",
                "Sat, Nov 23, 2019 12:45 PM###Cambridge-Narrows###A###M###Cambridge-Narrows###Caledonia###Colwell###Briggs###cancel### ",
                /////
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
        if (this.gamesList.size() == 0) {
            this.gamesList = new ArrayList<>(parseGameStrings(gameStrings));
        }
        else {
            this.gamesList.addAll(parseGameStrings(gameStrings));
        }
    }

    public void load_Full_season_2018_2019() {
        ArrayList<String> gameStrings = new ArrayList<>(Arrays.asList(
                "Fri, Sep 14, 2018 6:00 PM###Currie Center_Perf###Sr EDP### ### ###M###Tweedie###Briggs###$25### ",
                "Fri, Sep 14, 2018 7:00 PM###Currie Center_Perf###Sr EDP### ### ###M###Tweedie###Briggs###$25### "
//                "Thu, Oct 04, 2018 5:30 PM FHS FHSSP M Warriors Celtics Wilton Briggs $20",
//                "Thu, Oct 04, 2018 6:30 PM FHS FHSSP M Lakers Spurs Wilton Briggs $20",
//                "Sat, Oct 20, 2018 9:00 AM Naasis-Ct1 Jr EDP M Flann Briggs cancel",
//                "Sat, Oct 20, 2018 10:00 AM Naasis-Ct1 Jr EDP M Flann Briggs $20",
//                "Sat, Oct 20, 2018 11:00 AM Naasis-Ct1 Jr EDP M Flann Briggs $20",
//                "Sat, Oct 20, 2018 12:00 PM Naasis-Ct1 Jr EDP M Flann Briggs $20",
//                "Sat, Nov 03, 2018 12:00 PM Naasis-Ct1 U14 F Riverview 'A' Fundy Zhou Briggs $32",
//                "Sat, Nov 03, 2018 1:30 PM Naasis-Ct1 U14 F River Valley Moncton 'B' Zhou Briggs $32",
//                "Sat, Nov 10, 2018 1:00 PM Harvey A F Caledonia Hartland DeWolfe Briggs $42",
//                "Sat, Nov 10, 2018 2:45 PM Harvey A F Harvey St. Stephen DeWolfe Briggs $42",
//                "Tue, Nov 13, 2018 6:00 PM Eclaireurs A M FCA OHS Holloway Briggs cancel",
//                "Fri, Nov 16, 2018 5:30 PM Harvey JV-A F Harvey ESA McCullum Briggs cancel",
//                "Sat, Nov 17, 2018 9:00 AM Naasis-Ct1 U14 M NMBA Tier 2 Grand Falls Anderson Briggs $32",
//                "Sat, Nov 17, 2018 12:30 PM Cambridge-Narrows A M Cambridge-Narrows Blackville Zhou Briggs $42",
//                "Sat, Nov 17, 2018 2:15 PM Cambridge-Narrows A F Chipman Belleisle Zhou Briggs $42",
//                "Sat, Nov 17, 2018 4:00 PM Cambridge-Narrows A M Chipman Blackville Zhou Briggs $42",
//                "Sun, Nov 18, 2018 2:15 PM Cambridge-Narrows A F Championship T.Dolan Briggs $42",
//                "Sun, Nov 18, 2018 4:00 PM Cambridge-Narrows A M Championship T.Dolan Briggs $42",
//                "Mon, Nov 19, 2018 5:30 PM OHS JV-AA F OHS Woodstock Holloway Briggs $42",
//                "Mon, Nov 19, 2018 7:15 PM OHS JV-AA M OHS Woodstock Holloway Briggs $42",
//                "Tue, Nov 20, 2018 6:00 PM Eclaireurs A M FCA Tobique Valley MacDonald Briggs cancel",
//                "Sat, Nov 24, 2018 1:00 PM Stanley A M Stanley Dalhousie Aube Briggs $42",
//                "Mon, Nov 26, 2018 7:00 PM OHS JV-AA F OHS Leo Hayes Amos Briggs $42",
//                "Tue, Nov 27, 2018 6:30 PM OHS AA M OHS FHS Exhib McCullum Briggs cancel",
//                "Fri, Nov 30, 2018 4:35 PM ESA AA M Carleton North Bathurst Briggs Dickinson $42",
//                "Fri, Nov 30, 2018 8:15 PM Eclaireurs AA M Pugwash HTHS Woodworth Briggs $42",
//                "Sat, Dec 01, 2018 3:35 PM Eclaireurs JV-AAA M FHS Northumberland Dugas Briggs $42",
//                "Sat, Dec 01, 2018 7:15 PM Eclaireurs-Ct2 A F Quarter-Final Briggs Wilton $42",
//                "Sat, Dec 01, 2018 9:05 PM Eclaireurs-Ct2 A M Bathurst John Caldwell Briggs Wilton $42",
//                "Wed, Dec 05, 2018 6:30 PM OHS AA M OHS Stanley McCullum Briggs $42",
//                "Thu, Dec 06, 2018 7:00 PM Leo Hayes JV-AAA M Leo Hayes Stanley Robichaud Briggs $42",
//                "Sat, Dec 15, 2018 11:00 AM Minto A F Minto Petitcodiac Colwell Briggs $42",
//                "Sat, Dec 15, 2018 12:45 PM Minto A M Minto Petitcodiac Colwell Briggs $42",
//                "Tue, Dec 18, 2018 5:00 PM Chipman A F Chipman Moncton Christian Aube Briggs cancel",
//                "Tue, Dec 18, 2018 6:45 PM Chipman A M Chipman Moncton Christian Aube Briggs cancel",
//                "Sat, Jan 05, 2019 10:00 AM Minto A F Minto Cambridge-Narrows C.Dolan Briggs $42",
//                "Sat, Jan 05, 2019 12:00 PM Minto A M Minto Cambridge-Narrows C.Dolan Briggs $42",
//                "Sun, Jan 06, 2019 2:00 PM Minto A F Championship Zhou Briggs $42",
//                "Sun, Jan 06, 2019 4:00 PM Minto A M Championship Zhou Briggs $42",
//                "Mon, Jan 07, 2019 5:00 PM Cambridge-Narrows A F Cambridge-Narrows Moncton Christian Holloway Briggs $42",
//                "Mon, Jan 07, 2019 6:45 PM Cambridge-Narrows A M Cambridge-Narrows Moncton Christian Holloway Briggs $42",
//                "Wed, Jan 09, 2019 5:00 PM CNBA A F CNBA Blackville T.Dolan Briggs cancel",
//                "Wed, Jan 09, 2019 6:45 PM CNBA A M CNBA Blackville T.Dolan Briggs cancel",
//                "Sat, Jan 12, 2019 4:00 PM Bliss Carman MS8-1 M Naasis George St. Blizzard Briggs $32",
//                "Sat, Jan 12, 2019 5:30 PM Bliss Carman MS8-1 M Bliss Carman Harold Peterson Blizzard Briggs $32",
//                "Mon, Jan 14, 2019 6:00 PM Minto JV-A M Minto CNBA Briggs Amos $42 $38",
//                "Wed, Jan 16, 2019 4:30 PM Minto Middle Varsity F Minto Middle Harold Peterson Aube Briggs $32",
//                "Wed, Jan 16, 2019 5:45 PM Minto Middle Varsity M Minto Middle Harold Peterson Aube Briggs $32",
//                "Sat, Jan 19, 2019 11:00 AM Cambridge-Narrows A F Cambridge-Narrows Caledonia Briggs Dickinson $42 $53",
//                "Sat, Jan 19, 2019 12:45 PM Cambridge-Narrows A M Cambridge-Narrows Caledonia Briggs Dickinson cancel",
//                "Sat, Jan 19, 2019 6:00 PM George St. MS8-1 M Championship Dickinson Briggs $32",
//                "Sun, Jan 20, 2019 9:00 AM Bliss Carman MS8-1 F Semi-Final Colwell Briggs cancel",
//                "Sun, Jan 20, 2019 10:30 AM Bliss Carman MS8-1 F Semi-Final Colwell Briggs cancel",
//                "Mon, Jan 21, 2019 5:00 PM Chipman JV M Chipman Cambridge-Narrows Briggs Bennett cancel",
//                "Mon, Jan 21, 2019 6:15 PM Chipman JV F Chipman Gagetown Briggs Bennett cancel",
//                "Tue, Jan 22, 2019 6:00 PM Eclaireurs MS8-2 F FCA Bliss Carman Cormier Briggs $32",
//                "Wed, Jan 23, 2019 4:30 PM CNBA MS8-2 M CNBA Stanley Aube Briggs cancel",
//                "Wed, Jan 23, 2019 6:00 PM CNBA MS6 F CNBA FCA White Aube Briggs cancel",
//                "Sat, Jan 26, 2019 8:30 AM Minto Middle Varsity F Minto Middle Cambridge-Narrows Briggs Blizzard cancel",
//                "Sat, Jan 26, 2019 10:00 AM Minto Middle Varsity F Harold Peterson Ridgeview Briggs Blizzard cancel",
//                "Sat, Jan 26, 2019 11:30 AM Minto Middle Varsity F Cambridge-Narrows Stanley Briggs Blizzard cancel",
//                "Sun, Jan 27, 2019 12:00 PM Bliss Carman MS7 M 5th Place Flann Briggs cancel",
//                "Sun, Jan 27, 2019 1:30 PM Bliss Carman MS7 M 3rd Place Flann Briggs cancel",
//                "Mon, Jan 28, 2019 4:00 PM Stanley A F Stanley Dalhousie Holloway Briggs $42",
//                "Mon, Jan 28, 2019 6:00 PM Stanley A F Stanley Blackville Holloway Briggs $42",
//                "Mon, Jan 28, 2019 8:00 PM Stanley A M Stanley Blackville Holloway Briggs $42",
//                "Tue, Jan 29, 2019 5:00 PM F'ton Junction JV F Sunbury West Gagetown Briggs Robichaud $32 $30",
//                "Tue, Jan 29, 2019 6:15 PM F'ton Junction Varsity M Sunbury West Minto Middle Briggs Robichaud $32",
//                "Wed, Jan 30, 2019 5:00 PM CNBA A M CNBA Blackville Briggs Dickinson cancel",
//                "Wed, Jan 30, 2019 6:45 PM CNBA A F CNBA Blackville Briggs Dickinson cancel",
//                "Sat, Feb 02, 2019 1:30 PM F'ton Junction Bantam F Grand Manan Harold Peterson Briggs Bennett $32 $30",
//                "Sat, Feb 02, 2019 3:00 PM F'ton Junction Bantam F Devon Middle St. Stephen Briggs Bennett $32",
//                "Sat, Feb 02, 2019 4:30 PM F'ton Junction Bantam F Minto JV Grand Manan Briggs Bennett $32",
//                "Sun, Feb 03, 2019 10:30 AM Park St U10 M NMBA Harvey Briggs I.Humphrey $27",
//                "Sun, Feb 03, 2019 12:00 PM Park St U10 M Harvey Lancaster Briggs I.Humphrey $27",
//                "Sun, Feb 03, 2019 1:30 PM Park St U10 M NMBA Lancaster Briggs I.Humphrey $27",
//                "Mon, Feb 04, 2019 4:45 PM George St. MS6 M George St. Naasis Briggs O'Blenes $27",
//                "Mon, Feb 04, 2019 6:15 PM George St. MS6 F George St. Bliss Carman Briggs O'Blenes $27",
//                "Tue, Feb 05, 2019 6:15 PM George St. MS8-1 F George St. Naasis Briggs Zhou $32",
//                "Fri, Feb 08, 2019 5:00 PM Naasis-Ct1 MS6 F Minto Middle JV Bliss Carman Gallant Briggs cancel",
//                "Sat, Feb 09, 2019 1:30 PM CNBA MS8-2 F Colwell Briggs cancel",
//                "Sun, Feb 10, 2019 12:00 PM Barker's Point U12 F Rioux Briggs cancel",
//                "Sun, Feb 10, 2019 1:30 PM Barker's Point U12 F NMBA Tier 1 Copeland Briggs cancel",
//                "Sun, Feb 10, 2019 3:00 PM Currie Center_Rec2 U14 M KVBA 'A' Moncton 'A' Briggs Colwell $32",
//                "Sun, Feb 10, 2019 4:30 PM Currie Center_Rec2 U14 M YCBC Tier 1 Moncton 'A' Briggs T.Dolan $32",
//                "Mon, Feb 11, 2019 5:00 PM Gagetown JV F Gagetown Sunbury West Briggs Dickinson $32 $45",
//                "Tue, Feb 12, 2019 4:30 PM Minto Middle JV F Minto Middle Chipman Blizzard Briggs $32",
//                "Wed, Feb 13, 2019 4:00 PM Eclaireurs MS8-2 F FCA Devon Middle Red Briggs T.Dolan cancel",
//                "Fri, Feb 15, 2019 5:30 PM Eclaireurs MS8-2 F FCA Devon Middle Red Briggs Colwell $32",
//                "Sat, Feb 16, 2019 1:00 PM Naasis MS-T5 F Bliss Carman Tier 2 Grand Manan Briggs A.McCarthy $32",
//                "Sat, Feb 16, 2019 2:30 PM Naasis MS-T5 F Bliss Carman JV Max Aitken Briggs A.McCarthy $32",
//                "Sat, Feb 16, 2019 4:00 PM Naasis MS-T5 F Grand Manan Naasis JV Briggs Dickinson $32",
//                "Sun, Feb 17, 2019 1:30 PM F'ton Junction MS-T6 M 3rd Place Briggs Collier $32 $30",
//                "Sun, Feb 17, 2019 3:00 PM F'ton Junction MS-T6 M Provincial Championship Briggs Collier $32",
//                "Tue, Feb 19, 2019 5:00 PM Naasis-Ct3 MS6 M Naasis Keswick Valley Gallant Briggs $27",
//                "Thu, Feb 21, 2019 4:45 PM George St. MS8-1 M George St. Naasis Briggs Clarkson $32",
//                "Sat, Feb 23, 2019 10:00 AM Park St. U12-T4 M YCBC Tier 2 River Valley Dickinson Briggs $27",
//                "Sat, Feb 23, 2019 11:30 AM Park St. U12-T4 M SJ Rising Stars Moncton 'C' Dickinson Briggs $27",
//                "Sun, Feb 24, 2019 9:00 AM Currie Center_Rec U12-T2 F Moncton 'B' YCBC Tier 2 Black Briggs Clarkson $27",
//                "Sun, Feb 24, 2019 10:30 AM Currie Center_Rec U12-T2 F Centreville Sussex Briggs Clarkson $27",
//                "Mon, Feb 25, 2019 4:00 PM Harold Sappier MS8-2A F Quarter-Final [CNBA vs Nackawic] Briggs Dickinson cancel",
//                "Thu, Feb 28, 2019 5:00 PM Harold Peterson JV M District Championship Anderson Briggs $32",
//                "Thu, Feb 28, 2019 6:15 PM Harold Peterson Varsity M District Championship Anderson Briggs $32",
//                "Fri, Mar 01, 2019 6:00 PM Bliss Carman MS8-1 M Bliss Carman George St. Blizzard Briggs $32",
//                "Sun, Mar 10, 2019 12:00 PM UNB_LB Gym U14 M East Saint John Bath McCullum Briggs $32",
//                "Sun, Mar 10, 2019 1:30 PM UNB_LB Gym U14 M NMBA Tier 2 Bath Anderson Briggs $32",
//                "Sat, Mar 16, 2019 1:00 PM Currie Center_ Perf U14-T1 M KVBA 'A' YCBC Tier 1 Briggs P.McCarthy $32",
//                "Sat, Mar 23, 2019 1:30 PM Harvey U16-T2 F RVBA Woodstock Blizzard Briggs $42",
//                "Sat, Mar 23, 2019 3:15 PM Harvey U16-T2 F Miramichi Fundy Blizzard Briggs $42"
        ));
        if (this.gamesList.size() == 0) {
            this.gamesList = new ArrayList<>(parseGameStrings(gameStrings));
        }
        else {
            this.gamesList.addAll(parseGameStrings(gameStrings));
        }
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

package sample;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;

public class GameHistoryForm {

    private Date date, firstDate, lastDate;
    private String timeString;
    private double offset;
    private Gym gym;
    private Team homeTeam, awayTeam;
    private Referee refereeA, refereeB;
    private boolean filterDate, filterTime, filterGym, filterHomeTeam, filterAwayTeam, filterRefereeA, filterRefereeB;
    private boolean noFilterSelected, startFromBeginning, graphToEnd;

    public GameHistoryForm() {

    }

    public void collectAttributes() {
        this.date = Controller.gameHistory_getDate();
        this.timeString = Utilities.getTimeString(this.date);
        this.offset = Controller.gameHistory_getOffset();
        this.gym = Controller.gameHistory_getGym();
        this.homeTeam = Controller.gameHistory_getHomeTeam();
        this.awayTeam = Controller.gameHistory_getAwayTeam();
        this.refereeA = Controller.gameHistory_getRefereeA();
        this.refereeB = Controller.gameHistory_getRefereeB();

        this.filterDate = Controller.gameHistory_getDateFilterStatus();
        this.filterTime = Controller.gameHistory_getTimeFilterStatus();
        this.filterGym = Controller.gameHistory_getGymFilterStatus();
        this.filterHomeTeam = Controller.gameHistory_getHomeTeamFilterStatus();
        this.filterAwayTeam = Controller.gameHistory_getAwayTeamFilterStatus();
        this.filterRefereeA = Controller.gameHistory_getRefereeAFilterStatus();
        this.filterRefereeB = Controller.gameHistory_getRefereeBFilterStatus();

        this.noFilterSelected = checkFilterSelection();
        this.startFromBeginning = Controller.gameHistory_getStartBeginning();
        this.graphToEnd = Controller.gameHistory_getGraphToEnd();
    }

    public boolean checkValid() {
        if (this.date != null) {
            if (this.timeString != null) {
                if (this.gym != null) {
                    if (this.homeTeam != null) {
                        if (this.awayTeam != null) {
                            if (this.refereeA != null) {
                                if (this.refereeB != null) {
                                    return true;
                                }
                            }
                        }
                    }
                }
            }
        }
        return false;
    }

    public boolean checkFilterSelection() {
        if (!filterDate) {
            if (!filterTime){
                if (!filterGym){
                    if (!filterHomeTeam){
                        if (!filterAwayTeam){
                            if (!filterRefereeA){
                                if (!filterRefereeB){
                                    return true;
                                }
                            }
                        }
                    }
                }
            }
        }
        return false;
    }

    public boolean checkSelectionValidity() {
        if (this.filterDate && this.date == null) {
            return false;
        }
        if (this.filterTime && this.timeString == null) {
            return false;
        }
        if (this.filterGym && this.gym == null) {
            return false;
        }
        if (this.filterHomeTeam && this.homeTeam == null) {
            return false;
        }
        if (this.filterAwayTeam && this.awayTeam == null) {
            return false;
        }
        if (this.filterRefereeA && this.refereeA == null) {
            return false;
        }
        if (this.filterRefereeB && this.refereeB == null) {
            return false;
        }
        return true;
    }

    public ArrayList<Game> getFilteredGames() {
        ArrayList<Game> games = new ArrayList<>(Main.gameManager.getGames());
        // TODO ensure that the games list is sorted by date
        if (games.size() > 0) {
            this.firstDate = ((startFromBeginning)? Utilities.getFirstDate(games) : Controller.gameHistory_getStartDate());
            this.lastDate = ((graphToEnd)? Utilities.getLastDate(games) : Controller.gameHistory_getEndDate());
        }
        if (!startFromBeginning || !graphToEnd) {
            System.out.println("filtering between dates: {" + firstDate + " and " + lastDate + "}");
            games = new ArrayList<>(Main.gameManager.filterGamesBetweenDates(games, this.firstDate, this.lastDate));
        }
//        System.out.println("startFromBeginning: " + startFromBeginning + ", graphToEnd: " + graphToEnd + "\nFiltering between: " + Utilities.getDateString(firstDate) + " and " + Utilities.getDateString(lastDate));
        if (this.filterDate) {
            System.out.println("filtering by Date {" + date + "}");
            games = new ArrayList<>(Main.gameManager.filterGamesForDate(games, this.date, this.firstDate, this.lastDate));
        }
        if (this.filterTime) {
            System.out.println("filtering by Time {" + date + "}");
            games = new ArrayList<>(Main.gameManager.filterGamesForTime(games, this.date, this.offset, this.firstDate, this.lastDate));
        }
        if (this.filterGym) {
            System.out.println("filtering by Gym {" + gym + "}");
            games = new ArrayList<>(Main.gameManager.filterGamesForGym(games, this.gym, this.firstDate, this.lastDate));
        }
        if (this.filterHomeTeam) {
            System.out.println("filtering by Home Team {" + homeTeam + "}");
            games = new ArrayList<>(Main.gameManager.filterGamesForTeam(games, this.homeTeam, true, this.firstDate, this.lastDate));/////////////////////////////////////////////////////////
        }
        if (this.filterAwayTeam) {
            System.out.println("filtering by Away Team {" + awayTeam + "}");
            games = new ArrayList<>(Main.gameManager.filterGamesForTeam(games, this.awayTeam, false, this.firstDate, this.lastDate));/////////////////////////////////////////////////////////
        }
        if (this.filterRefereeA) {
            System.out.println("filtering by Referee A {" + refereeA + "}");
            games = new ArrayList<>(Main.gameManager.filterGamesForReferee(games, this.refereeA, true, this.firstDate, this.lastDate));/////////////////////////////////////////////////////////
        }
        if (this.filterRefereeB) {
            System.out.println("filtering by Referee B {" + refereeB + "}");
            games = new ArrayList<>(Main.gameManager.filterGamesForReferee(games, this.refereeB, false, this.firstDate, this.lastDate));/////////////////////////////////////////////////////////
        }
        return games;
    }

    public boolean isFilterDate() {
        return filterDate;
    }

    public boolean isFilterTime() {
        return filterTime;
    }

    public boolean isFilterGym() {
        return filterGym;
    }

    public boolean isFilterHomeTeam() {
        return filterHomeTeam;
    }

    public boolean isFilterAwayTeam() {
        return filterAwayTeam;
    }

    public boolean isFilterRefereeA() {
        return filterRefereeA;
    }

    public boolean isFilterRefereeB() {
        return filterRefereeB;
    }

    public boolean isNoFilterSelected() {
        return noFilterSelected;
    }

    public boolean isStartFromBeginning() {
        return startFromBeginning;
    }

    public boolean isGraphToEnd() {
        return graphToEnd;
    }

    public Date getFirstDate() {
        return firstDate;
    }

    public Date getLastDate() {
        return lastDate;
    }
}

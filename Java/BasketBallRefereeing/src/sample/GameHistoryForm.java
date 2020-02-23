package sample;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;

public class GameHistoryForm {

    private Date date;
    private String timeString;
    private double offset;
    private Gym gym;
    private Team homeTeam, awayTeam;
    private Referee refereeA, refereeB;
    private boolean filterDate, filterTime, filterGym, filterHomeTeam, filterAwayTeam, filterRefereeA, filterRefereeB;

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
        if (this.filterDate) {
            System.out.println("filtering by Date");
//            ArrayList<Game> temp = Main.gameManager.filterGamesForDate(games, this.date);
//            games.clear();
//            games.addAll(temp);
            games = new ArrayList<>(Main.gameManager.filterGamesForDate(games, this.date));
        }
        if (this.filterTime) {
            System.out.println("filtering by Time");
            ArrayList<Game> temp = Main.gameManager.filterGamesForTime(games, this.date, this.offset, true);///////////////////////////////////////////////
            games.clear();
            games.addAll(temp);
        }
        if (this.filterGym) {
            System.out.println("filtering by Gym");
            ArrayList<Game> temp = Main.gameManager.filterGamesForGym(games, this.gym);
            games.clear();
            games.addAll(temp);
        }
        if (this.filterHomeTeam) {
            System.out.println("filtering by Home Team");
            ArrayList<Game> temp = Main.gameManager.filterGamesForTeam(games, this.homeTeam, true);/////////////////////////////////////////////////////////
            games.clear();
            games.addAll(temp);
        }
        if (this.filterAwayTeam) {
            System.out.println("filtering by Away Team");
            ArrayList<Game> temp = Main.gameManager.filterGamesForTeam(games, this.awayTeam, true);/////////////////////////////////////////////////////////
            games.clear();
            games.addAll(temp);
        }
        if (this.filterRefereeA) {
            System.out.println("filtering by Referee A");
            ArrayList<Game> temp = Main.gameManager.filterGamesForReferee(games, this.refereeA, true);/////////////////////////////////////////////////////////
            games.clear();
            games.addAll(temp);
        }
        if (this.filterRefereeB) {
            System.out.println("filtering by Referee B");
            ArrayList<Game> temp = Main.gameManager.filterGamesForReferee(games, this.refereeB, false);/////////////////////////////////////////////////////////
            games.clear();
            games.addAll(temp);
        }
        return games;
    }
}

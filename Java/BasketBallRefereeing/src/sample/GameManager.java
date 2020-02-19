package sample;

import java.util.ArrayList;
import java.util.Date;

public class GameManager {

    private ArrayList<Game> gamesList;
    private Team gameCreation_homeTeamSelected;
    private Referee gameCreation_refereeASelected;

    public GameManager() {
        this.gamesList = new ArrayList<>();
    }

    private Game createGameObject(Date day, Gym gym, Referee refereeA, Referee refereeB, Team homeTeam, Team awayTeam) {
        return new Game(day, gym, refereeA, refereeB, homeTeam, awayTeam);
    }

    public Game createNewGame(Date day, Gym gym, Referee refereeA, Referee refereeB, Team homeTeam, Team awayTeam) {
        Game g = createGameObject(day, gym, refereeA, refereeB, homeTeam, awayTeam);
        this.gamesList.add(g);
        return g;
    }

    public void gameCreation_setHomeTeamSelected(Team t) {
        this.gameCreation_homeTeamSelected = t;
    }

    public Team getGameCreation_homeTeamSelected() {
        return this.gameCreation_homeTeamSelected;
    }

    public void gameCreation_setRefereeASelected(Referee referee) {
        this.gameCreation_refereeASelected = referee;
    }

    public Referee gameCreation_getRefereeASelected() {
        return this.gameCreation_refereeASelected;
    }

    public String toString() {
        StringBuilder res = new StringBuilder();
        for (Game g : gamesList) {
            res.append("\n").append(g).append("\n");
        }
        return "\n" + res;
    }
}

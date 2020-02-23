package sample;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;

public class GameManager {

    private ArrayList<Game> gamesList;
    private Team gameCreation_homeTeamSelected;
    private Referee gameCreation_refereeASelected;

    public GameManager() {
        this.gamesList = new ArrayList<>();
    }

    public ArrayList<Game> getGames() {
        return this.gamesList;
    }

    public Game createGameObject(Date day, Gym gym, Referee refereeA, Referee refereeB, Team homeTeam, Team awayTeam) {
        return new Game(day, gym, refereeA, refereeB, homeTeam, awayTeam);
    }

    public Game createNewGame(Date day, Gym gym, Referee refereeA, Referee refereeB, Team homeTeam, Team awayTeam) {
        Game g = createGameObject(day, gym, refereeA, refereeB, homeTeam, awayTeam);
        this.gamesList.add(g);
        return g;
    }

    public void addGameObject(Game game) {
        this.gamesList.add(game);
    }

    public void addGameObjectsArrayList(ArrayList<Game> games) {
        this.gamesList.addAll(games);
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

    public ArrayList<Game> filterGamesForDate(ArrayList<Game> arr, Date day) {
        if (arr == null) {
            arr = new ArrayList<>(gamesList);
        }
        ArrayList<Game> res = newArrayList();
        for (Game g : arr) {
            if (Utilities.sameDay(g.getDate(), day)) {
                res.add(g);
            }
        }
        return res;
    }

    /**
     * Returns a copy of the parameterized ArrayList filtered
     * by the hour +/- the window gap.
     * @param arr     - arr to filter, possibly null.
     * @param day     - day set to hour for searching.
     * @param window  - (0 <= x <= 1).
     * @param isHours - true for hours, false for minutes
     * @return new ArrayList of filtered games.
     */
    public ArrayList<Game> filterGamesForTime(ArrayList<Game> arr, Date day, double window, boolean isHours) {
        if (arr == null) {
            arr = new ArrayList<>(gamesList);
        }
        ArrayList<Game> res = newArrayList();
        for (Game g : arr) {
            if (Utilities.sameTime(day, g.getDate(), window, isHours)) {
                res.add(g);
            }
        }
        return res;
    }

    public ArrayList<Game> filterGamesForGym(ArrayList<Game> arr, Gym gym){
        if (arr == null) {
            arr = new ArrayList<>(gamesList);
        }
        ArrayList<Game> res = newArrayList();
        for (Game g : arr) {
            if (g.getGym() == gym) {
                res.add(g);
            }
        }
        return res;
    }

    public ArrayList<Game> filterGamesForTeam(ArrayList<Game> arr, Team team, boolean andHome) {
        if (arr == null) {
            arr = new ArrayList<>(gamesList);
        }
        ArrayList<Game> res = newArrayList();
        for (Game g : arr) {
            Team home = g.getHomeTeam();
            Team away = g.getAwayTeam();
            if (andHome) {
                if (home != team) {
                    // not the home team
                    continue;
                }
            }
            if (team == home || team == away) {
                res.add(g);
            }
        }
        return res;
    }

    public ArrayList<Game> filterGamesForTeams(ArrayList<Game> arr, Team teamA, Team teamB, boolean andHome) {
        if (arr == null) {
            arr = new ArrayList<>(gamesList);
        }
        ArrayList<Game> res = newArrayList();
        for (Game g : arr) {
            Team home = g.getHomeTeam();
            Team away = g.getAwayTeam();
            if (andHome) {
                if (home != teamA || away != teamB) {
                    // andHome doesn't match
                    continue;
                }
            }
            if (teamA == home && teamB == away) {
                res.add(g);
            }
        }
        return res;
    }

    public ArrayList<Game> filterGamesForReferee(ArrayList<Game> arr, Referee referee, boolean andDriver) {
        if (arr == null) {
            arr = new ArrayList<>(gamesList);
        }
        ArrayList<Game> res = newArrayList();
        for (Game g : arr) {
            Referee a = g.getRefereeA();
            Referee b = g.getRefereeB();
            if (andDriver) {
                if (a != referee) {
                    // not the driver
                    continue;
                }
            }
            if (referee == a || referee == b) {
                res.add(g);
            }
        }
        return res;
    }

    public ArrayList<Game> filterGamesForReferees(ArrayList<Game> arr, Referee refereeA, Referee refereeB, boolean andDriver) {
        if (arr == null) {
            arr = new ArrayList<>(gamesList);
        }
        ArrayList<Game> res = newArrayList();
        for (Game g : arr) {
            Referee a = g.getRefereeA();
            Referee b = g.getRefereeB();
            if (andDriver) {
                if (refereeA != a || refereeB != b) {
                    // andDriver doesn't match
                    continue;
                }
            }
            if (refereeA == a && refereeB == b) {
                res.add(g);
            }
        }
        return res;
    }

    private ArrayList<Game> newArrayList() {
        return new ArrayList<>();
    }

    public String toString() {
        StringBuilder res = new StringBuilder();
        for (Game g : gamesList) {
            res.append("\n").append(g).append("\n");
        }
        return "\n" + res;
    }
}

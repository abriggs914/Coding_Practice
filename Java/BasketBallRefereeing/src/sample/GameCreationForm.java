package sample;

import java.util.Date;

public class GameCreationForm {

    private Date day;
    private Team homeTeam;
    private Team awayTeam;
    private Gym gym;
    private Referee refereeA;
    private Referee refereeB;

    GameCreationForm() {

    }

    public void collectAttributes() {
        this.day = Controller.gameCreation_getDate();
        this.homeTeam = Controller.gameCreation_getHomeTeam();
        this.awayTeam = Controller.gameCreation_getAwayTeam();
        this.gym = Controller.gameCreation_getGym();
        this.refereeA = Controller.gameCreation_getRefereeA();
        this.refereeB = Controller.gameCreation_getRefereeB();
    }

    public Game createGame() {
        return Main.gameManager.createNewGame(
                getDay(), getGym(), getRefereeA(), getRefereeB(), getHomeTeam(), getAwayTeam()
        );
    }

    public Date getDay() {
        return this.day;
    }

    public Team getHomeTeam() {
        return this.homeTeam;
    }

    public Team getAwayTeam() {
        return this.awayTeam;
    }

    public Gym getGym() {
        return this.gym;
    }

    public Referee getRefereeA() {
        return this.refereeA;
    }

    public Referee getRefereeB() {
        return this.refereeB;
    }

    public boolean checkValid() {
        if (this.day != null) {
            if (this.gym != null) {
                if (this.homeTeam != null) {
                    if (this.awayTeam != null) {
                        if (this.refereeA != null) {
                            if (this.refereeB != null) {
                                // logic checks
                                if (this.homeTeam != this.awayTeam) {
                                    if (this.refereeA != this.refereeB) {
                                        return true;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        return false;
    }
}

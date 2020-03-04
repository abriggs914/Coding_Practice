package sample;

import java.util.Date;

public class Game {

    private Date date;
    private Gym gym;
    private Referee refereeA, refereeB;
    private Team homeTeam, awayTeam;

    public Game(Date day, Gym gym, Referee refereeA, Referee refereeB, Team homeTeam, Team awayTeam) {
        this.date = day;
        this.gym = gym;
        this.refereeA = refereeA;
        this.refereeB = refereeB;
        this.homeTeam = homeTeam;
        this.awayTeam = awayTeam;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public Gym getGym() {
        return gym;
    }

    public void setGym(Gym gym) {
        this.gym = gym;
    }

    public Referee getRefereeA() {
        return refereeA;
    }

    public void setRefereeA(Referee refereeA) {
        this.refereeA = refereeA;
    }

    public Referee getRefereeB() {
        return refereeB;
    }

    public void setRefereeB(Referee refereeB) {
        this.refereeB = refereeB;
    }

    public Team getHomeTeam() {
        return homeTeam;
    }

    public void setHomeTeam(Team homeTeam) {
        this.homeTeam = homeTeam;
    }

    public Team getAwayTeam() {
        return awayTeam;
    }

    public void setAwayTeam(Team awayTeam) {
        this.awayTeam = awayTeam;
    }

    public String getFormattedDateString() {
        return Utilities.getDateString(date) + ", " + Utilities.getTimeString(date);
    }

    public String getFormattedGameString() {
        String border = "#######################################################################################";
        return border + "\n\t" + awayTeam + "\tVS.\t" + homeTeam
                + "\n\t\t@\t" + gym + ", \t" + getFormattedDateString() + "\n\tRefereed by:\t"
                + refereeA + "\n\t\t\t\t" + refereeB + "\n" + border + "\n";
    }

    public String toString() {
        return "\n" + awayTeam + "\t@\t" + homeTeam + " {" + getFormattedDateString() + "}\nAT: " + gym + ", A: " + refereeA + ", B: " + refereeB;
    }
}

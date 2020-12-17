package sample.Version_4;

public class Angle {

    private String name;
    private double angle;

    public Angle(String name, double num) {
        this.name = name;
        this.angle = num;
    }

    public boolean known() {
        return this.angle != 0;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getAngle() {
        return angle;
    }

    public void setAngle(double angle) {
        this.angle = angle;
    }

    public String toString() {
        return "<Angle " + ", <" + this.angle + " degrees>>";
    }
}

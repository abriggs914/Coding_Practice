package sample;

public class Angle_v3 {

    public String name;
    public double angle;
    public sample.Side_v3 a;
    public sample.Side_v3 b;

    public Angle_v3(String name, double num) {
        this.name = name;
        this.angle = num;
    }

    public Angle_v3(String name, sample.Side_v3 a, sample.Side_v3 b, double num) {
        this.name = name;
        this.a = a;
        this.b = b;
        this.angle = num;
    }

    public boolean known() {
        return this.angle != 0;
    }

    public String toString() {
        return "<Angle " + this.name + ", a: " + this.a + ", b: " + this.b + ", d: " + this.angle + ">";
    }
}

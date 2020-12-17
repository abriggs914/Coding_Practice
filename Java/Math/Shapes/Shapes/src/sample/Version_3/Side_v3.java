package sample;

public class Side_v3 {

    public String name;
    public double length;

    public Side_v3(String name, double num) {
        this.name = name;
        this.length = num;
    }

    public boolean known() {
        return this.length != 0;
    }

    public String toString() {
        return "<Edge " + this.name + ", l: " + this.length + ">";
    }
}
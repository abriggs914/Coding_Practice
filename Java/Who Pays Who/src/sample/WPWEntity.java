package sample;

public class WPWEntity {

    private String name;
    private double balance;

    public WPWEntity(String nameIn) {
        System.out.println("A name: " + nameIn);
        new WPWEntity(nameIn, 0);
    }

    public WPWEntity(String nameIn, double balance) {
        System.out.println("B name: " + nameIn);
        this.name = nameIn;
        System.out.println("C name: " + this.name);
        this.balance = balance;
    }

    public String getName() {
        return this.name;
    }

    public double getBalance() {
        return this.balance;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }

    public String toString(){
        return "<Entity n: {" + name + "}, b: {" + balance + "}";
    }

    public static void main(String[] args) {
	    // write your code here
    }
}

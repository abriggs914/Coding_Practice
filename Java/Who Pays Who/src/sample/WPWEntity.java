package sample;
import java.util.ArrayList;

public class WPWEntity {

    public final static WPWEntity POT = new WPWEntity("Pot");

    private String name;
    private double balance;
    private ArrayList<Double> balanceHistory;

    public WPWEntity(String nameIn) {
        this.init(nameIn, 0.0);
    }

    public WPWEntity(String nameIn, double balance) {
        this.init(nameIn, balance);
    }

    private void init(String nameIn, double balanceIn) {
        this.name = nameIn;
        this.balance = balanceIn;
        this.balanceHistory = new ArrayList<>();
        this.balanceHistory.add(this.balance);
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

    public void addFromBalance(double amount) {
        this.setBalance(balance - amount);
    }

    public void addToBalance(double amount) {
        this.setBalance(balance + amount);
    }

    @Override
    public String toString(){
        return "<Entity n: {" + name + "}, b: {" + balance + "}";
    }

    public static void main(String[] args) {
	    // write your code here
    }
}

package com.company;

public class WPWEntity {

    String name;
    double balance;

    public WPWEntity(String name) {
        new WPWEntity(name, 0);
    }

    public WPWEntity(String name, double balance) {
        this.name = name;
        this.balance = balance;
    }

    public String toString(){
        return "<Entity n: %s b: %s".format(this.name, this.balance);
    }

    public static void main(String[] args) {
	    // write your code here
    }
}

// Best Fare Calculator
// Overview
// This project is slightly different than others you have encountered thus far on Codecademy. Instead of a step-by-step tutorial, this project contains a series of open-ended requirements which describe the project you’ll be building. There are many possible ways to correctly fulfill all of these requirements, and you should expect to use the internet, Codecademy, and other resources when you encounter a problem that you cannot easily solve.

// Project Goals
// If you’ve ever wondered if you chose the right fare option for riding the metro or bus, you’re not alone. In this project you will write a Java program that determines the best fare option for someone visiting New York City who plans to use the NYC transit system. The program should use constructors, methods, conditionals, loops, and arrays.

// Tasks
// 9/9Complete
// Mark the tasks as complete by checking them off
// Prerequisites
// 1.
// In order to complete this project, you should be familiar with Java classes and objects, methods, conditionals and control flow, loops, and arrays. Ideally, you’ve finished the first six sections of Learn Java (through Loops).

// Project Requirements
// 2.
// Start by building a TransitCalculator class in TransitCalculator.java. The class should include

// A main() method to run the code.
// A field to keep track of the number of days a person will be using the transit system (up to 30 days).
// A field to keep track of the number of individual rides the person expects to take in that time.
// 3.
// Build a class constructor for TransitCalculator that accepts the number of days and rides and sets the values for the corresponding fields.

// 4.
// The NYC transit system has three regular fare options:

// Pay-per-ride (single ride): $2.75
// 7-day Unlimited Rides: $33.00
// 30-day Unlimited Rides: $127.00
// Add variables or arrays to the class to keep track of these values.

// You can split up the values so that you have two arrays:

// one String array to hold the three options ("Pay-per-ride", etc.)
// one double array to hold the three prices (2.75, etc.)
// 5.
// Create a method unlimited7Price() with a double return type. The method should return the overall price per ride of using the 7-day Unlimited option.

// 20 rides over 19 days should return 4.95
// 50 rides over 22 days should return 2.64
// 14 rides over 6 days should return either 2.357142857142857 or 2.36
// Make sure to account for all days the person might be riding public transit in NYC. For example, if a person plans to use the train or bus over the course of 15 days, then three 7-day Unlimited purchases would be required.

// First you need to find out the number of weeks the card would be necessary for. There are a few ways of accomplishing this. You can use Math.ceil() or the % operator to round up when there are partial weeks.

// Next, you’ll need to determine the total cost of the 7-day Unlimited fare option. This should be the number of weeks calculated multiplied by the 7-day Unlimited fare.

// The return value can be calculated as the total cost of the 7-day Unlimited fare option divided by the total number of rides.

// 6.
// Build a method getRidePrices() that will return an array of doubles. Inside the method, you’ll need to calculate the price per ride for each fare option. You should use the unlimited7Price() method to determine this value for the 7-day Unlimited option.

// The method should return an array of the price per ride for the three fare options.

// Remember that the method’s return type should match its return value.

// You already have the Pay-per-ride option calculated. You can calculate the 30-day Unlimited option by dividing the fare by the total number of rides.

// 7.
// Create a String method called getBestFare().

// Inside the method, you should use the array of ride prices calculated with getRidePrices() and at least one loop to determine:

// the lowest price
// the best (corresponding) fare method
// At the end of the method, you should return a String that communicates the findings.

// For example, for 54 rides over the course of 26 days, the method should return the following text:

// You should get the 30-day Unlimited option at $2.35 per ride.
// For 12 rides over the course of 5 days, the method should return:

// You should get the Pay-per-ride option at $2.75 per ride.
// One way to do this is to loop over the array of ride prices while keeping track of the current index and the lowest fare index. Inside the loop, you can check if the ride price at the current index is less than the lowest fare index. If it is, then you should reset the lowest fare index.

// If you originally set up the fare options in an array, its indices should correspond to the new ride prices array, which means you can do something like this for your return statement:

// return "You should get the " + fareOptions[winningIndex] + " option at $" + ridePrices[winningIndex] + " per ride.";
// If you want to round the price to two decimals, you can use Math.round() like this:

// Math.round(price * 100.0) / 100.0
// Project Extensions & Solution
// 8.
// Nice work! If you’d like to see the solution, move to the next task. If you’d like to extend your project on your own, you could consider the following:

// The NYC transit system also offers reduced fare options for people with disabilities and people who are at least 65 years old. Refactor the TransitCalculator class so that it checks if the rider qualifies for reduced fare and calculates the best reduced fare option if they do.
// Pay-per-ride (single ride): $1.35
// 7-day Unlimited Rides: $16.50
// 30-day Unlimited Rides: $63.50
// NYC isn’t the only city where there are several fare options available! Extend your TransitCalculator to work for a different city. Pick your own, or choose from these below:
// Vancouver
// Mexico City
// Delhi
// Berlin
// Paris
// Seoul
// 9.
// Compare your project to our solution code. Your solution might not look exactly like ours, and that’s okay! The most important thing right now is to get your code working as it should (you can always refactor more later).

import java.lang.Math;
import java.util.Arrays;
public class TransitCalculator {
  
  int numDays;
  int rides;
  
  String[] rideTypes = {"Pay-per-ride (single ride)",
                        "7-day Unlimited Rides",
                        "30-day Unlimited Rides"};
  double[] prices = {2.75, 33.0, 127.0};
  
  public TransitCalculator(int days, int rides) {
    this.numDays = days;
    this.rides = rides;
  }
  
  public double payPerRidePrice() {
    return prices[0];
  }
  
  public double unlimited7Price() {
    int numPasses = (int) Math.ceil(this.numDays / 7.0);
    return (numPasses * prices[1]) / this.rides;
  }
  
  public double unlimited30Price() {
    int numPasses = (int) Math.ceil(this.numDays / 30.0);
    return (numPasses * prices[2]) / this.rides;
  }
  
  public double[] getRidePrices() {
    double[] pricesPerRideType = new double[prices.length];
    pricesPerRideType[0] = payPerRidePrice();
    pricesPerRideType[1] = unlimited7Price();
    pricesPerRideType[2] = unlimited30Price();
    return pricesPerRideType;
  }
  
  public String getBestFare() {
    int index = -1;
    double lowestPrice = Integer.MAX_VALUE;
    double[] pricesList = this.getRidePrices();
    for (int i = 0; i < pricesList.length; i++) {
      if (pricesList[i] < lowestPrice) {
        lowestPrice = pricesList[i];
        index = i;
      }
    }    
    String result = "You should get the " + rideTypes[index] + " option at $" + pricesList[index] + " per ride.";
    return result;
  }
  
  public static void main(String[] args) {
    int nd = 19;
    int nr = 20;
    TransitCalculator tc = new TransitCalculator(nd, nr);
    double[] prices = tc.getRidePrices();
    System.out.println(Arrays.toString(prices));
    System.out.println(tc.getBestFare());
  }
}
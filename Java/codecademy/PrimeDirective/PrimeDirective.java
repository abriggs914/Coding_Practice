// LEARN JAVA
// The Prime Directive
// Finding prime numbers is a common technical challenge in programming interviews.

// As it happens, Java loops are a great tool to help you do this!

// A prime number is an integer greater than 1 that is only divisible by 1 and itself.

// For example, 2, 3, 5, and 7 are all prime numbers, but 4, 6, 8, and 9 are not.

// Your prime directive: Build a PrimeDirective.java program that creates an ArrayList of all prime numbers in an array.

// Tasks
// 15/15Complete
// Mark the tasks as complete by checking them off
// Setting Up
// 1.
// Take a look at PrimeDirective.java:

// There’s a class PrimeDirective where you’ll be creating your program.

// Inside main(), an instance of PrimeDirective (pd) has been instantiated. Below that, you’ll see an int array called numbers that has a series of integers.

// To Do: Import ArrayList from java.util at the very top of your program, above the PrimeDirective class. This will allow you to use ArrayLists.

// This line should be at the top of the file:

// import java.util.ArrayList;
// Optimus Prime
// 2.
// First, we need a way to determine whether a number is prime or isn’t prime.

// Create an empty public method isPrime() that:

// has one parameter: an int called number
// will return true if number is prime
// will return false if number is not prime
// A method that returns true and false should have a boolean return type.

// public boolean isPrime(int number) {

//   // method body goes here

// }
// 3.
// Take a moment to consider what makes a prime number prime:

// greater than 1
// only divisible by 1 and itself
// In fact, every number is divisible by 1, so we don’t really care about being able to divide by 1.

// Imagine we have a number n. If n is prime, then n should not be divisible by any integers between 2 and n-1.

// But how can we check this?

// Before you move on, take out paper and a pencil and write down your ideas about how to check if a number is prime.

// If you smell a for loop or the % operator coming, you’re onto something…

// 4.
// Inside isPrime(), create a for loop:

// set a counter i equal to 2
// run the loop while i is less than number
// increment i
// for (int i = 2; i < number; i++) {

//   // check divisibility here

// }
// 5.
// As you loop through each i value, you want to check if number is divisible by it.

// Inside the loop:

// Check if number is divisible by i.
// If it is, then number is not prime, so you can return false from the method.
// To check if age is divisible by 4, you could use modulo (%) like this:

// if (age % 4 == 0) {

//   // stuff happens

// }
// The if statement should look like this now:

// if (number % i == 0) {

//   return false;

// }
// 6.
// Below the for loop, return true because number isn’t divisible by any two smaller integers.

// 7.
// Wait a second… what about 2 or numbers less than 2? Well, those are our edge cases.

// In isPrime() above the for loop, build an if/else if statement to handle the following edge cases:

// If number is 2, it is the smallest prime number.
// If number is less than 2, it is not prime.
// Your edge case handling should look something like this:

// if (number == 2) {
//   return true;
// } else if (number < 2) {
//   return false;
// }
// 8.
// Test out your isPrime() method on pd in main() and see if it works!

// Try it out with a few numbers:

// 7 should return true
// 28 should return false
// 2 should return true
// 0 should return false
// Don’t forget to run your code with the following:

// java PrimeDirective
// You can check if isPrime() is working as expected like this:

// System.out.println(pd.isPrime(6));
// // should print false
// If nothing happens, you may have a typo somewhere in your code — try compiling:

// javac PrimeDirective.java
// Only Primes
// 9.
// Nice work! Now, all that’s left is building an ArrayList of the prime numbers in the numbers array.

// You can create another method to handle this. Build an empty method called onlyPrimes() that:

// returns an ArrayList of integers
// has a parameter numbers, which is an array of ints
// .onlyPrimes() should look like this so far:

// public ArrayList<Integer> onlyPrimes(int[] numbers) {

//   // method body goes here

// }
// 10.
// Inside the onlyPrimes() body, create a new empty ArrayList called primes to store all the prime numbers that are found.

// ArrayList<Integer> primes = new ArrayList<Integer>();
// 11.
// So how do you find all of the primes in an array? Why using a for-each loop!

// Set up a for-each loop that checks each number in numbers.

// For-each loops look like:

// for (String animal : animals) {

//   // do something with animal

// }
// In this case, the loop should look like:

// for (int number : numbers) {

//   // loop body

// }
// 12.
// Now, if number is prime, you can add it to primes.

// Because .isPrime() is another public method in PrimeDirective, you can access it inside onlyPrimes() to check if number is prime:

// isPrime(number)
// // returns true or false
// To add something to an ArrayList called cats:

// cats.add("Captain McNugget");
// 13.
// At the end of the method below the for-each loop, return primes from onlyPrimes().

// The method should look something like this:

// public ArrayList<Integer> onlyPrimes(int[] numbers) {
//   ArrayList<Integer> primes = new ArrayList<Integer>();

//   for (int number : numbers) {
//     if (isPrime(number)) {
//       primes.add(number);
//     }
//   }

//   return primes;
// }
// 14.
// Time to put it all together!

// In main(), test out pd.onlyPrimes() on the numbers array.

// Don’t forget to run your code with

// java PrimeDirective
// You can check if onlyPrimes() is working as expected like this:

// System.out.println(pd.onlyPrimes(numbers));
// // should print [29, 11, 101, 43, 89]
// If nothing happens, you may have a typo somewhere in your code — try compiling:

// javac PrimeDirective.java
// Primed For More
// 15.
// Congrats on completing the Prime Directive!

// Want to do even more? Check the hint for some ideas to expand the project.

// Build a method that filters an array for odd or even numbers (bonus points if it can do either depending on arguments passed in!).
// Build a method that returns an ArrayList of the first n primes in an array.
// Build a method that returns an ArrayList of the first n Fibonacci numbers.

// Import statement:
import java.util.ArrayList;

public class PrimeDirective {
  
  // Add your methods here:
  public static boolean isPrime(int number) {
    int count = 2;
    while (count <= number) {
      boolean isPrime = true;
      for (int i = 2; i < ((int) Math.sqrt(count) + 1); i++) {
        if (count % i == 0) {
          isPrime = false;
          break;
        }
      }
      // System.out.println("\nnumber:\t" + number + "\tcount:\t" + count + "\tisPrime\t" + isPrime + "\n");
      if (isPrime) {
        if (count == number) {
          return true;
        }
      }
      count += 1;
    }
    return false;
  }
  
  public ArrayList<Integer> onlyPrimes(int[] number) {
    ArrayList<Integer> arr = new ArrayList<Integer>();
    for (int n : number) {
      if (isPrime(n)) {
        arr.add(n);
      }
    }
    return arr;
  }
  
  public static void main(String[] args) {

    PrimeDirective pd = new PrimeDirective();
    int[] numbers = {0,6, 29, 28, 33, 11, 100, 101, 43, 89};
    // for (int n : numbers) {
    //   System.out.println("n:\t" + n + "\tprime:\t" + isPrime(n));
    // }
    ArrayList<Integer> arr = pd.onlyPrimes(numbers); 
    System.out.println(arr);
  }  

}
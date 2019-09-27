// 1.12 Reversing
// 1 out of 1 step passed
// 1 out of 1 point  received
// Adaptive mode activated
// Write a program that reads a three digit number, calculates the new number by reversing its digits, and outputs a new number.

// Sample Input:
/*
682
*/
// Sample Output:
/*
286
*/

import java.util.Scanner;

class Reversing {
    public static Scanner sc = new Scanner(System.in);
    
    public static int readInt() {
        return sc.nextInt();
    }  
    
    public static String readLine() {
        return sc.nextLine();
    }
    
    public static int reverseNum(int num) {
        String n = Integer.toString(num);
        String reverseNum = "";
        for (int i = n.length() - 1; i >= 0; i--) {
            reverseNum += n.charAt(i);
        }
        return Integer.parseInt(reverseNum);
    }
    
	public static void main (String[] args) {
		int num = readInt();
		System.out.println(reverseNum(num));
	}
}
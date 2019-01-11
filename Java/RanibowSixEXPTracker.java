/*package whatever //do not write package name here 
*
*	Java Program that determines how much xp it takes between
*	levels in R6S. Also the number of minimum games and maximum
*	score achieved (3-0 Casual Win and 5000 EXP earned).
*	Aug 2018
*
*/

import java.io.*;

class GFG {
	public static void main (String[] args) {
		System.out.println("GfG!");
		int inBetween = 5000, sum = 0, b = 1, time = 0;
		final int EXPCAP = 5000;
		final int MINGAMETIME = 1050;
		for(int i = 0; i < 350; i++){
		    System.out.println("\nsum: " + sum + ", i(level): " + i + ", inBetween: " + inBetween);
		    sum += inBetween;
		    inBetween += 500;
		    if(i > 0){
		        int k = 0;
    		    for(int j = 0; j < inBetween; j += EXPCAP){
    		        k++;
    		    }
    		    b += k;
    		    time += k * MINGAMETIME;
    		    System.out.println("minimum # of games to level up: " + k + ", Total games: " + b + ", time: " + time);
		    }
		}
	}
}
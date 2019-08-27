/*package whatever //do not write package name here */

import java.io.*;
import java.util.Random;
import java.lang.Math;

class r6s_loot_roll_simulator {
    
    final static double RANKED_WIN_CHANCE = 3.0;
    final static double RANKED_LOSS_CHANCE = 2.5;
    final static double CASUAL_WIN_CHANCE = 2.0;
    final static double CASUAL_LOSS_CHANCE = 1.5;
    final static double VIP_BONUS = 0.3;
    
    static int num_alpha_packs = 0;
    static int num_rolls = 0;
    static int num_games = 0;
    static int num_wins = 0;
    static int num_losses = 0;
    
    public static double roll(double curr_percent, boolean ranked, boolean vip) {
        num_rolls += 1;
        Random rand = new Random();
        int rand_num = rand.nextInt(100);
        System.out.println("RAND_NUM:\t" + rand_num); // + ", chance = " + curr_percent);
        if (rand_num <= (int) Math.round(curr_percent)) {
            num_alpha_packs += 1;
            System.out.println("YOU WON A PACK AT " + curr_percent + " %");
            if (ranked) {
                curr_percent = RANKED_WIN_CHANCE;
            }
            else {
                curr_percent = CASUAL_WIN_CHANCE;
            }
        }
        else {
            if (ranked) {
                curr_percent += RANKED_WIN_CHANCE;
            }
            else {
                curr_percent += CASUAL_WIN_CHANCE;
            }
        }
        if (vip) {
            curr_percent += VIP_BONUS;
        }
        // System.out.println("NEW chance = " + curr_percent);
        return curr_percent;
	}
	
	public static void main (String[] args) {
		boolean ranked_game = true;
		boolean vip = true;
		int num_desired_packs = 1;
		double chance = 0.0;
		
		if (ranked_game) {
		    chance = RANKED_WIN_CHANCE;
		}
		else {
		    chance = CASUAL_WIN_CHANCE;
		}
		if (vip) {
		    chance += VIP_BONUS;
		}
		
// 		double new_chance = 
		while (num_alpha_packs < num_desired_packs) {
		    Random rand = new Random();
		    int win = rand.nextInt(2);
		    num_games += 1;
			System.out.println("percent chance = " + chance + " %");
		    if (win == 0) {
		        System.out.println("\tYOU WIN GAME # " + num_games);
		        chance = roll(chance, ranked_game, vip);
		    }
		    else {
		        System.out.println("\tYOU LOSE GAME # " + num_games);
		        if (vip) {
		            chance += VIP_BONUS;
		        }
		        if (ranked_game) {
		            chance += RANKED_LOSS_CHANCE;
		        }
		        else {
		            chance += CASUAL_LOSS_CHANCE;
		        }
		    }
		  //  System.out.println("new_chance:\t" + new_chance);
		}
	}
}
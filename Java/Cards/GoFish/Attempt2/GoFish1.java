/*
*	Go Fish attempt 1
*	Aug 2018
*
*/

import java.util.Scanner;
import java.util.Random;

public class GoFish1 extends Exception{

	public static int playerWins = 0, playerPairs = 0;
	public static int aiWins = 0, aiPairs = 0;
	public static int whoWentFirst = 0, round = 1, handsize = 0;		// 0 == player, 1 == ai;
	public static Scanner scan = new Scanner(System.in);
	public static Reminder timer = new Reminder(1);
	public static Card[] playerPairsArr = new Card[26];
	public static Card[] aiPairsArr = new Card[26];
	public static Card takenCard = new Card(100, 100, "TAKEN");
	
	public static void main(String[] args){
		//timer.wait(2);
		System.out.println("\tWelcome to Go Fish!\n\tLet's see who goes first:");
		//timer.wait(3);
		whoWentFirst = whoGoesFirst();
		if(whoWentFirst == 0){
			System.out.println("\n\n\tYou get to go first!");
			System.out.println("\n\tSince you won the coin flip you may chose\n\thow many cards you would like to start with");
			try{
				handsize = scan.nextInt();
				if(handsize > 20 || handsize < 1){
					throw new OutOfBoundsException();
				}
				//timer.wait(1);
				System.out.println("\thandsize has been set to: " + handsize);
			}
			catch(Exception e){
				//timer.wait(1);
				System.out.println("\n\n\tError, handsize set to 5.");
				handsize = 5;
			}
		}
		else{
			//timer.wait(1);
			System.out.println("\n\n\tThe AI gets to go first.");
			System.out.println("\n\tThe handsize has been set to 5.");
			handsize = 5;
		}
		System.out.println("\n\n\tLet the game begin!\n\n");
		//timer.wait(5);
		takenCard.populateTakenCards(playerPairsArr);
		takenCard.populateTakenCards(aiPairsArr);
		Deck deck1 = new Deck();
		//deck1.shuffle(deck1);
		System.out.println("\n\n\tYour Hand.");
		//timer.wait(2);
		Hand playerHandOBJ = deck1.handGeneratorGameVersion(deck1, handsize);
		Card[] playerHand = playerHandOBJ.myHand;
		
		//timer.wait(2);
		
		Hand aiHandOBJ = deck1.handGeneratorGameVersionAI(deck1, handsize);
		Card[] aiHand = aiHandOBJ.myHand;
		
		int h = playerHandOBJ.detectPairs(playerHandOBJ, deck1);
		System.out.println("Pairs detected: " + h);
		playerPairs += h;
		playerHandOBJ.printHand(playerHandOBJ);
	}
	
	public static int whoGoesFirst(){
		Random rand = new Random();
		int res = 5;
		while(res != 0 && res != 1){
			res = rand.nextInt(2);
		}
		return res;
	}
}
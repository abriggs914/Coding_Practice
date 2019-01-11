/*
*	Go Fish attempt 1
*	Aug 2018
*
*/

import java.util.Scanner;
import java.util.Random;

public class GoFish1G extends Exception{

	/*
	*
	*/
	public static int playerWins = 0, playerPairs = 0;
	/*
	*
	*/
	public static int aiWins = 0, aiPairs = 0;
	/*
	*
	*/
	public static int whoWentFirst = 0, round = 1, handsize = 0, cardsLeftInPlay = 52;		// 0 == player, 1 == ai;
	/*
	*
	*/
	public static Scanner scan = new Scanner(System.in);
	/*
	*
	*/
	public static Reminder timer = new Reminder(1);
	/*
	*
	*/
	public static CardG[] playerPairsArr = new CardG[26];
	/*
	*
	*/
	public static CardG[] aiPairsArr = new CardG[26];
	/*
	*
	*/
	public static CardG takenCard = new CardG(100, 100, "TAKEN", -1);
	
	/*
	*
	*/
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
					throw new OutOfBoundsExceptionG();
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
		cardsLeftInPlay -= (2*handsize);
		System.out.println("\n\n\tLet the game begin!\n\n");
		//timer.wait(5);
		DeckG deck1 = new DeckG();
		takenCard.populateTakenCards(playerPairsArr, deck1);
		takenCard.populateTakenCards(aiPairsArr, deck1);
		//deck1.shuffle(deck1);
		//timer.wait(2);
		HandG playerHandOBJ = deck1.handGeneratorGameVersion(deck1, handsize);
		CardG[] playerHand = playerHandOBJ.myHand;
		
		//timer.wait(2);
		
		HandG aiHandOBJ = deck1.handGeneratorGameVersionAI(deck1, handsize);
		CardG[] aiHand = aiHandOBJ.myHand;
		aiHandOBJ.printHand(aiHandOBJ);
		/*System.out.println("\n\n\tPrinting Deck\n");
		deck1.printDeck();
		System.out.println("\n\n\tDone Printing Deck\n\n");*/
		
		System.out.println("\tDetecting Pairs in Your Hand.");
		//timer.wait(2);
		playerPairs = playerHandOBJ.detectPairs(playerHandOBJ, deck1);
		System.out.println("\tDetecting Pairs in AI's Hand.");
		//timer.wait(2);
		aiPairs = aiHandOBJ.detectPairsNoPrinting(aiHandOBJ, deck1);
		aiHandOBJ.printHand(aiHandOBJ);
		deck1.printDeck();
		
		playerHandOBJ.printHand(playerHandOBJ);
		playerHandOBJ.drawCard(deck1, playerHandOBJ, 'p');
		
		/*
		while((playerPairs*2 + aiPairs*2) < 52){
			System.out.println("\tRound: " + round + "\n\n");
			System.out.println("Player Pairs Detected: " + playerPairs);
			System.out.println("AI Pairs Detected: " + aiPairs);
			round++;
			playerPairs += 5;
		}*/
	}
	
	/*
	*	Method returns a number, deciding who will go
	*	first. 0 == player, 1 == ai.
	*/
	public static int whoGoesFirst(){
		Random rand = new Random();
		int res = 5;
		while(res != 0 && res != 1){
			res = rand.nextInt(2);
		}
		return res;
	}
}
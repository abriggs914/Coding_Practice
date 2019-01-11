/*
* Java program to act as a driver for the tic-tac-toe board game.
* works with GameBoard.java
* August 2018
*/

import java.util.Scanner;

public class GameDriver1{
	public static void main(String[] args){
		Scanner scan = new Scanner(System.in);
		int[] arr = {1,5,2,1,4,1,2,3};
		GameBoard gb1 = new GameBoard(arr, 0, 0);
		System.out.println("\n\n");
		int bestOf = gb1.startGame();
		int playerScore = 0, aIScore = 0, round = 1, game = 1;
		boolean playerIsX = gb1.playerChoice();
		if(bestOf > 25){
			System.out.println("Too big");
			return;
		}
		while((game-1) < bestOf){
			int[] newArr = {0,0,0,0,0,0,0,0,0};
			round = 1;
			System.out.println("\n\t\tNew Game: " + game + "\t\tRound: " + round + "\n\tScore: \n\t\tPlayer: " + playerScore + "\t\tComputer: " + aIScore);
			gb1 = new GameBoard(newArr, playerScore, aIScore);
			while(!gb1.checkWinner(newArr, playerIsX)){
				System.out.println("\t\t\tGame: " + game + ", Round: " + round);
				//user move
				newArr = gb1.getPlayerMoveBasic(newArr, playerIsX);
				gb1 = new GameBoard(newArr, playerScore, aIScore);
				//ai move
				/*if(round != 5){
					break;
				}*/
				newArr = gb1.simulateAIMoveBasic(newArr, playerIsX);
				gb1 = new GameBoard(newArr, playerScore, aIScore);
				round++;
				//break;
			}
			game++;
			playerScore = gb1.playerScore;
			aIScore = gb1.aiScore;
		}
	}
}
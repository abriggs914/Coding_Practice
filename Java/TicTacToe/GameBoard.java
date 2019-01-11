/*
* Java class that prints a tic-tac-toe board to
* the console.
* August 2018
*/

import java.util.Scanner;

public class GameBoard{
	
	public int playerScore = 0;
	public int aiScore = 0;
	
	/*
	* Method creates and prints a tic-tac-toe board
	* to the console window
	* 
	*/
	public GameBoard(int[] arrIn, int playerScore, int aiScore){
		playerScore = this.playerScore;
		aiScore = this.aiScore;
		System.out.println("\n\n");
		int x = 0;
		int y = howManyMoves(arrIn);
		int choicesLeft = 1;
		char[] arr = convertValues(arrIn);
		for(int j = 0; j < 10; j++){
			System.out.print("\t\t\t");
			if((j+1) % 3 == 0){
				for(int i = 0; i < 13; i++){
					if(i == 0 || i == 12 || i == 4 || i == 8){
						System.out.print("|");
					}
					else if(i == 2 || i == 6 || i == 10){
						if(x < y){
							System.out.print(arr[x]);
							x++;
						}
						else{
							System.out.print(choicesLeft);
							choicesLeft++;
						}
					}
					else{
						System.out.print(" ");
					}
				}
				System.out.print("\n");
			}
			else{
				if(j % 3 != 0){
					for(int i = 0; i < 13; i++){
						if(i == 0 || i == 12 || i == 4 || i == 8){
							System.out.print("|");
						}
						else{
							System.out.print(" ");
						}
					}
				}
				else if(j > 1){
					System.out.print("|___|___|___|");
				}
				else{
					System.out.print("_____________");
				}
				System.out.print("\n");
			}
		}
		System.out.println();
	}
	
	/*
	* Helper method to convert game array
	* to X's and O's.
	* 
	*/
	public char[] convertValues(int[] arr){
		char[] res = new char[arr.length];
		for(int i = 0; i < res.length; i++){
			if(arr[i] == 1){
				res[i] = 'X';
			}
			else if(arr[i] == 2){
				res[i] = 'O';
			}
			else{
				res[i] = ' ';
			}
		}
		return res;
	}
	
	/*
	* Method asks user for how many games they would like
	* to play the computer at a best of.
	* 
	*/
	public int startGame(){
		Scanner scan = new Scanner(System.in);
		System.out.println("Welcome to Tic-Tac-Toe!\nPlease enter the number of\ngames you would like to play.");
		int numGames = 0;
		try{
			numGames = scan.nextInt();
		}
		catch(Exception e){
			numGames = 1;
		}
		System.out.println("\t\tYou selected: " + numGames + "\n");
		return numGames;
	}
	
	/*
	* Method asks user which symbol they would like
	* to use during the game.
	* X == true, O == false, default: O
	*/
	public boolean playerChoice(){
		Scanner scan = new Scanner(System.in);
		System.out.println("Please enter 'X' or 'O'. ");
		boolean choice = false;
		String line = scan.nextLine();
		if(line.equals("X") || line.equals("x")){
			System.out.println("\t\tYou selected: X" + "\n");
			return true;
		}
		System.out.println("\t\tYou selected: O" + "\n");
		return choice;
	}
	
	/*
	* Method takes in the current game array and the player
	* choice of symbol, and decides if there is a winner on the
	* board as well as prints out a winning message for
	* the winner.
	*/
	public boolean checkWinner(int[] arr, boolean choice){
		int playerKey, comp1 = 0, comp2 = 0;
		int[] playerMoveIndices;
		int[] aiMoveIndices;
		boolean playerWinner = false, aiWinner = false;
		if(choice){
			playerKey = 1; // X
		}
		else{
			playerKey = 2; // O
		}
		int p = 0, x = 0, o = 0;
		for(int i = 0; i < 9; i++){
			if(arr[i] == 0){
				p++;
			}
			else if(arr[i] == 1){
				x++;
			}
			else{
				o++;
			}
		}
		if(p > 4 || x < 2 || o < 2){
			return false;
		}
		else{
			if(playerKey == 1){
				playerMoveIndices = new int[x];
				aiMoveIndices = new int[o];
			}
			else{
				playerMoveIndices = new int[o];
				aiMoveIndices = new int[x];
			}
			if(playerKey == 1){
				for(int i = 0; i < 9; i++){
					if(arr[i] == 1){
						playerMoveIndices[comp1] = i;
						comp1++;
					}
					else if(arr[i] == 2){
						aiMoveIndices[comp2] = i;
						comp2++;
					}
				}
				System.out.println("checking player ");
				playerWinner = checkIfWinner(playerMoveIndices);
			}
			else{
				for(int i = 0; i < 9; i++){
					if(arr[i] == 2){
						playerMoveIndices[comp1] = i;
						comp1++;
					}
					else if(arr[i] == 1){
						aiMoveIndices[comp2] = i;
						comp2++;
					}
				}
				System.out.println("checking ai");
				aiWinner = checkIfWinner(aiMoveIndices);
			}
		}
		if(playerWinner){
			System.out.println("Player Wins!!");
			playerScore++;
			return true;
		}
		else if(aiWinner){
			System.out.println("Computer Wins");
			aiScore++;
			return true;
		}
		else{
			return false;
		}
	}
	
	/*
	* Helper method for checkWinner(), takes in a small array of 
	* moves and decides if that player has won the game.
	* 
	*/
	public boolean checkIfWinner(int[] arr){
		int j = arr.length;
		for(int i = 0; i < j; i++){
			System.out.println(arr[i]);
		}
		boolean middle = false;
		boolean k = false, l = false, m = false, n = false, o = false, p = false, q = false, r = false, s = false;
		for(int i = 0; i < j; i++){
			if(arr[i] == 0){
				k = true;
			}
			else if(arr[i] == 1){
				l = true;
			}
			else if(arr[i] == 2){
				m = true;
			}
			else if(arr[i] == 3){
				n = true;
			}
			else if(arr[i] == 4){
				o = true;
			}
			else if(arr[i] == 5){
				p = true;
			}
			else if(arr[i] == 6){
				q = true;
			}
			else if(arr[i] == 7){
				r = true;
			}
			else if(arr[i] == 8){
				s = true;
			}
		}
		if((k && n && q) || (l && o && r) || (m && p && r) || (k && l && m) || (n && o && p) || (q && r && s) || (m && o && q) || (k && o && s)){
			return true;
		}
		else{
			return false;
		}
	}
	
	public int[] getPlayerMoveBasic(int[] arr, boolean choice){
		int playerSymbol = 8, aiSymbol = 8;
		int[] newArr = new int[arr.length];
		if(choice){
			playerSymbol = 1;
			aiSymbol = 2;
		}
		else{
			playerSymbol = 2;
			aiSymbol = 1;
		}
		boolean checked = false;
		for(int i = 0; i < 9; i++){
			if(arr[i] == 0){
				if(!checked){
					newArr[i] = playerSymbol;
					checked = true;
				}
			}
			else{
				newArr[i] = arr[i];
			}
		}
		return newArr;
	}
	/*
	* Method takes in current game array and user symbol
	* then using a simple, fill next open space algorithm,
	* the game array is populated with ai moves.
	*/
	public int[] simulateAIMoveBasic(int[] arr, boolean choice){
		int playerSymbol = 9, aiSymbol = 9;
		int[] newArr = new int[arr.length];
		if(choice){
			playerSymbol = 1;
			aiSymbol = 2;
		}
		else{
			playerSymbol = 2;
			aiSymbol = 1;
		}
		boolean checked = false;
		for(int i = 0; i < 9; i++){
			if(arr[i] == 0){
				if(!checked){
					newArr[i] = aiSymbol;
					checked = true;
				}
			}
			else{
				newArr[i] = arr[i];
			}
		}
		return newArr;
	}
	
	/*public int[] getPlayerMove(int[] arr, boolean choice){
		Scanner scan = new Scanner(System.in);
		S
	}*/
	
	public int howManyMoves(int[] arr){
		int numMoves = 0;
		int numNoMoves = 0;
		for(int i = 0; i < arr.length; i++){
			if(arr[i] == 0){
				numNoMoves++;
			}
		}
		if(numNoMoves == 0){
			numNoMoves = 9;
		}
		else if(numNoMoves % 2 == 1){
			numMoves = (9 - numNoMoves);
		}
		else{
			numMoves = ((9 - numNoMoves) + 1);
		}
		return numMoves;
	}
}
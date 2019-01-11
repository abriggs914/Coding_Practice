import java.util.Random;
import java.util.Scanner;
public class Deck{
	
	Card[] myDeck = new Card[52];
	String[] suits = {"Clubs","Diamonds","Spades","Hearts"};
	int handNumber = 1;
	public Deck(){    //creats a deck object of 52 cards in ascending order in the suit order above.
		String currSuit;
		Card workingCard;
		int j = 0;
		int i = 1;
		for(int k  = 0; k < 52; k++){
			currSuit = suits[j];
			if(k/13 == 1){
				currSuit = suits[1];
			}
			else if(k/13 == 2){
				currSuit = suits[2];
			}
			else if(k/13 == 3){
				currSuit = suits[3];
			}
			if(i < 11 && i > 1){
				workingCard = new Card(k, i, currSuit);
				//System.out.println("New Card: " + workingCard.toString() + ", Index: " + workingCard.index);
			}
			else{
				int holder = i;
				switch(i){
					case 1  :	i = 65;
								break;
					case 11 : 	i = 74;
								break;
					case 12 : 	i = 81;
								break;
					case 13 : 	i = 75;
								break;
				}
				char faceValue = (char)i;
				char mode = 'y';
				workingCard = new Card(k, faceValue, currSuit, mode);
				//System.out.println("New Card: " + workingCard.toString() + ", Index: " + workingCard.index);
				i = holder;
			}
			myDeck[k] = workingCard;
			i++;
			if(i == 14){
				i = 1;
			}
		}
		/*
		for(int l = 0; l < 52; l++){
			System.out.println(myDeck[l].toString());
		}
		*/
	}
	
	public void handGenerator(Deck myDeck){
		System.out.println("Enter the number of cards in your hand");
		int number = 100;
		Scanner scan = new Scanner(System.in);
		try{
			number = scan.nextInt();
		}
		catch(Exception e){
			number = 5;
		}
		int n = 52 - (handNumber*number);
		System.out.println("n: " + n + ", handNumber: " + handNumber);
		if(n <= 0){
			System.out.println("No more possible hands of " + number + " cards can be made with the remaining cards.\n\n");
			return;
		}
		if(number > 52 || number < 1){
			System.out.println("Invalid parameters for a hand of up to 52 different cards: " + number);
			return;
		}
		Card[] myHand = new Card[number];
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = myDeck.myDeck[j].index;
		}
		//printARR(possibilities);
		int i, currCards = 0;
		boolean success = false;
		Card takenCard = new Card(100, 100, "TAKEN");
		int handStillPossible = 0;
		boolean possibleWithCardsRemaining = true;
		while(currCards < number && possibleWithCardsRemaining){
			i = randomInteger(possibilities);//rand.nextInt(52);
			success = checkIfAvailable(i, possibilities);
			if(success){
				myHand[currCards] = myDeck.myDeck[i];
				if(!lastCard(possibilities)){
					myDeck.myDeck[i] = takenCard;
				}
				currCards++;
				success = false;
			}
			/*if(handStillPossible > 49){
				possibleWithCardsRemaining = false;
			}
				//System.out.println(i);
			if(!possibleWithCardsRemaining){
				System.out.println("No more possible hands of " + number + " cards can be made with the remaining cards.\n\n");
				break;
			}*/
		}
		System.out.println("\n\n\tHand Number: " + handNumber);
		handNumber++;
		for(int h = 0; h < number; h++){
			System.out.println(myHand[h]);
		}
		Hand hand1 = new Hand(myHand);
		System.out.println("\n\n");
	}
	
	public Hand handGeneratorGameVersion(Deck myDeck, int number){
		Card[] myHand = new Card[number];
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = myDeck.myDeck[j].index;
		}
		int i, currCards = 0;
		boolean success = false;
		Card takenCard = new Card(100, 100, "TAKEN");
		int handStillPossible = 0;
		boolean possibleWithCardsRemaining = true;
		while(currCards < number && possibleWithCardsRemaining){
			i = randomInteger(possibilities);
			success = checkIfAvailable(i, possibilities);
			if(success){
				myHand[currCards] = myDeck.myDeck[i];
				if(!lastCard(possibilities)){
					myDeck.myDeck[i] = takenCard;
				}
				currCards++;
				success = false;
			}
		}
		System.out.println("\n\n\tHand");
		handNumber++;
		for(int h = 0; h < number; h++){
			System.out.println(myHand[h]);
		}
		Hand hand1 = new Hand(myHand);
		System.out.println("\n\n");
		return hand1;
	}
	
	public Hand handGeneratorGameVersionAI(Deck myDeck, int number){
		Card[] myHand = new Card[number];
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = myDeck.myDeck[j].index;
		}
		int i, currCards = 0;
		boolean success = false;
		Card takenCard = new Card(100, 100, "TAKEN");
		int handStillPossible = 0;
		boolean possibleWithCardsRemaining = true;
		while(currCards < number && possibleWithCardsRemaining){
			i = randomInteger(possibilities);
			success = checkIfAvailable(i, possibilities);
			if(success){
				myHand[currCards] = myDeck.myDeck[i];
				if(!lastCard(possibilities)){
					myDeck.myDeck[i] = takenCard;
				}
				currCards++;
				success = false;
			}
		}
		handNumber++;
		Hand hand1 = new Hand(myHand);
		System.out.println("\tAI hand generated\n\n");
		return hand1;
	}
	
	/*public void drawNewCards(Deck myDeck, Hand handIn, int number, int a, int b, int handSize){
		System.out.println("Drawing a new Card");
		Card[] myHand = new Card[handSize];
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = myDeck.myDeck[j].index;
		}
		for(int k = 0; k < myHand.length; k++){
			if(k != a && k != b){
				myHand[k] = handIn.myHand[k];
			}
			else{
				int i, currCards = 0;
				boolean success = false;
				Card takenCard = new Card(100, 100, "TAKEN");
				int handStillPossible = 0;
				boolean possibleWithCardsRemaining = true;
				//while(currCards < number && possibleWithCardsRemaining){
					i = randomInteger(possibilities);
					success = checkIfAvailable(i, possibilities);
					if(success){
						myHand[k] = myDeck.myDeck[i];
						if(!lastCard(possibilities)){
							myDeck.myDeck[k] = takenCard;
						}
						currCards++;
						success = false;
					}
				//}
			}
		}
		Hand hand1 = new Hand(myHand);
		handIn = hand1;
		hand1.printHand(hand1);
	}*/
	
	public boolean lastCard(int[] arr){
		boolean res = false;
		int zeroCounter = 0;
		for(int i = 0; i < 52; i++){
			if(arr[i] == 101){
				zeroCounter++;
			}
		}
		if(zeroCounter > 51){
			return true;
		}
		return res;
	}
	
	public int randomInteger(int[] arr){
		int res = 0;
		Random rand = new Random();
		boolean keepTrying = true;
		while(keepTrying){
			res = rand.nextInt(52);
			if(arr[res] != 100 && arr[res] != 101){
				return res;
			}
		}
		return res;
	}
	
	public boolean checkIfAvailable(int num, int[] arr){
		for(int i = 0; i < arr.length; i++){
			if(i == num){
				if(arr[i] != 101 && arr[i] != 100){
					//System.out.println("approved " + arr[i]);
					arr[i] = 101;
					return true;
				}
			}
		}
		//System.out.println("failed");
		return false;
	}
	
	public void printDeck(){
		for(int l = 0; l < 52; l++){
			System.out.println(myDeck[l].toString());
		}
		System.out.println("\n\n");
	}
	
	public void printARR(int[] arr){
		for(int l = 0; l < 52; l++){
			System.out.println(arr[l]);
		}
	}
	
	public void shuffle(Deck deckIn){
		Deck workingDeck = new Deck();
		int[] arr = new int[52];
		for(int i = 0; i < 52; i++){
			arr[i] = 0;
		}
		int counter = 0, num = 100;
		boolean success = false;
		while(counter < 52){
			num = randomIntegerGenerator();
			success = checkIfAvailable(num, arr);
			if(success){
				workingDeck.myDeck[counter] = getCardFromIndex(deckIn, num);
				counter++;
				success = false;
			}
		}
		workingDeck.printDeck();
		myDeck = workingDeck.myDeck;
	}
	
	public int randomIntegerGenerator(){
		Random rand = new Random();
		return rand.nextInt(52);
	}
	
	public Card getCardFromIndex(Deck deckIn, int num){
		int i = 0;
		for(i = 0; i < 52; i++){
			if(deckIn.myDeck[i].index == num){
				return deckIn.myDeck[i];
			}
		}
		i = 0;
		return deckIn.myDeck[i];
	}
}
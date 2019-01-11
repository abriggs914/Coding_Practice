import java.util.Random;
import java.util.Scanner;
public class DeckG{
	
	CardG[] myDeck = new CardG[52];
	CardG[] originalDeckIndex = new CardG[52];
	String[] suits = {"Clubs","Diamonds","Spades","Hearts"};
	int handNumber = 1;
	public DeckG(){    //creats a deck object of 52 cards in ascending order in the suit order above.
		String currSuit;
		CardG workingCard;
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
				workingCard = new CardG(k, i, currSuit, k);
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
				workingCard = new CardG(k, faceValue, currSuit, mode, k);
				//System.out.println("New Card: " + workingCard.toString() + ", Index: " + workingCard.index);
				i = holder;
			}
			myDeck[k] = workingCard;
			originalDeckIndex[k] = workingCard;
			i++;
			if(i == 14){
				i = 1;
			}
		}
		//printIndexDeck();
	}
	
	public void handGenerator(DeckG myDeck){
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
		CardG[] myHand = new CardG[number];
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = myDeck.myDeck[j].index;
		}
		//printARR(possibilities);
		int i, currCards = 0;
		boolean success = false;
		CardG takenCard = new CardG(100, 100, "TAKEN", -1);
		int handStillPossible = 0;
		boolean possibleWithCardsRemaining = true;
		while(currCards < number && possibleWithCardsRemaining){
			i = randomInteger(possibilities);//rand.nextInt(52);
			success = checkIfAvailable(i, possibilities, myDeck);
			if(success){
				myHand[currCards] = myDeck.myDeck[i];
				if(!lastCard(possibilities)){
					takenCard.id = myDeck.myDeck[i].id;
					takenCard.id = myDeck.myDeck[i].id;
					System.out.println("TakenCard being inserted: " + takenCard);
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
		HandG hand1 = new HandG(myHand);
		System.out.println("\n\n");
	}
	
	public HandG handGeneratorGameVersion(DeckG myDeck, int number){
		CardG[] myHand = new CardG[number];
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = myDeck.myDeck[j].index;
		}
		//System.out.println("printing possibilities array");
		//printARR(possibilities);
		int i, currCards = 0;
		boolean success = false;
		CardG takenCard = new CardG(100, 100, "TAKEN", -1);
		int handStillPossible = 0;
		boolean possibleWithCardsRemaining = true;
		while(currCards < number && possibleWithCardsRemaining){
			i = randomInteger(possibilities);
			success = checkIfAvailable(i, possibilities, myDeck);
			//System.out.println("printing deck after checkIfAvailable:\n");
			//myDeck.printDeck();
			if(success){
				myHand[currCards] = myDeck.myDeck[i];
				if(!lastCard(possibilities)){
					//takenCard.id = myDeck.myDeck[i].id;
					//takenCard.id = myDeck.myDeck[i].id;
					//System.out.println("TakenCard being inserted in hand generation: " + takenCard);
					//myDeck.myDeck[i] = takenCard;
				}
				currCards++;
				success = false;
			}
		}
		System.out.println("\n\n\tYour Hand");
		handNumber++;
		for(int h = 0; h < number; h++){
			System.out.println(myHand[h]);
		}
		HandG hand1 = new HandG(myHand);
		System.out.println("\n\n");
		return hand1;
	}
	
	public HandG handGeneratorGameVersionAI(DeckG myDeck, int number){
		CardG[] myHand = new CardG[number];
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = myDeck.myDeck[j].index;
		}
		//System.out.println("printing possibilities array");
		//printARR(possibilities);
		int i, currCards = 0;
		boolean success = false;
		CardG takenCard = new CardG(100, 100, "TAKEN", -1);
		int handStillPossible = 0;
		while(currCards < number){
			i = randomInteger(possibilities);
			success = checkIfAvailable(i, possibilities, myDeck);
			//System.out.println("printing deck after checkIfAvailable:\n");
			//myDeck.printDeck();
			if(success){
				myHand[currCards] = myDeck.myDeck[i];
				if(!lastCard(possibilities)){
					//takenCard.id = myDeck.myDeck[i].id;
					//takenCard.id = myDeck.myDeck[i].id;
					//System.out.println("TakenCard being inserted in hand generation: " + takenCard);
					//myDeck.myDeck[i] = takenCard;
				}
				currCards++;
				success = false;
			}
		}
		handNumber++;
		HandG hand1 = new HandG(myHand);
		System.out.println("\n\tAI hand generated\n\n");
		return hand1;
	}
	
	public CardG drawNewCards(DeckG myDeck, int number){
		System.out.println("Drawing card in Deck");
		CardG[] myHand = new CardG[number];
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = myDeck.myDeck[j].index;
		}
		int i, currCards = 0;
		boolean success = false;
		CardG takenCard = new CardG(100, 100, "TAKEN", -1);
		int handStillPossible = 0;
		boolean possibleWithCardsRemaining = true;
		while(currCards < number && possibleWithCardsRemaining){
			i = randomInteger(possibilities);
			success = checkIfAvailable(i, possibilities, myDeck);
			if(success){
				myHand[currCards] = myDeck.myDeck[i];
				if(!lastCard(possibilities)){
				}
				currCards++;
				success = false;
			}
		}
		System.out.println("\n\n");
		return myHand[number-1];
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
			if(arr[i] == 101 || arr[i] == -1 || arr[i] == -2){
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
			if(arr[res] != 100 && arr[res] != 101 && arr[res] != -1 && arr[res] != -2){
				if(res > 0 && res < 53){
					for(int i = 0; i < arr.length; i++){
						if(arr[i] > 0 && arr[i] < 53){
							//System.out.println("returning index: " + res);
							return res;
						}
					}
				}
			}
		}
		System.out.println("Something went wrong in randominteger generation");
		return res;
	}
	
	public boolean checkIfAvailable(int num, int[] arr, DeckG deckIn){
		
		CardG takenCard = new CardG(100, 100, "TAKEN", -1);
		for(int i = 0; i < arr.length; i++){
			if(i == num){
				if(arr[i] < 53 && arr[i] > 0){
					takenCard.id = deckIn.myDeck[i].id;
					deckIn.myDeck[i].index = takenCard.index;
					deckIn.myDeck[i].id = takenCard.id;
					//System.out.println("approved " + arr[i] + ", takenCard: " + takenCard);
					arr[i] = 101;
					/*
					if(arr[i] == -1){
						arr[i] = -1;
					}
					else if(arr[i] == -2){
						arr[i] = -2;
					}
					else if(arr[i] == 101){
						arr[i] = 101;
					}
					else if(arr[i] == 100){
						arr[i] = 100;
					}
					else{				
						arr[i] = arr[i];
					}*/
					return true;  // i think just return true works instead of the else ifs..
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
	
	public void printIndexDeck(){
		for(int l = 0; l < 52; l++){
			System.out.println(originalDeckIndex[l].toString());
		}
	}
	
	public void printARR(int[] arr){
		for(int l = 0; l < 52; l++){
			System.out.println(arr[l]);
		}
	}
	
	public void shuffle(DeckG deckIn){
		System.out.println("\n\n\tShuffling\n\n");
		DeckG workingDeck = new DeckG();
		int[] arr = new int[52];
		for(int i = 0; i < 52; i++){
			arr[i] = deckIn.myDeck[i].index;
		}
		int counter = 0, num = 100;
		boolean success = false;
		while(counter < 52){
			num = randomIntegerGenerator();
			success = checkIfAvailable(num, arr, deckIn);
			//System.out.println("\n\n\tLoop, Counter: " + counter + ", success: " + success);
			if(success){
				workingDeck.myDeck[counter] = getCardFromId(deckIn, num);
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
	
	public CardG getCardFromId(DeckG deckIn, int num){
		int i = 0;
		for(i = 0; i < 52; i++){
			//System.out.println("deckIn.myDeck[i]["+i+"].id: " + deckIn.myDeck[i].id + ", num: " + num);
			if(deckIn.myDeck[i].id == num){
				//if(deckIn.myDeck[i].index < 53 && deckIn.myDeck[i].index > -1){
					return deckIn.myDeck[i];
				//}
			}
		}
		i=0;
		System.out.println("Something went wrong in getting card from id.\n\tATTEMPTED: " + num);
		return deckIn.myDeck[i];
		
	}
	
	public void updateDeck(HandG handIn){	
		System.out.println("\n\n\tUpdating Deck\n\n");
		int intTarget = 0;
		String stringTarget = "";
		for(int i = 0; i < handIn.myHand.length; i++){
			intTarget = handIn.myHand[i].value;
			stringTarget = handIn.myHand[i].suit;
			for(int j = 0; j < myDeck.length; j++){
				if(myDeck[j].value == intTarget && myDeck[j].suit.equals(stringTarget)){
					myDeck[j].index = handIn.myHand[i].index;
				}
			}
		}
		System.out.println("Printing updated deck after checking for pairs");
		printDeck();
	}
}
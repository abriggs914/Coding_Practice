import java.util.Random;
public class Deck{
	
	Card[] myDeck = new Card[52];
	String[] suits = {"Clubs","Diamonds","Spades","Hearts"};
	int handNumber = 1;
	public Deck(){
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
				workingCard = new Card(k, faceValue, currSuit);
				i = holder;
			}
			myDeck[k] = workingCard;
			i++;
			if(i == 14){
				i = 1;
			}
		}
		for(int l = 0; l < 52; l++){
			System.out.println(myDeck[l].toString());
		}
	}
	
	public void handGenerator(Deck myDeck){
		if(handNumber > 10){
			return;
		}
		Card[] myHand = new Card[5];
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = myDeck.myDeck[j].index;
		}
		int i, currCards = 0;
		boolean success = false;
		Random rand = new Random();
		Card takenCard = new Card(100, 100, "TAKEN");
		int handStillPossible = 0;
		boolean possibleWithCardsRemaining = true;
		while(currCards < 5 && possibleWithCardsRemaining){
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
			else{
				if(handStillPossible < 53){
					myDeck.myDeck[i] = takenCard;
				}
				handStillPossible++;
			}
			if(handStillPossible > 52){
				possibleWithCardsRemaining = false;
			}
				//System.out.println(i);
			if(!possibleWithCardsRemaining){
				System.out.println("No more possible hands of 5 cards can be made with the remaining cards.\n\n");
				break;
			}
		}
		System.out.println("\n\n\tHand Number: " + handNumber);
		handNumber++;
		for(int h = 0; h < 5; h++){
			System.out.println(myHand[h]);
		}
	}
	
	public boolean lastCard(int[] arr){
		boolean res = false;
		int zeroCounter = 0;
		for(int i = 0; i < 52; i++){
			if(arr[i] == 100){
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
			if(arr[res] != 100){
				return res;
			}
		}
		return res;
	}
	
	/*public void handGenerator(Deck myDeck, Hand otherPlayer){
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = j;
		}
		for(int k = 0; k < 5; k++){
			for(int j = 0; j < 52; j++){
				if(otherPlayer.myHand[k].index == j){
					possibilities[j] = 100;
				}
			}
		}
		int i, currCards = 0;
		boolean success = false;
	
		//Random rand = new Random();
		Card[] myHand = new Card[5];
		Card takenCard = new Card(100, 100, "TAKEN");
		while(currCards < 5){
			i = randomInteger(myDeck);//rand.nextInt(52);
			success = checkIfAvailable(i, possibilities);
			if(success){
				myHand[currCards] = myDeck.myDeck[i];
				myDeck.myDeck[i] = takenCard;
				currCards++;
				success = false;
			}
			else{
				myDeck.myDeck[i] = takenCard;
			}
			//System.out.println(i);
		}
		System.out.println("\n\n");
		for(int h = 0; h < 5; h++){
			System.out.println(myHand[h]);
		}
	}*/
	
	public boolean checkIfAvailable(int num, int[] arr){
		for(int i = 0; i < arr.length; i++){
			if(i == num){
				if(arr[i] != 100){
					//System.out.println("approved " + arr[i]);
					arr[i] = 0;
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
	}
	
}
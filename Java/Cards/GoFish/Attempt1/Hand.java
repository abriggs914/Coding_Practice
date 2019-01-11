import java.util.Random;
public class Hand{
	
	public Card[] myHand = new Card[5];
	public Hand(Deck myDeck){
		int[] possibilities = new int[52];
		for(int j = 0; j < 52; j++){
			possibilities[j] = j;
		}
		int i, currCards = 0;
		boolean success = false;
		Random rand = new Random();
		Card takenCard = new Card(100, 100, "TAKEN");
		while(currCards < 5){
			i = rand.nextInt(52);
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
	}
	
	public Hand(Deck myDeck, Hand otherPlayer){
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
		Random rand = new Random();
		Card[] myHand = new Card[5];
		Card takenCard = new Card(100, 100, "TAKEN");
		while(currCards < 5){
			i = rand.nextInt(52);
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
	}
	
	/*
	* Method checks deck to see if it can place the card it wants to.
	* parameters are target num and deck possibilities arr.
	*/
	public boolean checkIfAvailable(int num, int[] arr){
		for(int i = 0; i < arr.length; i++){
			if(i == num){
				if(arr[i] != 0 && arr[i] != 100){
					//System.out.println("approved " + arr[i]);
					arr[i] = 0;
					return true;
				}
			}
		}
		//System.out.println("failed");
		return false;
	}
}
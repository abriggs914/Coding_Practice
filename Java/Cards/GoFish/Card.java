public class Card{

	public int index;
	public int value;
	public int id;
	public String suit;
	public char faceValue;
	
	public Card(int index, int value, String suit, int id){
		this.index = index+1;
		this.value = value;
		this.suit = suit;
		this.id = id;
	}
	
	public Card(int index, char faceValue, String suit, char mode, int id){
		//System.out.println("special card");
		this.index = index+1;
		this.faceValue = faceValue;
		this.suit = suit;
		this.value = getValue(faceValue);
		this.id = id;
	}
	
	public String toString(){
		String res = "";
		if(index > 53 || index <0
		){
			res += "\t";
		}
		if(value != 1 && value != 11 && value != 12 && value != 13){
			res += value;
		}
		else{
			res += faceValue;
		}
		res += " of ";
		res += suit;
		res += ", value: " + value + ", Index: " + index;
		res += ", DECKID: " + id;
		return res;
	}
	
	public int getValue(char c){
		int n = 0;
		//System.out.println("char: " + c);
		switch((int)c){ 	
			case 65  :	n = 1;
						break;
			case 74 : 	n = 11;
						break;
			case 81 : 	n = 12;
						break;
			case 75 : 	n = 13 ;
						break;
		}
		return n;
	}

	public void populateTakenCards(Card[] arr, Deck deckIn){
		Card takenCard = new Card(100, 100, "TAKEN", -1);
		for(int i = 0; i < 26; i++){
			takenCard.id = deckIn.myDeck[i].id;
			arr[i] = takenCard;
		}
	}
	
	public String pairRemoveStatement(){
		int a = this.value;
		String res = "";
		switch(a){
			case 1 :	res = " Aces ";
						break;
			case 2 :	res = " Twos ";
						break;
			case 3 :	res = " Threes ";
						break;
			case 4 :	res = " Fours ";
						break;
			case 5 :	res = " Fives ";
						break;
			case 6 :	res = " Sixes ";
						break;
			case 7 :	res = " Sevens ";
						break;
			case 8 :	res = " Eights ";
						break;
			case 9 :	res = " Nines ";
						break;
			case 10 :	res = " Tens ";
						break;
			case 11 :	res = " Jacks ";
						break;
			case 12 :	res = " Queens ";
						break;
			case 13 :	res = " Kings ";
						break;
			default : 	res = " Something went wrong ";
						break;
		}
		return res;
	}
}
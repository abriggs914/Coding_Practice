public class Card{

	public int index;
	public int value;
	public String suit;
	public char faceValue;
	
	public Card(int index, int value, String suit){
		this.index = index;
		this.value = value;
		this.suit = suit;
	}
	
	public Card(int index, char faceValue, String suit){
		this.index = index;
		this.faceValue = faceValue;
		this.suit = suit;
	}
	
	public String toString(){
		String res = "";
		if(value != 0){
			res += value;
		}
		else{
			res += faceValue;
		}
		res += " of ";
		res += suit;
		return res;
	}
}
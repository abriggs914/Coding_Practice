/*
*
*
*
*/
public class SpecialCardG extends CardG{

	public int numMatchingValuesInHand;
	
	public SpecialCardG(int index, int value, String suit, int id, int numIn){
		super(index+1, value, suit, id);
		numMatchingValuesInHand = numIn;
	}
	
	public SpecialCardG(int index, char faceValue, String suit, char mode, int id, int numIn){
		//System.out.println("special card");
		super(index+1, faceValue, suit, mode, id);
		numMatchingValuesInHand = numIn;
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
		res += ", numMatchingValuesInHand: " + numMatchingValuesInHand;
		return res;
	}
	
	public void printCardArr(CardG[] arr){
		System.out.println("\n\nPrinting\n\n");
		for(int i = 0; i < arr.length; i++){
			System.out.println(arr[i]);
		}
		System.out.println("\n\n\n\n");
	}
}
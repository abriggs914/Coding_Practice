public class IndexDriver{
	public static void main(String[] args){
	
		Card card0001 = new Card("The Locust God1", "creature", "BU", 4, 6, 6, "Magic Origins", 139, 199, true, "Flying, Haste, Fear, First Strike");
		Card card0003 = new Card("The Special", "creature", "RD", 4, 5, 6, "Not sure", 121, 199, true, "Flying, First Strike");
		Card card0002 = new Card("The Locust God2", "creature", "RD", 5, 4, 6, "Magic Origins", 138, 199, true, "Flying, Haste, Fear, First Strike");
		Card card0004 = new Card("The Special One", "creature", "RDWTB", 5, 4, 6, "Not sure", 139, 199, true, "");
		Card card0005 = new Card("The Special", "creature", "RD", 4, 5, 6, "Not sure", 121, 199, true, "Flying, First Strike");
		Card card0006 = new Card("The Locust God2", "creature", "RD", 5, 4, 6, "Not sure", 139, 199, true, "Flying, Haste, Fear, First Strike");
		Card card0007 = new Card("The Special One", "creature", "RDWTB", 5, 4, 6, "Magic Origins", 129, 199, true, "");
		Card[] arr = {card0001,card0002,card0003,card0004,card0005, card0006,card0007};
		IndexedCollection res = new IndexedCollection(arr);
		
		/*String set = "17   -   Magic Origins";
			System.out.println( "\n" + card0001.collection + ".\n" + set.substring(9, set.length()) + ".");
			String t = set.substring(9, set.length());
		if(t.equals(card0001.collection)){
			System.out.println("true");
		}
		else{
			System.out.println("false");
		}*/
	}
}
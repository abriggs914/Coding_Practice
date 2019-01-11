/*
*
*
*
*/
public class CardsDriver1G{
	public static void main(String[] args){
		DeckG deck1 = new DeckG();
		DeckG deck2 = new DeckG();
		//Hand hand1 = new Hand(deck1);
		
		//Hand hand2 = new Hand(deck1, hand1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.handGenerator(deck1);
		deck1.printDeck();
		deck2.shuffle(deck2);
		deck2.handGenerator(deck2);
		deck2.handGenerator(deck2);
	}
}
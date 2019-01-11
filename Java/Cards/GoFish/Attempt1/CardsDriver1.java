public class CardsDriver1{
	public static void main(String[] args){
		Deck deck1 = new Deck();
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
		deck1.printDeck();
	}
}
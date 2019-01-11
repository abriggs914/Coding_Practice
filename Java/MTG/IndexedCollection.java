/**
*Java program to sort a card collection into a set, and index them.
*Avery Briggs 3471065
*July 2018
*/

import java.util.Scanner;

public class IndexedCollection{
	
	public static int i;
	public static Card[] cardNames = new Card[1];
	
	public IndexedCollection(Card[] wholeCardCollection){
		//"Please select a collection that you would like to view:"
		String[] sets = {"1    -   Limited Edition Alpha","2    -   Limited Edition Beta","3    -   Unlimited Edition","4    -   Revised Edition", 
						   "5    -   Fourth Edition","6    -   Fifth Edition","7    -   Classic Sixth Edition", 
						   "8    -   Seventh Edition","9    -   Eighth Edition","10   -   Tenth Edition", 
						   "11   -   Magic 2010 Core Set","12   -   Magic 2011 Core Set","13   -   Magic 2012 Core Set", 
						   "14   -   Magic 2013 Core Set","15   -   Magic 2014 Core Set","16   -   Magic 2015 Core Set", 
						   "17   -   Magic Origins","18   -   Magic 2019 Core Set","19   -   Arabian Nights", 
						   "20   -   Antiquities","21   -   Legends","22   -   The Dark","23   -   Fallen Empires", 
						   "24   -   Ice Age","25   -   Homelands","26   -   Alliances","27   -   Mirage", 
						   "28   -   Visions","29   -   Weatherlight","30   -   Tempest","31   -   Stronghold", 
						   "32   -   Exodus","33   -   Urza's Saga","34   -   Urza's Legacy","35   -   Urza's Destiny", 
						   "36   -   Mercadian Masques","37   -   Nemesis","38   -   Prophecy","39   -   Invasion", 
						   "40   -   Planeshift","41   -   Apocalypse","42   -   Odyssey","43   -   Torment", 
						   "44   -   Judgement","45   -   Onslaught","46   -   Legions","47   -   Scourge", 
						   "48   -   Mirrodin","49   -   Darksteel","50   -   Fifth Dawn","51   -   Fifth Dawn", 
						   "52   -   Champions of Kamigawa","53   -   Betrayers of Kamigawa","54   -   Saviors of Kamigawa", 
						   "55   -   Ravnica: City of Guilds","56   -   Guildpact","57   -   Dissension","58   -   Coldsnap", 
						   "59   -   Time Spiral","60   -   Planar Chaos","61   -   Future Sight","62   -   Lorwyn", 
						   "63   -   Morningtide","64   -   Shadowmoor","65   -   Eventide","66   -   Shards of Alara", 
						   "67   -   Conflux","68   -   Alara Reborn","69   -   Zendikar","70   -   Worldwake", 
						   "71   -   Rise of the Eldrazi","72   -   Scars of Mirrodin","73   -   Mirrodin Besieged", 
						   "74   -   New Phyrexia","75   -   Innistrad","76   -   Dark Assension","77   -   Avacyn Restored", 
						   "78   -   Return to Ravnica","79   -   Gatecrash","80   -   Dragon's Maze","81   -   Theros", 
						   "82   -   Born of the Gods","83   -   Journey into Nyx","84   -   Khans of Tarkir","85   -   Fate Reforged", 
						   "86   -   Dragons of Tarkir","87   -   Battle for Zendikar","88   -   Oath of the Gatewatch", 
						   "89   -   Shadows over Innistrad","90   -   Eldritch Moon","91   -   Kaladesh","92   -   Aether Revolt", 
						   "93   -   Amonkhet","94   -   Hour of Devastion","95   -   Ixalan","96   -   Rivals of Ixalan", 
						   "97   -   Portal","98   -   Portal Second Age","99   -   Portal Three Kingdoms","100  -   Starter 1999", 
						   "101  -   Starter 2000","102  -   Chronicles","103  -   Rivals Quick Start Set","104  -   Multiverse Gift Box", 
						   "105  -   Anthologies","106  -   Battle Royale Box Set","107  -   Beatdown Box Set","108  -   Deckmasters: Garfeld vs. Finkel",
						   "109  -   Premium Foil Booster","110  -   Duels of the Planeswalkers","111  -   Modern Event Deck",
						   "112  -   Duel Decks: Elves vs. Goblins","113  -   Duel Decks: Jace vs. Chandra","114  -   Duel Decks: Divine vs. Demonic", 
						   "115  -   Duel Decks: Garruk vs. Liliana","116  -   Duel Decks: Phyrexia vs. Coalition","117  -   Duel Decks: Elspeth vs. Tezzeret", 
						   "118  -   Duel Decks: Knights vs. Dragons ","119  -   Duel Decks: Ajani vs. Nicol Bolas","120  -   Duel Decks: Venser vs. Koth", 
						   "121  -   Duel Decks: Izzet vs. Golgari","122  -   Duel Decks: Sorin vs. Tibalt","123  -   Duel Decks: Heroes vs. Monsters", 
						   "124  -   Duel Decks: Jace vs. Vraska","125  -   Duel Decks: Speed vs. Cunning","126  -   Duel Decks: Elspeth vs. Kiora", 
					       "127  -   Duel Decks: Zendikar vs. Eldrazi","128  -   Duel Decks: Blessed vs. Cursed", 
						   "129  -   Duel Decks: Nissa vs. Ob Nixilis","130  -   Duel Decks: Mind vs. Might","131  -   Duel Decks: Merfolk vs. Goblins", 
						   "132  -   Duel Decks: Elves vs. Inventors","133  -   From the Vault: Dragons","134  -   From the Vault: Exiled", 
						   "135  -   From the Vault: Relics","136  -   From the Vault: Legends","137  -   From the Vault: Realms", 
						   "138  -   From the Vault: Twenty","139  -   From the Vault: Annihilation","140  -   From the Vault: Angels", 
						   "141  -   From the Vault: Lore","142  -   From the Vault: Transform","143  -   Signature Spellbook: Jace", 
						   "144  -   Premium Deck Series: Slivers","145  -   Premium Deck Series: Fire and Lightning","146  -   Premium Deck Series: Graveborn", 
						   "147  -   Modern Masters","148  -   Modern Masters 2015 Edition","149  -   Eternal Masters", 
						   "150  -   Modern Masters 2017 Edition","151  -   Iconic Masters","152  -   Masters 25","153  -   Deck Builder's Toolkit",  
							"154  -   Deck Builder's Toolkit (Refreshed Version)","155  -   Deck Builder's Toolkit (2012 Edition)"
							,"156  -   Deck Builder's Toolkit (2014 Core Set Edition)","157  -   Deck Builder's Toolkit (2015 Core Set Edition)"
							,"158  -   Deck Builder's Toolkit (Magic Origins Edition)","159  -   Deck Builder's Toolkit (Shadows over Innistrad Edition)"
							,"160  -   Deck Builder's Toolkit (Amonkhet Edition)","161  -   Deck Builder's Toolkit (Ixalan Edition)"
							,"162  -   Planechase","163  -   Planechase 2012 Edition","164  -   Planechase Anthology","165  -   Archenemy"
							,"166  -   Archenemy: Nicol Bolas","167  -   Commander","168  -   Commander's Arsenal"
							,"169  -   Commander (2013 Edition)","170  -   Commander (2014 Edition)","171  -   Commander (2015 Edition)","172  -   Commander (2016 Edition)"
							,"173  -   Commander Anthology","174  -   Commander (2017 Edition)","175  -   Commander Anthology Volume II","176  -   Commander (2018 Edition)"
							,"177  -   Conspiracy","178  -   Conspiracy: Take the Crown","179  -   Explorers of Ixalan","180  -   Battlebond"
							,"181  -   Collector's Edition","182  -   International Collector's Edition"};
		for(i = 0; i < sets.length; i++){
			System.out.print(printLine(i, sets));
		}
		
		Scanner scan = new Scanner(System.in);
		int choice = 0;
		System.out.println("");
		System.out.println("Please select a collection that you would like to view:");
		try{
			choice = scan.nextInt();
		}
		catch(Exception e){
			choice = 1;
		}
		System.out.println("Selection\n\t\t " + sets[choice-1]);
		indexMyCards(wholeCardCollection, sets[choice-1]);
		
		System.out.println(" ");
		int k;
		for(k = 0; (k + 8) < 160; k++){
			if(k == 0){
				System.out.print("\t");
				System.out.print("t");
				k+=9;
			}
			for(int y = 0; y < 47; y++){
				System.out.print(" ");
				k++;
			}
			if((k + 8) < 160){
				System.out.print("t");
			}
			k++;
		}
		//System.out.println("k: " + k);
	}
	
	public static String printLine(int i, String[] arr){
		String res = "\n\t";
		int k, options = 0;
		for(k = 0; (k + 8) < 160 && options < 2; k++){
			if(k == 0){
				//System.out.print("\t");
				//System.out.print("t");
				res += "\t";
				res += arr[i];
				k+=9;
				i++;
				options++;
			}
			if(i > arr.length-1){
				break;
			}
			int y = arr[i].length();
			if(y > 47 && options > 0){
				for(int g = 0; g < 47; g++){
					res += " ";
					k++;
				}
				res += arr[i];
				i++;
				return res;
			}
			for(y = y; y < 47; y++){
				System.out.print(" ");
				k++;
			}
			if((k + 8) < 160 && options > 1){
				return res;
			}
			else{
				res += arr[i];
				k += arr[i].length();
				i++;
			}
			k++;
		}
		return res;
	}
	
	public static void indexMyCards(Card[] collection, String set){
		int a = collection.length;
		int b = 0;
		int c = 0;
		int x = 0;
		int y = 0;
		int[] collectionNums = new int[1];
		int[] tempCNums = new int [1];
		int coNuComp = 0;
		int[] tempC = new int[1];
		Card[] tempS = new Card[1];
		System.out.println("a: " + a);
		for(int i = 0; i < a; i++){
			//System.out.println("collection[i].collection: " + collection[i].collection + "\nset.substring(9, set.length()): " + set.substring(9, set.length())+
			//					"\ncollection[i].collection.equals(set.substring(9, set.length())): " + collection[i].collection.equals(set.substring(9, set.length())));
			if(collection[i].collection.equals(set.substring(9, set.length()))){
				x += collection[i].collectionTotal;
				collectionNums[coNuComp] = collection[i].collectionNum;
				cardNames[coNuComp] = collection[i];
				coNuComp++;
				tempC = new int[coNuComp+1];
				tempS = new Card[coNuComp+1];
				for(int j = 0; j < coNuComp; j++){
					tempC[j] = collectionNums[j];
					tempS[j] = cardNames[j];
				}
				collectionNums = tempC;
				cardNames = tempS;
				//System.out.println("collectionNums.length: " + collectionNums.length + ", cardNames.length: " + cardNames.length);
			}
		}
		tempCNums = new int[collectionNums.length];
		for(int j = 0; j < coNuComp; j++){
			tempCNums[j] = collectionNums[j];
		}
		System.out.println("collectionNums.length: " + collectionNums.length);
		int p = selectionSort(tempCNums);
		System.out.println("p: " + p);
		if(p != tempCNums.length){
			b = ((x-(tempCNums.length-p)*(x/coNuComp))/(coNuComp-(tempCNums.length-p))) ;
		}
		else{
			b = x/coNuComp;
		}
		if(coNuComp == 0){
			System.out.println("No cards in your collection fit this set");
			return;
		}
			//System.out.println("b: " + b + " offsets.length: " + offsets.length + "collectionNums.length: " + collectionNums.length);
			/*for(int j = 1; j < collectionNums.length; j++){
				System.out.println("collectionNums[j]: " + collectionNums[j]);
			}*/
		int k = 0;
		boolean collNumFound = false;
		System.out.println("Number of cards in set: " + b);
		for(int i = 0; i < b; i++){
			//System.out.println("i: " + i);
			String message = "] ";
			if(i < 100){
				message += "P";
			}
			if(i < 10){
				message += "Q";
			}
			message += ": \t";
			boolean alreadyIndexed = false;
			int count = 0;
			for(int j = 0; j < collectionNums.length-1; j++){
					if(i == collectionNums[j]){
						if(!alreadyIndexed){
							System.out.print("CARD["+i);         //   +message + );
							System.out.print("] " + ((i < 100)? " ":"") + ((i < 10)? " ":"") + ": \t" + cardNames[j].name);	
							collNumFound = true;
							alreadyIndexed = true;
							count ++;
						}
						else{
							count++;
						}
					}
					else if(j == collectionNums.length-2 && !collNumFound){
						System.out.print("CARD["+i);         //   +message + );
						System.out.println("] " + ((i < 100)? " ":"") + ((i < 10)? " ":"") + ": UNKNOWN");
						alreadyIndexed = false;
						count = 0;
					}
					if((count > 1) && (j == collectionNums.length-2)){
						System.out.println("  -  -  -  -  -  - X " + count);
						alreadyIndexed = false;
						count = 0;
					}
					else if(count == 1 && (j == collectionNums.length-2)){
						System.out.println("");
						alreadyIndexed = false;
						count = 0;
					}
				//}
			}
			collNumFound = false;
		}
		Scanner scan = new Scanner(System.in);
		/*boolean keepIndexingCards = true;
		int usrChoice = 0;
		for(int f = 0; f < 10 && keepIndexingCards; f++){85
			try{
				System.out.println("Would you like to see another deck?\n\t1 - yes\n\t2 - no");
				usrChoice = scan.nextInt();
			}
			catch(Exception e){
				keepIndexingCards = false;
			}
		}*/
		//storing all cards with correct set in an array and a number for index
	}
	
	public static int selectionSort(int arr[]){
		int unique = 0;
        int n = arr.length;
        // One by one move boundary of unsorted subarray
        for (int i = 0; i < n-1; i++){
            // Find the minimum element in unsorted array
            int min_idx = i;
            for (int j = i+1; j < n; j++)
                if (arr[j] < arr[min_idx]){
                    min_idx = j;
				}
				else if(arr[j] == arr[min_idx]){
					unique--;
				}
            // Swap the found minimum element with the first
            // element
            int temp = arr[min_idx];
            arr[min_idx] = arr[i];
            arr[i] = temp;
        }
		return uniqueElements(arr);
	}
	
	public static int uniqueElements(int[] arr){
		int unique = 0;
		for(int y = 0; y < arr.length-1; y++){
			if(arr[y] != arr[y+1]){
				unique++;
			}
		}
		return unique;
	}
}










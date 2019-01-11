/**
Java Program that creates a magic card object
Avery Briggs 3471065
June 2018
*/
import java.util.Scanner;
import java.io.*;
import java.text.NumberFormat;

public class Card{
	String iD, name, attributes, colour, collection, type;
	int atk, def, convertedManaCost, collectionNum, collectionTotal;
	boolean abilities;
	
	public Card(String name, String type, String colour, int convertedManaCost, int atk, int def, String collection, int collectionNum, int collectionTotal, boolean abilities, String attributes){
		this.name = name;
		this.type = type;
		this.colour = colourDesignation(colour);
		this.convertedManaCost = convertedManaCost;
		this.atk = atk;
		this.def = def; 
		this.collection = collection;
		this.collectionNum = collectionNum;
		this.collectionTotal = collectionTotal;
		this.abilities = abilities;
		this.attributes = attributesDesignation(attributes);
	}
	
	public Card(String iD, String name, String type, String colour, int convertedManaCost, int atk, int def, String collection, int collectionNum, int collectionTotal, boolean abilities, String attributes){
		this.iD = iD;
		this.name = name;
		this.type = type;
		this.colour = colour;
		this.convertedManaCost = convertedManaCost;
		this.atk = atk;
		this.def = def; 
		this.collection = collection;
		this.collectionNum = collectionNum;
		this.collectionTotal = collectionTotal;
		this.abilities = abilities;
		this.attributes = attributes;
	}
	
	public String attributesDesignation(String attributesIn){
		String abilitiesFinal;
		String temp;
		String workingString;
		int x = attributesIn.length();
		Scanner scan = new Scanner(System.in);
		boolean stopLooking = false;
		boolean multipleWordsRoutine = false;
		boolean multipleAttributesRoutine = false;
		String[] fourLetterWords = {"Crew", "Dash", "Echo", "Epic", "Fear", "Fuse"}; //6
		String[] fiveLetterWords = {"Delve", "Equip", "Evoke", "Flash", "Graft", "Haste", "Haunt", "Melee", "Morph", "Prowl", "Reach", "Skulk", "Storm", "Surge"}; //14
		String[] sixLetterWords = {"Absorb", "Ascend", "Assist", "Awaken", "Bestow", "Devoid", "Devour", "Dredge", "Embalm", "Emerge", "Evolve", "Extort", "Fading",
									"Flying", "Frenzy", "Heroic", "Infect", "Ingest", "Kicker", "Menace", "Morbid", "Myriad", "Renown", "Ripple", "Shadow", "Splice", "Strive", "Wither"}; //25
		String[] sevenLetterWords = {"Afflict", "Amplify", "Banding", "Bolster", "Bushido", "Buyback", "Cascade", "Cipher", "Convoke", "Cycling", "Enchant", "Entwine", "Exalted", "Exploit",
									"Fortify", "Imprint", "Madness", "Miracle", "Modular", "Outlast", "Partner", "Phasing", "Prowess", "Rampage", "Rebound", "Retrace",
									"Shroud", "Suspend", "Trample", "Tribute", "Undying", "Unearth", "Unleash"}; //30
		String[] eightLetterWords = {"Affinity", "Champion", "Conspire", "Cycling", "Defender", "Dethrone", "Escalate", "Flanking", "Forecast", "Hellbent", "Hexproof",
										"Hideaway", "Inspired", "Landfall", "Landwalk", "Lifelink", "Ninjutsu", "Offering", "Overload", "Persist", "Provoke", "Recover", "Scavenge",
										"Soulbond", "Sunburst"}; //22
		String[] nineLetterWords = {"Aftermath", "Battalion", "Bloodrush", "Fabricate", "Ferocious", "Flashback", "Immediate", "Improvise", "Megamorph", "Poisonous", "Reinforce", "Replicate", "Soulshift", "Transmute",
										"Undaunted", "Vanishing", "Vigilance"}; //12
		String[] tenLetterWords = {"Changeling", "Deathtouch", "Eternalize", "Formidable", "Gravestorm", "Intimidate", "Islandwalk", "Protection"}; //6
		String[] elevenLetterWords = {"Annihilator", "Bloodthirst", "Horsemanship", "Monstrosity", "Multikicker", "Transfigure"}; //4
		String[] twelveLetterWords = {"Split Second"};
		String[] thirteenLetterWords = {"Constellation"}; //1
		String[] fourteenLetterWords = {"Indestructible"}; //1
		String[] multipleWords = {"Aura Swap", "Battle Cry", "Cumulative Upkeep", "Double Strike", "First Strike", "Hidden Agenda", "Level Up", "Living Weapon",
									"Spell Mastery", "Split Second", "Totem Armor"}; //10
		if(attributesIn.contains(" ")){
			multipleWordsRoutine = true;
		}
		else{
			switch(x){								//for cards that have only one ability
				case 0 :    return "N/A";
				case 4 : 	abilitiesFinal = whichAbility(fourLetterWords.length, fourLetterWords, attributesIn);
							break;
				case 5 : 	abilitiesFinal = whichAbility(fiveLetterWords.length, fiveLetterWords, attributesIn);
							break;
				case 6 : 	abilitiesFinal = whichAbility(sixLetterWords.length, sixLetterWords, attributesIn);
							break;
				case 7 : 	abilitiesFinal = whichAbility(sevenLetterWords.length, sevenLetterWords, attributesIn);
							break;
				case 8 : 	abilitiesFinal = whichAbility(eightLetterWords.length, eightLetterWords, attributesIn);
							break;
				case 9 : 	abilitiesFinal = whichAbility(nineLetterWords.length, nineLetterWords, attributesIn);
							break;
				case 10 : 	abilitiesFinal = whichAbility(tenLetterWords.length, tenLetterWords, attributesIn);
							break;
				case 11 : 	abilitiesFinal = whichAbility(elevenLetterWords.length, elevenLetterWords, attributesIn);
							break;
				case 12 : 	return twelveLetterWords[0];
				case 13 : 	abilitiesFinal = whichAbility(thirteenLetterWords.length, thirteenLetterWords, attributesIn);
							break;
				case 14 : 	return fourteenLetterWords[0];
				default : 	System.out.println("ERROR");
							return "ERROR";
			}
			//System.out.println("abilitiesFinal " + abilitiesFinal);
			return abilitiesFinal;
		}
		if(attributesIn.contains(",")){
			multipleAttributesRoutine = true;
		}
		else{							//cards that have only one ability but its more than 1 word
			switch(x){
				case 8 : 	abilitiesFinal = multipleWords[6];
							break;
				case 9 : 	abilitiesFinal = multipleWords[0];
							break;
				case 10 : 	abilitiesFinal = multipleWords[1];
							break;
				case 11 : 	abilitiesFinal = multipleWords[9];
							break;
				case 12 :	if(attributesIn.equals(multipleWords[4])){
								abilitiesFinal = multipleWords[4];
							}
							else{
								abilitiesFinal = multipleWords[8];
							}
							break;
				case 13 : 	if(attributesIn.equals(multipleWords[3])){
								abilitiesFinal = multipleWords[3];
							}
							else if(attributesIn.equals(multipleWords[5])){
								abilitiesFinal = multipleWords[5];
							}
							else if(attributesIn.equals(multipleWords[10])){
								abilitiesFinal = multipleWords[10];
							}
							else{
								abilitiesFinal = multipleWords[7];
							}
							break;
				case 17 : 	abilitiesFinal = multipleWords[2];
							break;
				default : 	System.out.println("ERROR");
							return "ERROR";
			}
			//System.out.println("abilitiesFinal " + abilitiesFinal);
			return abilitiesFinal;
		}
		String[] breakDown = new String[x];
		int y = attributesIn.indexOf(',');
		int low = 0, high = y, index = 0, j = 0;
		temp = attributesIn.substring(low, high);
		workingString = attributesIn.substring(high+2);
		abilitiesFinal = "";
		while(index < breakDown.length){
			breakDown[index] = temp;
			//System.out.println("breakDown[index]: " + index + " : " + breakDown[index] + "hello there");
			index++;
			high = workingString.indexOf(',');
			if(high >= 0){
				temp = workingString.substring(low, high);
				workingString = workingString.substring(high+2);
			}
			else{
				temp = workingString;
				breakDown[index] = temp;
				break;
			}
		}
		for(y = 0; y < index+1; y++){
			abilitiesFinal += attributesDesignation(breakDown[y]);
			//System.out.println("abilitiesFinal " + abilitiesFinal);
			if(y < index){
				abilitiesFinal += "\n\t\t\t\t\t";
			}
		}
			//System.out.println("abilitiesFinal " + abilitiesFinal);
		return abilitiesFinal;
	}
	
	public String colourDesignation(String coloursIn){
		Scanner scan = new Scanner(System.in);
		String workingString = "";
		int x = coloursIn.length(), y = 0, i = 0, j = 0, count = 0, k = 0;
		if(x == 2){
			return coloursIn;
		}
		if(x%2 != 0){
			boolean validColour = false;
			String renter = "";
			System.out.println(this.toStringGUI());
			y = 0;
			while(!validColour && y < 5){
				System.out.println("ERROR in colours.\nRENTER colours.");
				renter = scan.nextLine();
				validColour = checkIfValidColour(renter);
				y++;
			}
			if(!validColour){
				System.out.println("Exiting the program.");
				System.exit(y);
			}
			coloursIn = renter;
			x = coloursIn.length();
		}
		int[] possibilities = {171, 151, 150, 149, 143, 141}; // WT > BU > RD > GN > NA > BK
		String[] possibileWords = {"WT", "BU", "RD", "GN", "NA", "BK"}; //WT, BU, RD, GN, NA, BK
		String[] results = new String[x/2];
		int[] resultsInt = new int[x/2];
		for(y = 0; y < x; y++){
			i += coloursIn.charAt(y);
			y++;
			i += coloursIn.charAt(y);
			for(j = 0; j < possibilities.length; j++){
				if(i == possibilities[j]){
					break;
				}
			}
			resultsInt[y/2] = i;
			i = 0;
		}
		selectionSort(resultsInt);
		while(i < resultsInt.length){
			while(resultsInt[i] != possibilities[k] && k < possibilities.length){
				k++;
			}
			i++;
			workingString += possibileWords[k];
			k = 0;
		}
		return workingString;
	}
	
	public String whichAbility(int x, String[] Words, String attributesIn){
		String temp = Words[x-1];
		while(x > 0){
			x--;
			temp = Words[x];
			if(temp.equals(attributesIn)){
				break;
			}
		}
		return Words[x];
	}
	
	public String toStringGUI(){
		String message = "\n\tCard:\nName: \t\t\t" + name + "\nType: \t\t\t" + type + "\nColour(s): \t\t" + colour + "\nConverted mana cost: \t" +
						convertedManaCost + "\nSTATS: \t\t\t" + atk + " / " + def + "\nabilities: \t\t" + attributes + "\nCollection: \t\t" + collection +
						"\nCatalog #: \t\t" + collectionNum + " / " + collectionTotal + "\n";
		return message;
	}
	
	public String toString(){
		String message = "\n\tCard:\nID Number: \t\t\t" + iD + "\nName: \t\t\t\t" + name + "\nType: \t\t\t\t" + type + "\nColour(s): \t\t\t" + colour + "\nConvt'd mana cost: \t" +
						convertedManaCost + "\nSTATS: \t\t\t\t" + atk + " / " + def + "\nabilities: \t\t\t" + attributes + "\nCollection:\t\t\t" + collection +
						"\nCatalog #: \t\t\t" + collectionNum + " / " + collectionTotal + "\n";
		return message;
	}
	
	public void sortCards(Card[] cards, int sortMode){
		int i, j, temp;
		Scanner scan = new Scanner(System.in);
		Card[] result = new Card[cards.length];
		Card workingCard;
		int[][] workingValues = new int[2][cards.length];
		System.out.println("cards.length: " + cards.length);
		switch(sortMode){
			case 1 :	for(i = 0, j = 0; j < cards.length-1; j++){
							workingValues[i][j] = cards[j].atk;
							workingValues[i+1][j] = j;
						}
						/*     Printing workingValues vertically
						for(int p = 0; p < workingValues.length; p++){
							for(int q = 0; q < workingValues[0].length; q++){
								System.out.println("workingValues["+p+"]["+q+"]: " + workingValues[p][q]);
							}
						}*/
						workingValues = modifiedSelectionSort(workingValues);
						cards = adjustCardsAfterSort(workingValues, cards);
						break;
			case 2 :	for(i = 0, j = 0; j < cards.length-1; j++){
							workingValues[i][j] = cards[j].def;
							workingValues[i+1][j] = j;
						}
						/*     Printing workingValues vertically
						for(int p = 0; p < workingValues.length; p++){
							for(int q = 0; q < workingValues[0].length; q++){
								System.out.println("workingValues["+p+"]["+q+"]: " + workingValues[p][q]);
							}
						}*/
						workingValues = modifiedSelectionSort(workingValues);
						cards = adjustCardsAfterSort(workingValues, cards);
						break;
			case 3 :	for(i = 0; i < cards.length-1; i++){  //sort by greatest difference in card stats
							temp = i;
							for(j = i+1; j < cards.length-1; j++){
								if(cards[j].compareToDIFF(cards[i]) < 0){
									temp = j;
								}
								workingCard = cards[temp];
								cards[temp] = cards[i];
								cards[i] = workingCard;
							}
						}
						break;		
			case 4 :	for(i = 0; i < cards.length-1; i++){  //sort by least difference in card stats
							temp = i;
							for(j = i+1; j < cards.length; j++){
								if(cards[j].compareToDIFF(cards[i]) > 0){
									temp = j;
								}
								//System.out.println("\ngg\n" + cards[j] + "\ngg\n" + cards[i] + "\ngg\n");
								workingCard = cards[temp];
								cards[temp] = cards[i];
								cards[i] = workingCard;
							}
						}
						break;	
			case 5 :	int[] possibilities = {171, 151, 150, 149, 143, 141}; //sort by colour WT, BU, RD, GN, NA, BL
						System.out.println("Which colour first?\n1 - WHITE\n2 - RED\n3 - GREEN\n4 - BLUE\n5 - BLACK");
						int response, key;
						try{
							response = scan.nextInt();
							key = response-1;
						}
						catch(Exception e){
							response = 0;
							key = 0;
						}
						for(int p = 0; p < possibilities.length; p++){
							for(i = 0; i < cards.length-1; i++){  //sort by colour WT, RD, GN, BU, BL
								temp = i;
								for(j = i+1; j < cards.length; j++){
									if(cards[j].compareToColour(cards[i], possibilities[key]) < 0){
										temp = j;
									}
									workingCard = cards[temp];
									cards[temp] = cards[i];
									cards[i] = workingCard;
								}
							}
							key++;
							if(key == possibilities.length){
								key = possibilities.length - key;
							}
						}
						break;
			default :   System.out.println("ERROR");
						break;		
		}
			printCollection(cards);	
	}
	
	public void statistics(Card[] cardsIn, int statMode){
		NumberFormat nf = NumberFormat.getInstance();
		Scanner scan = new Scanner(System.in);
		//basic stats
		double avg = 0;
		int n = cardsIn.length, averageMode = 0; 
		int[] workingArray = new int[n];
		Card[] cards;
		switch(statMode){
			case 1 :		System.out.println("Average of which values?\n1 --- power\n2 --- toughness\n3 --- converted mana cost");
							try{
								int x = 0;
								while((averageMode < 1 || averageMode > 10) && x < 5){
									averageMode = scan.nextInt();
									x++;
								}
								if(x == 5){
									System.out.println("choosing average of power for you.");
									averageMode = 1;
									cards = relevantCards(cardsIn, "CREATURE");
								}
							}
							catch(Exception e){
								int x = 0;
								while(x < 3){
									System.out.println("ERROR try again");
									String choice = scan.next();
									if(choice.length() == 1){
										if(choice.charAt(0) > 47 && choice.charAt(0) < 58){
											x = Integer.parseInt(choice);
										}
									}
									if(x < 3){
										x++;
									}
								}
								if(x == 3){
									System.out.println("choosing average of power for you.");
									x=1;
									averageMode = 1;
									cards = relevantCards(cardsIn, "CREATURE");
								}
								averageMode = x;
							}
							nf.setMaximumFractionDigits(4);
							switch(averageMode){
								case 1 :	cards = relevantCards(cardsIn, "CREATURE");
											for(int x = 0; x < cards.length-1; x++){
												workingArray[x] = cards[x].atk;
											}
											System.out.println("IN TERMS OF ATTACK POWER");
											avg = calcAverage(workingArray);
											break;
								case 2 :	cards = relevantCards(cardsIn, "CREATURE");
											for(int x = 0; x < cards.length-1; x++){
												workingArray[x] = cards[x].def;
											}
											System.out.println("IN TERMS OF DEFENCE TOUGHNESS");
											avg = calcAverage(workingArray);
											break;
								
								case 3 :	cards = relevantCards(cardsIn, "VALUES");
											for(int x = 0; x < cards.length-1; x++){
												workingArray[x] = cards[x].convertedManaCost;
											}
											System.out.println("IN TERMS OF CONVERTED MANA COST");
											avg = calcAverage(workingArray);
											break;
								default :   System.out.println("This functionality is not supported by this program");
											break;
							}
							System.out.println("\tDeck Average:\nn = " + n + " average: " + nf.format(avg));
							break;
			
			default :   System.out.println("This functionality is not supported by this program");
						break;
		}
	}
	
	public int compareToATK(Card cardIn){
		if(this.atk > cardIn.atk){
			return -1;
		}
		else if(this.atk < cardIn.atk){
			return 1;
		}
		return 0;
	}
	
	public int compareToDEF(Card cardIn){
		if(this.def > cardIn.def){
			return -1;
		}
		else if(this.def < cardIn.def){
			return 1;
		}
		return 0;
	}
	
	public int compareToDIFF(Card cardIn){
		if(Math.abs(this.atk - this.def) > Math.abs(cardIn.atk - cardIn.def)){
			return -1;
		}
		else if(Math.abs(this.atk - this.def) < Math.abs(cardIn.atk - cardIn.def)){
			return 1;
		}
		return 0;
	}
	
	public int compareToColour(Card cardIn, int key){
		int a = 0, b = 0;
		int[] possibilities = {171, 151, 150, 149, 143, 131}; // WT > BU > RD > GN > NA > BK
		for(int i = 0; i < 2; i++){
			a += this.colour.charAt(i);
			b += cardIn.colour.charAt(i);			
		}
		if(a == key){
			return -1;
		}
		else if(b == key){
			return 1;
		}
		return 0;
	}
	
	public void printCollection(Card[] cards){
		for(int i = 0; i < cards.length; i++){
			System.out.println("#"+(i+1)+"\n"+cards[i]);
		}
	}

	public void selectionSort(int arr[]){
        int n = arr.length;
        // One by one move boundary of unsorted subarray
        for (int i = 0; i < n-1; i++){
            // Find the minimum element in unsorted array
            int min_idx = i;
            for (int j = i+1; j < n; j++)
                if (arr[j] < arr[min_idx])
                    min_idx = j;
            // Swap the found minimum element with the first
            // element
            int temp = arr[min_idx];
            arr[min_idx] = arr[i];
            arr[i] = temp;
        }
    }
	
	public int[][] modifiedSelectionSort(int arr[][]){
        int n = arr[0].length;
        // One by one move boundary of unsorted subarray
        for (int i = 0; i < n-1; i++){
            // Find the minimum element in unsorted array
            int min_idx = i;
			int offIndex = i;
            for (int j = i+1; j < n; j++){
                if (arr[0][j] <= arr[0][min_idx]){
                    min_idx = j;
					offIndex = j;
				}
			}
            // Swap the found minimum element with the first
            // element
            int temp = arr[0][min_idx];
			int temp2 = arr[1][offIndex];
            arr[0][min_idx] = arr[0][i];
			arr[1][offIndex] = arr[1][i];
            arr[0][i] = temp;
			arr[1][i] = temp2;
        }
		/*    vertical print
		for(int i = 0; i < arr.length; i++){
			for(int j = 0; j < arr[0].length; j++){
				System.out.println("arr["+i+"]["+j+"]: " + arr[i][j]);
			}
		}*/
		//    horizontal print matrix style
		for(int i = 0; i < arr.length; i++){
			for(int j = 0; j < arr[0].length; j++){
				System.out.print(arr[i][j]+" ");
			}
			System.out.println("\n");
		}
		return arr;
    }

	public Card[] adjustCardsAfterSort(int[][] arr, Card[] deckIn){
		Card[] temp = new Card[deckIn.length];
		//System.out.println("deckIn.length: " + deckIn.length);
		for(int i = 0, j = deckIn.length-1; i < deckIn.length; i++){
				temp[i] = deckIn[arr[1][j]];
				//System.out.println("i: " + i + " arr[1][j: "+j+"]: "+ arr[1][j]);
				j--;
		}
		deckIn = temp;
		return deckIn;
	}

	public boolean checkIfValidColour(String lineIn){
		boolean isColour = false;
		int sum = 0, read;
		int[] possibilities = {171, 151, 150, 149, 143, 141}; // WT > BU > RD > GN > NA > BK
		if(lineIn != null && lineIn.length()%2 != 1){
			for(int x = 0; x < lineIn.length(); x+=2){
				for(int i = 0; i < 2; i++){
					read = lineIn.charAt(i);
					sum += read;
				}
				for(int j = 0; j < possibilities.length; j++){
					if(possibilities[j] == sum){
						isColour = true;
						if((x+2) >= lineIn.length()){
							return isColour;
						}
						else{
							sum = 0;
							isColour = false;
						}
					}
				}
			}
		}
		return isColour;
	}

	public double calcAverage(int[] deckIn){
		int sum = 0, i;
		double result;
		if(deckIn.length == 0){
			return 0;
		}
		for(i = 0; i < deckIn.length; i++){
			sum += deckIn[i];
		}
		double j = (double)i;
		result = sum/j;
		return result;
	}
	
	public static Card[] relevantCards(Card[] arrIn, String parameter){
		int arrLength = 1;
		Card[] arr = new Card[arrLength];
 		if(parameter == "VALUES"){
			for(int p = 0; p < arrIn.length-1; p++){
				if(!arrIn[p].type.contains("Token") && !arrIn[p].type.contains("Land")){
					arr[arrLength-1] = arrIn[p];
					arrLength++;
				}
				if(arr.length < p){
					Card[] temp = new Card[arrLength];
					for(int q = 0; q < arrLength-1; q++){
						temp[q] = arr[q];
					}
					arr = temp;
				}
			}
		}
		else if(parameter == "CREATURE"){
			for(int i = 0; i < arrIn.length-1; i++){
				if(arrIn[i].type.contains("Creature")){
					arr[arrLength-1] = arrIn[i];
					arrLength++;
				}
				if(arr.length < i){
					Card[] temp = new Card[arrLength];
					for(int j = 0; j < arrLength-1; j++){
						temp[j] = arr[j];
					}
					arr = temp;
				}
			}
		}
		return arr;
	}
}
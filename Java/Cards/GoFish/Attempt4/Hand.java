import java.util.Random;
import java.util.Arrays;
public class Hand{
	
	/*
	*	An array of cards that consists of 5 cards initially.
	*/
	public Card[] myHand = new Card[5];
	
	/*
	*	An array of Cards that stores player pairs during
	*	the game.
	*/
	public Card[] playerPairsLog = new Card[0];
	
	/*
	*	An array of Cards that stores AI pairs during
	*	the game.
	*/
	public Card[] aiPairsLog = new Card[0];
	
	/*
	*	An integer to store the number of cards in the 
	*	player's pair log.
	*/
	public int playerPairsLogLength = 0;

	/*
	*	An integer to store the number of cards in the 
	*	AI's pair log.
	*/
	public int aiPairsLogLength = 0;
	
	/*
	*	Constructor method that takes in a Card array from the 
	*	deck class. Sets class variable myHand to the recieved 
	*	cards.
	*	@param handIn - Card array
	*/
	public Hand(Card[] handIn){
		myHand = new Card[handIn.length];
		for(int i = 0; i < myHand.length; i++){
			myHand[i] = handIn[i];
		}
	}
	
	public boolean notASpecialIndex(int n, int[] arr){
		boolean notASpecialIndex = true;
		for(int i = 0; i < arr.length; i++){
			if(arr[i] == n){
				return false;
			}
		}
		return notASpecialIndex;
	}
	
	/*
	*
	*/
	public int detectPairs(Hand handIn, Deck deckIn){
		System.out.println("detecting pairs\n\n");
		SpecialCard workingCard = new SpecialCard(-25,-25,"MINUS25",-25,-25);
		SpecialCard[] handOfSpecialCards = new SpecialCard[handIn.myHand.length];
		int numMatchingCards = -25;
		boolean showCalc = false;
		for(int i = 0; i < handOfSpecialCards.length; i++){
			numMatchingCards = handPosses(handIn, deckIn, handIn.myHand[i].id);
			if(handIn.myHand[i].value > 1 && handIn.myHand[i].value < 11){
				workingCard = new SpecialCard(handIn.myHand[i].index ,handIn.myHand[i].value ,handIn.myHand[i].suit ,handIn.myHand[i].id ,numMatchingCards);
			}
			else{
				workingCard = new SpecialCard(handIn.myHand[i].index ,handIn.myHand[i].faceValue ,handIn.myHand[i].suit, 'm', handIn.myHand[i].id, numMatchingCards);
			}
			handOfSpecialCards[i] = workingCard;
		}
		int res = 0, threesCounter = 0;
		for(int i = 0; i < handOfSpecialCards.length; i++){
			if(handOfSpecialCards[i].numMatchingValuesInHand == 2 || handOfSpecialCards[i].numMatchingValuesInHand == 4){
				res++;
				showCalc = true;
			}
			else if(handOfSpecialCards[i].numMatchingValuesInHand == 3){
				res++;
				threesCounter++;
			}
		}
		workingCard.printCardArr(handOfSpecialCards);
		res = (((res - threesCounter) / 2) + (threesCounter / 3));
		System.out.println("\t" + res + " pairs found\n\nThreesCounter: " + threesCounter);
		int h = threesCounter;
		int[] pairIndicesFinal = new int[res*2];
		if(threesCounter > 0){
			int[][] threeOfAKindAndIndex = new int[threesCounter][2];
			threesCounter = 0;
			for(int i = 0; i < handOfSpecialCards.length; i++){
				if(handOfSpecialCards[i].numMatchingValuesInHand == 3){
					threeOfAKindAndIndex[threesCounter][0] = handOfSpecialCards[i].value;
					System.out.println("threeOfAKindAndIndex["+threesCounter+"]["+0+"]");
					threesCounter++;
				}
			}
			threesCounter = h;
			int pIFComp = 0;
			SpecialCard takenCard = new SpecialCard(-100,-100,"TAKEN",-100,-100);
			for(int i = 0; i < handOfSpecialCards.length; i++){
				if(handOfSpecialCards[i].numMatchingValuesInHand == 2 || handOfSpecialCards[i].numMatchingValuesInHand == 4){
					pairIndicesFinal[pIFComp] = handOfSpecialCards[i].id;
					pIFComp++;
					for(int j = 0; j < handOfSpecialCards.length; j++){
						if(handOfSpecialCards[j].value == handOfSpecialCards[i].value && handOfSpecialCards[j].id != handOfSpecialCards[i].id){
							pairIndicesFinal[pIFComp] = handOfSpecialCards[j].id;
							pIFComp++;
							handOfSpecialCards[i] = takenCard;
							handOfSpecialCards[j] = takenCard;
						}
					}
				}
				else if(handOfSpecialCards[i].numMatchingValuesInHand == 3){
					for(int j = 0; j < threeOfAKindAndIndex.length; j++){
						if(handOfSpecialCards[i].value == threeOfAKindAndIndex[j][0]){
							threeOfAKindAndIndex[j][1]++;
							if(threeOfAKindAndIndex[j][1] > 1){
								handOfSpecialCards[i] = takenCard;
							}
						}
					}
				}
			}		
			for(int i = 0; i < threeOfAKindAndIndex.length; i++){
				for(int j = 0; j < threeOfAKindAndIndex[i].length; j++){
					System.out.println("threeOfAKindAndIndex["+i+"]["+j+"]: " + threeOfAKindAndIndex[i][j]);
				}
			}
		}
		else if(showCalc){
			int pIFComp = 0;
			SpecialCard takenCard = new SpecialCard(-100,-100,"TAKEN",-100,-100);
			for(int i = 0; i < handOfSpecialCards.length; i++){
				if(handOfSpecialCards[i].numMatchingValuesInHand == 2 || handOfSpecialCards[i].numMatchingValuesInHand == 4){
					pairIndicesFinal[pIFComp] = handOfSpecialCards[i].id;
					pIFComp++;
					for(int j = 0; j < handOfSpecialCards.length; j++){
						if(handOfSpecialCards[j].value == handOfSpecialCards[i].value && handOfSpecialCards[j].id != handOfSpecialCards[i].id){
							pairIndicesFinal[pIFComp] = handOfSpecialCards[j].id;
							pIFComp++;
							handOfSpecialCards[i] = takenCard;
							handOfSpecialCards[j] = takenCard;
						}
					}
				}
			}
		}
		workingCard.printCardArr(handOfSpecialCards);
		int pIFComp = 0, fHACComp = 0;
		Card[] finalHandAfterCalc = new Card[handIn.myHand.length - pairIndicesFinal.length];
		for(int i = 0; i < handOfSpecialCards.length; i++){
			if(handOfSpecialCards[i].value > -1){
				finalHandAfterCalc[fHACComp] = deckIn.getCardFromId(deckIn, handIn.myHand[i].id);   //handIn.myHand[i];
				fHACComp++;
			}
			else{
				System.out.println("Removing your pair of" + handIn.myHand[i].pairRemoveStatement());
				pairIndicesFinal[pIFComp] = handIn.myHand[i].id;
				pIFComp++;
				handIn.myHand[i].index = -1; //player pair index code == -1
			}
		}
		
		
		/*
		
				if(who == 'p'){
					System.out.println("Removing your pair of" + handIn.myHand[i].pairRemoveStatement());
					deckIn.myDeck[pairIndicesFinal[temp]].index = -1; //player pair index code == -1
				}
				else if(who == 'a'){
					System.out.println("Removing AI's pair of" + handIn.myHand[i].pairRemoveStatement());
					deckIn.myDeck[pairIndicesFinal[temp]].index = -2;  //ai pair index code == -2
				}
		*/
		/*
		int res = 0, individualCounter = 1, companion = 0, keepingTrack = 0;
		int[] keepingTrackIndicies = new int[handIn.myHand.length/3];
		boolean pairDetected = false;
		boolean threeOfAKindDetected = false;
		for(int i = 0; i < keepingTrackIndicies.length; i++){
			keepingTrackIndicies[i] = 1111;
		}
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j){
					res++;
					pairDetected = true;
					individualCounter++;
					if(individualCounter > 2){
						threeOfAKindDetected = true;
						res -= 2;
						keepingTrackIndicies[keepingTrack] = workingCard.id;
						keepingTrack++;
					}
				}
			}
			individualCounter = 1;
		}
		System.out.println("\t" + res + " pairs found");
		printHand(handIn);
		int[] specialCaseIndicies = new int[keepingTrackIndicies.length];
		if(threeOfAKindDetected){
			int keepingTrackComp = 0;
			for(int i = 0; i < keepingTrackIndicies.length; i++){
				specialCaseIndicies[i] = 1111;
			}
			for(int i = 0; i < keepingTrackIndicies.length; i++){
				if(keepingTrackIndicies[i] != 1111){
					specialCaseIndicies[keepingTrackComp] = keepingTrackIndicies[i];
					keepingTrackComp++;
				}
			}
			int size = 0;
			for(int i = 0; i < keepingTrackIndicies.length; i++){
				if(specialCaseIndicies[i] == 1111){
					size = i;
					break;
				}
			}
			int[] workingSpecialCaseIndicies = new int[size];
			for(int i = 0; i < size; i++){
				workingSpecialCaseIndicies[i] = specialCaseIndicies[i];
			}
			specialCaseIndicies = workingSpecialCaseIndicies;
			if(keepingTrack > 0){
				System.out.println("\tPrinting specialCaseIndicies:");
				printARR(specialCaseIndicies);
			}
		}
		int[][] possibleValues = new int[handIn.myHand.length][4];
		int[] idValues = new int[handIn.myHand.length];
		for(int i = 0; i < possibleValues.length; i++){
			idValues[i] = handIn.myHand[i].id+1;
		}
		for(int i = 0, j = 0; i < possibleValues.length; i++, j++){
			if((idValues[j] / 13) == 0){
				possibleValues[i][0] = idValues[j]-1;
				possibleValues[i][1] = idValues[j]+12;
				possibleValues[i][2] = idValues[j]+25;
				possibleValues[i][3] = idValues[j]+38;
			}
			else if((idValues[j] / 13) == 1){
				possibleValues[i][0] = idValues[j]-14;
				possibleValues[i][1] = idValues[j]-1;
				possibleValues[i][2] = idValues[j]+12;
				possibleValues[i][3] = idValues[j]+25;
			}
			else if((idValues[j] / 13) == 2){
				possibleValues[i][0] = idValues[j]-27;
				possibleValues[i][1] = idValues[j]-14;
				possibleValues[i][2] = idValues[j]-1;
				possibleValues[i][3] = idValues[j]+12;				
			}
			else{
				possibleValues[i][0] = idValues[j]-40;
				possibleValues[i][1] = idValues[j]-27;
				possibleValues[i][2] = idValues[j]-14;
				possibleValues[i][3] = idValues[j]-1;					
			}
			for(int j = 0; j < idValues.length; j++){
				
			}
		}
		int[][] valuesAndIndicies = new int[handIn.myHand.length - (res*2)][2];
		int comp = 0, vAIComp = 0;
		printARR(idValues);
		
		for(int i = 0; i < idValues.length; i++){
			for(int j = i; j < idValues.length; j++){
				if(idValues[i] != idValues[j]  && notASpecialIndex(idValues[i], specialCaseIndicies)){
					valuesAndIndicies[vAIComp][0] = deckIn.getCardFromId(deckIn, idValues[i]).value;
					valuesAndIndicies[vAIComp][1] = idValues[i];
					System.out.println("approved: VALUE:valuesAndIndicies["+vAIComp+"][0]: " + valuesAndIndicies[vAIComp][0] + ", INDEX:valuesAndIndiciesvaluesAndIndicies["+vAIComp+"][1]: " + valuesAndIndicies[vAIComp][1]);
					vAIComp++;
					break;
				}
			}
		}
		for(int i = 0; i < idValues.length; i++){
			int target = idValues[i];
			int targetA = validateTargets(idValues, idValues[i]+13);
			int targetB = validateTargets(idValues, idValues[i]+26);
			int targetC = validateTargets(idValues, idValues[i]+39);
			int targetD = validateTargets(idValues, idValues[i]-13);
			int targetE = validateTargets(idValues, idValues[i]-26);
			int targetF = validateTargets(idValues, idValues[i]-39);
			for(int j = 0; j < idValues.length; j++){
				if(idValues[j] != target){
					if(idValues[j] == targetA){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;
					} 
					else if(idValues[j] == targetB){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
					else if(idValues[j] == targetC){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
					else if(idValues[j] == targetD){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
					else if(idValues[j] == targetE){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
					else if(idValues[j] == targetF){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
				}
			}
	}
		for(int k = 0; k < handIn.myHand.length; k++){
			int indicie1i = 101, indicie1T = 101, indicie1j;
			int indicie2i = 101, indicie2T = 101, indicie2j;
			for(int i = 0; i < possibleValues.length; i++){
				for(int j = 0; j < possibleValues[i].length; j++){
					System.out.println("possibleValues["+i+"]["+j+"]: " + possibleValues[i][j]);
					if(handIn.myHand[i].id == possibleValues[i][j]){
						indicie1i = i;
						indicie1T = possibleValues[i][j];
						indicie1j = j;
						possibleValues[i][j] = 101;
					}
				}
				for(int j = 0; j < possibleValues[i].length; j++){
					System.out.println("possibleValues["+i+"]["+j+"]: " + possibleValues[i][j]);
					if(handIn.myHand[i].id == possibleValues[i][j] && possibleValues[i][j] != indicie1T){
						indicie2i = i;
						indicie2T = possibleValues[i][j];
						indicie2j = j;
						possibleValues[i][j] = 101;
					}
				}
			}
		}
		for(int i = 0; i < possibleValues.length; i++){
			for(int j = 0; j < possibleValues[i].length; j++){
				System.out.println("possibleValues["+i+"]["+j+"]: " + possibleValues[i][j]);
			}
		}
		int res = 0, individualCounter = 1, companion = 0, keepingTrack = 0;
		int[] keepingTrackIndicies = new int[handIn.myHand.length/3];
		boolean threeOfAKindFound = false;
		boolean pairDetected = false;
		for(int i = 0; i < keepingTrackIndicies.length; i++){
			keepingTrackIndicies[i] = 1111;
		}
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j){
					res++;
					pairDetected = true;
					individualCounter++;
					if(individualCounter > 2){
						res -= 2;
						keepingTrackIndicies[keepingTrack] = workingCard.index;
						keepingTrack++;
					}
				}
			}
			individualCounter = 1;
		}
		System.out.println("\t" + res + " pairs found");
		int[][] pairIndices = new int[res*2][2];
		int timeCounter = 0;
		individualCounter = 1;
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			//System.out.println("workingCard: " + workingCard.toString());
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j  && timeCounter < 1){//&& (Arrays.binarySearch(keepingTrackIndicies, workingCard.index)) > 0){
					if(individualCounter > 1 || companion >= pairIndices.length){
						break;
					}
					timeCounter++;
					individualCounter++;
					pairIndices[companion][0] = handIn.myHand[i].value;
					System.out.println("Removing your pair of" + handIn.myHand[i].pairRemoveStatement());
					pairIndices[companion][1] = handIn.myHand[i].id+1;
					companion++;
					pairIndices[companion][0] = workingCard.value;
					pairIndices[companion][1] = workingCard.id+1;
					companion++;
					
				}
				if(timeCounter > 1){
					break;
				}
			}
			timeCounter = 0;
			individualCounter = 1;
		}
		
		System.out.println("Printing pairIndices:\n\n");
		for(int i = 0; i < pairIndices.length; i++){
			for(int j = 0; j < pairIndices[i].length; j++){
				System.out.println("pairIndices["+i+"]["+j+"]: " + pairIndices[i][j]);
			}
		}*/
		
		System.out.println("\n\n");/*
		if(res > 0){
			pairIndicesFinal = removeThreeOfAKinds(valuesAndIndicies, res);
		}
		System.out.println("\n\n");
		char who = 'p';
		if(pairDetected){
			removePairs(handIn, pairIndicesFinal, deckIn, who);
		}
		playerPairsLog = updatePairsLog(playerPairsLog, res, pairIndicesFinal, deckIn);
		printPlayerLog();*/
		printHand(handIn);
		System.out.println("\n\n");
		workingCard.printCardArr(finalHandAfterCalc);
		playerPairsLog = updatePairsLog(playerPairsLog, res, pairIndicesFinal, deckIn, playerPairsLogLength);
		printPlayerLog();
		//deckIn.printDeck();
		//deckIn.updateDeck(handIn);
		return res;
	}
	
	/*
	*
	*/
	public int detectPairsNoPrinting(Hand handIn, Deck deckIn){
		/*
		System.out.println("detecting pairs\n\n");
		int res = 0, individualCounter = 1, companion = 0, keepingTrack = 0;
		int[] keepingTrackIndicies = new int[handIn.myHand.length/3];
		boolean threeOfAKindFound = false;
		boolean pairDetected = false;
		for(int i = 0; i < keepingTrackIndicies.length; i++){
			keepingTrackIndicies[i] = 1111;
		}
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j){
					res++;
					pairDetected = true;
					individualCounter++;
					if(individualCounter > 2){
						res -= 2;
						keepingTrackIndicies[keepingTrack] = workingCard.index;
						keepingTrack++;
					}
				}
			}
			individualCounter = 1;
		}
		System.out.println("\t" + res + " pairs found");
		int[][] pairIndices = new int[res*2][2];
		int timeCounter = 0;
		individualCounter = 1;
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			//System.out.println("workingCard: " + workingCard.toString());
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j  && timeCounter < 1){//&& (Arrays.binarySearch(keepingTrackIndicies, workingCard.index)) > 0){
					if(individualCounter > 1 || companion >= pairIndices.length){
						break;
					}
					timeCounter++;
					individualCounter++;
					pairIndices[companion][0] = handIn.myHand[i].value;
					System.out.println("Removing your pair of" + handIn.myHand[i].pairRemoveStatement());
					pairIndices[companion][1] = handIn.myHand[i].id+1;
					companion++;
					pairIndices[companion][0] = workingCard.value;
					pairIndices[companion][1] = workingCard.id+1;
					companion++;
					
				}
				if(timeCounter > 1){
					break;
				}
			}
			timeCounter = 0;
			individualCounter = 1;
		}
		
		/*System.out.println("Printing pairIndices:\n\n");
		for(int i = 0; i < pairIndices.length; i++){
			for(int j = 0; j < pairIndices[i].length; j++){
				System.out.println("pairIndices["+i+"]["+j+"]: " + pairIndices[i][j]);
			}
		}
		System.out.println("\n\n");
		int[] pairIndicesFinal = new int[res*2];
		if(res > 0){
			pairIndicesFinal = removeThreeOfAKindsNoPrinting(pairIndices, res);
		}
		System.out.println("\n\n");
		char who = 'a';
		if(pairDetected){
			removePairs(handIn, pairIndicesFinal, deckIn, who);
		}
		aiPairsLog = updatePairsLog(aiPairsLog, res, pairIndicesFinal, deckIn);
		printAILog();
		//printHand(handIn);
		//deckIn.printDeck();
		//deckIn.updateDeck(handIn);
		return res;*/
		System.out.println("detecting pairs No Printing\n\n");
		SpecialCard workingCard = new SpecialCard(-25,-25,"MINUS25",-25,-25);
		SpecialCard[] handOfSpecialCards = new SpecialCard[handIn.myHand.length];
		int numMatchingCards = -25;
		boolean showCalc = false;
		for(int i = 0; i < handOfSpecialCards.length; i++){
			numMatchingCards = handPosses(handIn, deckIn, handIn.myHand[i].id);
			if(handIn.myHand[i].value > 1 && handIn.myHand[i].value < 11){
				workingCard = new SpecialCard(handIn.myHand[i].index ,handIn.myHand[i].value ,handIn.myHand[i].suit ,handIn.myHand[i].id ,numMatchingCards);
			}
			else{
				workingCard = new SpecialCard(handIn.myHand[i].index ,handIn.myHand[i].faceValue ,handIn.myHand[i].suit, 'm', handIn.myHand[i].id, numMatchingCards);
			}
			handOfSpecialCards[i] = workingCard;
		}
		int res = 0, threesCounter = 0;
		for(int i = 0; i < handOfSpecialCards.length; i++){
			if(handOfSpecialCards[i].numMatchingValuesInHand == 2 || handOfSpecialCards[i].numMatchingValuesInHand == 4){
				res++;
				showCalc = true;
			}
			else if(handOfSpecialCards[i].numMatchingValuesInHand == 3){
				res++;
				threesCounter++;
			}
		}
		workingCard.printCardArr(handOfSpecialCards);
		res = (((res - threesCounter) / 2) + (threesCounter / 3));
		System.out.println("\t" + res + " pairs found\n\nThreesCounter: " + threesCounter);
		int h = threesCounter;
		int[] pairIndicesFinal = new int[res*2];
		if(threesCounter > 0){
			int[][] threeOfAKindAndIndex = new int[threesCounter][2];
			threesCounter = 0;
			for(int i = 0; i < handOfSpecialCards.length; i++){
				if(handOfSpecialCards[i].numMatchingValuesInHand == 3){
					threeOfAKindAndIndex[threesCounter][0] = handOfSpecialCards[i].value;
					System.out.println("threeOfAKindAndIndex["+threesCounter+"]["+0+"]");
					threesCounter++;
				}
			}
			threesCounter = h;
			int pIFComp = 0;
			SpecialCard takenCard = new SpecialCard(-100,-100,"TAKEN",-100,-100);
			for(int i = 0; i < handOfSpecialCards.length; i++){
				if(handOfSpecialCards[i].numMatchingValuesInHand == 2 || handOfSpecialCards[i].numMatchingValuesInHand == 4){
					pairIndicesFinal[pIFComp] = handOfSpecialCards[i].id;
					pIFComp++;
					for(int j = 0; j < handOfSpecialCards.length; j++){
						if(handOfSpecialCards[j].value == handOfSpecialCards[i].value && handOfSpecialCards[j].id != handOfSpecialCards[i].id){
							pairIndicesFinal[pIFComp] = handOfSpecialCards[j].id;
							pIFComp++;
							handOfSpecialCards[i] = takenCard;
							handOfSpecialCards[j] = takenCard;
						}
					}
				}
				else if(handOfSpecialCards[i].numMatchingValuesInHand == 3){
					for(int j = 0; j < threeOfAKindAndIndex.length; j++){
						if(handOfSpecialCards[i].value == threeOfAKindAndIndex[j][0]){
							threeOfAKindAndIndex[j][1]++;
							if(threeOfAKindAndIndex[j][1] > 1){
								handOfSpecialCards[i] = takenCard;
							}
						}
					}
				}
			}		
			for(int i = 0; i < threeOfAKindAndIndex.length; i++){
				for(int j = 0; j < threeOfAKindAndIndex[i].length; j++){
					System.out.println("threeOfAKindAndIndex["+i+"]["+j+"]: " + threeOfAKindAndIndex[i][j]);
				}
			}
		}
		else if(showCalc){
			int pIFComp = 0;
			SpecialCard takenCard = new SpecialCard(-100,-100,"TAKEN",-100,-100);
			for(int i = 0; i < handOfSpecialCards.length; i++){
				if(handOfSpecialCards[i].numMatchingValuesInHand == 2 || handOfSpecialCards[i].numMatchingValuesInHand == 4){
					pairIndicesFinal[pIFComp] = handOfSpecialCards[i].id;
					pIFComp++;
					for(int j = 0; j < handOfSpecialCards.length; j++){
						if(handOfSpecialCards[j].value == handOfSpecialCards[i].value && handOfSpecialCards[j].id != handOfSpecialCards[i].id){
							pairIndicesFinal[pIFComp] = handOfSpecialCards[j].id;
							pIFComp++;
							handOfSpecialCards[i] = takenCard;
							handOfSpecialCards[j] = takenCard;
						}
					}
				}
			}
		}
		workingCard.printCardArr(handOfSpecialCards);
		int pIFComp = 0, fHACComp = 0;
		Card[] finalHandAfterCalc = new Card[handIn.myHand.length - pairIndicesFinal.length];
		for(int i = 0; i < handOfSpecialCards.length; i++){
			if(handOfSpecialCards[i].value > -1){
				finalHandAfterCalc[fHACComp] = deckIn.getCardFromId(deckIn, handIn.myHand[i].id);   //handIn.myHand[i];
				fHACComp++;
			}
			else{
				System.out.println("Removing AI's pair of" + handIn.myHand[i].pairRemoveStatement());
				pairIndicesFinal[pIFComp] = handIn.myHand[i].id;
				pIFComp++;
				handIn.myHand[i].index = -2; //AI pair index code == -2
			}
		}
		
		
		/*
		
				if(who == 'p'){
					System.out.println("Removing your pair of" + handIn.myHand[i].pairRemoveStatement());
					deckIn.myDeck[pairIndicesFinal[temp]].index = -1; //player pair index code == -1
				}
				else if(who == 'a'){
					System.out.println("Removing AI's pair of" + handIn.myHand[i].pairRemoveStatement());
					deckIn.myDeck[pairIndicesFinal[temp]].index = -2;  //ai pair index code == -2
				}
		*/
		/*
		int res = 0, individualCounter = 1, companion = 0, keepingTrack = 0;
		int[] keepingTrackIndicies = new int[handIn.myHand.length/3];
		boolean pairDetected = false;
		boolean threeOfAKindDetected = false;
		for(int i = 0; i < keepingTrackIndicies.length; i++){
			keepingTrackIndicies[i] = 1111;
		}
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j){
					res++;
					pairDetected = true;
					individualCounter++;
					if(individualCounter > 2){
						threeOfAKindDetected = true;
						res -= 2;
						keepingTrackIndicies[keepingTrack] = workingCard.id;
						keepingTrack++;
					}
				}
			}
			individualCounter = 1;
		}
		System.out.println("\t" + res + " pairs found");
		printHand(handIn);
		int[] specialCaseIndicies = new int[keepingTrackIndicies.length];
		if(threeOfAKindDetected){
			int keepingTrackComp = 0;
			for(int i = 0; i < keepingTrackIndicies.length; i++){
				specialCaseIndicies[i] = 1111;
			}
			for(int i = 0; i < keepingTrackIndicies.length; i++){
				if(keepingTrackIndicies[i] != 1111){
					specialCaseIndicies[keepingTrackComp] = keepingTrackIndicies[i];
					keepingTrackComp++;
				}
			}
			int size = 0;
			for(int i = 0; i < keepingTrackIndicies.length; i++){
				if(specialCaseIndicies[i] == 1111){
					size = i;
					break;
				}
			}
			int[] workingSpecialCaseIndicies = new int[size];
			for(int i = 0; i < size; i++){
				workingSpecialCaseIndicies[i] = specialCaseIndicies[i];
			}
			specialCaseIndicies = workingSpecialCaseIndicies;
			if(keepingTrack > 0){
				System.out.println("\tPrinting specialCaseIndicies:");
				printARR(specialCaseIndicies);
			}
		}
		int[][] possibleValues = new int[handIn.myHand.length][4];
		int[] idValues = new int[handIn.myHand.length];
		for(int i = 0; i < possibleValues.length; i++){
			idValues[i] = handIn.myHand[i].id+1;
		}
		for(int i = 0, j = 0; i < possibleValues.length; i++, j++){
			if((idValues[j] / 13) == 0){
				possibleValues[i][0] = idValues[j]-1;
				possibleValues[i][1] = idValues[j]+12;
				possibleValues[i][2] = idValues[j]+25;
				possibleValues[i][3] = idValues[j]+38;
			}
			else if((idValues[j] / 13) == 1){
				possibleValues[i][0] = idValues[j]-14;
				possibleValues[i][1] = idValues[j]-1;
				possibleValues[i][2] = idValues[j]+12;
				possibleValues[i][3] = idValues[j]+25;
			}
			else if((idValues[j] / 13) == 2){
				possibleValues[i][0] = idValues[j]-27;
				possibleValues[i][1] = idValues[j]-14;
				possibleValues[i][2] = idValues[j]-1;
				possibleValues[i][3] = idValues[j]+12;				
			}
			else{
				possibleValues[i][0] = idValues[j]-40;
				possibleValues[i][1] = idValues[j]-27;
				possibleValues[i][2] = idValues[j]-14;
				possibleValues[i][3] = idValues[j]-1;					
			}
			for(int j = 0; j < idValues.length; j++){
				
			}
		}
		int[][] valuesAndIndicies = new int[handIn.myHand.length - (res*2)][2];
		int comp = 0, vAIComp = 0;
		printARR(idValues);
		
		for(int i = 0; i < idValues.length; i++){
			for(int j = i; j < idValues.length; j++){
				if(idValues[i] != idValues[j]  && notASpecialIndex(idValues[i], specialCaseIndicies)){
					valuesAndIndicies[vAIComp][0] = deckIn.getCardFromId(deckIn, idValues[i]).value;
					valuesAndIndicies[vAIComp][1] = idValues[i];
					System.out.println("approved: VALUE:valuesAndIndicies["+vAIComp+"][0]: " + valuesAndIndicies[vAIComp][0] + ", INDEX:valuesAndIndiciesvaluesAndIndicies["+vAIComp+"][1]: " + valuesAndIndicies[vAIComp][1]);
					vAIComp++;
					break;
				}
			}
		}
		for(int i = 0; i < idValues.length; i++){
			int target = idValues[i];
			int targetA = validateTargets(idValues, idValues[i]+13);
			int targetB = validateTargets(idValues, idValues[i]+26);
			int targetC = validateTargets(idValues, idValues[i]+39);
			int targetD = validateTargets(idValues, idValues[i]-13);
			int targetE = validateTargets(idValues, idValues[i]-26);
			int targetF = validateTargets(idValues, idValues[i]-39);
			for(int j = 0; j < idValues.length; j++){
				if(idValues[j] != target){
					if(idValues[j] == targetA){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;
					} 
					else if(idValues[j] == targetB){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
					else if(idValues[j] == targetC){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
					else if(idValues[j] == targetD){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
					else if(idValues[j] == targetE){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
					else if(idValues[j] == targetF){
						valuesAndIndicies[comp][1] = idValues[j];
						valuesAndIndicies[comp][0] = deckIn.getCardFromId(deckIn, idValues[j]).value;
						comp++;
						idValues[j] = -1111;						
					}
				}
			}
	}
		for(int k = 0; k < handIn.myHand.length; k++){
			int indicie1i = 101, indicie1T = 101, indicie1j;
			int indicie2i = 101, indicie2T = 101, indicie2j;
			for(int i = 0; i < possibleValues.length; i++){
				for(int j = 0; j < possibleValues[i].length; j++){
					System.out.println("possibleValues["+i+"]["+j+"]: " + possibleValues[i][j]);
					if(handIn.myHand[i].id == possibleValues[i][j]){
						indicie1i = i;
						indicie1T = possibleValues[i][j];
						indicie1j = j;
						possibleValues[i][j] = 101;
					}
				}
				for(int j = 0; j < possibleValues[i].length; j++){
					System.out.println("possibleValues["+i+"]["+j+"]: " + possibleValues[i][j]);
					if(handIn.myHand[i].id == possibleValues[i][j] && possibleValues[i][j] != indicie1T){
						indicie2i = i;
						indicie2T = possibleValues[i][j];
						indicie2j = j;
						possibleValues[i][j] = 101;
					}
				}
			}
		}
		for(int i = 0; i < possibleValues.length; i++){
			for(int j = 0; j < possibleValues[i].length; j++){
				System.out.println("possibleValues["+i+"]["+j+"]: " + possibleValues[i][j]);
			}
		}
		int res = 0, individualCounter = 1, companion = 0, keepingTrack = 0;
		int[] keepingTrackIndicies = new int[handIn.myHand.length/3];
		boolean threeOfAKindFound = false;
		boolean pairDetected = false;
		for(int i = 0; i < keepingTrackIndicies.length; i++){
			keepingTrackIndicies[i] = 1111;
		}
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j){
					res++;
					pairDetected = true;
					individualCounter++;
					if(individualCounter > 2){
						res -= 2;
						keepingTrackIndicies[keepingTrack] = workingCard.index;
						keepingTrack++;
					}
				}
			}
			individualCounter = 1;
		}
		System.out.println("\t" + res + " pairs found");
		int[][] pairIndices = new int[res*2][2];
		int timeCounter = 0;
		individualCounter = 1;
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			//System.out.println("workingCard: " + workingCard.toString());
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j  && timeCounter < 1){//&& (Arrays.binarySearch(keepingTrackIndicies, workingCard.index)) > 0){
					if(individualCounter > 1 || companion >= pairIndices.length){
						break;
					}
					timeCounter++;
					individualCounter++;
					pairIndices[companion][0] = handIn.myHand[i].value;
					System.out.println("Removing your pair of" + handIn.myHand[i].pairRemoveStatement());
					pairIndices[companion][1] = handIn.myHand[i].id+1;
					companion++;
					pairIndices[companion][0] = workingCard.value;
					pairIndices[companion][1] = workingCard.id+1;
					companion++;
					
				}
				if(timeCounter > 1){
					break;
				}
			}
			timeCounter = 0;
			individualCounter = 1;
		}
		
		System.out.println("Printing pairIndices:\n\n");
		for(int i = 0; i < pairIndices.length; i++){
			for(int j = 0; j < pairIndices[i].length; j++){
				System.out.println("pairIndices["+i+"]["+j+"]: " + pairIndices[i][j]);
			}
		}*/
		
		System.out.println("\n\n");/*
		if(res > 0){
			pairIndicesFinal = removeThreeOfAKinds(valuesAndIndicies, res);
		}
		System.out.println("\n\n");
		char who = 'p';
		if(pairDetected){
			removePairs(handIn, pairIndicesFinal, deckIn, who);
		}
		playerPairsLog = updatePairsLog(playerPairsLog, res, pairIndicesFinal, deckIn);
		printPlayerLog();*/
		printHand(handIn);
		System.out.println("\n\n");
		workingCard.printCardArr(finalHandAfterCalc);
		aiPairsLog = updatePairsLog(aiPairsLog, res, pairIndicesFinal, deckIn, aiPairsLogLength);
		printAILog();
		//deckIn.printDeck();
		//deckIn.updateDeck(handIn);
		return res;
	}
	
	/*
	*
	*/
	public int[] removeThreeOfAKinds(int[][] arr, int numPairs){ //arr[x][0] = values, arr[x][1] = indicies
		System.out.println("removing 3 of a kinds");
		for(int i = 0; i < arr.length; i++){
			for(int j = 0; j < arr[i].length; j++){
				System.out.println("arr["+i+"]["+j+"]: " + arr[i][j]);
			}
		}
		int[] res = new int[numPairs*2];
		int[] safeIndicies = new int[numPairs];
		int size = arr.length, target = 0, counter = 1, safeIndex = 0, safeComp = 0, resComp = 0;
		boolean isThreeofAKind = false;
		int[][] numberOfOccurences = new int[2][13];
		int num = 1;
		for(int i = 0; i < 13; i++){
			numberOfOccurences[0][i] = i+1;
			for(int j = 0; j < arr.length; j++){
				if(arr[j][0] == i){
					numberOfOccurences[1][i] = num;
					num++;
					if(num == 3){
						isThreeofAKind = true;
						safeIndicies[safeComp] = arr[j][0];
						safeComp++;
					}
				}
			}
			num = 0;
			isThreeofAKind = false;
		}
		//System.out.println("\n\nPrinting safeIndicies array: \n\n");
		//printARR(safeIndicies);
		for(int i = 0; i < arr.length; i++){
			for(int j = 0; j < safeIndicies.length; j++){
				if(safeIndicies[j] != arr[i][1]){
					res[resComp] = (arr[i][1])-1;
					resComp++;
					break;
				}
			}
		}
		return res;
	}
	
	/*
	*
	*/
	public int[] removeThreeOfAKindsNoPrinting(int[][] arr, int numPairs){
		System.out.println("removing 3 of a kinds No Printing");
		for(int i = 0; i < arr.length; i++){
			for(int j = 0; j < arr[i].length; j++){
				System.out.println("arr["+i+"]["+j+"]: " + arr[i][j]);
			}
		}
		int[] res = new int[numPairs*2];
		int[] safeIndicies = new int[numPairs];
		int size = arr.length, target = 0, counter = 1, safeIndex = 0, safeComp = 0, resComp = 0;
		boolean isThreeofAKind = false;
		int[][] numberOfOccurences = new int[2][13];
		int num = 1;
		for(int i = 0; i < 13; i++){
			numberOfOccurences[0][i] = i+1;
			for(int j = 0; j < arr.length; j++){
				if(arr[j][0] == i){
					numberOfOccurences[1][i] = num;
					num++;
					if(num == 3){
						isThreeofAKind = true;
						safeIndicies[safeComp] = arr[j][0];
						safeComp++;
					}
				}
			}
			num = 0;
			isThreeofAKind = false;
		}
		//System.out.println("\n\nPrinting safeIndicies array: \n\n");
		//printARR(safeIndicies);
		for(int i = 0; i < arr.length; i++){
			for(int j = 0; j < safeIndicies.length; j++){
				if(safeIndicies[j] != arr[i][1]){
					res[resComp] = (arr[i][1])-1;
					resComp++;
					break;
				}
			}
		}
		return res;
	}

	/*
	*
	*/
	public void removePairs(Hand handIn, int[] pairIndicesFinal, Deck deckIn, char who){
		printHand(handIn);
		System.out.println("printing pairIndicesFinal array");
		printARR(pairIndicesFinal);
		Card[] arr = new Card[handIn.myHand.length-pairIndicesFinal.length];
		boolean success = true;
		int temp = 0, numMatchingCardsInHand = 1, counter = 0;
		for(int i = 0, j = 0; i < handIn.myHand.length; i++){
			for(int k = 0; k < pairIndicesFinal.length; k++){
				numMatchingCardsInHand = handPosses(handIn, deckIn, pairIndicesFinal[k]);
				if(handIn.myHand[i].id == pairIndicesFinal[k]){
					counter++;
					success = false;
					temp = k;
					break;
				}
			}
			if((!success || numMatchingCardsInHand == 2 || numMatchingCardsInHand ==4) && counter < 3){
				int preRemoval = 0;
				counter = 0;
				if(who == 'p'){
					System.out.println("Removing your pair of" + handIn.myHand[i].pairRemoveStatement());
					deckIn.myDeck[pairIndicesFinal[temp]].index = -1; //player pair index code == -1
				}
				else if(who == 'a'){
					System.out.println("Removing AI's pair of" + handIn.myHand[i].pairRemoveStatement());
					deckIn.myDeck[pairIndicesFinal[temp]].index = -2;  //ai pair index code == -2
				}
			}
			success = true;
			counter = 0;
		}
		int[] workingArr = new int[pairIndicesFinal.length];
		for(int p = 0; p < workingArr.length; p++){
			workingArr[p] = pairIndicesFinal[p];
		}
		for(int i = 0, k = 0; i < handIn.myHand.length; i++){
			//System.out.println("comparing: \nhandIn.myHand["+i+"] : " + handIn.myHand[i]);
			if(handIn.myHand[i].index != -1 && handIn.myHand[i].index != -2){
				arr[k] = handIn.myHand[i];
				//System.out.println("APPROVED: " + arr[k]);
				k++;
			}
		}
		System.out.println("\n\nPrinting Hand:\n\n");
		handIn.myHand = arr;
		printHand(handIn);
	}
	
	public int validateTargets(int[] arr, int n){
		if(n > 52 || n < 1){
			return -101;
		}
		for(int i = 0; i < arr.length; i++){
			if(arr[i] == n){
				System.out.println("validating index: "+ (n-1));
				return n-1;
			}
		}
		return -101;
	}
	
	/*
	*
	*/
	public void printHand(Hand handIn){
		for(int l = 0; l < handIn.myHand.length; l++){
			System.out.println(handIn.myHand[l]);
		}
		System.out.println("\n\n");
	}
	
	public void printARR(int[] arr){
		System.out.println("PRINTING");
		for(int l = 0; l < arr.length; l++){
			/*if(arr[l] == 1111){
				System.out.println("\n\n\tERROR\n\n");
			}
			else{*/
				System.out.println("\t" + arr[l]);
			/*}*/
		}
		System.out.println("\n\n");
	}
	
	/*
	*
	*/
	public void drawCard(Deck deckIn, Hand handIn){
		Card[] workingCard = new Card[handIn.myHand.length+1];
		Card newCard = deckIn.drawNewCards(deckIn, 1);
		for(int i = 0; i < workingCard.length; i++){
			if(i < handIn.myHand.length){
				workingCard[i] = handIn.myHand[i];
			}
			else{
				workingCard[i] = newCard;
			}
		}
		handIn.myHand = workingCard;
		printHand(handIn);
	}
	
	
	public Card[] updatePairsLog(Card[] log, int num, int[] arrIndicies, Deck deckIn, int logLength){
		System.out.println("\n\n\tUpdating Given Pair Log");
		if(num < 1){
			return log;
		}
		if(log.length == 0){
			Card[] res = new Card[num*2];
			//System.out.println("created card array [res] of size: " + res.length+"\n");
			for(int o = 0; o < res.length; o++){
				res[o] = deckIn.getCardFromId(deckIn, (arrIndicies[o]));
				//System.out.println("UPDTPRS: res["+o+"]: " + res[o] + ", arrIndicies["+o+"]: " + (arrIndicies[o]));		
			}
			return res;
		}
		else{
			int[] res = new int[log.length + (num*2)];
			for(int i = 0; i < log.length; i++){
				res[i] = log[i].id;
			}
			for(int i = log.length, j = 0; i < (arrIndicies.length + log.length); i++, j++){
				res[i] = arrIndicies[j];
			}
			Card[] finalArray = new Card[res.length];
			//System.out.println("created card array [finalArray] of size: " + finalArray.length + "\nprinting res array of paired card ids: \n");
			printARR(res);
			for(int i = 0, j = 0; i < deckIn.myDeck.length; i++){
				for(int k = 0; k < res.length; k++){
					if(deckIn.myDeck[i].id  == res[k]){
						//System.out.println("\n\t\tYou're telling me that these two cards are a pair:\n\t" + deckIn.myDeck[i].id + " : " + res[k]);
						finalArray[j] = deckIn.getCardFromId(deckIn, res[k]);
						break;
					}
				}
			}
			/*System.out.println("\n\n\tPrinting Pairs array:\n\n");
			for(int k = 0; k < res.length; k++){
				System.out.println(finalArray[k]);
			}*/
			System.out.println("\ndone updating\n");
			return finalArray;
		}
	}
	
	public int handPosses(Hand handIn, Deck deckIn, int targetIndex){
		int numTimes = 0;
		for(int i = 0; i < handIn.myHand.length; i++){
			if(handIn.myHand[i].value == deckIn.getCardFromId(deckIn, targetIndex).value){
				numTimes++;
			}
		}
		//System.out.println("Found " + numTimes + " occurences of " + targetIndex);
		return numTimes;
	}
	
	public void printPlayerLog(){
		System.out.println("\n\n\tPrinting Player Pairs Log");
		for(int i = 0; i < playerPairsLog.length; i++){
			System.out.println("playerPairsLog["+i+"]: " + playerPairsLog[i]);
		}
		System.out.println("\n\n");
	}
	
	public void printAILog(){
		System.out.println("\n\n\tPrinting AI Pairs Log");
		for(int i = 0; i < aiPairsLog.length; i++){
			System.out.println("AIPairsLog["+i+"]: " + aiPairsLog[i]);
		}
		System.out.println("\n\n");
	}
}
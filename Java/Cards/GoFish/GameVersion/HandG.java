/*
*
*
*
*/

import java.util.Random;
import java.util.Arrays;
public class HandG{
	
	/**
	*	An array of cards that consists of 5 cards initially.
	*/
	public CardG[] myHand = new CardG[5];
	
	/**
	*	An array of Cards that stores player pairs during
	*	the game.
	*/
	public CardG[] playerPairsLog = new CardG[0];
	
	/**
	*	An array of Cards that stores AI pairs during
	*	the game.
	*/
	public CardG[] aiPairsLog = new CardG[0];
	
	/**
	*	An integer to store the number of cards in the 
	*	player's pair log.
	*/
	public int playerPairsLogLength = 0;

	/**
	*	An integer to store the number of cards in the 
	*	AI's pair log.
	*/
	public int aiPairsLogLength = 0;
	
	/**
	*	Constructor method that takes in a Card array from the 
	*	deck class. Sets class variable myHand to the recieved 
	*	cards.
	*	@param handIn - Card array
	*/
	public HandG(CardG[] handIn){
		myHand = new CardG[handIn.length];
		for(int i = 0; i < myHand.length; i++){
			myHand[i] = handIn[i];
		}
	}
	
	/*
	*
	*/
	public int detectPairs(HandG handIn, DeckG deckIn){
		System.out.println("detecting pairs\n\n");
		SpecialCardG workingCard = new SpecialCardG(-25,-25,"MINUS25",-25,-25);
		SpecialCardG[] handOfSpecialCards = new SpecialCardG[handIn.myHand.length];
		int numMatchingCards = -25;
		boolean showCalc = false;
		for(int i = 0; i < handOfSpecialCards.length; i++){
			numMatchingCards = handPosses(handIn, deckIn, handIn.myHand[i].id);
			if(handIn.myHand[i].value > 1 && handIn.myHand[i].value < 11){
				workingCard = new SpecialCardG(handIn.myHand[i].index ,handIn.myHand[i].value ,handIn.myHand[i].suit ,handIn.myHand[i].id ,numMatchingCards);
			}
			else{
				workingCard = new SpecialCardG(handIn.myHand[i].index ,handIn.myHand[i].faceValue ,handIn.myHand[i].suit, 'm', handIn.myHand[i].id, numMatchingCards);
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
		System.out.println("\t" + res + " pairs found");
		int h = threesCounter;
		int[] pairIndicesFinal = new int[res*2];
		if(threesCounter > 0){
			int[][] threeOfAKindAndIndex = new int[threesCounter][2];
			threesCounter = 0;
			for(int i = 0; i < handOfSpecialCards.length; i++){
				if(handOfSpecialCards[i].numMatchingValuesInHand == 3){
					threeOfAKindAndIndex[threesCounter][0] = handOfSpecialCards[i].value;
					threesCounter++;
				}
			}
			threesCounter = h;
			int pIFComp = 0;
			SpecialCardG takenCard = new SpecialCardG(-100,-100,"TAKEN",-100,-100);
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
		}
		else if(showCalc){
			int pIFComp = 0;
			SpecialCardG takenCard = new SpecialCardG(-100,-100,"TAKEN",-100,-100);
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
		//workingCard.printCardArr(handOfSpecialCards);
		int pIFComp = 0, fHACComp = 0;
		CardG[] finalHandAfterCalc = new CardG[handIn.myHand.length - pairIndicesFinal.length];
		for(int i = 0; i < handOfSpecialCards.length; i++){
			if(handOfSpecialCards[i].value > -1){
				finalHandAfterCalc[fHACComp] = deckIn.getCardFromId(deckIn, handIn.myHand[i].id);   //handIn.myHand[i];
				fHACComp++;
			}
			else{
				pairIndicesFinal[pIFComp] = handIn.myHand[i].id;
				pIFComp++;
				handIn.myHand[i].index = -1; //player pair index code == -1
			}
		}
		handIn.myHand = finalHandAfterCalc;
		printHand(handIn);
		/*workingCard.printCardArr(finalHandAfterCalc);
		System.out.println("\nPrinting pairIndicesFinal: \n");
		printARR(pairIndicesFinal);
		System.out.println("\n\n");*/
		playerPairsLog = updatePairsLog(playerPairsLog, res, pairIndicesFinal, deckIn, playerPairsLogLength);
		playerPairsLogLength += res*2;
		printPlayerLog();
		//deckIn.printDeck();
		//deckIn.updateDeck(handIn);
		return res;
	}
	
	/*
	*
	*/
	public int detectPairsNoPrinting(HandG handIn, DeckG deckIn){
		System.out.println("detecting pairs No Printing\n\n");
		SpecialCardG workingCard = new SpecialCardG(-25,-25,"MINUS25",-25,-25);
		SpecialCardG[] handOfSpecialCards = new SpecialCardG[handIn.myHand.length];
		int numMatchingCards = -25;
		boolean showCalc = false;
		for(int i = 0; i < handOfSpecialCards.length; i++){
			numMatchingCards = handPosses(handIn, deckIn, handIn.myHand[i].id);
			if(handIn.myHand[i].value > 1 && handIn.myHand[i].value < 11){
				workingCard = new SpecialCardG(handIn.myHand[i].index ,handIn.myHand[i].value ,handIn.myHand[i].suit ,handIn.myHand[i].id ,numMatchingCards);
			}
			else{
				workingCard = new SpecialCardG(handIn.myHand[i].index ,handIn.myHand[i].faceValue ,handIn.myHand[i].suit, 'm', handIn.myHand[i].id, numMatchingCards);
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
		System.out.println("\t" + res + " pairs found");
		int h = threesCounter;
		int[] pairIndicesFinal = new int[res*2];
		if(threesCounter > 0){
			int[][] threeOfAKindAndIndex = new int[threesCounter][2];
			threesCounter = 0;
			for(int i = 0; i < handOfSpecialCards.length; i++){
				if(handOfSpecialCards[i].numMatchingValuesInHand == 3){
					threeOfAKindAndIndex[threesCounter][0] = handOfSpecialCards[i].value;
					threesCounter++;
				}
			}
			threesCounter = h;
			int pIFComp = 0;
			SpecialCardG takenCard = new SpecialCardG(-100,-100,"TAKEN",-100,-100);
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
		}
		else if(showCalc){
			int pIFComp = 0;
			SpecialCardG takenCard = new SpecialCardG(-100,-100,"TAKEN",-100,-100);
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
		CardG[] finalHandAfterCalc = new CardG[handIn.myHand.length - pairIndicesFinal.length];
		for(int i = 0; i < handOfSpecialCards.length; i++){
			if(handOfSpecialCards[i].value > -1){
				finalHandAfterCalc[fHACComp] = deckIn.getCardFromId(deckIn, handIn.myHand[i].id);   //handIn.myHand[i];
				fHACComp++;
			}
			else{
				pairIndicesFinal[pIFComp] = handIn.myHand[i].id;
				pIFComp++;
				handIn.myHand[i].index = -2; //AI pair index code == -2
			}
		}
		handIn.myHand = finalHandAfterCalc;
		System.out.println("\n\n");
		printHand(handIn);
		/*workingCard.printCardArr(finalHandAfterCalc);
		System.out.println("\nPrinting pairIndicesFinal: \n");
		printARR(pairIndicesFinal);
		System.out.println("\n\n");*/
		aiPairsLog = updatePairsLog(aiPairsLog, res, pairIndicesFinal, deckIn, aiPairsLogLength);
		aiPairsLogLength += res*2;
		printAILog();
		//deckIn.printDeck();
		//deckIn.updateDeck(handIn);
		return res;
	}
	
	/*
	*
	*/
	public void printHand(HandG handIn){
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
	public void drawCard(DeckG deckIn, HandG handIn, char mode){
		CardG[] workingCard = new CardG[handIn.myHand.length+1];
		CardG newCard = deckIn.drawNewCards(deckIn, 1);
		for(int i = 0; i < workingCard.length; i++){
			if(i < handIn.myHand.length){
				workingCard[i] = handIn.myHand[i];
			}
			else{
				workingCard[i] = newCard;
			}
		}
		handIn.myHand = workingCard;
		//printHand(handIn);
		if(mode == 112){
			detectPairs(handIn, deckIn);
		}
		else{
			detectPairsNoPrinting(handIn, deckIn);
		}
	}
	
	
	public CardG[] updatePairsLog(CardG[] log, int num, int[] arrIndicies, DeckG deckIn, int logLength){
		System.out.println("\n\n\tUpdating Given Pair Log");
		if(num < 1){
			return log;
		}
		if(log.length == 0){
			CardG[] res = new CardG[num*2];
			for(int o = 0; o < res.length; o++){
				res[o] = deckIn.getCardFromId(deckIn, (arrIndicies[o]));	
			}
			res = sortPairLog(log, logLength, num*2, res);
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
			CardG[] finalArray = new CardG[res.length];
			for(int i = 0, j = 0; i < deckIn.myDeck.length; i++){
				for(int k = 0; k < res.length; k++){
					if(deckIn.myDeck[i].id  == res[k]){
						finalArray[j] = deckIn.getCardFromId(deckIn, res[k]);
						break;
					}
				}
			}
			finalArray = sortPairLog(log, logLength, num*2, finalArray);
			System.out.println("\ndone updating\n");
			return finalArray;
		}
	}
	
	/**
	*	Method sorts an array of cards given from updatePairsLog().
	*	All cards have a pair, and starting from the beginning,
	*	the algorithm searches for the it's pair and calls swap()
	*	to switch them.
	*	@param log			-  A card array, either playerPairsLog or aiPairsLog.
	*	@param logLength	-  An integer, either playerPairsLogLength or aiPairsLogLength.
	*	@param numPairs		-  An integer representing the number of pairs in the hand.
	*	@param pairsArray	-  A card array containing an unsorted group of paired cards.
	*/
	public CardG[] sortPairLog(CardG[] log, int logLength, int numPairs, CardG[] pairsArray){
		int n = logLength + numPairs, h = 0;
		int target;
		while(h < numPairs){
			h++;
			for(int i = 0; i < pairsArray.length-1; i++){
				target = pairsArray[i].value;
				for(int j = i+1; j < pairsArray.length; j++){
					if(target == pairsArray[j].value){
						swap(pairsArray, i+1, j);
					}
				}
			}
			h++;
		}
		for(int i = 0; i < pairsArray.length; i += 2){
			System.out.println("\n\tREMOVING pair of:\n\t->" + pairsArray[i].pairRemoveStatement());
		}
		CardG[] res = new CardG[n];
		int pAComp = 0;
		for(int i = 0; i < n; i++){
			if(i < logLength){
				res[i] = log[i];
			}
			else{
				res[i] = pairsArray[pAComp];
				pAComp++;
			}
		}
		return res;
	}
	
	/**
	*	Method swaps the positions of two cards in an array.
	*	@param arr  	-  A card array representing all pairs.
	*	@param first  	-  the first index we wish to swap.
	*	@param second  	-  the second index we wish to swap.
	*/
	public void swap(CardG[] arr, int first, int second){
		CardG temp = arr[first];
		arr[first] = arr[second];
		arr[second] = temp;
	}
	
	/**
	*	Method counts how many cards have a matching value
	*	within the given hand.
	*	@param handIn  		-  A given hand object.
	*	@param deckIn  		-  A given Deck object.
	*	@param targetIndex  -  An integer representing the current
	*						   card that we want to match.
	*	@return numTimes 	-  An integer counter of the number of 
	*						   matching cards.
	*/
	public int handPosses(HandG handIn, DeckG deckIn, int targetIndex){
		int numTimes = 0;
		for(int i = 0; i < handIn.myHand.length; i++){
			if(handIn.myHand[i].value == deckIn.getCardFromId(deckIn, targetIndex).value){
				numTimes++;
			}
		}
		//System.out.println("Found " + numTimes + " occurences of " + targetIndex);
		return numTimes;
	}
	
	/**
	*	Method prints the current contents of the player
	*	pairs log.
	*/
	public void printPlayerLog(){
		System.out.println("\n\n\tPrinting Player Pairs Log");
		for(int i = 0; i < playerPairsLog.length; i++){
			System.out.println("playerPairsLog["+i+"]:  " + playerPairsLog[i]);
		}
		System.out.println("\n\n");
	}
	
	/**
	*	Method prints the current contents of the player
	*	pairs log.
	*/
	public void printAILog(){
		System.out.println("\n\n\tPrinting AI Pairs Log");
		for(int i = 0; i < aiPairsLog.length; i++){
			System.out.println("AIPairsLog["+i+"]:  " + aiPairsLog[i]);
		}
		System.out.println("\n\n");
	}
}
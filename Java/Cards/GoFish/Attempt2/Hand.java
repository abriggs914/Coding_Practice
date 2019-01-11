import java.util.Random;
public class Hand{
	
	public Card[] myHand = new Card[5];
	public Hand(Card[] handIn){
		myHand = new Card[handIn.length];
		for(int i = 0; i < myHand.length; i++){
			myHand[i] = handIn[i];
		}
	}
	
	public int detectPairs(Hand handIn, Deck deckIn){
		System.out.println("detecting pairs\n\n");
		int res = 0, individualCounter = 1, companion = 0;
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j){
					res++;
					individualCounter++;
					if(individualCounter > 2){
						res -= 2;
					}
				}
			}
			individualCounter = 1;
		}
		System.out.println(res + " pairs found");
		int[][] pairIndices = new int[res*2][2];
		
		for(int j = 0; j < handIn.myHand.length; j++){
			Card workingCard = handIn.myHand[j];
			//System.out.println("workingCard: " + workingCard.toString());
			for(int i = j; i < handIn.myHand.length; i++){
				if(handIn.myHand[i].value == workingCard.value && i != j){
					//pairingCards(handIn, deckIn, j, i);
					//res++;
					if(individualCounter > 2 || companion >= pairIndices.length){
						//System.out.println("individualCounter: " + individualCounter);
						//res -= 2;
						break;
					}
					individualCounter++;
					pairIndices[companion][0] = handIn.myHand[i].value;
					System.out.println("Removing your pair of" + handIn.myHand[i].pairRemoveStatement());
					pairIndices[companion][1] = handIn.myHand[i].index;
					companion++;
					pairIndices[companion][0] = workingCard.value;
					//System.out.println(handIn.myHand[i].pairRemoveStatement());
					pairIndices[companion][1] = workingCard.index;
					companion++;
					
				}
			}
			individualCounter = 1;
		}
		/*for(int i = 0; i < pairIndices.length; i++){
			for(int j = 0; j < pairIndices[i].length; j++){
				System.out.println("pairIndices["+i+"]["+j+"]: " + pairIndices[i][j]);
			}
		}*/
		//printHand(handIn);
		int[] pairIndicesFinal = new int[res*2];
		if(res > 0){
			pairIndicesFinal = removeThreeOfAKinds(pairIndices, res);
			//System.out.println("res > 0");
			//printARR(pairIndicesFinal);
		}
			//printARR(pairIndicesFinal);
		System.out.println("\n\n");
		removePairs(handIn, pairIndicesFinal);
		printHand(handIn);
		return res;
	}
	
	public int[] removeThreeOfAKinds(int[][] arr, int numPairs){
		//System.out.println("removing 3 of a kinds");
		int[] res = new int[numPairs*2];
		int[] safeIndicies = new int[numPairs];
		int size = arr.length, target = 0, counter = 0, safeIndex = 0, safeComp = 0, resComp = 0;
		boolean isThreeofAKind = false;
		for(int i = 0; i < size; i++){
			target = arr[i][0];
			//System.out.println("target: " + target + ", i: " + i);
			for(int j = i; j < 1; j++){
				if(arr[i][j] == target && i != j){
					counter++;
					if(counter == 3){
						//System.out.println("Counter == 3");
						safeIndex = arr[i][1];
						safeIndicies[safeComp] = safeIndex;
						safeComp++;
						int y = safeComp-1;
						//System.out.println("safeIndices["+(y)+"]: " + safeIndicies[safeComp-1]);
					}
				}
			}
			counter = 0;
		}
		
		for(int i = 0; i < arr.length; i++){
			for(int j = 0; j < safeIndicies.length; j++){
				if(safeIndicies[j] != arr[i][1]){
					res[resComp] = arr[i][1];
					resComp++;
					break;
				}
			}
		}
		return res;
	}
	
	/*public void removeCurrentPairs(Hand handIn, Deck deckIn, int numPairs){
		System.out.println("replaceCurrentPairs");
		if(numPairs == 0){
			return;
		}
		Card[] arr = new Card[handIn.myHand.length];
		Card[] arrFinal = new Card[handIn.myHand.length - (numPairs * 2)];
		Card takenCard = new Card(100, 100, "TAKEN");
		Card specialCard = new Card(100, 100, "SPECIAL");
		int[] pairIndices = new int[numPairs*2];
		boolean covered = false;
		int num = 0, temp = 0, coveredCounter = 1;
		for(int i = 0; i < pairIndices.length; i++){
			pairIndices[i] = 101;
		}
		int currValue = 0, companion = 0, counter = 0, posses = 0, specialIndex = 0;
		printARR(pairIndices);
		int[] threeOfAKind = new int[handIn.myHand.length];
		int threeOfAKindComp = 0;
		for(int i = 0; i < handIn.myHand.length; i++){
			currValue = handIn.myHand[i].value;
			posses = handPosses(handIn, currValue);
			if(posses == 3){
				num = currValue;
				threeOfAKind[threeOfAKindComp] = i;
				threeOfAKindComp++;
				covered = true;
				temp = i;
				System.out.println("\n\n\n\n\n\n\n\n\n\nPOSSES == 3\n\n\n\n\n\n\n\n\n\n\n");
				//System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
				counter++;
				System.out.println("companion: " + companion + ", i: " + i + ", posses: " + posses);
				specialCard = new Card(handIn.myHand[i].index, currValue, handIn.myHand[i].suit);
				specialIndex = i;
				//notAlreadyCovered(handIn, currValue, pairIndices, posses);
			}
			for(int j = i; j < handIn.myHand.length; j++){
				if(handIn.myHand[j].value == currValue && i != j && notAlreadyCovered(handIn, currValue, pairIndices, posses)){
					counter++;
					System.out.println("companion: " + companion + ", i: " + i + ", j: " + j + ", posses: " + posses);
					pairIndices[companion] = i;
					companion++;
					pairIndices[companion] = j;
					companion++;
					if(!covered){
						coveredCounter++;
					}
				}
			}
			if(counter == 3){
				counter = 0;
			}
		}
		boolean skip = false;
		companion = 0;
		int a = 0, b = 0, comp1 = 0, ta = 0, tb = 0;
		printARR(pairIndices);
		for(int i = 0; i < pairIndices.length; i += 2){
			if(a == 101 || b == 101){
				if(covered){
					System.out.println("covered this one");
					ta = a;
					tb = b;
				}
			}
			a = pairIndices[i];
			b = pairIndices[i+1];
			int[][] safeIndicesArr = new int[2][1];
			int[][] workingSafeIndicesArr = safeIndices(threeOfAKind, numPairs, deckIn, handIn);
			safeIndicesArr[0][0] = workingSafeIndicesArr[0][0];
			safeIndicesArr[1][0] = workingSafeIndicesArr[1][0];
			if(covered){
				a = safeIndicesArr[0][0];
				b = safeIndicesArr[1][0];
				System.out.println("safeIndex1: " + a + ", safeIndex2: " + b);
				System.out.println("removing your pair of: " + num);
				arr[companion] = specialCard;
				covered = false;
				for(int j = 0; j < handIn.myHand.length; j++){
					if(j != a && j != b){
						arr[companion] = handIn.myHand[j];
						System.out.println("arr.length: " + arr.length + ", arr[" + companion + "]: " + arr[companion]);
					}
					else{
						arr[companion] = takenCard;
						System.out.println("arr.length: " + arr.length + ", arr[" + companion + "]: " + arr[companion]);
					}
					if(i == a || i == b){
						arr[companion] = specialCard;
					}
					//System.out.println("arr[" + i + "]: " + arr[j]);
					companion++;
				}
			}
			else{
				if(a > handIn.myHand.length){
					System.out.println("1010101010101010101101101101010110110101011");
				}
				else{
					System.out.println("removing your pair of: " + handIn.myHand[a].pairRemoveStatement());
				
					for(int j = 0; j < handIn.myHand.length; j++){
						if(j != a && j != b){
							arr[companion] = handIn.myHand[j];
							System.out.println("arr.length: " + arr.length + ", arr[" + companion + "]: " + arr[companion]);
						}
						else{
							arr[companion] = takenCard;
							System.out.println("arr.length: " + arr.length + ", arr[" + companion + "]: " + arr[companion]);
						}
						//System.out.println("arr[" + i + "]: " + arr[j]);
						companion++;
						if(j == a){
							for(int k = 0; k < handIn.myHand.length; k++){
								if(k == b && j != k){
									skip = true;
								}
							}
					}
					handIn.myHand = arr;
					companion = 0;
				}
			}
		}
		
		
		for(int i = 0, j = 0; i < arr.length; i++){
			System.out.println("arr.length: " + arr.length + ", arr[" + i + "]: " + arr[i]);
			if(arr[i].index != 101 && arr[i].index != 100){
				arrFinal[j] = arr[i];
				//System.out.println("arrFinal[" + j + "]: " + arrFinal[j]);
				j++;
				if(j == arrFinal.length){
					break;
				}
			}
		}
		handIn.myHand = arr;//Final;
		printARR(pairIndices);
		printHand(handIn);
	}*/
	
	/*public int[][] safeIndices(int[] threeOfAKind, int numPairs, Deck deckIn, Hand handIn){
		int[][] res = new int[numPairs*2][1];
		int[] workingArr = threeOfAKind;
		int x = numPairs, y = 0, safeIndex1 = 0, safeIndex2 = 1;
		//while(x > 0){
			y = workingArr[0];
			for(int i = 0; i < workingArr.length; i++){
				if(workingArr[i] != y){
					safeIndex2 = workingArr[i];
					break;
				}
			}
			res[0][0] = getCardFromValue(deckIn, y);
			res[1][0] = getCardFromValue(deckIn, safeIndex2);
		//}
		return res;
	}*/
	
	
	public void removePairs(Hand handIn, int[] pairIndicesFinal){
		Card[] arr = new Card[handIn.myHand.length-pairIndicesFinal.length];
		boolean success = true;
		for(int i = 0, j = 0; i < handIn.myHand.length; i++){
			for(int k = 0; k < pairIndicesFinal.length; k++){
				//System.out.println("Pair index: " + pairIndicesFinal[k]);
				if(handIn.myHand[i].index == pairIndicesFinal[k]){
					success = false;
					//break;
				}
			}
			if(success){
				arr[j] = handIn.myHand[i];
				//System.out.println("myHand: " + handIn.myHand[i]);
				//System.out.println("arr: " + arr[j]);
				j++;
			}
			success = true;
		}
		handIn.myHand = arr;
	}
	
	/*public int getCardFromValue(Deck deckIn, int num){
		int i = 0;
		for(i = 0; i < 52; i++){
			if(deckIn.myDeck[i].value == num){
				return deckIn.myDeck[i].index;
			}
		}
		i = 0;
		return deckIn.myDeck[i].index;
	}*/
	
	/*public boolean notAlreadyCovered(Hand handIn, int currValue, int[] pairIndices, int posses){
		if(posses % 2 == 0 || posses == 1){
				System.out.println("result: true");
			return true;
		}
		else if(posses == 3){
			int h = 0;
			for(int i = 0; i < pairIndices.length; i++){
				int g = pairIndices[i];
				if(g != 101){
					if(handIn.myHand[g].value == currValue){
						h++;
					}
				}
				if(g == 101 && posses == 3){
					return false;
				}
			}
			if(h == 0){
				//System.out.println("result: true");
				return true;
			}
			else{
				//System.out.println("result: false");
				return false;
			}
		}
		return true;
	}*/
	
	/*public int handPosses(Hand handIn, int currValue){
		int res = 0;
		for(int i = 0; i < handIn.myHand.length; i++){
			if(currValue == handIn.myHand[i].value){
				res++;
			}
		}
		return res;
	}*/
	
	public void printHand(Hand handIn){
		for(int l = 0; l < handIn.myHand.length; l++){
			System.out.println(handIn.myHand[l]);
		}
		System.out.println("\n\n");
	}
	
	public void printARR(int[] arr){
		System.out.println("PRINTING");
		for(int l = 0; l < arr.length; l++){
			System.out.println("\t" + arr[l]);
		}
		System.out.println("\n\n");
	}
}
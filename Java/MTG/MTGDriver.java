/**
Java Main for MTG Program.
Avery Briggs 3471065
June 2018
The text file required to run this program is a file with MTG cards info line by line:
The Locust God, creature, BU, 4, 6, 6, Not sure, 139, 199, true, Flying, Haste, Fear, First Strike
NAME, TYPE, COLOUR. CVTDMANACOST, ATK, DEF, COLLECTION, NUMINCOLLECTION, TOTALCOLLECTION, ABILITIES?, IF(T)-> ATTRIBUTES
*/
import java.util.Scanner;
import java.io.*;
import java.io.FileReader;
import java.io.BufferedReader;
//import java.

public class MTGDriver extends Throwable{
	
	static String[] iDs = new String[1];
	static int count = 0;
	public static void main(String[] args){
		
		/////////////Input file init. variables////////////////
		String iD, name, attributes, colour, collection, type;
		int iDNum=0, atk, def, convertedManaCost, collectionNum, collectionTotal;
		boolean abilities;
		Card[] myCollection = new Card[1];
		Card firstCard;
		Card[] myWorkingCollection = new Card[1];
		///////////////////////////////////////////////////////
		if(args.length < 1){
			System.out.println("Please retry with a valid text file.");
			return;
		}
		else{
			FileReader fr;
			BufferedReader br;
			String lineIn, workingString;
			int count = 0, workingInt, checker = 0;
			Card temp, bareCard;
			int userSortChoice;
			Scanner scan;
			try{
				fr = new FileReader(args[0]);
				br = new BufferedReader(fr);
				lineIn = br.readLine(); 
				while(lineIn != null){
					System.out.println(lineIn);
					scan = new Scanner(lineIn);
					scan.useDelimiter(",");
					name = scan.next();
					workingString = scan.next();
					type = workingString.substring(1, workingString.length());
					checker = name.length() + workingString.length();
					workingString = scan.next();
					checker += workingString.length();
					colour = workingString.substring(1, workingString.length());
					workingString = scan.next();
					checker += workingString.length();
					convertedManaCost = Integer.parseInt(workingString.substring(1, workingString.length()));
					workingString = scan.next();
					checker += workingString.length();
					atk = Integer.parseInt(workingString.substring(1, workingString.length()));
					workingString = scan.next();
					checker += workingString.length();
					def = Integer.parseInt(workingString.substring(1, workingString.length()));
					workingString = scan.next();
					checker += workingString.length();
					collection = workingString.substring(1, workingString.length());
					workingString = scan.next();
					checker += workingString.length();
					collectionNum = Integer.parseInt(workingString.substring(1, workingString.length()));
					workingString = scan.next();
					checker += workingString.length();
					collectionTotal = Integer.parseInt(workingString.substring(1, workingString.length()));
					workingString = scan.next();
					checker += workingString.length();
					workingInt = (workingString.substring(1, workingString.length())).charAt(0);
					if(workingInt == 't'){
						abilities = true;
						checker +=4;
					}
					else{
						abilities = false;
						checker +=5;
					}					
					checker += workingString.length();
					if(abilities){
						workingString = lineIn.substring(checker+1, lineIn.length());
						attributes = workingString.substring(1, workingString.length());
						//System.out.println("hey"+attributes+"hey");
					}
					else{
						attributes = "";
					}
					iDNum++;
					bareCard = new Card(name, type, colour, convertedManaCost, atk, def, collection, collectionNum, collectionTotal, abilities, attributes);
					String idColour = bareCard.colour;
					iD = generateID(iDNum, idColour);
					temp = new Card(iD, name, type, bareCard.colour, convertedManaCost, atk, def, collection, collectionNum, collectionTotal, abilities, bareCard.attributes);
					myCollection[count] = temp;
					count++;
					lineIn = br.readLine();
					if(lineIn == null){
						br.close();
						fr.close();
					}
					else if(count == myCollection.length){
						int y = myCollection.length;
						Card[] transferArray = new Card[y+1];
						for(int x = 0; x < y; x++){
							transferArray[x] = myCollection[x];
						}
						myCollection = transferArray;
					}
				}
			}
			catch(Exception e){
				System.out.println("ERROR\nEXCEPTION\n");
				e.printStackTrace();
			}
		}
		if(myCollection.length > 0){
			int userSortChoice = 0, userStatChoice = 0;
			Scanner scan = new Scanner(System.in);
			firstCard = myCollection[myCollection.length-1];
			try{
				System.out.println("\nPlease select a method for sorting:\n1 --- By strongest to weakest in power.\n"+
									"2 --- By strongest to weakest in toughness\n3 --- By greatest to least difference in power and toughness");
				userSortChoice = scan.nextInt();
			}
			catch(Exception e){
				boolean tryagain = true;
				int count = 0;
				while(tryagain){
					Scanner insc = new Scanner(System.in);
					userSortChoice = 0;
					try{
							System.out.println("\nPlease select a method for sorting:\n1 --- By strongest to weakest in power.\n"+
											"2 --- By strongest to weakest in toughness.\n3 --- By greatest to least difference in power and toughness.");
							userSortChoice = insc.nextInt();
							if(userSortChoice > 0 && userSortChoice < 4){
								tryagain = false;
								break;
							}
					}
					catch(Exception ex){
						count++;
						if(count > 3){
							tryagain = false;
							break;
						}
					}
				}
				if(tryagain){
					System.out.println("\nPlease try again later.");
					System.exit(1);
				}
			}
				myWorkingCollection = relevantCards(myCollection, "CREATURE");
				firstCard.sortCards(myWorkingCollection, userSortChoice);
			try{
				Scanner sacn = new Scanner(System.in);
				System.out.println("\nPlease select a statistic to view:\n1 --- Average.\n");
				userStatChoice = sacn.nextInt();
			}
			catch(Exception e){
				boolean tryagain = true;
				int count = 0;
				while(tryagain){
					Scanner insc = new Scanner(System.in);
					userStatChoice = 0;
					try{
							System.out.println("\nPlease select a statistic to view:\n1 --- Average.\n");
							userStatChoice = insc.nextInt();
							if(userStatChoice > 0 && userStatChoice < 4){
								tryagain = false;
								break;
							}
					}
					catch(Exception ex){
						count++;
						if(count > 3){
							tryagain = false;
							break;
						}
					}
				}
				if(tryagain){
					System.out.println("\nPlease try again later.");
					System.exit(1);
				}
			}
			firstCard.statistics(myCollection, userStatChoice);
			IndexedCollection res = new IndexedCollection(myCollection);
		}
		/*for(int y = 0; y < iDs.length-1; y++){
			System.out.println(iDs[y]);
		}*/
	}
	
	public static String generateID(int iDNum, String idColour){
		String result = generateIDHelper(idColour);
		//System.out.println("BEFORE: " + result);
		if((iDNum / 10000) == 0){
			result += "0";
		}
		if((iDNum / 1000) == 0){
			result += "0";
		}
		if((iDNum / 100) == 0){
			result += "0";
		}
		if((iDNum / 10) == 0){
			result += "0";
		}
		result += Integer.toString(iDNum);
		//System.out.println(result);
		iDs[count] = result;
		count++;
		if(count == iDs.length){
			String[] tempString = new String[iDs.length+1];
			for(int y = 0; y < iDs.length; y++){
				tempString[y] = iDs[y];
			}
			iDs = tempString;
		}
		return result;
	}
	
	public static String generateIDHelper(String colour){
		int[] possibilities = {171, 151, 150, 149, 143, 141}; // WT > BU > RD > GN > NA > BK
		String result = "";
		int n = colour.length(), num = 0;
		if(n == 2){
			for(int x = 0; x < n; x++){
				num += colour.charAt(x);
			}
			for(int x = 0; x < possibilities.length; x++){
				if(num == possibilities[x]){
					result += "1";
				}
				else{
					result += "0";
				}
			}
		}
		else{
			boolean finished = false;
			int m = 0, i = 0, j = 0;
			int colours[] = new int[n/2];
			while(!finished){
				while(m < n){
					i = m;
					num = 0;
					for(int x = 0; x < 2; x++){
						num += colour.charAt(x+i);
					}
					System.out.println("num: " + num);
					colours[m/2] = num;
					m+=2;
				}
				selectionSort(colours);
				for(int f = 0; f < possibilities.length; f++){
					if(colours[j] == possibilities[f]){
						result += "1";
						if(j < colours.length-1){
							j++;
						}
					}
					else{
						result += "0";
					}
				}
				finished = true;
			}
		}
		return result;
	}
	
	public static void selectionSort(int arr[]){
        int n = arr.length;
        // One by one move boundary of unsorted subarray
        for (int i = 0; i < n-1; i++){
            // Find the minimum element in unsorted array
            int min_idx = i;
            for (int j = i+1; j < n; j++)
                if (arr[j] > arr[min_idx])
                    min_idx = j;
            // Swap the found minimum element with the first
            // element
            int temp = arr[min_idx];
            arr[min_idx] = arr[i];
            arr[i] = temp;
        }
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
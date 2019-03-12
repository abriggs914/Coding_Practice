/*
* Java program to parse all yugioh
* cards in the combinations.txt file.
* Uses the Card class to store each
* card's data. Program can produce
* a list of possible combinations.
*
* March 2019
* Avery Briggs
* 3471065
*/

import java.io.FileInputStream;
import java.util.Scanner;
import java.util.ArrayList;

public class CardIndexer{

  public static String file = "./combinations.txt";
  public static Scanner scan, tokenizer;
  public static Card[] cardsList = new Card[722];
  public static Card[][] combos = new Card[722][722];
  public static ArrayList<Card> myHand = new ArrayList<Card>();
  public static ArrayList<Card> myBoard = new ArrayList<Card>();

  public static void main(String[] args) {
    try{
      scan = new Scanner(new FileInputStream(file));
      String line = scan.nextLine();
      Card temp;
      int j = 0;
      while(scan.hasNext() && line != null){
        //System.out.println(line);
        tokenizer = new Scanner(line);
        if(!line.equals("-------------------------------------------------------------------------------")){
          //System.out.println("next: " + ((tokenizer.next().equals("+") || tokenizer.next().equals("="))? "yes" : "no"));
          String checkLine = tokenizer.next();
          if(!(checkLine.equals("+") || checkLine.equals("="))){
            temp = lineToCard(line);
            cardsList[j] = temp;
            j++;
          }
        }
        line = scan.nextLine();
      }
      initCombosTable();
      scan = new Scanner(new FileInputStream(file));
      int rowId = 0, colId = 0;
      while(scan.hasNext() && !(line = scan.nextLine()).equals(null)){
        if(!line.equals("-------------------------------------------------------------------------------")){
          //System.out.println("next: " + ((tokenizer.next().equals("+") || tokenizer.next().equals("="))? "yes" : "no"));
          tokenizer = new Scanner(line);
          String checkLine = tokenizer.next();
          //System.out.println(line);
          if(checkLine.equals("+")){  // identifier found (card2)
           //|| checkLine.equals("="))){
            //temp = lineToCard(line);
            //cardsList[j] = temp;
            //j++;
            //System.out.println("checkLine: " + checkLine);//+ " tokenizer.next(): " + tokenizer.next());
            colId = Integer.parseInt(tokenizer.next());
            //System.out.println("colId: " + colId);
          }
          else if(checkLine.equals("=")){ // resutlt of combo

            Card temp1 = lineToCard(line.substring(1));
          //System.out.println("colId: " + colId + " rowId: " + rowId + " temp: " + temp1);
            combos[rowId][colId] = temp1;
          }
          else{ // identifier found (card1)
              rowId = Integer.parseInt(checkLine);
          }
          //j++;
        }
        //line = scan.nextLine();
      }
      /*System.out.println(combos[719-1][0]);
      System.out.println(combos[0][712-1]);
      System.out.println(combos[719][712]);
      System.out.println(combos[715-1][0]);
      System.out.println(combos[0][103-1]);
      System.out.println(combos[715][103]);*/
      int[] currDeck = {2,16,16,31,31,45,45,85,89,97,97,124,127,131,150,213,254,272,304,332,334,336,337,349,349,366,367,400,408,415,463,473,482,512,567,651,652,690,712,714};
      Card psychoPuppet = combos[715-1][0];
      Card babyDragon = combos[4-1][0];
      String suSk = "Summoned Skull";
      /*System.out.println("cardVal: " + psychoPuppet);
      //System.out.println(possibleFusionPartners(psychoPuppet));
      System.out.println("cardVal: " + babyDragon);
      //System.out.println(possibleFusionPartners(babyDragon));
      Card summonedSkull = getCardFromName(suSk);
      System.out.println("cardVal: " + summonedSkull);
      ArrayList<Card> suSkFusions = getFusions(summonedSkull);
      System.out.println(suSkFusions.size());
      //ArrayList<Card> hand = genRandomHand();
      */
      /*
        Implement a draw() method to do this in less typing
      */
      // draw("Emperor of the Land and Sea", 'h');
      // draw("Thousand Dragon", 'h');
      // draw("Ancient Tool", 'h');
      // draw("Umi", 'h');
      // draw("Dragon Zombie", 'h');
      // draw("Raigeki", 'h');
      // draw("Mystical Elf", 'h');
      // draw("Jirai Gumo", 'h');
      // draw("Electric Snake", 'h');
      draw("Mechanicalchacer", 'h');
      // draw("Octoberser", 'h');
      // draw("Emperor of the Land and Sea", 'h');
      // draw("Labyrinth Wall", 'h');
      // draw("Cannon Soldier", 'h');
      draw("Koumori Dragon", 'h');
      // draw("Pragtical", 'h');
      // draw("Mystical Elf", 'h');
      // draw("Oscillo Hero #2", 'h');
      // draw("Catapult Turtle", 'h');
      // draw("Ancient Tool", 'h');
      // draw("Mavelus", 'h');
      // draw("Firewing Pegasus", 'h');
      // draw("Dragon Zombie", 'h');
      // draw("King of Yamimakai", 'h');
      // draw("Time Wizard", 'h');
      draw("Time Wizard", 'b');
      // draw("Raigeki", 'h');
      // draw("Spellbinding Circle", 'h');
      // draw("Axe of Despair", 'h');
      // draw("Mountain", 'h');
      // draw("Aqua Madoor", 'h');
      // draw("The Immortal of Thunder", 'h');
      // draw("Darkworld Thorns", 'h');
      // draw("Giant Mech-soldier", 'h');
      // draw("Twin-headed Thunder Dragon", 'h');
      // draw("Meteor Dragon", 'h');
      // draw("Mystical Elf", 'h');
      // draw("Akihiron", 'h');
      // draw("Vermillion Sparrow", 'h');
      // draw("Ansatsu", 'h');
      // draw("Crimson Sunbird", 'h');
      // draw("Kaminarikozou", 'h');
      // draw("Yami", 'h');
      draw("Embryonic Beast", 'h');
      draw("LaLa Li-oon", 'h');
      // draw("Skullbird", 'h');
      System.out.println();
      System.out.println(myHand);
      System.out.println();
      System.out.println("hand.size(): " + myHand.size());
      System.out.println("COMBOS AVAILABLE");
      ArrayList<Card> handCombos = new ArrayList<Card>();
      ArrayList<Card> tempHand = new ArrayList<Card>();
      tempHand = myHand;
      tempHand.addAll(myBoard);
      handCombos = fusionInHand(tempHand);
      int handNumCombos = handCombos.size() / 3;
      System.out.println("combos in hand : " + handNumCombos);
      printCombosInHand(handCombos);
      //printCombos();

      /*System.out.println(currDeck.length);
      System.out.println(deckFromIds(currDeck));
      System.out.println(fusionInHand(deckFromIds(currDeck)));
      System.out.println("\n\n\n");
      ArrayList<Card> tHTDFusions = getFusions(getCardFromName("Twin-headed Thunder Dragon"));
      */
      // ArrayList<Card> abc =  getFusions(getCardFromName("Red-eyes B. Dragon"));
      // printGetFusions(abc);
      /*System.out.println("j: " + j);
      for(int x = 0; x < cardsList.length; x++){
        System.out.println(cardsList[x].toString());
      }*/
    }
      catch(Exception e){
        e.printStackTrace();
      }
  }

  public static void draw(String cardName, char hORb) throws CardException{
    if(hORb == 'h'){
      myHand.add(getCardFromName(cardName));
    }
    else if(hORb == 'b'){
      myBoard.add(getCardFromName(cardName));
    }
    else{
      throw new CardException("hey");
    }
  }

  public static void printGetFusions(ArrayList<Card> a){
    for(int i = 0; i < a.size(); i++){
      if(i % 2 == 0){
        System.out.print(a.get(i) + " + ");
      }
      else{
        System.out.println(a.get(i));
      }
    }
  }

  public static void printCombosInHand(ArrayList<Card> arr){
    for(int i = 0; i < arr.size(); i += 3){
      printOneCombo(arr.get(i), arr.get(i+1), arr.get(i+2));
    }
  }

  public static int[] merge(int[] arr, int l, int m, int r){
    int nLeft = m - l + 1;
    int nRight = r - m;
    int i = 0, j = 0, k;
    int[] left = new int[nLeft];
    int[] right = new int[nRight];
    for(i = 0; i < nLeft; i++){
      left[i] = arr[l + i];
    }
    for(j = 0; j < nRight; j++){
      right[j] = arr[m + 1 + j];
    }
    i = 0;
    j = 0;
    k = l;
    while(i < nLeft && j < nRight){
      if(left[i] <= right[j]){
        arr[k] = left[i];
        i++;
      }
      else{
        arr[k] = right[j];
        j++;
      }
      k++;
    }
    while(i < nLeft){
      arr[k] = left[i];
      i++;
      k++;
    }
    while(j < nRight){
      arr[k] = right[j];
      j++;
      k++;
    }
    return arr;
  }

  public static int[] removeDuplicates(int[] arr){
    sort(arr);
		int c = 1;
		int[] b = new int[arr.length];
		if(arr.length <= 1){
		    return arr;
		}
		int i, j = arr[0];
		b[0] = arr[0];
		for(i = 1; i < arr.length; i++){
		    if(arr[i] == j){
		    }
		    else{
		        b[c-1] = j;
		        j = arr[i];
		        c++;
		    }
		    if(i == arr.length-1){
		        b[c-1] = j;
		    }
		}
		return b;
	}

  public static int[] mergeSort(int[] arr, int l, int r){
	   if(l < r){
	      int m = (l + r)/2;
			arr = mergeSort(arr, l, m);
			arr = mergeSort(arr , m + 1, r);
			arr = merge(arr, l, m, r);
		}
    return arr;
	}

  public static int[] sort(int[] arr){
	   int n = arr.length;
	   arr = mergeSort(arr, 0, n - 1);
    return arr;
	}

  public static int SumCharVals(String line){
    int sum = 0;
    for(int j = 0; j < line.length(); j++){
      sum += line.charAt(j);
    }
    return sum;
  }

  public static ArrayList<Card> removeDuplicateCombos(ArrayList<Card> fusions){
    if(fusions.size() < 2){
      return fusions;
    }
    //System.out.println(fusions);
    int[] fus = new int[fusions.size() / 3];
    int c = 0, index = 0;
    ArrayList<String> temp = new ArrayList<String>();
    ArrayList<String> track = new ArrayList<String>();
    for(int i = 0; i < fusions.size(); i += 3){ // group into three cards
      //System.out.println("i: " + i);
      for(int j = 0; j < 3; j++){ // group into three strings
        temp.add(fusions.get(j+i).toString());
        track.add(fusions.get(j+i).toString());
        //System.out.println("fusions: " + fusions.get(j+i).toString());
        if(j == 2){
          for(int k = 0; k < temp.size(); k++){ // visit each string
            String curr = temp.get(k);
              c += SumCharVals(curr); // sum the string
          }
        }
      }
      fus[index] = c;
      index++;
      c = 0;
      temp.clear();
    }
    fus = removeDuplicates(fus);
    int curr = 0;
    String line = "";
    ArrayList<String> result = new ArrayList<String>();
    ArrayList<Integer> fusList = new ArrayList<Integer>();
    for(int i = 0; i < fus.length; i++){
      if(fus[i] != 0){
        fusList.add(fus[i]);
      }
    }
    for(int i = 0; i < fusList.size(); i++){
      for(int s = 0; s < track.size(); s += 3){
        line = track.get(s);
        line += track.get(s+1);
        line += track.get(s+2);
        int sum = SumCharVals(line);
        if(fusList.get(i) == sum){
          result.add(track.get(s));
          result.add(track.get(s+1));
          result.add(track.get(s+2));
          fusList.remove(i);
          if(i != 0){
            i--;
          }
          else if(fusList.size() == 0){
            break;
          }
        }
      }
    }
    fusions.clear();
    for(int i = 0; i < result.size(); i++){
      fusions.add(getCardFromName(getNameFromString(result.get(i))));
    }
    return fusions;
  }

  public static String getNameFromString(String line){
    //line = line.split(" ").toString();
    //System.out.println("\tline: " + line);
    line = line.subSequence(0, 3).toString().trim();
    int s = Integer.parseInt(line);
    line = combos[0][s-1].name;
    //System.out.println("\tline: " + line);
    return line;
  }

  public static ArrayList<Card> fusionChains(ArrayList<Card> fusions, ArrayList<Card> hand, ArrayList<Card> board){
    //fusions = removeDuplicateCombos(fusions);
    //System.out.println(fusions);
    if(fusions.size() < 2){
      return fusions;
    }
    System.out.println(hand);
    System.out.println(fusions);
    System.out.println(board);
    ArrayList<Card> handBoardCombos = new ArrayList<Card>();
    ArrayList<Card> fusHandCombos = new ArrayList<Card>();
    ArrayList<Card> fusBoardCombos = new ArrayList<Card>();
    ArrayList<Card> a = new ArrayList<Card>();
    handBoardCombos.addAll(hand);
    handBoardCombos.addAll(board);
    fusBoardCombos.addAll(fusions);
    fusBoardCombos.addAll(board);
    a.addAll(fusions);
    a.addAll(board);
    fusHandCombos.addAll(fusions);
    fusHandCombos.addAll(hand);
    //ArrayList<Card> temp = new ArrayList<Card>();
    //ArrayList<Card> temp = new ArrayList<Card>();
    if(a == fusBoardCombos){
      System.out.println("hey");
    }
    ArrayList<Card> newHand = hand;
    System.out.println("\thandBoardCombos FUSIONS");
    // System.out.println(handBoardCombos);
    System.out.println(fusionInHand(handBoardCombos));
    System.out.println("\tfusHandCombos FUSIONS");
    // System.out.println(fusHandCombos);
    System.out.println(fusionInHand(fusHandCombos));
    System.out.println("\tfusBoardCombos FUSIONS");
    // System.out.println(fusBoardCombos);
    System.out.println(fusionInHand(fusBoardCombos));
    System.out.println(fusions);
    System.out.println("\thand");
    System.out.println(hand);
    /*for(int j = 0 ; j < newHand.size(); j++){
      for(int i = 0; i < fusions.size(); i += 3){
        newHand.remove(fusions.get(i+1));
        newHand.remove(fusions.get(i));
        newHand.add(fusions.get(i+2));
      }
      System.out.println("\nNEWHAND\n"+newHand);
    }*/
    return fusions;
  }

  public static ArrayList<Card> deckFromIds(int[] ids){
    ArrayList<Card> res = new ArrayList<Card>();
    for(int i = 0; i < ids.length; i++){
      res.add(cardsList[ids[i] - 1]);
    }
    return res;
  }


  public static ArrayList<Card> genRandomHand(){
    int i = 0, c;
    ArrayList<Card> res = new ArrayList<Card>();
    for(i = 0; i < 5; i++){
      c = (int) (Math.floor(Math.random()*722));
      //System.out.println(c);
      res.add(cardsList[c]);
    }
    return res;
  }

  public static int abcde = 0;

  public static boolean handHasCorrectCards(ArrayList<Card> arr, Card target, ArrayList<Card> hand){
    ArrayList<Card> arrTemp = new ArrayList<Card>();
    arrTemp.add(target);
    arrTemp.addAll(arr);
    //System.out.println("target: " + target);
    ArrayList<Card> temp = new ArrayList<Card>();
    temp.addAll(hand);
    boolean res = true;
    for(int j = 0; j < arrTemp.size(); j++){
      if(hand.contains(arrTemp.get(j))){
        res &= temp.remove(arrTemp.get(j));
      }
    }
    return res;
  }

  public static void printOneCombo(Card a, Card b, Card c){
    System.out.println("== " + c + " ==\n\t" + a + " + " + b);
  }

  public static ArrayList<Card> fusionInHand(ArrayList<Card> hand){
    int s = hand.size();
    ArrayList<Card> res = new ArrayList<Card>();
    ArrayList<Card> temp = new ArrayList<Card>();
    boolean combo = false;
    for(int i = 0; i < s; i++){
      temp = possibleFusionPartners(hand.get(i));
      if(handHasCorrectCards(temp, hand.get(i), hand)){
        for(int j = 0; j < s; j++){
          for(int k = 0; k < temp.size(); k++){
            if(temp.get(k).id == hand.get(j).id){
              //printOneCombo(combos[temp.get(k).id][hand.get(i).id], temp.get(k), hand.get(i));
              combo = true;
              res.add(temp.get(k));
              res.add(hand.get(i));
              res.add(combos[temp.get(k).id][hand.get(i).id]);
              break;
            }
          }
        }
      }
      //System.out.println("combo: " + combo);
    }
    if(res.size() > 0){
      //res = fusionChains(res, hand, myBoard);
    }
    return removeDuplicateCombos(res);
  }


  public static void printCombos(){
    for(int f = 0; f < combos.length; f++){
      for(int g = 0; g < combos[f].length; g++){
        if(combos[f][g] != null){
          System.out.println("f: " + f + " g: " + g + " " +combos[f][g]);
        }
      }
    }
  }

  public static void initCombosTable(){
    for(int i = 0; i < cardsList.length; i++){
      if(i == 0){
        for(int j = 0; j < cardsList.length; j++){
          combos[i][j] = cardsList[j];
        }
      }
      else{
        combos[i][0] = cardsList[i];
      }
    }
  }

  public static Card lineToCard(String line){
    Scanner tokenizer = new Scanner(line);
    int id = -1, atkPoints = -1, defPoints = -1, cost = -1, j = -1, s = -1;
    String name = "", type = "NA", attribute = "NA", planet1 = "NA", planet2 = "NA", temp = "NA";
    ArrayList<String> brokenLine = new ArrayList<String>();
    while(tokenizer.hasNext() && (temp = tokenizer.next()) != null){
      brokenLine.add(temp);
    }
    id = Integer.parseInt(brokenLine.get(0));
    s = brokenLine.size();
    if(s >= 8){
      planet2 = brokenLine.get(--s);
      planet1 = brokenLine.get(--s);
      defPoints = Integer.parseInt(brokenLine.get(--s));
      atkPoints = Integer.parseInt(brokenLine.get(--s));
      cost = Integer.parseInt(brokenLine.get(--s));
      attribute = brokenLine.get(--s);
      type = brokenLine.get(--s);
    }
    else{
      type = brokenLine.get(--s);
    }
    for(j = 1; j < s; j++){
      name += brokenLine.get(j);
      if(j < s-1){
        name += " ";
      }
    }
    Card res = new Card(id, name, type, attribute, cost, atkPoints,
                        defPoints, planet1, planet2);
    return res;
  }

  public static boolean verifyCardName(String cardName){
    for(int i = 0; i < cardsList.length; i++){
      if(cardsList[i].name.equals(cardName)){
        return true;
      }
    }
    return false;
  }

  public static ArrayList<Card> possibleFusionPartners(Card target){
    ArrayList<Card> res = new ArrayList<Card>();
    for(int i = 0; i < combos.length; i++){
      if(target == combos[i][0]){
        //System.out.println("target: " + target + " combos " + combos[i][0]);
        for(int j = 1; j < combos[i].length; j++){
          if(combos[i+1][j] != null){
            //System.out.println("i: " + i + " j: " + j + " " + combos[i+1][j]);
            res.add(combos[0][j-1]);
          }
        }
      }
    }
    //System.out.println(res);
    return res;
  }

  public static Card getCardFromName(String cardName){
    for(int i = 0; i < cardsList.length; i++){
      if(cardsList[i].name.equals(cardName)){
        return cardsList[i];
      }
    }
    return null;
  }

  public static ArrayList<Card> getFusions(Card result){
    ArrayList<Card> res = new ArrayList<Card>();
    //System.out.println("result: " + result);
    for(int i = 1; i < combos.length; i++){
      for(int j = 1; j < combos[i].length; j++){
        if(combos[i][j] != null){
          if(combos[i][j].id == result.id){
            //System.out.println("i: " + i + " j: " + j + " " + combos[i][j]);
            res.add(combos[i-1][0]);
            res.add(combos[0][j-1]);
          }
        }
      }
    }
    return res;
  }

}

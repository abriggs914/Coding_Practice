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

import java.io.*;
import java.util.*;

public class CardIndexer{

  public static String file = "./combinations.txt";
  public static Scanner scan, tokenizer;
  public static Card[] cardsList = new Card[722];
  public static Card[][] combos = new Card[722][722];

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
      ArrayList<Card> hand = new ArrayList<Card>();
      /*
        Implement a draw() method to do this in less typing
      */
      // hand.add(getCardFromName("Emperor of the Land and Sea"));
      // hand.add(getCardFromName("Thousand Dragon"));
      // hand.add(getCardFromName("Ancient Tool"));
      // hand.add(getCardFromName("Umi"));
      // hand.add(getCardFromName("Dragon Zombie"));
      // hand.add(getCardFromName("Raigeki"));
      // hand.add(getCardFromName("Mystical Elf"));
      hand.add(getCardFromName("Jirai Gumo"));
      // hand.add(getCardFromName("Electric Snake"));
      // hand.add(getCardFromName("Mechanicalchacer"));
      //hand.add(getCardFromName("Octoberser"));
      // hand.add(getCardFromName("Emperor of the Land and Sea"));
      // hand.add(getCardFromName("Labyrinth Wall"));
      // hand.add(getCardFromName("Cannon Soldier"));
      // hand.add(getCardFromName("Koumori Dragon"));
      // hand.add(getCardFromName("Pragtical"));
      // hand.add(getCardFromName("Mystical Elf"));
      hand.add(getCardFromName("Oscillo Hero #2"));
      // hand.add(getCardFromName("Catapult Turtle"));
      // hand.add(getCardFromName("Ancient Tool"));
      // hand.add(getCardFromName("Mavelus"));
      // hand.add(getCardFromName("Firewing Pegasus"));
      // hand.add(getCardFromName("Dragon Zombie"));
      // hand.add(getCardFromName("King of Yamimakai"));
      // hand.add(getCardFromName("Time Wizard"));
      // hand.add(getCardFromName("Raigeki"));
      // hand.add(getCardFromName("Spellbinding Circle"));
      // hand.add(getCardFromName("Axe of Despair"));
      // hand.add(getCardFromName("Mountain"));
      hand.add(getCardFromName("Aqua Madoor"));
      // hand.add(getCardFromName("The Immortal of Thunder"));
      // hand.add(getCardFromName("Darkworld Thorns"));
      // hand.add(getCardFromName("Giant Mech-soldier"));
      // hand.add(getCardFromName("Twin-headed Thunder Dragon"));
      // hand.add(getCardFromName("Meteor Dragon"));
      // hand.add(getCardFromName("Mystical Elf"));
      // hand.add(getCardFromName("Akihiron"));
      hand.add(getCardFromName("Vermillion Sparrow"));
      // hand.add(getCardFromName("Ansatsu"));
      // hand.add(getCardFromName("Crimson Sunbird"));
      // hand.add(getCardFromName("Kaminarikozou"));
      // hand.add(getCardFromName("Embryonic Beast"));
      System.out.println();
      System.out.println(hand);
      System.out.println();
      System.out.println("hand.size(): " + hand.size());
      System.out.println("COMBOS AVAILABLE");
      System.out.println(fusionInHand(hand).size());
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


  public static void fusionChains(ArrayList<Card> fusions, ArrayList<Card> hand){

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

  public static ArrayList<Card> fusionInHand(ArrayList<Card> hand){
    int s = hand.size();
    ArrayList<Card> res = new ArrayList<Card>();
    ArrayList<Card> temp = new ArrayList<Card>();
    boolean combo = false;
    for(int i = 0; i < s; i++){
      temp = possibleFusionPartners(hand.get(i));
      for(int j = 0; j < s; j++){
        for(int k = 0; k < temp.size(); k++){
          boolean allReadyChecked = false;
          if(temp.get(k).id == hand.get(j).id && !allReadyChecked){
            System.out.println("== "+combos[temp.get(k).id][hand.get(i).id]+" ==\n\t"+temp.get(k)+" + "+hand.get(i));
            combo = true;
            allReadyChecked = true;
            //if(!res.contains(temp.get(k))){
              res.add(temp.get(k));
              res.add(hand.get(i));
              res.add(combos[temp.get(k).id][hand.get(i).id]);
            break;
          }
        }
      }
      //System.out.println("combo: " + combo);
    }
    return res;
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
        //System.out.println("target: " + combos[i][0]);
        for(int j = 1; j < combos[i].length; j++){
          if(combos[i+1][j] != null){
            //System.out.println("i: " + i + " j: " + j + " " + combos[i+1][j]);
            res.add(combos[0][j-1]);
          }
        }
      }
    }
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

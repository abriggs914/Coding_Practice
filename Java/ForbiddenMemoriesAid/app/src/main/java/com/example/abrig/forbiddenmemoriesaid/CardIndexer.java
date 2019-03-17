package com.example.abrig.forbiddenmemoriesaid;

/**
 * Java program to parse all yugioh
 * cards in the combinations.txt file.
 * Uses the Card class to store each
 * card's data. Program can produce
 * a list of possible combinations.
 *
 * March 2019
 * @author Avery Briggs
 * 3471065
 */

import java.io.FileInputStream;
import java.util.Scanner;
import java.util.ArrayList;

public class CardIndexer{

    public String file = "./combinations.txt";
    public Scanner scan, tokenizer;
    public Card[] cardsList = new Card[722];
    public Card[][] combos = new Card[722][722];
    public ArrayList<Card> myHand = new ArrayList<Card>();
    public ArrayList<Card> myBoard = new ArrayList<Card>();
    public ArrayList<Card> enemyBoard = new ArrayList<Card>();

    public void main(String[] args) throws CardException{
        //parseCombinationsFile();


        /*    int[] currDeck = {2,16,16,31,31,45,45,85,89,97,
                97,124,127,131,150,213,254,272,304,332,
                334,336,337,349,349,366,367,400,408,415,
                463,473,482,512,567,651,652,690,712,714};
        Card psychoPuppet = combos[715-1][0];
        Card babyDragon = combos[4-1][0];
        String suSk = "Summoned Skull";
      System.out.println("cardVal: " + psychoPuppet);
      //System.out.println(possibleFusionPartners(psychoPuppet));
      System.out.println("cardVal: " + babyDragon);
      //System.out.println(possibleFusionPartners(babyDragon));
      Card summonedSkull = getCardFromName(suSk);
      System.out.println("cardVal: " + summonedSkull);
      ArrayList<Card> suSkFusions = getFusions(summonedSkull);
      System.out.println(suSkFusions.size());
      //ArrayList<Card> hand = genRandomHand();

        // draw("Emperor of the Land and Sea", 'h');
        // draw("Thousand Dragon", 'h');
        // draw("Ancient Tool", 'h');
        // draw("Umi", 'h');
        // draw("Dragon Zombie", 'h');
        draw("Dragon Zombie", 'h');
        // draw("Raigeki", 'h');
        // draw("Mystical Elf", 'h');
        // draw("Jirai Gumo", 'h');
        draw("Electric Snake", 'h');
        // draw("Mechanicalchacer", 'h');
        // draw("Octoberser", 'h');
        // draw("Emperor of the Land and Sea", 'h');
        draw("Labyrinth Wall", 'h');
        // draw("Cannon Soldier", 'h');
        // draw("Koumori Dragon", 'h');
        // draw("Pragtical", 'h');
        // draw("Mystical Elf", 'h');
        draw("Oscillo Hero #2", 'h');
        // draw("Oscillo Hero #2", 'h');
        // draw("Catapult Turtle", 'h');
        // draw("Ancient Tool", 'h');
        // draw("Mavelus", 'h');
        // draw("Firewing Pegasus", 'h');
        // draw("Dragon Zombie", 'h');
        // draw("King of Yamimakai", 'h');
        // draw("Time Wizard", 'h');
        draw("Time Wizard", 'h');
        // draw("Raigeki", 'h');
        // draw("Spellbinding Circle", 'h');
        draw("Axe of Despair", 'h');
        // draw("Mountain", 'h');
        // draw("Aqua Madoor", 'h');
        // draw("The Immortal of Thunder", 'h');
        // draw("Darkworld Thorns", 'h');
        draw("Giant Mech-soldier", 'h');
        // draw("Twin-headed Thunder Dragon", 'b');
        // draw("B. Dragon Jungle King", 'b');
        draw("Meteor Dragon", 'h');
        draw("Mystical Elf", 'h');
        // draw("Akihiron", 'h');
        draw("Vermillion Sparrow", 'h');
        // draw("Ansatsu", 'h');
        // draw("Crimson Sunbird", 'h');
        // draw("Kaminarikozou", 'h');
        // draw("Yami", 'b');
        draw("Embryonic Beast", 'h');
        draw("LaLa Li-oon", 'h');
        // draw("Skullbird", 'h');
        draw("Catapult Turtle", 'h');
        // draw("Sea King Dragon", 'b');
        // draw("Kaminari Attack", 'h');
        draw("Meteor B. Dragon", 'h');


        // draw("Millennium Shield", 'e');
        // draw("Nekogal #2", 'e');
        // draw("Judge Man", 'e');
        // draw("Dark Hole", 'b');
        // draw("Axe of Despair", 'b');
        // System.out.println();
        // System.out.println(myHand);
        // System.out.println();
        // System.out.println("hand.size(): " + myHand.size());
        System.out.println("COMBOS AVAILABLE");
        ArrayList<Card> handCombos = new ArrayList<Card>();
        //myHand = genRandomHand();
        ArrayList<Card> tempHand = new ArrayList<Card>();
        tempHand = myHand;
        tempHand.addAll(myBoard);
        // handCombos = fusionInHand(myHand);
        handCombos = fusionInHand(tempHand);
        System.out.println();
        System.out.println(myHand);
        System.out.println();
        System.out.println("hand.size(): " + myHand.size());
        int handNumCombos = handCombos.size() / 3;
        System.out.println("combos in hand : " + handNumCombos);
        printCombosInHand(handCombos);
        System.out.println();
        System.out.println();
        selectStrongestCard(myHand, handCombos);

        //viewStarSigns(true);


        //printCombos();

      System.out.println(currDeck.length);
      System.out.println(deckFromIds(currDeck));
      System.out.println(fusionInHand(deckFromIds(currDeck)));
      System.out.println("\n\n\n");
      ArrayList<Card> tHTDFusions = getFusions(getCardFromName("Twin-headed Thunder Dragon"));

        // ArrayList<Card> abc =  getFusions(getCardFromName("Red-eyes B. Dragon"));
        // printGetFusions(abc);
      System.out.println("j: " + j);
      for(int x = 0; x < cardsList.length; x++){
        System.out.println(cardsList[x].toString());
      }
        Card a = getCardFromName("Twin-headed Thunder Dragon");
        Card b = getCardFromName("Judge Man");
        if(validFusionPartners(getCardFromName("Time Wizard"), getCardFromName("Koumori Dragon"))){
            System.out.println("true");
        }
        else{
            System.out.println("false");
        }
        //System.out.println(starSignAdvantage(a.planet2, b.planet1));
        */
    }

    public void parseCombinationsFile(){
        try{
            scan = new Scanner(new FileInputStream(file));
            String line = scan.nextLine();
            Card temp;
            int j = 0;
            while(scan.hasNext() && line != null){
                tokenizer = new Scanner(line);
                if(!line.equals("-------------------------------------------------------------------------------")){
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
                    tokenizer = new Scanner(line);
                    String checkLine = tokenizer.next();
                    if(checkLine.equals("+")){  // identifier found (card2)
                        colId = Integer.parseInt(tokenizer.next());
                        //System.out.println("colId: " + colId);
                    }
                    else if(checkLine.equals("=")){ // resutlt of combo
                        Card temp1 = lineToCard(line.substring(1));
                        combos[rowId][colId] = temp1;
                    }
                    else{ // identifier found (card1)
                        rowId = Integer.parseInt(checkLine);
                    }
                }
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
    }


    public void selectStrongestCard(ArrayList<Card> hand, ArrayList<Card> fusions){
        int maxH = -1;
        int maxF = -1;
        int maxIndexH = -1;
        int maxIndexF = -1;
        if(hand.size() == 0 && fusions.size() == 0){
            return;
        }
        for(int i = 0; i < hand.size(); i++){
            if(hand.get(i).atkPoints > maxH){
                maxH = hand.get(i).atkPoints;
                maxIndexH = i;
            }
        }
        for(int i = 2; i < fusions.size(); i += 3){
            if(fusions.get(i).atkPoints > maxH){
                maxF = fusions.get(i).atkPoints;
                maxIndexF = i;
            }
        }
        if(maxF >= 0 || maxH >= 0){
            // System.out.println("\n\tSelecting:\nBest Card in hand\t\tBest Card in Fusions\n"
            // + hand.get(maxIndexH) + fusions.get(maxIndexF));
            int maxFinal = 0;
            int maxIndexFinal = 0;
            boolean hORf = true;
            if(maxF > maxH){
                maxFinal = maxF;
                maxIndexFinal = maxIndexF;
                hORf = false;
            }
            else{
                maxFinal = maxH;
                maxIndexFinal = maxIndexH;
            }
            ArrayList<Card> temp = new ArrayList<Card>();
            temp.addAll(fusions);
            temp.addAll(hand);
            System.out.println("\n\tBest Card:\n\t" + ((hORf)? hand.get(maxIndexFinal) : fusions.get(maxIndexFinal))
                    + "\n\tFrom" +((hORf)? " your hand.": " possible fusions list."));
        }
    }


    public void viewStarSigns(boolean userIsAttacker) throws CardException{
        if(enemyBoard.size() > 0){
            ArrayList<Card> handBoard = new ArrayList<Card>();
            handBoard.addAll(myHand);
            handBoard.addAll(myBoard);
            System.out.println(handBoard);
            System.out.println(enemyBoard);
            for(int i = 0; i < enemyBoard.size(); i++){
                for(int j = 0; j < handBoard.size(); j++){
                    if(userIsAttacker){
                        System.out.println("handBoard: " + handBoard.get(j).name + " VS enemyBoard: " + enemyBoard.get(i).name);
                        System.out.println("handBoard: " + handBoard.get(j).planet2 + "\t enemyBoard: " + enemyBoard.get(i).planet1);
                        vssAttackSimulator(handBoard.get(j));
                        //playCard(handBoard.get(j));
                        // System.out.println(starSignAdvantage(handBoard.get(j).planet1, enemyBoard.get(i).planet1));
                    }
                    else{ // enemy is attacking

                    }
                }
            }
        }
    }

    public void vssAttackSimulator(Card card) throws CardException{
        if(enemyBoard.size() > 0){
            System.out.println("\n\tvssAttackSimulator envoked:");
            System.out.println("you played: " + card);
            System.out.println("Is it in Attack Mode?");
            System.out.println("enter\t1 - yes\n\t0 - no");
            Card attackingMonster = card;
            Card defendingMonster = card;
            boolean correctInput = false;
            scan = new Scanner(System.in);
            String line = "";
            String atkORDef = "";
            String starSign = "";
            int optionCount = 0;
            while(!correctInput){
                line = scan.nextLine();
                int s = 0;
                try {
                    s = Integer.parseInt(line);
                    if(s == 0){
                        atkORDef = "DEF";
                        correctInput = true;
                    }
                    else if(s == 1){
                        atkORDef = "ATK";
                        correctInput = true;
                    }
                    else{
                        throw new Exception();
                    }
                }
                catch(Exception e){
                    System.out.println("Try Again:");
                    System.out.println("you played: " + card);
                    System.out.println("Is it in Attack Mode?");
                    System.out.println("enter\t1 - yes\n\t0 - no");
                }
            }
            System.out.println("atkORDef selected: " + atkORDef);
            correctInput = false;
            System.out.println("you played: " + card);
            System.out.println("What is it's Star Sign?");
            System.out.println("enter\t1 - " + card.planet1 + "\n\t0 - " + card.planet2);
            while(!correctInput){
                line = scan.nextLine();
                int s = 0;
                try {
                    s = Integer.parseInt(line);
                    if(s == 1){
                        starSign = card.planet1;
                        correctInput = true;
                    }
                    else if(s == 0){
                        starSign = card.planet2;
                        correctInput = true;
                    }
                    else{
                        throw new Exception();
                    }
                }
                catch(Exception e){
                    System.out.println("Try Again:");
                    System.out.println("you played: " + card);
                    System.out.println("What is it's Star Sign?");
                    System.out.println("enter\t1 - " + card.planet1 + "\n\t0 - " + card.planet2);
                }
            }
            System.out.println("starSign selected: " + starSign);
            String[] res = new String[2];
            res[0] = atkORDef;
            res[1] = starSign;
            //card = getCardFromName(card.name);
            int id = card.id;
            String name = card.name;
            String type = card.type;
            String attribute = card.attribute;
            int cost = card.cost;
            int atkPoints = card.atkPoints;
            int defPoints = card.defPoints;
            String planet1 = card.planet1;
            String planet2 = card.planet2;
            card = new Card(id,name,type,attribute,cost,atkPoints,defPoints,
                    planet1,planet2,res[0],res[1]);
            card.setStarSignPlay(res[1]);
            if(!verifyCardName(card.name)){
                throw new CardException("UNKC");
            }
            myBoard.add(card);
            if(!atkORDef.equals("DEF")){
                System.out.println("Which card are you attacking?");
                optionCount = 0;
                for(int i = 0; i < enemyBoard.size(); i++, optionCount++){
                    System.out.println("\t" + optionCount + " - " + enemyBoard.get(i));
                }
                correctInput = false;
                while(!correctInput){
                    line = scan.nextLine();
                    int s = 0;
                    try{
                        s = Integer.parseInt(line);
                        for(int i = 0; i < enemyBoard.size(); i++){
                            if(s == i){
                                defendingMonster = enemyBoard.get(i);
                                attackingMonster = card;
                                correctInput = true;
                            }
                        }
                        throw new Exception();
                    }
                    catch(Exception e){
                        System.out.println("Try Again:");
                        System.out.println("defending card: " + card);
                        System.out.println("Which card are you attacking?");
                        optionCount = 0;
                        for(int i = 0; i < enemyBoard.size(); i++, optionCount++){
                            System.out.println("\t" + optionCount + " - " + enemyBoard.get(i));
                        }
                    }
                }
            }
            else{ // you are defending
                System.out.println("Which card is attacking?");
                optionCount = 0;
                for(int i = 0; i < enemyBoard.size(); i++, optionCount++){
                    System.out.println(optionCount + " - " + enemyBoard.get(i));
                }
                correctInput = false;
                while(!correctInput){
                    line = scan.nextLine();
                    int s = 0;
                    try{
                        s = Integer.parseInt(line);
                        for(int i = 0; i < enemyBoard.size(); i++){
                            if(s == i){
                                attackingMonster = enemyBoard.get(i);
                                defendingMonster = card;
                                correctInput = true;
                                break;
                            }
                        }
                        throw new Exception();
                    }
                    catch(Exception e){
                        System.out.println("Try Again:");
                        System.out.println("defending card: " + card);
                        System.out.println("Which card is attacking?");
                        optionCount = 0;
                        for(int i = 0; i < enemyBoard.size(); i++, optionCount++){
                            System.out.println("\t" + optionCount + " - " + enemyBoard.get(i));
                        }
                    }
                }
            }
            System.out.println("\n\tFIGHT!\n");
            System.out.println("attackingMonster: " + attackingMonster);
            System.out.println("defendingMonster: " + defendingMonster);
            String advantagePlanet = starSignAdvantage(attackingMonster.planet1, defendingMonster.planet1);
            System.out.println("starSign advantage: " + advantagePlanet);
        }
    }

    /**
     draw method is called to add a new card to either a hand or the board,
     based on the value of hORb. Takes a string, a char and returns void.
     @param cardName String value of a cards name.
     @param hORb Char value signifying where the card is to be stored.
     @throws CardException Ensuring that the given char is among acceptable
     criteria.
     */
    public void draw(String cardName, char hORb) throws CardException{
        if(hORb == 'h'){
            myHand.add(getCardFromName(cardName));
        }
        else if(hORb == 'b'){
            myBoard.add(getCardFromName(cardName));
        }
        else if(hORb == 'e'){
            Card card = getCardFromName(cardName);
            int id = card.id;
            String name = card.name;
            String type = card.type;
            String attribute = card.attribute;
            int cost = card.cost;
            int atkPoints = card.atkPoints;
            int defPoints = card.defPoints;
            String planet1 = card.planet1;
            String planet2 = card.planet2;
            String[] states = cardStates(card);
            card = new Card(id,name,type,attribute,cost,atkPoints,defPoints,
                    planet1,planet2,states[0],states[1]);
            card.setStarSignPlay(states[1]);
            if(!verifyCardName(card.name)){
                throw new CardException("UNKC");
            }
            enemyBoard.add(card);
        }
        else{
            throw new CardException("HORB");
        }
    }

    public String[] cardStates(Card card){
        // NEED USER INPUT TO DETERMINE AI CHOICES
        System.out.println("\n\tcardStates envoked:");
        System.out.println("Computer played: " + card);
        System.out.println("Is it in Attack Mode?");
        System.out.println("enter\t1 - yes\n\t0 - no");
        boolean correctInput = false;
        scan = new Scanner(System.in);
        String line = "";
        String atkORDef = "";
        String starSign = "";
        while(!correctInput){
            line = scan.nextLine();
            int s = 0;
            try {
                s = Integer.parseInt(line);
                if(s == 0){
                    atkORDef = "DEF";
                    correctInput = true;
                }
                else if(s == 1){
                    atkORDef = "ATK";
                    correctInput = true;
                }
                else{
                    throw new Exception();
                }
            }
            catch(Exception e){
                System.out.println("Try Again:");
                System.out.println("Computer played: " + card);
                System.out.println("Is it in Attack Mode?");
                System.out.println("enter\t1 - yes\n\t0 - no");
            }
        }
        System.out.println("atkORDef selected: " + atkORDef);
        correctInput = false;
        System.out.println("Computer played: " + card);
        System.out.println("What is it's Star Sign?");
        System.out.println("enter\t1 - " + card.planet1 + "\n\t0 - " + card.planet2);
        while(!correctInput){
            line = scan.nextLine();
            int s = 0;
            try {
                s = Integer.parseInt(line);
                if(s == 1){
                    starSign = card.planet1;
                    correctInput = true;
                }
                else if(s == 0){
                    starSign = card.planet2;
                    correctInput = true;
                }
                else{
                    throw new Exception();
                }
            }
            catch(Exception e){
                System.out.println("Try Again:");
                System.out.println("Computer played: " + card);
                System.out.println("What is it's Star Sign?");
                System.out.println("enter\t1 - " + card.planet1 + "\n\t0 - " + card.planet2);
            }
        }
        System.out.println("starSign selected: " + starSign);
        System.out.println();
        System.out.println(card);
        System.out.println();
        String[] res = new String[2];
        res[0] = atkORDef;
        res[1] = starSign;
        return res;
    }

    /**
     printGetFusions method is called to print the results of possibleFusionPartners.
     Prints pairs of cards in a Card A " + " Card B format. Returns void.
     @param a ArrayList<Card> representing pairs of card combinations.
     */
    public void printGetFusions(ArrayList<Card> a){
        for(int i = 0; i < a.size(); i++){
            if(i % 2 == 0){
                System.out.print(a.get(i) + " + ");
            }
            else{
                System.out.println(a.get(i));
            }
        }
    }

    /**
     printCombosInHand method prints the results of fusionInHand as triples
     of card combos. Takes 3 cards at a time and calls printOneCombo to format
     the results. Returns void.
     @param arr ArrayList<Card> of card combinations in triple form
     (a1, b1, c1, a2, b2, ...).
     */
    public void printCombosInHand(ArrayList<Card> arr){
        for(int i = 0; i < arr.size(); i += 3){
            printOneCombo(arr.get(i), arr.get(i+1), arr.get(i+2));
        }
    }

    /**
     merge method is called to merge an integer array into one sorted
     integer array, returns the integer array.
     @param arr An integer array.
     @param l The leftmost starting int index.
     @param m The middle int index of arr.
     @param r The rightmost ending int index.
     @return Returns an updated version of the arr parameter.
     */
    public int[] merge(int[] arr, int l, int m, int r){
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

    /**
     removeDuplicates method is called to remove all duplicate integers
     in a given integer array. Returns an array of unique sorted integers,
     by calling sort.
     @param arr An integer array.
     @return An integer array of unique and sorted values.
     */
    public int[] removeDuplicates(int[] arr){
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

    /**
     mergeSort method is called by sort to sort an integer array using
     a mergeSort algorithm. Returns the given integer array sorted in
     ascending order.
     @param arr The unsorted integer array.
     @param l The leftmost starting index for sorting.
     @param r The rightmost ending index for sorting.
     @return The parameterized array sorted.
     */
    public int[] mergeSort(int[] arr, int l, int r){
        if(l < r){
            int m = (l + r)/2;
            arr = mergeSort(arr, l, m);
            arr = mergeSort(arr , m + 1, r);
            arr = merge(arr, l, m, r);
        }
        return arr;
    }

    /**
     sort method is called to act as a handler / starting point for then
     mergeSort method. Returns a sorted integer array
     @param arr An unsorted integer array.
     @return The given integer array sorted.
     */
    public int[] sort(int[] arr){
        int n = arr.length;
        arr = mergeSort(arr, 0, n - 1);
        return arr;
    }

    /**
     sumCharVals method is called to sum each character's ascii value
     within a given string. Returns the sum.
     @param line The string value to be computed.
     @return The sum of all ascii values for each character of the string.
     */
    public int sumCharVals(String line){
        int sum = 0;
        for(int j = 0; j < line.length(); j++){
            sum += line.charAt(j);
        }
        return sum;
    }

    /**
     removeDuplicateCombos method takes in an ArrayList<Card> of possible
     fusion triples of the form (a1, b1, c1, a2, b2,...). Method returns an
     ArrayList<Card> of only unique combos. Uses local ArrayLists to keep track
     of order, and sums of each combination triples strings (calculated with
     sumCharVals).
     (I.E. if hand: {"Time Wizard", "Time Wizard", "Koumouri Dragon"}
     then possible combos: {A + C = "Thousand Dragon", B + C = "Thousand Dragon"}
     but we want to exclude 1 of these duplicate combos.
     => return result of only one of the combos since the are the same.)
     @param fusions An ArrayList<Card> of card combination triples (a,b,c).
     @return An ArrayList<Card> of only unique combinations.
     */
    public ArrayList<Card> removeDuplicateCombos(ArrayList<Card> fusions){
        System.out.println(fusions);
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
                        c += sumCharVals(curr); // sum the string
                    }
                }
            }
            fus[index] = c;
            index++;
            c = 0;
            temp.clear();
        }
        fus = removeDuplicates(fus);
        for(int i = 0; i < fus.length; i++){
            // System.out.println("fus["+i+"]: " + fus[i]);
        }
        int curr = 0;
        String line = "";
        ArrayList<String> result = new ArrayList<String>();
        ArrayList<Integer> fusList = new ArrayList<Integer>();
        for(int i = 0; i < fus.length; i++){
            if(fus[i] != 0){
                fusList.add(fus[i]);
            }
        }
        // System.out.println("\tfusList:\n" + fusList);
        // System.out.println("\n\ttrack: \n" + track);
        for(int i = 0; i < fusList.size(); i++){
            boolean counted = false;
            for(int j = 0; j < track.size(); j += 3){
                line = track.get(j);
                line += track.get(j+1);
                line += track.get(j+2);
                int sum = sumCharVals(line);
                // System.out.println("sum: " + sum + " counted: " + counted);
                if(fusList.get(i) == sum && !counted){
                    counted = true;
                    result.add(track.get(j));
                    result.add(track.get(j+1));
                    result.add(track.get(j+2));
                    // System.out.println("fusList["+i+"]: " + fusList.get(i));
                    fusList.remove(i);
                    // System.out.println("\tfusList: @ ( i = "+i+" )\n" + fusList);
                    i--;
                    break;
                }
            }
        }
        fusions.clear();
        for(int i = 0; i < result.size(); i++){
            fusions.add(getCardFromName(getNameFromString(result.get(i))));
        }
        return sortCardsByAttack(fusions);
    }

    /**
     getNameFromString method takes in a card string, the
     results of calling toString() on a Card, and returns the
     Card's name that corresponds to the string. Uses the
     combos array and and id lookup algorithm. Returns the string.
     @param line a string.
     @return String value for a card's name.
     */
    public String getNameFromString(String line){
        // System.out.println("\tline: " + line);
        line = line.subSequence(0, 3).toString().trim();
        if(line.charAt(1) == ' '){
            line = line.subSequence(0, 2).toString().trim();
        }
        // System.out.println("\tline: " + line);
        int s = Integer.parseInt(line);
        line = combos[0][s-1].name;
        // System.out.println("\tline: " + line);
        if(verifyCardName(line)){
            return line;
        }
        else{
            return "";
        }
    }


    public ArrayList<Card> sortCardsByAttack(ArrayList<Card> arr){
        ArrayList<Card> result = new ArrayList<Card>();
        ArrayList<Card> arrTemp = new ArrayList<Card>();
        arrTemp.addAll(arr);
        for (int i = 2; i < arrTemp.size(); i += 3){
            Card temp = arrTemp.get(i);
            int targetIndex = i;
            for (int j = i + 3; j < arrTemp.size(); j += 3){
                if(temp.compareTo(arrTemp.get(j)) == 1){
                    targetIndex = j;
                    temp = arrTemp.get(j);
                }
            }
            // System.out.println("\nPlaced: " + temp + "\n");
            result.add(arrTemp.get(targetIndex - 2));
            result.add(arrTemp.get(targetIndex - 1));
            result.add(temp);
            arrTemp.remove(targetIndex - 2);
            arrTemp.remove(targetIndex - 2);
            arrTemp.remove(targetIndex - 2);
            i -= 3;

            // used for reducingthe list to uniquely sorted cards. not the primary
            // functionality of the method.
      /*int c = 0;
      for(int j = 2; j < arrTemp.size(); j += 3){
        if(temp.id == arrTemp.get(j).id){
          System.out.println("\n\n\n"+arrTemp.get(j));
          arrTemp.remove(j-2);
          arrTemp.remove(j-2);
          arrTemp.remove(j-2);
          j -= 3;
          c += 3;
        }
      }
      System.out.println("c: " + c);
      //arrTemp.remove(i);
      if(i - c >= 0){
        i -= c;
      }*/
        }
        arr.clear();
        arr.addAll(result);
        return arr;
    }


    public void fusionChains(ArrayList<Card> fusions, ArrayList<Card> hand, ArrayList<Card> board){
        //fusions = removeDuplicateCombos(fusions);
        //System.out.println(fusions);
        if(fusions.size() < 2){
            return ;//fusions;
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
        //return fusions;
    }


    public boolean validFusionPartners(Card a, Card b){
        Card res = combos[a.id][b.id];
        return res != null;
    }


    /**
     deckFromIdsis called to turn an integer array of card id's
     into an ArrayList<Card> of Card objects. Returns an ArrayList<Card>.
     @param ids An Integer array of card ids.
     @return An ArrayList<Card>.
     */
    public ArrayList<Card> deckFromIds(int[] ids){
        ArrayList<Card> res = new ArrayList<Card>();
        for(int i = 0; i < ids.length; i++){
            res.add(cardsList[ids[i] - 1]);
        }
        return res;
    }


    /**
     genRandomHand is called to generate an ArrayList<Card> of five
     cards randomly. Returns the new ArrayList.
     @return The ArrayList of Cards.
     */
    public ArrayList<Card> genRandomHand(){
        int i = 0, c;
        ArrayList<Card> res = new ArrayList<Card>();
        for(i = 0; i < 5; i++){
            c = (int) (Math.floor(Math.random()*722));
            //System.out.println(c);
            res.add(cardsList[c]);
        }
        // System.out.println(res);
        return res;
    }


    /**
     handHasCorrectCards method is called to check that a given hand contains
     all cards that are said to be combinations (in arr). Loops through the
     combinations and determines if the combination is valid.
     Returns a boolean value, true if all necessary cards are found,
     else returns false.
     (Used to catch combos that can be made with two of the same card.)
     @param arr An ArrayList<Card> of possible fusions.
     @param target The card that the fusion list was created with.
     @param hand An ArrayList<Card> of remaining cards in hand.
     @return A boolean value corresponding to if all cards necessary are present.
     */
    public boolean handHasCorrectCards(ArrayList<Card> arr, Card target, ArrayList<Card> hand){
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


    /**
     printOneCombo is called to print three given cards in a A + B = C
     fusion format. Returns void.
     EX :
     == 425 Thunder Dragon Th L 5 1600 1500 P J ==
     191 LaLa Li-oon Th Wi 2 600 600 P Mo + 31 Koumori Dragon Dr D 4 1500 1200 Mo J
     @param a Card a.
     @param a Card b.
     @param a Card c.
     */
    public void printOneCombo(Card a, Card b, Card c){
        System.out.println("== " + c + " ==\n\t" + a + " + " + b);
    }


    /**
     fusionInHand method takes in an ArrayList<Card> and determines
     if any of the cards can be combined together. Method calls fusionChains
     and removeDuplicateCombos to reduce the list of combinations.
     results will be sorted in ascending attack power as a sideeffect
     of removeDuplicateCombos. Returns an ArrayList<card> of combination
     triples (A + B = c).
     @return An ArrayList<Card> of combination triples.
     @param hand An ArrayList<Card>.
     */
    private ArrayList<Card> fusionInHand(ArrayList<Card> hand){
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
            // fusionChains(res, hand, myBoard);
        }
        return removeDuplicateCombos(res);
    }


    /**
     initCombosTable method is called to create a 2D array of Cards, and
     set the first row and first column to the values of each possible
     game card in order of id number. This will create a chart where each
     card on one axis can be compared to another on the other axis.
     Called at the beginning of program execution. Returns void.
     */
    public void initCombosTable(){
        parseCombinationsFile();
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


    /**
     lineToCard method is called to turn a bufferered string into a Card object.
     Uses a scanner to tokenize each character, and assign to card attribute
     values. Returns the created Card.
     @param line A string of characters read from the combinations.txt file.
     @return The created Card.
     */
    public Card lineToCard(String line){
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


    /**
     verifyCardName method is called to verify if a computed card name is valid,
     according to the parsed cardsList array. Returns true or false based on the
     validity of the given card name.
     @param cardName A string corresponding to a card's name.
     @return A boolean corresponding to the validity of the card's name.
     */
    public boolean verifyCardName(String cardName){
        for(int i = 0; i < cardsList.length; i++){
            if(cardsList[i].name.equals(cardName)){
                return true;
            }
        }
        return false;
    }


    /**
     possibleFusionPartners method is called to return an ArrayList<Card>
     of every possible fusion partner that the given taret card can fuse with.
     @param target A Card.
     @return ArrayList<Card> of all possible fusion partners.
     */
    public ArrayList<Card> possibleFusionPartners(Card target){
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
        // System.out.println(res);
        return res;
    }


    /**
     getCardFromName method is called to return the card corresponding to
     a given card's name in string form. Returns the target card.
     @param cardName A card's name in string form.
     @return A card corresponding to the given card name.
     */
    public Card getCardFromName(String cardName){
        for(int i = 0; i < cardsList.length; i++){
            if(cardsList[i].name.equals(cardName)){
                return cardsList[i];
            }
        }
        return null;
    }


    public String starSignAdvantage(String ss1Atk, String ss2Def) throws CardException{
        String[] first = {"Sun", "Moon", "Venus", "Mercury"};
        String[] second = {"Mars","Jupiter","Saturn","Uranus","Pluto","Neptune"};
        int ss1Index = -1;
        int ss2Index = -1;
        int cutOff = 2;
        String temp = "";
        boolean fORs1 = true;
        boolean fORs2 = true;
        for(int i = 0; i < first.length; i++){
            if(ss1Atk.length() == 1){
                cutOff = 1;
            }
            temp = first[i].subSequence(0, cutOff).toString();
            if(ss1Atk.equals(temp)){
                ss1Index = i;
            }
            cutOff = 2;
            if(ss2Def.length() == 1){
                cutOff = 1;
            }
            temp = first[i].subSequence(0, cutOff).toString();
            if(ss2Def.equals(temp)){
                ss2Index = i;
            }
            cutOff = 2;
        }
        if(ss1Index < 0 || ss2Index < 0){
            for(int i = 0; i < second.length; i++){
                if(ss1Atk.length() == 1){
                    cutOff = 1;
                }
                temp = second[i].subSequence(0, cutOff).toString();
                if(ss1Atk.equals(temp)){
                    ss1Index = i;
                    fORs1 = false;
                }
                cutOff = 2;
                if(ss2Def.length() == 1){
                    cutOff = 1;
                }
                temp = second[i].subSequence(0, cutOff).toString();
                if(ss2Def.equals(temp)){
                    ss2Index = i;
                    fORs2 = false;
                }
                cutOff = 2;
            }
        }
        if(fORs1 != fORs2){
            return "NONE";
        }
        else{
            if(fORs1){
                if(ss1Index == 3){
                    ss1Index = -1;
                }
                if(ss1Index + 1 == ss2Index){
                    return ss1Atk;
                }
                if(ss2Index == 3){
                    ss2Index = -1;
                }
                if(ss2Index + 1 == ss1Index){
                    return ss2Def;
                }
            }
            else{
                if(ss1Index == 5){
                    ss1Index = -1;
                }
                if(ss1Index + 1 == ss2Index){
                    return ss1Atk;
                }
                if(ss2Index == 5){
                    ss2Index = -1;
                }
                if(ss2Index + 1 == ss1Index){
                    return ss2Def;
                }
                else{
                    if(ss1Index > ss2Index){
                        if(ss1Index - ss2Index >= 2){
                            return "NONE";
                        }
                    }
                    else{
                        if(ss2Index - ss1Index >= 2){
                            return "NONE";
                        }
                    }
                }
            }
        }
        throw new CardException("SSUC");
    }

    public ArrayList<String> genTypeList(){
        ArrayList<String> res = new ArrayList<String>();
        for(int i = 0; i < cardsList.length; i++){
            String type = cardsList[i].type;
            if(!res.contains(type)){
                res.add(type);
            }
        }
        System.out.println(res);
        return res;
    }


  /*


  public ArrayList<Card> getFusions(Card result){
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
    System.out.println(res);
    return res;
  }*/

}


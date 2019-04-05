/*

*/

import java.util.*;
import java.io.*;

public class Passwords{

  public static String fileName = "./passwords.txt";

  public static void main(String[] args){
    BufferedReader br;
    try{
      br = new BufferedReader(new InputStreamReader(new FileInputStream(fileName)));
      String line = "";
      ArrayList<String> inputLines = new ArrayList<String>();
      String[] cards = new String[722];
      while((line = br.readLine()) != null){
        inputLines.add(line);
      }
      int len = inputLines.size();
      for(int i = 0; i < len; i++){
        try{
          String temp = inputLines.get(i);
          int x = Integer.parseInt(temp.substring(0, 3));
          if(cards[x-1] == null && !temp.substring(4, 14).equals("Starchips")){
            cards[x-1] = temp;
          }
        }
        catch(Exception e){}
      }
      int[] passwordsArr = new int[722];
      for(int i = 0; i < cards.length; i++){
        if(cards[i].substring(cards[i].length() - 3, cards[i].length()).equals("N/A")){
          passwordsArr[i] = Integer.parseInt(cards[i].substring(cards[i].length() - 12, cards[i].length() - 5));
        }
        else{
          passwordsArr[i] = Integer.parseInt(cards[i].substring(cards[i].length() - 15, cards[i].length() - 7));
        }
      }
      Arrays.sort(passwordsArr);
      // System.out.println("inputLines: " + inputLines);
      System.out.println();
      System.out.println();
      System.out.println("cards: ");
      for(int i = 0; i < cards.length; i++){
        System.out.println("cards["+i+"]: " + cards[i]);
      }
      for(int i = 0; i < passwordsArr.length; i++){
        System.out.println("passwordsArr["+i+"]: " + passwordsArr[i]);
      }
      System.out.println(cards.length);
    }
    catch(Exception e){
      System.out.println("Something went wrong in general");
      e.printStackTrace();
    }
  }

}

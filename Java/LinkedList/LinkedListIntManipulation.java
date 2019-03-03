/*
  Simple java program to read in a list of
  integers and add them to a linked list
  structure. then the last n elements are
  removed from the list according to the
  value of the first elementof the array.

  Adaptive Java Stepik Assignment
  Mar.3/19
  Avery Briggs
  3471065
*/


import java.util.*;
import java.io.*;

public class LinkedListIntManipulation{
  public static void main(String[] args) throws IOException {
      BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
      int str = reader.read();
      LinkedList<Integer> ll = new LinkedList<Integer>();
      while (str > 0){
            str -= 48;
            int x = reader.read() - 48;
            int i = 1;
            while(x >= 0){
              str = (int) (Math.pow(10,i) * str) + x;
              x = reader.read() - 48;
              if(x < 0){
                break;
              }
              i++;
            }
          if(str >= 0){
            ll.add(str);
          }
          str = reader.read();
      }

      int removeNum = ll.get(0);
      for(int i = 0; i < removeNum * 3 && i < ll.size(); i++){
        ll.removeLast();
      }

      for(int i = 0; i < ll.size(); i++){
          System.out.println(ll.get(i));
      }

  }
}

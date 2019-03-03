/*
  Simple java program to compute the
  number of times an integer is found
  in a given integer array.

  Adaptive Java Stepik Assignment
  Mar.3/19
  Avery Briggs
  3471065
*/

import java.util.*;
class targetCounterIntArray {
  public static void main(String[] args) {
    // put your code here
      Scanner scan = new Scanner(System.in);
      int target = Integer.parseInt(scan.nextLine());
      int num = scan.nextInt();
      int count = 0;
      while(num != 0){
          if(num == target){
              count++;
          }
          num = scan.nextInt();
      }
      System.out.println(count);
  }
}

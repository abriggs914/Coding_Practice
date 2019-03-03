/*
  Simple java program to compute the
  sum of an integer array ending in 0.

  Adaptive Java Stepik Assignment
  Mar.3/19
  Avery Briggs
  3471065
*/

import java.util.*;
class sumIntArray {
  public static void main(String[] args) {
    // put your code here
      Scanner scan = new Scanner(System.in);
      int num = scan.nextInt();
      int sum = 0;
      while(num != 0){
          if(num == 0){
              break;
          }
          sum += num;
          num = scan.nextInt();
      }
      System.out.println(sum);
  }
}

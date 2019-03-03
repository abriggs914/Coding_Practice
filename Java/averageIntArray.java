/*
  Simple java program to compute the
  average of an integer array ending in 0.

  Adaptive Java Stepik Assignment
  Mar.3/19
  Avery Briggs
  3471065
*/

import java.util.*;
class averageIntArray {
  public static void main(String[] args) {
    // put your code here
      Scanner scan = new Scanner(System.in);
      int num = scan.nextInt();
      int sum = 0;
      int count = 0;
      while(num != 0){
          if(num == 0){
              break;
          }
          sum += num;
          num = scan.nextInt();
          count++;
      }
      System.out.println(((double)sum)/((double)count));
  }
}

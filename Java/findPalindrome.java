/*
  Simple java program to determine if a
  given string is a palindrome or not.
  runs in O(n) and makes use of the
  charsubsequence data type

  Adaptive Java Stepik Assignment
  Mar.3/19
  Avery Briggs
  3471065
*/

import java.util.*;
class findPalindrome {
  public static void main(String[] args) {
    // put your code here
    Scanner scan = new Scanner(System.in);
    String line = scan.nextLine();
      boolean palindrome = true;
    if(line.length() > 1){
        String first, last;
        int mid = line.length()/2;
        first = line.subSequence(0,mid).toString();
        last = line.subSequence(mid,line.length()).toString();
        int j = mid - ((line.length() % 2 == 0)? 1 : 0);
        for(int i = 0; i < mid; i++, j--){
          //System.out.println("i: " + i + " j: " + j);
            if(first.charAt(i) != last.charAt(j)){
              palindrome = false;
            }
        }
    }
    if(palindrome){
        System.out.println("yes");
    }
    else{
        System.out.println("no");
    }
  }
}

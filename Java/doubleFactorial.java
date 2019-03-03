/*
  Simple java program to compute the
  double fatorial of an integer using
  the BigInteger class.

  Adaptive Java Stepik Assignment
  Mar.3/19
  Avery Briggs
  3471065
*/

import java.math.BigInteger;

public class doubleFactorial{

  public static void main(String[] args) {
    int n = 7;
    System.out.println(calcDoubleFactorial(n));
  }

  public static BigInteger calcDoubleFactorial(int n) {
      // type your java code here
      if(n == 1 || n == 0){
          return BigInteger.valueOf(1);
      }
      else{
          return BigInteger.valueOf(n).multiply(calcDoubleFactorial(n-2));
      }
  }
}

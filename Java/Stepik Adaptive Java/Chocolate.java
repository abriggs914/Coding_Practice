// Chocolate

// A chocolate bar has a shape of rectangle, divided into NxM segments. You can break down this chocolate bar into two parts by a single straight line (only once). Find whether you can break off exactly K segments from the chocolate. Each segment is 1x1.

// Input data format

// The program gets an input of three integers: N, M, K

// Output data format

// The program must output one of the two words: YES or NO.

// Sample Input 1:
/*
4
2
6
*/
// Sample Output 1:
/*
YES
*/
// Sample Input 2:
/*
2
10
7
*/
// Sample Output 2:
/*
NO
*/

import java.util.Scanner;

class Chocolate {
    
  public static Scanner sc = new Scanner(System.in);
    
  public static int readInt() {
      return sc.nextInt();
  }  
    
  public static String readLine() {
      return sc.next();
  }
    
  public static int compute_squares(int n, int m) {
      return n * m;   
  }
    
  public static void main(String[] args) {
    // put your code here
      int n = readInt();
      int m = readInt();
      int k = readInt();
      boolean f = false;
      
      
      for (int i = n; i > 0; i--) {
          int cs = compute_squares(i, m);
          //System.out.println("cs:\t" + cs);
          if (cs == k) {
              //System.out.println("YES");
              f = true;
          }          
      }
      for (int j = m; j > 0; j--) {
          int cs = compute_squares(n, j);
          //System.out.println("cs:\t" + cs);
          if (cs == k) {
              //System.out.println("YES");
              f = true;
          }
      }
      if (f) {
          System.out.println("YES");
      }
      else {
          System.out.println("NO");          
      }
  }
}
/**
Java program to calculate the angle between two given vector. the input
must be of the form: vector1component1 vector1component2
                     vector2component1 vector2component2
Avery Briggs 
3471065
May 2018
*/
import java.util.Scanner;
public class AngleBetweenVectors{

  public static void main(String[] args) {
    //put your code here
    Scanner scan = new Scanner(System.in);
    int[][] a = new int[2][2];
    for(int i = 0; i < a.length; i++){
       a[0][i] = scan.nextInt(); 
    }
    for(int j = 0; j < a[0].length; j++){
       a[1][j] = scan.nextInt();     
    }
    for(int i = 0; i < a.length; i++){
        for(int j = 0; j < a[0].length; j++){
          // System.out.println("a["+i+"]["+j+"]: " + a[i][j]);   
        }
    }
    double res = angle(a);
    System.out.println("angle between line (0,0) to ("+a[0][0]+","+a[0][1]+
                        ") and (0,0) to ("+a[1][0]+","+a[1][1]+"), is: "+res+" degrees."); 
  }
  
  static public double angle(int[][] vectors){
      int dotProduct;
      int magA;
      int magB;
      double res;
      double magADouble;
      double magBDouble;
      double denominator;
      dotProduct = ((vectors[0][0]*vectors[1][0]) + (vectors[0][1]*vectors[1][1]));
      magA = ((vectors[0][0]*vectors[0][0]) + (vectors[0][1]*vectors[0][1]));
      magB = ((vectors[1][0]*vectors[1][0]) + (vectors[1][1]*vectors[1][1]));
      magADouble = Math.sqrt(magA);
      magBDouble = Math.sqrt(magB);
      res = ((double)dotProduct/(magADouble*magBDouble));
      System.out.println("\ndotProduct: " + dotProduct + " magA: " + magA + 
                            " magB: " + magB + " res: " + res + " \nmagADouble: " + magADouble +
                            " magBDouble: " + magBDouble);
      res = (Math.acos(res) * (180/Math.PI));
      return res;
  }
}
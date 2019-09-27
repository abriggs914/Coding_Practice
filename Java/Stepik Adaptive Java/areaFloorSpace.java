// Floor-space of the room
// Residents of the Malevia country often experiment with the plan of their rooms. Rooms can be triangular, rectangular and round. To quickly calculate the floorage it is required to write a program, which gets the type of the room shape and the relevant parameters as input - the program should output the area of the resulting room.

// The value of 3.14 is used instead of the number π in Malevia.

// Input format used by the Malevians:

// triangle
// a
// b
// c
// where a, b and c — lengths of the triangle sides.

// rectangle
// a
// b
// where a and b —lengths of the rectangle sides.

// circle
// r
// where r — circle radius.

// Sample Input 1:
/*
rectangle
4
10
*/
// Sample Output 1:
/*
40.0
*/

// Sample Input 2:
/*
circle
5
*/
// Sample Output 2:
/*
78.5
*/

// Sample Input 3:
/*
triangle
3
4
5
*/
// Sample Output 3:
/*
6.0
*/

import java.util.Scanner;
import java.text.NumberFormat;

class areaFloorSpace {
  
  public static Scanner s = new Scanner(System.in);
  public static NumberFormat nf = NumberFormat.getInstance();
  public static final double PI = 3.14;    
    
  public static void main(String[] args) {
    // put your code here
      String shape = s.next();
      int[] dims;
      nf.setMaximumFractionDigits(1);
      nf.setMinimumFractionDigits(1);
      if (shape.equals("triangle")) {
          dims = readTriangle();
          int a = dims[0];
          int b = dims[1];
          int c = dims[2];
          System.out.println("TRIANGLE\n\tdims[0]:\t" + a + "\tdims[1]:\t" + b + "\tdims[2]:\t" + c);
          double areaD = solveTriangleArea(a, b, c);
          System.out.println("\nAREA\n\t" + areaD);
          String area = nf.format(areaD);
          System.out.println(area);
      }
      else if (shape.equals("rectangle")) {
          dims = readRectangle(); 
          int l = dims[0];
          int w = dims[1];    
          System.out.println("RECTANGLE\n\tdims[0]:\t" + l + "\tdims[1]:\t" + w);
          double areaD = solveRectangleArea(l, w);
          System.out.println("\nAREA\n\t" + areaD);
          String area = nf.format(areaD);
          System.out.println(area);
      }
      else if (shape.equals("circle")) {
          dims = readCircle();    
          int r = dims[0]; 
          System.out.println("CIRCLE\n\tdims[0]:\t" + r);
          double areaD = solveCircleArea(r);
          System.out.println("\nAREA\n\t" + areaD);
          String area = nf.format(areaD);
          System.out.println(area);
      }
      else {
           System.out.println("ERROR IN SHAPE\t[" + shape + "]");   
      }
      // System.out.println("a:\t" + a + "\tb:\t" + b + "\tc:\t" + c);
  }
    
  public static double solveTriangleArea(int a, int b, int c) { 
      double area = 0.0;
      double sumHalfed = (double) (a + b + c) / (double) 2;
      double partA = sumHalfed - a;
      double partB = sumHalfed - b;
      double partC = sumHalfed - c;
      System.out.println("sumHalfed:\t" + sumHalfed + "\tpartA:\t" + partA + "\tpartB:\t" + partB + "\tpartC\t" + partC);
      area = Math.sqrt(sumHalfed * partA * partB * partC);
      return area;
  }
    
  public static double solveRectangleArea(int l, int w) { 
      return (double) l * w;
  }
    
  public static double solveCircleArea(int r) { 
      return PI * Math.pow(r, 2);
  }
    
  public static int[] readTriangle() {
      int[] res = new int[3];
      int a = s.nextInt();
      int b = s.nextInt();
      int c = s.nextInt();
      res[0] = a;
      res[1] = b;
      res[2] = c;
      return res;
  }
    
  public static int[] readRectangle() {
      int[] res = new int[2];
      int l = s.nextInt();
      int w = s.nextInt();
      res[0] = l;
      res[1] = w;
      return res;
  }
    
  public static int[] readCircle() {
      int[] res = new int[1];
      int r = s.nextInt();
      res[0] = r;
      return res;
  }
}
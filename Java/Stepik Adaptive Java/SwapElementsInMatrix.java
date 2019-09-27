// 1.132 Swap the elements in matrix
// 1 out of 1 step passed
// 1 out of 1 point  received
// Adaptive mode activated
// Write a program, which inputs the rectangular matrix from a sequence of lines, ending with a line, containing the only word "end" (without the quotation marks).

// The program should output the matrix of the same size, where each elements in the position (i, j) is equal to the sum of the elements from the first matrix on the positions (i-1, j), (i+1, j), (i, j-1), (i, j+1). Boundary elements have neighbours on the opposite side of the matrix. In the case with one row or column, the element itself maybe its neighbour.

// Sample Input 1:
/*
9 5 3
0 7 -1
-5 2 9
end
*/
// Sample Output 1:
/*
3 21 22
10 6 19
20 16 -1
*/
// Sample Input 2:
/*
1
end
*/
// Sample Output 2:
/*
4
*/

import java.util.Scanner;
import java.util.ArrayList;

class SwapElementsInMatrix {
    
  public static Scanner sc = new Scanner(System.in);
    
  public static int readInt() {
      return sc.nextInt();
  }  
    
  public static String readLine() {
      return sc.nextLine();
  }
  
  public static int[][] matrixify(ArrayList<String[]> lines) {
      int n = lines.size();
      int m = lines.get(0).length;
    //   System.out.println("n:\t" + n + "\tm:\t" + m);
      int[][] matrix = new int[n][m];
      for (String[] line : lines) {
          for (int i = 0; i < line.length; i++) {
              int r = lines.indexOf(line);
              int c = i;
              String num = line[i];
              matrix[r][c] = Integer.parseInt(num);
          }
      }
      return matrix;
  }
  
  public static void printMatrix(int[][] matrix) { 
      boolean matrixFormPrint = true;
      int mL = matrix.length;
      if (mL > -1) {
          int mW = matrix[0].length;
      }
      else{
          System.out.println("MATRIX TOO SMALL");
          return;
      }
      for (int i = 0; i < mL; i++) {
          for (int j = 0; j < matrix[i].length; j++) {
              if (matrixFormPrint) {
                  System.out.print(matrix[i][j] + " ");
              }
              else {
                  System.out.println("matrix["+i+"]["+j+"]:\t" + matrix[i][j]);
              }
          }
          if (matrixFormPrint) {
              System.out.println();
          }
      }
  }
  
  public static int[][] sumNeighbours(int[][] matrix) {
      int mL = matrix.length;
      int mW;
      if (mL > -1) {
          mW = matrix[0].length;
      }
      else{
          System.out.println("MATRIX TOO SMALL");
          return new int[0][0];
      }
      int[][] summedNeighboursMatrix = new int[mL][mW];
      for (int i = 0; i < mL; i++) {
          for (int j = 0; j < mW; j++) {
              int n = i - 1;
              int e = j + 1;
              int s = i + 1;
              int w = j - 1;
              if (n < 0) {
                  n = mL - 1;
              }
              if (e >= mW) {
                  e = 0;
              }
              if (s >= mL) {
                  s = 0;
              }
              if (w < 0) {
                  w = mW - 1;
              }
            //   System.out.println("matrix["+i+"]["+j+"]:\t" + matrix[i][j]);
              summedNeighboursMatrix[i][j] = matrix[n][j] + matrix[i][e] + matrix[s][j] + matrix[i][w];
          }
      }
      return summedNeighboursMatrix;
  }
  
  public static void main(String[] args) {
    // put your code here
    String input = "";
    ArrayList<String[]> matrixInput = new ArrayList<String[]>();
    while (!input.equals("end")) {
        input = readLine();
        // System.out.println("line:\t" + input);
        String[] nums = input.split(" ", 0);
        for (String n : nums) {
            // System.out.println("n:\t" + n);
        }
        if (!input.equals("end")) {
            matrixInput.add(nums);
        }
        // System.out.println("-" + String.split(input, " "));
    }
    int[][] matrix = matrixify(matrixInput);
    // printMatrix(matrix);
    int[][] summedNeighboursMatrix = sumNeighbours(matrix);
    printMatrix(summedNeighboursMatrix);
  }
}
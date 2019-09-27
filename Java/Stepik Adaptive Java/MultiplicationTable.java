// Multiplication table

// When Paul studied at school, he memorized the multiplication table by rectangular blocks. For his practice it would be very nice to have a program, which outputs a block of the multiplication table.

// Write a program, which gets four numbers a, b, c and d as input, each on its own line. The program should output a fragment of multiplication table for all numbers of the interval [a;b] by all numbers of the interval [c;d].

// Numbers a, b, c and d are natural ones and do not exceed 10, a≤b, c≤d.

// Follow the output format from the example, use '\t' (tab character) to separate elements inside the line. Adding a space instead of line break is performed by the "end" parameter of the print function:

// print(x, end=" ")
// Please output the numbers from the specified intervals themselves in the left column and the top row (as headers).

// Sample Input 1:
/*
7
10
5
6
*/
// Sample Output 1:
/*
	5	6
7	35	42
8	40	48
9	45	54
10	50	60
*/
// Sample Input 2:
/*
5
5
6
6
*/
// Sample Output 2:
/*
	6
5	30
*/
// Sample Input 3:
/*
1
3
2
4
*/
// Sample Output 3:
/*
	2	3	4
1	2	3	4
2	4	6	8
3	6	9	12
*/

import java.util.Scanner;

class MultiplicationTable {
    
  public static Scanner sc = new Scanner(System.in);
    
  public static int readInt() {
      return sc.nextInt();
  }  
    
  public static String readLine() {
      return sc.next();
  }
 
  public static void main(String[] args) {
    // put your code here
    int y0 = readInt();
    int y1 = readInt();
    int x0 = readInt();
    int x1 = readInt();
      
    for (int i = y0 - 1; i <= y1; i++) {
        String line = "";
        for (int j = x0 - 1; j <= x1; j++) {
            if (i == y0 - 1) {
                if (j == x0 - 1) {
                    line += "\t";        
                }
                else{
                    line += j + "\t";
                }
            }
            else if (j == x0 - 1) {
                line += i + "\t";   
            }
            else {
                line += i*j + "\t";   
            }
        }
        System.out.println(line);
    }
  }
}
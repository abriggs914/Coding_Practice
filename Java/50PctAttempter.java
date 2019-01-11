/*package whatever //do not write package name here */
/**
 * Java Program to determine the success rate of the 37% selection algorithm.
 * Program takes a the number of variables and tests all possibilities for a
 * successful outcome.
*/

import java.io.*;
import java.util.Scanner;

class GFG {
	public static void main (String[] args) {
		System.out.println("GfG!");
		int a,b,c,d, temp1;
		Scanner scan = new Scanner(System.in);
    	temp1 = scan.nextInt();
		/*while(temp1 != 0){
    		a = temp1/1000;
    		b = (temp1%1000)/100;
    		c = (temp1%100)/10;
    		d = temp1%10;
		    System.out.println("\na: " + a + "\nb: " + b + "\nc: " + c + "\nd: " + d);
    	    temp1 = scan.nextInt();
    	    
		}*/
		if(temp1 < 9 && temp1 >= 0){
		    int[] possibilities = new int[fact(temp1)];
		    boolean[] successful = new boolean[possibilities.length];
		    placement(possibilities, temp1, 0);
		}
		else{
		    System.out.println("Number entered is out of bounds. " +
		    "Keep in mind we are taking the factorial of the number, " +
		    "so make it small.");
		}
	}
	
	public static int fact(int n){
        int i, fact = 1;
        for(i = 1; i <= n; i++){
            fact = fact * i;
        }
        return fact;
    }
    
    public static void placement(int[] arr, int n, int section){
        int m = n-1;
        int p, z;
		int a = section+1, b = 0, c = 3, d = 4, temp1;
		if(a != 1){
		    b = 1;
		}
		else{
		    b = 2;
		}
		if(a == 3 || a == 4){
		    c = 2;
		}
		if(a == 4){
		    d = 3;
		}
		System.out.println("\na: " + a + "\nb: " + b + "\nc: " + c + "\nd: " + d);
        if(n == 0){
            return;
        }
        else if(n == 1){
            arr[0] = 1;
            return;
        }
        z = fact(n-1);
        int y = z*section;
        System.out.println("ENTER FOR Section: " + section + "\n\n");
		for(int i = 0 + y; i < (z + y)-1; i++){
		    arr[i] = a*1000 + b*100 + c*10 + d;
		    System.out.println("arr["+i+"]:" + arr[i]);
		    temp1 = c;
		    c = d;
		    d = temp1;
		    if((i)%3 == 2){
		        temp1 = d;
		        d = b;
		        b = temp1;
		    }
		    System.out.println("\na: " + a + "\nb: " + b + "\nc: " + c + "\nd: " + d + "\ni: " + i);
		    if(i >= arr.length){
		        return;
		    }
		}
        System.out.println("EXIT FOR Section: " + section + "\n\n");
		section++;
		if(((z*(section))) >= arr.length){
		    return;
		}
		else{
		    placement(arr, n, section);
		}
    }
}
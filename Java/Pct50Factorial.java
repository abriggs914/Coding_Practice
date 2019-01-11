/*package whatever //do not write package name here */

/*
*   Java program to take an input n from the user, and print out every
*   arrangement of n letters.
*
*/


import java.io.*;
import java.util.Scanner;


class Pct50Factorial {
	public static void main (String[] args) {
		//System.out.println("GfG!");
		Scanner scan = new Scanner(System.in);
		int n; 
		int a, b, comp, comp2;
		String[] finalArr;
		char[] ar;
		boolean started;
		System.out.println("How many letters would you like to see? (2-8)");
		try{
			n = Integer.parseInt(scan.nextLine());
		}
		catch(Exception e){
			n = 2;
		}
		System.out.println("Which letter would you like to start at? (default: A)");
		String line = scan.nextLine();
		if(n > -1 && n < 9){
		    a = fact(n);
		    b = fact(n-1);
		    comp2 = 0;
		    comp = 0;
		    finalArr = new String[a];
		    initializeArr(finalArr);
		    ar = setCharArray(n, line);
		    //printCharArr(ar);
		    started = startArrFill(finalArr, n, ar);
		    //printStringArr(finalArr);
		    finishArray(finalArr, ar, true);
		    finishArray(finalArr, ar, false);
		    printStringArr(finalArr);
		}
		else if(n > 8){
		    System.out.println("Number is too big.");
		    return;
		}
		else{
		    System.out.println("Number is negative.");
		    return;
		}
		if(started){
		    //System.out.println("GfG!");
			return;
		}
	}
	
	/*
	* Method populates String array with blank strings
	*/
	public static void initializeArr(String[] arr){
	    for(int i = 0; i < arr.length; i++){
	        arr[i] = "";
	    }
	}
	
	/*
	* Method produces the factorial of int n recursively
	*/
	public static int fact(int n){
	    if(n < 0){
	       return 0;
	    }
	    if(n == 0 || n == 1){
	        return 1;
	    }
	    else{
	        return n*fact(n-1); 
	    }
	}
	
	/*
	* Method populates char array for letter referencing
	*/
	public static char[] setCharArray(int n, String line){
	    char t = line.charAt(0); 
	    char[] arr = new char[n];
	    if(t < 123 && t > 96){
	        line = line.toUpperCase();
	        t = line.charAt(0);
	    }
	    if(t > 90 || t < 65){
	        t = (char)65;
	    }
	    for(int i = 0, j = t; i < n; i++, j++){
	        arr[i] = (char)j;
	        if(j == 90){
	            j = 64;
	        }
	    }
	    return arr;
	}
	
	/*
	* Method prints a paramerterized char arr
	*/
	public static void printCharArr(char[] arr){
	    for(int i = 0; i < arr.length; i++){
	        System.out.println(arr[i]);
	    }
	}
	
	/*
	* Method prints a paramerterized string arr
	*/
	public static void printStringArr(String[] arr){
	    for(int i = 0; i < arr.length; i++){
	        System.out.println(arr[i]);
	    }
	}
	
	/*
	* Method returns true if a paramerterized char is in
	* a given paramerterized string
	*/
	public static boolean contains(String string, char letter){
	    boolean bool = false;
	    for(int i = 0; i < string.length(); i++){
	        if(string.charAt(i) == letter){
	            bool = true;
	        }
	    }
	    return bool;
	}
	
	/*
	* Method populates the total possibilities array.
	* Only does columns that aren't the last 2 (fact(n) == 1)
	*/
	public static boolean startArrFill(String[] strings, int n, char[] chars){
	    int comp = 0, comp2 = 0, b = fact(n-1), c = n-1, comp3 = 0;
	    for(int j = comp2; b != 1; j++){
    	    for(int i = 0; i < strings.length; i++){
    	        while(contains(strings[i], chars[comp2])){
    	            comp2++;
    	            if(comp2 == chars.length){
    	                comp2 = 0;
    	            }
    	        }
    	        //System.out.println("comp2: " + comp2 + ", chars[comp2]: " + chars[comp2]);
    	        strings[i] += chars[comp2];
    	        //System.out.println("i: " + i + ", j: " + j + "\t" +strings[i]);
    	        comp++;
    	        if(comp == b){
    	            comp2++;
    	            comp = 0;
    	            if(comp2 == chars.length){
    	                comp2 = 0;
    	            }
    	        }
    	    }
    	    c--;
    	    b = fact(c);
	    }
	    //System.out.println("b: " + b);
	    return true;
	}
	
	/*
	* Method finalizes possibilities array with letters
	*/
	public static void finishArray(String[] strings, char[] chars, boolean mode){
	    int comp2 = 0;
	    for(int i = 0; i < strings.length; i++){
	        while(contains(strings[i], chars[comp2])){
    	        comp2++;
    	        if(comp2 == chars.length){
    	            comp2 = 0;
    	        }
    	    }
    	    //System.out.println("strings[i]: " + strings[i] + ", chars["+comp2+"]: " + chars[comp2]);
    	    strings[i] += chars[comp2];
    	    if(mode){
    	        comp2++;
        	    if(comp2 == chars.length){
        	        comp2 = 0;
        	    }
    	        while(contains(strings[i], chars[comp2])){
    	            comp2++;
        	        if(comp2 == chars.length){
        	            comp2 = 0;
        	        }
    	        }
    	        strings[i+1] += chars[comp2];
    	        i++;
    	    }
	    }
	}
}
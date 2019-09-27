/*package whatever //do not write package name here */

import java.io.*;
import java.util.*;

class GFG {
	public static void main (String[] args) {
		ArrayList<Integer> a = new ArrayList<>();
		a.add(-1);
		a.add(5);
		a.add(7);
		a.add(0);
		a.add(-1);
		a.add(15);
		ArrayList<Integer> b = new ArrayList<>();
		b.addAll(a);
		System.out.println("Part A");
		System.out.println("a:\t" + a);
		System.out.println("b:\t" + b);
		System.out.println();
		System.out.println("Part B");
		ArrayList<Integer> c = removeIndexes(a, new ArrayList<Integer>(Arrays.asList(1,2,3)));
		System.out.println("a:\t" + a);
		System.out.println("c:\t" + c);
		System.out.println("b:\t" + b);
		System.out.println();
		System.out.println("Part C");
		ArrayList<Integer> d = removeIndexes(a, new ArrayList<Integer>(Arrays.asList()));
		System.out.println("a:\t" + a);
		System.out.println("c:\t" + c);
		System.out.println("d:\t" + d);
		System.out.println("b:\t" + b);
		System.out.println();
	}
	
	public static ArrayList<Integer> removeIndexes(ArrayList<Integer> a, ArrayList<Integer> lst) {
	    ArrayList<Integer> cpy = new ArrayList<Integer>();
	    cpy.addAll(a);
	    int s = cpy.size();
        Collections.sort(lst); 
        Collections.reverse(lst);
	    for (int idx : lst) {
	        if (s > idx) {
	            cpy.remove(idx);
	            s = cpy.size();
	            
	           // removeLst.add(a.get(idx));
	        }
	    }
	   // a.clear();
	   // a.addAll(cpy);
	    return cpy;
	}
}
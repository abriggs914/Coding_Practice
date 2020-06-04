/*package whatever //do not write package name here */

import java.io.*;

public interface Interface {
    String printIt(String text);
    public static String x(String text) {
        System.out.println("x: " + text);
        return text;
    }
}

class GFG {
	public static void main (String[] args) {
		System.out.println("GfG!");
		doStuff();
	}
	
	public static void doStuff() {
	    Interface i = (String t) -> {
	        System.out.println("Printing: " + t);
	        return t;
	    };
	    
	    System.out.println("i: " + i);
	    System.out.println("i: " + i.printIt("String"));
	    System.out.println("i(x): " + Interface.x("String"));
	   // i("String");
	}
}

/*  Output

GfG!
i: GFG$$Lambda$1/250421012@119d7047
Printing: String
i: String
x: String
i(x): String

*/
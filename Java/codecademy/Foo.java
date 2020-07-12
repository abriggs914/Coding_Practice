/*package whatever //do not write package name here */

import java.io.*;
import java.util.*;

class Foo {
    
    private Foo foo;
    private static int[] counts = new int[4];
    
    public Foo() {
        foo = foo();
        counts[0]++;
    }
    
    public Foo FOO(){
        System.out.println("Foo");
        counts[1]++;
        return foo;
    }
    
    public Foo FOO(String FOO) {
        counts[2]++;
        return FOO();
    }
    
    public Foo foo() {
        counts[3]++;
        return this;
    }
    
	public static void main (String[] args) {
		Foo foo = new Foo().foo.FOO().FOO("FOO").foo.foo.foo.FOO();
		foo.FOO("FOO").foo.foo.FOO().foo.FOO("FOO").FOO().foo.FOO();
		System.out.println(Arrays.toString(counts));
	}
}
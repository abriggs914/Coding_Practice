/*
*	Exception class for Go Fish
*	Aug 2018
*
*/

public class OutOfBoundsException extends Exception{
	public OutOfBoundsException(){
		System.out.println("\n\n\tHandsize is out of bounds.\n\tSetting to 5.");
	}
}
/**
Sorter class provides methods for sorting lists.
Adapted from Java Software Solutions 9th Ed, Lewis & Loftus 
*/

public class Sorter<T extends Comparable<T>>{
	
	/**
	Sorts the specified array using selection sort algorithm.
	@param list The array of objects to sort.
	*/
	public void selectionSort(T[] list){
		int min; 
		T temp;
		
		for(int index = 0; index < list.length-1; index++){
			min = index;
			for(int scan = index+1; scan < list.length; scan++)
				if(list[scan].compareTo(list[min]) < 0)
					min = scan;
					
			temp = list[min];
			list[min] = list[index];
			list[index] = temp;
		}
	}
	
}
	

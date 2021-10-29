import java.util.ArrayList;

public class Item {
	
	private String name;
	private ArrayList<String> coloursList;
	
	public Item(String name, ArrayList<String> coloursList) {
		this.name = name;
		this.coloursList = new ArrayList<>(coloursList);
	}
	
	
	public String toString() {
		return this.name;
	}

	public ArrayList<String> getColoursList() {
		return coloursList;
	}

	public void setColoursList(ArrayList<String> coloursList) {
		this.coloursList = coloursList;
	}
}
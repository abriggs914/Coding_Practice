public class clear_terminal{
	public static void main(String[] args){
		String[] abc = new String[26];
		for(int i = 0; i < 26; i++){
			abc[i] = ((char)(i+65) + "\33");
		}
		for(int i = 0; i < 26; i++){
			//System.out.println("100");
			System.out.println("\33"+abc[i]);
		}		
	}
}
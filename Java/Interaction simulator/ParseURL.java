import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.io.FileWriter;
import java.util.ArrayList;

/*
	Java file to handle webpage scraping and writing scraped contents to a file.
	
	July 2020
*/

public class ParseURL{
	
	/*
		Writes the contents of a parsed page to the given file.
		@param content		A list of parsed content line-by-line.
		@param filename		The destination filename.
	*/
	public static void readPageWriteFile(ArrayList<String> content, String filename){			
		try {
			FileWriter myWriter = new FileWriter(filename);
			for (String line: content){
				myWriter.write(line + "\n");
			}
			
			myWriter.close();
			System.out.println("Successfully wrote to the file.");
		} 
		catch (IOException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
	}
	
	/*
		Read a given URL and return the contents. Can also write to a file if desired.
		@param url			The address to the page to read.
		@param writeToFile	Boolean value indicating if file writing is desired.
		@param filename		The file to write to, can be empty or null if no file writing is desired.
		@return				The parsed content in a string format.
	*/
	public static String readPage(URL url, boolean writeToFile, String filename){
		// Get the input stream through URL Connection
		String line = null;
		try {
			
			URLConnection con = url.openConnection();
			InputStream is = con.getInputStream();
			
			BufferedReader br = new BufferedReader(new InputStreamReader(is));
			ArrayList<String> content = new ArrayList<>();
			int i = 0;
			while ((line = br.readLine()) != null) {
				content.add(line);
				// myWriter.write(line + "\n");
			}
			
			System.out.println("Successfully read the page.");
			if (writeToFile) {
				readPageWriteFile(content, filename);
			}
			line = join(content);
		} 
		catch (IOException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
		
		return line;
	}
	
	/*
		Join an ArrayList of strings separated by new lines.
		@param content		The list of strings to be joined.
		@return				The concatenated string.
	*/
	public static String join(ArrayList<String> content) {
		String result = "";
		for (String line: content) {
			result += line + "\n";
		}
		return result;
	}

    public static void main(String[] args) throws IOException {

        // Make a URL to the web page
        URL url = new URL("https://www.worldometers.info/coronavirus/");
		
		String data = readPage(url, false, "");
		System.out.println("data parsed:\n" + data);
    }
}
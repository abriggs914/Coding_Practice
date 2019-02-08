import java.io.*;
import java.util.*;
import java.util.regex.*;

/**
 * A Java implementation of Norvig's spell checker. Norvig's paper and Python spell
 * checker can be found at: http://www.norvig.com/spell-correct.html
 * This Java version from: http://raelcunha.com/spell-correct.php
 *
 * The goal of the author was to write a short spell checker. On the web page
 * (without comments) it was 35 non-blank lines.
 *
 * Comments and modifications by Scot Drysdale
 * @author Rael Cunha
 */
class Spelling {


  public static String[] types = {"Normal","Fight","Flying","Poison","Ground",
                                  "Rock","Bug","Ghost","Steel","Fire","Water",
                                  "Grass","Electric","Psychic","Ice","Dragon",
                                  "Dark"};
  private HashMap<String, Integer> nWords;
  public String[] allPokemonNames = new String[908];
  public static String[][] allPokemon;
  public static Spelling corrector;

  /**
   * Constructs a new spell corrector.  Builds up a map of correct words with
   * their frequencies, based on the words in the given file.
   *
   * @param file the text to process
   * @throws IOException
   */
  public Spelling(String file) throws IOException {
    nWords = new HashMap<String, Integer>();
    BufferedReader in = new BufferedReader(new FileReader(file));

    // This pattern matches any word character (letters or digits)
    Pattern p = Pattern.compile("\\w+");
    for(String temp = ""; temp != null; temp = in.readLine()){
      Matcher m = p.matcher(temp.toLowerCase());
      // find looks for next match for pattern p (in this case a word).  True if found.
      // group then returns the last thing matched.
      // The ? is a conditional expression.
      while(m.find())
        nWords.put((temp = m.group()), nWords.containsKey(temp) ? nWords.get(temp) + 1 : 1);
    }
    in.close();
  }

  /**
   * Constructs a list of all words within edit distance 1 of the given word.
   * @param word the word to construct the list from
   * @return a list of words with in edit distance 1 of word
   */
  private ArrayList<String> edits(String word) {
    ArrayList<String> result = new ArrayList<String>();

    // All deletes of a single letter
    for(int i=0; i < word.length(); ++i)
      result.add(word.substring(0, i) + word.substring(i+1));

    // All swaps of adjacent letters
    for(int i=0; i < word.length()-1; ++i)
      result.add(word.substring(0, i) + word.substring(i+1, i+2) +
                 word.substring(i, i+1) + word.substring(i+2));

    // All replacements of a letter
    for(int i=0; i < word.length(); ++i)
      for(char c='a'; c <= 'z'; ++c)
        result.add(word.substring(0, i) + String.valueOf(c) + word.substring(i+1));

    // All insertions of a letter
    for(int i=0; i <= word.length(); ++i)
      for(char c='a'; c <= 'z'; ++c)
        result.add(word.substring(0, i) + String.valueOf(c) + word.substring(i));

    return result;
  }

  /**
   * Corrects the spelling of a word, if it is within edit distance 2.
   * @param word the word to check/correct
   * @return word if correct or too far from any word; corrected word otherwise
   */
  public String correct(String word) {
    // If in the dictionary, return it as correctly spelled
    if(nWords.containsKey(word))
      return word;

    ArrayList<String> list = edits(word);  // Everything edit distance 1 from word
    HashMap<Integer, String> candidates = new HashMap<Integer, String>();

    // Find all things edit distance 1 that are in the dictionary.  Also remember
    //   their frequency count from nWords.
    // (Note if equal frequencies the last one will be the one remembered.)
    for(String s : list)
      if(nWords.containsKey(s))
        candidates.put(nWords.get(s),s);

    // If found something edit distance 1 return the most frequent word
    if(candidates.size() > 0)
      return candidates.get(Collections.max(candidates.keySet()));

    // Find all things edit distance 1 from everything of edit distance 1.  These
    // will be all things of edit distance 2 (plus original word).  Remember frequencies
    for(String s : list)
      for(String w : edits(s))
        if(nWords.containsKey(w))
          candidates.put(nWords.get(w),w);

    // If found something edit distance 2 return the most frequent word.
    // If not return the word with a "?" prepended.  (Original just returned the word.)
    return candidates.size() > 0 ?
        candidates.get(Collections.max(candidates.keySet())) : "" + word;
  }

  /**
   * Original version read a single word to correct from the command line.
   * It is commented out below
   * @throws IOException
   */

/*
   public static void main(String args[]) throws IOException {
    if(args.length > 0) System.out.println((new Spelling("big.txt")).correct(args[0]));
  }
*/

   public static void main(String args[]) throws IOException {
     corrector = new Spelling("./pokedex.txt");
     Scanner input = new Scanner(System.in);
     allPokemon = parseCSV();

     System.out.println("Enter words to correct");
     String word = input.next();

     while(true) {
       String[] temp = new String[2];
       temp[0] = corrector.correct(word);
       temp[1] = typesFromNameFromInput(word);
       temp = capitalizeStringArray(temp);
       System.out.println(word + " is corrected to " + temp[0] + ", types: " + temp[1]);
       word = input.next();
     }
   }

   public static String[] capitalizeStringArray(String[] arr) {
       int j = 0, k;
       for(String item : arr){
           int size = item.length();
           if(size > 0) {
               char firstLetter = Character.toUpperCase(item.charAt(0));
               StringBuilder line = new StringBuilder(Character.toString(firstLetter));
               for (k = 1; k < size; k++) {
                   line.append(Character.toString(item.charAt(k)));
               }
               item = line.toString();
               arr[j] = item;
               j++;
           }
       }
       return arr;
   }

   private static String typesFromNameFromInput(String nameInput) {
        StringBuilder result = new StringBuilder();
        for(int i = 0; i < allPokemon.length; i++){
            if(allPokemon[i][0].equals(nameInput)){
                String secondType = ((allPokemon[i][2].equals("None")? "" : allPokemon[i][2]));
                result.append(allPokemon[i][1]).append(",").append(secondType);
                break;
            }
        }
        String line = result.toString();
        System.out.println("\nLine: "+line+"\n");
        if(line.length() < 2){
            return "";
        }
        else {
            //TextView resultsMessageDisplay = (TextView) findViewById(R.id.results_window);
            //resultsMessageDisplay.setText("Processing");
            String res = corrector.correct(line);
            if(isPokemonName(line)){
              return line;
            }
            return "NOT A VALID NAME";
        }
    }

    public static String[][] parseCSV() {
         String csvFile = "./pokedex.csv";
         String line;
         String[][] pokemonArr = new String[909][1];
         BufferedReader br = null;
         int curr = 0;
         try {
             br = new BufferedReader(new FileReader(csvFile));
             while ((line = br.readLine()) != null) {
                 // use comma as separator
                 String[] pokemon = line.split(",");
                 pokemonArr[curr] = pokemon;
                 curr++;
             }

         } catch (FileNotFoundException e) {
             //e.printStackTrace();
         } catch (IOException e) {
             //e.printStackTrace();
         } finally {
             if (br != null) {
                 try {
                     br.close();
                 } catch (IOException e) {
                     //e.printStackTrace();
                 }
             }
         }
         return pokemonArr;
     }

     public static boolean isPokemonName(String line){
       List<String> list = Arrays.asList(types);
       String[] regions = {"Kanto","Johto","Hoenn","Sinnoh",
                           "Unova","Kalos","Alola"};
       if(list.contains(line)){
           return false;
       }
       list = Arrays.asList(regions);
       if(list.contains(line)){
         return false;
       }
       return true;
     }


}

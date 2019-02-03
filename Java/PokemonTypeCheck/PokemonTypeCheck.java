import java.util.*;
import java.io.*;

public class PokemonTypeCheck{

  public static String[][] allPokemon;

  public static void main(String[] args){

    String[] types = {"Normal","Fight","Flying","Poison","Ground","Rock","Bug",
                      "Ghost","Steel","Fire","Water","Grass","Electric",
                      "Psychic","Ice","Dragon","Dark"};
    // each row corresponds to a type. The first column
    // identifies the type for that row, each type after
    // column 1, is a type that would be a good match up
    // for the row-type.
    // I.E. Fighting type attackS will be super effective
    // against Ice or Dark types
    String[][] strongATTK =
                {{"Normal"},
                {"Fight","Normal","Rock","Steel","Ice","Dark"},
                {"Flying","Fight","Bug","Grass"},
                {"Poison","Grass"},
                {"Ground","Poison","Rock","Steel","Fire","Electric"},
                {"Rock","Flying","Bug","Fire","Ice"},
                {"Bug","Grass","Psychic","Dark"},
                {"Ghost","Ghost","Psychic"},
                {"Steel","Rock","Ice"},
                {"Fire","Bug","Steel","Grass","Ice"},
                {"Water","Ground","Rock","Fire"},
                {"Grass","Ground","Rock","Water"},
                {"Electric","Flying","Water"},
                {"Psychic","Fight","Poison"},
                {"Ice","Flying","Ground","Grass","Dragon"},
                {"Dragon","Dragon"},
                {"Dark","Ghost","Psychic"}};

// each row corresponds to a type. The first column
// identifies the type for that row, each type after
// column 1, is a type that would be a good match up
// for the row-type.
// I.E. Fighting type DEFENCE will be super effective
// against Bug or Dark types
    String[][] strongDEF =
                {{"Normal"},
                {"Fight","Rock","Bug","Dark"},
                {"Flying","Fight","Bug","Grass"},
                {"Poison","Fight","Poison","Bug","Grass"},
                {"Ground","Poison","Rock"},
                {"Rock","Normal","Flying","Poison","Fire"},
                {"Bug","Fight","Ground","Grass"},
                {"Ghost","Poison","Bug"},
                {"Steel","Normal","Flying","Rock","Bug","Ghost","Steel",
                  "Grass","Psychic","Ice","Dragon","Dark"},
                {"Fire","Bug","Steel","Fire","Grass","Ice"},
                {"Water","Steel","Fire","Water","Ice"},
                {"Grass","Ground","Water","Grass","Electric"},
                {"Electric","Flying","Steel","Electric"},
                {"Psychic","Fight","Psychic"},
                {"Ice","Ice"},
                {"Dragon","Fire","Water","Grass","Electric"},
                {"Dark","Ghost","Dark"}};

    printArr(types);
    print2DArr(strongATTK);
    System.out.println("BEST TYPES");
    String[] currTypes = {"Fire"};
    String[] bestTypesToUse = bestTypes(strongATTK, currTypes);
    printArr(bestTypesToUse);
    Scanner scan = new Scanner(System.in);
    String line = scan.nextLine();
    System.out.println("BEST TYPES");
    currTypes = decipher(line, types);
    bestTypesToUse = bestTypes(strongATTK, currTypes);
    printArr(bestTypesToUse);
    allPokemon = parseCSV();
    System.out.println(allPokemon[1][2]);
    capitalizeTypeNames();
    //print2DArr(allPokemon);
    String[] a = "hey there how are you".split(" ");
    printArr(a);
    //allPokemon[1][2].charAt(0) = Character.toUpperCase(allPokemon[1][2].charAt(0));
  }

  /*
  * bestTypes() takes in a 2D array of types and their strong
  * attack effectiveness(strongATTK), and a list of types that
  * a current pokemon that wants to attack.
  * returns a list of the best types for this currently attacking
  * pokemon to attack (Highest DMG multiplier).
  */
  public static String[] bestTypes(String[][] types, String[] currPokemonTypes){
    String[] result = new String[0];
    // loop current pokemon types
    for(int i = 0; i < currPokemonTypes.length; i++){
      // loop 2D array looking at the first column
      for(int j = 0; j < types.length; j++){
        // if the types match record all other types in that row
        if(types[j][0].equals(currPokemonTypes[i])){
          int size = types[j].length-1;
          int resSize = result.length;
          int l, k = 0;
          String[] temp = new String[resSize + size];
          // first type
          if(i == 0){
            for(l = 1; l < size+1; l++,k++){
              temp[k] = types[j][l];
            }
          }
          // more than one type
          else{
            for(k = 0; k < resSize; k++){
              temp[k] = result[k];
            }
            for(l = 1; l < size+1; l++,k++){
              temp[k] = types[j][l];
            }
          }
          result = temp;
        }
      }
    }
    // remove all duplicate types accumulated
    result = removeDuplicates(result);
    return result;
  }

  /*
  * removeDuplicates takes in an array of strings, and returns a
  * new array of every unique string in the original array.
  */
  public static String[] removeDuplicates(String[] arr){
    return new HashSet<String>(Arrays.asList(arr)).toArray(new String[0]);
  }

  public static String[] decipher(String line, String[] types){
    String[] result = new String[1];
    boolean earlyExit = true;
    int len = line.length(), curr = 0;
    earlyExit = len > 15;
    earlyExit = earlyExit || (line.indexOf(",") == -1 && len > 8);
    if(earlyExit){ // earlyExit conditions met
      return result;
    }
    String typeToAdd = "";
    int i;
    for(i = 0; i < len; i++){
      if(line.charAt(i) != ',' && line.charAt(i) != ' '){
        typeToAdd += line.charAt(i);
      }
      if(line.charAt(i) == ',' || i == len-1){
        if(curr > 0){
          String[] arr = new String[result.length+1];
          System.arraycopy(result, 0, arr, 0, result.length); // copies an array
          result = arr;
        }
        for (String type : types) {
          if (type.equals(typeToAdd)) {
            result[curr] = typeToAdd;
            curr++;
            break;
          }
        }
        typeToAdd = "";
      }
    }
    return result;
  }

  public static void printArr(String[] arr){
    System.out.println("\tBEGIN ARRAY");
    for(int i = 0; i < arr.length; i++){
      System.out.println(arr[i]);
    }
    System.out.println("\tEND ARRAY n="+arr.length+" items");
  }

  public static void print2DArr(String[][] arr){
    System.out.println("\tTypes");
    boolean bool = false;
    for(String[] type : arr){
      System.out.println(type[0]);
      for(String a : type){
        if(!a.equals(type[0]) || bool){
          bool = true;
          System.out.println("\t"+a);
        }
      }
      bool = false;
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

   public static void capitalizeTypeNames() {
       int i, j, k;
       for(i = 0; i < allPokemon.length; i++){
           for(j = 0; j < allPokemon[i].length; j++){
               char firstLetter = Character.toUpperCase(allPokemon[i][j].charAt(0));
               String line = Character.toString(firstLetter);
               for(k = 1; k < allPokemon[i][j].length(); k++){
                   line += Character.toString(allPokemon[i][j].charAt(k));
               }
               allPokemon[i][j] = line;
           }
       }
   }

}

import java.io.FileReader;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.util.ArrayList;

public class CollectionIndexer{

  public static void main(String[] args){
    String fileName = "./Collection2.csv";
    readFile(fileName);
  }

  public static void readFile(String fileName){
    int c = 0;
    int s = 0;
    int semiColons = 0;
    ArrayList<String> lines = new ArrayList<String>();
    try{
      FileReader file = new FileReader(fileName);
      BufferedReader br = new BufferedReader(file);
      String line = "";
      while((line = br.readLine()) != null && c < 10){
        if(c > 0){
          // System.out.println(line);
          // s += Integer.parseInt(line.subSequence(0, 1).toString());
          int sc = countSemiColons(line);
          String temp = line;
          while(sc < 13){
            int i = 0;
            line = br.readLine();
            temp += line;
            sc = countSemiColons(temp);
            sc = adjustSCForInput(sc, c, i);
            System.out.println("sc: " + sc + ", c: " + c);
            i++;
          }
          System.out.println("\ttemp: " + temp+"\n");
          lines.add(temp);
        }
        c++;
      }
      System.out.println(c + " lines");
      System.out.println("s: " + s);
      System.out.println("semiColons: " + semiColons);
    }
    catch (Exception e) {
      System.out.println("ERROR, C: " + c);
    }
  }

  public static int adjustSCForInput(int s, int c, int i){
    switch(c){
      case  1 : return s - 1;
      case  2 : return ((i == 0)? (s - 1) : s);
      default : return s;
    }
  }

  public static int countSemiColons(String line){
    int semiColons = 0;
    // System.out.println("line: " + line);
    for(int i = 0; i < line.length(); i++){
      if(line.charAt(i) == ';'){
        semiColons++;
      }
    }
    // System.out.println("semiColons: " + semiColons);
    return semiColons;
  }
}

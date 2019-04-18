import java.util.FileReader;
import java.util.BufferedReader;
import java.util.FileInputStream;

public class CollectionIndexer{

  public static void main(String[] args){
    String fileName = "./Collection2.csv";
    readFile(fileName);
  }

  public static void readFile(String fileName){
    try{
      File file = new FileInputStream(fileName);
      BufferedReader br = new BufferedReader(new FileReader(file));
      String line = "";
      while((line = br.readLine()) != null){
        System.out.println(line);
      }
    }
  }
}

import java.util.*;

public class PokemonTypeCheck{

  public static void main(String[] args){
    String[] types = {"Normal","Fight","Flying","Poison","Ground","Rock","Bug",
                      "Ghost","Steel","Fire","Water","Grass","Electric",
                      "Psycic","Ice","Dragon","Dark"};
    String[][] strongATTK =
                {{"Normal"},
                {"Fight","Normal","Rock","Steel","Ice","Dark"},
                {"Flying","Fight","Bug","Grass"},
                {"Poison","Grass"},
                {"Ground","Poison","Rock","Steel","Fire","Electric"},
                {"Rock","Flying","Bug","Fire","Ice"},
                {"Bug","Grass","Psycic","Dark"},
                {"Ghost","Ghost","Psycic"},
                {"Steel","Rock","Ice"},
                {"Fire","Bug","Steel","Grass","Ice"},
                {"Water","Ground","Rock","Fire"},
                {"Grass","Ground","Rock","Water"},
                {"Electric","Flying","Water"},
                {"Phscic","Fight","Poison"},
                {"Ice","Flying","Ground","Grass","Dragon"},
                {"Dragon","Dragon"},
                {"Dark","Ghost","Psycic"}};
    for(int i = 0; i < types.length; i++){
      System.out.println(types[i]);
    }
    System.out.println();
    boolean bool = false;
    for(String[] type : strongATTK){
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

}

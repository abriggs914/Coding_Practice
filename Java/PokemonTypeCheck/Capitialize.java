public class Capitialize{

  public static void main(String[] args){
    String[] arr = {"avery","Briggs","","0"};
    arr = capitalizeStringArray(arr);
    for(String item : arr){
     System.out.println(item);
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
            }
            else{
              item =  "";
            }
            arr[j] = item;
            j++;
        }
        return arr;
  }
}

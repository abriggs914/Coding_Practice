public class FizzBuzz {
  
  public static void main(String[] args) {
    int start = 1;
    int end = 100;
    for (int i = start; i < end + 1; i++) {
      String res = "";
      if (i % 3 == 0) {
        res += "Fizz";
      }
      if (i % 5 == 0) {
        res += "Buzz";
      }
      if (res.equals("")) {
        res = Integer.toString(i);
      }
      System.out.println(res);
    }
  }  
}
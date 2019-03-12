
public class CardException extends Exception{

  public CardException(String message){
    System.out.println(message);
    if(message.equals("hey")){
      HORBException();
    }
    System.out.println("Exception constructor");
  }

  public static void HORBException(){
    System.out.println("Invalid card status identifier entered");
  }

}

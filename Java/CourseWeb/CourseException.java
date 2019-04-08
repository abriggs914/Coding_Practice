
public class CourseException extends Exception{

  public CourseException(String errorMessage){
    if(errorMessage.equals("PLMS")){
      inValidGrade();
    }
  }

  public void inValidGrade(){
    System.out.println("Invalid grade given.");
  }
}

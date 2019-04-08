
import java.util.ArrayList;

public class Course{

  private int numCoursesTaken = 0;

  private String name;
  private String dept;
  private String grade;
  private int courseNum;
  private int courseHours;
  private int chronologicalIndex;
  private double courseValue;
  private ArrayList<Course> preReqs;

  public Course(String dept, int courseNum, String grade, int courseHours) throws CourseException{
    this.dept = dept;
    this.courseNum = courseNum;
    this.grade = grade;
    this.courseHours = courseHours;
    this.chronologicalIndex = numCoursesTaken++;
    this.preReqs = new ArrayList<Course>();
    this.courseValue = computeValue();
    this.name = combineName();
  }

  public Course(String dept, int courseNum, String grade, int courseHours, ArrayList<Course> preReqs) throws CourseException{
    this.dept = dept;
    this.courseNum = courseNum;
    this.grade = grade;
    this.courseHours = courseHours;
    this.chronologicalIndex = numCoursesTaken++;
    this.preReqs = preReqs;
    this.courseValue = computeValue();
    this.name = combineName();
  }

  public String combineName(){
    return this.dept + Integer.toString(this.courseNum);
  }

  public double computeValue() throws CourseException{
    String grade = this.grade;
    char letterGrade = grade.charAt(0);
    double gpa = 0;
    if(grade.length() > 1){
      char plusMinus = grade.charAt(1);
      final double THIRD = (double) 1 / (double) 3;
      if(plusMinus == '+'){
        gpa += THIRD;
      }
      else if(plusMinus == '-'){
        gpa -= THIRD;
      }
      else{
        throw new CourseException("PLMS");
      }
    }
    switch(letterGrade){
      case  'A' : gpa += 4;
                  break;
      case  'B' : gpa += 3;
                  break;
      case  'C' : gpa += 2;
                  break;
      case  'D' : gpa += 1;
                  break;
      case  'F' : gpa += 0;
                  break;

    }
    return gpa;
  }

  public String getName(){
    return this.name;
  }

  public int getCourseNum(){
    return this.courseNum;
  }

  public int getCourseHours(){
    return this.courseHours;
  }

  public String getGrade(){
    return this.grade;
  }

  public double getGradeValue(){
    return this.courseValue;
  }

  public ArrayList<Course> getPreReqs(){
    return this.preReqs;
  }

  public String toString(){
    return this.name;
  }

  public int getChronoIndex(){
    return this.chronologicalIndex;
  }

}

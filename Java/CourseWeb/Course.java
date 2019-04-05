
import java.util.ArrayList;

public class Course{

  private String name;
  private String dept;
  private String grade;
  private int courseNum;
  private int courseHours;
  private ArrayList<Course> preReqs;

  public Course(String dept, int courseNum, String grade, int courseHours){
    this.dept = dept;
    this.courseNum = courseNum;
    this.grade = grade;
    this.courseHours = courseHours;
    this.preReqs = new ArrayList<Course>();
    this.name = combineName();
  }

  public Course(String dept, int courseNum, String grade, int courseHours, ArrayList<Course> preReqs){
    this.dept = dept;
    this.courseNum = courseNum;
    this.grade = grade;
    this.courseHours = courseHours;
    this.preReqs = preReqs;
    this.name = combineName();
  }

  public String combineName(){
    return this.dept + Integer.toString(this.courseNum);
  }

  public String getName(){
    return this.name;
  }

  public int getCourseNum(){
    return this.courseNum;
  }

  public String getGrade(){
    return this.grade;
  }

  public ArrayList<Course> getPreReqs(){
    return this.preReqs;
  }

}

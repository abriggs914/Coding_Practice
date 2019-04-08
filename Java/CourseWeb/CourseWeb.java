
// import java.util.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

public class CourseWeb{

  public static ArrayList<Course> courseList = new ArrayList<Course>();

  public static void main(String[] args) throws CourseException{

    /*

        DO NOT SORT courseList  IT IS ALREADY IN CHRONOLOGICAL ORDER

    */

    courseList.add(new Course("BIOL", 1001, "C", 3));
		courseList.add(new Course("CHEM", 1001, "B", 3));
		courseList.add(new Course("CHEM", 1006, "A-", 2));
		courseList.add(new Course("MATH", 1003, "C", 3));
		courseList.add(new Course("PHYS", 1061, "C", 3));
		courseList.add(new Course("PHYS", 1091, "C", 2));
		courseList.add(new Course("BIOL", 1012, "C", 3, new ArrayList<Course>(Arrays.asList(courseList.get(0)))));//new Course("BIOL", 1001, "C", 3)))));
		courseList.add(new Course("CHEM", 1012, "B", 3, new ArrayList<Course>(Arrays.asList(courseList.get(1)))));//new Course("CHEM", 1001, "B", 3)))));
		courseList.add(new Course("CHEM", 1017, "A+", 2, new ArrayList<Course>(Arrays.asList(courseList.get(2)))));//new Course("CHEM", 1006, "A-", 2)))));
		courseList.add(new Course("PHYS", 1092, "B-", 2, new ArrayList<Course>(Arrays.asList(courseList.get(5)))));//new Course("PHYS", 1091, "C", 2)))));
		courseList.add(new Course("MATH", 1013, "B-", 3, new ArrayList<Course>(Arrays.asList(courseList.get(3)))));//new Course("MATH", 1003, "C", 3)))));
		courseList.add(new Course("CHEM", 2416, "C+", 2, new ArrayList<Course>(Arrays.asList(courseList.get(8)))));
		courseList.add(new Course("CHEM", 2421, "C+", 3, new ArrayList<Course>(Arrays.asList(courseList.get(7)))));
		courseList.add(new Course("CHEM", 2601, "C", 3, new ArrayList<Course>(Arrays.asList(courseList.get(7), courseList.get(10)))));
		courseList.add(new Course("ENGL", 1144, "B-", 3));
		courseList.add(new Course("CS", 1073, "B-", 4));
		courseList.add(new Course("CS", 1303, "B+", 4));
		courseList.add(new Course("CS", 1203, "B+", 3));
		courseList.add(new Course("MATH", 1503, "B", 3));
		courseList.add(new Course("INFO", 1103, "B-", 4, new ArrayList<Course>(Arrays.asList(courseList.get(15)))));
		courseList.add(new Course("CS", 2333, "B", 4, new ArrayList<Course>(Arrays.asList(courseList.get(15), courseList.get(16)))));
		courseList.add(new Course("CS", 1083, "B", 4, new ArrayList<Course>(Arrays.asList(courseList.get(15)))));
		// courseList.add(new Course("STAT", 2593, "F", 3, new ArrayList<Course>(Arrays.asList(courseList.get(10)))));
		courseList.add(new Course("STAT", 2593, "B+", 3, new ArrayList<Course>(Arrays.asList(courseList.get(10)))));
		courseList.add(new Course("CS", 2253, "B", 4, new ArrayList<Course>(Arrays.asList(courseList.get(16)))));
		courseList.add(new Course("CS", 2263, "B", 4, new ArrayList<Course>(Arrays.asList(courseList.get(21)))));
		courseList.add(new Course("CS", 3997, "B+", 3));
		courseList.add(new Course("CS", 3853, "B+", 4, new ArrayList<Course>(Arrays.asList(courseList.get(23)))));
		courseList.add(new Course("CS", 2043, "A-", 4, new ArrayList<Course>(Arrays.asList(courseList.get(21)))));
		courseList.add(new Course("CS", 2383, "B+", 4, new ArrayList<Course>(Arrays.asList(courseList.get(16), courseList.get(21)))));
		courseList.add(new Course("CS", 2613, "B", 4, new ArrayList<Course>(Arrays.asList(courseList.get(21)))));
		courseList.add(new Course("CS", 3413, "B+", 4, new ArrayList<Course>(Arrays.asList(courseList.get(24)))));
		courseList.add(new Course("CS", 3113, "D", 3, new ArrayList<Course>(Arrays.asList(courseList.get(15), courseList.get(18)))));
		courseList.add(new Course("CS", 2063, "F", 4, new ArrayList<Course>(Arrays.asList(courseList.get(27)))));
		courseList.add(new Course("CS", 3383, "F", 4, new ArrayList<Course>(Arrays.asList(courseList.get(20), courseList.get(22), courseList.get(28)))));
		courseList.add(new Course("CS", 3613, "F", 4, new ArrayList<Course>(Arrays.asList(courseList.get(20), courseList.get(24), courseList.get(29)))));
		courseList.add(new Course("CS", 3873, "F", 4, new ArrayList<Course>(Arrays.asList(courseList.get(24)))));
		courseList.add(new Course("CS", 3503, "F", 4, new ArrayList<Course>(Arrays.asList(courseList.get(19)))));

    // courseList.forEach((c) -> System.out.println(c.getName()));
    System.out.println("Average grade: " + computeAverageGrade());
    computeGPA();

    // courseList.remove(21);
    printLstCoursesWithPreReqs();
  }

  public static String computeAverageGrade(){
    ArrayList<String> grades = new ArrayList<String>();
    courseList.forEach((c) -> grades.add(c.getGrade()));
    int sum = 0;
    int numGrades = grades.size();
    for(int i = 0; i < numGrades; i++){
      String curr = grades.get(i);
      if(curr.length() == 1){
        char c = curr.charAt(0);
        sum += c;
      }
      else if(curr.length() == 2){
        char c = curr.charAt(0);
        sum += c;
        c = curr.charAt(1);
        switch(c){
          case '-'  : sum++;
                      break;
          case '+'  : sum--;
                      break;
          default   : sum = 0;
                      System.out.println("ERROR invalid grade given.");
                      break;
        }
      }
      else{
        System.out.println("Error invalid grade given.");
        return "";
      }
    }
    // System.out.println("sum: " + sum);
    // System.out.println("numGrades: " + numGrades);
    double d = sum / numGrades;
    // System.out.println("d: " + d);
    double dRes = sum % numGrades;
    // System.out.println("dRes: " + dRes);
    String res = "";
    char dChar = (char) d;
    res += Character.toString(dChar);
    if(dRes != 0){
      double lowOffset = numGrades * ((double) 1 / (double) 3);
      double highOffset = numGrades * ((double) 2 / (double) 3);
      // System.out.println(lowOffset + "      " + highOffset);
      if(dRes <= lowOffset){
        dChar = '-';
      }
      else if(dRes >= (numGrades * (2 / 3))){
        dChar = '+';
      }
      else{
        System.out.println("ERROR");
      }
      res += Character.toString(dChar);
    }
    return res;
  }

  public static void computeGPA(){

    int numCoursesTaken = courseList.size();
    computeGPAValue();
  }

  public static double computeGPAValue(){
    ArrayList<Double> grades = new ArrayList<Double>();
    courseList.forEach((c) -> grades.add(c.getGradeValue() * c.getCourseHours()));
    // for(int i = 0; i < courseList.length; i++){
    //   grades.get(i) *= cou
    // }
    System.out.println(grades);
    double gpaSum = 0;
    int numCreditHoursAttempted = 0;
    for(int i = 0; i < grades.size(); i++){
      gpaSum += grades.get(i);
      numCreditHoursAttempted += courseList.get(i).getCourseHours();
    }
    gpaSum /= (double) numCreditHoursAttempted;
    return gpaSum;
  }

  public static ArrayList<Course> collectCoursePreReqs(Course course){
    ArrayList<Course> preReqs = course.getPreReqs();
    if(preReqs.isEmpty()){
      return new ArrayList<Course>();
    }
    else{
      ArrayList<Course> temp = course.getPreReqs();
      // temp.addAll(preReqs);
      for(int i = 0; i < preReqs.size(); i++){
        temp.addAll(collectCoursePreReqs(preReqs.get(i)));
      }
      return temp;
    }
  }
    // System.out.println();

  /**
  *
  */
  public static void printLstCoursesWithPreReqs(){
    for(int i = 0; i < courseList.size(); i++){
      System.out.println("\n\tCourse: " + courseList.get(i).getName());
      ArrayList<Course> res = collectCoursePreReqs(courseList.get(i));
      ArrayList<Course> preReqs = new ArrayList<Course>();
      // preReqs.clear();
      for(Course c : res){
        // System.out.println(preReqs);
        if(!preReqs.contains(c)){
          preReqs.add(c);
        }
      }
      sortCoursesByCourseNum(preReqs);
      preReqs.forEach((c) -> System.out.println(c));
    }
  }

  public static void printLstCoursesWithPreReqsTimeLine(){
    for(int i = 0; i < courseList.size(); i++){
      System.out.println("\n\tCourse: " + courseList.get(i).getName());
      ArrayList<Course> res = collectCoursePreReqs(courseList.get(i));
      ArrayList<Course> preReqs = new ArrayList<Course>();
      // preReqs.clear();
      for(Course c : res){
        // System.out.println(preReqs);
        if(!preReqs.contains(c)){
          preReqs.add(c);
        }
      }
      sortCoursesByCourseNum(preReqs);
      mapPreReqsTimeline(courseList.get(i), preReqs);
      preReqs.forEach((c) -> System.out.println(c));
    }
  }

  public static void sortCoursesByCourseNum(ArrayList<Course> arr){
    arr.sort((c1, c2) -> {
      return c1.getCourseNum() - c2.getCourseNum();
    });
  }

  public static void sortCoursesByOrderTaken(ArrayList<Course> arr){
    arr.sort((c1, c2) -> {
      return c1.getChronoIndex() - c2.getChronoIndex();
    });
  }

  public static void mapPreReqsTimeline(Course course, ArrayList<Course> preReqs){

    // preReqs.forEach((c) -> System.out.println(c));
  }
}

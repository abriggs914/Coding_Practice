#Create a Grade class, with minimum_passing as an attribute set to 65.
#Give Grade a constructor. Take in a parameter score and assign it to self.score.
class Grade:
  minimum_passing = 65
  
  def __init__(self, score):
    self.score = score
  
  def is_passing(self):
    if (self.score >= self.minimum_passing):
      return True
    return False
    
#Define a class Student this will be our data model at Jan van Eyck High School and Conservatory.
#In the body of the constructor for Student, declare self.grades as an empty list.
#Add an .add_grade() method to Student that takes a parameter, grade.
#.add_grade() should verify that grade is of type Grade and if so, add it to the Student‘s .grades.
#If grade isn’t an instance of Grade then .add_grade() should do nothing.
class Student:
  
  #Add a constructor for Student. Have the constructor take in two parameters: a name and a year. Save those two as attributes .name and .year.
  def __init__(self, name, year):
    self.name = name
    self.year = year
    self.grades = []
    
  def add_grade(self, grade):
    if (type(grade) == Grade):
      self.grades.append(grade)
      
  def get_average(self):
    sum_scores = 0
    lst = getattr(self, "grades", [])
    if (len(lst) == 0):
      return
    for score in lst:
      sum_scores += score.score
    return sum_scores / len(lst)
  
#Create three instances of the Student class:
#Roger van der Weyden, year 10
#Sandro Botticelli, year 12
#Pieter Bruegel the Elder, year 8
#Save them into the variables roger, sandro, and pieter.
roger = Student("Roger van der Weyden", 10)
sandro = Student("Sandro Botticelli", 12)
pieter = Student("Pieter Bruegel the Elder", 8)

#Create a new Grade with a score of 100 and add it to pieter‘s .grades attribute using .add_grade().
pieter.add_grade(Grade(100)) 

#Great job! You’ve created two classes and defined their interactions. This is object-oriented programming! From here you could:
#Write a Grade method .is_passing() that returns whether a Grade has a passing .score.
print(Grade(100).is_passing())
#Write a Student method get_average() that returns the student’s average score.
print(pieter.get_average())
pieter.add_grade(Grade(80)) 
print(pieter.get_average())
#Add an instance variable to Student that is a dictionary called .attendance, with dates as keys and booleans as values that indicate whether the student attended school that day.
#Write your own classes to do whatever logic you want!
  
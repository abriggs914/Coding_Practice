#In the example below, we created a class and named it Facade. We used the pass keyword in Python to indicate that the body of the class was intentionally left blank so we don’t cause an IndentationError. We’ll learn about all the things we can put in the body of a class in the next few exercises.
class Facade:
  pass

  
#In script.py we see our Facade class from last exercise. Make a Facade instance and save it to the variable facade_1. 
facade_1 = Facade()

#In Python __main__ means “this current file that we’re running” and so one could read the output from type() to mean “the class Facade that was defined here, in the script you’re currently running.”
#In script.py we see facade_1 from last exercise. Try calling type() on facade_1 and saving it to the variable facade_1_type.
#Print out facade_1_type.
facade_1_type = type(facade_1)
print(facade_1_type)

#Methods are functions that are defined as part of a class. The first argument in a method is always the object that is calling the method. Convention recommends that we name this first argument self. Methods always have at least this one argument.
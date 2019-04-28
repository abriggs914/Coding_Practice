class Circle:
  pi = 3.14
    
  # Add constructor here:
  #Since we seem more frequently to know the diameter of a circle, it should take the argument diameter.
  #Now have the constructor print out the message "New circle with diameter: {diameter}" when a new circle is created.
	#Create a circle teaching_table with diameter 36.
  def __init__(self, diameter):
    print("New circle with diameter: {diameter}".format(diameter = diameter))
  
  def __repr__(self):
    return "Circle with radius {radius}".format(radius = self.radius)
  
  def area(self, radius):
    area = Circle.pi * radius ** 2
    return area

  def circumference(self):
    return self.pi * 2 * self.radius

circle = Circle(1)

#You go to measure several circles you happen to find around.
#A medium pizza that is 12 inches across.
#Your teaching table which is 36 inches across.
#The Round Room auditorium, which is 11,460 inches across.
#You save the areas of these three things into pizza_area, teaching_table_area, and round_room_area.
#Remember that the radius of a circle is half the diameter. We gave three diameters here, so halve them before you calculate the given circle’s area.
pizza_area = circle.area((12/2))
teaching_table_area = circle.area((36/2))
round_room_area = circle.area((11460/2))
print(pizza_area)
print(teaching_table_area)
print(round_room_area)
    
teaching_table = Circle(36)
  
    
#In script.py we have a list of different data types, some strings, some lists, and some dictionaries, all saved in the variable how_many_s.
#For every element in the list, check if the element has the attribute count. If so, count the number of times the string "s" appears in the element. Print this number.
how_many_s = [{'s': False}, "sassafrass", 18, ["a", "c", "s", "d", "s"]]
for item in how_many_s:
  if(hasattr(item, "count")):
    print(item.count("s"))
    
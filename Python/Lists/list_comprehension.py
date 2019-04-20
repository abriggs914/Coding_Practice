heights = [161, 164, 156, 144, 158, 170, 163, 163, 157]

# We have defined a list heights of visitors to a theme park.
# In order to ride the Topsy Turvy Tumbletron roller coaster,
# you need to be above 161 centimeters. Using a list comprehension,
# create a new list called can_ride_coaster that has every element
# from heights that is greater than 161.

can_ride_coaster = [height for height in heights if height > 161]

#-----------------------------------------------------------------------------------------------------------------------------

celsius = [0, 10, 15, 32, -5, 27, 3]
# We have provided a list of temperatures in celsius. Using a list
# comprehension, create a new list called fahrenheit that converts
# each element in the celsius list to fahrenheit.
#*Note: * To convert, use the formula:
fahrenheit = [c * 9/5 + 32 for c in celsius]
print(fahrenheit)

#-----------------------------------------------------------------------------------------------------------------------------

#Create a list called single_digits that consists of the numbers 0-9 (inclusive).
single_digits = list(range(10))

#Create a for loop that goes through single_digits and prints out each one.

# Create a list called squares. Assign it to be an empty list to begin with.

# Inside the loop that iterates through single_digits, append the squared value
# of each element of single_digits to the list squares. You can do this before
# or after printing the element.

squares = []

for i in single_digits:
  print(i)
  squares.append(i**2)
  
#After the for loop, print out squares.
print(squares)

# Create the list cubes using a list comprehension on the single_digits list.
# Each element of cubes should be an element of single_digits taken to the third power.
cubes = [i**3 for i in single_digits]

#Print cubes.
print(cubes)

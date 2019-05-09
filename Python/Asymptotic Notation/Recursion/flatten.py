#RECURSION: PYTHON
#No Nested Lists Anymore, I Want Them to Turn Flat
#Let’s use recursion to solve another problem involving lists: flatten().
#We want to write a function that removes nested lists within a list but keeps the values contained.
#nested_planets = ['mercury', 'venus', ['earth'], 'mars', [['jupiter', 'saturn']], 'uranus', ['neptune', 'pluto']]
#flatten(nested_planets)
# ['mercury', 
#  'venus', 
#  'earth', 
#  'mars', 
#  'jupiter', 
#  'saturn', 
#  'uranus', 
#  'neptune', 
#  'pluto']
#Remember our tools for recursive functions. We want to identify a base case, and we need to think about a recursive step that takes us closer to achieving the base case.
#For this problem, we have two scenarios as we move through the list.
#The element in the list is a list itself.
#We have more work to do!
#The element in the list is not a list.
#All set!
#Which is the base case and which is the recursive step?
#Instructions
#1.
#Define flatten() which has a single parameter named my_list.
#We’ll start by declaring a variable, result and setting it to an empty list.
#result is our intermediary variable that houses elements from my_list.
#Return result.
#2.
#Returning an empty list isn’t much good to us, it should be filled with the values contained in my_list.
#Use a for loop to iterate through my_list.
#Inside the loop, we need a conditional for our recursive step. Check if the element in the current iteration is a list.
#We can use Python’s isinstance() like so:
#a_list = ['listing it up!']
#not_a_list = 'string here'
#isinstance(a_list, list)
# True
#isinstance(not_a_list, list)
# False
#For now, print "List found!" in the conditional.
#Outside of the method definition, call flatten() and pass planets as an argument.
#Use isinstance(iteration_element, list).
#Here’s an example:
#my_list = ['apples', ['cherries'], 'bananas']
#for element in my_list:
#  if isinstance(element, list):
#    print("this element is a list!")
#  else:
#    print(element)
# apples
# this element is a list!
# bananas
#3.
#We need to make the recursive step draw us closer to the base case, where every element is not a list.
#After your print statement, declare the variable flat_list, and assign it to a recursive call to flatten() passing in your iterating variable as the argument.
#flatten() will return a list, update result so it now includes every element contained in flat_list.
#Test flatten() by calling it on the planets and printing the result.
#We can combine two lists like so:
#first_list = ['a', 'b', 'c']
#second_list = ['d', 'e', 'f']
#first_list + second_list
# ['a', 'b', 'c', 'd', 'e', 'f']
#We can use this to update the result list like so:
#result = ['a']
#flat_list = ['b', 'c']
#result += flat_list
#result # ['a', 'b', 'c']
#4.
#Nice work! Now the base case.
#If the iterating variable is not a list, we can update result, so it includes this element at the end of the list.
#flatten() should now return the complete result.
#Print the result!
#Why is it important that the element is added at the end?
#Let’s think through how these recursive calls will work in a simple case:
#nested = ['green', 'red', ['blue', 'yellow'], 'purple']
#flatten(nested)
# inside flatten()...
# result = ['green']
# result = ['green', 'red']
# recursive call! flatten(['blue', 'yellow'])
# inside recursive flatten()...
# recursive result = ['blue']
# recursive result = ['blue', 'yellow']
# recursive call resolves
# flat_list = ['blue', 'yellow']
# result += flat_list
# result = ['green', 'red', 'blue', 'yellow', 'purple']
#If elements weren’t added to the end of result, the ordering would be lost!

# define flatten() below...
def flatten(my_list):
  result = []
  for item in my_list:
    if (isinstance(item, list)):
      print("List found!")
      flat_list = flatten(item)
      result += flat_list
    else:
      result.append(item)
  return result


### reserve for testing...
planets = ['mercury', 'venus', ['earth'], 'mars', [['jupiter', 'saturn']], 'uranus', ['neptune', 'pluto']]

print(flatten(planets))

## ==>
#nested_planets = ['mercury', 'venus', ['earth'], 'mars', [['jupiter', 'saturn']], 'uranus', ['neptune', 'pluto']]

#flatten(nested_planets)
# ['mercury', 
#  'venus', 
#  'earth', 
#  'mars', 
#  'jupiter', 
#  'saturn', 
#  'uranus', 
#  'neptune', 
#  'pluto']
border = "".join(["#" for i in range(60)])

# TECHNICAL INTERVIEW PROBLEMS IN PYTHON: LISTS
# List Rotation: Slice
# For our first problem, we would like to “rotate” a list, or move elements forward in a list by a number of spaces, k.

# Elements at the greatest index will “wrap around” to the beginning of the list.

# list = ['a', 'b', 'c', 'd', 'e', 'f']
# rotate(list, 0)
# # ['a', 'b', 'c', 'd', 'e', 'f']
# rotate(list, 1)
# # ['f', 'a', 'b', 'c', 'd', 'e']
# rotate(list, 3)
# # ['d', 'e', 'f', 'a', 'b', 'c']
# Clarifying Questions:

# Are there constraints on time or space efficiency?
# Nope! Just solve the problem.
# Should I account for negative inputs?
# The rotation input will always be positive.
# What if the rotation is greater than the list length?
# Continue wrapping!
# The “rotated” list would be the same as the original when k is equal to the length.
# Instructions
# 1.
# Write a function rotate(), with the parameters my_list and num_rotations.

# rotate() should return the input list rotated num_rotations forward.


# Hint
# One approach would be to .pop() an element and .insert() it at the beginning of the list as many times as needed.

# This might feel the most intuitive since we’re literally moving each element forward one at a time!

# We can also think of how the list will look at the end the number of rotations. All elements up to but not including the rotation point index will be placed at the end of all elements from the index to the end of the list.

# The slice operator, [], and a negative rotation input as the index will split the original list into two sub-lists which can be added together.

# num_rotations = 3
# letters = ['a', 'b', 'c', 'd', 'e']

# # to create ['c', 'd', 'e', 'a', 'b']
# # we can use the slice operator...

# letters[:-num_rotations]
# # ['a', 'b']
# letters[-num_rotations:]
# # ['c', 'd' ,'e']


# rotate list
# no time/space requirements
# return "rotated" version of input list

def rotate(my_list, num_rotations):
  r = num_rotations % len(my_list)
  x =  my_list[-r:] + my_list[:-r]
  # print("lst:\t" + str(my_list))
  # print("x:\t" + str(x))
  return x


#### TESTS SHOULD ALL BE TRUE ####
print(border)
print("{0}\n should equal \n{1}\n {2}\n".format(rotate(['a', 'b', 'c', 'd', 'e', 'f'], 1), ['f', 'a', 'b', 'c', 'd', 'e'], rotate(['a', 'b', 'c', 'd', 'e', 'f'], 1) == ['f', 'a', 'b', 'c', 'd', 'e']))

print("{0}\n should equal \n{1}\n {2}\n".format(rotate(['a', 'b', 'c', 'd', 'e', 'f'], 2), ['e', 'f', 'a', 'b', 'c', 'd'], rotate(['a', 'b', 'c', 'd', 'e', 'f'], 2) == ['e', 'f', 'a', 'b', 'c', 'd']))

print("{0}\n should equal \n{1}\n {2}\n".format(rotate(['a', 'b', 'c', 'd', 'e', 'f'], 3), ['d', 'e', 'f', 'a', 'b', 'c'], rotate(['a', 'b', 'c', 'd', 'e', 'f'], 3) == ['d', 'e', 'f', 'a', 'b', 'c']))

print("{0}\n should equal \n{1}\n {2}\n".format(rotate(['a', 'b', 'c', 'd', 'e', 'f'], 4), ['c', 'd', 'e', 'f', 'a', 'b'], rotate(['a', 'b', 'c', 'd', 'e', 'f'], 4) == ['c', 'd', 'e', 'f', 'a', 'b']))
print(border)
#######################################################################################################################
# TECHNICAL INTERVIEW PROBLEMS IN PYTHON: LISTS
# List Rotation: Indices
# Optimizing a solution means reducing the memory required (space complexity), or reducing the number of instructions the computer must execute (time complexity).

# Sometimes this means entirely rethinking the approach to a question and it’s always meant to be a difficult task.

# In the last exercise we created a new list using the slice operator. This requires O(N) space, because a new list is made with copies of each value, and O(N) time because every value is visited while copying. N represents the number of values in the list.

# We need to do better than O(N).

# For time complexity, there’s not much we can do. Rotations could encompass the list, requiring us to iterate approximately N times.

# For space complexity, we can optimize by constructing in-place solutions, meaning we don’t create any additional data structures for storing values.

# Single variable declarations are considered O(1), or constant space, because we’re not allocating memory in relation to the input.

# This example function adds "!" to each string in a list.

# def constant_space(list_of_strings):
#   # variable the same regardless of input
#   exclamation = "!"
#   for element in list_of_strings:
#     element += exclamation

#   # input mutated but no more space used
#   return list_of_strings

# def linear_space(list_of_strings):
#   exclamation_list = [] # new structure
#   exclamation = "!"

#   for element in list_of_strings:
#     # adding a new value each loop
#     exclamation_list.append(element + exclamation)

#   # holds as many new values as the input!
#   return exclamation_list   
# Given a list and a positive integer, return the same list “rotated” a number of times that match the input integer. This time, we’ll rotate the list backward and use O(1) space.

# list = ['a', 'b', 'c', 'd', 'e', 'f']
# rotate(list, 1)
# # ['b', 'c', 'd', 'e', 'f', 'a']
# rotate(list, 4)
# # ['e', 'f', 'a', 'b', 'c', 'd']
# Instructions
# 1.
# It’s always harder to optimize, so don’t get discouraged!

# Write a function rotate(), with the parameters my_list and num_rotations.

# rotate() should return the same input list rotated num_rotations backward.


# Hint
# Like the last exercise, we can look at the num_rotations input as the key to unlocking this problem.

# Instead of making copies, we’ll reverse sections of the list:

# # <> marks selected elements

# # 2 rotations
# ['a', 'b', 'c', 'd', 'e', 'f'] 

# # reverse first 2
# [<'b', 'a',> 'c', 'd' ,'e', 'f'] 

# # reverse all but first 2
# ['b', 'a', <'f', 'e', 'd', 'c'>] 

# # reverse all
# [<'c', 'd', 'e', 'f', 'a', 'b'>] 

# # all done!
# ['c', 'd', 'e', 'f', 'a', 'b']
# It’s the same approach as before, but we’re reversing elements in place of copying and combining sub-lists.

# Use this helper method to reverse a section of a list:

# def rev(lst, low, high):
#   while low < high:
#     lst[low], lst[high] = lst[high], lst[low]
#     high -= 1
#     low += 1
#   return lst

# rotate list
# Constant space requirement
# return input list "rotated"

#from itertools import islice

def rotate(my_list, num_rotations):
  l = len(my_list)
  r = num_rotations % l
  my_list.extend(my_list[r:])
  my_list.extend(my_list[:r])
  my_list.reverse()
  for i in range(l):
    my_list.pop()
  my_list.reverse()
  return my_list


  #my_list = islice(my_list, num_rotations%len(my_list)) + islice(my_list, num_rotations%len(my_list))
  # r = num_rotations%len(my_list)
  # my_list = my_list[r:]
  # c = 0
  # for i in range(len(my_list)-r):
  #   my_list.append(my_list[c])
  #   c+=1
  # return my_list
  #return my_list[num_rotations%len(my_list):] + my_list[:num_rotations%len(my_list)]  # apparantly this is linear...
  #islicing doesnt work either...




#### TESTS SHOULD ALL BE TRUE ####
print(border)
print("{0}\n should equal \n{1}\n {2}\n".format(rotate(['a', 'b', 'c', 'd', 'e', 'f'], 1), ['b', 'c', 'd', 'e', 'f', 'a'], rotate(['a', 'b', 'c', 'd', 'e', 'f'], 1) == ['b', 'c', 'd', 'e', 'f', 'a']))

print("{0}\n should equal \n{1}\n {2}\n".format(rotate(['a', 'b', 'c', 'd', 'e', 'f'], 2), ['c', 'd', 'e', 'f', 'a', 'b'], rotate(['a', 'b', 'c', 'd', 'e', 'f'], 2) == ['c', 'd', 'e', 'f', 'a', 'b']))

print("{0}\n should equal \n{1}\n {2}\n".format(rotate(['a', 'b', 'c', 'd', 'e', 'f'], 3), ['d', 'e', 'f', 'a', 'b', 'c'], rotate(['a', 'b', 'c', 'd', 'e', 'f'], 3) == ['d', 'e', 'f', 'a', 'b', 'c']))

print("{0}\n should equal \n{1}\n {2}\n".format(rotate(['a', 'b', 'c', 'd', 'e', 'f'], 4), ['e', 'f', 'a', 'b', 'c', 'd'], rotate(['a', 'b', 'c', 'd', 'e', 'f'], 4) == ['e', 'f', 'a', 'b', 'c', 'd']))
print(border)
#######################################################################################################################
# TECHNICAL INTERVIEW PROBLEMS IN PYTHON: LISTS
# Rotation Point: Linear Search
# We’ll continue our theme of list rotation by flipping the problem: given a sorted list rotated k times, return the index where the “unrotated” list would begin.

# rotated_list = ['c', 'd', 'e', 'f', 'a']
# rotation_point(rotated_list)
# # index 4
# # a sorted list would start with 'a'

# another_rotated_list = [13, 8, 9, 10, 11] 
# rotation_point(rotated_list)
# # index 1
# # a sorted list would start with 8
# Clarifying Questions:

# Are there constraints on time or space efficiency?
# No! Any solution will do.
# Does the rotation direction matter?
# This won’t affect the return value.
# What if the input isn’t rotated?
# Return 0.
# Instructions
# 1.
# Write a function count_rotations() which has one parameter rotated_list.

# count_rotations() should return the index where the sorted list would begin.


# Hint
# Essentially, we’re looking for the index of the minimum element in the list.

# Iterate through each element and check to see if it’s the lowest value.

# The minimum can default to the first element, we won’t test this function on empty lists.

# Return the minimum index when you’re finished iterating.

# This is a linear time complexity and constant space complexity solution.

# find rotation point 
# No time/space requirements
# return index of "rotation point" element

def rotation_point(rotated_list):
  # sorted_list = rotated_list.sort()
  for i in range(len(rotated_list) - 1):
    if rotated_list[i] > rotated_list[i + 1]:
      return i + 1
  return 0



#### TESTS SHOULD ALL BE TRUE ####
print(border)
print("{0}\n should equal \n{1}\n {2}\n".format(rotation_point(['a', 'b', 'c', 'd', 'e', 'f']), 0, rotation_point(['a', 'b', 'c', 'd', 'e', 'f']) == 0))

print("{0}\n should equal \n{1}\n {2}\n".format(rotation_point(['c', 'd', 'e', 'f', 'a']), 4, rotation_point(['c', 'd', 'e', 'f', 'a']) == 4))

print("{0}\n should equal \n{1}\n {2}\n".format(rotation_point([13, 8, 9, 10, 11]), 1, rotation_point([13, 8, 9, 10, 11]) == 1))
print(border)
#######################################################################################################################
# find rotation point 
# O(logN) time requirement
# return index of "rotation point" element
one_answer = """
def rotation_point(rotated_list):
  def mid(lower, upper):
    return int((upper - lower) / 2) + lower
  # def in_order(a, b, c):
  #   return a <= b <= c
  lower = 0
  upper = len(rotated_list) - 1
  m = mid(lower, upper)
  curr_min = None
  print("BEFORE, lower",lower, ", upper", upper, ", m", m, ", curr_min", curr_min, ", RL[lower]", rotated_list[lower], ", RL[upper]", rotated_list[upper], ", rotated_list", rotated_list)
  while lower < upper and m not in [lower, upper]:
    print("A, lower",lower, ", upper", upper, ", m", m, ", curr_min", curr_min, ", rotated_list", rotated_list)
    if not curr_min or rotated_list[m] < curr_min:
      curr_min = min(rotated_list[lower], rotated_list[m], rotated_list[upper])
    if rotated_list[m - 1] < curr_min:
      upper = m
    else:#elif rotated_list[m + 1] < curr_min:
      lower = m
    #else:
    #  if rotated_list[lower] < rotated_list[upper]:
    #    upper = m
    #  else:
    #    lower = m
      #m = lower  else upper  
    m = mid(lower, upper)
    print("B, lower",lower, ", upper", upper, ", m", m, ", curr_min", curr_min, ", rotated_list", rotated_list)
  return m #(m + 1) % len(rotated_list)
"""


def rotation_point(rotated_list):
  def mid(lower, upper):
    return int((upper - lower) / 2) + lower
  # def in_order(a, b, c):
  #   return a <= b <= c
  lower = 0
  upper = len(rotated_list) - 1
  m = mid(lower, upper)
  curr_max = None
  count = 10
  print("BEFORE, lower",lower, ", upper", upper, ", m", m, ", curr_max", curr_max, ", RL[lower]", rotated_list[lower], ", RL[upper]", rotated_list[upper], ", rotated_list", rotated_list)
  while lower < upper:
    if not curr_max:
      curr_max = rotated_list[m]
    if rotated_list[lower] > curr_max:
      upper = m
      curr_max = rotated_list[m]
      print("adjusting upper")
    elif rotated_list[upper] > curr_max:
      lower = m
      curr_max = rotated_list[m]
      print("adjusting upper")
    else:
      m += 1
    if (upper - lower) < 1:
      m = lower if rotated_list[lower] > rotated_list[upper] else upper
    if count == 0:
      print("\t\tBREAK, Too large")
      break
    m = mid(lower, upper)
    count -= 1
    print("B, l",lower, ", u", upper, ",@{l:u}:", (rotated_list[lower], rotated_list[upper]),", m", m, ", curr_max", curr_max)	
  return (m + 1) % len(rotated_list)
	  
	
  #return rotated_list.index(min(rotated_list))  # linear time and space






#### TESTS SHOULD ALL BE TRUE ####
'''
print(border)
print("{0}\n should equal \n{1}\n {2}\n".format(rotation_point(['a', 'b', 'c', 'd', 'e', 'f']), 0, rotation_point(['a', 'b', 'c', 'd', 'e', 'f']) == 0))

print("{0}\n should equal \n{1}\n {2}\n".format(rotation_point(['c', 'd', 'e', 'f', 'a']), 4, rotation_point(['c', 'd', 'e', 'f', 'a']) == 4))

print("{0}\n should equal \n{1}\n {2}\n".format(rotation_point(['c', 'd', 'e', 'f', 'a', 'b']), 4, rotation_point(['c', 'd', 'e', 'f', 'a', 'b']) == 4))

print("{0}\n should equal \n{1}\n {2}\n".format(rotation_point([13, 8, 9, 10, 11]), 1, rotation_point([13, 8, 9, 10, 11]) == 1))
print(border)
'''

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
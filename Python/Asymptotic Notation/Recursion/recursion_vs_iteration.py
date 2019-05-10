#Implement your version of factorial() which has the same functionality without using any recursive calls!
def factorial(n):
  res = 1
  while(n > 1):
    res *= n
    n-=1
  return res

# test cases
print(factorial(3) == 6)
print(factorial(0) == 1)
print(factorial(5) == 120)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#Implement your version of fibonacci() which has the same functionality without using any recursive calls!
def fibonacci(n):
  if (n <= 0):
    return 0
  a = 0
  b = 1
  while (n > 1):
    c = b
    b += a
    a = c
    n -= 1
  return b

# test cases
print(fibonacci(3) == 2)
print(fibonacci(7) == 13)
print(fibonacci(0) == 0)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#Implement your version of sum_digits() which has the same functionality using recursive calls!
def sum_digits(n):
  if n < 10:
    return n
  i = n % 10
  return i + sum_digits(n//10)

# test cases
print(sum_digits(12) == 3)
print(sum_digits(552) == 12)
print(sum_digits(123456789) == 45)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#Implement your version of find_min() which has the same functionality using recursive calls!
#HINT:
# function definition with two inputs: 
# a list and a min that defaults to None
  # BASE CASE
  # if input is an empty list
    # return min
  # else
    # RECURSIVE STEP
    # if min is None
    # OR
    # first element of list is < min
      # set min to be first element
  # return recursive call with list[1:] and the min
def find_min(lst):
  if (len(lst) == 0):
    return None
  def helper(lst, min_val):
    if (len(lst) == 0):
      return min_val
    if (lst[0] < min_val):
      return helper(lst[1:], lst[0])
    return helper(lst[1:], min_val)
  return helper(lst, lst[0])

# test cases
print(find_min([42, 17, 2, -1, 67]) == -1)
print(find_min([]) == None)
print(find_min([13, 72, 19, 5, 86]) == 5)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#Implement your version of is_palindrome() which has the same functionality using recursive calls!
#def is_palindrome_iter(my_string):
#  while len(my_string) > 1:
#    if my_string[0] != my_string[-1]:
#      return False
#    my_string = my_string[1:-1]
#  return True 
#
#palindrome_iter("abba")
# True
#palindrome_iter("abcba")
# True
#palindrome_iter("")
# True
#palindrome_iter("abcd")
# False
def is_palindrome(my_string):
  if (len(my_string) < 2):
    return True
  if (my_string[0] != my_string[-1]):
    return False
  return is_palindrome(my_string[1:-1])


# test cases
print(is_palindrome("abba") == True)
print(is_palindrome("abcba") == True)
print(is_palindrome("") == True)
print(is_palindrome("abcd") == False)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#def multiplication_iter(num_1, num_2):
#  result = 0
#  for count in range(0, num_2):
#    result += num_1
#  return result
#multiplication_iter(3, 7)
# 21
#multiplication_iter(5, 5)
# 25
#multiplication_iter(0, 4)
# 0
def multiplication(num_1, num_2):
  if (num_1 == 0 or num_2 == 0):
    return 0  
  return num_1 + multiplication(num_1, num_2 - 1)

# test cases
print(multiplication(3, 7) == 21)
print(multiplication(5, 5) == 25)
print(multiplication(0, 4) == 0)
print("res 3x7 =",multiplication(3, 7) )
print("res 5x5 =",multiplication(5, 5) )
print("res 0x4 =",multiplication(0, 4) )

#---------------------------------------------------------------------------------------------------------------------------------------------------------


#Implement your version of depth() which has the same functionality using recursive calls!
#RECURSION VS. ITERATION - CODING THROWDOWN
#How Deep Is Your Tree?
#Binary trees, trees which have at most two children per node, are a useful data structure for organizing hierarchical data.
#It’s helpful to know the depth of a tree, or how many levels make up the tree.
# first level
#root_of_tree = {"data": 42}
# adding a child - second level
#root_of_tree["left_child"] = {"data": 34}
#root_of_tree["right_child"] = {"data": 56}
# adding a child to a child - third level
#first_child = root_of_tree["left_child"]
#first_child["left_child"] = {"data": 27}
#Here’s an iterative algorithm for counting the depth of a given tree.
#We’re using Python dictionaries to represent each tree node, with the key of "left_child" or "right_child" referencing another tree node, or None if no child exists.

# def depth_iter(tree):
#   result = 0
#   # our "queue" will store nodes at each level
#   queue = [tree]
#   # loop as long as there are nodes to explore
#   while queue:
#     # count the number of child nodes
#     # level_count = len(queue)
#     for child_count in range(0, level_count):
#       # loop through each child
#       child = queue.pop(0)
#      # add its children if they exist
#       if child["left_child"]:
#         queue.append(child["left_child"])
#       if child["right_child"]:
#         queue.append(child["right_child"])
#     # count the level
#     result += 1
#   return result

# two_level_tree_a = {
# "data": 6, 
# "left_child":
#   {"data": 2}
# }

# four_level_tree_a = {
# "data": 54,
# "right_child":
#   {"data": 93,
#    "left_child":
#      {"data": 63,
#       "left_child":
#         {"data": 59}
#       }
#    }
# }


# depth_iter(two_level_tree_a)
# # 2
# depth_iter(four_level_tree_a)
# 4
#This algorithm will visit each node in the tree once, which makes it a linear runtime, O(N), where N is the number of nodes in the tree.

#HINT
#Here’s our strategy:
# function takes "tree_node" as input
  # BASE CASE
  # if tree_node is None
    # return 0
  # RECURSIVE STEP
  # set left_depth to recursive call passing tree_node's left child
  # set right_depth to recursive call passing tree_node's right child

  # if left_depth is greater than right depth:
    # return left_depth + 1
  # else
    # return right_depth + 1

def num_nodes(tree):
  if (tree is None):
    return 0
  if (tree["data"] is None):
    return 0
  return 1 + num_nodes(tree["left_child"]) + num_nodes(tree["right_child"])

def depth(tree):
  if (tree is None):
    return 0
  if (tree["data"] == None):
    return 0
  return 1 + max(depth(tree["left_child"]), depth(tree["right_child"]))


# HELPER FUNCTION TO BUILD TREES
def build_bst(my_list):
  if len(my_list) == 0:
    return None

  mid_idx = len(my_list) // 2
  mid_val = my_list[mid_idx]

  tree_node = {"data": mid_val}
  tree_node["left_child"] = build_bst(my_list[ : mid_idx])
  tree_node["right_child"] = build_bst(my_list[mid_idx + 1 : ])

  return tree_node

# HELPER VARIABLES
tree_level_1 = build_bst([1])
tree_level_2 = build_bst([1, 2, 3])
tree_level_4 = build_bst([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]) 

# print(tree_level_1)
# print(tree_level_2)
# print(tree_level_4)

# test cases
print(depth(tree_level_1) == 1)
print(depth(tree_level_2) == 2)
print(depth(tree_level_4) == 4)
print(depth(tree_level_1))
print(depth(tree_level_2))
print(depth(tree_level_4))



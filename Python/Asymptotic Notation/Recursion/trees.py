#RECURSION: PYTHON
#Recursive Data Structures
#Data structures can also be recursive.
#Trees are a recursive data structure because their definition is self-referential. A tree is a data structure which contains a piece of data and references to other trees!
#Trees which are referenced by other trees are known as children. Trees which hold references to other trees are known as the parents.
#A tree can be both parent and child. We’re going to write a recursive function that builds a special type of tree: a binary search tree.
#Binary search trees:
#Reference two children at most per tree node.
#The “left” child of the tree must contain a value lesser than its parent
#The “right” child of the tree must contain a value greater than its parent.
#Trees are an abstract data type, meaning we can implement our version in a number of ways as long as we follow the rules above.
#For the purposes of this exercise, we’ll use the humble Python dictionary:
#bst_tree_node = {"data": 42}
#bst_tree_node["left_child"] = {"data": 36}
#bst_tree_node["right_child"] = {"data": 73}
#bst_tree_node["data"] > bst_tree_node["left_child"]["data"]
# True
#bst_tree_node["data"] < bst_tree_node["right_child"["data"]
# True
#We can also assume our function will receive a sorted list of values as input.
#This is necessary to construct the binary search tree because we’ll be relying on the ordering of the list input.
#Our high-level strategy before moving through the checkpoints.
#base case: the input list is empty
#Return "No Child" to represent the lack of node
#recursive step: the input list must be divided into two halves
#Find the middle index of the list
#Store the value located at the middle index
#Make a tree node with a "data" key set to the value
#Assign tree node’s "left child" to a recursive call using the left half of the list
#Assign tree node’s "right child" to a recursive call using the right half of the list
#Return the tree node
#Instructions
#1.
#Define the build_bst() function with my_list as the sole parameter.
#If my_list has no elements, return “No Child” to represent the lack of a child tree node.
#This is the base case of our function.
#The recursive step will need to remove an element from the input to eventually reach an empty list.
#2.
#We’ll be building this tree by dividing the list in half and feeding those halves to the left and right sides of the tree.
#This dividing step will eventually produce empty lists to satisfy the base case of the function.
#Outside of the conditional you just wrote, declare middle_idx and set it to the middle index of my_list.
#Then, declare middle_value and set it to the value in my_list located at middle_idx.
#Print “Middle index: “ + middle_idx.
#Then, print “Middle value: “ + middle_value
#You can use .format() or addition for the print the statement. Addition will require you to use str() on the variables since they are integers!
#You can reach the mid-point of a list like so:
#colors = ['brown', 'red', 'olive']
#mid_idx = len(colors) // 2
# 1
#mid_color_value = colors[mid_idx]
# 'red'
#and format a string like so:
#color = "blue"
#print("My favorite color is: {0}".format(color))
# "My favorite color is: blue"
#3.
#After the print statements, declare the variable tree_node that points to a Python dictionary with a key of "data" pointing to middle_value.
#tree_node represents the tree being created in this function call. We want a tree_node created for each element in the list, so we’ll repeat this process on the left and right sub-trees using the appropriate half of the input list.
#Now for the recursive calls!
#Set the key of "left_child" in tree_node to be a recursive call to build_bst() with the left half of the list not including the middle value as an argument.
#Set the key of "right_child" in tree_node to be a recursive call to build_bst() with the ** right half of the list not including the middle value** as an argument.
#It’s very important we don’t include the middle_value in the lists we’re passing as arguments, or else we’ll create duplicate nodes!
#Finally, return tree_node. As the recursive calls resolve and pop off the call stack, the final return value will be the root or “top” tree_node which contains a reference to every other tree_node.
#Our recursive calls will look like the following:
#tree_node["left_child"] = build_bst(left_half_of_list)
#tree_node["right_child"] = build_bst(right_half_of_list)
#We can copy half of a list like so:
#pets = ["dogs", "cats", "lizards", "parrots", "giraffes"]
#middle_idx = len(pets) // 2
# 2
#first_half_pets = pets[:middle_idx + 1]
# ["dogs", "cats", "lizards"]
#last_half_pets = pets[middle_idx + 1:]
# ["parrots", "giraffes"]
#4.
#Congratulations! You’ve built up a recursive data structure with a recursive function!
#This data structure can be used to find values in an efficient O(logN) time.
#Fill in the variable runtime with the runtime of your build_bst() function.
#This runtime is a tricky one so don’t be afraid to use that hint!
#N is the length of our input list.
#Our tree will be logN levels deep, meaning there will logN times where a new parent-child relationship is created.
#If we have an 8 element list, the tree is 3 levels deep: 2**3 == 8.
#Each recursive call is going to copy approximately N elements when the left and right halves of the list are passed to the recursive calls. We’re reducing by 1 each time (the middle_value), but that’s a constant factor.
#Putting that together, we have N elements being copied logN levels for a big O of N*logN.

# Define build_bst() below...
def build_bst(my_list):
  if (len(my_list) == 0):
    print("No Child")
    return "No Child"
  #else:
  middle_idx = len(my_list) // 2
  middle_value = my_list[middle_idx]
  print("Middle index: {0}".format(middle_idx))
  print("Middle value: {0}".format(middle_value))
  tree_node = {"data":middle_value}
  left = my_list[:middle_idx]
  
  
  right = my_list[middle_idx+1:]
  print("left_tree",left)
  print("right_tree",right)
  tree_node["left_child"] = build_bst(left)
  tree_node["right_child"] = build_bst(right)
  return tree_node

# For testing
sorted_list = [12, 13, 14, 15, 16]
binary_search_tree = build_bst(sorted_list)
print(binary_search_tree)

# fill in the runtime as a string
# 1, logN, N, N*logN, N^2, 2^N, N!
runtime = "???"

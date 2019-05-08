from linkedlist import LinkedList

#ASYMPTOTIC NOTATION: PYTHON
#Finding the Maximum Value in a Linked List
#Now that we can analyze the runtime of a function, lets see take a look at the runtime of data structures.
#We often search through data structures to find a specific value. In this exercise, you will write a function to find the maximum value of a linked list and you will also analyze the runtime of your function.
#The function, find_max, takes in linked_list as an input. The function should return the maximum value in the linked list.

#Fill in the find_max function such that you return the maximum value in linked_list by only traversing the linked_list once.
#Use the methods in linkedlist.py and node.py to traverse and get values from the list.
#Test cases have been provided for you in order to test your code.

#Fill in Function
def find_max(linked_list):
  print("--------------------------")
  print("Finding the maximum value of:\n{0}".format(linked_list.stringify_list()))
  #Write Code Here
  item = linked_list.head_node
  max = item.value
  while(item.get_next_node() != None):
    item = item.get_next_node()
    if (item.value > max):
      max = item.value
  return max
  
  

#Test Cases
ll = LinkedList(6)
ll.insert_beginning(32)
ll.insert_beginning(-12)
ll.insert_beginning(48)
ll.insert_beginning(2)
ll.insert_beginning(1)
print("The maximum value in this linked list is {0}\n".format(find_max(ll)))

ll_2 = LinkedList(60)
ll_2.insert_beginning(12)
ll_2.insert_beginning(22)
ll_2.insert_beginning(-10)
print("The maximum value in this linked list is {0}\n".format(find_max(ll_2)))

ll_3 = LinkedList("A")
ll_3.insert_beginning("X")
ll_3.insert_beginning("V")
ll_3.insert_beginning("L")
ll_3.insert_beginning("D")
ll_3.insert_beginning("Q")
print("The maximum value in this linked list is {0}\n".format(find_max(ll_3)))

#Runtime
runtime = "N"
print("The runtime of find_max is O({0})".format(runtime))
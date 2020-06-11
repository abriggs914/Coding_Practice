# We'll be using our Node class
class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node
    
  def get_value(self):
    return self.value
  
  def get_next_node(self):
    return self.next_node
  
  def set_next_node(self, next_node):
    self.next_node = next_node

# Our LinkedList class
class LinkedList:
  def __init__(self, value=None):
    self.head_node = Node(value)
  
  def get_head_node(self):
    return self.head_node
# Add your insert_beginning and stringify_list methods below.  
  def insert_beginning(self, new_value):
    new_node = Node(new_value)
    new_node.set_next_node(self.head_node)
    self.head_node = new_node
    
  def stringify_list(self):
    res = ""
    node = self.get_head_node()
    while (node != None):
      res += str(node.get_value()) + "\n"
      node = node.get_next_node()
    return res

# Test your code by uncommenting the statements below - did your list print to the terminal?
ll = LinkedList(5)
ll.insert_beginning(70)
ll.insert_beginning(5675)
ll.insert_beginning(90)
print(ll.stringify_list())

################################################
# We'll be using our Node class
#class Node:
#  def __init__(self, value, next_node=None):
#    self.value = value
#    self.next_node = next_node
#    
#  def get_value(self):
#    return self.value
#  
#  def get_next_node(self):
#    return self.next_node
#  
#  def set_next_node(self, next_node):
#    self.next_node = next_node
#
#
#Within script.py in the pane to the right, create an empty LinkedList class.
#Define an .__init__() method for the LinkedList. We want to be able to instantiate a LinkedList with a head node, so .__init__() should take value as an argument. Make sure value defaults to None if no value is provided.
#Inside the .__init__() method, set self.head_node equal to a new Node with value as its value.    

#Define a .get_head_node() method that helps us peek at the first node in the list.
#Inside the method, return the head node of the linked list.

#Define an .insert_beginning() method which takes new_value as an argument.
#Inside the method, instantiate a Node with new_value. Name this new_node.
#Now, link new_node to the existing head_node.
#Finally, replace the current head_node with new_node.
#Note: Because the workspace is set up with spaces instead of tabs, you will need to use spaces to prevent Python from throwing an error. You can learn more about this here.
# Create your LinkedList class below:
#class LinkedList:
#  def insert_beginning(self, new_value):
#    new_node = Node(new_value)
#    new_node.set_next_link(self.head_node)
#    self.head_node = new_node
#  def __init__(self, value=None):
#    self.head_node = Node(value)
#  def get_head_node(self):  
#    return self.head_node
#Define a new method has_space() in Stack. The method should return True if self.limit is greater than self.size.

#Go back to your push() method — we need to make sure we’re keeping track of our stack size when we add new items. At the end of your method body, increment self.size by 1.

#Now add an if clause at the top of push() that checks if your stack has space (using your newly created helper method).
#If there’s space, the rest of the body of the method should execute
#If there’s no space, we want to print a message letting users know that the stack is already full. Something like “All out of space!” should be good.

#Finally, let’s define a new method is_empty() in Stack.
#The method should return True if the stack’s size is 0.
#Anywhere we’ve written if self.size > 0: can now be replaced with if not self.is_empty().

from node import Node

class Stack:
  def __init__(self, limit=1000):
    self.top_item = None
    self.size = 0
    self.limit = limit
  
  def push(self, value):
    if (self.has_space()):
      item = Node(value)
      item.set_next_node(self.top_item)
      self.top_item = item
      # Increment stack size by 1 here:
      self.size += 1
    else:
      print("No room!")

  def pop(self):
    if not self.is_empty():
      item_to_remove = self.top_item
      self.top_item = item_to_remove.get_next_node()
      self.size -= 1
      return item_to_remove.get_value()
    else:
      print("This stack is totally empty.")
  
  def peek(self):
    if self.size > 0:
	    return self.top_item.get_value()
    else:
      print("Nothing to see here!")
      
  # Define has_space() and is_empty() below:
  
  def has_space(self):
    b = self.size < self.limit
    return b
  
  def is_empty(self):
    return self.size == 0
  
  
  
  
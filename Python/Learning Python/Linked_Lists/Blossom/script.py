#Lets add in the separate chaining aspect of our algorithm. Import the linked list and node library by calling
#from linked_list import Node, LinkedList
#At the top of script.py
from linked_list import Node, LinkedList

#Now lets add in some flower definitions! Use
#from blossom_lib import flower_definitions 
#To import the flower definitions.
from blossom_lib import flower_definitions

#LEARN HASH MAPS
#Blossom
#The language of the flowers has a long history and has often been a topic resigned to the domain of dusty books in a thrift bookseller or a library. With Blossom, we want to give people lightning fast access to all of the possible meanings of their favorite flowers.
#In this project, we are going to implement a hash map to relate the names of flowers to their meanings. In order to avoid collisions when our hashing function collides the names of two flowers, we are going to use separate chaining. We will implement the Linked List data structure for each of these separate chains.
#If you get stuck during this project or would like to see an experienced developer work through it, click Get Help to see a project walkthrough video.
# https://youtu.be/pJycHIBqPNg

#The underlying data structure for Blossom is going to be a key-value store that uses the common names for flowers as the key and saves the floral meaning of the flower as the value.
#In order to implement this functionality, were going to build out a hash map with separate chains of linked lists at every index.
#First, lets define our HashMap class.

class HashMap:
  
  #The first thing that well need for our hash map is an array. Pythons lists behave similar to an array, but well need to keep track and enforce the lists size to make the resemblance stronger.
  #Give HashMap a constructor that takes a size parameter. Save size into self.array_size.
  #After that, create a list of None objects of length size and save it into self.array.
  
  #In HashMap.__init__, find the line where we created a list of None objects.
  #Change this so that self.array instead is a list of LinkedLists.
  #The resulting self.array should be a Python list of LinkedList objects, make sure to instantiate them.
  def __init__(self, size):
    self.array_size = size
    #self.array = [None for i in range(size)]
    self.array = [LinkedList() for i in range(size)]
    
  #In order to implement a hash map, we need to implement four different methods.
#The first two are the internal methods needed to perform the basic responsibilities of a hash map: .hash() and .compress().
	#The next two are the external methods someone interacting with the hash map will use: .assign() and .retrieve().
	#Lets start by implementing a basic hash function. When the key is a string (which is true for all of Blossoms keys) well need to calculate a number for that string. Lets sum up the character encodings of each character in the string and use that.
	#Define a method called .hash() that takes both self and key as parameters.
  
  #Calculate the hash code for the key by calling key.encode() and performing the sum on the resulting list-like object.
  def hash(self, key):
    hash_code = sum(key.encode())
    return hash_code
  
  #Now that we have a hash function, that returns a number, well also need a compression function that reduces this number into an array index.
  #Define a .compress() method that takes a hash_code parameter. Return the result of calculating the remainder of dividing hash_code by self.array_size.
  def compress(self, hash_code):
    return hash_code % self.array_size

  #With our hash and compression functions written, all we need to create a basic hash map are our .assign() and .retrieve() methods. Lets start with .assign().
  #Define a .assign() method that takes three parameters: self, key, and value. Get the hash code by plugging key into .hash() and then get the array index by plugging the resulting hash code into .compress(). Save the result into the variable array_index.
  
  #In the array, at the address array_index, save both the key and the value as a list: [key, value].
  
  #In .assign(), were going to be replacing the assign logic after getting the array_index from the .hash() and .compressor() methods.
  #Create a new Node object with value [key, value]. Assign that Node object to a variable called payload.
  
  #Well need to check if the key exists in the LinkedList before we add our new payload to it. Save self.array[array_index] into the variable list_at_array.
  
  #Iterate through list_at_array using a for loop. For every item in list_at_array, check if the key (the element at index 0) is the same as the key were trying to assign.
  
  #If we do find a key at one of the items in the linked list, overwrite its value with value.
  
  #If weve iterated through the list and not found our key, we need to add it.
  #Remove the line where we assign
  #self.array[array_index] = [key, value]
  #And change it so that we use list_at_array.insert() to insert the payload to our chained list.
  def assign(self, key, value):
    array_index = self.compress(self.hash(key))
    #self.array[array_index] = [key, value]
    payload = Node([key, value])
    list_at_array = self.array[array_index]
    
    for item in list_at_array:      
      if (item[0] == key):
        item[1] = value
        return
    list_at_array.insert(payload)

  #Now that we have an assignment function, lets also build out our retrieval function.
  #Define a .retrieve() method that takes two parameters: self and key.
  
  #.retrieve() should find the hash code for key by plugging it into .hash() and then find the array index by plugging that hash code into .compress().
  #Save that index into a variable called array_index
  
  #Save the value of self.array at array_index into a variable called payload.
  
  #If payload is not None, then we know its a list that looks like [key, value].
  #Check the first item (payload[0]) and compare it with key. If they are the same, return the second item in payload (the value!).
  #If payload is None or the first item is not the same as key, return None.
  
  #Now were going to update .retrieve() to use separate chaining. Were going to rewrite the code after we get our array_index.
  #Using the array_index variable, get the LinkedList object at that index in self.array. Before we called this payload but since it represents a different type of object, lets name it something different.
  #Save the result into a variable called list_at_index.
  
  #Iterate through the linked list similarly to how .assign() did, checking the key in each part of the list to see if its the same as our key.
  
  #If you do find the key, return the value (at index 1 in the nodes value), otherwise return None!
  def retrieve(self, key):
    array_index = self.compress(self.hash(key))
    list_at_index = self.array[array_index]
    for item in list_at_index:
      if (item[0] == key):
        return item[1]
    return None
    #
    #payload = self.array[array_index]
    #if (not payload is None):
    #  if (payload[0] == key):
    #    return payload[1]
    #return None
    
#Now lets create a new instance of our HashMap create an instance called blossom. Make the list of our new HashMap the same length as flower_definitions.
blossom = HashMap(len(flower_definitions))

#Now, for every element of flower_definitions, assign the value (index 1) to its key (index 0) using blossom.assign().
for flower in flower_definitions:
  blossom.assign(flower[0], flower[1])

#Now use our app! Look up a flower’s meaning using blossom.retrieve('daisy'). Try printing it out!
#Does it work? Next, try looking up another flower. Is the flower you’re looking for missing? How would you add it in?
print(blossom.retrieve("daisy"))





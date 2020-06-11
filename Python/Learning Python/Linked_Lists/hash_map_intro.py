#Create a method for HashMap called .hash(). This method should take two arguments: self and key.

#Turn the key into a list of bytes by calling key.encode(). Save this into a variable called key_bytes.

#.encode() is a string method that converts a string into its corresponding bytes, a list-like object with the numerical representation of each character in the string.

#Turn the bytes object into a hash code by calling sum() on key_bytes. Save the result from that into a variable called hash_code.

#Return hash_code.

#Create a .compressor() method for your hash map.
#It should take two parameters: self and hash_code.
  
#Take the modulus of the hash code by the maps array_size in order to reduce the hash code to a possible index for the array.
#Return the modulus.

#Create a .assign() method for the hash map. It should take three parameters: self, key, and value.

#Save the value (just the value for now) to the maps array at the index determined by plugging the key into the .hash() method and plugging the hash code into the .compressor() method.

#Define a .retrieve()method for HashMap. It should take two parameters: self and key.

#.retrieve() should calculate the array index in the same way our .assign() does and then retrieve the value at that index.
#Return that value.

#Were going to overwrite the functionality for .assign(). After finding the array_index, we want to do a check of the content thats currently at self.array[array_index].
#In order to avoid overwriting the wrong key, check the existing value in the array at self.array[array_index]. Save this into current_array_value.

#There are three possibilities for current_array_value:

#It has the same key as key.
#It has a different key than key.
#Its None.
#If current_array_value already has contents, check if the saved key is different from the key we are currently processing. If the keys are the same, overwrite the array value.
#If the keys are different, were going to implement a way to find the next array index where our key should go. Well get to handling different keys later.

#In our .retrieve() method, after finding the array index, we want to check to make sure that the index corresponds to the key we’re looking for.
#Save the array value at our compressed hash code into possible_return_value.

#Instead of just returning the array’s contents at that index, check if possible_return_value is None. If so, return None.

#If possible_return_value is not None, check if the first element in possible_return_value (index 0) is the same as key.
#If so, return possible_return_value[1], the value.

#If our current array value doesn’t contain the key we’re getting, we’ll need to use open addressing to find the next place where the key will be. We’ll be doing that soon!

class HashMap:
  def __init__(self, array_size):
    self.array_size = array_size
    self.array = [None for item in range(array_size)]
    
  def hash(self, key):
    key_bytes = key.encode()
    hash_code = sum(key_bytes)
    return hash_code
  
  def compressor(self, hash_code):
    return hash_code % self.array_size
  
  #all keys are treated as the same key
  #lots of colliisions and overridding data 
  #def assign(self, key, value):
  #  self.array[self.compressor(self.hash(key))] = value   
  
  def assign(self, key, value):
    array_index = self.compressor(self.hash(key))
    current_array_value = self.array[array_index]

    if current_array_value is None:
      self.array[array_index] = [key, value]
      return

    if current_array_value[0] == key:
      self.array[array_index] = [key, value]
      return

    # current_array_value currently holds different key
    return      
      
    
  #  no addressing methods implemented at this point.
  def retrieve(self, key):
    array_index = self.compressor(self.hash(key))
    possible_return_value = self.array[array_index]
    if (possible_return_value == None):
      return None
    else:
      if (possible_return_value[0] == key):
        return possible_return_value[1]
	  return None
      
  
#Outside the HashMap class (completely unindented below the class definition) create a new hash map called hash_map. Give it an array size of 20.
hash_map = HashMap(20)

#We want to use this hash map to store geologic information  types of rocks.
#In hash_map save the value "metamorphic" for the key "gneiss".
hash_map.assign("gneiss", "metamorphic")

#Now retrieve the value of hash_map for the key gneiss. Print it out, does your HashMap work as expected?
print(hash_map.retrieve("gneiss"))





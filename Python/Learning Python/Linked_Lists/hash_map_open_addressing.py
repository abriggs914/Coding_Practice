#Open Addressing
#Now we’re going to implement an open addressing system so our hash map can resolve collisions. In open addressing systems, we check the array at the address given by our hashing function. One of three things can happen:
#The address points to an empty cell.
#The cell holds a value for the key we are getting/setting
#The cell holds a value for a different key.
#In the first case, this means that the hash map does not have a value for the key and no collision resolution needs to happen. Notice that this does not work if we want to be able to delete keys in our hash map. There are strategies for deleting pairs from a hash map (see Lazy Deletion) but we will not be investigating these.
#In the second case, we’ve found the value for our key-value pair!
#In the third case, we need to use our collision addressing strategy to find if our key is somewhere else (it may or may not be) so we should recalculate the index of our array.

class HashMap:
  
  def __init__(self, array_size):
    self.array_size = array_size
    self.array = [None for item in range(array_size)]

  #Give HashMap.hash() a second parameter: count_collisions. This will be the number of times the .hash() has hit a collision.
	#Have count_collisions default to 0.
  
  #Instead of returning hash_code from .hash(), return hash_code + count_collisions.
  def hash(self, key, count_collisions=0):
    key_bytes = key.encode()
    hash_code = sum(key_bytes)
    return hash_code + count_collisions

  def compressor(self, hash_code):
    return hash_code % self.array_size

	#Now that we have a hash function that uses the number of collisions to determine the hash code, we can update where we set a key in the event of a collision.
	#When we notice that the key we’re trying to set is different from the key at our hash code’s address, create a new variable called number_collisions, set that equal to 1.
  
  #After defining number_collisions, create a new while loop that checks if current_array_value[0] != key.
  
  #In the while loop, you want to replicate our setting logic while incrementing the number of collisions.
  #Call .hash() with both the key and number_collisions. Save that result into new_hash_code.
  
  #Plug new_hash_code into .compressor(). Save that result into new_array_index.
  
  #Check self.array at new_array_index and save the result as current_array_value. Check against the three possibilities:
  #If it’s None, save the [key, value] at self.array[new_array_index] and then return.
  #If it has a value, but the same key as key, overwrite the array at that address with [key, value] and then return.
  #If it has a value, but a different key, increment number_collisions.
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
    else:
      number_collisions = 1
      while (current_array_value[0] != key):
        new_hash_code = self.hash(key, number_collisions)
        new_array_index = self.compressor(new_hash_code)
        current_array_value = self.array[new_array_index]
        if (current_array_value is None):
          self.array[new_array_index] = [key, value]
          return
        if (current_array_value[0] == key):
          current_key_value[1] = value
          return
        else:
          number_collisions += 1
        
  #In .retrieve() if possible_return_value has a different key than the one we’re looking for, we should continue searching.
	#Define a new variable called retrieval_collisions and set it equal to 1.
  
  #Insert a new while loop that checks if
  #possible_return_value[0] != key
  #In the while loop, we want to replicate our retrieval logic while increasing the count of retrieval_collisions so that we continue to look at other locations within our array.
  #Call .hash() with both the key and retrieval_collisions. Save that result into new_hash_code.
  
  #Plug new_hash_code into .compressor(). Save that result into retrieving_array_index.
  
  #Check self.array at retrieving_array_index and save the result as possible_return_value. Check against the three possibilities:
  #If it’s None, return None
  #If it has a value, but a different key, increment retrieval_collisions.
  #If it’s key matches our key return possible_return_value[1].
  def retrieve(self, key):
    array_index = self.compressor(self.hash(key))
    possible_return_value = self.array[array_index]

    if possible_return_value is None:
        return None

    if possible_return_value[0] == key:
        return possible_return_value[1]

    # possible_return_value holds different key
    retrieval_collisions = 1
    while (possible_return_value[0] != key):
      new_hash_code = self.hash(key, retrieval_collisions)
      retrieving_array_index = self.compressor(new_hash_code)
      possible_return_value = self.array[retrieving_array_index]
      if (possible_return_value == None):
        return None
      if (possible_return_value[0] != key):
        retrieval_collisions += 1
      else:
        return possible_return_value[1]
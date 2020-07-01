# CODE CHALLENGE: DICTIONARIES
# Sum Values
# sum_values()

# Instructions
# 1.
# Write a function named sum_values that takes a dictionary named my_dictionary as a parameter. The function should return the sum of the values of the dictionary


# Hint
# Create a counter variable and start it at 0. Loop through all of the elements of my_dictionary.values() and add each value to your counter variable.

# Write your sum_values function here:
def sum_values(kwargs):
  return sum(kwargs.values())
  #s = 0
  #for k, v in kwargs.items():
  #  s += v
  #return s

# Uncomment these function calls to test your sum_values function:
print(sum_values({"milk":5, "eggs":2, "flour": 3}))
# should print 10
print(sum_values({10:1, 100:2, 1000:3}))
# should print 6

#######################################################################################################################
# CODE CHALLENGE: DICTIONARIES
# Even Keys
# sum_even_keys()

# Instructions
# 1.
# Create a function called sum_even_keys that takes a dictionary named my_dictionary, with all integer keys and values, as a parameter. This function should return the sum of the values of all even keys.


# Hint
# Create a counter variable and start it at 0. Loop through all of the elements of the keys of the dictionary by using my_dictionary.keys(). If the key is even (which you can check by using key % 2 == 0), add the corresponding value to the counter.

# Write your sum_even_keys function here:
def sum_even_keys(kwargs):
  return sum([v for k, v in kwargs.items() if k % 2 == 0])

# Uncomment these function calls to test your  function:
print(sum_even_keys({1:5, 2:2, 3:3}))
# should print 2
print(sum_even_keys({10:1, 100:2, 1000:3}))
# should print 6
#######################################################################################################################
# CODE CHALLENGE: DICTIONARIES
# Add Ten
# add_ten()

# Instructions
# 1.
# Create a function named add_ten that takes a dictionary with integer values named my_dictionary as a parameter. The function should add 10 to every value in my_dictionary and return my_dictionary


# Hint
# Loop through every key in the dictionary and add 10 to the value by using my_dictionary[key] += 10.

# Write your add_ten function here:
def add_ten(d):
  return {k: v+10 for k, v in d.items()}

# Uncomment these function calls to test your  function:
print(add_ten({1:5, 2:2, 3:3}))
# should print {1:15, 2:12, 3:13}
print(add_ten({10:1, 100:2, 1000:3}))
# should print {10:11, 100:12, 1000:13}
#######################################################################################################################
# CODE CHALLENGE: DICTIONARIES
# Values That Are Keys
# values_that_are_keys()

# Instructions
# 1.
# Create a function named values_that_are_keys that takes a dictionary named my_dictionary as a parameter. This function should return a list of all values in the dictionary that are also keys.


# Hint
# Loop through all values in the dictionary by using for value in my_dictionary.values(). Check to see if value is in my_dictionary.keys() and if so, append it to a list.

# Write your values_that_are_keys function here:

def values_that_are_keys(d):
  keys = d.keys()
  return [v for v in d.values() if v in keys]

# Uncomment these function calls to test your  function:
print(values_that_are_keys({1:100, 2:1, 3:4, 4:10}))
# should print [1, 4]
print(values_that_are_keys({"a":"apple", "b":"a", "c":100}))
# should print ["a"]
#######################################################################################################################

# CODE CHALLENGE: DICTIONARIES
# Largest Value
# max_key()

# Instructions
# 1.
# Write a function named max_key that takes a dictionary named my_dictionary as a parameter. The function should return the key associated with the largest value in the dictionary.


# Hint
# Begin by creating two variables named largest_key and largest_value. Initialize largest_value to be the smallest number possible (you can use float("-inf"). Initialize largest_key to be an empty string.

# Loop through all keys/value pair in the dictionary. Any time you find a value larger than what is currently stored in largest_value, replace largest_value with that new value. Similarly, replace largest_key with the key associated with the new largest value.

# After looping through all key/value pairs, return largest_key.
# Write your max_key function here:
def max_key(d):
  max_key = None
  max_val = None
  for k, v in d.items():
    if not max_key or v > max_val:
      max_key = k
      max_val = v
  return max_key

# Uncomment these function calls to test your  function:
print(max_key({1:100, 2:1, 3:4, 4:10}))
# should print 1
print(max_key({"a":100, "b":10, "c":1000}))
# should print "c"
#######################################################################################################################
# CODE CHALLENGE: DICTIONARIES
# Word Length Dict
# word_length_dictionary()

# Instructions
# 1.
# Write a function named word_length_dictionary that takes a list of strings named words as a parameter. The function should return a dictionary of key/value pairs where every key is a word in words and every value is the length of that word.


# Hint
# First create an empty dictionary named something like word_lengths. Loop through every word in words and add a new key using word_lengths[word] = len(word)

# Write your word_length_dictionary function here:
def word_length_dictionary(lst):
  sizes = [len(s) for s in lst]
  return dict(zip(lst, sizes))

# Uncomment these function calls to test your  function:
print(word_length_dictionary(["apple", "dog", "cat"]))
# should print {"apple":5, "dog": 3, "cat":3}
print(word_length_dictionary(["a", ""]))
# should print {"a": 1, "": 0}
#######################################################################################################################
# CODE CHALLENGE: DICTIONARIES
# Frequency Count
# frequency_dictionary()

# Instructions
# 1.
# Write a function named frequency_dictionary that takes a list of elements named words as a parameter. The function should return a dictionary containing the frequency of each element in words.


# Hint
# First, create a new empty dictionary. Then, loop through every word in words. If word is not a key in the dictionary, make word a key with a value of 1. If word was already a key, increase the value associated with word by 1.

# Write your frequency_dictionary function here:
def frequency_dictionary(words):
  s = set(words)
  c = [words.count(w) for w in s]
  return dict(zip(s, c))

# Uncomment these function calls to test your  function:
print(frequency_dictionary(["apple", "apple", "cat", 1]))
# should print {"apple":2, "cat":1, 1:1}
print(frequency_dictionary([0,0,0,0,0]))
# should print {0:5}
#######################################################################################################################
# CODE CHALLENGE: DICTIONARIES
# Unique Values
# unique_values()

# Instructions
# 1.
# Create a function named unique_values that takes a dictionary named my_dictionary as a parameter. The function should return the number of unique values in the dictionary.


# Hint
# Begin by creating a new empty list named seen_values. Loop through all of the values of my_dictionary. For every value, check to see if that value is in seen_values. If it is, continue to the next value. If it is not, add it to seen_values. After looping through all values, return the length of seen_values.

# Write your unique_values function here:
def unique_values(d):
  return len(set(d.values()))

# Uncomment these function calls to test your  function:
print(unique_values({0:3, 1:1, 4:1, 5:3}))
# should print 2
print(unique_values({0:3, 1:3, 4:3, 5:3}))
# should print 1
#######################################################################################################################
# CODE CHALLENGE: DICTIONARIES
# Count First Letter
# count_first_letter()

# Instructions
# 1.
# Create a function named count_first_letter that takes a dictionary named names as a parameter. names should be a dictionary where the key is a last name and the value is a list of first names. For example, the dictionary might look like this:

# names = {"Stark": ["Ned", "Robb", "Sansa"], "Snow" : ["Jon"], "Lannister": ["Jaime", "Cersei", "Tywin"]}
# The function should return a new dictionary where each key is the first letter of a last name, and the value is the number of people whose last name begins with that letter.

# So in example above, the function would return:

# {"S" : 4, "L": 3}

# Hint
# Begin by creating an empty dictionary named something like letters. Loop through the keys of names and access the first letter of each the key using key[0].

# If that letter is not a key in letters, create a new key/value pair where the key is key[0] and the value is the length of names[key].

# If that letter is a key in letters, simply add the length of names[key] to value associated with key[0] in letters.

# Write your count_first_letter function here:
def count_first_letter(names):
  d = {}
  for key, v in names.items():
    k = key[0]
    if k not in d:
      d[k] = len(v)
    else:
      d[k] += len(v)
  return d


# Uncomment these function calls to test your  function:
print(count_first_letter({"Stark": ["Ned", "Robb", "Sansa"], "Snow" : ["Jon"], "Lannister": ["Jaime", "Cersei", "Tywin"]}))
# should print {"S": 4, "L": 3}
print(count_first_letter({"Stark": ["Ned", "Robb", "Sansa"], "Snow" : ["Jon"], "Sannister": ["Jaime", "Cersei", "Tywin"]}))
# should print {"S": 7}
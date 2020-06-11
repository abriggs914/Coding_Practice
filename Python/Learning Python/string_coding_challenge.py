# CODE CHALLENGE: STRING METHODS
# Count Letters
# unique_english_letters(word)

# Instructions
# 1.
# Write a function called unique_english_letters that takes the string word as a parameter. The function should
# return the total number of unique letters in the string. Uppercase and lowercase letters should be
# counted as different letters.

# We’ve given you a list of every uppercase and lower case letter in the English alphabet. It will be
# helpful to include that list in your function.


# Hint
# Loop through the list of English letters and check to see if each letter is included in word by using in.

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
# Write your unique_english_letters function here:

def unique_english_letters(word):
  return len(set(word))

# Uncomment these function calls to test your function:
print(unique_english_letters("mississippi"))
# should print 4
print(unique_english_letters("Apple"))
# should print 4

#######################################################################################################################

# CODE CHALLENGE: STRING METHODS
# Count X
# count_char_x()

# Instructions
# 1.
# Write a function named count_char_x that takes a string named word and a single character named x as parameters.
# The function should return the number of times x appears in word.


# Hint
# Use a for loop to loop through all of the characters of word. If the letter is equal to the value of x,
# increase a counter variable by one.

# Write your count_char_x function here:

def count_char_x(word, x):
  return word.count(x)

# Uncomment these function calls to test your tip function:
print(count_char_x("mississippi", "s"))
# should print 4
print(count_char_x("mississippi", "m"))
# should print 1

#######################################################################################################################
# CODE CHALLENGE: STRING METHODS
# Count Multi X
# count_multi_char_x()

# Instructions
# 1.
# Write a function named count_multi_char_x that takes a string named word and a string named x. This function should do the same thing as the count_char_x function you just wrote - it should return the number of times x appears in word. However, this time, make sure your function works when x is multiple characters long.

# For example, count_multi_char_x("Mississippi", "iss") should return 2


# Hint
# Consider using the split function. How does the length of word.split(x) relate to the number of times x was in word?

# Write your count_multi_char_x function here:

def count_multi_char_x(word, x):
  return word.count(x)

# Uncomment these function calls to test your function:
print(count_multi_char_x("mississippi", "iss"))
# should print 2
print(count_multi_char_x("apple", "pp"))
# should print 1
#######################################################################################################################
# CODE CHALLENGE: STRING METHODS
# Substring Between
# substring_between_letters()

# Instructions
# 1.
# Write a function named substring_between_letters that takes a string named word, a single character named start, and another character named end. This function should return the substring between the first occurrence of start and end in word. If start or end are not in word, the function should return word.

# For example, substring_between_letters("apple", "p", "e") should return "pl".


# Hint
# Begin by finding the indices of the start and end characters by using word.find(start) and word.find(end).

# If either of those indices are -1, then the original string didn’t contain one of those characters, and you should return word.

# If neither are -1, then slice word using those indices. Remember, slicing is [inclusive:exclusive]!
# Write your substring_between_letters function here:

def substring_between_letters(word, start, end):
  start_idx = word.find(start) + 1
  end_idx = word.find(end)
  if start_idx < 0 or end_idx < 0:
    return word
  return word[start_idx: end_idx]

# Uncomment these function calls to test your function:
print(substring_between_letters("apple", "p", "e"))
# should print "pl"
print(substring_between_letters("apple", "p", "c"))
# should print "apple"
#######################################################################################################################
# CODE CHALLENGE: STRING METHODS
# X Length
# x_length_words()

# Instructions
# 1.
# Create a function called x_length_words that takes a string named sentence and an integer named x as parameters. This function should return True if every word in sentence has a length greater than or equal to x.


# Hint
# First create a list of every word in sentence by using sentence.split(). Then iterate through that list and if any of the words have a length less than x, return False. If you iterate through all of the words and haven’t returned False, you know every word had a length greater than or equal to x, so you should return True.

# Write your x_length_words function here:
def x_length_words(sentence, x):
  is_longer = True
  for s in sentence.split(" "):
      is_longer = is_longer and len(s) >= x
  return is_longer

# Uncomment these function calls to test your tip function:
print(x_length_words("i like apples", 2))
# should print False
print(x_length_words("he likes apples", 2))
# should print True
#######################################################################################################################
# CODE CHALLENGE: STRING METHODS
# Check Name
# check_for_name()

# Instructions
# 1.
# Write a function called check_for_name that takes two strings as parameters named sentence and name. The function should return True if name appears in sentence in all lowercase letters, all uppercase letters, or with any mix of uppercase and lowercase letters. The function should return False otherwise.

# For example, the following three calls should all return True:

# check_for_name("My name is Jamie", "Jamie")
# check_for_name("My name is jamie", "Jamie")
# check_for_name("My name is JAMIE", "Jamie")

# Hint
# name.lower() in sentence.lower() will help you find out if the name is in the sentence.
# Write your check_for_name function here:

def check_for_name(sentence, name):
  return name.lower() in sentence.lower()

# Uncomment these function calls to test your  function:
print(check_for_name("My name is Jamie", "Jamie"))
# should print True
print(check_for_name("My name is jamie", "Jamie"))
# should print True
print(check_for_name("My name is Samantha", "Jamie"))
# should print False
#######################################################################################################################
# CODE CHALLENGE: STRING METHODS
# Every Other Letter
# every_other_letter()

# Instructions
# 1.
# Create a function named every_other_letter that takes a string named word as a parameter. The function should return a string containing every other letter in word.


# Hint
# The following code will print all letters of a string by index:

# my_string = "Hello World"
# for i in range(len(my_string)):
#   print my_string[i]
# In this code, i starts at 0 and increase until it is once less than the length of my_string. How could you make i increase by more than one each time?

# Additionally, instead of printing each individual letter, you should add each letter to a new string using +.

# Write your every_other_letter function here:
def every_other_letter(word):
  r = ""
  for i in range(0, len(word), 2):
    r += word[i]
  return r

# Uncomment these function calls to test your function:
print(every_other_letter("Codecademy"))
# should print Cdcdm
print(every_other_letter("Hello world!"))
# should print Hlowrd
print(every_other_letter(""))
# should print 
#######################################################################################################################
# Instructions
# 1.
# Write a function named reverse_string that has a string named word as a parameter. The function should return word in reverse.


# Hint
# Just like the last challenge, you want to access each letter of word by it’s index.

# my_string = "Hello World"
# for i in range(len(my_string)):
#   print my_string[i]
# However, you don’t want i to start at 0. Instead you want it to start at the last index of your string (len(my_string)-1) and end at 0.

# Edit the call to the range function to do this. Remember, the range function can take three parameters: the starting number (inclusive), the ending number (exclusive), and the step. To count down, make the step -1.

# Write your reverse_string function here:
def reverse_string(word):
  r = ""
  for i in range(len(word)-1, -1, -1):
    r += word[i]
  return r

# Uncomment these function calls to test your  function:
print(reverse_string("Codecademy"))
# should print ymedacedoC
print(reverse_string("Hello world!"))
# should print !dlrow olleH
print(reverse_string(""))
# should print
#######################################################################################################################
# CODE CHALLENGE: STRING METHODS
# Make Spoonerism
# make_spoonerism()

# Instructions
# 1.
# A Spoonerism is an error in speech when the first syllables of two words are switched. For example, a Spoonerism is made when someone says “Belly Jeans” instead of “Jelly Beans”.

# Write a function called make_spoonerism that takes two strings as parameters named word1 and word2. Finding the first syllable of a word is a difficult task, so for our function, we’re going to switch the first letters of each word. Return the two new words as a single string separated by a space.


# Hint
# word2[0] will access the first letter of word2. word1[1:] will access everything but the first letter of word1. Combining those with a + will give you your first new word.

# Write your make_spoonerism function here:
def make_spoonerism(word1, word2):
  return word2[0] + word1[1:] + " " + word1[0] + word2[1:]

# Uncomment these function calls to test your function:
print(make_spoonerism("Codecademy", "Learn"))
# should print Lodecademy Cearn
print(make_spoonerism("Hello", "world!"))
# should print wello Horld!
print(make_spoonerism("a", "b"))
# should print b a
#######################################################################################################################
# CODE CHALLENGE: STRING METHODS
# Add Exclamation
# add_exclamation()

# Instructions
# 1.
# Create a function named add_exclamation that has one parameter named word. This function should add exclamation points to the end of word until word is 20 characters long. If word is already at least 20 characters long, just return word.


# Hint
# Use a while loop to add exclamation points to word. The while loop should stop when the length of word is greater than or equal to 20.

# Write your add_exclamation function here:
def add_exclamation(word):
  x = len(word)
  y = []
  if x < 20:
    y = ["!" for i in range(20-x)]
  return word + "".join(y)

# Uncomment these function calls to test your function:
print(add_exclamation("Codecademy"))
# should print Codecademy!!!!!!!!!!
print(add_exclamation("Codecademy is the best place to learn"))
# should print Codecademy is the best place to learn
#######################################################################################################################
#Write a function called contains that takes two arguments, big_string and little_string and returns True if big_string contains little_string.
#For example contains("watermelon", "melon") should return True and contains("watermelon", "berry") should return False.
def contains(big_string, little_string):
  if little_string in big_string:
    return True
  return False

#Write a function called common_letters that takes two arguments, string_one and string_two and then returns a list with all of the letters they have in common.
#The letters in the returned list should be unique. For example,
#common_letters("banana", "cream")
#should return ['a'].
def common_letters(string_one, string_two): 
  res = []
  for letterA in string_one:
    for letterB in string_two:
      if (letterA == letterB and res.count(letterA) == 0):
        res.append(letterA)
  return res
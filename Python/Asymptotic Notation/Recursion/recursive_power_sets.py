#RECURSION: PYTHON
#Stack Over-Whoa!
#The previous exercise ended with a stack overflow, which is a reminder that recursion has costs that iteration doesn’t. We saw in the first exercise that every recursive call spends time on the call stack.
#Put enough function calls on the call stack, and eventually there’s no room left.
#Even when there is room for any reasonable input, recursive functions tend to be at least a little less efficient than comparable iterative solutions because of the call stack.
#The beauty of recursion is how it can reduce complex problems into an elegant solution of only a few lines of code. Recursion forces us to distill a task into its smallest piece, the base case, and the smallest step to get there, the recursive step.
#Let’s compare two solutions to a single problem: producing a power set. A power set is a list of all subsets of the values in a list.
#This is a really tough algorithm. Don’t be discouraged!
#power_set(['a', 'b', 'c'])
# [
#   ['a', 'b', 'c'], 
#   ['a', 'b'], 
#   ['a', 'c'], 
#   ['a'], 
#   ['b', 'c'], 
#   ['b'], 
#   ['c'], 
#   []
# ]
#Phew! That’s a lot of lists! Our input length was 3, and the list returned had a length of 8.
#Producing subsets requires a runtime of at least O(2^N), we’ll never do better than that because a set of N elements creates a power set of 2^N elements.
#Binary, a number system of base 2, can represent 2^N numbers for N binary digits. For example:
# 1 binary digit, 2 numbers
# 0 in binary
#0
# 1 in binary
#1
# 2 binary digits, 4 numbers
# 00 => 0
# 01 => 1
# 10 => 2
# 11 => 3
#The iterative approach uses this insight for a very clever solution by including an element in the subset if its “binary digit” is 1.
#set = ['a', 'b', 'c']
#binary_number = "101"
# produces the subset ['a', 'c']
# 'b' is left out because its binary digit is 0
#That process is repeated for all O(2^N) numbers!
#Here is the complete solution. You’re not expected to understand every line, just take in the level of complexity.
#def power_set(set):
#  power_set_size = 2**len(set)
#  result = []
#  for bit in range(0, power_set_size):
#    sub_set = []
#    for binary_digit in range(0, len(set)):
#      if((bit & (1 << binary_digit)) > 0):
#        sub_set.append(set[binary_digit])
#    result.append(sub_set)
#  return result
#Very clever but not very intuitive! Let’s try recursion.
#Consider the base case, where the problem has become so simple we can solve it without doing any work.
#What’s the simplest power set possible? An empty list!
#power_set([])
# [[]]
#Now the recursive step. We need to progress towards our base case, an empty list, so we’ll be removing an element from the input.
#Examine the simplest powerset that isn’t the base case:
#power_set(['a'])
# [[], ['a']]
#A power set in the recursive step requires:
#all subsets which contain the element
#in this case "a"
#all subsets which don’t contain the element
#in this case [].
#With the recursive approach, we’re able to articulate the problem in terms of itself. No need to bring in a whole number system to find the solution!
#Here’s the recursive solution in its entirety:
#def power_set(my_list):
#  if len(my_list) == 0:
#    return [[]]
#  power_set_without_first = power_set(my_list[1:])
#  with_first = [ [my_list[0]] + rest for rest in power_set_without_first ]
#  return with_first + power_set_without_first
#Neither of these solutions is simple, this is a complicated algorithm, but the recursive solution is almost half the code and more directly conveys what this algorithm does.
#Give yourself a pat on the back for making it through a tough exercise!

#-------------------------------------------------------------------------------------------------------------------------------------------------------

def power_set_iter(set):
  power_set_size = 2**len(set)
  result = []

  for bit in range(0, power_set_size):
    sub_set = []
    for binary_digit in range(0, len(set)):
      if((bit & (1 << binary_digit)) > 0):
        sub_set.append(set[binary_digit])
    result.append(sub_set)
  return result
  
def power_set_rec(my_list):
  if len(my_list) == 0:
    return [[]]
  power_set_without_first = power_set_rec(my_list[1:])
  with_first = [ [my_list[0]] + rest for rest in power_set_without_first ]
  return with_first + power_set_without_first
  
print(power_set_iter([]))
print(power_set_iter(["a","b"]))
print(power_set_iter(["a","b","c","d"]))

print(power_set_rec([]))
print(power_set_rec(["a","b"]))
print(power_set_rec(["a","b","c","d"]))

#-------------------------------------------------------------------------------------------------------------------------------------------------------

def power_set(my_list):
    # base case: an empty list
    if len(my_list) == 0:
        return [[]]
    # recursive step: subsets without first element
    power_set_without_first = power_set(my_list[1:])
    # subsets with first element
    with_first = [ [my_list[0]] + rest for rest in power_set_without_first ]
    # return combination of the two
    return with_first + power_set_without_first
  
universities = ['MIT', 'UCLA', 'Stanford', 'NYU']
power_set_of_universities = power_set(universities)

for set in power_set_of_universities:
  print(set)

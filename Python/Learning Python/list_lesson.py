'''
Python Code Challenges: Lists
Python Code Challenges involving Lists

This article will help you review Python functions by providing some code challenges involving lists.

Some of these challenges are difficult! Take some time to think about them before starting to code.

You might not get the solution correct on your first try — look at your output, try to find where you’re going wrong, and iterate on your solution.

Finally, if you get stuck, use our solution code! If you “Check Answer” twice with an incorrect solution, you should see an option to get our solution code. However, truly investigate that solution — experiment and play with the solution code until you have a good grasp of how it is working. Good luck!

Function Syntax
As a refresher, function syntax looks like this:

def some_function(some_input1, some_input2):
  # … do something with the inputs …
  return output
For example, a function that returns the sum of the first and last elements of a given list might look like this:

def first_plus_last(lst):
  return lst[0] + lst[-1]
And this would produce output like:

>>> first_plus_last([1, 2, 3, 4])
5
>>> first_plus_last([8, 2, 5, -8])
0
>>> first_plus_last([-10, 2, 3, -4])
-14
Challenges
We’ve included 5 list challenges below. Try to answer all of them and polish up your problem-solving skills and your list expertise

1. Append Sum
Write a function named append_sum that has one parameter — a list named named lst.

The function should add the last two elements of lst together and append the result to lst. It should do this process three times and then return lst.

For example, if lst started as [1, 1, 2], the final result should be [1, 1, 2, 3, 5, 8].

1
#Write your function here
2
​
3
def append_sum(lst):
4
  for i in range(3):
5
    lst.append(lst[-1] + lst[-2])
6
  return lst
7
​
8
#Uncomment the line below when your function is done
9
print(append_sum([1, 1, 2]))
[1, 1, 2, 3, 5, 8]
 
👏
You got it!
2. Larger List
Write a function named larger_list that has two parameters named lst1 and lst2.

The function should return the last element of the list that contains more elements. If both lists are the same size, then return the last element of lst1.

1
#Write your function here
2
​
3
def larger_list(lst1, lst2):
4
  return lst1[-1] if len(lst1) >= len(lst2) else lst2[-1]
5
​
6
​
7
#Uncomment the line below when your function is done
8
print(larger_list([4, 10, 2, 5], [-10, 2, 5, 10]))
5
 
👏
You got it!
3. More Than N
Create a function named more_than_n that has three parameters named lst, item, and n.

The function should return True if item appears in the list more than n times. The function should return False otherwise.

1
#Write your function here
2
​
3
def more_than_n(lst, item, n):
4
  return lst.count(item) > n
5
​
6
​
7
#Uncomment the line below when your function is done
8
print(more_than_n([2, 4, 6, 2, 3, 2, 1, 2], 2, 3))
True
 
👏
You got it!
4. Append Size
Create a function called append_size that has one parameter named lst.

The function should append the size of lst (inclusive) to the end of lst. The function should then return this new list.

For example, if lst was [23, 42, 108], the function should return [23, 42, 108, 3] because the size of lst was originally 3.

1
#Write your function here
2
​
3
def append_size(lst):
4
  lst.append(len(lst))
5
  return lst
6
​
7
​
8
#Uncomment the line below when your function is done
9
print(append_size([23, 42, 108]))
[23, 42, 108, 3]
 
👏
You got it!
5. Combine Sort
Write a function named combine_sort that has two parameters named lst1 and lst2.

The function should combine these two lists into one new list and sort the result. Return the new sorted list.

1
#Write your function here
2
​
3
def combine_sort(lst1, lst2):
4
  lst3 = lst1 + lst2
5
  lst3.sort()
6
  return lst3
7
​
8
​
9
#Uncomment the line below when your function is done
10
print(combine_sort([4, 10, 2, 5], [-10, 2, 5, 10]))
[-10, 2, 2, 4, 5, 5, 10, 10]
 
👏
You got it!
'''

'''
Advanced Python Code Challenges: Lists
Difficult Python Code Challenges involving Lists

This article will help you review Python functions by providing some code challenges involving lists.

Some of these challenges are difficult! Take some time to think about them before starting to code.

You might not get the solution correct on your first try — look at your output, try to find where you’re going wrong, and iterate on your solution.

Finally, if you get stuck, use our solution code! If you “Check Answer” twice with an incorrect solution, you should see an option to get our solution code. However, truly investigate that solution — experiment and play with the solution code until you have a good grasp of how it is working. Good luck!

Function Syntax
As a refresher, function syntax looks like this:

def some_function(some_input1, some_input2):
  # … do something with the inputs …
  return output
For example, a function that returns the sum of the first and last elements of a given list might look like this:

def first_plus_last(lst):
  return lst[0] + lst[-1]
And this would produce output like:

>>> first_plus_last([1, 2, 3, 4])
5
>>> first_plus_last([8, 2, 5, -8])
0
>>> first_plus_last([-10, 2, 3, -4])
-14
Challenges
We’ve included 5 list challenges below. Try to answer all of them and polish up your problem-solving skills and your list expertise!

1. Every Three Numbers
Create a function called every_three_nums that has one parameter named start.

The function should return a list of every third number between start and 100 (inclusive). For example, every_three_nums(91) should return the list [91, 94, 97, 100]. If start is greater than 100, the function should return an empty list.

1
1
#Write your function here
2
​
3
def every_three_nums(start):
4
  return list(range(start, 101, 3))
5
​
6
​
7
#Uncomment the line below when your function is done
8
print(every_three_nums(91))
[91, 94, 97, 100]
 
👏
You got it!
2. Remove Middle
Create a function named remove_middle which has three parameters named lst, start, and end.

The function should return a list where all elements in lst with an index between start and end (inclusive) have been removed.

For example, the following code should return [4, 23, 42] because elements at indices 1, 2, and 3 have been removed:

remove_middle([4, 8 , 15, 16, 23, 42], 1, 3)
1
#Write your function here
2
​
3
def remove_middle(lst, start, end):
4
  return lst[:start] + lst[end + 1:]
5
​
6
​
7
#Uncomment the line below when your function is done
8
print(remove_middle([4, 8, 15, 16, 23, 42], 1, 3))
[4, 23, 42]
 
👏
You got it!
3. More Frequent Item
Create a function named more_frequent_item that has three parameters named lst, item1, and item2.

Return either item1 or item2 depending on which item appears more often in lst.

If the two items appear the same number of times, return item1.

item2
1
#Write your function here
2
​
3
def more_frequent_item(lst, item1, item2):
4
  return item1 if lst.count(item1) >= lst.count(item2) else item2
5
​
6
#Uncomment the line below when your function is done
7
print(more_frequent_item([2, 3, 3, 2, 3, 2, 3, 2, 3], 2, 3))
3
 
👏
You got it!
4. Double Index
Create a function named double_index that has two parameters: a list named lst and a single number named index.

The function should return a new list where all elements are the same as in lst except for the element at index. The element at index should be double the value of the element at index of the original lst.

If index is not a valid index, the function should return the original list.

For example, the following code should return [1,2,6,4] because the element at index 2 has been doubled:

double_index([1, 2, 3, 4], 2)
After writing your function, un-comment the call to the function that we’ve provided for you to test your results.

1
#Write your function here
2
def double_index(lst, index):
3
  if index < len(lst):
4
    lst[index] *= 2
5
  return lst
6
​
7
#Uncomment the line below when your function is done
8
print(double_index([3, 8, -10, 12], 2))
[3, 8, -20, 12]
 
👏
You got it!
5. Middle Item
Create a function called middle_element that has one parameter named lst.

If there are an odd number of elements in lst, the function should return the middle element. If there are an even number of elements, the function should return the average of the middle two elements.

1
#Write your function here
2
​
3
def middle_element(lst):
4
  mid = int(len(lst) / 2)
5
  print("mid: " + str(mid) + ", l[mid]: " + str(lst[mid]))
6
  if len(lst) % 2 == 1:
7
    return lst[mid]
8
  else:
9
    return (lst[mid - 1] + lst[mid]) / 2
10
#Uncomment the line below when your function is done
11
​
12
l = [5, 2, -10, -4, 4, 5]
13
print(middle_element(l))
14
print(middle_element(l) == -7)
mid: 3, l[mid]: -4
-7.0
mid: 3, l[mid]: -4
True
 
👏
You got it!
'''
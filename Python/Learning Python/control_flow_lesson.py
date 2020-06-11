'''
Python Code Challenges: Control Flow
Python Code Challenges involving Control Flow

This article will help you review Python functions by providing some code challenges about control flow.

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
We’ve included 5 challenges below. Try to answer all of them and polish up your problem-solving skills and your control flow expertise.

1. Large Power
Create a function named large_power() that takes two parameters named base and exponent.

If base raised to the exponent is greater than 5000, return True, otherwise return False

1
# Write your large_power function here:
2
def large_power(base, exponent):
3
  return base ** exponent > 5000
4
​
5
# Uncomment these function calls to test your large_power function:
6
print(large_power(2, 13))
7
# should print True
8
print(large_power(2, 12))
9
# should print False
True
False
 
👏
You got it!
2. Over Budget
Create a function called over_budget that has five parameters named budget, food_bill, electricity_bill, internet_bill, and rent.

The function should return True if budget is less than the sum of the other four parameters — you’ve gone over budget! Return False otherwise.

1
# Write your over_budget function here:
2
def over_budget(budget, food_bill, electricity_bill, internet_bill, rent):
3
  return budget < (food_bill + electricity_bill + internet_bill + rent)
4
​
5
# Uncomment these function calls to test your over_budget function:
6
print(over_budget(100, 20, 30, 10, 40))
7
# should print False
8
print(over_budget(80, 20, 30, 10, 30))
9
# should print True
False
True
 
👏
You got it!
3. Twice As Large
Create a function named twice_as_large() that has two parameters named num1 and num2.

Return True if num1 is more than double num2. Return False otherwise.

1
# Write your twice_as_large function here:
2
​
3
def twice_as_large(num1, num2):
4
  return num1 > 2*num2
5
​
6
# Uncomment these function calls to test your twice_as_large function:
7
print(twice_as_large(10, 5))
8
# should print False
9
print(twice_as_large(11, 5))
10
# should print True
False
True
 
👏
You got it!
4. Divisible By Ten
Create a function called divisible_by_ten() that has one parameter named num.

The function should return True if num is divisible by 10, and False otherwise. Consider using modulo (%) to check for divisibility.

1
# Write your divisible_by_ten function here:
2
​
3
def divisible_by_ten(num):
4
  return num % 10 == 0
5
​
6
# Uncomment these function calls to test your divisible_by_ten function:
7
print(divisible_by_ten(20))
8
# should print True
9
print(divisible_by_ten(25))
10
# should print False
True
False
 
👏
You got it!
5. Not Equal
Create a function named not_sum_to_ten() that has two parameters named num1 and num2.

Return True if num1 and num2 do not sum to 10. Return False otherwise.

1
# Write your not_sum_to_ten function here:
2
​
3
def not_sum_to_ten(num1, num2):
4
  return num1 + num2 != 10
5
  
6
# Uncomment these function calls to test your not_sum_to_ten function:
7
print(not_sum_to_ten(9, -1))
8
# should print True
9
print(not_sum_to_ten(9, 1))
10
# should print False
11
print(not_sum_to_ten(5,5))
12
# should print False
True
False
False
 
👏
You got it!
'''

'''
Advanced Python Code Challenges: Control Flow
Difficult Python Code Challenges Involving Control Flow

This article will help you review Python functions by providing some code challenges involving control flow.

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
We’ve included 5 challenges below. Try to answer all of them and polish up your problem-solving skills!

1. In Range
Create a function named in_range() that has three parameters named num, lower, and upper.

The function should return True if num is greater than or equal to lower and less than or equal to upper. Otherwise, return False.

1
# Write your in_range function here:
2
​
3
def in_range(num, lower, upper):
4
  return num in range(lower, upper + 1)
5
​
6
# Uncomment these function calls to test your in_range function:
7
print(in_range(10, 10, 10))
8
# should print True
9
print(in_range(5, 10, 20))
10
# should print False
True
False
 
👏
You got it!
2. Same Name
Create a function named same_name() that has two parameters named your_name and my_name.

If our names are identical, return True. Otherwise, return False.

1
# Write your same_name function here:
2
def same_name(your_name, my_name):
3
  return your_name == my_name
4
​
5
# Uncomment these function calls to test your same_name function:
6
print(same_name("Colby", "Colby"))
7
# should print True
8
print(same_name("Tina", "Amber"))
9
# should print False
True
False
 
👏
You got it!
3. Always False
Create a function named always_false() that has one parameter named num.

Using an if statement, your variable num, and the operators >, and <, make it so your function will return False no matter what number is stored in num.

An if statement that is always false is called a contradiction. You will rarely want to do this while programming, but it is important to realize it is possible to do this.

1
# Write your always_false function here:
2
​
3
def always_false(num):
4
  return num > 0 and num < 0
5
​
6
# Uncomment these function calls to test your always_false function:
7
print(always_false(0))
8
# should print False
9
print(always_false(-1))
10
# should print False
11
print(always_false(1))
12
# should print False
False
False
False
 
👏
You got it!
4. Movie Review
Create a function named movie_review() that has one parameter named rating.

If rating is less than or equal to 5, return "Avoid at all costs!". If rating is between 5 and 9, return "This one was fun.". If rating is 9 or above, return "Outstanding!"

eview
1
# Write your movie_review function here:
2
​
3
def movie_review(rating):
4
  if rating < 6:
5
    return "Avoid at all costs!"
6
  elif rating in range(5, 9):
7
    return "This one was fun."
8
  else:
9
    return "Outstanding!"
10
​
11
# Uncomment these function calls to test your movie_review function:
12
print(movie_review(9))
13
# should print "Outstanding!"
14
print(movie_review(4))
15
# should print "Avoid at all costs!"
16
print(movie_review(6))
17
# should print "This one was fun."
Outstanding!
Avoid at all costs!
This one was fun.
 
👏
You got it!
5. Max Number
Create a function called max_num() that has three parameters named num1, num2, and num3.

The function should return the largest of these three numbers. If any of two numbers tie as the largest, you should return "It's a tie!".

-2
1
# Write your max_num function here:
2
​
3
def max_num(num1, num2, num3):
4
  l = [num1, num2, num3]
5
  l.sort()
6
  return l[-1] if l[-2] != l[-1] else "It\'s a tie!"
7
​
8
# Uncomment these function calls to test your max_num function:
9
print(max_num(-10, 0, 10))
10
# should print 10
11
print(max_num(-10, 5, -30))
12
# should print 5
13
print(max_num(-5, -10, -10))
14
# should print -5
15
print(max_num(2, 3, 3))
16
# should print "It's a tie!"
17
​
10
5
-5
It's a tie!
 
👏
You got it!
'''
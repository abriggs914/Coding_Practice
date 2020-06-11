'''
This article will help you review Python functions by providing some code challenges.

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
We’ve included 5 challenges below. Try to answer all of them and polish up your problem-solving skills and your function expertise.

1. Tenth Power
Write a function named tenth_power() that has one parameter named num.

The function should return num raised to the 10th power.

1
# Write your tenth_power function here:
2
​
3
def tenth_power(num):
4
  return num ** 10
5
​
6
# Uncomment these function calls to test your tenth_power function:
7
print(tenth_power(1))
8
# 1 to the 10th power is 1
9
print(tenth_power(0))
10
# 0 to the 10th power is 0
11
print(tenth_power(2))
12
# 2 to the 10th power is 1024
1
0
1024
 
👏
You got it!
2. Square Root
Write a function named square_root() that has one parameter named num.

Use exponents (**) to return the square root of num.

1
# Write your square_root function here:
2
​
3
def square_root(num):
4
  return num ** 0.5
5
​
6
# Uncomment these function calls to test your square_root function:
7
print(square_root(16))
8
# should print 4
9
print(square_root(100))
10
# should print 10
4.0
10.0
 
👏
You got it!
3. Win Percentage
Create a function called win_percentage() that takes two parameters named wins and losses.

This function should return out the total percentage of games won by a team based on these two numbers.

int
1
# Write your win_percentage function here:
2
​
3
def win_percentage(wins, losses):
4
  return int((wins / (wins + losses)) * 100)
5
​
6
# Uncomment these function calls to test your win_percentage function:
7
print(win_percentage(5, 5))
8
# should print 50
9
print(win_percentage(10, 0))
10
# should print 100
50
100
 
👏
You got it!
4. Average
Write a function named average() that has two parameters named num1 and num2.

The function should return the average of these two numbers.

1
# Write your average function here:
2
​
3
def average(num1, num2):
4
  return (num1 + num2) / 2
5
​
6
# Uncomment these function calls to test your average function:
7
print(average(1, 100))
8
# The average of 1 and 100 is 50.5
9
print(average(1, -1))
10
# The average of 1 and -1 is 0
50.5
0.0
 
👏
You got it!
5. Remainder
Write a function named remainder() that has two parameters named num1 and num2.

The function should return the remainder of twice num1 divided by half of num2.

d print 2
print(remainder(9, 6))
# should print 0
1
# Write your remainder function here:
2
​
3
def remainder(num1, num2):
4
  return (num1 * 2) % (num2 / 2)
5
​
6
# Uncomment these function calls to test your remainder function:
7
print(remainder(15, 14))
8
# should print 2
9
print(remainder(9, 6))
10
# should print 0
'''

'''
Advanced Python Code Challenges: Functions
Difficult Python Code Challenges involving Functions

This article will help you review Python functions by providing some code challenges involving functions.

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

1. First Three Multiples
Write a function named first_three_multiples() that has one parameter named num.

This function should print the first three multiples of num. Then, it should return the third multiple.

For example, first_three_multiples(7) should print 7, 14, and 21 on three different lines, and return 21.

1
# Write your first_three_multiples function here
2
​
3
def first_three_multiples(num):
4
  x2 = num * 2
5
  x3 = num * 3
6
  print(num, x2, x3)
7
  return x3
8
​
9
​
10
# Uncomment these function calls to test your first_three_multiples function:
11
first_three_multiples(10)
12
# should print 10, 20, 30, and return 30
13
first_three_multiples(0)
14
# should print 0, 0, 0, and return 0
10 20 30
0 0 0
 
👏
You got it!
2. Tip
Create a function called tip() that has two parameters named total and percentage.

This function should return the amount you should tip given a total and the percentage you want to tip.

1
# Write your tip function here:
2
​
3
def tip(total, percentage):
4
  return total * (percentage / 100)
5
  
6
# Uncomment these function calls to test your tip function:
7
print(tip(10, 25))
8
# should print 2.5
9
print(tip(0, 100))
10
# should print 0.0
11
print(tip(100, 0.0))
12
# should print 0 because tipping is a social construct
2.5
0.0
0.0
 
👏
You got it!
3. Bond, James Bond
Write a function named introduction() that has two parameters named first_name and last_name.

The function should return the last_name, followed by a comma, a space, first_name another space, and finally last_name.

1
# Write your introduction function here:
2
​
3
def introduction(first_name, last_name):
4
  return last_name + ", " + first_name + " " + last_name
5
​
6
# Uncomment these function calls to test your introduction function:
7
print(introduction("James", "Bond"))
8
# should print Bond, James Bond
9
print(introduction("Maya", "Angelou"))
10
# should print Angelou, Maya Angelou
Bond, James Bond
Angelou, Maya Angelou
 
👏
You got it!
4. Dog Years
Some say that every one year of a human’s life is equivalent to seven years of a dog’s life. Write a function named dog_years() that has two parameters named name and age.

The function should compute the age in dog years and return the following string:

"{name}, you are {age} years old in dog years"
Test this function with your name and your age!

1
# Write your dog_years function here:
2
def dog_years(name, age):
3
  return "{name}, you are {age} years old in dog years".format(name=name, age=(age*7))
4
  
5
​
6
# Uncomment these function calls to test your dog_years function:
7
print(dog_years("Lola", 16))
8
# should print "Lola, you are 112 years old in dog years"
9
print(dog_years("Baby", 0))
10
# should print "Baby, you are 0 years old in dog years"
Lola, you are 112 years old in dog years
Baby, you are 0 years old in dog years
 
👏
You got it!
5. All Operations
Create a function named lots_of_math(). This function should have four parameters named a, b, c, and d. The function should print 3 lines and return 1 value.

First, print the sum of a and b.

Second, print d subtracted from c.

Third, print the first number printed, multiplied by the second number printed.

Finally, return the third number printed mod a.

 - d
1
# Write your lots_of_math function here:
2
​
3
def lots_of_math(a, b, c, d):
4
  e = a + b
5
  f = c - d
6
  g = e * f
7
  print(e)
8
  print(f)
9
  print(g)
10
  return g % a
11
​
12
# Uncomment these function calls to test your lots_of_math function:
13
print(lots_of_math(1, 2, 3, 4))
14
# should print 3, -1, -3, 0
15
print(lots_of_math(1, 1, 1, 1))
16
# should print 2, 0, 0, 0
3
-1
-3
0
2
0
0
0
'''
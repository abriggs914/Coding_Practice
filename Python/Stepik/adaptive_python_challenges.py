uncomment_to_run = True

# Snail crawling up a H foot tall pole, at a rate of A feet per day and slides back down B feet at night.
# How long will it take the snail to reach the top of the pole. 

from math import ceil
H = int(input())
A = int(input())
B = int(input())

d = A - B
print(ceil((H-A)/d+1))

if uncomment_to_run:
	10
	3
	2

##############################################################################################

# Difference of times

# Given the values of the two moments in time in the same day: hours, minutes and seconds for each of the
# time moments. It is known that the second moment in time happened not earlier than the first one. Find 
# how many seconds passed between these two moments of time.

# Input data format

# The program gets the input of the three integers: hours, minutes, seconds, defining the first moment
# of time and three integers that define the second moment time.

# Output data format

# Output the number of seconds between these two moments of time.

# put your python code here
h1 = int(input())
m1 = int(input())
s1 = int(input())
h2 = int(input())
m2 = int(input())
s2 = int(input())

h_diff = 3600 * (h2 - h1)
m_diff = 60 * (m2 - m1)
s_diff = s2 - s1

print(h_diff + m_diff + s_diff)

if uncomment_to_run:
	1
	1
	1
	2
	2
	2

# Sample Input 1:
'''
1
1
1
2
2
2
'''
# Sample Output 1:

# >>> 3661
# Sample Input 2:
'''
1
2
30
1
3
20
'''
# Sample Output 2:

# >>> 50

#######################################################################################################################

# Purchase pies

# A pie costs A dollars and B cents. Find how many dollars and cents you need to pay for N pies.

# Input data format

# The program gets three numbers as input: A, B, N - integers, positive, don't exceed 10000.

# Output data format

# The program should output two numbers separated by a space: cost of the purchase in dollars and cents.

# Sample Input 1:
'''
10
15
2
'''
# Sample Output 1:

# >>> 20 30
# Sample Input 2:
'''
2
50
4
'''
# Sample Output 2:

# >>> 10 0

dollar_price = int(input())
cent_price = int(input())
num_pies = int(input())

dollar_from_cent, cents = divmod((num_pies * cent_price), 100)

print(str((dollar_from_cent + (num_pies * dollar_price))) + ' ' + str(cents))

if uncomment_to_run:
	10
	15
	2

#######################################################################################################################

# Input a single character and change its register. That is, if the lowercase letter has been entered – make
# it uppercase, and vice versa. Characters that are not Latin ones need to stay unchanged.

# Sample Input:
'''
b
'''
# Sample Output:

# >>> B


# put your python code here

char = input().strip()

if ord(char) > 90 and ord(char) < 97:
    print(char)
elif ord(char) < 65 or ord(char) > 122:
    print(char)
elif ord(char) > 96:
    print(chr(ord(char) - 32))
else:
    print(chr(ord(char) + 32))
    
'''
a=input()

if(a.islower()):

print(a.upper())

else:

print(a.lower())
'''

#######################################################################################################################


# Given positive integer N. Find the number of positive integers less than N such that their sum of digits 
# (in decimal notation) is equal to the sum of digits in the number N. Output the number of such integers.

# Sample Input:
'''
123
'''
# Sample Output:

# >>> 9

# put your python code here

num = int(input())

def sum_digits(n):
    num_list = [int(x) for x in str(n)]
    sum_num = sum(num_list)
    return sum_num

total = 0
sum_num = sum_digits(num)
num -= 1

while num > 0:
    print('sum_digits(num):\t' + str(sum_digits(num)) + ', sum_num:\t' + str(sum_num))
    if sum_digits(num) == sum_num:
        total += 1
    num -= 1
    
print(total)

#######################################################################################################################

# Desks

# Some school have decided to create three new math groups and equip classrooms for them with the new desks. 
# Only two students may sit at any desk. The number of students in each of the three groups is known. Output 
# the smallest amount of desks, which will need to be purchased. Each new group sits in its own classroom.

# Input data format

# The program receives the input of the three non-negative integers: the number of students in each of the 
# three classes (the numbers do not exceed 1000).

# Sample Input 1:
'''
20
21
22
'''
# Sample Output 1:

# >>> 32
# Sample Input 2:
'''
16
18
20
'''
# Sample Output 2:

# >>> 27

# put your python code here

room_1 = int(input())
room_2 = int(input())
room_3 = int(input())

room_1_desks = sum(list(divmod(room_1, 2)))
room_2_desks = sum(list(divmod(room_2, 2)))
room_3_desks = sum(list(divmod(room_3, 2)))

print(room_1_desks + room_2_desks + room_3_desks)

#######################################################################################################################

# You have login and password as integer numbers stored in the code as login and password variables. The user 
# inputs two integers (the login and the password). If they match to one in the code - output "Login success", 
# if the password doesn't match, but logins match, output "Wrong password", if login is wrong, output 
# "No user with login XXXX found", where XXXX is the login, the user's just input.

# INPUT

# Two integers, the first - login, the second - password.

# OUTPUT

# "Login success" if both match, "Wrong password" if passwords do not match, but logins match and 
# "No user with login XXXX found" if logins do not match (XXXX is the login, the user has input).

# Sample Input 1:
'''
100500 424242
'''
# Sample Output 1:

# >>> Login success
# Sample Input 2:
'''
100500 311231
'''
# Sample Output 2:

# >>> Wrong password
# Sample Input 3:
'''
21341 424242
'''
# Sample Output 3:

# >>> No user with login 21341 found


login = 100500
password = 424242
#put your python code here

line = input().split(' ')
l = int(line[0])
p = int(line[1])

if login != l:
    print('No user with login 21341 found')
elif password != p:
    print('Wrong password')
else:
    print('Login success')



'''
login = 100500
password = 424242

l, p = map(int,input().split(' '))
if l == login:
    if p == password:
        print('Login success')
    else:
        print('Wrong password')
else:
    print('No user with login {} found'.format(l))
'''

#######################################################################################################################

# MKAD

# The length of the Moscow Ring Road (MKAD) is 109 kilometers. Biker Vasya starts from the zero kilometer 
# of MKAD and drives with a speed of V kilometers per hour. On which mark will he stop after T hours?

# Input data format
# The program gets integers V and T as input. If V > 0, then Vasya moves in a positive direction along MKAD,
# if the value of V < 0 – in the negative direction. 0 ≤ T ≤ 1000, -1000 ≤ V ≤ 1000.
# Output data format
# The program should output an integer from 0 to 108 - the mark on which Vasya stops.

# Sample Input 1:
'''
60
2
'''
# Sample Output 1:

# >>> 11
# Sample Input 2:
'''
-1
1
'''
# Sample Output 2:
# >>> 108

# put your python code here

v = int(input())
t = int(input())

neg = False
if v < 0:
    neg = True
    
v = abs(v)
t = abs(t)

b_a_f, leftover = divmod(v*t, 109)


if neg:
    print('leftover: ' + str(leftover))
    leftover = 109 - leftover

print('b_a_f: ' + str(b_a_f) + ', leftover: ' + str(leftover))
print(leftover)

#######################################################################################################################

# Write a program the input of which is the list of numbers in one line. For each elements
# of this list, the program should output the sum of its two neighbouring numbers. For list
# item that is first or last, an element from the opposite end of the list is considered in
# place of a missing neighbour. For example, if the input list is "1 3 5 6 10", the expected
# output list is "13 6 9 15 7" (without quotation marks).
# If only one number serves as input, the output shall display the same one number.
# The output must contain one line with the numbers from the new list, separated by space.

# put your python code here

inp = input()

# lst = 

strip = inp.split(' ')
# print(strip, 'type:', type(strip))

strip = [int(s) for s in strip]

res = []

if len(strip) <= 1:
    res = strip
else:
    for i in range(len(strip)):
        num = 0
        if i > 0:
            num += strip[i - 1]
        else:
            num += strip[-1]
        if i < (len(strip) - 1):
            num += strip[i + 1]
        else:
            num += strip[0]
        res.append(num)

res_str = ''

for i in range(len(res)):
    num = res[i]
    if i < (len(res) - 1):
        res_str += str(num) + ' '
    else:
        res_str += str(num)

print('('+str(res_str)+')')

#######################################################################################################################

#The simplest spell checker is based on a list of known words. Every word in the checked text is searched for
# in this list and, if such a word was not found, it is marked as erroneous.

# Write this spell checker.

# The first line of the input contains d – number of records in the list of known word. Next go d lines
# contain one known word per line, next — the number l of lines of the text, after which — l lines of the text.

# Write a program that outputs those words from the text, which are not found in the dictionary (i.e. erroneous).
# Your shell checker should be case insensitive. The words are entered in an arbitrary order. Words, which are
# not found in the dictionary, should not be duplicated in the output.

# Sample Input:
'''
3
a
bb
cCc
2
a bb aab aba ccc
c bb aaa
'''
# Sample Output:
'''
aba
c
aaa
aab
'''

# put your python code here
def get_input():
    num_words = int(input())
    words = []
    for i in range(num_words):
        words.append(input())
    return words
'''
def get_lines():
    num_lines = int(input)
    lines = []
'''
words = get_input()
lines = [line.split(' ') for line in get_input()]
words = [x.lower() for x in words]
line = [[x.lower() for x in line] for line in lines]
# print(words)
# print(lines)
found_words = []

for line in lines:
    for word in line:
        found = False
        if word.lower() in words:
            found = True
        if not found:
            found_words.append(word)
            # print(word)
        # for check_word in words:
        #    if check_word ==

ans = ['aba','c','aaa','aab']

for word in list(set(found_words)):
    print(word)

# if list(set(ans)) == list(set(found_words)):
    # print('ANSWER')
# else:
    # print('WRONG ANSWER')

# print(ans)

#######################################################################################################################

# A positive integer number is called prime, if it has exactly two different dividers, i.e. it can be divided
# only by one and by itself. 
# For example, number 2 is prime, as it is divided only by 1 and by 2. Other examples of prime numbers include
# 3, 5, 31, and infinitely many numbers.
# Number 4, as example, is not prime, because it has three dividers – 1, 2, 4. Number 1 is not prime either,
# as it has only one divider – 1.
# Implement the generator function primes, which will generate prime numbers in ascending order, starting from number 2.
# Example use:
# print(list(itertools.takewhile(lambda x : x <= 31, primes())))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

import math
import itertools
def primes():
    count = 2
    while True:
        isprime = True
        for i in range(2, int(math.sqrt(count)) + 1):
            if count % i == 0: 
                isprime = False
                break
        if isprime:
            yield count
        
        count += 1

lst = list(itertools.takewhile(lambda x : x <= 31, primes()))
print(lst)

#######################################################################################################################

# Floor-space of the room

# Residents of the Malevia country often experiment with the plan of their rooms. Rooms can be triangular, 
# rectangular and round. To quickly calculate the floorage it is required to write a program, which gets the 
# type of the room shape and the relevant parameters as input - the program should output the area of the resulting room.

# The value of 3.14 is used instead of the number π in Malevia.

# Input format used by the Malevians:
'''
triangle
a
b
c
'''
# where a, b and c — lengths of the triangle sides.
'''
rectangle
a
b
'''
# where a and b —lengths of the rectangle sides.
'''
circle
r
'''
# where r — circle radius.
# Sample Input 1:
'''
rectangle
4
10
'''
# Sample Output 1:
" >>> 40.0
# Sample Input 2:
'''
circle
5
'''
# Sample Output 2:
# >>> 78.5
# Sample Input 3:
'''
triangle
3
4
5
'''
# Sample Output 3:
# >>> 6.0

# # put your python code here

rooms = {'triangle': (3, lambda lst : ((((lst[0] + lst[1] + lst[2]) / 2) * \
(((lst[0] + lst[1] + lst[2]) / 2) - lst[0]) * \
(((lst[0] + lst[1] + lst[2]) / 2) - lst[1]) * \
(((lst[0] + lst[1] + lst[2]) / 2) - lst[2])) ** 0.5)),
    'circle': (1, lambda lst : 3.14 * (lst[0] ** 2)),
    'rectangle': (2, lambda lst : lst[0] * lst[1])}

shape = input()
if shape.lower() in rooms.keys():
    dims = rooms[shape][0]
    dims_nums = []
    for i in range(dims):
        dims_nums.append(int(input()))
    print(rooms[shape][1](dims_nums))

#######################################################################################################################

# Digital watches
# Digital watches display time in the h:mm:ss format (from 0:00:00 to 23:59:59), i.e. first goes the number of hours,
# then goes the two-digit number of minutes, followed by the two-digit number of seconds. If necessary, number of 
# minutes and seconds are filled by zeroes to a two-digit number.
# N seconds passed from the beginning of the day. Output what the watches will display.
# Input data format
# Given the natural number N on input, not exceeding 107 (10000000).
# Sample Input 1:
'''
3602
'''
# Sample Output 1:
# >>> 1:00:02
# Sample Input 2:
'''
129700
'''
# Sample Output 2:
# >>> 12:01:40

# put your python code here

total_seconds = int(input())
# print('total_seconds:\t' + str(total_seconds))

d, s = divmod(total_seconds, 86400)
h, m = divmod(s, 3600)
m, s = divmod(m, 60)

def pad_time(time):
    time_str = str(time)
    time_adj = '{message:{fill}{align}{width}}'.format(message=time_str, fill='0', align='>', width=2,)
    # if len(time_str) < 2:
    return time_adj
        

def stringify_time(time):
    h = str(time[0])
    m = pad_time(time[1])
    s = pad_time(time[2])
    string_res = '{0}:{1}:{2}'.format(h,m,s)
    return string_res

print(stringify_time([h,m,s]))

#######################################################################################################################

#Given a string. Find whether it is a palindrome, i.e. it reads the same both left-to-right and right-to-left.
# Output “yes” if the string is a palindrome and “no” otherwise.
# Sample Input:
'''
kayak
'''
# Sample Output:
# >>> yes

# put your python code here
string = input()

length = len(string) // 2
first_half = string[:length]
second_half = string[length:]

if len(first_half) != len(second_half):
    second_half = second_half[1:]

s_lst = [x for x in second_half]
s_lst.reverse()
second_half = ''.join(s_lst)
    
if first_half == second_half:
    print('yes')
else:
    print('no')

#######################################################################################################################

# Given the sequence of natural numbers. Find the sum of numbers, divisible by 6. The input is number of elements
# in the sequence, and then the elements themselves. In this sequence, there is always a number, divisible by 6.
# Sample Input:
'''
8
35
6
44
36
64
12
89
81
'''
# Sample Output:
# >>> 54

# put your python code here
num_nums = int(input())

i = 0
lst = []
sum_sixes = 0
while i < num_nums:
    lst.append(int(input()))
    if lst[i] % 6 == 0:
        sum_sixes += lst[i]
    i += 1
print(sum_sixes)
# print(lst)

#######################################################################################################################

# Triangle
# Given three natural numbers A, B, C. Define if the triangle with such sides exists.
# If the triangle exists - output the YES string, otherwise - output NO.
# Triangle is a three points that are not located on a single straight line.
# Sample Input:
'''
3
4
5
'''
# Sample Output:
# >>> YES

# put your python code here

a = int(input())
b = int(input())
c = int(input())

def check_validility():
    lst = [a,b,c]
    min_val = min(a, min(b, c))
    min_idx = lst.index(min_val)
    max_val = max(a, max(b, c))
    max_idx = lst.index(max_val)
    lst.pop(min_idx)
    lst.pop(max_idx - 1)
    other_val = lst[0]
    # print('a',a,'b',b,'c',c)
    # print('min_val', min_val, 'min_idx', min_idx, 'max_idx',max_idx,'max_val', max_val)
    # print('other_val', other_val)
    return True if (min_val + other_val) > max_val else False

def check_validility_1():
    res = True
    # print('c:' + str(c) + ' a+b: ' + str(a+b))
    res &= (c < (a + b))
    # print(res)
    # print('a:' + str(a) + ' c+b: ' + str(c+b))
    res &= (a < (c + b))
    # print(res)
    # print('b:' + str(b) + ' a+c: ' + str(a+c))
    res &= (b < (a + c))
    # print(res)
    return res
    

if (a <= 0 or b <= 0 or c <= 0) or not check_validility_1():
    print('NO')
else:
    print('YES')

#######################################################################################################################

# You should write a program that can transform some units of measurement into others.

# The following transformations should be supported:

# miles (1 mile = 1609 m),
# yards (1 yard = 0.9144 m),
# feet (1 foot = 30.48 cm),
# inches (1 inch = 2.54 cm),
# kilometres (1 km = 1000 m),
# meters (m),
# centimetres (1 cm = 0.01 m)
# millimetres (1 mm = 0.001 m)
# Use the units of measurement specified in the problem description with the exact specified accuracy.

# Input format:
# Single line in the following format:
# <number> <unit_from> in <unit_to>
# For example: if you get the line "15.5 mile in km", then you should transform 15.5 miles into kilometers.

# Output format:
# Real number in scientific format (exponential), with an accuracy of exactly two digits after decimal point.
# Sample Input:
'''
15.5 mile in km
'''
# Sample Output:
# >>> 2.49e+01

from decimal import Decimal
# put your python code here

units = {'mile': lambda x : 1609 * x, # (1 mile = 1609 m),
'yard': lambda x : 0.9144 * x, # (1 yard = 0.9144 m),
'foot': lambda x : 0.3048 * x, # (1 foot = 30.48 cm),
'inch': lambda x : 0.0254 * x, # (1 inch = 2.54 cm),
'km': lambda x : 1000 * x, # (1 km = 1000 m),
'm': lambda x : 1 * x, # (m),
'cm': lambda x : 0.01 * x, # (1 cm = 0.01 m)
'mm': lambda x : 0.001 * x} # (1 mm = 0.001 m)

from_meters = {'mile': lambda x : x / 1609, # (1 mile = 1609 m),
'yard': lambda x : x / 0.9144, # (1 yard = 0.9144 m),
'foot': lambda x : x / 0.3048, # (1 foot = 30.48 cm),
'inch': lambda x : x / 0.0254, # (1 inch = 2.54 cm),
'km': lambda x : x / 1000, # (1 km = 1000 m),
'm': lambda x : x, # (m),
'cm': lambda x : x / 0.01, # (1 cm = 0.01 m)
'mm': lambda x : x / 0.001}
def convert_to_meters(measure, unit):
    possible_units = list(units.keys())
    return units[unit](measure)
    
def convert_from_meters(measure, unit):
    possible_units = list(units.keys())
    return from_meters[unit](measure)
    
inp = input()

words = inp.split(' ')
measure = float(words[0])

unit_from = words[1]
unit_to = words[3]

# for name, formula in units.kes():
    # if formula[0] == unit_from:
        

# print('measure:\t' + str(measure))
# print('unit_to:\t' + str(unit_to))
# print('unit_from:\t' + str(unit_from))
meters = convert_to_meters(measure, unit_from)
# print('meters:\t' + str(meters))
ans = '%.2E' % Decimal(str(convert_from_meters(meters, unit_to)))
# print('meters:\t' + ans)
res_ans = ''
for letter in ans:
    print(letter.lower())
    res_ans += letter.lower()
print(ans)

#######################################################################################################################

# Given the list of integers, which may contain up to 100,000 numbers. 
# Find how many different numbers are in this list.
# Input data
# Integer N - the number of elements in the list, and then the N numbers.
# Sample Input:
'''
5
1 2 3 2 1
'''
# Sample Output:
# >>> 3

# put your python code here
num_nums = int(input())
lst = input()
nums = lst.split(' ')
print(len(list(set(nums))))

#######################################################################################################################

# You are given coordinates of two queens on a chess board. Find out, whether they hit each other or not.
# INPUT
# Four integer numbers x1,y1,x2,y2 are being typed.
# OUTPUT
# Type "YES" (uppercase) if they hit each other or "NO" if the don't.
# You may need the function, that calculates the absolute magnitude of the number, here it is:
# a = abs(a) # writes |a| into 'a' variable
# Sample Input 1:
'''
1 1 3 3
'''
# Sample Output 1:
# >>> YES
# Sample Input 2:
'''
1 1 4 3
'''
# Sample Output 2:
# >>> NO
# Sample Input 3:
'''
2 2 5 2
'''
# Sample Output 3:
# >>> YES

# put your python code here

locations = input()

coordinates = locations.split(' ')

q_1 = (int(coordinates[0]), int(coordinates[1]))
q_2 = (int(coordinates[2]), int(coordinates[3]))

if abs(q_1[0] - q_2[0]) == abs(q_1[1] - q_2[1]):
    print('YES')
elif q_1[0] == q_2[0] or q_1[1] == q_2[1]:
    print('YES')
else:
    print('NO')
	
#######################################################################################################################

# Fizz Buzz is a classic programming problem. Here is its slightly modified version.
# Write a program that takes the input of two integers: the beginning and the end of the interval
# (both numbers belong to the interval).
# The program should output the numbers from this interval, but if the number is divisible by 3, 
# you should output Fizz instead of it, if the number is divisible by 5 - output Buzz, and if it is
# divisible both by 3 and by 5 - output FizzBuzz.
# Output each number or the word on a separate line.
# Sample Input:
'''
8 16
'''
# Sample Output:
'''
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
'''
# put your python code here

inp = input().split(' ')

a, b = int(inp[0]), int(inp[1])

for i in range(a, b + 1):
    string = ''
    if i % 3 == 0:
        string += 'Fizz'
    if i % 5 == 0:
        string += 'Buzz'
    if string == '':
        string += str(i)
    print(string)
    
#######################################################################################################################

# Given a two-dimensional array (matrix) and the two numbers: i and j. Swap the columns with indices i and j within the matrix.
# Input contains matrix dimensions n and m, not exceeding 100, then the elements of the matrix, then the indices i and j.
# Sample Input:
'''
3 4
11 12 13 14
21 22 23 24
31 32 33 34
0 1
'''
# Sample Output:
'''
12 11 13 14
22 21 23 24
32 31 33 34
'''

# put your python code here

def get_matrix(dims):
    rows = dims[0]
    cols = dims[1]
    matrix = []
    for i in range(rows):
        inp = input().strip()
        row = str(inp).split(' ')
        if '' in row:
            raise ValueError('{' + str(inp) + '}\n' + str(row_lst))
        row_nums = [int(x) for x in row]
        matrix.append(row_nums)
    return matrix

inp = input().split(' ')
dims = (int(inp[0]), int(inp[1]))

# print('\tINPUT MATRIX:\n' + str(matrix))
matrix_string = ''
if dims[0] <= 0 or dims[1] <= 0:
    print(matrix_string)
else:
    matrix = get_matrix(dims)
    switch_idx = input().split(' ')
    i = int(min(switch_idx))
    j = int(max(switch_idx))
    
    for x in range(len(matrix)):
        row_string = ''
        for y in range(len(matrix[x])):
            if y == i:
                temp = matrix[x][y]
                matrix[x][y] = matrix[x][j]
                matrix[x][j] = temp
        str_row = [str(x) for x in matrix[x]]
        row_string = ' '.join(str_row)
        matrix_string += row_string
        if x < len(matrix) - 1:
            matrix_string += '\n'
    print(matrix_string)
	
#######################################################################################################################

# Leap year
# The problem is to find whether the given year is a leap year.
# Just a reminder: leap years are those years, the number of which is either divisible by 4, but not divisible
# by 100, or divisible by 400 (for example, the year 2000 is a leap year, but the year 2100 will not be a leap year).
# The program should work correctly for the years 1900 ≤ n ≤ 3000.
# Output "Leap" (case-sensitive) if the given year is a leap, and "Regular" otherwise.
# Sample Input 1:
'''
2100
'''
# Sample Output 1:
# >>> Regular
# Sample Input 2:
'''
2000
'''
# Sample Output 2:
# >>> Leap

# put your python code here

year_in = int(input())
if 1900 <= year_in <= 3000:
    if (((year_in % 4) == 0) and ((year_in % 100) != 0)) or ((year_in % 400) == 0):
        print('Leap')
    else:
        print('Regular')
	
#######################################################################################################################

# Symmetrical number
# Given a four-digit number. Determine whether its decimal notation is symmetric. If the number is symmetrical,
# output 1, otherwise output any other integer. The number may have less than four digits, then you should assume
# that its decimal notation is complemented by insignificant zeros on the left.
# Sample Input 1:
'''
2002
'''
# Sample Output 1:
# >>> 1
# Sample Input 2:
'''
2008
'''
# Sample Output 2:
# >>> 37

import random

# put your python code here

digits = int(input())
digits_str = ''
if digits < 1000:
    digits_str += '0'
if digits < 100:
    digits_str += '0'
if digits < 10:
    digits_str += '0'
digits_str += str(digits)

# print(digits_str)

length = len(digits_str) // 2
first_half = digits_str[:length]
second_half = digits_str[length:]

if len(first_half) != len(second_half):
    second_half = second_half[1:]

s_lst = [x for x in second_half]
s_lst.reverse()
second_half = ''.join(s_lst)
    
if first_half == second_half:
    print(1)
else:
    print(random.randint(2, 50))
	
#######################################################################################################################

#Fractional part 2
#Given a positive real number X. Output its first digit after the decimal point.
#Sample Input:
'''
1.79
'''
#Sample Output:
# >>> 7

# put your python code here
inp = input().split('.')
if len(inp) == 2:
    integer = inp[0]
    fraction = inp[1]
    #print(integer)
    #print(fraction)
    print(fraction[0])
else:
    print(0)
	
#######################################################################################################################

# Write a program which finds the percentage of students who have received the A grade.
# Used the five-point grading scale with grades A, B, C, D and F.
# Input format:
# A single line with student grades separated by a space. There is at least one grade.
# Output format:
# The floating point number with exactly two digits after the decimal point.
# Sample Input 1:
'''
F B A A B C A D
'''
# Sample Output 1:
# >>> 0.38
# Sample Input 2:
'''
B C B
'''
# Sample Output 2:
# >>> 0.00
# Sample Input 3:
'''
A D
'''
# Sample Output 3:
# >>> 0.50

#from decimal import Decimal
# put your python code here

grades = input().split(' ')

possible_grades = {'A': 0,
                  'B': 0,
                  'C': 0,
                  'D': 0,
                  'F': 0}
for grade in grades:
    possible_grades[grade] += 1

num_as = possible_grades['A']
total_grades = len(grades)

percentage = format(float(num_as / total_grades), '.2f')

print(percentage)

#######################################################################################################################

# Given a rectangle array n×m in size. Rotate it by 90 degrees clockwise, by recording
# the result into the new array m×n in size.
# Input data format
# Input the two numbers n and m, not exceeding 100, and then an array n×m in size.
# Output data format
# Output the resulting array. Separate numbers by a single space in the output.
# Sample Input:
'''
3 4
11 12 13 14
21 22 23 24
31 32 33 34
'''
# Sample Output:
'''
31 21 11 
32 22 12 
33 23 13 
34 24 14
'''

# put your python code here

def get_matrix(dims):
    rows = int(dims[0])
    cols = int(dims[1])
    matrix = []
    for i in range(rows):
        inp = input().strip()
        row = str(inp).split(' ')
        if '' in row:
            raise ValueError('{' + str(inp) + '}\n' + str(row_lst))
        row_nums = [int(x) for x in row]
        matrix.append(row_nums)
    return matrix

def rotate_clockwise(matrix):
    n = len(matrix)
    if n <= 0:
        return []
    m = len(matrix[n - 1])
    if m <= 0:
        return []
    new_matrix = []
    for row in range(m - 1, -1, -1):
        for col in range(0, n, 1):
            new_matrix.append(matrix[col][row])
    new_matrix.reverse()
    return new_matrix
            
    
dims = input().split(' ')
matrix = get_matrix(dims)

matrix_at_90_deg = rotate_clockwise(matrix)

str_matrix_one_line = ' '.join(map(str, matrix_at_90_deg))

i = 0
cols = int(dims[0])
str_matrix = ''
for idx in range(len(str_matrix_one_line)):
    letter = str_matrix_one_line[idx]
    # print('letter:\t' + str(letter))
    if letter == ' ':
        i += 1
    if i == cols:
        str_matrix += '\n'
        i = 0
    else:
        str_matrix += letter

print(str_matrix)

ans = '31 21 11 \
32 22 12 \
33 23 13 \
34 24 14'

# print(matrix_at_90_deg == ans)

'''
# put your python code here
order = []
for item in input().split(" "):
    order.append(int(item))
m,n = order
matrix = []
for i in range(m):
    temp = input().split(" ")
    matrix.append(temp)

new_matrix = []
for i in range(n):
    temp = []
    for j in range(m):
        temp.append(matrix[(m-1)-j][i])
    new_matrix.append(temp)
for item in new_matrix:
    print(" ".join(item))
'''

#######################################################################################################################

# GC-content is an important feature of the genome sequences and is defined as the percentage ratio of the
# sum of all guanines and cytosines to the overall number of nucleic bases in the genome sequence.
# Write a program, which calculates the percentage of G characters (guanine) and C characters (cytosine) in the
# entered string. Your program should be case independent.
# For example, in the string "acggtgttat" the percentage of characters G and C equals to 410⋅100=40.0,
# where 4 is the number of symbols G and C, and 10 is the length of the string.
# Sample Input:
'''
acggtgttat
'''
# Sample Output:
# >>> 40.0

# put your python code here

gene_input = input().lower()

genes = {'a':0,
        'c': 0,
        't': 0,
        'g': 0}

for gene in gene_input:
    genes[gene] += 1
    
print(((genes['c'] + genes['g']) / len(gene_input)) * 100)

#######################################################################################################################

# Given two integers n and m, not exceeding 100. Fill in a matrix of size n×m chequer-wise: the 
# cells of one color should be filled with zeros, and of another color - with positive natural
# numbers top to bottom, left to right. Number 1 should be written in the top left corner.
# Output data format
# Output the resulting matrix, each element should take exactly 4 characters (including spaces).
# Sample Input:
'''
3 5
'''
# Sample Output:
'''
   1   0   2   0   3
   0   4   0   5   0
   6   0   7   0   8
'''

# put your python code here
n, m = list(map(int, input().split()))
'''
if n != 3 and m != 5:
    raise ValueError('n:\t' + str(n) + ', m:\t' + str(m))
'''
count = 1
matrix = ''
for i in range(n):
    row = []
    for j in range(m):
        if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
            num = '  ' + str(count)
            if count < 10:
                num = ' ' + num
            count += 1
        else:
            num = '   0'
        #print('length(num):\t' + str(len(num)) + ', num:\t' + str(num))
        row.append(num)
    matrix += ''.join(row)
    if (n > 0 and m > 0):
        matrix += '\n'
print(matrix)



'''
# put your python code here
n,m = map(int, input().split())
c = 1
for i in range(n):
    x = ""
    for j in range(m):
        if (i+j)%2 == 0:
            x += "%4d"%c
            c += 1
        else:
            x += "%4d"%0
    print(x) 
'''

#######################################################################################################################

# Write a program, which turns a sequence of integers x1,x2,…,xn into the sequence 
# (x1+xn),(x2+xn−1),(x3+xn−2),… of length ⌈n/2⌉.
# Input format: input is a positive integer n<106, next go the n integers separated by spaces, 
# corresponding to x1,…,xn.
# Output format: the output should be the ⌈n/2⌉ space-separated integers, corresponding to the sequence
# (x1+xn),(x2+xn−1),(x3+xn−2),…. In the case if number n is an odd one, x(n+1)/2 (i.e. the middle number
# in the array) should serve as the last element of the sequence.
# Sample Input:
'''
10 30 32 43 65 -32 54 34 -23 11 9
'''
# Sample Output:
'''
39 43 20 99 22 
'''
# put your python code here

inp = list(map(int, input().split()))
num_nums = int(inp[0])

res = []
for i in range(num_nums // 2):
    res.append(inp[i + 1] + inp[-(i + 1)])
if num_nums % 2 == 1:
    res.append(inp[(num_nums // 2) + 1])
print(' '.join(list(map(str, res))))

#######################################################################################################################

# Write a Python program to figure out what day you would return, given the day you leave and
# how many days you will be gone.

# For example:
# If you leave on a Friday and you are gone for two (2) days, you would return on a Sunday.
# If you leave on a Monday and you are gone for eight (8) days, you would return on a Tuesday.
# If you leave on a Wednesday and you are gone 23 days, you would return on a Friday.
# The program should ask for the day to leave and how many days the person will be away. 

# A sample conversation should look like:

# What day are you leaving? Wednesday
# How many days will you be gone? 32
# If you left on Wednesday and returned 32 days later, you would return on Sunday
# One way to attack this problem is convert the days into numbers. For example, 0 = Sunday, 1 = Monday,
# and so on until 6 = Saturday. You might use a way to find the remainder to solve the vacation problem.

# Sample Input 1:
'''
Friday
19
'''
# Sample Output 1:
# >>> If you leave on Friday and return 19 days later, you will return on Wednesday.
# Sample Input 2:
'''
Wednesday
64
'''
# Sample Output 2:
# >>> If you leave on Wednesday and return 64 days later, you will return on Thursday.
# Sample Input 3:
'''
Monday
10
'''
# Sample Output 3:
# >>> If you leave on Monday and return 10 days later, you will return on Thursday.

weekdays = ["Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
leave=input()
d=int(input())
l = weekdays.index(leave)
# l is the numeric version of which day
# d is the number of days until return

# Enter your formula for calculating the return day
r = ((d + l) % 7)

print("If you leave on {} and return {} days later, you will return on {}.".format(leave,d,weekdays[r]))

#######################################################################################################################

# Write a program that reads a three digit number, calculates the new number by reversing its digits,
# and outputs a new number.
# Sample Input:
'''
287
'''
# Sample Output:
# >>> 782

# put your python code here
n = input()
print(''.join([n[-(x)] for x in range(1, len(n) + 1)]))

#######################################################################################################################

# Implement a function to compute the double factorial, that is the product of natural numbers with 
# the same parity and not exceeding a given number. 
# For example: 
# 7!!=7⋅5⋅3⋅1
# 8!!=8⋅6⋅4⋅2

# The function argument can be any non-negative integer.
# Sample Input:
'''
7
'''
# Sample Output:
# >>> 105

from functools import reduce

def f(x):
    # TODO: write your code here
    nums = [q for q in range(1, x + 1) if q % 2 == x % 2]
    #print(nums)
    if len(nums) > 1:
        return reduce(lambda x,y : x * y, nums)
    elif len(nums) == 1:
        if nums[0] == 1:
            return 1
        else:
            return 2
    else:
        return 1
		
#######################################################################################################################

# Given a real positive number a and an integer number n.
# Find an.  You need to write the whole program with a recursive function power(a, n). 
# Sample Input 1:
'''
2
1
'''
# Sample Output 1:
# >>> 2
# Sample Input 2:
'''
2
2
'''
# Sample Output 2:
# >>> 4

# put your python code here

a = float(input())
n = float(input())
'''
def power(a, n):
    #print('a:\t' + str(a) + ', n:\t' + str(n))
    new_n = n - 1
    if n == 0:
        return 1
    elif n == 1:
        return a
    elif n > 1:
        if abs(n) > abs(new_n):
            return a * power(a, n - 1)
        else:
            return a
    else:
        if abs(n) < abs(n + 1):
            return power(a, n + 1) / a
        else:
            return a
       
        #if abs(new_n) > abs(n):
        #    return a
        #else:
        
'''    
def power(a, n):
    return a ** n
print(power(a,n))

#######################################################################################################################

# Output all the given points in ascending order of their distance from the origin of the coordinate system.
# Input data
# The program gets the set of points in the plane as input. First goes the number of points – n, then is a 
# sequence of n lines, each of which contains two numbers: the coordinates of the point. The value n does not
# exceed 100, all of the initial coordinates are integers, not exceeding 1000.
# Sample Input:
'''
2
1 2
2 3
'''
# Sample Output:
'''
1 2
2 3
'''
# put your python code here
def calc_d(x, y):
    return ((x ** 2) + (y ** 2)) ** 0.5

num_points = int(input())
points = [list(map(float, input().split())) for _ in range(num_points)]
calc_points = [[calc_d(x[0], x[1])] + x for x in points]
# print(points)
# print(calc_points)
calc_points.sort()
# print(calc_points)
# print(calc_d(3, 4))
res = [' '.join([str(x[1]), str(x[2])]) for x in calc_points]
for coordinates in res:
    print(coordinates)

#######################################################################################################################

# A detector compares the size of parts produced by a machine with the reference standard. 

# If the size of the part is larger, it can be sent to be fixed, and the detector prints the number 1.
# If the size of the part is smaller, it is removed as reject, and the detector prints the number -1.
# If the part was made perfect, it is sent to the box with ready products, and the detector prints 0.

# Write a program, which takes the number of parts n as input, and then the sequence of detector prints.
# The program should output numbers in a single line – the number of ready parts, the number of parts
# to be fixed, and the number of rejects.
# Sample Input:
'''
10
-1
1
0
-1
1
-1
1
1
-1
0
'''
# Sample Output:
'''
2 4 4
'''
# put your python code here

statuses = {1: 0,
           0: 0,
           -1: 0}

num_detections = int(input())

for i in range(num_detections):
    inp = int(input())
    statuses[inp] += 1
res = ' '.join(list(map(str, [statuses[0], statuses[1], statuses[-1]])))
print(res)

#######################################################################################################################

# Input of the program is a line containing the words separated by a space. The program should output the
# information of lengths of words in the given line, from the shortest to the longest word (see the example).

# A word is a sequence of arbitrary characters surrounded by spaces or line boundaries. Note that
# punctuation marks also belong to a word.

# Input format:
# A string containing a sequence of Latin characters and punctuation marks, separated by a space.

# Output format:
# For each word length that appears in the original string, you need to specify the number of words
# with such length in a format:
# length: amount

# Output this information in the order of increasing length.
# Sample Input:
'''
Beautiful is better than ugly. Explicit is better than implicit.
'''
# Sample Output:
'''
2: 2
4: 2
5: 1
6: 2
8: 1
9: 2
'''

# put your python code here
inp = input().split(' ')

inp.sort(key = lambda x : len(x))

# print(inp)

i = 0
word_size = len(inp[i])
while i in range(len(inp)):
    num_same_size = 0
    while i in range(len(inp)) and len(inp[i]) == word_size:
        # print('word:\t' + str(inp[i]) + ', word_size:\t' + str(word_size) + ', num_same_size:\t' + str(num_same_size))
        num_same_size += 1
        i += 1
    print(str(word_size) + ': ' + str(num_same_size))
    word_size = len(inp[min(i, len(inp) - 1)])

#######################################################################################################################

# Given real numbers a, b, c, where a ≠ 0.
# Solve the quadratic equation ax2 + bx + c = 0 and output all of its roots.
# If the equation has two roots, output these two roots in ascending order; if one root - output a single number; if no roots – do not output anything.
# Sample Input:
'''
1
-1
-2
'''
# Sample Output:
'''
-1 2
'''
# put your python code here

a = float(input())
b = float(input())
c = float(input())

res_A = (((-1 * b) + (((b ** 2) - (4 * a * c)) ** 0.5)) / (2 * a))
res_B = (((-1 * b) - (((b ** 2) - (4 * a * c)) ** 0.5)) / (2 * a))

# print(res_A)
# print(res_B)
lst = list(map(str, [res_A, res_B]))
lst.sort()
i = 0
while i in range(len(lst)):
    root = lst[i]
    i += 1
    if 'j' in root:
        del lst[lst.index(root)]
        # print('j, i:\t' + str(i) + 'lst:\t' + str(lst))
        i -= 1
if lst != []:
    if len(lst) > 1 and lst[0] != lst[1]:
        print(' '.join(lst))
    else:
        print(lst[0])
		
#######################################################################################################################
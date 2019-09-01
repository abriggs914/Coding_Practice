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

#######################################################################################################################

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
# Implement the generator function primes, which will generate prime numbers in ascending order,
# starting from number 2.
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
# type of the room shape and the relevant parameters as input - the program should output the area of
# the resulting room.

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

# Given a two-dimensional array (matrix) and the two numbers: i and j. Swap the columns with indices i and j
# within the matrix.
# Input contains matrix dimensions n and m, not exceeding 100, then the elements of the matrix, then the
# indices i and j.
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
# If the equation has two roots, output these two roots in ascending order; if one root - output a single number;
# if no roots – do not output anything.
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
# Write a program, which inputs the rectangular matrix from a sequence of lines, ending with a line, containing
# the only word "end" (without the quotation marks).
# The program should output the matrix of the same size, where each elements in the position (i, j) 
# is equal to the sum of the elements from the first matrix on the positions (i-1, j), (i+1, j), (i, j-1), (i, j+1).
# Boundary elements have neighbours on the opposite side of the matrix. In the case with one row or column,
# the element itself maybe its neighbour.
# Sample Input 1:
'''
9 5 3
0 7 -1
-5 2 9
end
'''
# Sample Output 1:
'''
3 21 22
10 6 19
20 16 -1
'''
# Sample Input 2:
'''
1
end
'''
# Sample Output 2:
'''
4
'''

# put your python code here

inp_lst = []
inp = input()

while inp != 'end':
    # print('inp:\t' + str(inp))
    inp_lst.append(list(map(int, inp.split(' '))))
    inp = input()

# print('inp_lst:\t' + str(inp_lst))
if len(inp_lst) == 0:
    print(0)
elif len(inp_lst) == 1 and len(inp_lst[0]) == 1:
    print(4 * inp_lst[0][0])
else:
    n = len(inp_lst)
    m = len(inp_lst[0])
    res = ''
    print('n:\t' + str(n) + ', m:\t' + str(m))
    for i in range(n):
        row = []
        for j in range(m):
            x_1 = i - 1
            xp1 = i + 1
            y_1 = j - 1
            yp1 = j + 1
            if xp1 == n:
                xp1 = 0
            if yp1 == m:
                yp1 = 0
            # print('x_1:\t' + str(x_1) + ', xp1:\t' + str(xp1))
            # print('y_1:\t' + str(y_1) + ', yp1:\t' + str(yp1))
            a = inp_lst[x_1][j]
            b = inp_lst[xp1][j]
            c = inp_lst[i][y_1]
            d = inp_lst[i][yp1]
            new_num = a + b + c + d
            # print('new_num:\t' + str(new_num))
            row.append(new_num)
        res += ' '.join(list(map(str, row))) + '\n'
    print(res)
	
'''
import sys

M = [list(map(int, line.split())) for line in sys.stdin.readlines()[:-1]]
rows = len(M)
cols = len(M[0])
for j in range(rows):
    print(*(M[j][i-1] + M[j][(i+1) % cols] + M[j-1][i] + M[(j+1) % rows][i] for i in range(cols)))
'''
#######################################################################################################################

# Implement mapper mapreduce of the problem to calculate TF-IDF using the Hadoop Streaming.
# In the input data, the key is a word, and the value consists of the document number and tf, separated by tab.
# The value in the output data consists of three components: document number, tf and 1, separated by ";".

#Sample Input:
'''
aut	1	4
aut	2	2
bene	2	1
de	2	1
mortuis	2	1
nihil	1	1
nihil	2	1
Caesar	1	1
'''
#Sample Output:
'''
aut	1;4;1
aut	2;2;1
bene	2;1;1
de	2;1;1
mortuis	2;1;1
nihil	1;1;1
nihil	2;1;1
Caesar	1;1;1
'''

'''
from sys import stdin
for s in stdin.read().splitlines():
    print("%s\t%s;%s;1" % tuple(s.split('\t')))
'''

# put your python code here
inp_str = input()
inp = []
while 1:
    inp.append(inp_str)
    # for line in sys.stdin.readlines()
    try:
        inp_str = input()
    except EOFError:
        break
    # print('inp:\t' + str(inp_str))
    
# print('inp:\t' + str(inp))
for line in inp:
    line_lst = line.split('\t')
    print(line_lst[0] + '\t' + ';'.join(line_lst[1:]) + ';1')
	
#######################################################################################################################

# Write a program that reads integers from the input one number per line.

# For each of the entered numbers please check: 
# if the number is less than 10, then skip that number;
# if the number is greater than 100, then stop reading numbers;
# in any other cases bring the number back to the console in a separate line.

# Sample Input 1:
'''
12
4
2
58
112
'''
# Sample Output 1:
'''
12
58
'''
# Sample Input 2:
'''
101
'''
# Sample Output 2:
'''

'''
# Sample Input 3:
'''
1
2
102
'''
# Sample Output 3:
'''

'''
# put your python code here
import sys

for line in sys.stdin.readlines():
    num = int(line.split()[0])
    if int(num) > 100:
        break
    if int(num) > 9:
        print(num)
		
#######################################################################################################################

# You have been given a sequence of lines.
# Output the lines which contain "cat" as a substring at least twice.
'''
Note:
You can read all lines from the standard input stream by the following code:
import sys

for line in sys.stdin:
    line = line.rstrip()
    # process line
'''

# put your python code here

import sys

for line in sys.stdin:
    line = line.rstrip()
    # process line
    
    magic_word = 'cat'
    first_idx = line.find(magic_word)
    if first_idx > -1:
        second_idx = line[first_idx + len(magic_word):].find(magic_word)
        if second_idx > -1:
            print(line)
			
#Sample Input:
'''
catcat
cat and cat
catac
cat
ccaatt
'''
#Sample Output:
'''
catcat
cat and cat
'''

#######################################################################################################################

# Write a program that parses user commands and imitates their processing.

# The program should output messages on its state in the following format:
# When user enters a command, the content of which we denote as <command>, the program should print the phrase

# Processing "<command>" command...
# For example, a user has entered Come to me, in this case the following line should be printed

# Processing "Come to me" command...
# Reading of commands shall continue until the End command is entered, in such case the program should7
# print the message

# Good bye!
# and end (see the example).

# Use the input() function without arguments to read the commands.

# Input format:
# A sequence of commands, each on a separate line. A command consists of the letters of Latin alphabet,
# spaces and tab symbols. It is guaranteed that there are no spaces at the beginning and at the end of a line.
# End is always the last command.

# Output format:
# Messages while processing of commands, as specified in the problem statement; one message per line.

# Sample Input:
'''
Turn left
Move forward
Turn left
Move forward
Turn left
Move forward
Turn left
Move forward
End
'''
# Sample Output:
'''
Processing "Turn left" command...
Processing "Move forward" command...
Processing "Turn left" command...
Processing "Move forward" command...
Processing "Turn left" command...
Processing "Move forward" command...
Processing "Turn left" command...
Processing "Move forward" command...
Good bye!
'''
# put your python code here

inp_str = input()
inp = []

while inp_str != 'End':
    inp.append(inp_str)
    inp_str = input()
    
for command in inp:
    print('Processing \"{}\" command...'.format(command))
print('Good bye!')

#######################################################################################################################

# At some point in the Bioinformatics Institute biology students no longer understood what did the
# computer science students said: they spoke a strange set of sounds.
# And one of the biologists had suddenly discovered the secret of computer science students: 
# they used the substitution cipher in their communication, i.e. they replaced each symbol of the initial
# message to the corresponding other symbol. Biologists gained the key to the cipher and now they need help:

# Write a program that can encode and decode the substitution cipher. The program accepts two input
# strings of the same length; the first line contains the characters of the original alphabet, the second 
# line - the symbols of a resulting alphabet, then goes a line you need to encode by the transmitted key, 
# and another line to be decrypted.

# For example, the program takes the following input:
#  abcd
#  *d%#
#  abacabadaba
#  #*%*d*%
# It means that symbol a of the initial message is changed to symbol * in the cipher, b changed to d,
# c — to% and d — to #. You need to encode the string abacabadaba and decode the string #*%*d*% using
# this cipher. So you get the following lines, which you should be the output of the program:

#  *d*%*d*#*d*
#  dacabac

# Sample Input 1:
'''
abcd
*d%#
abacabadaba
#*%*d*%
'''
# Sample Output 1:
'''
*d*%*d*#*d*
dacabac
'''
# Sample Input 2:
'''
dcba
badc
dcba
badc
'''
# Sample Output 2:
'''
badc
dcba
'''

# put your python code here
used_alphabet = input()
cipher_alphabet = input()
to_encode = [x for x in input()]
to_decode = [x for x in input()]

encoded = ['' for x in to_encode]
decoded = ['' for x in to_decode]

# print(used_alphabet)
# print(cipher_alphabet)
# print(to_encode)
# print(to_decode)
for idx in range(len(used_alphabet)):
    find_letter = used_alphabet[idx]
    encode_letter = cipher_alphabet[idx]
    # print('find_letter:\t' + str(find_letter) + ', encode_letter:\t' + str(encode_letter))
    # print(to_encode)
    for i in range(len(to_encode)):
        letter = to_encode[i]
        # print(letter)
        if find_letter == letter:
            # print('find_letter:\t' + str(find_letter) + ', letter:\t' + str(letter))
            encoded[i] = encode_letter
    # print(to_decode)
    for i in range(len(to_decode)):
        letter = to_decode[i]
        # print(letter)
        if encode_letter == letter:
            # print('encode_letter:\t' + str(encode_letter) + ', letter:\t' + str(letter))
            decoded[i] = find_letter
            
a = ''.join(encoded)
b = ''.join(decoded)
ans_1 = '*d*%*d*#*d*'
ans_2 = 'dacabac'
# print(a + '\t' + ans_1)
# print(b + '\t' + ans_2)
# print(a == ans_1)
# print(b == ans_2)
print(a)
print(b)

#######################################################################################################################

# Find the greatest common denominator of the two integers.
# Sample Input:
'''
779820539 641724086
'''
# Sample Output:
'''
1
'''

# put your python code here

a, b = map(int, input().split())

# Using Euclid's Algorithm
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

print(gcd(max(a, b), min(a, b)))

#######################################################################################################################

# Write a program that takes a list of integers as input,
# and outputs the values that are repeated in it more than once.
# You may need the list method sort to solve this problem.
# Input format:
# One line with integers, separated by a space.
# Output format:
# A line with integers, separated by a space. The numbers must not be repeated, the output order can be arbitrary.

# Sample Input:
'''
4 8 0 3 4 2 0 3
'''
# Sample Output:
'''
0 3 4
'''
# put your python code here

repeated = []
try:
    inp_lst = input()
    inp_nums = list(map(int, inp_lst.split()))
    nums = sorted(inp_nums)
    if len(nums) > 0:
        curr = nums[0]
        for i in range(1, len(nums)):
            num = nums[i]
            if num == curr and num not in repeated:
                repeated.append(num)
            else:
                curr = num
except EOFError:
    pass
print(' '.join(list(map(str, repeated))))

#######################################################################################################################

# Write a program that uses regular expressions to check whether the input string is a phone number. 
# A phone number has the following form: 19∗∗∗∗∗∗∗∗∗, where ∗ is any number from 0 to 9.

# The program should print Yes or No.

# Sample Input:
'''
19123456789
'''
# Sample Output:
'''
Yes
'''

# put your python code here
import re
str1 = input() # "The8rain in Spain0"
#Check if the string contains any digits (numbers from 0-9):
x = re.findall("\d", str1[2:])
y = re.search('^19', str1)
z = len(x) == 9
'''
print('x:\t' + str(x))
print('y:\t' + str(y))
print('z:\t' + str(z))
'''
if x and y and z:
  print("Yes")
else:
  print("No")
  
#######################################################################################################################

# Implement reducer in the problem of calculating the average time a user spent on the page.

# Mapper transfers data to reducer in a form of key / value, where key - page address, value - number of seconds
# the user spent on this page. 

# Cast the average time at the output to an integer. The output data should be displayed in the order in
# which they came.

# Sample Input:
'''
www.facebook.com	100
www.google.com	10
www.google.com	5
www.google.com	15
stepic.org	60
stepic.org	100
'''
# Sample Output:
'''
www.facebook.com	100
www.google.com	10
stepic.org	80
'''
# put your python code here
import sys

sites = {}
for line in sys.stdin.readlines():
    site, views = line.split()
    visit = 1
    if site in sites:
        sites[site] = (sites[site][0] + visit, sites[site][1] + int(views))
    else:
        sites[site] = (visit, int(views))
        
        
for site in sites:
    print(site + '\t' + str(sites[site][1] // sites[site][0]))

#######################################################################################################################

# Write a program that takes a matrix as input, performs its transposing and outputs the result.

# Input format:
# In the first line – two integers n and m – the number of rows and columns, respectively.
# Next go n lines, with m integers each, separated by a space.

# Output format:
# The program should output m lines of the content of transposed matrix. Elements of the matrix
# should be separated by a space.

# Sample Input 1:
'''
2 3
1 2 3
4 5 6
'''
# Sample Output 1:
'''
1 4
2 5
3 6
'''
# Sample Input 2:
'''
2 2
1 2
3 4
'''
# Sample Output 2:
'''
1 3
2 4
'''
# put your python code here

def scan_matrix():
    n,m = list(map(int, input().split()))
    in_m = []
    for r in range(n):
        in_m.append(list(map(int, input().split())))
    return in_m

def reverse_matrix_rows(m):
    new_m = [[0 for y in range(len(m[x]))] for x in range(len(m))]
    for r in range(len(m)):
        row = m[r]
        for c in range(len(m[r])):
            new_m[r][c] = m[-1*(r+1)][-1*(c+1)]
    return new_m

def transpose(m):
    if len(m) == 0:
        return []
    new_m = [[0 for y in range(len(m))] for x in range(len(m[0]))]
    # print(new_m)
    for r in range(len(m)):
        row = m[r]
        for c in range(len(m[r])):
            new_m[c][r] = m[r][c]
    return new_m

def print_matrix(m):
    for r in m:
        print(' '.join(list(map(str, r))))

m = scan_matrix()
m_t = transpose(m)
# print(m)
print_matrix(m_t)

#######################################################################################################################

# Print the number of integers that are relatively prime (coprime) to input n
# Sample Input
'''
237642351
'''
# Sample Output
'''
158383680
'''

'''
This version naively checks every integer to n instead of using the totient function
to check only integers that may yield a new result


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)
    
def coprimes(n):
    c = 0
    for i in range(1, n):
        a = max(i, n)
        b = min(i , n)
        if gcd(a, b) == 1:
            c += 1 
    return c
    
n = int(input())
print(coprimes(n))
'''

# Python 3 program to calculate 
# Euler's Totient Function 
# using Euler's product formula 
  
def phi(n) : 
  
    result = n   # Initialize result as n 
       
    # Consider all prime factors 
    # of n and for every prime 
    # factor p, multiply result with (1 - 1 / p) 
    p = 2
    while(p * p<= n) : 
  
        # Check if p is a prime factor. 
        if (n % p == 0) : 
  
            # If yes, then update n and result 
            while (n % p == 0) : 
                n = n // p 
            result = result * (1.0 - (1.0 / (float) (p))) 
        p = p + 1
          
          
    # If n has a prime factor 
    # greater than sqrt(n) 
    # (There can be at-most one 
    # such prime factor) 
    if (n > 1) : 
        result = result * (1.0 - (1.0 / (float)(n))) 
   
    return (int)(result) 
      
      
# Driver program to test above function 
# for n in range(1, 11) : 
    # print("phi(", n, ") = ", phi(n)) 
n = int(input())
print(phi(n))
  
# This code is contributed 
# by Nikita Tiwari. 

#######################################################################################################################

# You need to write a program that "flips" a sequence of positive integers. On input there is a sequence of space
# separated positive integers. The sequence ends with zero. You are required to output the sequence in the 
# reverse order.
# The numbers should be space separated on the output. The terminating zero is simply the indicator of the end of
# the sequence, it is not a part of it, i.e. you should not output it.
# Sample Input:
'''
15 26 1 42 0
'''
# Sample Output:
'''
42 1 26 15
'''

# put your python code here

line = input()
nums = line.split()
flipped_nums = []
for i in range(len(nums) - 2, -1, -1):
    flipped_nums.append(nums[i])
print(" ".join(flipped_nums))    

#######################################################################################################################

# You are given an integer number of indefinite length. Check, whether this number divides by 3 or not, without
# using the remainder (%) operation.
# Print "YES" if the number divides by 3 and "NO" if it doesn't.
# Note: What happens, when you divide, say, 17 by 3? And then back.
# Sample Input 1:
'''
7
'''
# Sample Output 1:
'''
NO
'''
# Sample Input 2:
'''
43
'''
# Sample Output 2:
'''
NO
'''
# Sample Input 3:
'''
18
'''
# Sample Output 3:
'''
YES
'''

# put your python code here

def cont_divide(n):
    n = abs(n)
    if n < 3:
        return "NO"
    while n >= 3:
        n -= 3
        if n == 0:
            return "YES"
    return "NO"

n = int(input())
print(cont_divide(n))

'''
a = int(input())
print("type(a):\t" + str(type(a)))
b = a / 3
c = round(b)
print("type(b):\t" + str(type(b)))
print("c:\t" + str(c))
if int(b) == c:
    print("YES")
else:
    print("NO")
'''

#######################################################################################################################

# Class filter is one of the most frequently used classes in Python. In the constructor it takes the two
# arguments a and f – a sequence and a function, and allows to iterate only by such elements x from the sequence
# a that f(x) equals to True. Let’s say that in this case the function f accepts the element x, and the
# element x is an accepted one.

# In this problem, we ask you to implement the multifilter class, which will do the same as the standard
# filter class, but will use several functions instead of a single one.

# The decision to accept an element will be taken based on how many functions accept  this element,
# and how many don't. Let us mark these quantities as pos and neg.

# Let us introduce the notion of the decision function – this is the function, which takes the two
# arguments – numbers pos and neg, and returns True, if the element is allowed, and False otherwise.

# Let’s consider the acceptance process in more details in the following example:
# a = [1, 2, 3]
# f2(x) = x % 2 == 0 # returns True, if x is divisible by 2
# f3(x) = x % 3 == 0
# judge_any(pos, neg) = pos >= 1 # returns True, if at least one function accepts an element

# In this example, we want to filter the sequence a and keep only those elements, which are divided by two or three.

# The f2 function accepts only for the elements, which can be divided by two, and the f3 function accepts only
# for the elements, divided by three. The decision function accepts the element only in the case it was
# accepted by at least one of the functions f2 or f3, i.e. the elements, which can be divided
# either by two, or by three.

# Let’s take the first element x = 1.
# f2(x) is False, i.e. the function f2 does not accept the element x.
# f3(x) is also False, i.e. the function f3 also does not accept the element x.
# In this case pos = 0, as non of the functions accepts x, and, accordingly, neg = 2.
# judge_any(0, 2) is False, it means that we don't accept the element x = 1.

# Let’s take the second element x = 2.
# f2(x) is True
# f3(x) is False
# pos = 1, neg = 1
# judge_any(1, 1) is True, and it means that we accept the element x = 2.
# Similar for the third element x = 3.

# Thus, we got the sequence of the accepted elements [2, 3].
# The class should have the following structure:


class multifilter:
    def judge_half(pos, neg):
        # accepts the element, if at least half of the functions accept this 
        # element (pos >= neg)
        return pos >= neg

    def judge_any(pos, neg):
        # accepts the element, if at least one of the functions accept it (pos >= 1)
        return pos >= 1

    def judge_all(pos, neg):
        # accepts the element, if at all functions accept it (neg == 0)
        return neg == 0

    def __init__(self, iterable, *funcs, judge=judge_any):
        # iterable - the original sequence
        # funcs - the allowing functions
        # judge - the judging function
        self.iterable = iterable
        self.funcs = funcs
        self.judge = judge

    def __iter__(self):
        # returns iterator on the resulting sequencedef next(self):
        for i in self.iterable:
            pos = 0
            neg = 0
            for func in self.funcs:
                if func(i):
                    pos += 1
                else:
                    neg += 1
            if self.judge(pos, neg):
                yield i

def mul2(x):
    return x % 2 == 0

def mul3(x):
    return x % 3 == 0

def mul5(x):
    return x % 5 == 0


a = [i for i in range(31)] # [0, 1, 2, ... , 30]

ar = list(multifilter(a, mul2, mul3, mul5))
aa = [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]
print(str(ar) + "\n" + str(aa) + "\n" + str(aa == ar)) 
# [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]

br = list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_half))
ba = [0, 6, 10, 12, 15, 18, 20, 24, 30]
print(str(br) + "\n" + str(ba) + "\n" + str(ba == br)) 
# [0, 6, 10, 12, 15, 18, 20, 24, 30]

cr = list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_all))
ca = [0, 30]
print(str(cr) + "\n" + str(ca) + "\n" + str(ca == cr)) 
# [0, 30]

# print(list(multifilter([], mul2, judge=multifilter.judge_half)))


#print(list(multifilter(a, mul2, mul3, mul5))) 
# [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]

#print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_half))) 
# [0, 6, 10, 12, 15, 18, 20, 24, 30]

#print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_all))) 
# [0, 30]

# print(list(multifilter([], mul2, judge=multifilter.judge_half)))

#######################################################################################################################

# Given a list of football teams with the result of the match. Output the summary table of the results of all matches.
# The team gets 3 points for winning, 0 points for loosing, 1 point for draw.
# Input format:
# The first line specifies the integer n — the number of completed games.
# After this follow the n lines, which contain the game results in the following format:
# First_team;Goals_by_first_team;Second_team;Goals_by_second_team
# Output of your program should look like the following:
# Team:Total_games Wins Draws Defeats Total_points
# You can output teams in an arbitrary order.

# Sample Input1:
'''
3
Zenit;3;Spartak;1
Spartak;1;CSKA;1
CSKA;0;Zenit;2
'''
# Sample Output1:
'''
CSKA:2 0 1 1 1
Zenit:2 2 0 0 6
Spartak:2 0 1 1 1
'''
# Sample Input2:
'''
5
Zenit;3;Spartak;1
Spartak;1;CSKA;1
CSKA;0;Zenit;2
CSKA;0;Avery;3
Avery;5;Zenit;3
'''
# Sample Output2:
'''
Zenit:3 2 0 1 6
Spartak:2 0 1 1 1
CSKA:3 0 1 2 1
Avery:2 2 0 0 6
'''

team_stats = {}

class Team:
    def __init__(self, name, gf, ga):
        self.team_name = name
        self.goals_for = gf
        self.goals_against = ga
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.games_played = 0
        self.points = 0
        self.update_stats(gf, ga)
        
    def __repr__(self):
        name = str(self.team_name)
        gp = str(self.games_played)
        w = str(self.wins)
        l = str(self.losses)
        d = str(self.draws)
        p = str(self.points)
        return name + ":" + gp + " " + w + " " + d + " " + l + " " + p
    
    def update_stats(self, goals_for, goals_against):
        self.games_played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        win_game = goals_for > goals_against
        draw_game = goals_for == goals_against
        if win_game:
            self.wins += 1
            self.points += 3
        elif draw_game:
            self.draws += 1
            self.points += 1
        else:
            self.losses += 1
            
class ReportGame:
    def __init__(self, game_string):
        game_stats = game_string.split(";")
        self.game_string = game_string
        self.game_stats = game_stats
        team1 = game_stats[0]
        team1_score = game_stats[1]
        team2 = game_stats[2]
        team2_score = game_stats[3]
        if team1 not in team_stats:
            team_stats[team1] = Team(team1, team1_score, team2_score)
        else:
            team_stats[team1].update_stats(team1_score, team2_score)
        if team2 not in team_stats:
            team_stats[team2] = Team(team2, team2_score, team1_score)
        else:
            team_stats[team2].update_stats(team2_score, team1_score)
            
num_games = int(input())
games = [input() for line in range(num_games)]
# print(games)

for game in games:
    ReportGame(game)
    
for team, stats in team_stats.items():
    print(stats)
	
#######################################################################################################################

#Calculator

# Write a simple calculator that reads the three input lines: the first number, the second number and the
# operation, after which it applies the operation to the entered numbers ("first number" "operation" "second number")
# and outputs the result to the screen. Note that the numbers can be real.

# Supported operations: +, -, /, *, mod, pow, div; where 
# mod — taking the residue, 
# pow — exponentiation, 
# div — integer division.

# If a user performs the division and the second number is 0, it is necessary to output the line "Division by 0!".

# Sample Input 1:
'''
5.0
0.0
mod
'''
# Sample Output 1:
'''
Division by 0!
'''
# Sample Input 2:
'''
-12.0
-8.0
*
'''
# Sample Output 2:
'''
96.0
'''
# Sample Input 3:
'''
5.0
10.0
/
'''
# Sample Output 3:
'''
0.5
'''

# put your python code here

num_1 = float(input())
num_2 = float(input())
op = input()

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def fdiv(x, y):
    if y == 0:
        return "Division by 0!"
    return x / y

def mod(x, y):
    if y == 0:
        return "Division by 0!"
    return int(x) % int(y)

def exp(x, y):
    return x ** y

def div(x, y):
    if y == 0:
        return "Division by 0!"
    return x // y

supported_ops = {"+": add,
                 "-": sub,
                 "*": mul,
                 "/": fdiv,
                 "mod": mod,
                 "pow": exp,
                 "div": div}

if op in supported_ops:
    print(supported_ops[op](num_1, num_2))
	
#######################################################################################################################

# Write a program that checks whether two given words are anagrams.

# The program should output True in the case if entered words are anagrams, and False otherwise.

# Input format:

# Two words, each on a separate line. Words can only consist of Latin characters. Your solution should
# be case insensitive, i.e. characters' case should not affect the answer.

# Sample Input 1:
'''
silent
listen
'''
# Sample Output 1:
'''
True
'''
# Sample Input 2:
'''
AbaCa
AcaBa
'''
# Sample Output 2:
'''
True
'''
# Sample Input 3:
'''
abaca
acada
'''
# Sample Output 3:
'''
False
'''

# put your python code here

a = input()
b = input()

def anagram(a, b):
    a = a.upper()
    b = b.upper()
    if len(a) == len(b):
        for letter in a:
            if letter not in b:
                return False
            idx = b.index(letter)
            b = b[:idx] + b[idx + 1:]
            # print(b)
        return True
    else:
        return False
            
print(anagram(a, b))

#######################################################################################################################

# Fractional part 1

# Given a positive real number X. Output its fractional part.

# Sample Input:
'''
17.9
'''
# Sample Output:
'''
0.9
'''

# put your python code here

inp = input()
num = inp.split(".")
fraction = num[-1] if "." in inp else 0
print("0." + str(fraction))

'''
num = float(input())
whole = int(num)
print(str(num) + "\n" + str(whole) + "\n" + str(num - whole))
'''

#######################################################################################################################

# There are two horses on a chess board and four coordintes x1, y1, x2, y2 are typed in. Determine,
# whether they can hit each other or not. 

# INPUT

# Four integer coordinates in the following sequence: x1,y1,x2,y2. The coordinates are not the same.

# OUTPUT

# "YES" (uppercase), if they hit each other and "NO" if they don't. 

# Sample Input 1:
'''
4 4 2 5
'''
# Sample Output 1:
'''
YES
'''
# Sample Input 2:
'''
4 4 6 6
'''
# Sample Output 2:
'''
NO
'''
# Sample Input 3:
'''
4 4 6 5
'''
# Sample Output 3:
'''
YES
'''

# put your python code here

x1, y1, x2, y2 = list(map(int, input().split()))

def possible_moves_knight(knight_coordinates):
    ''' Knights move in L shapes '''
    '''
        _ # _ # _ # _
        # _ H _ A _ #
        _ G _ # _ B _
        # _ # K # _ #
        _ F _ # _ C _
        # _ E _ D _ #
        _ # _ # _ # _
    '''
    x = knight_coordinates[0]
    y = knight_coordinates[1]
    possible_locations = []
    new_coordinates = [ (x + 1, y + 2),
                        (x + 2, y + 1),
                        (x + 2, y - 1),
                        (x + 1, y - 2),
                        (x - 1, y - 2),
                        (x - 2, y - 1),
                        (x - 2, y + 1),
                        (x - 1, y + 2)]
    for coordinate in new_coordinates:
        new_x = coordinate[0]
        new_y = coordinate[1]
        if 0 <= new_x <= 7:
            if 0 <= new_y <= 7:
                possible_locations.append(coordinate)
    return possible_locations
    
knight1 = (x1, y1)
knight2 = (x2, y2)
# print(possible_moves_knight(knight1))
# print(possible_moves_knight(knight2))

def check_knight_hit(knight1, knight2):
    if knight2 in possible_moves_knight(knight1):
        return "YES"
    if knight1 in possible_moves_knight(knight2):
        return "YES"
    return "NO"

print(check_knight_hit(knight1, knight2))

#######################################################################################################################

# You are given two coordinates on a chess board of the first queen and two of the second. Find out, whether two queens hit each other or not.

# INPUT
# Four integer numbers x1,y1,x2,y2 are being typed.

# OUTPUT
# Type "YES" (uppercase) if they hit each other or "NO" if the don't.
# Sample Input 1:
'''
1 1 3 3
'''
# Sample Output 1:
'''
YES
'''
# Sample Input 2:
'''
1 1 4 3
'''
# Sample Output 2:
'''
NO
'''
# Sample Input 3:
'''
2 2 5 2
'''
# Sample Output 3:
'''
YES
'''

# put your python code here

x1, y1, x2, y2 = list(map(int, input().split()))

def possible_moves_queen(queen_coordinates):
    ''' Queens move vertically, horizontally and diagonally '''
    '''
        X # _ X _ # X
        # X # X # X #
        _ # X X X # _
        X X X Q X X X
        _ # X X X # _
        # X # X # X #
        X # _ X _ # X
    '''
    x = queen_coordinates[0]
    y = queen_coordinates[1]
    possible_locations = []
    new_coordinates = []
    for i in range(1, 7):
        ne = (x + i, y + i)
        se = (x + i, y - i)
        sw = (x - i, y - i)
        nw = (x - i, y + i)
        n = (x, y + i)
        e = (x + i, y)
        s = (x, y - i)
        w = (x - i, y)
        new_coordinates.append(ne)
        new_coordinates.append(se)
        new_coordinates.append(sw)
        new_coordinates.append(nw)
        new_coordinates.append(n)
        new_coordinates.append(e)
        new_coordinates.append(s)
        new_coordinates.append(w)
    
    for coordinate in new_coordinates:
        new_x = coordinate[0]
        new_y = coordinate[1]
        if 0 <= new_x <= 7:
            if 0 <= new_y <= 7:
                possible_locations.append(coordinate)
    return possible_locations
    
queen1 = (x1, y1)
queen2 = (x2, y2)
# print(possible_moves_queen(queen1))
# print(possible_moves_queen(queen2))

def check_queen_hit(queen1, queen2):
    if queen2 in possible_moves_queen(queen1):
        return "YES"
    if queen1 in possible_moves_queen(queen2):
        return "YES"
    return "NO"

print(check_queen_hit(queen1, queen2))

#######################################################################################################################

# A user inputs a word.

# Remove all letters that are in even positions in the word, and print what's left.

# Sample Input:
'''
Blackbeard
'''
# Sample Output:
'''
Baker
'''

# put your python code here
line = input()

res = ""
for i in range(len(line)):
    if i % 2 == 0:
        res += line[i]
print(res)

#######################################################################################################################

# Implement a data structure that represents an extended stack. It is necessary to support the pushing
# (appending) of the element to the top of the stack, the popping (removal) from the top of the stack,
# and also the operations of addition, subtraction, multiplication and integer division.

# The operation of addition on the stack is defined as follows. The top element (top1) is removed from the stack,
# then the next top element (top2) is removed, and then the element equal to top1 + top2 is pushed to the stack.

# In similar way are defined the operations of subtraction (top1 - top2), multiplication (top1 * top2) and
# integer division (top1 // top2).

# Implement this data structure as the ExtendedStack class, by inheriting it from the standard list class.
# The required class structure:

# class ExtendedStack(list):
    # def sum(self):
        # addition

    # def sub(self):
        # substraction

    # def mul(self):
        # multiplication

    # def div(self):
        # integer division
 
# Note Use the append method to push an element to the stack, and the pop method - to remove it. It is guaranteed
# that the extended operations will be requested only if the stack contains at least two elements.

class ExtendedStack(list):
    def sum(self):
        # addition
        a = self.pop()
        b = self.pop()
        self.append(a + b)

    def sub(self):
        # substraction
        a = self.pop()
        b = self.pop()
        self.append(a - b)

    def mul(self):
        # multiplication
        a = self.pop()
        b = self.pop()
        self.append(a * b)

    def div(self):
        # integer division
        a = self.pop()
        b = self.pop()
        self.append(a // b)
        
lst = [1, 3, 5]
es = ExtendedStack(lst)
print(es)
es.mul()
print(es)
es.sum()
print(es)

#######################################################################################################################

# Implement insertion sort for array of integers.

# The number of integers in the array is determined by the end of the standard input stream and is not
# known in advance.

# Sample Input:
'''
3 1 2
'''
# Sample Output:
'''
1 2 3
'''

# put your python code here

def insertion_sort(lst):
    res = []
    for i in range(len(lst)):
        num = lst[i]
        c = 0
        for j in range(len(res)):
            if num > res[j]:
                c += 1
        res = res[:c] + [num] + res[c:]
    return res

try:
    nums = input()
except:
    nums = ""
nums = list(map(int, nums.split()))
#nums = [i for i in range(1000)]
print(" ".join(list(map(str,insertion_sort(nums)))))

#######################################################################################################################

# Find the number of "Ds", "Cs", "Bs" and "As" for the last test on informatics in the class consisting of n
# students. The program gets number n as input, and then gets the grades themselves (one by one). The program
# should output four numbers in a single line - the number of "D", the number of "C", the number of "B" and the
# number of "A" grades.

# Sample Input:
'''
14
3
4
5
3
3
4
3
3
3
2
4
2
3
3
'''
# Sample Output:
'''
2 8 3 1
'''

# put your python code here

num_students = int(input())

grades = [int(input()) for student in range(num_students)]

a = grades.count(5)
b = grades.count(4)
c = grades.count(3)
d = grades.count(2)

grades_count = [d, c, b, a]
print(" ".join(list(map(str, grades_count))))

#######################################################################################################################

# Given two integers 1<=a,b<=2^10^9.

# Find the smallest integer m, which can be divided both by a, and by b.

# Sample Input:
'''
18 35
'''
# Sample Output:
'''
630
'''

# put your python code here

a, b = list(map(int, input().split()))

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)
    
def lcm(a, b):
    return (a * b) // gcd(a, b)

print(lcm(a, b))

#######################################################################################################################

# Transform the symbol into uppercase.

# Input data

# A single symbol.

# Output data

# If the entered symbol is a lowercase letter of the Latin alphabet, output the same uppercase letter.
# Otherwise, output the symbol that was entered.

# Sample Input:
'''
b
'''
# Sample Output:
'''
B
'''

# put your python code here
symbol = input().upper()
print(symbol)

#######################################################################################################################

# Given the array of length M with integers in the range 1 ... N, where N is not greater than 20. You need to
# go through the array and count how many times each number appears.

# Please do not use the 20 individual variables for the counters, but create an array from them.

# Input data contain M and N in the first line. Second line (it may be quite long) contains M numbers,
# separated by a space.

# The solution should contain exactly N numbers, separated by spaces. The first indicates the number
# of ones in the original array, the second – the number of twos, and so on.

# Sample Input:
'''
2 3
1 3
'''
# Sample Output:
'''
1 0 1
'''

# put your python code here

m, n = list(map(int, input().split()))

nums = list(map(int, input().split()))

res = []
for i in range(n):
    c = nums.count(i + 1)
    res.append(c)

print(" ".join(list(map(str, res))))

#######################################################################################################################

# Swap the position of neighbouring items of the list (A[0] with A[1], A[2] with A[3] etc.). If there is
# odd number of elements in the list, the last element remains at its position.

# Input data format

# The first line of the input contains the number of elements in the array. The second line contains
# the elements of the array.

# Sample Input:
'''
5
1 2 3 4 5
'''
# Sample Output:
'''
2 1 4 3 5
'''

# put your python code here
n = int(input())
nums = list(map(int, input().split()))

def swap_neighbours(lst):
    n = len(lst)
    for i in range(0, n, 2):
        a = lst[i]
        if i < n - 1:
            b = lst[i + 1]
            lst[i] = b
            lst[i + 1] = a
    return lst

print(" ".join(list(map(str, swap_neighbours(nums)))))

#######################################################################################################################
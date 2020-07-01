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
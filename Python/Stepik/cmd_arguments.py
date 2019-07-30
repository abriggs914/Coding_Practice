# Write a program that runs from the console and prints the values of all the transferred arguments on the screen (the name of the script does not need to be displayed). Do not change the order of the arguments in the output.
# To access the command-line arguments of the program import the sys module and use the argv variable from this module.
# Example of the program operation:
# > python3 my_solution.py arg1 arg2
# arg1 arg2

import sys

args = sys.argv

print(' '.join(args[1:]))
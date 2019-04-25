#In script.py import the datetime type from the datetime library.
#Create a variable current_time and set it equal to datetime.now().
#Print out current_time.
# Import datetime from datetime below:
from datetime import datetime
current_time = datetime.now()
print(current_time)

#-------------------------------------------------------------------------------------------------------------------------------------

#In script.py import the random library.
# Import random below:
import random

#Create a variable random_list and set it equal to an empty list
#Turn the empty list into a list comprehension that uses random.randint() to generate a random integer between 1 and 100 (inclusive) for each number in range(101).
# Create random_list below:
random_list = []
random_list = [random.randint(1,101) for i in range(101)]

# Create randomer_number below:
randomer_number = random.choice(random_list)

#Print randomer_number out to see what number was picked!
# Print randomer_number below:
print(randomer_number)

#-------------------------------------------------------------------------------------------------------------------------------------

# Import Decimal below:

from decimal import Decimal

cost_of_gum = 0.10
cost_of_gumdrop = 0.35

cost_of_transaction = cost_of_gum + cost_of_gumdrop
print(cost_of_transaction)

# Fix the floating point math below:
#Use Decimal to make two_decimal_points only have two decimals points and four_decimal_points to only have four decimal points.

two_decimal_points = 0.2 + 0.69
two_decimal_points = Decimal('0.2')
two_decimal_points += Decimal('0.69')

print(two_decimal_points)

four_decimal_points = 0.53 * 0.65
four_decimal_points = Decimal('0.53')
four_decimal_points += Decimal('0.65')
print(four_decimal_points)

# Import library below:
from libraryAlwaysThree import always_three


# Call your function below:
#Call your always_three() function in script.py. Check out that error message you get in the output terminal and the consequences of file scope.
always_three()


#import codecademylib
import pandas as pd

#WORKING WITH MULTIPLE DATAFRAMES
# Review
# This lesson introduced some methods for combining multiple DataFrames:
# Creating a DataFrame made by matching the common columns of two DataFrames is called a merge
# We can specify which columns should be matches by using the keyword arguments left_on and right_on
# We can combine DataFrames whose rows don’t all match using left, right, and outer merges and the how keyword argument
# We can stack or concatenate DataFrames with the same columns using pd.concat

visits = pd.read_csv('visits.csv',
                        parse_dates=[1])
checkouts = pd.read_csv('checkouts.csv',
                        parse_dates=[1])

#Cool T-Shirts Inc. just created a website for ordering their products. They want you to analyze two datasets for them:
#visits contains information on all visits to their landing page
#checkouts contains all users who began to checkout on their website
#Use print to inspect each DataFrame.
print(visits)
print(checkouts)

#We want to know the amount of time from a user’s initial visit to the website to when they start to check out.
#Use merge to combine visits and checkouts and save it to the variable v_to_c.
v_to_c = pd.merge(visits, checkouts)
print(v_to_c)

#In order to calculate the time between visiting and checking out, define a column of v_to_c called time by pasting the following code into script.py:
#v_to_c['time'] = v_to_c.checkout_time - \
#                 v_to_c.visit_time
#print(v_to_c)
v_to_c['time'] = v_to_c.checkout_time - \
                 v_to_c.visit_time

print(v_to_c)

#To get the average time to checkout, paste the following code into script.py:
#print(v_to_c.time.mean())
print(v_to_c.time.mean())


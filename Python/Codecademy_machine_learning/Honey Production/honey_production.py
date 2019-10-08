# SUPERVISED LEARNING: REGRESSION
# Honey Production
# Now that you have learned how linear regression works, let’s try it on an example of real-world data.

# As you may have already heard, the honeybees are in a precarious state right now. You may have seen articles about the decline of the honeybee population for various reasons. You want to investigate this decline and how the trends of the past predict the future for the honeybees.

# Note: All the tasks can be completed using Pandas or NumPy. Pick whichever one you prefer.

# If you get stuck during this project or would like to see an experienced developer work through it, click “Get Help“ to see a project walkthrough video.

import codecademylib3_seaborn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

df = pd.read_csv("https://s3.amazonaws.com/codecademy-content/programs/data-science-path/linear_regression/honeyproduction.csv")

#1.
# We have loaded in a DataFrame for you about honey production in the United States from Kaggle. It is called df and has the following columns:

# state
# numcol
# yieldpercol
# totalprod
# stocks
# priceperlb
# prodvalue
# year
# Use .head() to get a sense of how this DataFrame is structured.

#A DataFrame is a 2-dimensional labeled data structure with columns of potentially different types. you can think of it like a spreadsheet or a SQL table. it is generally the most commonly used pandas object.
# The .head() function return the first n rows:
# print(df.head())

print(df.head())

#2.
# For now, we care about the total production of honey per year. Use the .groupby() method provided by pandas to get the mean of totalprod per year.
# Store this in a variable called prod_per_year.

# To group the years, you might use a command like this:
# prod_per_year = df.groupby('year').totalprod.mean().reset_index()
# This will group the year column.

prod_per_year = df.groupby('year').totalprod.mean().reset_index()
# print(prod_per_year)

#3.
# Create a variable called X that is the column of years in this prod_per_year DataFrame.

# After creating X, we will need to reshape it to get it into the right format, using this command:

# X = X.values.reshape(-1, 1)
#You can select a column from a DataFrame by using bracket notation:
# column_of_interest = df["column name"]
X = prod_per_year['year']
X = X.values.reshape(-1, 1)
print(X)

#4.
# Create a variable called y that is the totalprod column in the prod_per_year dataset.
#You can select a column from a DataFrame by using bracket notation:
#column_of_interest = df["column name"]
y = prod_per_year['totalprod']
print(y)

plt.scatter(X, y)

# 6.
# Create a linear regression model from scikit-learn and call it regr.
# Use the LinearRegression() constructor from the linear_model module to do this.
# The LinearRegression class is from the linear_model module.
# To create a new LinearRegression object, just call linear_model.LinearRegression() and assign it to your variable name:
# my_regression_model = linear_model.LinearRegression()
regr = linear_model.LinearRegression()

#Fit the model to the data by using .fit(). You can feed X into your regr model by passing it in as a parameter of .fit().
regr.fit(X,y)

#After you have fit the model, print out the slope of the line (stored in a list called regr.coef_) and the intercept of the line (regr.intercept_).
#The slope of the line will be the first (and only) element of the regr.coef_ list. So using:
#print(regr.coef_[0])
#should print the slope.
print('slope:\t' + str(regr.coef_[0]))
print('intercept:\t' + str(regr.intercept_))

#9. Create a list called y_predict that is the predictions your regr model would make on the X data.
# You can use the .predict() method, using X as a parameter, to get the predictions from the regr object.
y_predict = regr.predict(X)

#10. Plot y_predict vs X as a line, on top of your scatterplot using plt.plot().
#Make sure to call plt.show() after plotting the line.
#After the first call to plt.plot(), but before you call plt.show(), you can plot a line using:
#plt.plot(X, y_predict)
plt.plot(X, y_predict)
plt.show()

# Predict the Honey Decline
# So, it looks like the production of honey has been in decline, according to this linear model. Let’s predict what the year 2050 may look like in terms of honey production.

# Our known dataset stops at the year 2013, so let’s create a NumPy array called X_future that is the range from 2013 to 2050. The code below makes a NumPy array with the numbers 1 through 10

# nums = np.array(range(1, 11))
# After creating that array, we need to reshape it for scikit-learn.

# X_future = X_future.reshape(-1, 1)
# You can think of reshape() as rotating this array. Rather than one big row of numbers, X_future is now a big column of numbers — there’s one number in each row.

# reshape() is a little tricky! It might help to print out X_future before and after reshaping.
#We want to make a list out of a range object:
#X_future = np.array(range(start_year, end_year))
X_future = np.array(range(2013, 2051))
X_future = X_future.reshape(-1, 1)

#12. Create a list called future_predict that is the y-values that your regr model would predict for the values of X_future.
#You can use the .predict() method, using X_future as a parameter, to get the predictions from the regr object.
future_predict = regr.predict(X_future)

#13. Plot future_predict vs X_future on a different plot.
# How much honey will be produced in the year 2050, according to this?
# Complete the following line of code:
# plt.plot(X_future, _____)
plt.plot(X_future, future_predict)

plt.show()
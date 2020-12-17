
# MULTIPLE LINEAR REGRESSION
# Introduction to Multiple Linear Regression
# Linear regression is useful when we want to predict the values of a variable from its relationship with other variables. There are two different types of linear regression models (simple linear regression and multiple linear regression).

# In predicting the price of a home, one factor to consider is the size of the home. The relationship between those two variables, price and size, is important, but there are other variables that factor in to pricing a home: location, air quality, demographics, parking, and more. When making predictions for price, our dependent variable, we’ll want to use multiple independent variables. To do this, we’ll use Multiple Linear Regression.

# Multiple Linear Regression uses two or more independent variables to predict the values of the dependent variable. It is based on the following equation that we’ll explore later on:

# y = b + m_{1}x_{1} + m_{2}x_{2} + ... + m_{n}x_{n}y=b+m 
# 1
# ​	 x 
# 1
# ​	 +m 
# 2
# ​	 x 
# 2
# ​	 +...+m 
# n
# ​	 x 
# n
# ​	 
# StreetEasy Dataset

# You’ll learn multiple linear regression by performing it on this dataset. It contains information about apartments in New York.

# Instructions
# 1.
# Before we start digging into the StreetEasy data, add this line at the end of script.py:

# plt.show()
# And then press run to see the graph!

# In this example, we used size (ft²) and building age (years) as independent variables to predict the rent ($).

# When we have two independent variables, we can create a linear regression plane. We can now guess what the rent is by plugging in the independent variables and finding where they lie on the plane.

# Checkpoint 2 Passed

# Hint
# Don’t worry if you don’t quite understand the model just yet!

# When we are looking at relationships, the independent variables are what you change. The dependent variable is what you measure. So, if we are looking at the way soil quality and watering frequency affects the height of a house plant, the independent variables would be:

# Soil quality
# Watering frequency
# The dependent variable would be height.

import codecademylib3_seaborn

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mpl_toolkits.mplot3d import Axes3D

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

streeteasy = pd.read_csv("https://raw.githubusercontent.com/sonnynomnom/Codecademy-Machine-Learning-Fundamentals/master/StreetEasy/manhattan.csv")

df = pd.DataFrame(streeteasy)

x = df[['size_sqft','building_age_yrs']]
y = df[['rent']]

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, test_size = 0.2, random_state=6)

ols = LinearRegression()

ols.fit(x_train, y_train)

# Plot the figure

fig = plt.figure(1, figsize=(6, 4))
plt.clf()

elev = 43.5
azim = -110

ax = Axes3D(fig, elev=elev, azim=azim)

ax.scatter(x_train[['size_sqft']], x_train[['building_age_yrs']], y_train, c='k', marker='+')

ax.plot_surface(np.array([[0, 0], [4500, 4500]]), np.array([[0, 140], [0, 140]]), ols.predict(np.array([[0, 0, 4500, 4500], [0, 140, 0, 140]]).T).reshape((2, 2)), alpha=.7)

ax.set_xlabel('Size (ft$^2$)')
ax.set_ylabel('Building Age (Years)')
ax.set_zlabel('Rent ($)')

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])

# Add the code below:
plt.show()

#######################################################################################################################

# MULTIPLE LINEAR REGRESSION
# StreetEasy Dataset
# StreetEasy Logo

# StreetEasy is New York City’s leading real estate marketplace — from studios to high-rises, Brooklyn Heights to Harlem.

# In this lesson, you will be working with a dataset that contains a sample of 5,000 rentals listings in Manhattan, Brooklyn, and Queens, active on StreetEasy in June 2016.

# It has the following columns:

# rental_id: rental ID
# rent: price of rent in dollars
# bedrooms: number of bedrooms
# bathrooms: number of bathrooms
# size_sqft: size in square feet
# min_to_subway: distance from subway station in minutes
# floor: floor number
# building_age_yrs: building’s age in years
# no_fee: does it have a broker fee? (0 for fee, 1 for no fee)
# has_roofdeck: does it have a roof deck? (0 for no, 1 for yes)
# has_washer_dryer: does it have washer/dryer in unit? (0/1)
# has_doorman: does it have a doorman? (0/1)
# has_elevator: does it have an elevator? (0/1)
# has_dishwasher: does it have a dishwasher (0/1)
# has_patio: does it have a patio? (0/1)
# has_gym: does the building have a gym? (0/1)
# neighborhood: (ex: Greenpoint)
# borough: (ex: Brooklyn)
# More information about this dataset can be found in the StreetEasy Dataset article.

# Let’s start by doing exploratory data analysis to understand the dataset better. We have broken the dataset for you into:

# manhattan.csv
# brooklyn.csv
# queens.csv
# Instructions
# 1.
# First, pick a borough out of the three (Manhattan, Brooklyn, and Queens) that you are most interested in!

# We are going to import the dataset and store it in a variable called df.

# To import, we will need to run this snippet:

# pd.read_csv("path")
# Replace path with one of the three URL’s above.

# Checkpoint 2 Passed

# Hint
# For example, if you want to take a look at the Manhattan data:

# df = pd.read_csv("https://raw.githubusercontent.com/Codecademy/datasets/master/streeteasy/manhattan.csv")
# Each dataset is going to be very different from the others. In this lesson, you are going to pick one of them!

# And now we have a DataFrame named df.

# A DataFrame is a 2-dimensional labeled data structure with columns of potentially different types. You can think of it like a spreadsheet or a SQL table. It is generally the most commonly used pandas object.

# Different Boroughs
# 2.
# Let’s take a look at the first few rows using df.head():

# How far is the apartment in the third row from a subway station?
# Which neighborhood is it in?
# Checkpoint 3 Passed

# Hint
# print(df.head())
# A table should appear on the right panel with column names and 5 rows of apartments.

# The answers to these questions depend on the borough that you picked!

import codecademylib3_seaborn
import pandas as pd

# df = pd.read_csv("manhattan.csv")
df = pd.read_csv("https://raw.githubusercontent.com/Codecademy/datasets/master/streeteasy/manhattan.csv")

print(df.head())

#######################################################################################################################

# MULTIPLE LINEAR REGRESSION
# Training Set vs. Test Set
# As with most machine learning algorithms, we have to split our dataset into:

# Training set: the data used to fit the model
# Test set: the data partitioned away at the very start of the experiment (to provide an unbiased evaluation of the model)
# Training Set vs. Testing Set

# In general, putting 80% of your data in the training set and 20% of your data in the test set is a good place to start.

# Suppose you have some values in x and some values in y:

# from sklearn.model_selection import train_test_split

# x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2)
# Here are the parameters:

# train_size: the proportion of the dataset to include in the train split (between 0.0 and 1.0)
# test_size: the proportion of the dataset to include in the test split (between 0.0 and 1.0)
# random_state: the seed used by the random number generator [optional]
# To learn more, here is a Training Set vs Validation Set vs Test Set article.

# Instructions
# 1.
# Import train_test_split from sklearn.model_selection.

# Checkpoint 2 Passed

# Stuck? Get a hint
# 2.
# Create a DataFrame x that selects the following columns from the main df DataFrame:

# 'bedrooms'
# 'bathrooms'
# 'size_sqft'
# 'min_to_subway'
# 'floor'
# 'building_age_yrs'
# 'no_fee'
# 'has_roofdeck'
# 'has_washer_dryer'
# 'has_doorman'
# 'has_elevator'
# 'has_dishwasher'
# 'has_patio'
# 'has_gym'
# Create a DataFrame y that selects the rent column from the main df DataFrame.

# These are the columns we want to use for our regression model.

# Checkpoint 3 Passed

# Hint
# To select columns from a DataFrame:

# name = df[['Column1', 'Column2']]
# So it should look something like:

# x = df[['bedrooms', 'bathrooms', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs', 'no_fee', 'has_roofdeck', 'has_washer_dryer', 'has_doorman', 'has_elevator', 'has_dishwasher', 'has_patio', 'has_gym']]

# y = df[['rent']]
# 3.
# Use scikit-learn’s train_test_split() method to split x into 80% training set and 20% testing set and generate:

# x_train
# x_test
# y_train
# y_test
# Set the random_state to 6.

# Checkpoint 4 Passed

# Hint
# x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, test_size = 0.2, random_state=6)
# 4.
# Let’s take a look at the shapes of x_train, x_test, y_train, and y_test to see we got the proportion we wanted.

# We have 14 features that we’re looking for for each apartment, and 1 label we’re looking for for each apartment.

# Checkpoint 5 Passed

# Hint
# The .shape attribute for NumPy arrays returns the dimensions of the array. If array has n rows × m columns, then array.shape returns (n, m).

# print(x_train.shape)
# print(x_test.shape)

# print(y_train.shape)
# print(y_test.shape)
# For the Manhattan data, this results in:

# (2831, 14)
# (708, 14)
# (2831, 1)
# (708, 1)

import codecademylib3_seaborn
import pandas as pd

# import train_test_split
from sklearn.model_selection import train_test_split

streeteasy = pd.read_csv("https://raw.githubusercontent.com/sonnynomnom/Codecademy-Machine-Learning-Fundamentals/master/StreetEasy/manhattan.csv")

df = pd.DataFrame(streeteasy)

cols = ['bedrooms',
'bathrooms',
'size_sqft',
'min_to_subway',
'floor',
'building_age_yrs',
'no_fee',
'has_roofdeck',
'has_washer_dryer',
'has_doorman',
'has_elevator',
'has_dishwasher',
'has_patio',
'has_gym']

x = df[cols]
y = df[['rent']]

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2, random_state=6)

frames = [x_train, x_test, y_train, y_test]
for f in frames:
  print(f.shape)

# print("x_train.size:", x_train.size)
# print("x_test.size:", x_test.size)
# print("y_train.size:", y_train.size)
# print("y_test.size:", y_test.size)


#######################################################################################################################

# MULTIPLE LINEAR REGRESSION
# Multiple Linear Regression: Scikit-Learn
# Now we have the training set and the test set, let’s use scikit-learn to build the linear regression model!

# The steps for multiple linear regression in scikit-learn are identical to the steps for simple linear regression. Just like simple linear regression, we need to import LinearRegression from the linear_model module:

# from sklearn.linear_model import LinearRegression
# Then, create a LinearRegression model, and then fit it to your x_train and y_train data:

# mlr = LinearRegression()

# mlr.fit(x_train, y_train) 
# # finds the coefficients and the intercept value
# We can also use the .predict() function to pass in x-values. It returns the y-values that this plane would predict:

# y_predicted = mlr.predict(x_test)
# # takes values calculated by `.fit()` and the `x` values, plugs them into the multiple linear regression equation, and calculates the predicted y values. 
# We will start by using two of these columns to teach you how to predict the values of the dependent variable, prices.

# Instructions
# 1.
# Import LinearRegression from scikit-learn’s linear_model module.

# Checkpoint 2 Passed

# Hint
# It should look something like:

# from sklearn.linear_model import LinearRegression
# 2.
# Create a Linear Regression model and call it mlr.

# Fit the model using x_train and y_train.

# Checkpoint 3 Passed

# Hint
# # Create the model
# mlr = LinearRegression()

# # Fit the model
# mlr.fit(x_train, y_train)
# 3.
# Use the model to predict y-values from x_test. Store the predictions in a variable called y_predict.

# Now we have:

# x_test
# x_train
# y_test
# y_train
# and y_predict!
# Checkpoint 4 Passed

# Hint
# y_predict = mlr.predict(x_test)
# 4.
# To see this model in action, let’s test it on Sonny’s apartment in Greenpoint, Brooklyn!

# Or if you reside in New York, plug in your own apartment’s values and see if you are over or underpaying!

# Checkpoint 5 Passed

# Hint
# This is a 1BR/1Bath apartment that is 620 ft². We have pulled together the data for you:

# Features	Sonny’s Apartment
# bedrooms	1
# bathrooms	1
# size_sqft	620 ft²
# min_to_subway	16 min
# floor	1
# building_age_yrs	98 (built in 1920)
# no_fee	1
# has_roofdeck	0
# has_washer_dryer	Yas
# has_doorman	0
# has_elevator	0
# has_dishwasher	1
# has_patio	1
# has_gym	0

# # Sonny doesn't have an elevator so the 11th item in the list is a 0
# sonny_apartment = [[1, 1, 620, 16, 1, 98, 1, 0, 1, 0, 0, 1, 1, 0]]

# predict = mlr.predict(sonny_apartment)

# print("Predicted rent: $%.2f" % predict)
# The result is:

# Predicted rent: $2393.58
# And Sonny is only paying $2,000. Yay!

import codecademylib3_seaborn
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split


streeteasy = pd.read_csv("https://raw.githubusercontent.com/sonnynomnom/Codecademy-Machine-Learning-Fundamentals/master/StreetEasy/manhattan.csv")

df = pd.DataFrame(streeteasy)

x = df[['bedrooms', 'bathrooms', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs', 'no_fee', 'has_roofdeck', 'has_washer_dryer', 'has_doorman', 'has_elevator', 'has_dishwasher', 'has_patio', 'has_gym']]

y = df[['rent']]

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, test_size = 0.2, random_state=6)

# Add the code here:

from sklearn.linear_model import LinearRegression

mlr = LinearRegression()
mlr.fit(x_train, y_train)

y_predict = mlr.predict(x_test)

# Sonny doesn't have an elevator so the 11th item in the list is a 0
sonny_apartment = [[1, 1, 620, 16, 1, 98, 1, 0, 1, 0, 0, 1, 1, 0]]

predict = mlr.predict(sonny_apartment)

print("Predicted rent: $%.2f" % predict)


#######################################################################################################################

# MULTIPLE LINEAR REGRESSION
# Visualizing Results with Matplotlib
# You’ve performed Multiple Linear Regression, and you also have the predictions in y_predict. However, we don’t have insight into the data, yet. In this exercise, you’ll create a 2D scatterplot to see how the independent variables impact prices.

# How do you create 2D graphs?

# Graphs can be created using Matplotlib’s pyplot module. Here is the code with inline comments explaining how to plot using Matplotlib’s .scatter():

# # Create a scatter plot
# plt.scatter(x, y, alpha=0.4)

# # Create x-axis label and y-axis label
# plt.xlabel("the x-axis label")
# plt.ylabel("the y-axis label")

# # Create a title
# plt.title("title!")

# # Show the plot
# plt.show()
# We want to create a scatterplot like this:

# Visualization
# Instructions
# 1.
# Create a 2D scatter plot using y_test and y_predict.

# The x-axis should represent actual rent prices and the y-axis should represent predicted rent prices.

# Checkpoint 2 Passed

# Hint
# It should look something like:

# plt.scatter(y_test, y_predict, alpha=0.4)
# The alpha parameter is added to better understand overlapping of points (0.0 transparent - 1.0 opaque).

# 2.
# Add appropriate x-axis labels and y-axis labels, as well as a title.

# Checkpoint 3 Passed

# Hint
# plt.xlabel("Prices: $Y_i$")
# plt.ylabel("Predicted prices: $\hat{Y}_i$")
# plt.title("Actual Rent vs Predicted Rent")
# 3.
# Show the plot using plt.show().

# Checkpoint 4 Passed

# Hint
# This line displays the figure:

# plt.show()

import codecademylib3_seaborn
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

streeteasy = pd.read_csv("https://raw.githubusercontent.com/sonnynomnom/Codecademy-Machine-Learning-Fundamentals/master/StreetEasy/manhattan.csv")

df = pd.DataFrame(streeteasy)

x = df[['bedrooms', 'bathrooms', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs', 'no_fee', 'has_roofdeck', 'has_washer_dryer', 'has_doorman', 'has_elevator', 'has_dishwasher', 'has_patio', 'has_gym']]

y = df[['rent']]

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, test_size = 0.2, random_state=6)

lm = LinearRegression()

model=lm.fit(x_train, y_train)

y_predict = lm.predict(x_test)

plt.scatter(y_test, y_predict)
plt.title("Rent prices")
plt.xlabel("actual rent prices")
plt.ylabel("predicted rent prices")
plt.show()

#######################################################################################################################

# MULTIPLE LINEAR REGRESSION
# Multiple Linear Regression Equation
# Now that we have implemented Multiple Linear Regression, we will learn how to tune and evaluate the model. Before we do that, however, it’s essential to learn the equation behind it.

# Equation 6.1 The equation for multiple linear regression that uses two independent variables is this:

# y = b + m_{1}x_{1} + m_{2}x_{2}y=b+m 
# 1
# ​	 x 
# 1
# ​	 +m 
# 2
# ​	 x 
# 2
# ​	 
# Equation 6.2 The equation for multiple linear regression that uses three independent variables is this:
# m1 * x1 + m2 * x2

# y = b + m_{1}x_{1} + m_{2}x_{2} + m_{3}x_{3}y=b+m 
# 1
# ​	 x 
# 1
# ​	 +m 
# 2
# ​	 x 
# 2
# ​	 +m 
# 3
# ​	 x 
# 3
# ​	 
# Equation 6.3 As a result, since multiple linear regression can use any number of independent variables, its general equation becomes:
# m1 * x1 + m2 * x2 + m3 * x3

# y = b + m_{1}x_{1} + m_{2}x_{2} + ... + m_{n}x_{n}y=b+m 
# 1
# ​	 x 
# 1
# ​	 +m 
# 2
# ​	 x 
# 2
# ​	 +...+m 
# n
# ​	 x 
# n
# ​	 
# Here, m1, m2, m3, … mn refer to the coefficients, and b refers to the intercept that you want to find. You can plug these values back into the equation to compute the predicted y values.
# m1 * x1 + m2 * x2 + ... + mn * xn

# Remember, with sklearn‘s LinearRegression() method, we can get these values with ease.

# The .fit() method gives the model two variables that are useful to us:

# .coef_, which contains the coefficients
# .intercept_, which contains the intercept
# After performing multiple linear regression, you can print the coefficients using .coef_.

# Coefficients are most helpful in determining which independent variable carries more weight. For example, a coefficient of -1.345 will impact the rent more than a coefficient of 0.238, with the former impacting prices negatively and latter positively.

# Instructions
# 1.
# Print out the coefficients using .coef_.

# Checkpoint 2 Passed

# Hint
# print(mlr.coef_)
# The coefficients should look something like (depend on which borough dataset that you used):

# [[ -302.73009383  1199.3859951      4.79976742   -24.28993151
     # 24.19824177    -7.58272473  -140.90664773    48.85017415   191.4257324
   # -151.11453388    89.408889     -57.89714551   -19.31948556
    # -38.92369828]]

import codecademylib3_seaborn
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

streeteasy = pd.read_csv("https://raw.githubusercontent.com/sonnynomnom/Codecademy-Machine-Learning-Fundamentals/master/StreetEasy/manhattan.csv")

df = pd.DataFrame(streeteasy)

x = df[['bedrooms', 'bathrooms', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs', 'no_fee', 'has_roofdeck', 'has_washer_dryer', 'has_doorman', 'has_elevator', 'has_dishwasher', 'has_patio', 'has_gym']]

y = df[['rent']]

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, test_size = 0.2, random_state=6)

mlr = LinearRegression()

model=mlr.fit(x_train, y_train)

y_predict = mlr.predict(x_test)

# Input code here:
print(mlr.coef_)


#######################################################################################################################

# MULTIPLE LINEAR REGRESSION
# Correlations
# In our Manhattan model, we used 14 variables, so there are 14 coefficients:

# [ -302.73009383  1199.3859951  4.79976742  -24.28993151  24.19824177  -7.58272473  -140.90664773  48.85017415  191.4257324  -151.11453388  89.408889  -57.89714551  -19.31948556  -38.92369828 ]]
# bedrooms - number of bedrooms
# bathrooms - number of bathrooms
# size_sqft - size in square feet
# min_to_subway - distance from subway station in minutes
# floor - floor number
# building_age_yrs - building’s age in years
# no_fee - has no broker fee (0 for fee, 1 for no fee)
# has_roofdeck - has roof deck (0 for no, 1 for yes)
# has_washer_dryer - has in-unit washer/dryer (0/1)
# has_doorman - has doorman (0/1)
# has_elevator - has elevator (0/1)
# has_dishwasher - has dishwasher (0/1)
# has_patio - has patio (0/1)
# has_gym - has gym (0/1)
# To see if there are any features that don’t affect price linearly, let’s graph the different features against rent.

# Interpreting graphs

# In regression, the independent variables will either have a positive linear relationship to the dependent variable, a negative linear relationship, or no relationship. A negative linear relationship means that as X values increase, Y values will decrease. Similarly, a positive linear relationship means that as X values increase, Y values will also increase.

# Graphically, when you see a downward trend, it means a negative linear relationship exists. When you find an upward trend, it indicates a positive linear relationship. Here are two graphs indicating positive and negative linear relationships:

# Positive and Negative Linear Relationships

# Instructions
# 1.
# Create a scatterplot of size_sqft and rent:

# plt.scatter(df[['size_sqft']], df[['rent']], alpha=0.4)
# Is there a strong correlation?

# Checkpoint 2 Passed

# Hint
# The alpha parameter is added to better understand overlapping of points (0.0 transparent - 1.0 opaque).

# 2.
# Create a scatterplot of min_to_subway and rent:

# plt.scatter(df[['min_to_subway']], df[['rent']], alpha=0.4)
# Is there a strong correlation?

# Checkpoint 3 Passed

# Hint
# The alpha parameter is added to better understand overlapping of points (0.0 transparent - 1.0 opaque).

# 3.
# Do the same for a few others and write down the ones that don’t have strong correlations.

import codecademylib3_seaborn
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

streeteasy = pd.read_csv("https://raw.githubusercontent.com/sonnynomnom/Codecademy-Machine-Learning-Fundamentals/master/StreetEasy/manhattan.csv")

df = pd.DataFrame(streeteasy)

# Input code here:

# plt.scatter(df[["size_sqft"]], df[["rent"]], alpha=0.4)
# plt.xlabel("size_sqft")
# plt.ylabel("rent")
# plt.title("size_sqft vs rent")
# Very strong correlation between these 2 variables

# plt.scatter(df[["min_to_subway"]], df[["rent"]], alpha=0.4)
# plt.xlabel("min_to_subway")
# plt.ylabel("rent")
# plt.title("min_to_subway vs rent")
# No strong correlation between these 2 variables

variables = ["bedrooms", "bathrooms", "size_sqft","min_to_subway", "floor", "building_age_yrs", "no_fee", "has_roofdeck", "has_washer_dryer", "has_elevator", "has_dishwasher", "has_patio", "has_gym"]

for var in variables:
  plt.clf()
  plt.scatter(df[["rent"]], df[[var]], alpha=0.4)
  plt.ylabel(var)
  plt.xlabel("rent")
  plt.title(str(var) + " vs rent")
  plt.show()

# plt.show()

#######################################################################################################################

# MULTIPLE LINEAR REGRESSION
# Evaluating the Model's Accuracy
# When trying to evaluate the accuracy of our multiple linear regression model, one technique we can use is Residual Analysis.

# The difference between the actual value y, and the predicted value ŷ is the residual e. The equation is:

# e = y - \hat{y}e=y− 
# y
# ^
# ​	 
# In the StreetEasy dataset, y is the actual rent and the ŷ is the predicted rent. The real y values should be pretty close to these predicted y values.

# sklearn‘s linear_model.LinearRegression comes with a .score() method that returns the coefficient of determination R² of the prediction.

# The coefficient R² is defined as:

# 1 - \frac{u}{v}1− 
# v
# u
# ​	 
# where u is the residual sum of squares:

# ((y - y_predict) ** 2).sum()
# and v is the total sum of squares (TSS):

# ((y - y.mean()) ** 2).sum()
# The TSS tells you how much variation there is in the y variable.

# R² is the percentage variation in y explained by all the x variables together.

# For example, say we are trying to predict rent based on the size_sqft and the bedrooms in the apartment and the R² for our model is 0.72 — that means that all the x variables (square feet and number of bedrooms) together explain 72% variation in y (rent).

# Now let’s say we add another x variable, building’s age, to our model. By adding this third relevant x variable, the R² is expected to go up. Let say the new R² is 0.95. This means that square feet, number of bedrooms and age of the building together explain 95% of the variation in the rent.

# The best possible R² is 1.00 (and it can be negative because the model can be arbitrarily worse). Usually, a R² of 0.70 is considered good.

# Instructions
# 1.
# Use the .score() method from LinearRegression to find the mean squared error regression loss for the training set.

# Write that number down.

# Checkpoint 2 Passed

# Hint
# print("Train score:")
# print(lm.score(x_train, y_train))
# 2.
# Use the .score() method from LinearRegression to find the mean squared error regression loss for the testing set.

# Write that number down.

# Checkpoint 3 Passed

# Hint
# print("Test score:")
# print(lm.score(x_test, y_test))
# Optional: If you want to graph a scatter plot of residuals vs. predicted_y values:

# residuals = y_predict - y_test

# plt.scatter(y_predict, residuals, alpha=0.4)
# plt.title('Residual Analysis')

# plt.show()

import codecademylib3_seaborn
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

streeteasy = pd.read_csv("https://raw.githubusercontent.com/sonnynomnom/Codecademy-Machine-Learning-Fundamentals/master/StreetEasy/manhattan.csv")

df = pd.DataFrame(streeteasy)

x = df[['bedrooms', 'bathrooms', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs', 'no_fee', 'has_roofdeck', 'has_washer_dryer', 'has_doorman', 'has_elevator', 'has_dishwasher', 'has_patio', 'has_gym']]

y = df[['rent']]

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, test_size = 0.2, random_state=6)

mlr = LinearRegression()

model=mlr.fit(x_train, y_train)

y_predict = mlr.predict(x_test)

# Input code here:

print("mlr.score(x_train, y_train):\t", mlr.score(x_train, y_train))
print("mlr.score(x_test, y_test):\t", mlr.score(x_test, y_test))

residuals = y_predict - y_test

plt.scatter(y_predict, residuals, alpha=0.4)
plt.title('Residual Analysis')

plt.show()

#######################################################################################################################

# MULTIPLE LINEAR REGRESSION
# Rebuild the Model
# Now let’s rebuild the model using the new features as well as evaluate the new model to see if we improved!

# For Manhattan, the scores returned:

# Train score: 0.772546055982
# Test score:  0.805037197536
# For Brooklyn, the scores returned:

# Train score: 0.613221453798
# Test score:  0.584349923873
# For Queens, the scores returned:

# Train score: 0.665836031009
# Test score:  0.665170319781
# For whichever borough you used, let’s see if we can improve these scores!

# Instructions
# 1.
# Print the coefficients again to see which ones are strongest.

# Checkpoint 2 Passed
# 2.
# Currently the x should look something like:

# x = df[['bedrooms', 'bathrooms', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs', 'no_fee', 'has_roofdeck', 'has_washer_dryer', 'has_doorman', 'has_elevator', 'has_dishwasher', 'has_patio', 'has_gym']]
# Remove some of the features that don’t have strong correlations and see if your scores improved!

# Post your best model in the Slack channel!

# Checkpoint 3 Passed

# Hint
# There is no right answer! Try building a model using different features!

import codecademylib3_seaborn
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

streeteasy = pd.read_csv("https://raw.githubusercontent.com/sonnynomnom/Codecademy-Machine-Learning-Fundamentals/master/StreetEasy/manhattan.csv")

df = pd.DataFrame(streeteasy)

# x before
# x = df[['bedrooms', 'bathrooms', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs', 'no_fee', 'has_roofdeck', 'has_washer_dryer', 'has_doorman', 'has_elevator', 'has_dishwasher', 'has_patio', 'has_gym']]

# x after
x = df[['size_sqft', 'floor', 'has_roofdeck', 'has_elevator']]

y = df[['rent']]

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, test_size = 0.2, random_state=6)

lm = LinearRegression()

model = lm.fit(x_train, y_train)

y_predict= lm.predict(x_test)

print("Train score:")
print(lm.score(x_train, y_train))

print("Test score:")
print(lm.score(x_test, y_test))

plt.scatter(y_test, y_predict)
plt.plot(range(20000), range(20000))

plt.xlabel("Prices: $Y_i$")
plt.ylabel("Predicted prices: $\hat{Y}_i$")
plt.title("Actual Rent vs Predicted Rent")

plt.show()

# zoe_apartment = [[1, 1, 620, 16, 1, 98, 0, 0, 1, 0, 0, 0, 1, 0]]
# predict = model.predict(zoe_apartment)
# print("Predicted rent: $%.2f" % predict)

print("lm.coef_:\n", lm.coef_)


#######################################################################################################################

# MULTIPLE LINEAR REGRESSION
# Review
# Great work! Let’s review the concepts before you move on:

# Multiple Linear Regression uses two or more variables to make predictions about another variable:
# y = b + m_{1}x_{1} + m_{2}x_{2} + ... + m_{n}x_{n}y=b+m 
# 1
# ​	 x 
# 1
# ​	 +m 
# 2
# ​	 x 
# 2
# ​	 +...+m 
# n
# ​	 x 
# n
# ​	 
# Multiple linear regression uses a set of independent variables and a dependent variable. It uses these variables to learn how to find optimal parameters. It takes a labeled dataset and learns from it. Once we confirm that it’s learned correctly, we can then use it to make predictions by plugging in new x values.
# We can use scikit-learn’s LinearRegression() to perform multiple linear regression.
# Residual Analysis is used to evaluate the regression model’s accuracy. In other words, it’s used to see if the model has learned the coefficients correctly.
# Scikit-learn’s linear_model.LinearRegression comes with a .score() method that returns the coefficient of determination R² of the prediction. The best score is 1.0.

#######################################################################################################################
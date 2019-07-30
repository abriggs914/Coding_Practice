#LINEAR REGRESSION
# Points and Lines
# In the last exercise, you were probably able to make a rough estimate about the next data point for Sandra’s lemonade stand without thinking too hard about it. For our program to make the same level of guess, we have to determine what a line would look like through those data points.

# A line is determined by its slope and its intercept. In other words, for each point y on a line we can say:

# y = m x + by=mx+b
# where m is the slope, and b is the intercept. y is a given point on the y-axis, and it corresponds to a given x on the x-axis.

# The slope is a measure of how steep the line is, while the intercept is a measure of where the line hits the y-axis.

# When we perform Linear Regression, the goal is to get the “best” m and b for our data. We will determine what “best” means in the next exercises.

# Instructions
# 1.
# We have provided a slope, m, and an intercept, b, that seems to describe the revenue data you have been given.

# Create a new list, y, that has every element in months, multiplied by m and added to b.

# A list comprehension is probably the easiest way to do this!

# The syntax for a list comprehension to find the points of a line might look like:

# y_values = [slope*x_value + intercept for x_value in x_values]
# This goes through each value in the list of x-values, multiplies it by the slope, adds it to the intercept, and appends it to a new list of y-values.

# 2.
# Plot the y values against months as a line on top of the scatterplot that was plotted with the line plt.plot(months, revenue, "o").

# To plot a line, you can use the syntax:

# plt.plot(x, y)
# Make both .plot() calls before you call .show() to have them on the same line.

# 3.
# Change m and b to the values that you think match the data the best.

# What does the slope look like it should be? And the intercept?

# To make the line steeper, increase the m value. To move the line up, increase the b value.

import codecademylib3_seaborn
import matplotlib.pyplot as plt
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
revenue = [52, 74, 79, 95, 115, 110, 129, 126, 147, 146, 156, 184]

#slope:
m = 10
#intercept:
b = 45

y = [((x * m) + b) for x in months]
plt.plot(months, y)

plt.plot(months, revenue, y, "o")

plt.show()
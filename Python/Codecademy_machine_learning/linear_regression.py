# LINEAR REGRESSION
# Loss
# When we think about how we can assign a slope and intercept to fit a set of points, we have to define what the best fit is.

# For each data point, we calculate loss, a number that measures how bad the model’s (in this case, the line’s) prediction was. You may have seen this being referred to as error.

# We can think about loss as the squared distance from the point to the line. We do the squared distance (instead of just the distance) so that points above and below the line both contribute to total loss in the same way:


# In this example:

# For point A, the squared distance is 9 (3²)
# For point B, the squared distance is 1 (1²)
# So the total loss, with this model, is 10. If we found a line that had less loss than 10, that line would be a better model for this data.

# Instructions
# 1.
# We have three points, (1, 5), (2, 1), and (3, 3). We are trying to find a line that produces lowest loss.

# We have provided you the list of x-values, x, and y-values, y, for these points.

# Find the y-values that the line with weights m1 and b1 would predict for the x-values given. Store these in a list called y_predicted1.

# A list comprehension is probably the easiest way to do this.

# The syntax might look like:

# y_predicted1 = [slope*x_value + intercept for x_value in x]
# This goes through each value in the list of x-values, multiplies it by the slope, adds it to the intercept, and appends it to a new list of y-values.

# 2.
# Find the y values that the line with weights m2 and b2 would predict for the x-values given. Store these in a list called y_predicted2.

# A list comprehension is probably the easiest way to do this.

# The syntax might look like:

# y_predicted2 = [slope*x_value + intercept for x_value in x]
# This goes through each value in the list of x-values, multiplies it by the slope, adds it to the intercept, and appends it to a new list of y-values.

# 3.
# Create a variable called total_loss1 and set it equal to zero.

# Then, find the sum of the squared distance between the actual y-values of the points and the y_predicted1 values by looping through the list:

# Calculating the difference between y and y_predicted1
# Squaring the difference
# Adding it to total_loss1
# 4.
# Create a variable called total_loss2 and set it equal to zero.

# Find the sum of the squared distance between the actual y-values of the points and the y_predicted2 values by looping through the list:

# Calculating the difference between y and y_predicted2
# Squaring the difference
# Adding it to total_loss2
# You can do this in the same for loop you made for the last total_loss value.

# So now it should look like:

# total_loss1 = 0
# total_loss2 = 0

# for i in range(len(y)):
#   total_loss1 += (y[i] - y_predicted1[i]) ** 2
#   total_loss2 += (y[i] - y_predicted2[i]) ** 2
# 5.
# Print out total_loss1 and total_loss2. Out of these two lines, which would you use to model the points?

# Create a variable called better_fit and assign it to 1 if line 1 fits the data better and 2 if line 2 fits the data better.

# The result should look something like:

# 17 13.5
# The line that produces the lowest total loss will be the line of better fit. So here, the second line is a line of better fit.

x = [1, 2, 3]
y = [5, 1, 3]

#y = x
m1 = 1
b1 = 0

#y = 0.5x + 1
m2 = 0.5
b2 = 1

y_predicted1 = [m1*i + b1 for i in x]
y_predicted2 = [m2*i + b2 for i in x]
print('y_predicted1:\t' + str(y_predicted1))
print('y_predicted2:\t' + str(y_predicted2))

total_loss1 = 0

for i in range(len(y)):
  d = y[i] - y_predicted1[i]
  total_loss1 += d ** 2

total_loss2 = 0

for i in range(len(y)):
  d = y[i] - y_predicted2[i]
  total_loss2 += d ** 2
  
print('total_loss1:\t' + str(total_loss1))
print('total_loss2:\t' + str(total_loss2))

better_fit = 2

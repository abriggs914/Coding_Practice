# LINEAR REGRESSION
# Gradient Descent for Intercept
# As we try to minimize loss, we take each parameter we are changing, and move it as long as we are decreasing loss. It’s like we are moving down a hill, and stop once we reach the bottom:


# The process by which we do this is called gradient descent. We move in the direction that decreases our loss the most. Gradient refers to the slope of the curve at any point.

# For example, let’s say we are trying to find the intercept for a line. We currently have a guess of 10 for the intercept. At the point of 10 on the curve, the slope is downward. Therefore, if we increase the intercept, we should be lowering the loss. So we follow the gradient downwards.


# We derive these gradients using calculus. It is not crucial to understand how we arrive at the gradient equation. To find the gradient of loss as intercept changes, the formula comes out to be:

# \frac{2}{N}\sum_{i=1}^{N}-(y_i-(mx_i+b)) 
# N
# 2
# ​	  
# i=1
# ∑
# N
# ​	 −(y 
# i
# ​	 −(mx 
# i
# ​	 +b))
# N is the number of points we have in our dataset
# m is the current gradient guess
# b is the current intercept guess
# Basically:

# we find the sum of y_value - (m*x_value + b) for all the y_values and x_values we have
# and then we multiply the sum by a factor of -2/N. N is the number of points we have.
# Instructions
# 1.
# Define a function called get_gradient_at_b() that takes in a set of x values, x, a set of y values, y, a slope m, and an intercept value b.

# For now, have it return b, unchanged.

# In Python, a function is defined using the def keyword:

# def get_gradient_at_b(x, y, m, b):
#   # We will be adding code here next
#   return b
# 2.
# In the get_gradient_at_b() function, we want to go through all of the x values and all of the y values and compute (y - (m*x+b)) for each of them.

# Create a variable called diff that has the sum of all of these values.

# Instead of returning b from the get_gradient_at_b() function, return diff.

# First, to recreate this formula with Python:

# (y-(mx+b))(y−(mx+b))
# We can do (y - (m*x+b)).

# To recreate this formula:

# \sum_{i=1}^{N}(y_i-(mx_i+b)) 
# i=1
# ∑
# N
# ​	 (y 
# i
# ​	 −(mx 
# i
# ​	 +b))
# We can do:

# # Create a variable called diff
# diff = 0

# for i in range(0, len(x)):
#   y_val = y[i]
#   x_val = x[i]
#   diff += (y_val - ((m * x_val) + b))
# So your function should now look like:

# def get_gradient_at_b(x, y, m, b):
#   # Create a variable called diff
#   diff = 0
#   N = len(x)
#   for i in range(0, len(x)):
#     y_val = y[i]
#     x_val = x[i]
#     diff += (y_val - ((m * x_val) + b))
#   return diff
# 3.
# Still in the get_gradient_at_b() function, define a variable called b_gradient and set it equal to the -2/N multiplied by diff.

# Note: N is the number of points, i.e. the length of the x list or the y list.

# Instead of returning diff, return b_gradient.

# The len() function returns the number of items in an object:

# N = len(x)
# Your code should look like:

# def get_gradient_at_b(x, y, m, b):
#   diff = 0
#   # N is the number of points
#   N = len(x)
#   for i in range(0, len(x)):
#     y_val = y[i]
#     x_val = x[i]
#     diff += (y_val - ((m * x_val) + b))
#   # Define b_gradient
#   b_gradient = -2/N * diff
#   return b_gradient

def get_gradient_at_b(x, y, m, b):
  diff = 0
  for i in range(len(x)):
    diff += (y[i] - ((m * x[i]) + b))
  b_gradient = (-2 / len(x)) * diff
  return b_gradient
# LINEAR REGRESSION
# Gradient Descent for Slope
# We have a function to find the gradient of b at every point. To find the m gradient, or the way the loss changes as the slope of our line changes, we can use this formula:

# \frac{2}{N}\sum_{i=1}^{N}-x_i(y_i-(mx_i+b)) 
# N
# 2
# ​	  
# i=1
# ∑
# N
# ​	 −x 
# i
# ​	 (y 
# i
# ​	 −(mx 
# i
# ​	 +b))
# Once more:

# N is the number of points you have in your dataset
# m is the current gradient guess
# b is the current intercept guess
# To find the m gradient:

# we find the sum of x_value * (y_value - (m*x_value + b)) for all the y_values and x_values we have
# and then we multiply the sum by a factor of -2/N. N is the number of points we have.
# Once we have a way to calculate both the m gradient and the b gradient, we’ll be able to follow both of those gradients downwards to the point of lowest loss for both the m value and the b value. Then, we’ll have the best m and the best b to fit our data!

# Instructions
# 1.
# Define a function called get_gradient_at_m() that takes in a set of x values, x, a set of y values, y, a slope m, and an intercept value b.

# For now, have it return m.

# Create a brand new function here.

# 2.
# In this function, we want to go through all of the x values and all of the y values and compute x*(y - (m*x+b)) for each of them.

# Create a variable called diff that has the sum of all of these values, and return it from the function.

# 3.
# Define a variable called m_gradient and set it equal to the -2/N multiplied by diff.

# Instead of returning diff, return m_gradient.

def get_gradient_at_b(x, y, m, b):
    diff = 0
    N = len(x)
    for i in range(N):
      y_val = y[i]
      x_val = x[i]
      diff += (y_val - ((m * x_val) + b))
    b_gradient = -2/N * diff
    return b_gradient
  
def get_gradient_at_m(x, y, m, b):
    diff = 0
    N = len(x)
    for i in range(N):
      y_val = y[i]
      x_val = x[i]
      diff += x_val * (y_val - ((m * x_val) + b))
    m_gradient = -2/N * diff
    return m_gradient
  
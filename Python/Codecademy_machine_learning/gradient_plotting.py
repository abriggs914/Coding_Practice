# LINEAR REGRESSION
# Put it Together II
# At each step, we know how to calculate the gradient and move in that direction with a step size proportional to our learning rate. Now, we want to make these steps until we reach convergence.

# Instructions
# 1.
# We have all of the functions we have defined throughout the lesson.

# Now, let’s create a function called gradient_descent() that takes in x, y, learning_rate, and a num_iterations.

# For now, return [-1,-1].

# 2.
# In the function gradient_descent(), create variables b and m and set them both to zero for our initial guess.

# Return b and m from the function.

# 3.
# Update your step_gradient() function to take in the parameter learning_rate (as the last parameter) and replace the 0.01s in the calculations of b_gradient and m_gradient with learning_rate.

# Your b_gradient should now be calculated like:

# b = b_current - (learning_rate * b_gradient)
# 4.
# Let’s go back and finish the gradient_descent() function.

# Create a loop that runs num_iterations times. At each step, it should:

# Call step_gradient() with b, m, x, y, and learning_rate
# Update the values of b and m with the values step_gradient() returns.
# 5.
# Outside of the function, uncomment the line that calls gradient_descent on months and revenue, with a learning rate of 0.01 and 1000 iterations.

# It stores the results in variables called b and m.

# 6.
# Uncomment the lines that will plot the result to the browser.

import codecademylib3_seaborn
import matplotlib.pyplot as plt

def get_gradient_at_b(x, y, b, m):
  N = len(x)
  diff = 0
  for i in range(N):
    x_val = x[i]
    y_val = y[i]
    diff += (y_val - ((m * x_val) + b))
  b_gradient = -(2/N) * diff  
  return b_gradient

def get_gradient_at_m(x, y, b, m):
  N = len(x)
  diff = 0
  for i in range(N):
      x_val = x[i]
      y_val = y[i]
      diff += x_val * (y_val - ((m * x_val) + b))
  m_gradient = -(2/N) * diff  
  return m_gradient

#Your step_gradient function here
def step_gradient(b_current, m_current, x, y, learning_rate):
    b_gradient = get_gradient_at_b(x, y, b_current, m_current)
    m_gradient = get_gradient_at_m(x, y, b_current, m_current)
    b = b_current - (learning_rate * b_gradient)
    m = m_current - (learning_rate * m_gradient)
    return [b, m]
  
#Your gradient_descent function here:  
def gradient_descent(x, y, learning_rate, num_iterations):
  b = 0
  m = 0
  for i in range(num_iterations):
    b, m = step_gradient(b, m, x, y, learning_rate)
  return (b, m)

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
revenue = [52, 74, 79, 95, 115, 110, 129, 126, 147, 146, 156, 184]

#Uncomment the line below to run your gradient_descent function
b, m = gradient_descent(months, revenue, 0.01, 1000)

#Uncomment the lines below to see the line you've settled upon!
y = [m*x + b for x in months]

plt.plot(months, revenue, "o")
plt.plot(months, y)

plt.show()
# LINEAR REGRESSION
# Scikit-Learn
# Congratulations! You’ve now built a linear regression algorithm from scratch.

# Luckily, we don’t have to do this every time we want to use linear regression. We can use Python’s scikit-learn library. Scikit-learn, or sklearn, is used specifically for Machine Learning. Inside the linear_model module, there is a LinearRegression() function we can use:

# from sklearn.linear_model import LinearRegression
# You can first create a LinearRegression model, and then fit it to your x and y data:

# line_fitter = LinearRegression()
# line_fitter.fit(X, y)
# The .fit() method gives the model two variables that are useful to us:

# the line_fitter.coef_, which contains the slope
# the line_fitter.intercept_, which contains the intercept
# We can also use the .predict() function to pass in x-values and receive the y-values that this line would predict:

# y_predicted = line_fitter.predict(X)
# Note: the num_iterations and the learning_rate that you learned about in your own implementation have default values within scikit-learn, so you don’t need to worry about setting them specifically!

# Instructions
# 1.
# We have imported a dataset of soup sales data vs temperature.

# Run the code to see the scatterplot. Can you envision the line that would fit this data?

# 2.
# Create an sklearn linear regression model and call it line_fitter.

# We have imported the sklearn LinearRegression() function that creates a model. Call this function and assign the result to line_fitter.

# 3.
# Fit the line_fitter object to temperature and sales.

# You can use the .fit() method of line_fitter. Just pass in temperature and sales as the parameters.

# 4.
# Create a list called sales_predict that is the predicted sales values that line_fitter would generate from the temperature list.

# You can use the .predict() method of line_fitter. Pass in temperature as the parameter, and call the result sales_predict.

# 5.
# Plot sales_predict against temperature as a line, on the same plot as the scatterplot.

# You can use this syntax to plot the line:

# plt.plot(temperature, sales_predict)
# Make sure you call it before the call to plt.show(), so that all of the data will be plotted on the same graph.

import codecademylib3_seaborn
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

temperature = np.array(range(60, 100, 2))
temperature = temperature.reshape(-1, 1)
sales = [65, 58, 46, 45, 44, 42, 40, 40, 36, 38, 38, 28, 30, 22, 27, 25, 25, 20, 15, 5]

line_fitter = LinearRegression()
line_fitter.fit(temperature, sales)
sales_predict = line_fitter.predict(temperature)

plt.plot(temperature, sales, 'o')
plt.plot(temperature, sales_predict)

plt.show()
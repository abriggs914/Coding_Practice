#import codecademylib
import pandas as pd

#WORKING WITH MULTIPLE DATAFRAMES
# Inner Merge II
# It is easy to do this kind of matching for one row, but hard to do it for multiple rows.
# Luckily, Pandas can efficiently do this for the entire table. We use the .merge method.
# The .merge method looks for columns that are common between two DataFrames and then looks for rows where those column’s values are the same. It then combines the matching rows into a single row in a new table.
# We can call the pd.merge method with two tables like this:
# new_df = pd.merge(orders, customers)
# This will match up all of the customer information to the orders that each customer made.
sales = pd.read_csv('sales.csv')
print(sales)
targets = pd.read_csv('targets.csv')
print(targets)

#You are an analyst Cool T-Shirts Inc. You are going to help them analyze some of their sales data.

# There are two DataFrames defined in the file script.py:
# sales contains the monthly revenue for Cool T-Shirts Inc. It has two columns: month and revenue.
# targets contains the goals for monthly revenue for each month. It has two columns: month and target.
# Create a new DataFrame sales_vs_targets which contains the merge of sales and targets.
sales_vs_targets = pd.merge(sales, targets)
print(sales_vs_targets)

#Cool T-Shirts Inc. wants to know the months when they crushed their targets.
#Select the rows from sales_vs_targets where revenue is greater than target. Save these rows to the variable crushing_it.
crushing_it = sales_vs_targets[sales_vs_targets.revenue > sales_vs_targets.target]
print(crushing_it)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#import codecademylib
#import pandas as pd

#In addition to using pd.merge, each DataFrame has its own merge method. For instance, if you wanted to merge orders with customers, you could use:
# new_df = orders.merge(customers)
# This produces the same DataFrame as if we had called pd.merge(orders, customers).
# We generally use this when we are joining more than two DataFrames together because we can chain the commands. The following command would merge orders to customers, and then the resulting DataFrame to products:
# big_df = orders.merge(customers)\
#     .merge(products)

sales = pd.read_csv('sales.csv')
print(sales)
targets = pd.read_csv('targets.csv')
print(targets)

#We have some more data from Cool T-Shirts Inc. The number of mens and womens t-shirts sold per month is in a file called men_women_sales.csv. Load this data into a DataFrame called men_women.
men_women = pd.read_csv('men_women_sales.csv')
print(men_women)

#Merge all three DataFrames (sales, targets, and men_women) into one big DataFrame called all_data.
all_data = men_women.merge(sales).merge(targets)
print(all_data)

#Cool T-Shirts Inc. thinks that they have more revenue in months where they sell more womens t-shirts.
# Select the rows of all_data where:
# revenue is greater than target
# AND
# women is greater than men
# Save your answer to the variable results.
results = all_data[(all_data.revenue > all_data.target) & (all_data.women > all_data.men)]
print(results)





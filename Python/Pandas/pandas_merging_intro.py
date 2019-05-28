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

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#import codecademylib
#import pandas as pd

# WORKING WITH MULTIPLE DATAFRAMES
# Merge on Specific Columns
# In the previous example, the merge function “knew” how to combine tables based on the columns that were the same between two tables. For instance, products and orders both had a column called product_id. This won’t always be true when we want to perform a merge.
# Generally, the products and customers DataFrames would not have the columns product_id or customer_id. Instead, they would both be called id and it would be implied that the id was the product_id for the products table and customer_id for the customers table. They would look like this:
# Customers
# id	customer_name	address	phone_number
# 1	John Smith	123 Main St.	212-123-4567
# 2	Jane Doe	456 Park Ave.	949-867-5309
# 3	Joe Schmo	798 Broadway	112-358-1321
# Products
# id	description	price
# 1	thing-a-ma-jig	5
# 2	whatcha-ma-call-it	10
# 3	doo-hickey	7
# 4	gizmo	3
# **How would this affect our merges?**
# Because the id columns would mean something different in each table, our default merges would be wrong.
# One way that we could address this problem is to use .rename to rename the columns for our merges. In the example below, we will rename the column id to customer_id, so that orders and customers have a common column for the merge.
# pd.merge(
#     orders,
#     customers.rename(columns={'id': 'customer_id'}))

orders = pd.read_csv('orders.csv')
print(orders)
products = pd.read_csv('products.csv')
print(products)

#Merge orders and products using rename. Save your results to the variable orders_products.
orders_products = pd.merge(orders, products.rename(columns = {'id': 'customer_id'}))
print(orders_products)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#import codecademylib
#import pandas as pd

#WORKING WITH MULTIPLE DATAFRAMES
# Merge on Specific Columns II
# In the previous exercise, we learned how to use rename to merge two DataFrames whose columns dont match.
# If we dont want to do that, we have another option. We could use the keywords left_on and right_on to specify which columns we want to perform the merge on. In the example below, the left table is the one that comes first (orders), and the right table is the one that comes second (customers). This syntax says that we should match the customer_id from orders to the id in customers.
# pd.merge(
#     orders,
#     customers,
#     left_on='customer_id',
#     right_on='id')
# If we use this syntax, well end up with two columns called id, one from the first table and one from the second. Pandas wont let you have two columns with the same name, so it will change them to id_x and id_y.
# It will look like this:
# id_x	customer_id	product_id	quantity	timestamp	id_y	customer_name	address	phone_number
# 1	2	3	1	2017-01-01 00:00:00	2	Jane Doe	456 Park Ave	949-867-5309
# 2	2	2	3	2017-01-01 00:00:00	2	Jane Doe	456 Park Ave	949-867-5309
# 3	3	1	1	2017-01-01 00:00:00	3	Joe Schmo	789 Broadway	112-358-1321
# 4	3	2	2	2016-02-01 00:00:00	3	Joe Schmo	789 Broadway	112-358-1321
# 5	3	3	3	2017-02-01 00:00:00	3	Joe Schmo	789 Broadway	112-358-1321
# 6	1	4	2	2017-03-01 00:00:00	1	John Smith	123 Main St.	212-123-4567
# 7	1	1	1	2017-02-02 00:00:00	1	John Smith	123 Main St.	212-123-4567
# 8	1	4	1	2017-02-02 00:00:00	1	John Smith	123 Main St.	212-123-4567
# The new column names id_x and id_y arent very helpful for us when we read the table. We can help make them more useful by using the keyword suffixes. We can provide a list of suffixes to use instead of _x and _y.
# For example, we could use the following code to make the suffixes reflect the table names:
# pd.merge(
#     orders,
#     customers,
#     left_on='customer_id',
#     right_on='id',
#     suffixes=['_order', '_customer']
# )
# The resulting table would look like this:
orders = pd.read_csv('orders.csv')
print(orders)
products = pd.read_csv('products.csv')
print(products)


#Merge orders and products using left_on and right_on. Use the suffixes _orders and _products. Save your results to the variable orders_products.
orders_products = pd.merge(
  orders,
  products,
  left_on='customer_id',
  right_on='id',
  suffixes=['_orders', '_products'])
print(orders_products)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#import codecademylib
#import pandas as pd

#WORKING WITH MULTIPLE DATAFRAMES
#Mismatched Merges
#In our previous examples, there were always matching values when we were performing our merges. What happens when that isnt true?
#Lets imagine that our products table is out of date and is missing the newest product: Product 5. What happens when someone orders it?

orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')
# Weve just released a new product with product_id equal to 5. People are ordering this product, but we havent updated the products table.
# In script.py, youll find two DataFrames: products and orders. Inspect these DataFrames using print.
# Notice that the third order in orders is for the mysterious new product, but that there is no product_id 5 in products.
print(orders)
print(products)

#Merge orders and products and save it to the variable merged_df.
#Inspect merged_df using:
#print(merged_df)
#What happened to order_id 3?
merged_df = pd.merge(orders, products)
print(merged_df)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#import codecademylib
#import pandas as pd

#WORKING WITH MULTIPLE DATAFRAMES
# Outer Merge
# In the previous exercise, we saw that when we merge two DataFrames whose rows don’t match perfectly, we lose the unmatched rows.
# This type of merge (where we only include matching rows) is called an inner merge. There are other types of merges that we can use when we want to keep information from the unmatched rows.
# Suppose that two companies, Company A and Company B have just merged. They each have a list of customers, but they keep slightly different data. Company A has each customer’s name and email. Company B has each customer’s name and phone number. They have some customers in common, but some are different.
# company_a
# name	email
# Sally Sparrow	sally.sparrow@gmail.com
# Peter Grant	pgrant@yahoo.com
# Leslie May	leslie_may@gmail.com
# company_b
# name	phone
# Peter Grant	212-345-6789
# Leslie May	626-987-6543
# Aaron Burr	303-456-7891
# If we wanted to combine the data from both companies without losing the customers who are missing from one of the tables, we could use an Outer Join. An Outer Join would include all rows from both tables, even if they don’t match. Any missing values are filled in with None or nan (which stands for “Not a Number”).
# pd.merge(company_a, company_b, how='outer')
# The resulting table would look like this:

store_a = pd.read_csv('store_a.csv')
print(store_a)
store_b = pd.read_csv('store_b.csv')
print(store_b)

#There are two hardware stores in town: Store A and Store B. Store A’s inventory is in DataFrame store_a and Store B’s inventory is in DataFrame store_b. They have decided to merge into one big Super Store!
#Combine the inventories of Store A and Store B using an outer merge. Save the results to the variable store_a_b_outer.
store_a_b_outer = pd.merge(store_a, store_b, how='outer')
#Display store_a_b_outer using print.
#Which values are nan or None?
#What does that mean?
print(store_a_b_outer)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#import codecademylib
#import pandas as pd

#WORKING WITH MULTIPLE DATAFRAMES
# Left and Right Merge
# Let’s return to the merge of Company A and Company B.
# Left Merge
# Suppose we want to identify which customers are missing phone information. We would want a list of all customers who have email, but don’t have phone.
# We could get this by performing a Left Merge. A Left Merge includes all rows from the first (left) table, but only rows from the second (right) table that match the first table.
# For this command, the order of the arguments matters. If the first DataFrame is company_a and we do a left join, we’ll only end up with rows that appear in company_a.
# By listing company_a first, we get all customers from Company A, and only customers from Company B who are also customers of Company A.
# pd.merge(company_a, company_b, how='left')
# The result would look like this: 
# name	email	phone
# Sally Sparrow	sally.sparrow@gmail.com	None
# Peter Grant	pgrant@yahoo.com	212-345-6789
# Leslie May	leslie_may@gmail.com	626-987-6543
# Now let’s say we want a list of all customers who have phone but no email. We can do this by performing a Right Merge.

# Right Merge
# Right merge is the exact opposite of left merge. Here, the merged table will include all rows from the second (right) table, but only rows from the first (left) table that match the second table.
# By listing company_a first and company_b second, we get all customers from Company B, and only customers from Company A who are also customers of Company B.
# pd.merge(company_a, company_b, how="right")
# The result would look like this: 
# name	email	phone
# Peter Grant	pgrant@yahoo.com	212-345-6789
# Leslie May	leslie_may@gmail.com	626-987-6543
# Aaron Burr	None	303-456-7891

store_a = pd.read_csv('store_a.csv')
print(store_a)
store_b = pd.read_csv('store_b.csv')
print(store_b)

#Let’s return to the two hardware stores, Store A and Store B. They’re not quite sure if they want to merge into a big Super Store just yet.
# Store A wants to find out what products they carry that Store B does not carry. Using a left merge, combine store_a to store_b and save the results to store_a_b_left.
# The items with null in store_b_inventory are carried by Store A, but not Store B.
store_a_b_left = pd.merge(store_a, store_b, how='left')
print(store_a_b_left)

#Now, Store B wants to find out what products they carry that Store A does not carry. Use a left join, to combine the two DataFrames but in the reverse order (i.e., store_b followed by store_a) and save the results to the variable store_b_a_left.
#Which items are not carried by Store A, but are carried by Store B?
store_b_a_left = pd.merge(store_b, store_a, how='left')
print(store_b_a_left)

#Paste the following code into script.py:
#print(store_a_b_left)
#print(store_b_a_left)
#What do you notice about these two DataFrames?
#How are they different?
#How are they the same?
print(store_a_b_left)
print(store_b_a_left)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

#import codecademylib
#import pandas as pd

#WORKING WITH MULTIPLE DATAFRAMES
# Concatenate DataFrames
# Sometimes, a dataset is broken into multiple tables. For instance, data is often split into multiple CSV files so that each download is smaller.
# When we need to reconstruct a single DataFrame from multiple smaller DataFrames, we can use the method pd.concat([df1, df2, df2, ...]). This method only works if all of the columns are the same in all of the DataFrames.
# For instance, suppose that we have two DataFrames:
# df1
# name	email
# Katja Obinger	k.obinger@gmail.com
# Alison Hendrix	alisonH@yahoo.com
# Cosima Niehaus	cosi.niehaus@gmail.com
# Rachel Duncan	rachelduncan@hotmail.com
# df2
# name	email
# Jean Gray	jgray@netscape.net
# Scott Summers	ssummers@gmail.com
# Kitty Pryde	kitkat@gmail.com
# Charles Xavier	cxavier@hotmail.com
# If we want to combine these two DataFrames, we can use the following command:
# pd.concat([df1, df2])
# That would result in the following DataFrame:
# name	email
# Katja Obinger	k.obinger@gmail.com
# Alison Hendrix	alisonH@yahoo.com
# Cosima Niehaus	cosi.niehaus@gmail.com
# Rachel Duncan	rachelduncan@hotmail.com
# Jean Gray	jgray@netscape.net
# Scott Summers	ssummers@gmail.com
# Kitty Pryde	kitkat@gmail.com
# Charles Xavier	cxavier@hotmail.com
# Instructions

bakery = pd.read_csv('bakery.csv')
print(bakery)
ice_cream = pd.read_csv('ice_cream.csv')
print(ice_cream)
# An ice cream parlor and a bakery have decided to merge.
# The bakery’s menu is stored in the DataFrame bakery, and the ice cream parlor’s menu is stored in DataFrame ice_cream.
# Create their new menu by concatenating the two DataFrames into a DataFrame called menu.
menu = pd.concat([bakery, ice_cream])
print(menu)




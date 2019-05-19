#AGGREGATES IN PANDAS
#Calculating Column Statistics
#In the previous lesson, you learned how to perform operations on each value in a column using apply.
#In this exercise, you will learn how to combine all of the values from a column for a single calculation.
#Some examples of this type of calculation include:
#The DataFrame customers contains the names and ages of all of your customers. You want to find the median age:
#print(customers.age)
#>> [23, 25, 31, 35, 35, 46, 62]
#print(customers.age.median())
#>> 35
#The DataFrame shipments contains address information for all shipments that you’ve sent out in the past year. You want to know how many different states you have shipped to (and how many shipments went to the same state).
#print(shipments.state)
#>> ['CA', 'CA', 'CA', 'CA', 'NY', 'NY', 'NJ', 'NJ', 'NJ', 'NJ', 'NJ', 'NJ', 'NJ']
#print(shipments.state.nunique())
#>> 3
#The DataFrame inventory contains a list of types of t-shirts that your company makes. You want a list of the colors that your shirts come in.
#print(inventory.color)
#>> ['blue', 'blue', 'blue', 'blue', 'blue', 'green', 'green', 'orange', 'orange', 'orange']
#print(inventory.color.unique())
#>> ['blue', 'green', 'orange']
#The general syntax for these calculations is:
#df.column_name.command()
#The following table summarizes some common commands:
#Command	Description
#mean	Average of all values in column
#std	Standard deviation
#median	Median
#max	Maximum value in column
#min	Minimum value in column
#count	Number of values in column
#nunique	Number of unique values in column
#unique	List of unique values in column

#import codecademylib
import pandas as pd

orders = pd.read_csv('orders.csv')

#Once more, we’ll revisit our orders from ShoeFly.com. Our new batch of orders is in the DataFrame orders. Examine the first 10 rows using the following code:
#print(orders.head(10))
print(orders.head(10))

#Our finance department wants to know the price of the most expensive pair of shoes purchased. Save your answer to the variable most_expensive.
most_expensive = orders.price.max()

#Our fashion department wants to know how many different colors of shoes we are selling. Save your answer to the variable num_colors.
num_colors = orders.shoe_color.nunique()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#AGGREGATES IN PANDAS
#Calculating Aggregate Functions I
#When we have a bunch of data, we often want to calculate aggregate statistics (mean, standard deviation, median, percentiles, etc.) over certain subsets of the data.
#Suppose we have a grade book with columns student, assignment_name, and grade. The first few lines look like this:
#student	assignment_name	grade
#Amy	Assignment 1	75
#Amy	Assignment 2	35
#Bob	Assignment 1	99
#Bob	Assignment 2	35
#…		
#We want to get an average grade for each student across all assignments. We could do some sort of loop, but Pandas gives us a much easier option: the method .groupby.
#For this example, we’d use the following command:
#grades = df.groupby('student').grade.mean()
#The output might look something like this:
#student	grade
#Amy	80
#Bob	90
#Chris	75
#…	
#In general, we use the following syntax to calculate aggregates:
#df.groupby('column1').column2.measurement()
#where:
#column1 is the column that we want to group by ('student' in our example)
#column2 is the column that we want to perform a measurement on (grade in our example)
#measurement is the measurement function we want to apply (mean in our example)
orders = pd.read_csv('orders.csv')
print(orders)

#Let’s return to our orders data from ShoeFly.com.
#In the previous exercise, our finance department wanted to know the most expensive shoe that we sold.
#Now, they want to know the most expensive shoe for each shoe_type (i.e., the most expensive boot, the most expensive ballet flat, etc.).
#Save your answer to the variable pricey_shoes.
pricey_shoes = orders.groupby('shoe_type').price.max()
print(pricey_shoes)
print(type(pricey_shoes))

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#AGGREGATES IN PANDAS
#Calculating Aggregate Functions II
#After using groupby, we often need to clean our resulting data.
#As we saw in the previous exercise, the groupby function creates a new Series, not a DataFrame. For our ShoeFly.com example, the indices of the Series were different values of shoe_type, and the name property was price.
#Usually, wed prefer that those indices were actually a column. In order to get that, we can use reset_index(). This will transform our Series into a DataFrame and move the indices into their own column.
#Generally, youll always see a groupby statement followed by reset_index:
#df.groupby('column1').column2.measurement()
#    .reset_index()
#When we use groupby, we often want to rename the column we get as a result. For example, suppose we have a DataFrame teas containing data on types of tea:
#id	tea	category	caffeine	price
#0	earl grey	black	38	3
#1	english breakfast	black	41	3
#2	irish breakfast	black	37	2.5
#3	jasmine	green	23	4.5
#4	matcha	green	48	5
#5	camomile	herbal	0	3
#				
#We want to find the number of each category of tea we sell. We can use:
#teas_counts = teas.groupby('category').id.count().reset_index()
#This yields a DataFrame that looks like:
#category	id
#0	black	3
#1	green	4
#2	herbal	8
#3	white	2
#		
#The new column contains the counts of each category of tea sold. We have 3 black teas, 4 green teas, and so on. However, this column is called id because we used the id column of teas to calculate the counts. We actually want to call this column counts. Remember that we can rename columns:
#teas_counts = teas_counts.rename(columns={"id": "counts"})
#Our DataFrame now looks like:
#category	counts
#0	black	3
#1	green	4
#2	herbal	8
#3	white	2

orders = pd.read_csv('orders.csv')

#Modify your code from the previous exercise so that it ends with reset_index, which will change pricey_shoes into a DataFrame.
pricey_shoes = orders.groupby('shoe_type').price.max().reset_index()
#Examine the object that you’ve just created using the following code:
print(pricey_shoes)

#Now, what type of object is pricey_shoes?
#Enter the following code to check:
print(type(pricey_shoes))




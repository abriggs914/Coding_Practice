#CREATING, LOADING, AND SELECTING DATA WITH PANDAS
#Review
#You’ve completed the lesson! You’ve just learned the basics of working with a single table in Pandas, including:
#Create a table from scratch
#Loading data from another file
#Selecting certain rows or columns of a table
#Let’s practice what you’ve learned.

#import codecademylib
import pandas as pd

#In this example, you’ll be the data analyst for ShoeFly.com, a fictional online shoe store. You’ve seen this data; now it’s your turn to work with it!
#Load the data from shoefly.csv into the variable orders.
orders = pd.read_csv('shoefly.csv')

#Inspect the first 5 lines of the data.
print(orders.iloc[:5])

#Your marketing department wants to send out an email blast to everyone who ordered shoes!
#Select all of the email addresses from the column email and save them to a variable called emails.
emails = orders.email

#Frances Palmer claims that her order was wrong. What did Frances Palmer order?
#Use logic to select that row of orders and save it to the variable frances_palmer.
frances_palmer = orders[(orders.first_name == 'Frances') & (orders.last_name == 'Palmer')]

#We need some customer reviews for our comfortable shoes. Select all orders for shoe_type: clogs, boots, and ballet flats and save them to the variable comfy_shoes.
comfy_shoes = orders[orders.shoe_type.isin(['clogs','boots','ballet flats'])]


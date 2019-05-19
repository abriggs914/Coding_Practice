#MODIFYING DATAFRAMES
#Review
#Great job! In this lesson, you learned how to modify an existing DataFrame. Some of the skills youve learned include:
#Adding columns to a DataFrame
#Using lambda functions to calculate complex quantities
#Renaming columns
#Lets practice what you just learned!

#import codecademylib
import pandas as pd

orders = pd.read_csv('shoefly_1.csv')

#Once more, youll be the data analyst for ShoeFly.com, a fictional online shoe store.
#More messy order data has been loaded into the variable orders. Examine the first 5 rows of the data using print and head.
print(orders.head())

#Many of our customers want to buy vegan shoes (shoes made from materials that do not come from animals). Add a new column called shoe_source, which is vegan if the materials is not leather and animal otherwise.
#mylambda = lambda x: 'animal' if x == 'leather' else 'vegan'
orders['shoe_source'] = orders.shoe_material.apply(lambda x: 'animal' if x == 'leather' else 'vegan')

#Our marketing department wants to send out an email to each customer. Using the columns last_name and gender create a column called salutation which contains Dear Mr. <last_name> for men and Dear Ms. <last_name> for women.
#Here are some examples:
#last_name	gender	salutation
#Smith	Male	Dear Mr. Smith
#Jones	Female	Dear Ms. Jones
orders['salutation'] = orders.apply(lambda x:
                                   'Dear Mr. ' + str(x.last_name) if x.gender == 'male' else 'Dear Ms. ' + str(x.last_name),
                                   axis = 1)

print(orders)




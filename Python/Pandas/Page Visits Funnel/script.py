#import codecademylib
import pandas as pd

#DATA ANALYSIS WITH PANDAS
# Page Visits Funnel
# Cool T-Shirts Inc. has asked you to analyze data on visits to their website. Your job is to build a funnel, which is a description of how many people continue to the next step of a multi-step process.
# In this case, our funnel is going to describe the following process:
# A user visits CoolTShirts.com
# A user adds a t-shirt to their cart
# A user clicks checkout
# A user actually purchases a t-shirt
# If you get stuck during this project or would like to see an experienced developer work through it, click Get Help to see a project walkthrough video.

visits = pd.read_csv('visits.csv',
                     parse_dates=[1])
cart = pd.read_csv('cart.csv',
                   parse_dates=[1])
checkout = pd.read_csv('checkout.csv',
                       parse_dates=[1])
purchase = pd.read_csv('purchase.csv',
                       parse_dates=[1])

#Inspect the DataFrames using print and head:
#visits lists all of the users who have visited the website
#cart lists all of the users who have added a t-shirt to their cart
#checkout lists all of the users who have started the checkout
#purchase lists all of the users who have purchased a t-shirt
print(visits.head())
print(cart.head())
print(checkout.head())
print(purchase.head())

#Combine visits and cart using a left merge.
#If we want to combine df1 and df2 with a left merge, we use the following code:
# pd.merge(df1, df2, how='left')
# OR
# df1.merge(df2, how='left')
visits_cart = pd.merge(visits, cart, how='left')
print(visits_cart)

#How long is your merged DataFrame?
#Use len to find out the number of rows in a DataFrame.
print(len(visits_cart))

#How many of the timestamps are null for the column cart_time?
#What do these null rows mean?
#You can select null rows from column1 of a DataFrame df using the following code:
#df[df.column1.isnull()]
print(len(visits_cart[visits_cart.cart_time.isnull()]))

#What percent of users who visited Cool T-Shirts Inc. ended up not placing a t-shirt in their cart?
#Note: To calculate percentages, it will be helpful to turn either the numerator or the denominator into a float, by using float(), with the number to convert passed in as input. Otherwise, Python will use integer division, which truncates decimal points.
#If a row of your merged DataFrame has cart_time equal to null, then that user visited the website, but did not place a t-shirt in their cart.
visited_len = len(visits)
cart_len = len(cart)
print(float(cart_len) / float(visited_len))

visited_len_1 = len(visits_cart)
cart_len_1 =  visited_len_1 - len(visits_cart[visits_cart.cart_time.isnull()])
print('What percent of users who visited Cool T-Shirts Inc. ended up not placing a t-shirt in their cart?\n\t' + str( float(float(cart_len_1) / float(visited_len_1))))

#Repeat the left merge for cart and checkout and count null values. What percentage of users put items in their cart, but did not proceed to checkout?
#You can find the percentage of users who put items in their cart but did not proceed to checkout by counting the null values of checkout_time and comparing it to the total number of users who put items in their cart.
cart_checkout = pd.merge(cart, checkout, how='left')

cart_len = len(cart_checkout)
checkout_len =  cart_len_1 - len(cart_checkout[cart_checkout.checkout_time.isnull()])
print('What percentage of users put items in their cart, but did not proceed to checkout?\n\t' + str(float(float(cart_len) / float(checkout_len))))

#Merge all four steps of the funnel, in order, using a series of left merges. Save the results to the variable all_data.
#Examine the result using print and head.
#df1.merge(df2, how='left')\
   #.merge(df3, how='left')
#all_data = visits_cart.merge(cart_checkout, how='left')
all_data = visits.merge(cart, how='left').merge(checkout, how='left').merge(purchase, how='left')
print(all_data.head())

#What percentage of users proceeded to checkout, but did not purchase a t-shirt?
visited = len(all_data[~all_data.visit_time.isnull()])
put_in_cart = len(all_data[~all_data.cart_time.isnull()])
got_to_checkout = len(all_data[~all_data.checkout_time.isnull()])
purchased_time = len(all_data[~all_data.purchase_time.isnull()])
not_purchased_item = len(all_data[~all_data.checkout_time.isnull() & all_data.purchase_time.isnull()])
print('put_in_cart: ' + str(put_in_cart))
print('got_to_checkout: ' + str(got_to_checkout))
print('purchased_time: ' + str(purchased_time))

print('got to checkout: ' + str(got_to_checkout) + ', did not purchase item & got to checkout: ' + str(not_purchased_item) + '\n')
print('What percentage of users proceeded to checkout, but did not purchase a t-shirt?\n\t' + str(float(float(not_purchased_item) / float(got_to_checkout))))

#Which step of the funnel is weakest (i.e., has the highest percentage of users not completing it)?
#How might Cool T-Shirts Inc. change their website to fix this problem?
print('Which step of the funnel is weakest (i.e., has the highest percentage of users not completing it)?')
visit_to_cart = float(float(put_in_cart) / float(visited))
print('Percentage that got from visit to cart: ' + str(visit_to_cart))
cart_to_checkout = float(float(got_to_checkout) / float(put_in_cart))
print('Percentage that got from cart to checkout: ' + str(cart_to_checkout))
checkout_to_purchase = float(float(purchased_time) / float(got_to_checkout))
print('Percentage that got from checkout to purchase: ' + str(checkout_to_purchase))
vals = {'visit_to_cart' : visit_to_cart, 'cart_to_checkout' : cart_to_checkout, 'checkout_to_purchase' : checkout_to_purchase, }
min_val = None
for key in vals:
  if min_val is None or vals[key] < min_val[1]:
    min_val = (key, vals[key])
  print(min_val[0], min_val[1], key, vals[key])
print('\nThe weakest funnel is {0} with a percentage of {1}\n'.format(min_val[0], min_val[1]))

#Using the giant merged DataFrame all_data that you created, let’s calculate the average time from initial visit to final purchase. Start by adding the following column to your DataFrame:
#all_data['time_to_purchase'] = \
#    all_data.purchase_time - \
#    all_data.visit_time
all_data['time_to_purchase'] = \
    all_data.purchase_time - \
    all_data.visit_time

#Examine the results using:
#print(all_data.time_to_purchase)
print(all_data.time_to_purchase)

#Calculate the average time to purchase using the following code:
#print(all_data.time_to_purchase.mean())
print(all_data.time_to_purchase.mean())

# print(all_data)
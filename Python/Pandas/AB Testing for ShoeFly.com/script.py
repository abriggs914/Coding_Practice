#DATA ANALYSIS WITH PANDAS
# A/B Testing for ShoeFly.com
# Our favorite online shoe store, ShoeFly.com is performing an A/B Test. They have two different versions of an ad, which they have placed in emails, as well as in banner ads on Facebook, Twitter, and Google. They want to know how the two ads are performing on each of the different platforms on each day of the week. Help them analyze the data using aggregate measures.
# If you get stuck during this project or would like to see an experienced developer work through it, click “Get Help“ to see a project walkthrough video.

import codecademylib
import pandas as pd

ad_clicks = pd.read_csv('ad_clicks.csv')

#Examine the first few rows of ad_clicks.
#Try pasting the following code:
#print(ad_clicks.head())
print(ad_clicks.head())

#Your manager wants to know which ad platform is getting you the most views.
#How many views (i.e., rows of the table) came from each utm_source?
#Try using the following code:
#ad_clicks.groupby('utm_source')\
#    .user_id.count()\
#    .reset_index()
num_utm_source_views = ad_clicks.groupby('utm_source').user_id.count().reset_index()
print(num_utm_source_views)

#If the column ad_click_timestamp is not null, then someone actually clicked on the ad that was displayed.
#Create a new column called is_click, which is True if ad_click_timestamp is not null and False otherwise.
#ad_clicks['is_click'] = ad_clicks.apply(lambda x:
#                                       True if #~x.ad_click_timestamp.isnull() else False)
#Try using the following code:
#ad_clicks['is_click'] = ~ad_clicks\
#   .ad_click_timestamp.isnull()
#The ~ is a NOT operator, and isnull() tests whether or not the value of ad_click_timestamp is null.
ad_clicks['is_click'] = ~ad_clicks\
   .ad_click_timestamp.isnull()
print(ad_clicks)

#We want to know the percent of people who clicked on ads from each utm_source.
#Start by grouping by utm_source and is_click and counting the number of user_id‘s in each of those groups. Save your answer to the variable clicks_by_source.
#Try using the following code:
#clicks_by_source = ad_clicks\
#   .groupby(['utm_source',
#             'is_click'])\
#   .user_id.count()\
#   .reset_index()
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()
print(clicks_by_source)

#Now let’s pivot the data so that the columns are is_click (either True or False), the index is utm_source, and the values are user_id.
#Save your results to the variable clicks_pivot.
#Try using the following code:
#clicks_pivot = clicks_by_source\
#   .pivot(index='utm_source',
#          columns='is_click',
#          values='user_id')\
#   .reset_index()
clicks_pivot = clicks_by_source.pivot(columns = 'is_click', index = 'utm_source', values = 'user_id')
print(clicks_pivot)

#Create a new column in clicks_pivot called percent_clicked which is equal to the percent of users who clicked on the ad from each utm_source.
#Was there a difference in click rates for each source?
#Try the following code:
#clicks_pivot['percent_clicked'] = \
#   clicks_pivot[True] / \
#   (clicks_pivot[True] + 
#    clicks_pivot[False])
#clicks_pivot[True] is the number of people who clicked (because is_click was True for those users)
#clicks_pivot[False] is the number of people who did not click (because is_click was False for those users)
#So, the percent of people who clicked would be (Total Who Clicked) / (Total Who Clicked + Total Who Did Not Click)
clicks_pivot['percent_clicked'] = clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False])
print(clicks_pivot)

#Analyzing an A/B Test
#The column experimental_group tells us whether the user was shown Ad A or Ad B.
#Were approximately the same number of people shown both adds?
#We can group by experimental_group and count the number of users.
print(ad_clicks.groupby('experimental_group').user_id.count().reset_index())

#Using the column is_click that we defined earlier, check to see if a greater percentage of users clicked on Ad A or Ad B.
#Group by both experimental_group and is_click and count the number of user_id‘s.
#You might want to use a pivot table like we did for the utm_source exercises.
ad_clicks_pivot = ad_clicks.groupby(['experimental_group', 'is_click']) \
.user_id.count().reset_index() \
.pivot(columns = 'is_click', index = 'experimental_group', values = 'user_id')
print(ad_clicks_pivot)

#The Product Manager for the A/B test thinks that the clicks might have changed by day of the week.
#Start by creating two DataFrames: a_clicks and b_clicks, which contain only the results for A group and B group, respectively.
#To create a_clicks:
#a_clicks = ad_clicks[
#   ad_clicks.experimental_group
#   == 'A']
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

print(a_clicks)
print(b_clicks)

#For each group (a_clicks and b_clicks), calculate the percent of users who clicked on the ad by day.
#First, group by is_click and day. Next, pivot the data so that the columns are based on is_click. Finally, calculate the percent of people who clicked on the ad.
a_clicks_percent_per_day = a_clicks.groupby(['is_click', 'day']).user_id.count().reset_index().pivot(columns = 'is_click', index = 'day', values = 'user_id')
a_clicks_percent_per_day['percent_per_day'] = a_clicks_percent_per_day[True] / (a_clicks_percent_per_day[True] + a_clicks_percent_per_day[False])

b_clicks_percent_per_day = b_clicks.groupby(['is_click', 'day']).user_id.count().reset_index().pivot(columns = 'is_click', index = 'day', values = 'user_id')
b_clicks_percent_per_day['percent_per_day'] = b_clicks_percent_per_day[True] / (b_clicks_percent_per_day[True] + b_clicks_percent_per_day[False])



print(a_clicks_percent_per_day)
print(b_clicks_percent_per_day)

#Compare the results for A and B. What happened over the course of the week?
#Do you recommend that your company use Ad A or Ad B?

#Ad A I believe, it has the best overall success rate


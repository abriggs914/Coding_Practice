# Tennis Ace
# Overview
# This project is slightly different than others you have encountered thus far on Codecademy. Instead of a step-by-step tutorial, this project contains a series of open-ended requirements which describe the project you’ll be building. There are many possible ways to correctly fulfill all of these requirements, and you should expect to use the internet, Codecademy, and other resources when you encounter a problem that you cannot easily solve.

# Project Goals
# You will create a linear regression model that predicts the outcome for a tennis player based on their playing habits. By analyzing and modeling the Association of Tennis Professionals (ATP) data, you will determine what it takes to be one of the best tennis players in the world.

# Setup Instructions
# If you choose to do this project on your computer instead of Codecademy, you can download what you’ll need by clicking the “Download” button below. If you need help setting up your computer, be sure to check out our setup guide.

# Tasks
# 8/8 Complete
# Mark the tasks as complete by checking them off
# Prerequisites
# 1.
# In order to complete this project, you should have completed the Linear Regression and Multiple Linear Regression lessons in the Machine Learning Course.

# Project Requirements
# 2.
# “Game, Set, Match!”

# No three words are sweeter to hear as a tennis player than those, which indicate that a player has beaten their opponent. While you can head down to your nearest court and aim to overcome your challenger across the net without much practice, a league of professionals spends day and night, month after month practicing to be among the best in the world. Today you will put your linear regression knowledge to the test to better understand what it takes to be an all-star tennis player.

# Provided in tennis_stats.csv is data from the men’s professional tennis league, which is called the ATP (Association of Tennis Professionals). Data from the top 1500 ranked players in the ATP over the span of 2009 to 2017 are provided in file. The statistics recorded for each player in each year include service game (offensive) statistics, return game (defensive) statistics and outcomes. Load the csv into a DataFrame and investigate it to gain familiarity with the data.

# Open the hint for more information about each column of the dataset.


# Hint
# The ATP men’s tennis dataset includes a wide array of tennis statistics, which are described below:

# Identifying Data
# Player: name of the tennis player
# Year: year data was recorded
# Service Game Columns (Offensive)
# Aces: number of serves by the player where the receiver does not touch the ball
# DoubleFaults: number of times player missed both first and second serve attempts
# FirstServe: % of first-serve attempts made
# FirstServePointsWon: % of first-serve attempt points won by the player
# SecondServePointsWon: % of second-serve attempt points won by the player
# BreakPointsFaced: number of times where the receiver could have won service game of the player
# BreakPointsSaved: % of the time the player was able to stop the receiver from winning service game when they had the chance
# ServiceGamesPlayed: total number of games where the player served
# ServiceGamesWon: total number of games where the player served and won
# TotalServicePointsWon: % of points in games where the player served that they won
# Return Game Columns (Defensive)
# FirstServeReturnPointsWon: % of opponents first-serve points the player was able to win
# SecondServeReturnPointsWon: % of opponents second-serve points the player was able to win
# BreakPointsOpportunities: number of times where the player could have won the service game of the opponent
# BreakPointsConverted: % of the time the player was able to win their opponent’s service game when they had the chance
# ReturnGamesPlayed: total number of games where the player’s opponent served
# ReturnGamesWon: total number of games where the player’s opponent served and the player won
# ReturnPointsWon: total number of points where the player’s opponent served and the player won
# TotalPointsWon: % of points won by the player
# Outcomes
# Wins: number of matches won in a year
# Losses: number of matches lost in a year
# Winnings: total winnings in USD($) in a year
# Ranking: ranking at the end of year
# 3.
# Perform exploratory analysis on the data by plotting different features against the different outcomes. What relationships do you find between the features and outcomes? Do any of the features seem to predict the outcomes?


# Hint
# We utilized matplotlib’s .scatter() method to plot different features against different outcomes. Check out the documentation here for a refresher on how to utilize it.

# We found a strong relationship between the BreakPointsOpportunities feature and the Winnings outcome.

# 4.
# Use one feature from the dataset to build a single feature linear regression model on the data. Your model, at this point, should use only one feature and predict one of the outcome columns. Before training the model, split your data into training and test datasets so that you can evaluate your model on the test set. How does your model perform? Plot your model’s predictions on the test set against the actual outcome variable to visualize the performance.


# Hint
# Our first single feature linear regression model used 'FirstServeReturnPointsWon' as our feature and Winnings as our outcome.

# features = data[['FirstServeReturnPointsWon']]
# outcome = data[['Winnings]]
# We utilized scikit-learn’s train_test_split function to split our data into training and test sets:

# features_train, features_test, outcome_train, outcome_test = train_test_split(features, outcome, train_size = 0.8)
# We then created a linear regression model and trained it on the training data:

# model = LinearRegression()
# model.fit(features_train,outcome_train)
# To score the model on the test data, we used our LinearRegression object’s .score() method.

# model.score(features_test,outcome_test)
# We then found the predicted outcome based on our model and plotted it against the actual outcome:

# prediction = model.predict(features_test)
# plt.scatter(outcome_test,prediction, alpha=0.4)
# 5.
# Create a few more linear regression models that use one feature to predict one of the outcomes. Which model that you create is the best?


# Hint
# We found that our best single feature linear regression model came from using 'BreakPointsOpportunities' as the feature to predict 'Winnings'.

# 6.
# Create a few linear regression models that use two features to predict yearly earnings. Which set of two features results in the best model?


# Hint
# We followed the same steps as in the last exercise to create a linear regression model with 'BreakPointsOpportunities' and 'FirstServeReturnPointsWon' as our features to predict 'Winnings'.

# features = data[['BreakPointsOpportunities',
# 'FirstServeReturnPointsWon']]
# outcome = data[['Winnings']]
# 7.
# Create a few linear regression models that use multiple features to predict yearly earnings. Which set of features results in the best model?

# Head to the Codecademy forums and share your set of features that resulted in the highest test score for predicting your outcome. What features are most important for being a successful tennis player?


# Hint
# We created a linear regression model with the below features to predict 'Winnings':

# features = players[['FirstServe','FirstServePointsWon','FirstServeReturnPointsWon',
# 'SecondServePointsWon','SecondServeReturnPointsWon','Aces',
# 'BreakPointsConverted','BreakPointsFaced','BreakPointsOpportunities',
# 'BreakPointsSaved','DoubleFaults','ReturnGamesPlayed','ReturnGamesWon',
# 'ReturnPointsWon','ServiceGamesPlayed','ServiceGamesWon','TotalPointsWon',
# 'TotalServicePointsWon']]
# outcome = players[['Winnings']]
# Solution
# 8.
# Great work! Visit our forums to compare your project to our sample solution code. You can also learn how to host your own solution on GitHub so you can share it with other learners! Your solution might look different from ours, and that’s okay! There are multiple ways to solve these projects, and you’ll learn more by seeing others’ code.

import codecademylib3_seaborn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# load and investigate the data here:

df = pd.read_csv("tennis_stats.csv")
print(df.head())

print("column names:", df.columns)
players = df[["Player"]]
print("players:\n", players)


# perform exploratory analysis here:

def show_scatters():
  variables = ["Year", "Aces", "DoubleFaults", "FirstServe", "FirstServePointsWon", "SecondServePointsWon", "BreakPointsFaced", "BreakPointsSaved", "ServiceGamesPlayed", "ServiceGamesWon", "TotalServicePointsWon", "FirstServeReturnPointsWon", "SecondServeReturnPointsWon", "BreakPointsOpportunities", "BreakPointsConverted", "ReturnGamesPlayed", "ReturnGamesWon", "ReturnPointsWon", "TotalPointsWon"]

  outcomes = ["Wins", "Losses", "Winnings", "Ranking"]

  for outcome in outcomes:
    for var in variables:
      plt.clf()
      plt.scatter(df[[outcome]], df[[var]], alpha=0.4)
      plt.ylabel(var)
      plt.xlabel(outcome)
      plt.title(outcome + " vs " + var)
      plt.show()

# show_scatters()


## perform single feature linear regressions here:

def single_linear_regression(feature, outcome):
  feature_train, feature_test, outcome_train, outcome_test = train_test_split(df[[feature]], df[[outcome]], train_size = 0.8, test_size = 0.2, random_state=6)

  model = LinearRegression()
  model.fit(feature_train, outcome_train)
  outcome_predictions = model.predict(feature_test)
  # print(outcome + " predict: (" + str(len(outcome_predictions)) + ")\n", outcome_predictions)
  score = model.score(feature_test, outcome_test)
  print("Score:\n", score)
  
  plt.clf()
  plt.scatter(outcome_test, outcome_predictions, alpha=0.4)
  plt.xlabel(feature)
  plt.ylabel(outcome + " predictiona")
  plt.title(feature + " tests VS. " + outcome + " predicitons")
  plt.show()

# Comparing Losses to DoubleFaults
single_linear_regression("DoubleFaults", "Losses")
# losses_train, losses_test, df_train, df_test = train_test_split(df[["Losses"]], df[["DoubleFaults"]], train_size = 0.8, test_size = 0.2, random_state=6)

# l_df_lr = LinearRegression()
# l_df_lr.fit(losses_train, df_train)
# losses_predictions = l_df_lr.predict(losses_test)
# print("losses predict: (" + str(len(losses_predictions)) + ")\n", losses_predictions)
# score = l_df_lr .score(losses_test, df_test)
# print("Score:\n", score)

# plt.clf()
# plt.scatter(df_test, losses_predictions, alpha=0.4)
# plt.xlabel("df_test")
# plt.ylabel("losses_predictiona")
# plt.title("double fault tests VS. losses_predicitons")
# plt.show()

## perform two feature linear regressions here:



# Comparing Wins to Aces
single_linear_regression("Aces", "Wins")

# Comparing Winnings to BreakPointsOpportunities
single_linear_regression("BreakPointsOpportunities", "Winnings")

## perform multiple feature linear regressions here:

def multi_linear_regression(features, outcome):
  features = [features] if not isinstance(features, list) else features
  print("\tMulti Linear Regression\nComparing features:\n-\t" + "\n-\t".join(features) + "\nto outcome:\n-\t" + outcome)
  features_train, features_test, outcome_train, outcome_test = train_test_split(df[features], df[[outcome]], train_size = 0.8, test_size = 0.2, random_state=6)

  model = LinearRegression()
  model.fit(features_train, outcome_train)
  outcome_predictions = model.predict(features_test)
  # print(outcome + " predict: (" + str(len(outcome_predictions)) + ")\n", outcome_predictions)
  score = model.score(features_test, outcome_test)
  print("Score:\n", score)
  
  plt.clf()
  plt.scatter(outcome_test, outcome_predictions, alpha=0.4)
  plt.xlabel(" ".join(features))
  plt.ylabel(outcome + " predictiona")
  plt.title(str(features) + " tests VS. " + outcome + " predicitons")
  plt.show()

multi_linear_regression(["Aces", "TotalServicePointsWon"], "Wins")
multi_linear_regression(["Aces", "BreakPointsOpportunities"], "Wins")
multi_linear_regression(["Aces", "BreakPointsOpportunities", "TotalServicePointsWon",], "Wins")


# predict winnings

winnings_variables = ['FirstServe','FirstServePointsWon','FirstServeReturnPointsWon',
'SecondServePointsWon','SecondServeReturnPointsWon','Aces',
'BreakPointsConverted','BreakPointsFaced','BreakPointsOpportunities',
'BreakPointsSaved','DoubleFaults','ReturnGamesPlayed','ReturnGamesWon',
'ReturnPointsWon','ServiceGamesPlayed','ServiceGamesWon','TotalPointsWon',
'TotalServicePointsWon']

multi_linear_regression(winnings_variables, "Winnings")
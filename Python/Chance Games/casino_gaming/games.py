from game import Game
import chohan
import flip
import war
import roulette

'''
Games of Chance
Overview
This project is slightly different than others you have encountered thus far on Codecademy. Instead of a step-by-step tutorial, this project contains a series of open-ended requirements which describe the project you’ll be building. There are many possible ways to correctly fulfill all of these requirements, and you should expect to use the internet, Codecademy, and other resources when you encounter a problem that you cannot easily solve.

Project Goals
You will work to write several functions that simulate games of chance. Each one of these functions will use a number of parameters, random number generation, conditionals, and return statements.

Setup Instructions
If you choose to do this project on your computer instead of Codecademy, you can download what you’ll need by clicking the “Download” button below. If you need help setting up your computer, be sure to check out our setup guide.

Tasks
9/9Complete
Mark the tasks as complete by checking them off
Prerequisites
1.
In order to complete this project, you should have completed the first 3 sections of the Learn Python 3 Course.

This includes the lessons on Syntax, Functions, and Control Flow.

Project Requirements
2.
The project starts by importing the random module. Every game of chance will involve generating a random number.

For example, to generate a random between 1 and 10 (inclusive) and store it in a variable named num, use this line of code:

num = random.randint(1, 10)
The project also has a variable named money that starts at 100. This represents your current amount of money. In every game of chance, you will be able to bet money. The value of money should change depending on whether you win or lose the game.

At the end of the project, we will have you call several of these functions in a row to see how much money you can win. But it is a good idea to call these functions to test them as you are creating them.

Your functions should have print statements to help the user understand what has happened. For example, in games of chance that involve rolling dice, you should print out the result of those dice rolls. You should also print whether the player won or lost the game, and how much money they won or lost.

3.
Create a function that simulates flipping a coin and calling either "Heads" or "Tails". This function (along with all of the other functions you will write in this project) should have a parameter that represents how much the player is betting on the coin flip.

This function should also have a parameter that lets the player call either "Heads" or "Tails".

If the player wins the game, the function should return the amount that they won. If the player loses the game, the function should return the amount that they lost as a negative number.

Our function definition looked like this:

def coin_flip(guess, bet):
Simulate a coin flip by randomly generating an integer between 1 and 2 (inclusive).

4.
Create a function that simulates playing the game Cho-Han. The function should simulate rolling two dice and adding the results together. The player predicts whether the sum of those dice is odd or even and wins if their prediction is correct.

The function should have a parameter that allows for the player to guess whether the sum of the two dice is "Odd" or "Even". The function should also have a parameter that allows the player to bet an amount of money on the game.

To simulate rolling a dice, generate a random integer between 1 and 6.

5.
Create a function that simulates two players picking a card randomly from a deck of cards. The higher number wins.

Once again, this function should have a parameter that allows a player to bet an amount of money on whether they have a higher card. In this game, there can be a tie. What should be returned if there is a tie?

Check the hint to see an additional challenge for this game.

If the game is a tie, you should return 0. The player doesn’t win or lose any money.

It’s possible that your solution doesn’t really simulate drawing two cards from the same deck. For example, if I draw a 4, it is less likely that you will draw a 4 when you draw a card. As a challenge, think about how you might create a system that knows which cards have already been draw.

Hint: if you’re familiar with lists, this would be a good place to use them!

6.
Create a function that simulates some of the rules of roulette. A random number should be generated that determines which space the ball lands on.

When we wrote our function, we allowed the user to guess "Odd", "Even", or a specific number. We also implemented the logic associated with the 0 and 00 spots. For example, the player loses if they guess either "Odd" or "Even" and either 0 or 00 comes up.

Implement as many rules of roulette as you’d like. Make sure to consider the different ways roulette rewards a win. Check the hint to see more about this!

The amount of money you get back from roulette changes depending on what kind of guess you make. For example, if you bet 1 dollar on a specific number, and you win, you will get 35 dollars back. But if you bet 1 dollar on "Even" and win, you will only get one dollar back. The return value of your function should reflect the different ways roulette rewards its winners.

7.
Call each of your functions at least once. Below is an example of betting $10 on a coin flip and updating the amount of money you have based on whether you win or lose :

money += coin_flip("Heads", 10)
Make sure there are enough print statements so you can understand what games were played, what happened during those games, and the amount of money you have after each game is played.

8.
Expand your program to check for edge cases. What should happen if a player tries to bet more money than they have? What should happen if a player bets a negative amount of money? What should happen if a player calls "heads" or "Heads!" rather than "Heads".

Try to make it very difficult for someone to break your program.

Solution
9.
Compare your program to our sample solution code - remember, that your program might look different from ours (and probably will) and that’s okay!
'''

BORDER = "".join(["#" for i in range(60)])


#Write your game of chance functions here
  
  
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
  
  
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


    
  
'''
#Call your game of chance functions here

print(flip(4, "Tails"))
print(choHan(15, "Odd"))
print(war(10))


# deck = gen_new_deck()
# for i in range(25) :
#   print(war(8, deck))


# print(gen_roulette_board())
# print(roll_roulette())
print("ROULETTE_TEST_1\n" + str(roulette(100, 26)))
print("ROULETTE_TEST_2\n" + str(roulette(100, 0, 1)))
print("ROULETTE_TEST_3\n" + str(roulette(100, 9, 11)))
print("ROULETTE_TEST_4\n" + str(roulette(100, 9, 11, "RED")))
print("ROULETTE_TEST_5\n" + str(roulette(100, 9, 11, "RED", "CORNER")))
print("ROULETTE_TEST_6\n" + str(roulette(100, 9, 11, "RED", "SPLIT")))
print("ROULETTE_TEST_7\n" + str(roulette(100, None, None, None, "COLUMN")))
print("ROULETTE_TEST_8\n" + str(roulette(100, None, 1, None, "COLUMN")))
print("ROULETTE_TEST_9\n" + str(roulette(100, None, 1, "GREEN", "BASKET")))

# money += choHan(2, "Odd")
# print("Money: " + str(money))
# money += flip(3, "Tails")
# print("Money: " + str(money))
# money += war(2)
# print("Money: " + str(money))
'''


game_chohan = Game("Chohan", chohan.choHan, chohan.get_O_or_E, chohan.get_O_or_E_input)
game_flip = Game("Flip", flip.flip, flip.get_H_or_T, flip.get_H_or_T_input)
game_war = Game("War", war.war, None, None)
game_roulette = Game("Roulette", roulette.roulette, roulette.get_rand_inp, roulette.get_roulette_input)

list_of_games = [game_chohan, game_flip, game_war, game_roulette]

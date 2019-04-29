from stack import Stack

#LEARN STACKS
#Towers of Hanoi
#Towers of Hanoi is an ancient mathematical puzzle that starts off with three stacks and many disks.
#The objective of the game is to move the stack of disks from the leftmost stack to the rightmost stack.
#The game follows three rules:
#Only one disk can be moved at a time.
#Each move consists of taking the upper disk from one of the stacks and placing it on top of another stack or on an empty rod.
#No disk may be placed on top of a smaller disk.
#In this project, we are going to use our knowledge of stacks to implement this game! Lets get started!
#If you get stuck during this project or would like to see an experienced developer work through it, click Get Help to see a project walkthrough video.

print("\nLet's play Towers of Hanoi!!")

#Create the Stacks
stacks = []
left_stack = Stack("left stack")
middle_stack = Stack("middle stack")
right_stack = Stack("right stack")

stacks.append(right_stack)
stacks.append(middle_stack)
stacks.append(left_stack)

#Set up the Game
num_disks = int(input("\nHow many disks do you want to play with?\n"))
while (num_disks < 3):
  num_disks = int(input("Enter a number greater than or equal to 3\n"))
  
for disk in range(num_disks, 0, -1):
  left_stack.push(disk)
  
num_optimal_moves = 2**(num_disks-1)
print("\nThe fastest you can solve this game is in {x} moves".format(x = num_optimal_moves))

#Get User Input

def get_input():
  #choices= ["L", "M", "R"] hard-code
  choices = [stack.get_name()[0].upper() for stack in stacks]
  print(choices)
  while True:
    for i in range(len(choices)):
      name = stacks[i].get_name()
      letter = choices[i]
      print("Enter {x} for {y}".format(x = letter, y = name))
    user_input = input("")
    if (str(user_input).upper() in choices):
      for i in range(len(stacks)):
        if (str(user_input).upper() == choices[i]):
          return stacks[i]       
        
#Play the Game
num_user_moves = 0
while (right_stack.get_size() != num_disks):
  print("\n\n\n...Current Stacks...")
  for stack in stacks:
    stack.print_items()
  while (True):
    print("\nWhich stack do you want to move from?\n")
    from_stack = get_input()
    print("\nWhich stack do you want to move to?\n")
    to_stack = get_input()
    if (from_stack.is_empty()):
       print("\n\nInvalid Move. Try Again")
    elif (to_stack.is_empty() or from_stack.peek() < to_stack.peek()):
      disk = from_stack.pop()
      to_stack.push(disk)
      num_user_moves += 1
      break
    else:
      print("\n\nInvalid Move. Try Again")
print("\n\nYou completed the game in {x} moves, and the optimal number of moves is {y}".format(x = num_user_moves, y = num_optimal_moves))
			


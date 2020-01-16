
import random
from styles import BORDER

def flip(bet, call) :
  print("\n" + BORDER)
  print("Let's flip a coin!")
  flipped = random.choice(["Heads", "Tails"]).upper()
  earned = bet if flipped == call.upper() else -1 * bet
  print(("You win!" if earned > 0 else "You lose.") + " by guessing: " + call + ", earning: $ " + str(earned))
  print(BORDER + "\n")
  return earned


def get_H_or_T(args):
    return random.choice(["Heads", "Tails"])


def get_H_or_T_input(args) :
    inp = input("\nEnter \"Heads\" or \"Tails\".\n")
    accepted_input = ["h", "H", "heads", "Heads", "HEADS", "o", "O", "odd", "Odd", "ODD"]
    if inp in accepted_input :
        if "h" in inp or "H" in inp :
            return "Heads"
        elif "o" in inp or "O" in inp :
            return "Tails"
    return ""

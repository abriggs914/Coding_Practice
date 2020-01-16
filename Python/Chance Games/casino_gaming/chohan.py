import random
from styles import BORDER


def roll(sides):
    sides = max(1, sides)
    rolled = random.randint(1, sides)
    print("Rolled: " + str(rolled))
    return rolled


def odd_even(n):
    result = "Even" if n % 2 == 0 else "Odd"
    print(str(n) + " is " + result)
    return result


def choHan(bet, call):
    print("\n" + BORDER)
    die_1 = roll(6)
    die_2 = roll(6)
    result = odd_even(die_1 + die_2).upper()
    earned = bet if result == call.upper() else -1 * bet
    print(("You win!" if earned > 0 else "You lose.") + " by guessing: " + call + ", earning: $ " + str(earned))
    print(BORDER + "\n")
    return earned


def get_O_or_E(args):
    return random.choice(["Odd", "Even"])


def get_O_or_E_input(args) :
    o_e = input("\nEnter \"Odd\" or \"Even\".\n")
    accepted_input = ["o", "O", "odd", "Odd", "ODD", "e", "E", "Even", "even", "EVEN"]
    if o_e in accepted_input :
        if "o" in o_e or "O" in o_e :
            return "Odd"
        elif "e" in o_e or "E" in o_e :
            return "Even"
    return ""
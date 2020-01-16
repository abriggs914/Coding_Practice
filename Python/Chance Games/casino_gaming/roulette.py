import random
from styles import BORDER

ROULETTE_BETS = ["STRAIGHT UP",
                 "SPLIT",
                 "STREET",
                 "CORNER",
                 "BASKET",
                 "SIX LINE",
                 "COLUMN",
                 "DOZEN",
                 "ODD",
                 "EVEN",
                 "RED",
                 "BLACK",
                 "HIGH",
                 "LOW",
                 None]


def get_valid_call(which_bet):
    call = None
    if which_bet == "STRAIGHT UP":
        call = sim_valid_call(straight_up)
    elif which_bet == "SPLIT":
        call = sim_valid_call(split)
    elif which_bet == "STREET":
        call = sim_valid_call(street)
    elif which_bet == "CORNER":
        call = sim_valid_call(corner)
    elif which_bet == "BASKET":
        call = sim_valid_call(basket)
    elif which_bet == "SIX LINE":
        call = sim_valid_call(six_line)
    elif which_bet == "COLUMN":
        call = sim_valid_call(same_col)
    elif which_bet == "DOZEN":
        call = sim_valid_call(dozen)
    elif which_bet == "ODD":
        call = sim_valid_call(odd)
    elif which_bet == "EVEN":
        call = sim_valid_call(even)
    elif which_bet == "RED":
        call = sim_valid_call(red)
    elif which_bet == "BLACK":
        call = sim_valid_call(black)
    elif which_bet == "HIGH":
        call = sim_valid_call(high)
    elif which_bet == "LOW":
        call = sim_valid_call(low)
    else:
        print("UNABLE TO IDENTIFY CALL: " + str(which_bet))
    print("\n\tSelecting call for you to bet on: " + str(which_bet).title() + "\n\tNew call: " + str(call) + "\n")
    return call


def sim_valid_call(func):
    print("simulating valid call => func: " + str(func))
    while True:
        n, c = sim_roll_roulette()  # wheel results
        call_n = n
        if func == corner or func == six_line:
            call_n, call_c = sim_roll_roulette()
        t, is_true, odds = func(call_n, n, c, False)
        if is_true:
            return n


def gen_roulette_board():
    board = []
    x = 1
    for i in range(12):
        row = []
        for j in range(3):
            row.append(x)
            x += 1
        board.append(row)
    return board


def init_coloured_wheel():
    wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
             5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
    coloured_wheel = []
    for n in wheel:
        i = wheel.index(n)
        if i == 0:
            colour = "GREEN"
        elif i % 2 == 0:
            colour = "BLACK"
        else:
            colour = "RED"
        coloured_wheel.append((n, colour))
    return coloured_wheel


COLOURED_WHEEL = init_coloured_wheel()


def roll_roulette():
    wheeled = random.choice(COLOURED_WHEEL)
    print("\tRoulette wheeled: " + str(wheeled))
    return wheeled


def sim_roll_roulette():
    # print("coloured_wheel: " + str(COLOURED_WHEEL))
    wheeled = random.choice(COLOURED_WHEEL)
    return wheeled


def get_row(n):
    return (n - 1) // 3


def get_col(n):
    return (n - 1) % 3


def straight_up(call, n, c, p=True):
    is_true = call == n
    m = 35
    if is_true and p:
        print("\tStraight up! " + str(call) + " => x" + str(m))
    return "STRAIGHT UP", is_true, m


def split(call, n, c, p=True):
    is_true = abs(call - n) < 5
    m = 17
    if is_true and p:
        print("\tSplit! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "SPLIT", is_true, m


def street(call, n, c, p=True):
    a = get_row(call)
    b = get_row(n)
    is_true = a == b
    m = 11
    if is_true and p:
        print("\tStreet! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "STREET", is_true, m


def corner(call, n, c, p=True):
    a_row = get_row(call)
    a_col = get_col(call)
    b_row = get_row(n)
    b_col = get_col(n)
    # print("a_row: " + str(a_row) + ", a_col: " + str(a_col))
    # print("b_row: " + str(b_row) + ", b_col: " + str(b_col))
    diff_rows = abs(a_row - b_row) == 1
    diff_cols = False
    if a_col == 0:
        if b_col == 1:
            diff_cols = True
    elif a_col == 2:
        if b_col == 1:
            diff_cols = True
    else:
        if b_col != a_col:
            diff_cols = True
    is_true = diff_rows and diff_cols
    m = 8
    # print("diff_rows: " + str(diff_rows) + ", diff_cols: " + str(diff_cols))
    if is_true and p:
        print("\tCorner! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "CORNER", is_true, m


def basket(call, n, c, p=True):
    is_true = abs(call - n) < 4 and n < 4 and call < 4
    m = 8
    if is_true and p:
        print("\tBasket! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "BASKET", is_true, m


def six_line(call, n, c, p=True):
    a = get_row(call)
    b = get_row(n)
    is_true = abs(a - b) == 1
    m = 5
    if is_true and p:
        print("\tSix line! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "SIX LINE", is_true, m


def same_col(call, n, c, p=True):
    a = get_col(call)
    b = get_col(n)
    is_true = a == b
    m = 2
    if is_true and p:
        print("\tSame column! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "COLUMN", is_true, m


def dozen(call, n, c, p=True):
    a = get_row(call)
    b = get_row(n)
    is_true = abs(a - b) < 4
    is_true = is_true and ((a // 4) == (b // 4))
    m = 2
    if is_true and p:
        print("\tSame dozen! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "DOZEN", is_true, m


def odd(call, n, c, p=True):
    a = call % 2 == 1
    b = n % 2 == 1
    is_true = a and b
    m = 1
    if is_true and p:
        print("\tOdd! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "ODD", is_true, m


def even(call, n, c, p=True):
    a = call % 2 == 0
    b = n % 2 == 0
    is_true = a and b
    m = 1
    if is_true and p:
        print("\tEven! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "EVEN", is_true, m


def red(call, n, c, p=True):
    return colour(call, n, c, "RED", p)


def black(call, n, c, p=True):
    return colour(call, n, c, "BLACK", p)


def colour(call, n, c, bet, p=True):
    c_colour = COLOURED_WHEEL[call][1].upper()
    is_true = (c_colour == c.upper()) and c_colour == bet
    m = 1
    if is_true and p:
        print("\t" + c_colour.title() + "! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return c_colour, is_true, m


def high(call, n, c, p=True):
    is_true = min(call, n) > 18
    m = 1
    if is_true and p:
        print("\tHigh! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "HIGH", is_true, m


def low(call, n, c, p=True):
    is_true = max(call, n) < 19
    m = 1
    if is_true and p:
        print("\tLow! n: " + str(n) + ", call: " + str(call) + " => x" + str(m))
    return "LOW", is_true, m


def get_n_of_colour(c):
    while True:
        n, new_c = roll_roulette()
        if c == new_c:
            return n


def valid(n, c):
    if not -1 < n < 37:
        n = random.randint(0, 37)
    wheel = COLOURED_WHEEL
    wheel_c = wheel[n][1]
    result = c == wheel_c
    print("\tchecking: " + str(n) + ", " + c + " vs. " + wheel_c + " => " + str(result))
    return result


def sim_valid(n, c):
    if not -1 < n < 37:
        n = random.randint(0, 37)
    wheel = COLOURED_WHEEL
    wheel_c = wheel[n][1]
    result = c == wheel_c
    return result


def handle_roulette_input(n, c):
    new_n, new_c = roll_roulette()
    if n is None or c is None:
        if n is None:
            if c is None:
                n = new_n
            else:
                n = get_n_of_colour(c)
        if c is None:
            if n is None:
                c = new_c
            else:
                c = COLOURED_WHEEL[n][1]
    if not valid(n, c):
        if n is not None:
            c = COLOURED_WHEEL[n][1]
        else:
            n, c = new_n, new_c
    print("\tRoulette wheel results:\n\tn:\t" + str(n) + "\n\tc:\t" + c + "\n")
    return n, c


def sim_handle_roulette_input(n, c):
    new_n, new_c = sim_roll_roulette()
    if n is None or c is None:
        if n is None:
            if c is None:
                n = new_n
            else:
                n = get_n_of_colour(c)
        if c is None:
            if n is None:
                c = new_c
            else:
                c = COLOURED_WHEEL[n][1]
    if not sim_valid(n, c):
        if n is not None:
            c = COLOURED_WHEEL[n][1]
        else:
            n, c = new_n, new_c
    return n, c


# Can be called with test cases.
# enter either a number (0 - 36) or
# a colour ("GREEN", "BLACK", "RED")
# or both. All inputs are validated.
# which_bet is used for determining
# which bet was actually placed instead
# of calculating the max bet.
def roulette(bet, call=None, n=None, c=None, which_bet=None):
    entered_call = call
    entered_n = n
    entered_c = c
    print("\n" + BORDER)
    print("Welcome to European Roulette!\n")
    if not call:
        if not which_bet:
            print("NOT ENOUGH INFORMATION ENTERED.\n\tTAKING YOUR MONEY " + str(-1 * bet))
            return -1 * bet
        else:
            call = get_valid_call(which_bet)
    call_colour = COLOURED_WHEEL[call][1]
    payout_odds = 1
    bets_to_check = [straight_up,
                     split,
                     street,
                     corner,
                     basket,
                     six_line,
                     same_col,
                     dozen,
                     odd,
                     even,
                     red,
                     black,
                     high,
                     low]
    if call == 0 or n == 0:
        bets_to_check = [straight_up, basket]
    n, c = handle_roulette_input(n, c)
    winner = False
    best_bet = None

    for check_bet in bets_to_check:
        bet_type, is_true, new_odds = check_bet(call, n, c)
        if is_true:
            if new_odds > payout_odds or not best_bet:
                best_bet = bet_type

            if which_bet and which_bet == bet_type.upper():
                if not winner:
                    print("\n\tWINNING on a " + str(which_bet) + ".\n")
                winner = True
                payout_odds = new_odds
            elif not which_bet:
                if not winner:
                    print("WINNING " + str(which_bet))
                winner = True
                if new_odds > payout_odds:
                    payout_odds = new_odds

    result = "\n"
    if which_bet:
        result += "\tBet on:    " + which_bet.title() + "\n\tBest bet:  " + str(best_bet).title() + "\n\n"
    else:
        result += "\tNo explicit bet selected.\n\tUsing the max multiplier encountered.\n\n"
    earned = bet
    if winner:
        result += "\tYou win!"
    else:
        result += "\tYou lose."
        payout_odds *= -1

    earned *= payout_odds
    result += "\nentered: \n\t\tbet:\t" + str(bet)
    result += "\n\t\tcall:\t" + str(entered_call)
    result += "\n\t\tn:\t" + str(entered_n)
    result += "\n\t\tc:\t" + str(entered_c)
    result += "\n\tstrategy:\t" + str(which_bet)
    result += "\nYour guess: " + str(call) + " " + call_colour
    result += "\nWheel results: " + str(n) + " " + c
    result += "\nTotal payout multiplier: " + str(payout_odds)
    result += "\n\n\tYou earned:\t$ " + str(earned) + "\n"
    print(result + BORDER + "\n")
    return earned


def sim_roulette(bet, call=None, n=None, c=None, which_bet=None):
    if not call:
        if not which_bet:
            return -1 * bet
        else:
            print("adjusting for: " + str(which_bet))
            call = get_valid_call(which_bet)
    call_colour = COLOURED_WHEEL[call][1]
    payout_odds = 1
    bets_to_check = [straight_up,
                     split,
                     street,
                     corner,
                     basket,
                     six_line,
                     same_col,
                     dozen,
                     odd,
                     even,
                     red,
                     black,
                     high,
                     low]
    if call == 0 or n == 0:
        bets_to_check = [straight_up, basket]
    n, c = sim_handle_roulette_input(n, c)
    winner = False
    best_bet = None

    for check_bet in bets_to_check:
        bet_type, is_true, new_odds = check_bet(call, n, c, False)
        if is_true:
            if new_odds > payout_odds or not best_bet:
                best_bet = bet_type

            if which_bet and which_bet == bet_type.upper():
                winner = True
                payout_odds = new_odds
            elif not which_bet:
                winner = True
                if new_odds > payout_odds:
                    payout_odds = new_odds
    earned = bet
    if not winner:
        payout_odds *= -1
    earned *= payout_odds
    return earned


def choose_roulette_strategy(bet, call):
    best_strat = None
    max_score = 0
    n_sims = 10
    for strat in ROULETTE_BETS:
        for i in range(n_sims):
            n, c = sim_roll_roulette()
            round_max_score = 0
            round_best_strat = None
            for i in range(n_sims):
                m = sim_roulette(bet, call, n, c, strat)
                if m > round_max_score:
                    round_max_score = m
                    round_best_strat = strat
            if max_score < round_max_score:
                max_score = round_max_score
                best_strat = round_best_strat
    return best_strat


def get_int_input():
    while True:
        n = input("\nEnter an integer between 0 and 36.\n")
        try:
            i = int(n)
            if -1 < i < 37:
                return i
            else:
                raise ValueError
        except:
            print("please try again.")
            continue


def get_rand_strat():
    return random.choice(ROULETTE_BETS)


def get_strat_input() :
    i = 0
    message = "\nEnter the corresponding number to select a strategy\n"
    for s in ROULETTE_BETS :
        title = str(s).title()
        message += "\t" + str(i) + "\t-\t" + title + "\n"
        i += 1
    while True :
        inp = input(message)
        try :
            i = int(inp)
            if -1 < i < len(ROULETTE_BETS) :
                return ROULETTE_BETS[i]
            else :
                raise ValueError
        except :
            print("please try again")
            continue

def get_roulette_input(args):
    message = "\nWould you like to play a strategy\nor with a random guess, where the\nbest overall "
    message += "score is selected.\nEnter:\n\t\"Strat\"\tfor a strategy selection\n\t\"Num\"\tto select a number\n"
    accepted_input = ["s", "strat", "S", "Strat", "STRAT", "n", "N", "num", "Num", "NUM"]
    num = None
    strat = None
    while True :
        inp = input(message)
        if inp in accepted_input:
            if "n" in inp or "N" in inp:
                num = get_int_input()
                break
            elif "s" in inp or "S" in inp :
                strat = get_strat_input()
                break
    return num, strat


def get_rand_inp(args):
    call = random.choice([i for i in range(36)])
    return call, None

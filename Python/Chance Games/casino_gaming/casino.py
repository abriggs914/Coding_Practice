import random
import sys
#from games import choHan, flip, war, roulette, gen_new_deck, choose_roulette_strategy, BORDER
from games import list_of_games
from styles import BORDER, CASINO_BORDER, GAME_BORDER
from war import gen_new_deck

MAX = sys.maxsize
MIN = -sys.maxsize -1

EXIT_CODE = "q"

print("\n\n\tPRINTING LIST OF GAMES:\n" + str(list_of_games))
bet = 10
args = {}
args["war_deck"] = gen_new_deck()

# for g in list_of_games :
#   print("\n\t" + str(g) + "\n\t\t" + str(g.play(bet, args, True)))

#######################################################################################################################
#######################################################################################################################

DEFAULT_N_GAMES = 10
DEFAULT_MONEY = 1000
DEFAULT_HOW_LUCKY = 0.5
DEFAULT_DEDUCTION = 0.9
DEFAULT_RISK_INCREASE = 1.0
DEFAULT_RISK_ANSWER = False
DEFAULT_N_BORROWS = 5
DEFAULT_BORROW_AMOUNT = 500
DEFAULT_BORROW_INTEREST = 0.3
DEFAULT_GAMES = list_of_games

#######################################################################################################################
#######################################################################################################################

money = DEFAULT_MONEY							# **
borrowed = 0
borrow_interest = DEFAULT_BORROW_INTEREST		# **
borrow_amount = DEFAULT_BORROW_AMOUNT			# **
borrowed_amount = 0
borrow_terms_accepted = None
times_allowed_to_borrow = DEFAULT_N_BORROWS		# **
times_borrowed = 0
games = DEFAULT_GAMES							# **
deck = gen_new_deck()
start_money = money
how_lucky = DEFAULT_HOW_LUCKY					# **
risk_deduction_factor = DEFAULT_DEDUCTION		# **
risk_factor = how_lucky
risk_increase_answer = DEFAULT_RISK_ANSWER		# **
risk_increase = DEFAULT_RISK_INCREASE			# **
n_games = DEFAULT_N_GAMES						# **
games_played = 0
games_chosen = {}

money_used = 0
with_interest = 0
roi = 0
ratio = 0
payouts = 0

#######################################################################################################################
#######################################################################################################################

def early_exit_message() :
  print("\n\tEXITING EARLY\n")
  exit()
  
def get_game_title(g) :
  return str(g).split(" ")[1].title()
  
def check_int(n) :
  accept = False
  try :
    i = int(n)
    accept = True
  except :
    pass
  return accept
  
def check_float(n) :
  accept = False
  try :
    i = float(n)
    accept = True
  except :
    pass
  return accept
	  
def get_int_input(terms, unit="", ranges=None) :
  print(BORDER)
  inp = input(terms + "\n")
  attempts = 1
  accept = False
  percent_unit = ""
  if not ranges :
    ranges = (MIN, MAX)
  if unit == " %" :
    percent_unit = unit
    unit = ""
  while True :
    range_check = check_int(inp) and ranges[0] <= int(inp) <= ranges[1]
    # print("range_check: " + str(range_check) + ", r[0]: " + str(ranges[0]) + " <= " + str(inp) + " <= " + str(ranges[1]))
    if str(inp) == EXIT_CODE:
      early_exit_message()
    confirmation = get_confirmation_input(terms + "\n\tEntered:\t" + unit + inp + percent_unit)
    accept = range_check and confirmation 
    # print("accept_check: " + str(accept) + ", r: " + str(range_check) + " c: " + str(confirmation))
	# correct input
    if accept:
      inp = int(inp)
      break
    else :
      inp = input(terms + "\n" + unit)
    attempts += 1
    if attempts > 5 :
      print("\n\n\tToo many tries...")
      # early_exit_message()
      break
  print(BORDER)
  return accept, inp
	  
def get_float_input(terms, unit="", ranges=None) :
  print(BORDER)
  inp = input(terms + "\n")
  attempts = 1
  accept = False
  percent_unit = ""
  if not ranges :
    ranges = (float('-inf'), float('inf'))
  if unit == " %" :
    percent_unit = unit
    unit = ""
  while True :
    range_check = check_float(inp) and ranges[0] <= float(inp) <= ranges[1]
    if str(inp) == EXIT_CODE:
      early_exit_message()
    confirmation = get_confirmation_input(terms + "\n\tEntered:\t" + unit + inp + percent_unit)
    accept = range_check and confirmation 
    # print("accept_check: " + str(accept) + ", r: " + str(range_check) + " c: " + str(confirmation))
	# correct input
    if accept :
      inp = float(inp)
      break
    else :
      inp = input(terms + "\n" + unit)
    attempts += 1
    if attempts > 5 :
      print("\n\n\tToo many tries...\n\tSelecting defaults.\n")
      # early_exit_message()
      break
  print(BORDER)
  return accept, inp
  
def get_yes_no_input(terms) :
  print(BORDER + terms)
  inp = input()
  accepted_yes = ["y", "Y", "yes", "Yes", "YES", 1]
  accepted_no = ["n", "N", "no", "No", "NO", 0]
  res = (False, "")
  if inp in accepted_yes :
    res = True, inp
  elif inp in accepted_no :
    res = False, inp
  else :
    i = 1
    while i < 5:
      print(terms)
      inp = input()
      i += 1
      if inp in accepted_yes :
        res = True, inp
        break
      elif inp in accepted_no :
        res = False, inp
        break
  print("\n" + BORDER)
  return res
  
def get_games_selection() :
  global games_chosen, games
  games_to_use = []
  for game in DEFAULT_GAMES :
    accept = False
    print("game:\t" + str(game))
    title = game.get_name()
    print(BORDER + "\n\n")
    message = "\n\tWould you like to add " + title + " to your games selection?\n\tCurrently selected:\n"
    if len(list(games_chosen.keys())) > 0 :
      for g in games_chosen.keys() :
        message += "\t\t" + str(g) + "\n"
    else :
      message += "\t\tNONE\n"
    message += "Enter \'y\' to add game or enter \'n\' to skip.\n"
    accepted, entered = get_yes_no_input(message)
    print("accepted: " + str(accepted) + ", entered: " + str(entered))
    accept = accepted#  and str(entered).upper() == "Y"
    # print("title: " + str(title))
    if accept :
      stats = {"n_games" : 0,
	  "n_wins" : 0,
	  "n_losses" : 0,
	  "bets_total" : 0,
	  "bets_min" : MAX,
	  "bets_max" : MIN,
	  "bets_won" : 0,
	  "bets_lost" : 0,
	  "bet_best_win" : [MIN, 1],		# used for best bet to earning ratio when you win
	  "bet_worst_win" : [MAX, 1],		# used for worst bet to earning ratio when you win
	  "bet_best_loss" : [MIN, 1],		# used for best bet to earning ratio when you lose
	  "bet_worst_loss" : [MAX, 1],		# used for worst bet to earning ratio when you lose
	  "earning_max" : 0,
	  "earning_min" : 0,
	  "earning_win_total" : 0,
	  "earning_loss_total" : 0,
	  "earning_total" : 0}
      games_chosen[title] = [game, stats]
      games_to_use.append(game)
      print("\n\t" + title + " has been added to your games selection!")
  print("games_chosen:\t" + str(games_chosen))
  if len(list(games_chosen.keys())) == 0 :
    print("\n\n\tNo games selected.")
    early_exit_message()
  games = games_to_use
  print("\n" + BORDER)

def get_confirmation_input(terms) :
  accept = False
  inp = input("\n\n\tTERMS:\t\t" + str(terms) + "\n\tEnter 0 to accept and anything else to decline.\n")
  if inp and type(inp) == str :
    try :
      i = int(inp)
      if i == 0 :
        accept = True
        print("\n\tAccepting these terms. {" + str(inp) + "}\n\n")
      else :
        raise ValueError
    except :
      print("\n\tDeclining these terms. {" + str(inp) + "}\n\n")
  return accept

def get_input_values() :
  global how_lucky, money, games_played, times_borrowed, times_allowed_to_borrow, n_games, borrow_amount, borrow_interest, borrowed_amount, risk_deduction_factor, start_money, risk_factor
  games_range = (1, MAX)
  money_ranges = (1, 1000000000)
  lucky_ranges = (0, 1)
  risk_deduction_ranges = (0, 1)
  interest_ranges = (0, 1)
  
  user_wants_custom = get_yes_no_input("\n\n\tWould you like to add custom input?\n\tEnter YES or NO\n")[0]
  if user_wants_custom :
    print(BORDER + "\n\tGetting custom inputs for casino gaming:\n")
	
    games_input = get_int_input("How many games would you like to play today?", "x ", games_range)
    money_input = get_int_input("How much money do you have to start with?\n\tBetween\t\t$ " + str(money_ranges[0]) + " and $ "  + str(money_ranges[1]), "$ ", money_ranges)
    how_lucky_input = get_float_input("How risky do you feel?\n\tBetween\t\t" + str(lucky_ranges[0]) + " % and "  + str(lucky_ranges[1]) + " %", " %", lucky_ranges)
    deduction_input = get_float_input("How much of a penalty to risk would\n\tyou like if you were to bust?\n\tBetween\t\t" + str(risk_deduction_ranges[0]) + " % and "  + str(risk_deduction_ranges[1]) + " %", " %", risk_deduction_ranges)
    n_borrows_input = get_int_input("How many times would you like lenders\n\tto offer you a buy-back?", "x ", (0, MAX))
    borrow_amount_input = get_int_input("How much would you like lenders\n\tto offer you for a buy-back?", "$ ", (0, MAX))
    borrow_interest_input = get_float_input("How much would you like lenders\n\tto charge you for interest?\n\tBetween\t\t" + str(interest_ranges[0]) + " % and "  + str(interest_ranges[1]) + " %", " %", interest_ranges)
  
    n_games = games_input[1] if games_input[0] else DEFAULT_N_GAMES
    money = money_input[1] if money_input[0] else DEFAULT_MONEY
    how_lucky = how_lucky_input[1] if how_lucky_input[0] else DEFAULT_HOW_LUCKY
    risk_deduction_factor = deduction_input[1] if deduction_input[0] else DEFUAULT_DEDUCTION
    times_allowed_to_borrow = n_borrows_input[1] if n_borrows_input[0] else DEFAULT_N_BORROWS
    borrow_amount = borrow_amount_input[1] if borrow_amount_input[0] else DEFAULT_BORROW_AMOUNT
    borrow_interest = borrow_interest_input[1] if borrow_interest_input[0] else DEFAULT_BORROW_INTEREST
  
    risk_factor = how_lucky
    start_money = money
    #how_lucky, games_played, times_borrowed, times_allowed_to_borrow, n_games, borrow_amount, borrow_interest, borrowed_amount, risk_deduction_factor, start_money]
    print(BORDER + "\n")

def lender_message() :
  res = "\n\tLenders are prepared to offer you " + str(times_allowed_to_borrow)
  res += " bonus payment" + ("s" if times_allowed_to_borrow > 1 or times_allowed_to_borrow == 0 else "") 
  res += " of $ " + str(borrow_amount) + "\n\tat an interest rate of " + str(borrow_interest) + " %"
  if borrow_terms_accepted is not None :
    if borrow_terms_accepted :
      res += "\n\tYou chose to ACCEPT these terms."
    else :
      res += "\n\tYou chose to DECLINE these terms."
  return res

def ask_lender_terms() :
  global borrow_terms_accepted
  res = lender_message()
  print(str(res) + "\n\n\tWould you like to accept these terms?")
  inp = input("\n\n\tEnter 0 to accept and anything else to decline.\n")
  accept = False
  if inp and type(inp) == str :
    try :
      i = int(inp)
      if i == 0 :
        accept = True
        print("\n\tAccepting these terms. {" + str(inp) + "}\n\n")
      else :
        raise ValueError
    except :
      print("\n\tDeclining these terms. {" + str(inp) + "}\n\n")
  borrow_terms_accepted = accept
  
def winner_message(earning) :
  return "\n\n\t\tWINNER WINNER CHICKEN DINNER!!!!\n\n\t\tYOU WIN: $ " + str(earning) + " !!!!\n\n"
  
def losing_message(earning) :
  return "\n\n\t\tTHE HOUSE WINS YOUR MONEY\n\n\t\tYOU LOSE: $ " + str(earning) + "\n\n"
  
def luck_str(how_lucky) :
  luck = "\t  " + str(how_lucky) + " %"
  if how_lucky <= 0.1 :
    return "very unlucky " + luck
  elif how_lucky <= 0.2 :
    return "unlucky \t" + luck
  elif how_lucky <= 0.3 :
    return "conservative " + luck
  elif how_lucky <= 0.4 :
    return "withholding " + luck
  elif how_lucky <= 0.5 :
    return "50 / 50 \t" + luck
  elif how_lucky <= 0.6 :
    return "confident " + luck
  elif how_lucky <= 0.7 :
    return "hopeful \t" + luck
  elif how_lucky <= 0.8 :
    return "optimistic " + luck
  elif how_lucky <= 0.9 :
    return "lucky \t" + luck
  else :
    return "very lucky \t" + luck
	
def res_str(money, interest, roi, ratio) :
  luck = "\t$ " + str(roi)
  if ratio <= 0 :
    return " a VERY bad idea.\t" + luck
  elif ratio <= 0.5 :
    return " not a very good idea." + luck
  elif ratio < 1 :
    return " not a very good idea." + luck
  elif ratio == 1 :
    return " a waste of time." + luck
  elif ratio <= 1.5 :
    return " somewhat worth it." + luck
  elif ratio < 2 :
    return " a half decent payout." + luck
  elif ratio == 2 :
    return " a double payout day!" + luck
  elif ratio <= 5 :
    return " a very good decision!" + luck
  elif ratio <= 10 :
    return " a very fortunate payout!!" + luck
  else :
    return " a VERY fortunate decision!!" + luck
	
def update_stats(bet, earning, title, stats) :
  win = False
  stats["n_games"] += 1
  stats["bets_total"] += bet
  if bet > stats["bets_max"] :
    stats["bets_max"] = bet
  if bet < stats["bets_min"] :
    stats["bets_min"] = bet
  if earning > stats["earning_max"] :
    stats["earning_max"] = earning
  if earning < stats["earning_min"] :
    stats["earning_min"] = earning
  # WIN
  ratio = earning / bet
  curr_bw_ratio = stats["bet_best_win"][0] / stats["bet_best_win"][1]
  curr_ww_ratio = stats["bet_worst_win"][0] / stats["bet_worst_win"][1]
  curr_bl_ratio = stats["bet_best_loss"][0] / stats["bet_best_loss"][1]
  curr_wl_ratio = stats["bet_worst_loss"][0] / stats["bet_worst_loss"][1]
  print("r: " + str(ratio) + ", bw: " + str(curr_bw_ratio) + ", ww: " + str(curr_ww_ratio) + ", bl: " + str(curr_bl_ratio) + ", wl: " + str(curr_wl_ratio))
  if earning > 0 :
    stats["n_wins"] += 1
    stats["bets_won"] += bet
    if ratio > curr_bw_ratio :
      print("adjusting: bet_best_win : " + str(stats["bet_best_win"]) + " -> " + str([earning, bet]) + " due to r (" + str(ratio) + ") > bw (" + str(curr_bw_ratio) + ").")
      stats["bet_best_win"][0] = earning
      stats["bet_best_win"][1] = bet
    if ratio < curr_ww_ratio :
      print("adjusting: bet_worst_win : " + str(stats["bet_worst_win"]) + " -> " + str([earning, bet]) + " due to r (" + str(ratio) + ") < ww (" + str(curr_ww_ratio) + ").")
      stats["bet_worst_win"][0] = earning
      stats["bet_worst_win"][1] = bet
  # LOSS
  elif earning < 0 :
    stats["n_losses"] += 1
    stats["bets_lost"] += bet
    if ratio > curr_bl_ratio :
      print("adjusting: bet_best_loss : " + str(stats["bet_best_loss"]) + " -> " + str([earning, bet]) + " due to r ( " + str(ratio) + ") > bl (" + str(curr_bl_ratio) + ").")
      stats["bet_best_loss"][0] = earning
      stats["bet_best_loss"][1] = bet
    if ratio < curr_wl_ratio :
      print("adjusting: bet_worst_loss : " + str(stats["bet_worst_loss"]) + " -> " + str([earning, bet]) + " due to r ( " + str(ratio) + ") < wl (" + str(curr_wl_ratio) + ").")
      stats["bet_worst_loss"][0] = earning
      stats["bet_worst_loss"][1] = bet
	
'''
stats = {"n_games" : 0,			*
	  "n_wins" : 0,				*
	  "n_losses" : 0,			*
	  "bets_total" : 0,			*
	  "bets_min" : MAX,			*
	  "bets_max" : MIN,			*
	  "bets_won" : 0,			*
	  "bets_lost" : 0,			*
	  "bet_best_win" : 0,		*
	  "bet_worst_win" : 0,		*
	  "bet_best_loss" : 0,		*
	  "bet_worst_loss" : 0}		*
'''

def print_stats() :
  global games_chosen
  print("\n" + BORDER + "\n")
  for title, record in games_chosen.items() :
    print("\n\t--\t" + title + " stats:\t--\n")
    for category, stat in record[1].items() :
      space = "\t" if category == "n_wins" else ""
      print("\t\t" + category + ":" + space + "\t\t\t" + str(stat))
  print("\n" + BORDER + "\n")
  
def calculate_bet(money, how_lucky) :
  i = max(1, int(how_lucky * money))
  return i if i == 1 else random.randint(1, i)

def play_games() :
    global how_lucky, money, games_played, times_borrowed, times_allowed_to_borrow, n_games, borrow_terms_accepted, borrow_amount, borrowed_amount, risk_deduction_factor, money_used, roi, payouts, with_interest, ratio, start_money, games_chosen
    for i in range(n_games) :
        game = random.choice(games)
        bet = calculate_bet(money, how_lucky)
        title = game.get_name()
        stats = games_chosen[title][1]
        print("\n" + GAME_BORDER + "\n\n\tVV\tGame " + str(i + 1) + "\t" + title + "\t" + "\tVV\n")
        print("\tMoney:\t\t\t\t$ " + str(money))
        print("\tI'm feeling " + luck_str(how_lucky))
        print("\tWilling to bet:\t\t\t$ " + str(bet))
        # if game == choHan :
        #     e_o = random.choice(["Even", "Odd"])
        #     earning = choHan(bet, e_o)
        # elif game == war :
        #     earning = war(bet, deck)
        # elif game == flip :
        #     h_t = random.choice(["Heads", "Tails"])
        #     earning = flip(bet, h_t)
        # else :
        #     call = random.randint(0, 36)
        #     strategy = choose_roulette_strategy(bet, call)
        #     # strategy = random.choice(ROULETTE_BETS)
        #     earning = roulette(bet, call, None, None, strategy)
        #     print("Earned: " + str(earning))
        earning = game.play(bet, args, True)
        if earning > 0 :
            print(winner_message(earning))
        else :
            print(losing_message(earning))
        money += earning
        games_played += 1
        update_stats(bet, earning, title, stats)
        if money <= 0 :
            # check borrowing measures
            if times_borrowed < times_allowed_to_borrow and i < n_games and borrow_terms_accepted:
                money += borrow_amount
                borrowed_amount += borrow_amount
                times_borrowed += 1
                print("\tBORROWING: " + str(borrow_amount))
                print("\tBE LESS RISKY (risk factor x" + str(risk_deduction_factor) + ")")
                how_lucky *= risk_deduction_factor
            else :
                print("\n\tBUST!\n\nSorry you don't have any money left to play.\n")
                break
        print("\n\t^^\tGame: " + str(i + 1) + "\t^^\n" + GAME_BORDER + "\n")
    money_used = (start_money + borrowed_amount)
    # borrowed_amount = borrow_amount * times_borrowed
    with_interest = borrowed_amount + (borrowed_amount * borrow_interest) if times_borrowed > 0 else 0
    roi = (money - with_interest) - start_money
    ratio = money / money_used
    payouts = money - money_used

def print_results() :
  global borrow_terms_accepted
  print(BORDER + "\n\tRESULTS\n\nGames played:\t\t\tx " + str(games_played))
  print("Grand Total cashing out:\t$ " + str(money))
  print("Started with:\t\t\t$ " + str(start_money))
  print("Total money used:\t\t$ " + str(money_used))
 
  if borrow_terms_accepted :
    print(BORDER + "\n\tLENDERS:")
    print("Borrowed:\t\t\tx " + str(times_borrowed))
    print("Borrowed from lenders:\t\t$ " + str(borrowed_amount))
    print("Interest:\t\t\t% " + str(borrow_interest))
    print("Pay to lenders:\t\t\t$ " + str(with_interest))
    print(BORDER)
  
  print("Return on investment:\t\t$ " + str(roi) + "\nratio:\t\t\t\t: " + str(ratio))
  print(BORDER + "\n\tRISK ANALYSIS:")
  
  print("Starting Risk factor:\t\t% " + str(risk_factor))
  print("Risk adjustment factor:\t\t% " + str(risk_deduction_factor))
  print("Ending Risk factor:\t\t% " + str(how_lucky))
  print(BORDER)
  
  print(BORDER + "\n\tSUMMARY\n") 
  print("Total payouts:\t\t\t$ " + str(payouts))
  print("Coming to the casino today\nwas" + res_str(money, with_interest, roi, ratio)) 
  #print("\n" + BORDER) 
	  

def welcome_to_casino() :
  print(CASINO_BORDER)
  print("\n\nWelcome to the casino:\n\n")
  get_games_selection()
  get_input_values()
  ask_lender_terms()
  play_games()
  print_results()
  print_stats()
  print(CASINO_BORDER)

# welcome_to_casino()


'''

Lenders information output about how many borrows and such..

input controls for all game variables.

individual game histories and records.
	-	max min tuples dont like to be re-assigined.
	
ask the user if they want to update the stats and include the defaults in the messages.

give descriptions of choices like the risk deduction factor and what it will do.

separate all games into their own files and create a master "game" class to facilitate
new games being made.

'''

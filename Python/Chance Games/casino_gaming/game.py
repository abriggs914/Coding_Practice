import chohan

class Game :

  def __init__(self, name, game_func, rand_call_func, inp_call_func) :
    self.name = name
    self.game_func = game_func
    self.get_rand_call = rand_call_func
    self.inp_call_func = inp_call_func


  def get_name(self) :
    return self.name

  def play(self, bet, args, get_input=False) :
    roi = 0
    mult = 1
    n = self.name
    print("playing " + str(n))
    if n == "War" :
      deck = args["war_deck"]
      roi = self.game_func(bet, deck)
    elif n == "Roulette" :
      call, strat = self.inp_call_func(args) if get_input else self.get_rand_call(args)
      args["roulette_strat"] = strat
      roi = self.game_func(bet, call, None, None, strat)
    else :
      call = self.inp_call_func(args) if get_input else self.rand_call_func(args)
      roi = self.game_func(bet, call)

    # if n == "Chohan" :
    #   call = self.inp_call_func() if get_input else self.rand_call_func()
    # #   call = chohan.get_H_or_T() if get_input else
    # elif n == "Flip" :
    #   call = self.
    return roi

  # def get_rand_call(self):
  #   return self.rand_call_func()

  def __repr__(self) :
    return self.name

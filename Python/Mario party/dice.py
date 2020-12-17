import csv

with open("dice.csv", "r") as file:
	player_dice = csv.DictReader(file)
	players = {} 
	
	def get_die_slots(player):
		return [player["slot1"], player["slot2"], player["slot3"], player["slot4"], player["slot5"], player["slot6"]]
	
	def expected_coins(player):
		die_slots = get_die_slots(player)
		coin_rolls = [val for val in die_slots if "+" in val or "-" in val]
		return sum([(-1 if "-" in val else 1) * int(val[1:]) for val in coin_rolls]) / len(die_slots)
	
	def expected_displacement(player):
		die_slots = get_die_slots(player)
		move_rolls = [val for val in die_slots if "+" not in val and "-" not in val]
		return sum([int(val) for val in move_rolls]) / len(die_slots)
		
	def rank(r):
		if r == "S":
			return 5
		if r == "A":
			return 4
		if r == "B":
			return 3
		if r == "C":
			return 2
		if r == "D":
			return 1
		if r == "F":
			return 0
		return -1
		
	# Add "exp_move" and "exp_coins" values for each player.
	for player in player_dice:
		# print("\n")
		keys = []
		vals = []
		for k, v in player.items():
			if k != "Name":
				keys.append(k)
				vals.append(v)
		exp_coins = expected_coins(player)
		exp_move = expected_displacement(player)
		players[player["Name"]] = dict(zip(keys, vals))
		players[player["Name"]]["exp_coins"] = exp_coins
		players[player["Name"]]["exp_move"] = exp_move
		
	def best_ranked():
		return {k: v for k, v in sorted(players.items(), key=lambda item: rank(item[1]["rank"]), reverse=True)}
	def best_earners():
		return {k: v for k, v in sorted(players.items(), key=lambda item: item[1]["exp_coins"], reverse=True)}
	def best_movers():
		return {k: v for k, v in sorted(players.items(), key=lambda item: item[1]["exp_move"], reverse=True)}
	def best_scored():
		return {k: v for k, v in sorted(players.items(), key=lambda item: score(item[1]))}
	
			
	def print_best(name, key, lst):
		print("\n\tbest {0}:\n".format(name))
		for i, player in enumerate(lst):
			line = str(i+1) + ".\t"
			line += player.ljust(30) + str(lst[player][key])
			print(line)
			
	def print_best_earners():
		print_best("earners", "exp_coins", best_earners())
		
	def print_best_movers():
		print_best("movers", "exp_move", best_movers())
		
	def print_best_ranked():
		print_best("ranked", "rank", best_ranked())
		
	def print_best_scored():
		print_best("scored", "score", best_scored())
			
	def score(player):
		be = best_earners()
		bm = best_movers()
		br = best_ranked()
		earnings = [player["exp_coins"] for name, player in be.items()]
		displacements = [player["exp_move"] for name, player in bm.items()]
		ranks = [player["rank"] for name, player in br.items()]
		s = earnings.index(player["exp_coins"])
		s += displacements.index(player["exp_move"])
		s += ranks.index(player["rank"])
		# print("SCORE: " + str(s))
		player["score"] = s / 3
		return s / 3
		
	print_best_earners()
	print_best_movers()
	print_best_ranked()
	print_best_scored()
import random
import math
import statistics as stats

odds = [
	(22, range(10)),
	(28, range(28)),
	(32, range(28)),
	(38, range(24)),
	(110, range(6)),
	(250, range(4))
]

# odds = [
	# (110, range(60)),
	# (250, range(40))
# ]

renown_left = 180000 # 45000 - 39031
season_pass_val = 0.1

def random_n():
	return round(random.randint(0, 99))	
	
	
def which_odds():
	n = random_n()
	start, stop = 0, 0
	for r, o in odds:
		# print("n:", n, "start:", start, "stop:", stop)
		stop += o.stop
		if n in range(start, stop):
			return r
		start += o.stop
	
	
	
# print("which_odds", which_odds())

def run_sim(season_pass=False):
	renown_banked = 0
	games_played = 0
	renown_earned_list = []

	while renown_banked < renown_left:
		renown_earned = which_odds()
		# print("renown_earned:", renown_earned)
		if season_pass:
			renown_earned *= int(1 + season_pass_val)
		# print("renown_earned:", renown_earned)
		renown_banked += renown_earned
		games_played += 1
		renown_earned_list.append(renown_earned)
		
	avg_renown = stats.mean(renown_earned_list)
	print("Games played:", games_played, "renown_banked:", renown_banked, "avg renown earned", avg_renown)
		
		
def min_games(renown_left, season_pass=False):
	if season_pass:
		renown_left = ((1 - season_pass_val) * renown_left)
	return math.ceil(renown_left / odds[-1][0])
	

def max_games(renown_left, season_pass=False):
	if season_pass:
		renown_left = ((1 - season_pass_val) * renown_left)
	return math.ceil(renown_left / odds[0][0])
		
		
for i in range(10):
	run_sim(season_pass=True)
	
# minimum_games_required = math.ceil(renown_left / odds[-1][0])
# maximum_games_required = math.ceil(renown_left / odds[-1][0])
minimum_games_required = min_games(renown_left, True)
maximum_games_required = max_games(renown_left, True)
print("minimum_games_required:", minimum_games_required)
print("maximum_games_required:", maximum_games_required)
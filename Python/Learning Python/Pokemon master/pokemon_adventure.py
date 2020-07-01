import random as rd
import time


# ---- CLASSES
class Pokemon:
	def __init__(self, name, level, atk_type, xp=0, ko=False):
		self.name = name
		self.level = level
		self.atk_type = atk_type
		self.max_hp = level * 10
		self.curr_hp = level * 10
		self.xp = xp
		self.ko = ko

	def attack(self, other):
		stab = 1.0
		for t in self.atk_type:
			for y in other.atk_type:
				if (t == 'fire' and y == 'grass') \
					or (t == 'grass' and y == 'water') \
					or (t == 'water' and y == 'fire'):
					stab += 0.5
				elif (t == 'grass' and y == 'fire') \
				    or (t == 'fire' and y == 'water') \
				    or (t == 'water' and y == 'grass'):
					stab -= 0.5

		damage = self.level * stab + (rd.randint(-5, 5) * 0.10)
		other.curr_hp = max(other.curr_hp - damage, 0)
		print("{} hits {} for {} damage!".format(self.name, other.name, round(damage, 1)))

		if other.curr_hp == 0:
			other.ko = True

	def level_up(self):
		self.level += 1
		self.max_hp = self.level * 10


class Trainer:
	def __init__(self, name, belt, pack, wallet):
		self.name = name
		self.belt = belt
		self.pack = pack
		self.wallet = wallet

	def get_avg_level(self):
		return sum(slot.level for slot in self.belt) / len(self.belt)

	def has_pkmn(self):
		for pkmn in self.belt:
			if (not pkmn.ko):
				return True
		return False

	def view_pkmn(self):
		print(f"%s's Pokemon:" % self.name)
		for idx, pkmn in enumerate(self.belt):
			is_ko = ''
			if (pkmn.ko):
				is_ko = " - fainted!"
			print(f"%d - %s  Lv.%d  %d/%d HP%s" % (idx + 1, pkmn.name, pkmn.level, pkmn.curr_hp, pkmn.max_hp, is_ko))

	def view_pack(self, in_wild=False):
		items_d = {}
		i = 1
		for k, v in self.pack.items():
			items_d[str(i)] = k
			i += 1
		print(f"Wallet: %dg" % self.wallet)
		for str_num, name in items_d.items():
			print(f"%s) %s - %d" % (str_num, name, self.pack[name]))
		print("[number] to select, or [Enter] to close")
		selection = input()
		if (selection in [str(i + 1) for i in range(len(self.belt))] and self.pack[items_d[selection]] > 0):
			if (items_d[selection] in ["pokeball", "ultraball"]):
				if (in_wild):
					return self.catch_pkmn(items_d, selection)
				else:
					print("There's no wild pokemon to catch.")
					return False
			# elif (items_d[selection] == "ultraball"):
			# 	if (in_wild):
			# 		return self.catch_pkmn(items_d, selection, 75)
			self.view_pkmn()
			print("[number] to apply effect, or [Enter] to close")
			slot = input()
			if (slot in [str(i + 1) for i in range(len(self.belt))]):
				if (items_d[selection] == "potion"):
					self.belt[int(slot) - 1].curr_hp = min(self.belt[int(slot) - 1].curr_hp + 30,
					                                            self.belt[int(slot) - 1].max_hp)
					self.pack[items_d[selection]] -= 1
				elif (items_d[selection] == "revive"):
					self.belt[int(slot) - 1].curr_hp = min(self.belt[int(slot) - 1].curr_hp + 1,
					                                            self.belt[int(slot) - 1].max_hp)
					self.belt[int(slot) - 1].ko = False
					self.pack[items_d[selection]] -= 1
				# elif (items_d[selection] == "pokeball"):
				# 	return self.catch_pkmn()
				return False
			return False
		return False

	def catch_pkmn(self, items_d, selection):
		balls = {"pokeball": 30,
		         "ultraball": 75}
		self.pack[items_d[selection]] -= 1
		print("You throw a pokeball.")
		catching_phrases = ["The ball lurches violently!",
		                    "The ball shudders in protest.",
		                    "The ball shakes weakly."]
		time.sleep(2)
		for i in range(3):
			chance = rd.randint(0, 100)
			if (chance < balls[items_d[selection]]):
				return True
			else:
				print(catching_phrases[i])
				time.sleep(1.2)
		print("The ball shatters!")
		return False

	def swap_pkmn(self):
		self.view_pkmn()
		print("[number] to change leader, or [Enter] to close")
		selection = input()
		if selection in [str(i + 1) for i in range(len(self.belt))]:
			if (not self.belt[int(selection) - 1].ko):
				self.set_active_pkmn(int(selection) - 1)
			else:
				self.swap_pkmn()
		elif (self.belt[0].ko):
			self.swap_pkmn()

	def set_active_pkmn(self, selection):
		self.belt.insert(0, self.belt.pop(self.belt.index(self.belt[selection])))


# ---- VARIABLES
player = Trainer("missingno", [], {"potion": 10, "revive": 3}, 5000)
opponent_names = ["Brock", "Misty", "Lt. Surge", "Erika", "Koga", "Sabrina", "Blaine", "Giovanni"]
dex = [{"Name": "Bulbasaur", "atk_type": ["grass"]},
        {"Name": "Charmander", "atk_type": ["fire"]},
        {"Name": "Squirtle", "atk_type": ["water"]}]


# ---- FUNCTIONS
def display_belt(player, pkmn):
	print(player.name, end=' - ')
	for slot in player.belt:
		if slot.ko:
			print("[/]", end=' ')
		else:
			print("[_]", end=' ')
	print(f"\n%s  Lv.%d  %d/%d HP" % (pkmn.name, pkmn.level, pkmn.curr_hp, pkmn.max_hp))
	print()


def instantiate_opponent_trainer():
	belt = []
	adj_level = 0
	for slot in range(rd.randint(1, 6)):
		rand_pkmn = rd.choice(dex)
		adj_level = player.get_avg_level() + rd.randint(-2, 2)
		belt.append(Pokemon(rand_pkmn["Name"], adj_level, rand_pkmn["atk_type"]))
	wallet = adj_level * 10
	return Trainer(rd.choice(opponent_names), belt, {}, wallet)


def wild_battle():
	rand_pkmn = rd.choice(dex)
	adj_level = player.get_avg_level() + rd.randint(-2, 2)
	opponent_pkmn = Pokemon(rand_pkmn["Name"], adj_level, rand_pkmn["atk_type"])
	caught = False

	# commence battle
	print(f"Go, %s!" % player.belt[0].name)
	player_pkmn = player.belt[0]
	# opponent_pkmn = opponent.belt[0]

	# battle loop
	while (player.has_pkmn() and not opponent_pkmn.ko and not caught):
		# print()
		# display_belt(opponent, opponent_pkmn)
		print(f"\n%s  Lv.%d  %d/%d HP" % (opponent_pkmn.name, opponent_pkmn.level,
		                                  opponent_pkmn.curr_hp, opponent_pkmn.max_hp))
		print()
		display_belt(player, player_pkmn)
		choice = input("1) Attack\n2) Switch\n3) Use item\n")
		if (choice == '1'):
			player_pkmn.attack(opponent_pkmn)
			if (opponent_pkmn.ko):
				print(f"Enemy %s has fainted!" % opponent_pkmn.name)
				player_pkmn.xp += 1
				if player_pkmn.xp == 4:
					player_pkmn.level_up()
				# else:
				# 	continue
			else:
				opponent_pkmn.attack(player_pkmn)
			if (player_pkmn.ko):
				print(f"\n%s has fainted!" % player_pkmn.name)
				if (player.has_pkmn()):
					print("Choose next pokemon:")
					player.swap_pkmn()
					player_pkmn = player.belt[0]
		elif (choice == '2'):
			player.swap_pkmn()
			player_pkmn = player.belt[0]
		elif (choice == '3'):
			caught = player.view_pack(in_wild=True)
			time.sleep(1.5)

	if (not player.has_pkmn()):
		print(f"\n%s is out of useable Pokemon!\n%s blacked out!" % (player.name, player.name))
		return False
	elif (opponent_pkmn.ko):
		print(f"\n%s defeated %s!" % (player.name, opponent_pkmn.name))
		# print(f"%s got %dg for winning." % (player.name, opponent.wallet))
		# player.wallet += opponent.wallet
	elif (caught):
		print(f"Alright, you caught the %s!" % opponent_pkmn.name)
		if (len(player.belt) < 6):
			player.belt.append(opponent_pkmn)
		else:
			print(f"You upload the caught %s to your PokeCloud storage device." % opponent_pkmn.name)
		time.sleep(1.5)
	return True


def trainer_battle():
	opponent = instantiate_opponent_trainer()

	# commence battle
	print(f"Go, %s!" % player.belt[0].name)
	player_pkmn = player.belt[0]
	opponent_pkmn = opponent.belt[0]

	# battle loop
	while (opponent.has_pkmn() and player.has_pkmn()):
		print()
		display_belt(opponent, opponent_pkmn)
		display_belt(player, player_pkmn)
		choice = input("1) Attack\n2) Switch\n3) Use item\n")
		if (choice == '1'):
			player_pkmn.attack(opponent_pkmn)
			if (opponent_pkmn.ko):
				print(f"Enemy %s has fainted!" % opponent_pkmn.name)
				player_pkmn.xp += 1
				if player_pkmn.xp == 4:
					player_pkmn.level_up()
				if (opponent.has_pkmn()):
					opponent_pkmn = rd.choice([pk for pk in opponent.belt if (not pk.ko)])
					print(f"%s sends out %s." % (opponent.name, opponent_pkmn.name))
				else:
					continue
			else:
				opponent_pkmn.attack(player_pkmn)
			if (player_pkmn.ko):
				print(f"\n%s has fainted!" % player_pkmn.name)
				if (player.has_pkmn()):
					print("Choose next pokemon:")
					player.swap_pkmn()
					player_pkmn = player.belt[0]
		elif (choice == '2'):
			player.swap_pkmn()
			player_pkmn = player.belt[0]
		elif (choice == '3'):
			player.view_pack()

	if (not player.has_pkmn()):
		print(f"\n%s is out of useable Pokemon!\n%s blacked out!" % (player.name, player.name))
		return False
	elif (not opponent.has_pkmn()):
		print(f"\n%s defeated %s!" % (player.name, opponent.name))
		print(f"%s got %dg for winning." % (player.name, opponent.wallet))
		player.wallet += opponent.wallet
	return True


def shop():
	stock_d = {"1": {"name": "potion", "cost": 10},
	         "2": {"name": "revive", "cost": 30},
	         "3": {"name": "pokeball", "cost": 100},
	         "4": {"name": "ultraball", "cost": 1000}}
	print(f"PokeCenter:       (You have %dg)" % player.wallet)
	for str_num, dyct in stock_d.items():
		print(f"%s) %s - %dg" % (str_num, dyct["name"], dyct["cost"]))
	print("What would you like to buy?")
	# print("1) potion - 10g\n2) revive - 30g")
	item_choice = input()
	if (item_choice in stock_d):
		print("How many?")
		print("1) 1\n2) 10\n3) max")
		quantity_choice = input()
		purchase(stock_d[item_choice], quantity_choice)
	print("Thank you.")


def purchase(item, quantity):
	if (quantity == '1' and player.wallet >= item["cost"]):
		player.pack[item["name"]] = player.pack.get(item["name"], 0) + 1
		player.wallet -= item["cost"]
	elif (quantity == '2' and player.wallet >= item["cost"] * 10):
		player.pack[item["name"]] = player.pack.get(item["name"], 0) + 10
		player.wallet -= item["cost"] * 10
	elif (quantity == '3'):
		player.pack[item["name"]] = player.pack.get(item["name"], 0) + player.wallet / item["cost"]
		player.wallet = player.wallet % item["cost"]


def main():
	print("Welcome to the world of Pokemon! Professor Oak is out, but let me take your name down anyway.")
	player.name = input()
	print(f"Great, so your name is %s." % player.name)
	print("Look, it's my first day, and with the professor out of the lab right now..."
	      "you know what, just take these three pokeballs. I'm sure it'll be fine.\n")
	player.belt.extend([Pokemon("Bulbasaur", 5, ['grass']),
	                    Pokemon("Charmander", 5, ['fire']),
	                    Pokemon("Squirtle", 5, ['water'])])
	print("(You slot the pokeballs into your belt, and leave the lab before someone notices.)")

	playing = True
	while playing:
		choice = input("\nWhat would you like to do?\n"
		               "1) Search tall grass\n"
		               "2) Trainer Battle\n"
		               "3) Pokemon\n"
		               "4) Pack\n"
		               "5) Shop\n"
		               "6) Quit\n")
		if (choice == '1'):
			playing = wild_battle()
		elif (choice == '2'):
			playing = trainer_battle()
		elif (choice == '3'):
			player.view_pkmn()
		elif (choice == '4'):
			player.view_pack()
		elif (choice == '5'):
			shop()
		elif (choice == '6'):
			playing = False
	print(f"You completed %.2f%% of your pokedex. Good enough!" % (rd.randint(0, 15) * 0.1))

main()
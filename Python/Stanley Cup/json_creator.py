import csv
from utility import *
from colour_utility import *

file_name = "past winners.csv"
dataset_001 = "dataset_nhl_team_wins.json"
dataset_002 = "dataset_nhl_team_losses.json"
dataset_003 = "dataset_nhl_team_apperances.json"
# skip 2005 back fill

with open(file_name) as csv_file:
	lines = csv.DictReader(csv_file)
	data_by_year = {}
	header = lines.fieldnames
	print("header", header)
	last = None
	for i, line in enumerate(lines):
		if last is not None:
			if any([val is None or val == "" for val in line.values()]):
				#print("missing values, check last:", last)
				if line["Year"] == "2005":
					continue
				for last_key, curr_key in zip(last, line):
					last_val = last[last_key]
					curr_val = line[curr_key]
					if curr_val is None or curr_val == "":
						line[curr_key] = last_val
			
		line["Winning Team"] = line["Winning Team"].split("(")[0].strip()
		line["Losing Team"] = line["Losing Team"].split("(")[0].strip()
		print(dict_print(line))
		data_by_year[str(line["Year"])] = line
		if 0 < i:
			last = line
	
	data_by_year = {k:v for k, v in data_by_year.items() if "1900" <= k}
	
	print(dict_print(data_by_year, "data_by_year"))
	data_by_team = {}
	data_by_coach = {}
	first_year = None
	last_year = None
	for key, val in data_by_year.items():
		year = int(key)
		if first_year is None:
			first_year = year
		if last_year is None or year > last_year:
			last_year = year
			
		w_team = val["Winning Team"]
		l_team = val["Losing Team"]
		if w_team not in data_by_team:
			data_by_team[w_team] = {"WYear": [], "LYear": [], "appearances": 0}
		if l_team not in data_by_team:
			data_by_team[l_team] = {"WYear": [], "LYear": [], "appearances": 0}
			
		data_by_team[w_team]["WYear"].append(key)
		data_by_team[l_team]["LYear"].append(key)
		data_by_team[w_team]["appearances"] += 1
		data_by_team[l_team]["appearances"] += 1
		data_by_team[w_team]["W% (per appearance)"] = len(data_by_team[w_team]["WYear"]) / data_by_team[w_team]["appearances"]
		data_by_team[l_team]["W% (per appearance)"] = len(data_by_team[l_team]["WYear"]) / data_by_team[l_team]["appearances"]
		data_by_team[l_team]["L% (per appearance)"] = len(data_by_team[l_team]["LYear"]) / data_by_team[l_team]["appearances"]
		data_by_team[w_team]["L% (per appearance)"] = len(data_by_team[w_team]["LYear"]) / data_by_team[w_team]["appearances"]
		
			
		w_coach = val["WCoach"]
		l_coach = val["LCoach"]
		if w_coach not in data_by_coach:
			data_by_coach[w_coach] = {"WYear": [], "LYear": [], "appearances": 0}
		if l_coach not in data_by_coach:
			data_by_coach[l_coach] = {"WYear": [], "LYear": [], "appearances": 0}
			
		data_by_coach[w_coach]["WYear"].append(key)
		data_by_coach[l_coach]["LYear"].append(key)
		data_by_coach[w_coach]["appearances"] += 1
		data_by_coach[l_coach]["appearances"] += 1
		data_by_coach[w_coach]["W% (per appearance)"] = percent(len(data_by_coach[w_coach]["WYear"]) / data_by_coach[w_coach]["appearances"])
		data_by_coach[l_coach]["W% (per appearance)"] = percent(len(data_by_coach[l_coach]["WYear"]) / data_by_coach[l_coach]["appearances"])
		data_by_coach[l_coach]["L% (per appearance)"] = percent(len(data_by_coach[l_coach]["LYear"]) / data_by_coach[l_coach]["appearances"])
		data_by_coach[w_coach]["L% (per appearance)"] = percent(len(data_by_coach[w_coach]["LYear"]) / data_by_coach[w_coach]["appearances"])
	                                                                                                                                                                                        
	teams_list = list(data_by_team.keys())
	teams_list.sort()
	for team in data_by_team:
		w_list = data_by_team[team]["WYear"]
		l_list = data_by_team[team]["LYear"]
		data_by_team[team]["Appearance % ({} to {})".format(first_year, last_year)] = percent((len(w_list) + len(l_list)) / (last_year - first_year))
		data_by_team[team]["Appearance W% ({} to {})".format(first_year, last_year)] = percent(len(w_list) / (last_year - first_year))
		data_by_team[team]["Appearance L% ({} to {})".format(first_year, last_year)] = percent(len(l_list) / (last_year - first_year))
		#data_by_team[team]["won_against"] = []
		#data_by_team[team]["lost_against"] = []
		greatest_rival = None
		most_lost_to = None
		most_won_against = None
		for team_b in teams_list:
			# if team != team_b:
			if team_b not in data_by_team[team]:
				data_by_team[team][team_b] = {"won_against": [], "lost_against": []}
			for year in data_by_team[team]["WYear"]:
				if data_by_year[year]["Losing Team"] == team_b:
					data_by_team[team][team_b]["won_against"].append(year)
			for year in data_by_team[team]["LYear"]:
				if data_by_year[year]["Winning Team"] == team_b:
					data_by_team[team][team_b]["lost_against"].append(year)
					
			if greatest_rival is None:
				greatest_rival = (team_b, data_by_team[team][team_b]["won_against"] + data_by_team[team][team_b]["lost_against"])
			elif len(data_by_team[team][team_b]["won_against"]) + len(data_by_team[team][team_b]["lost_against"]) > len(greatest_rival[1]):
				greatest_rival = (team_b, data_by_team[team][team_b]["won_against"] + data_by_team[team][team_b]["lost_against"])
			elif len(data_by_team[team][team_b]["won_against"]) + len(data_by_team[team][team_b]["lost_against"]) == len(greatest_rival[1]):
				if data_by_team[team][team_b]["won_against"] + data_by_team[team][team_b]["lost_against"]:
					if max(data_by_team[team][team_b]["won_against"] + data_by_team[team][team_b]["lost_against"]) > max(greatest_rival[1]):
						greatest_rival = (team_b, data_by_team[team][team_b]["won_against"] + data_by_team[team][team_b]["lost_against"])
				
			if most_lost_to is None:
				most_lost_to = (team_b, data_by_team[team][team_b]["lost_against"])
			elif len(data_by_team[team][team_b]["lost_against"]) > len(most_lost_to[1]):
				most_lost_to = (team_b, data_by_team[team][team_b]["lost_against"])
			elif len(data_by_team[team][team_b]["lost_against"]) == len(most_lost_to[1]):
				if data_by_team[team][team_b]["lost_against"]:
					if max(data_by_team[team][team_b]["lost_against"]) > max(most_lost_to[1]):
						most_lost_to = (team_b, data_by_team[team][team_b]["lost_against"])
				
			if most_won_against is None:
				most_won_against = (team_b, data_by_team[team][team_b]["won_against"])
			elif len(data_by_team[team][team_b]["won_against"]) > len(most_won_against[1]):
				most_won_against = (team_b, data_by_team[team][team_b]["won_against"])
			elif len(data_by_team[team][team_b]["won_against"]) == len(most_won_against[1]):
				if data_by_team[team][team_b]["won_against"]:
					if max(data_by_team[team][team_b]["won_against"]) > max(most_won_against[1]):
						most_won_against = (team_b, data_by_team[team][team_b]["won_against"])
					
		data_by_team[team]["greatest_rival"] = greatest_rival
		if most_lost_to[1]:
			data_by_team[team]["most_lost_to"] = most_lost_to
		if most_won_against[1]:
			data_by_team[team]["most_won_against"] = most_won_against
	print(dict_print(data_by_team, "Data By Team"))     
	print("parsed teams:\n", "\n".join(teams_list))
	
	
	##################################################################################################################
	##################################################################################################################
	##################################################################################################################
	##################################################################################################################

	
	tab_depth = 0
	
	def tdp():
		return tab_depth * "\t"
		
	def ooj(use_tab=True):
		global tab_depth
		tab_depth += 1
		return ((tab_depth - 1) * "\t" if use_tab else "") + "{\n"
		
	def coj(next=False):
		global tab_depth
		tab_depth -= 1
		return "\n" + max(0, tab_depth) * "\t" + "}" + ("," if next else "")
		
	def okey(k_name, new_line=True):
		return ("\n" if new_line else "") + tdp() + f"\"{k_name}\": " + ooj(use_tab=False)
		
	def ckey(next=False):
		return tdp() + coj(next=next)
		
	def wkv(k, v, next=True, new_line=True):
		x = "\"" if isinstance(v, str) else ""
		if v == "null":
			x = ""
		return "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t=tdp(), k=k, v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
		
	team_counts = dict(zip(teams_list, [0 for _ in teams_list]))
	with open(dataset_001, "w") as d1json:
		d1json.write(ooj())
		d1json.write(okey("ENTITIES", new_line=False))
		for i, team_name in enumerate(teams_list):
			d1json.write(okey(team_name))
			d1json.write(wkv("name", team_name))
			d1json.write(wkv("colour", random_colour(name=True)))
			d1json.write(wkv("image_path", "null", next=False))
			d1json.write(ckey(next=(i != len(teams_list) - 1)))
		d1json.write(ckey(next=True))
		for i, year_year_dat in enumerate(data_by_year.items()):
			year, year_dat = year_year_dat
			team_counts[year_dat["Winning Team"]] += 1
			d1json.write(okey(year))
			for j, team_name in enumerate(teams_list):
				d1json.write(wkv(team_name, team_counts[team_name], next=(j != len(teams_list) - 1)))
			d1json.write(ckey(next=(i != len(data_by_year) - 1)))
		d1json.write(coj())
	
	team_counts = dict(zip(teams_list, [0 for _ in teams_list]))
	with open(dataset_002, "w") as d2json:
		d2json.write(ooj())
		d2json.write(okey("ENTITIES", new_line=False))
		for i, team_name in enumerate(teams_list):
			d2json.write(okey(team_name))
			d2json.write(wkv("name", team_name))
			d2json.write(wkv("colour", random_colour(name=True)))
			d2json.write(wkv("image_path", "null", next=False))
			d2json.write(ckey(next=(i != len(teams_list) - 1)))
		d2json.write(ckey(next=True))
		for i, year_year_dat in enumerate(data_by_year.items()):
			year, year_dat = year_year_dat
			team_counts[year_dat["Losing Team"]] += 1
			d2json.write(okey(year))
			for j, team_name in enumerate(teams_list):
				d2json.write(wkv(team_name, team_counts[team_name], next=(j != len(teams_list) - 1)))
			d2json.write(ckey(next=(i != len(data_by_year) - 1)))
		d2json.write(coj())
	
	team_counts = dict(zip(teams_list, [0 for _ in teams_list]))
	with open(dataset_003, "w") as d3json:
		d3json.write(ooj())
		d3json.write(okey("ENTITIES", new_line=False))
		for i, team_name in enumerate(teams_list):
			d3json.write(okey(team_name))
			d3json.write(wkv("name", team_name))
			d3json.write(wkv("colour", random_colour(name=True)))
			d3json.write(wkv("image_path", "null", next=False))
			d3json.write(ckey(next=(i != len(teams_list) - 1)))
		d3json.write(ckey(next=True))
		for i, year_year_dat in enumerate(data_by_year.items()):
			year, year_dat = year_year_dat
			team_counts[year_dat["Winning Team"]] += 1
			team_counts[year_dat["Losing Team"]] += 1
			d3json.write(okey(year))
			for j, team_name in enumerate(teams_list):
				d3json.write(wkv(team_name, team_counts[team_name], next=(j != len(teams_list) - 1)))
			d3json.write(ckey(next=(i != len(data_by_year) - 1)))
		d3json.write(coj())
					
	
	##################################################################################################################
	##################################################################################################################
	##################################################################################################################
	##################################################################################################################

	
	for coach in data_by_coach:
		w_list = data_by_coach[coach]["WYear"]
		l_list = data_by_coach[coach]["LYear"]
		data_by_coach[coach]["Appearance % ({} to {})".format(first_year, last_year)] = (len(w_list) + len(l_list)) / (last_year - first_year)
		data_by_coach[coach]["Appearance W% ({} to {})".format(first_year, last_year)] = len(w_list) / (last_year - first_year)
		data_by_coach[coach]["Appearance L% ({} to {})".format(first_year, last_year)] = len(l_list) / (last_year - first_year)
	print(dict_print(data_by_coach, "Data By Team"))
	coaches_list = list(data_by_coach.keys())
	coaches_list.sort()
	print("parsed coaches:\n", "\n".join(coaches_list))
	# count # time each team / coach has won.
	# count # time each team met and won/lost against each other team.
	# count # GWG -> period, timeOfPeriod
	
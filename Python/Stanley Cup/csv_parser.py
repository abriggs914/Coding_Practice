import csv
from utility import *

file_name = "past winners.csv"
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
	
	data_by_year = {k:v for k, v in data_by_year.items() if "1995" <= k}
	
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
	
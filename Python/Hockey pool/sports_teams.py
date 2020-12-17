import csv

# Python program to analyze north american professional sports clubs found at:
# https://en.wikipedia.org/wiki/List_of_professional_sports_teams_in_the_United_States_and_Canada
# Question was originally how many NHL teams are non plural?
#
# July 2020

team_stats = {}
try:
	with open("sports_teams.csv") as teams_file:
		teams_dict = csv.DictReader(teams_file, delimiter='%')
		header = teams_dict.fieldnames
		for row in teams_dict:
			name = row[header[0]].strip()
			location = row[header[1]].strip()
			arena = row[header[2]].strip()
			team_stats[name] = dict(zip(list(map(str.strip, header[1:])), [location, arena]))
		# print(team_stats)
except:
	print("error parsing")
	
if not team_stats:
	print("File was not correctly parsed")
	quit()
	
team_names = list(map(str.title, team_stats.keys()))

def teams_from_place(place):
	p = place.lower()
	return [team for team in team_stats if p in team_stats[team]["Location"].lower()]
	
def non_plural_teams():
	return [team for team in team_stats if len([word for word in team.split()[-2:] if word.lower().endswith("s")]) == 0]


# Stats
print("Teams from New Brunswick:\n\t", teams_from_place("new brunswick"))
print("Non-plural team names:\n\t", non_plural_teams())
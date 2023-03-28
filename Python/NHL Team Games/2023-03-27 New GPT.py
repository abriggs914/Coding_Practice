import random
from itertools import combinations

from utility import clamp

# Define the teams by division
metropolitan_teams = ["Carolina", "New Jersey", "NY Rangers", "Washington", "NY Islanders", "Pittsburgh",
                      "Philadelphia", "Columbus"]
atlantic_teams = ["Boston", "Toronto", "Tampa Bay", "Buffalo", "Florida", "Detroit", "Ottawa", "Montreal"]
central_teams = ["Winnipeg", "Dallas", "Minnesota", "Colorado", "St. Louis", "Nashville", "Arizona", "Chicago"]
pacific_teams = ["Vegas", "Seattle", "Los Angeles", "Edmonton", "Calgary", "Vancouver", "San Jose", "Anaheim"]

# Create a list of all teams
all_teams = metropolitan_teams + atlantic_teams + central_teams + pacific_teams

# Define the number of games to play against each team
num_division_games = 4
num_non_division_games = 2
num_left_over_games = 6
num_rival_games = 1
num_teams = len(all_teams) - 1

# Generate the schedule
schedule = {}
for team in all_teams:
    # Initialize the list of opponents for the current team
    opponents = []

    # Add the division opponents
    # division = team.split()[0]
    # print(f"{division=}, {team=}")
    if team in metropolitan_teams:
        division_teams = metropolitan_teams
    elif team in atlantic_teams:
        division_teams = atlantic_teams
    elif team in central_teams:
        division_teams = central_teams
    else:
        division_teams = pacific_teams

    for division_team in division_teams:
        if division_team != team:
            for i in range(num_division_games):
                opponents.append(division_team)

    # Add the non-division opponents
    non_division_teams = set(all_teams) - set(division_teams) - {team,}
    for non_division_team in non_division_teams:
        for i in range(num_non_division_games):
            opponents.append(non_division_team)

    # # Add the r['Arizona', 'Arizona', 'Arizona', 'Boston', 'Boston', 'Boston', 'Buffalo', 'Buffalo', 'Buffalo', 'Calgary', 'Calgary', 'Calgary', 'Calgary', 'Carolina', 'Carolina', 'Carolina', 'Chicago', 'Chicago', 'Chicago', 'Colorado', 'Colorado', 'Colorado', 'Columbus', 'Columbus', 'Columbus', 'Dallas', 'Dallas', 'Dallas', 'Detroit', 'Detroit', 'Detroit', 'Edmonton', 'Edmonton', 'Edmonton', 'Edmonton', 'Florida', 'Florida', 'Florida', 'Los Angeles', 'Los Angeles', 'Los Angeles', 'Los Angeles', 'Minnesota', 'Minnesota', 'Minnesota', 'Montreal', 'Montreal', 'Montreal', 'NY Islanders', 'NY Islanders', 'NY Islanders', 'NY Rangers', 'NY Rangers', 'NY Rangers', 'Nashville', 'Nashville', 'Nashville', 'New Jersey', 'New Jersey', 'New Jersey', 'Ottawa', 'Ottawa', 'Ottawa', 'Philadelphia', 'Philadelphia', 'Philadelphia', 'Pittsburgh', 'Pittsburgh', 'Pittsburgh', 'San Jose', 'San Jose', 'San Jose', 'San Jose', 'Seattle', 'Seattle', 'Seattle', 'Seattle', 'St. Louis', 'St. Louis', 'St. Louis', 'Tampa Bay', 'Tampa Bay', 'Tampa Bay', 'Toronto', 'Toronto', 'Toronto', 'Vancouver', 'Vancouver', 'Vancouver', 'Vancouver', 'Vegas', 'Vegas', 'Vegas', 'Vegas', 'Washington', 'Washington', 'Washington', 'Winnipeg', 'Winnipeg', 'Winnipeg']n_division_team)

    # # Add the rivalry game
    # rivals = random.sample(list(non_division_teams), num_left_over_games)
    # # rivals = random.sample()
    # for rival in rivals:
    #     opponents.append(rival)
    #     non_division_teams.remove(rival)

    # # Add the remaining non-division opponents
    # for non_division_team in non_division_teams:
    #     for i in range(num_rival_games):
    #         opponents.append(non_division_team)
    #
    # # Shuffle the list of opponents
    # random.shuffle(opponents)

    # Shuffle the list of opponents
    # random.shuffle(opponents)
    opponents.sort()

    # Add the schedule to the dictionary
    schedule[team] = opponents


# Print the schedule
for team, opponents in schedule.items():
    print(f"{team.ljust(14)}: l={str(len(opponents)).ljust(4)} | {opponents}")


tt = [t for t in all_teams]
print(f"{tt=}")
while tt:
    team = random.sample(tt, 1)[0]

    if team in metropolitan_teams:
        division_teams = metropolitan_teams
    elif team in atlantic_teams:
        division_teams = atlantic_teams
    elif team in central_teams:
        division_teams = central_teams
    else:
        division_teams = pacific_teams

    non_division_teams = list(set(tt) - set(division_teams) - {team,})
    k = clamp(0, 82 - len(schedule[team]), 6)
    print(f"{team.ljust(12)}, l={len(non_division_teams)}, {k=}, {non_division_teams=}")
    opponents = random.sample(non_division_teams, k=k)
    print(f"\t{team.ljust(12)}, l={len(opponents)}, {opponents=}")
    schedule[team] = schedule[team] + opponents
    for t in opponents:
        schedule[t] = schedule[t] + [team]
        if len(schedule[t]) >= 82:
            print(f"{t.rjust(12)} l={len(schedule[t])} FINISHED B")
            tt.remove(t)
    tt.remove(team)
    print(f"{team.rjust(12)} l={len(schedule[team])} FINISHED A")


# for i in range(0, len(all_teams), 2):

all_games = []
# Print the schedule
for team, opponents in schedule.items():
    print(f"{team.ljust(14)}: l={str(len(opponents)).ljust(4)} | {opponents}")
    for opp in opponents:
        all_games.append((team, opp))

print(f"length: {len(all_games)}")


u_games = []
v_teams = set()
for team, opponents in schedule.items():
    print(f"{team.ljust(14)}: l={str(len(opponents)).ljust(4)} | {opponents}")
    for opp in opponents:
        if opp not in v_teams:
            u_games.append((team, opp))
    v_teams.add(team)

print(f"length: l={len(u_games)}\n{u_games}")
with open("2023-03-28 Season Output.txt", "w") as f:
    for team_a, team_b in u_games:
        f.write(f"'{team_a}', '{team_b}'\n")


# import random
# from itertools import combinations
#
# # Define the teams by division
# metropolitan_teams = ["Carolina", "New Jersey", "NY Rangers", "Washington", "NY Islanders", "Pittsburgh",
#                       "Philadelphia", "Columbus"]
# atlantic_teams = ["Boston", "Toronto", "Tampa Bay", "Buffalo", "Florida", "Detroit", "Ottawa", "Montreal"]
# central_teams = ["Winnipeg", "Dallas", "Minnesota", "Colorado", "St. Louis", "Nashville", "Arizona", "Chicago"]
# pacific_teams = ["Vegas", "Seattle", "Los Angeles", "Edmonton", "Calgary", "Vancouver", "San Jose", "Anaheim"]
#
# # Create a list of all teams
# all_teams = metropolitan_teams + atlantic_teams + central_teams + pacific_teams
#
# # Define the number of games to play against each team
# num_division_games = 4
# num_non_division_games = 2
# num_rival_games = 1
# num_teams = len(all_teams) - 1
#
# # Generate the schedule
# schedule = {}
# for team in all_teams:
#     # Initialize the list of opponents for the current team
#     opponents = []
#
#     # Add the division opponents
#     division = team.split()[0]
#     if division == "Carolina":
#         division_teams = metropolitan_teams
#     elif division == "Boston":
#         division_teams = atlantic_teams
#     elif division == "Winnipeg":
#         division_teams = central_teams
#     else:
#         division_teams = pacific_teams
#
#     for division_team in division_teams:
#         if division_team != team:
#             for i in range(num_division_games):
#                 opponents.append(division_team)
#
#     # Add the non-division opponents
#     non_division_teams = set(all_teams) - set(division_teams) - set([team])
#     for non_division_team in non_division_teams:
#         for i in range(num_non_division_games):
#             opponents.append(non_division_team)
#
#     # # Add the rivalry game
#     # rival = random.choice(list(non_division_teams))
#     # opponents.append(rival)
#     # non_division_teams.remove(rival)
#     #
#     # # Add the remaining non-division opponents
#     # for non_division_team in non_division_teams:
#     #     for i in range(num_rival_games):
#     #         opponents.append(non_division_team)
#
#     # Shuffle the list of opponents
#     # random.shuffle(opponents)
#     opponents.sort()
#
#     # Add the schedule to the dictionary
#     schedule[team] = opponents
#
# # Print the schedule
# for team, opponents in schedule.items():
#     print(f"{team.ljust()}: l={str(len(opponents)).ljust(4)} | {opponents}")
# NHL playoff clinching calculator

# Define the number of teams, divisions, and games in a season
num_teams = 32
num_divisions = 4
num_games = 82

# Define the number of playoff spots available in each division and conference
num_division_spots = 3
num_wildcard_spots = 2

# Define the number of points awarded for each type of game outcome
win_points = 2
ot_loss_points = 1
reg_loss_points = 0

# Define the current standings for each team
# The standings should be a list of tuples, where each tuple represents a team and their current points total
# For example: [("Team A", 90), ("Team B", 88), ("Team C", 86), ...]
divisions = [
    "Division A",
    "Division B",
    "Division C",
    "Division D"
]

conferences = [
    divisions[:2],
    divisions[2:]
]

standings = [(f"Team {chr(65 + i)}", 0, divisions[i // (num_teams // len(divisions))]) for i in range(num_teams)]

# Define a function to calculate the maximum number of points that a team can earn in their remaining games
def max_points_remaining(points, games_left):
    return points + (win_points * games_left)

# Define a function to calculate the maximum number of points that the teams below a given team in the standings can earn
def max_points_below(standings, team_index):
    max_points = 0
    for i in range(team_index + 1, len(standings)):
        team_points = standings[i][1]
        games_left = (num_games * num_divisions) - (team_index * num_games)
        max_points += max_points_remaining(team_points, games_left)
    return max_points

# Define a function to calculate the number of points needed for a team to clinch a playoff spot
def clinching_points(standings, team_index):
    team_points = standings[team_index][1]
    max_points = max_points_below(standings, team_index)
    remaining_spots = num_division_spots + num_wildcard_spots - team_index % num_divisions
    return max_points - team_points + 1 if remaining_spots > 0 else 0

# Test the function with the current standings
for i, team in enumerate(standings):
    clinching_points_needed = clinching_points(standings, i)
    print(f"{team[0]} needs {clinching_points_needed} points to clinch a playoff spot")

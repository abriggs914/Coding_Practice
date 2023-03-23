from itertools import combinations
from utility import *


teams = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G"
    # ,
    # "H",
    # "I",
    # "J",
    # "K",
    # "L",
    # "M",
    # "N",
    # "O",
    # "P",
    # "Q",
    # "R",
    # "S",
    # "T",
    # "U",
    # "V",
    # "W",
    # "X",
    # "Y",
    # "Z",
    # "0",
    # "1",
    # "2",
    # "3",
    # "4",
    # "5"
]

all_games_schedule = combinations(teams, 2)
print(f"{all_games_schedule=}")

pts_reg_w = 2
pts_ot_w = 2
pts_reg_l = 0
pts_ot_l = 1

n_games = len(teams) - 1
max_points_per_game = max(
    pts_reg_w,
    pts_ot_w,
    pts_reg_l,
    pts_ot_l
)

season_standings = {
    team: {t: "" if t != team else "-" for t in ["#", *teams]}
    for team in teams
}

for i, team in enumerate(teams):
    season_standings[team].update({
        "#": i,
        " ": " ",
        "GP": 0,
        "PTS": 0,
        "W": 0,
        "L": 0,
        "OTW": 0,
        "OTL": 0,
        "GL": n_games,
        "MP": n_games * max_points_per_game
    })

for i, match_up in enumerate(all_games_schedule):
    team_a, team_b = match_up
    a_wins = randint(0, 1)
    in_ot = int(randint(0, 3) == 0)
    # season_standings[team_b][team_a] = 0 if a_wins else 1
    # season_standings[team_b]["GP"] += 1

    # print(f"Aold: {season_standings[team_a]['PTS']}, Bold: {season_standings[team_b]['PTS']}")
    a_pts = season_standings[team_a]["PTS"] + (pts_reg_w if a_wins and not in_ot else (pts_ot_w if a_wins and in_ot else (pts_reg_l if not a_wins and not in_ot else pts_ot_l)))
    b_pts = season_standings[team_b]["PTS"] + (pts_reg_l if a_wins and not in_ot else (pts_ot_l if a_wins and in_ot else (pts_reg_w if not a_wins and not in_ot else pts_ot_w)))
    # print(f"awins: {a_wins}, in_ot: {in_ot}")
    # print(f"Anew: {a_pts}, Bnew: {b_pts}")

    season_standings[team_a].update({
        team_b: a_wins,
        "GP": season_standings[team_a]["GP"] + 1,
        "PTS": a_pts,
        "W": season_standings[team_a]["W"] + (1 if a_wins else 0),
        "L": season_standings[team_a]["W"] + (0 if a_wins else 1),
        "OTW": season_standings[team_a]["OTW"] + (1 if a_wins and in_ot else 0),
        "OTL": season_standings[team_a]["OTL"] + (1 if not a_wins and in_ot else 0),
        "GL": season_standings[team_a]["GL"] - 1,
        "MP": a_pts + (season_standings[team_a]["GL"] - 1) * max_points_per_game
    })

    season_standings[team_b].update({
        team_a: 0 if a_wins else 1,
        "GP": season_standings[team_b]["GP"] + 1,
        "PTS": b_pts,
        "W": season_standings[team_b]["W"] + (0 if a_wins else 1),
        "L": season_standings[team_b]["W"] + (1 if a_wins else 0),
        "OTW": season_standings[team_b]["OTW"] + (1 if not a_wins and in_ot else 0),
        "OTL": season_standings[team_b]["OTL"] + (1 if a_wins and in_ot else 0),
        "GL": season_standings[team_b]["GL"] - 1,
        "MP": b_pts + (season_standings[team_b]["GL"] - 1) * max_points_per_game
    })

    sorted_standings = sorted(season_standings.keys(), key=lambda x: season_standings[x]['PTS'], reverse=True)
    sorted_standings = {team: season_standings[team] for team in sorted_standings}
    print(dict_print(sorted_standings, f"season standings GP = {i + 1}\n\t\t\tMatchup: '{team_a}' VS '{team_b}'"))

from itertools import combinations
from utility import *

metropolitan = {
    "Carolina": {"acr": "CAR"},
    "New Jersey": {"acr": "NJD"},
    "NY Rangers": {"acr": "NYR"},
    "Washington": {"acr": "WSH"},
    "NY Islanders": {"acr": "NYI"},
    "Pittsburgh": {"acr": "PIT"},
    "Philadelphia": {"acr": "PHI"},
    "Columbus": {"acr": "CBJ"}
}

atlantic = {
    "Boston": {"acr": "BOS"},
    "Toronto": {"acr": "TOR"},
    "Tampa Bay": {"acr": "TBL"},
    "Buffalo": {"acr": "BUF"},
    "Florida": {"acr": "FLA"},
    "Detroit": {"acr": "DET"},
    "Ottawa": {"acr": "OTT"},
    "Montreal": {"acr": "MTL"}
}

central = {
    "Winnipeg": {"acr": "WPG"},
    "Dallas": {"acr": "DAL"},
    "Minnesota": {"acr": "MIN"},
    "Colorado": {"acr": "COL"},
    "St. Louis": {"acr": "STL"},
    "Nashville": {"acr": "NSH"},
    "Arizona": {"acr": "ARI"},
    "Chicago": {"acr": "CHI"}
}

pacific = {
    "Vegas": {"acr": "VGK"},
    "Seattle": {"acr": "SEA"},
    "Los Angeles": {"acr": "LAK"},
    "Edmonton": {"acr": "EDM"},
    "Calgary": {"acr": "CGY"},
    "Vancouver": {"acr": "VAN"},
    "San Jose": {"acr": "SJS"},
    "Anaheim": {"acr": "ANA"}
}


def team_acr(team):
    if team in metropolitan:
        return metropolitan[team]["acr"]
    if team in central:
        return central[team]["acr"]
    if team in atlantic:
        return atlantic[team]["acr"]
    if team in pacific:
        return pacific[team]["acr"]


league = {
    "eastern": {
        "metropolitan": [metropolitan[t]["acr"] for t in metropolitan],
        "atlantic": [atlantic[t]["acr"] for t in atlantic]
    },
    "western": {
        "central": [central[t]["acr"] for t in central],
        "pacific": [pacific[t]["acr"] for t in pacific]
    }
}


print(f"{league}")
print(dict_print(league, "league"))

team_lookup = {}
for conf, division_data in league.items():
    for div, team_list in division_data.items():
        for team in team_list:
            team_lookup[team] = {"conf": conf, "div": div}

conferences = {k: v for k, v in league.items()}
divisions = flatten([[div for div in league[conf]] for conf in conferences])


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
n_game_per_division_rivals = 4
n_game_per_res_of_league = 2
n_games_per_rest_divs = 2

# n_games = len(teams) - 1
n_games = 82
max_points_per_game = max(
    pts_reg_w,
    pts_ot_w,
    pts_reg_l,
    pts_ot_l
)

#
# def gen_schedule_old(league_breakdown):
#     # team_lookup = {team: {"conf": conf, "div": league_breakdown[conf]} for conf in conferences for team in teams}
#
#     print(f"{conferences=}")
#     print(f"{divisions=}")
#     schedule = {}
#     schedule_c = {t: 0 for t in team_lookup}
#     schedule_p = list()
#     for i, team in enumerate(team_lookup):
#         conf = team_lookup[team]["conf"]
#         div = team_lookup[team]["div"]
#
#         rest_div_teams = rest_teams_div(team)
#         # rest_league_teams = rest_teams(team)
#         rest_league_teams = rest_teams_out_div(team)
#         rest_league_divs = rest_divs(div)
#         print(f"{team=}")
#         print(f"{rest_league_divs=}")
#         # schedule[team] =
#         for j in range(n_game_per_division_rivals):
#             for div_rival in rest_div_teams:
#                 # if (div_rival, team) not in schedule_p:
#                 schedule_c[team] += 1
#                 schedule_c[div_rival] += 1
#                 schedule_p.append((team, f"{div_rival}||A||{j + 1}"))
#
#         for j in range(n_game_per_res_of_league):
#             for div_rival in rest_league_teams:
#                 # if (div_rival, team) not in schedule_p:
#                 schedule_c[team] += 1
#                 schedule_c[div_rival] += 1
#                 schedule_p.append((team, f"{div_rival}||B||{j + 1}"))
#
#         for j in range(n_games_per_rest_divs):
#             for div_rival in rest_league_divs:
#                 rnd_team = choice([t for t in team_lookup if team_lookup[t]["div"] == div_rival])
#                 while schedule_c[rnd_team] >= (2 * 82):
#                     rnd_team = choice([t for t in team_lookup if team_lookup[t]["div"] == div_rival])
#                 # if (div_rival, team) not in schedule_p:
#                 schedule_c[team] += 1
#                 schedule_c[rnd_team] += 1
#                 schedule_p.append((team, f"{rnd_team}||C||{j + 1}"))
#
#         # print(f"{team=}, {conf=}, {div=}")
#         # print(f"{rest_conf(conf)=}")
#         # print(f"{rest_teams_conf(team)=}")
#         # print(f"{rest_divs(div)=}")
#         # print(f"{rest_teams_div(team)=}")
#     schedule_p.sort()
#     # schedule_p.sort(key=lambda tup: tup)
#     print_by_line(schedule_p)
#     print(f"total length: {len(schedule_p)}")
#     return schedule_p
#

def gen_schedule(league_breakdown):
    # team_lookup = {team: {"conf": conf, "div": league_breakdown[conf]} for conf in conferences for team in teams}

    print(f"{conferences=}")
    print(f"{divisions=}")
    schedule = {}
    schedule_c = {t: 0 for t in team_lookup}
    schedule_p = list()
    i = 0
    tl = list(team_lookup)
    while team_lookup:
        team = tl[i]
        conf = team_lookup[team]["conf"]
        div = team_lookup[team]["div"]

        rest_conf = lambda conf_in: [conf for conf in conferences if conf != conf_in]
        rest_divs = lambda div_in: [div for div in divisions if div != div_in]
        rest_teams = lambda team_in: [team for team in team_lookup if team_in != team]
        rest_teams_conf = lambda team_in: [team for team in team_lookup if
                                           team_in != team and team_lookup[team]["conf"] == team_lookup[team_in][
                                               "conf"]]
        rest_teams_div = lambda team_in: [team for team in team_lookup if
                                          team_in != team and team_lookup[team]["div"] == team_lookup[team_in]["div"]]
        rest_teams_out_div = lambda team_in: [team for team in team_lookup if
                                              team_in != team and team_lookup[team]["div"] != team_lookup[team_in][
                                                  "div"]]
        teams_in_div = lambda div_in: [team for team in team_lookup if
                                       team_lookup[team]["div"] == div_in]
        teams_in_conf = lambda conf_in: [team for team in team_lookup if
                                         team_lookup[team]["conf"] == conf_in]

        rest_div_teams = rest_teams_div(team)
        # rest_league_teams = rest_teams(team)
        rest_league_teams = rest_teams_out_div(team)
        rest_league_divs = rest_divs(div)
        print(f"{team=}")
        print(f"{rest_league_divs=}")
        # schedule[team] =
        for j in range(n_game_per_division_rivals):
            for div_rival in rest_div_teams:
                # if (div_rival, team) not in schedule_p:
                schedule_c[team] += 1
                schedule_c[div_rival] += 1
                schedule_p.append((team, f"{div_rival}||A||{j + 1}"))

        for j in range(n_game_per_res_of_league):
            for div_rival in rest_league_teams:
                # if (div_rival, team) not in schedule_p:
                schedule_c[team] += 1
                schedule_c[div_rival] += 1
                schedule_p.append((team, f"{div_rival}||B||{j + 1}"))

        for j in range(n_games_per_rest_divs):
            for div_rival in rest_league_divs:
                print(f"{team_lookup=}")
                r_list = [t for t in team_lookup if team_lookup[t]['div'] == div_rival]
                print(f"{r_list=}")
                if r_list:
                    rnd_team = choice(r_list)
                    while schedule_c[rnd_team] >= (2 * 82):
                        rnd_team = choice([t for t in team_lookup if team_lookup[t]["div"] == div_rival])
                    # if (div_rival, team) not in schedule_p:
                    schedule_c[team] += 1
                    schedule_c[rnd_team] += 1
                    schedule_p.append((team, f"{rnd_team}||C||{j + 1}"))

        # print(f"{team=}, {conf=}, {div=}")
        # print(f"{rest_conf(conf)=}")
        # print(f"{rest_teams_conf(team)=}")
        # print(f"{rest_divs(div)=}")
        # print(f"{rest_teams_div(team)=}")
        i += 1
        del team_lookup[team]
        if not team_lookup:
            break

    schedule_p.sort()

    schedule_p = schedule_p[:len(schedule_p) // 2]

    # schedule_p.sort(key=lambda tup: tup)
    print_by_line(schedule_p)
    print(f"total length: {len(schedule_p)}")
    return schedule_p


teams = list(team_lookup)
all_games_schedule = gen_schedule(league)


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
    team_b = team_b.split("||")[0]
    a_wins = randint(0, 1)
    in_ot = int(randint(0, 3) == 0)
    # season_standings[team_b][team_a] = 0 if a_wins else 1
    # season_standings[team_b]["GP"] += 1

    # print(f"Aold: {season_standings[team_a]['PTS']}, Bold: {season_standings[team_b]['PTS']}")
    a_pts = season_standings[team_a]["PTS"] + (pts_reg_w if a_wins and not in_ot else (
        pts_ot_w if a_wins and in_ot else (pts_reg_l if not a_wins and not in_ot else pts_ot_l)))
    b_pts = season_standings[team_b]["PTS"] + (pts_reg_l if a_wins and not in_ot else (
        pts_ot_l if a_wins and in_ot else (pts_reg_w if not a_wins and not in_ot else pts_ot_w)))
    # print(f"awins: {a_wins}, in_ot: {in_ot}")
    # print(f"Anew: {a_pts}, Bnew: {b_pts}")

    # print(f"{season_standings[team_a][team_b]=}")
    # print(f"{season_standings[team_b][team_a]=}")
    season_standings[team_a].update({
        team_b: (season_standings[team_a][team_b] if season_standings[team_a][team_b] else 0) + a_wins,
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
        team_a: (season_standings[team_b][team_a] if season_standings[team_b][team_a] else 0) + (0 if a_wins else 1),
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
    if i == len(all_games_schedule) - 1:
        print(dict_print(sorted_standings, f"season standings GP = {i + 1}\n\t\t\tMatchup: '{team_a}' VS '{team_b}'"))

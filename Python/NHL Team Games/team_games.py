import random
from itertools import permutations, combinations


metropolitan = [
    "Carolina",
    "New Jersey",
    "NY Rangers",
    "Washington",
    "NY Islanders",
    "Pittsburgh",
    "Philadelphia",
    "Columbus"
]


atlantic = [
    "Boston",
    "Toronto",
    "Tampa Bay",
    "Buffalo",
    "Florida",
    "Detroit",
    "Ottawa",
    "Montreal"
]


central = [
    "Winnipeg",
    "Dallas",
    "Minnesota",
    "Colorado",
    "St. Louis",
    "Nashville",
    "Arizona",
    "Chicago"
]


pacific = [
    "Vegas",
    "Seattle",
    "Los Angeles",
    "Edmonton",
    "Calgary",
    "Vancouver",
    "San Jose",
    "Anaheim"
]


divisions = {
    "eastern": [
        metropolitan,
        atlantic
    ],
    "western": [
        central,
        pacific
    ]
}


def get_conf(team):
    if isinstance(team, int):
        team = assignments_teams[team]
    for conf, conf_divs in divisions.items():
        for div in conf_divs:
            if team in div:
                return conf


def get_division(team):
    if isinstance(team, int):
        team = assignments_teams[team]
    if team in divisions["eastern"][0]:
        return "metropolitan"
    if team in divisions["eastern"][1]:
        return "atlantic"
    if team in divisions["western"][0]:
        return "central"
    if team in divisions["western"][1]:
        return "pacific"


assignments_teams = dict(zip(range(32), metropolitan + atlantic + central + pacific))
assignments_teams_rev = dict(zip(metropolitan + atlantic + central + pacific, range(32)))
assignments_divisions = dict(zip(["metropolitan", "atlantic", "central", "pacific"], [0, 1, 0, 1]))


if __name__ == "__main__":
    teams = list(range(32))
    # everyones_games = permutations(teams, 3)
    # everyones_games = combinations(teams, 3)
    team_games = {}

    for i, team_a in enumerate(teams):
        for j in range(2):
            for k, team_b in enumerate(teams):
                if j == 0 and k == 0:
                    team_games[team_a] = []
                if team_a != team_b:
                    team_games[team_a].append(team_b)

    for i, team in enumerate(teams):
        team_name = assignments_teams[team]
        conf_name = get_conf(team)
        div_name = get_division(team)
        div_idx = assignments_divisions[div_name]
        rest_div = [t for t in divisions[conf_name][div_idx]]
        rest_conf = [t for t in divisions[conf_name][0] + divisions[conf_name][1]]
        print(f"===\n{i=}\n{team=}\n{team_name=}\n{conf_name=}\n{div_name=}\n{div_idx=}\n{rest_div=}\n{rest_conf=}\n===")
        rest_div.remove(team_name)
        rest_conf.remove(team_name)
        for team_b in rest_div:
            team_games[team].append(assignments_teams_rev[team_b])
            team_games[team].append(assignments_teams_rev[team_b])

        while 82 - len(team_games[team]) > 0:
            team_games[team].append(assignments_teams_rev[random.choice(rest_conf)])


    # print(f"{teams=}\n")
    # for team, vs_a, vs_b in everyones_games:
    #     print(f"\t{team=}, {vs_a=}, {vs_b=}")
    #     if team not in team_games:
    #         team_games[team] = []
    #     team_games[team].insert(vs_a, vs_a)
    #     team_games[team].insert(vs_b, vs_b)
    # print(f"{len(list(combinations(teams, 3)))=}")

    # print(f"{team_games=}")
    for k, v in team_games.items():
        print(f"{k=}, {len(v)=}, {v=}")
import datetime
import random
from collections import OrderedDict
from enum import Enum

import pandas as pd

from utility import dict_print, flatten, clamp, print_by_line, minmax, maxmin

schedule_template = [
    ["1 {conf_oal} {div_oal} {team_00} \\", 45, "/ {team_00} {div_oal} {conf_oal} 1",
     ["team_00", "div_oal", "conf_oal"]],
    ["8 {conf_oal} {div_oal} {team_07} /", 45, "\\ {team_08} {div_oal} {conf_oal} 8",
     ["team_07", "div_oal", "conf_oal"]]
]

template_1 = """
  N  |  CO  |  DO  |  DT  |  PT  |  TN  |   
{N}|{CO}|{DO}|{DT}|{PT}|{T} \\
                                      = 
{N}|{CO}|{DO}|{DT}|{PT}|{T} /      \\
                       = TOR
{N}|{CO}|{DO}|{DT}|{PT}|{T} \      /      \\
                = FLA         \\
{N}|{CO}|{DO}|{DT}|{PT}|{T} /               \
                                = TOR vs. VGK =
{N}|{CO}|{DO}|{DT}|{PT}|{T} \               /
                = WSH         /
{N}|{CO}|{DO}|{DT}|{PT}|{T} /      \      /
                       = CAR
{N}|{CO}|{DO}|{DT}|{PT}|{T} \      /
                = CAR
{N}|{CO}|{DO}|{DT}|{PT}|{T} /
""".strip()

data_1 = eval("""
[['TOR', 'atlantic', 'eastern', 'A__E_0', 0, 107, 0],
['CAR', 'metropolitan', 'eastern', 'M__E_0', 0, 106, 7],
['WSH', 'metropolitan', 'eastern', 'M__E_1', 1, 102, 4],
['TBL', 'atlantic', 'eastern', 'A__E_1', 1, 98, 2],
['PHI', 'metropolitan', 'eastern', 'M__E_2', 2, 98, 5],
['FLA', 'atlantic', 'eastern', 'A__E_2', 2, 98, 3],
['OTT', 'atlantic', 'eastern', 'WC_E_0', 6, 97, 6],
['MTL', 'atlantic', 'eastern', 'WC_E_1', 7, 97, 1],
['EDM', 'pacific', 'western', 'P__W_0', 0, 107, 0],
['NSH', 'central', 'western', 'C__W_0', 0, 100, 7],
['ARI', 'central', 'western', 'C__W_1', 1, 98, 4],
['SEA', 'pacific', 'western', 'P__W_1', 1, 98, 2],
['ANA', 'pacific', 'western', 'P__W_2', 2, 98, 3],
['WPG', 'central', 'western', 'C__W_2', 2, 93, 5],
['MIN', 'central', 'western', 'WC_W_0', 6, 93, 6],
['VAN', 'pacific', 'western', 'WC_W_1', 7, 93, 1]]
""".strip())

data = eval("""
[['TOR', 'atlantic', 'eastern', 'A__E_0', 0, 107, 0],
['CAR', 'metropolitan', 'eastern', 'M__E_0', 0, 106, 7],
['WSH', 'metropolitan', 'eastern', 'M__E_1', 1, 102, 4],
['TBL', 'atlantic', 'eastern', 'A__E_1', 1, 98, 2],
['PHI', 'metropolitan', 'eastern', 'M__E_2', 2, 98, 5],
['FLA', 'atlantic', 'eastern', 'A__E_2', 2, 98, 3],
['OTT', 'atlantic', 'eastern', 'WC_E_0', 6, 97, 6],
['MTL', 'atlantic', 'eastern', 'WC_E_1', 7, 97, 1],
['EDM', 'pacific', 'western', 'P__W_0', 0, 107, 0],
['NSH', 'central', 'western', 'C__W_0', 0, 100, 7],
['ARI', 'central', 'western', 'C__W_1', 1, 98, 4],
['SEA', 'pacific', 'western', 'P__W_1', 1, 98, 2],
['ANA', 'pacific', 'western', 'P__W_2', 2, 98, 3],
['WPG', 'central', 'western', 'C__W_2', 2, 93, 5],
['MIN', 'central', 'western', 'WC_W_0', 6, 93, 6],
['VAN', 'pacific', 'western', 'WC_W_1', 7, 93, 1]]
""".strip())


def draw_shedule(standings_in, half=None):
    team_list_data = OrderedDict()
    team_data = {}
    for i in range(len(standings_in)):
        print(f"{i=}")
        team = standings_in[i][0]
        team_list_data.update({
            f"team_{('00' + str(i))[-2:]}": team
        })
        team_data[team] = {
            'div_oal': standings_in[i][6],
            'conf_oal': i % 8
        }

    print(team_list_data)
    print(team_data)
    print(f"{team_list_data['team_00']=}")

    if not isinstance(half, str):
        half = ""
    result = ""
    for i, template_line in enumerate(schedule_template):
        left, n_spaces, right, keys = template_line
        fmts = dict(zip(keys, [v for k, v in team_list_data.items() if k in keys]))
        team = list(fmts.values())[0]
        print(f"A\n{left=}\n{n_spaces=}\n{right=}\n{keys=}\n{fmts=}")
        fmts.update({k: str(team_data[team][k]).center(3) for k in keys if k in team_data[team]})
        print(f"B\n{left=}\n{n_spaces=}\n{right=}\n{keys=}\n{fmts=}")
        left = left.format(**fmts)
        if half.lower() == "eastern":
            result += left
        # if half.lower() == "western":
        #     left = left.format(**fmts)
        #     print()
        # else:
        #     print()
        result += "\n"
    return result


def sched():
    header_l = "  N  |  CO |  DO |  DT  |  PT |  TN  "
    team_line_l = "{N}|{CO}|{DO}|{DT}|{PT}|{T} "
    header_r = "|".join(header_l.split("|")[::-1])
    team_line_r = "|".join(team_line_l.split("|")[::-1])
    results = ""
    lm = " " * (len(header_l) + 1)
    ms = " " * 53
    both_brackets = len(data_1) > 8
    times = 2 if both_brackets else 1
    data_1.sort(key=lambda tup: (tup[2], tup[-1]))
    ti = 0
    for i in range(1 + ((1 + (times % 2)) * 8)):
        if i == 0:
            results += header_l
            if both_brackets:
                results += ms + header_r
            results += "\n"

        else:

            minus = 0
            for j in range(times):
                tii = ti + (j * 8)
                print(f"ld={len(data_1)}, {i=}, {j=}, {ti=}, {tii=}")
                co_ = str(data_1[tii][4]).center(5)
                do_ = str(data_1[tii][-1]).center(5)
                dt_ = str(data_1[tii][3]).center(6)
                pt_ = str(data_1[tii][5]).center(5)
                tn_ = str(data_1[tii][0]).center(5)
                n_ = str(data_1[tii][6] + 1).center(5)
                if (i - 1) % 2 == 0:
                    suf = "\\" if j == 0 else "/"
                else:
                    suf = "/" if j == 0 else "\\"
                if j == 0:
                    results += team_line_l.format(CO=co_, DO=do_, DT=dt_, PT=pt_, T=tn_, N=n_) + f"{suf}"
                    if ti % 4 == 1:
                        results += f"{' ' * 6}\\"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 7
                    elif ti % 4 == 2:
                        results += f"{' ' * 6}/"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 7

                    if ti == 2:
                        results += f"{' ' * 7}\\"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 8
                        if both_brackets:
                            results += f"{' ' * 21}/"
                            minus += 22
                    elif ti == 3:
                        results += f"{' ' * 16}\\"
                        minus += 17
                        if both_brackets:
                            results += f"{' ' * 17}/"
                            minus += 18
                    elif ti == 4:
                        results += f"{' ' * 16}/"
                        minus += 17
                        if both_brackets:
                            results += f"{' ' * 17}\\"
                            minus += 18
                    elif ti == 5:
                        results += f"{' ' * 7}/"
                        minus += 8
                        if both_brackets:
                            results += f"{' ' * 21}\\"
                            minus += 22

                    if ti == 1:
                        if both_brackets:
                            results += f"{ms[:(len(ms) // 2) + 5]}{' ' * 6}/"
                            minus += 7 + len(ms[:(len(ms) // 2) + 5])
                    elif ti == 2:
                        if both_brackets:
                            results += f"{' ' * 7}\\"
                            minus += 8
                    elif ti == 5:
                        if both_brackets:
                            results += f"{' ' * 7}/"
                            minus += 8
                    elif ti == 6:
                        if both_brackets:
                            results += f"{ms[:(len(ms) // 2) + 5]}{' ' * 6}\\"
                            minus += 7 + len(ms[:(len(ms) // 2) + 5])
                else:
                    results += f"{ms[:len(ms) - (2 + minus)]}{suf}" + team_line_r.format(CO=co_, DO=do_, DT=dt_, PT=pt_,
                                                                                         T=tn_, N=n_)
                    minus = 0

            if i == 4:
                results += f"\n{lm}{ms[:(len(ms) // 2) - 8]}= ___ vs. ___ ="
            else:
                results += f"\n{lm}"
            if ti % 2 == 0:
                if ti == 0 or ti == 6:
                    results += f"= ___{ms[:(len(ms) // 2) + 15]}___ ="
                else:
                    if ti == 2:
                        results += f"= ___{' ' * 10}\\{ms[:(len(ms) // 4) + 6]}/{' ' * 10}___ ="
                    else:
                        results += f"= ___{' ' * 10}/{ms[:(len(ms) // 4) + 6]}\\{' ' * 10}___ ="
            elif ti % 4 == 1:
                results += f"{' ' * 8}= ___{ms[:(len(ms) // 4) + 12]}___ ="
            results += f"\n"
            ti += 1

    return results


def sched():
    header_l = "  N  |  CO |  DO |  DT  |  PT |  TN  "
    team_line_l = "{N}|{CO}|{DO}|{DT}|{PT}|{T} "
    header_r = "|".join(header_l.split("|")[::-1])
    team_line_r = "|".join(team_line_l.split("|")[::-1])
    results = ""
    lm = " " * (len(header_l) + 1)
    ms = " " * 53
    both_brackets = len(data_1) > 8
    times = 2 if both_brackets else 1
    data_1.sort(key=lambda tup: (tup[2], tup[-1]))
    ti = 0
    for i in range(1 + ((1 + (times % 2)) * 8)):
        if i == 0:
            results += header_l
            if both_brackets:
                results += ms + header_r
            results += "\n"

        else:

            minus = 0
            for j in range(times):
                tii = ti + (j * 8)
                print(f"ld={len(data_1)}, {i=}, {j=}, {ti=}, {tii=}")
                co_ = str(data_1[tii][4]).center(5)
                do_ = str(data_1[tii][-1]).center(5)
                dt_ = str(data_1[tii][3]).center(6)
                pt_ = str(data_1[tii][5]).center(5)
                tn_ = str(data_1[tii][0]).center(5)
                n_ = str(data_1[tii][6] + 1).center(5)
                if (i - 1) % 2 == 0:
                    suf = "\\" if j == 0 else "/"
                else:
                    suf = "/" if j == 0 else "\\"
                if j == 0:
                    results += team_line_l.format(CO=co_, DO=do_, DT=dt_, PT=pt_, T=tn_, N=n_) + f"{suf}"
                    if ti % 4 == 1:
                        results += f"{' ' * 6}\\"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 7
                    elif ti % 4 == 2:
                        results += f"{' ' * 6}/"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 7

                    if ti == 2:
                        results += f"{' ' * 7}\\"  # + ("\\" if ti % 4 == 1 else "/")
                        minus += 8
                        if both_brackets:
                            results += f"{' ' * 21}/"
                            minus += 22
                    elif ti == 3:
                        results += f"{' ' * 16}\\"
                        minus += 17
                        if both_brackets:
                            results += f"{' ' * 17}/"
                            minus += 18
                    elif ti == 4:
                        results += f"{' ' * 16}/"
                        minus += 17
                        if both_brackets:
                            results += f"{' ' * 17}\\"
                            minus += 18
                    elif ti == 5:
                        results += f"{' ' * 7}/"
                        minus += 8
                        if both_brackets:
                            results += f"{' ' * 21}\\"
                            minus += 22

                    if ti == 1:
                        if both_brackets:
                            results += f"{ms[:(len(ms) // 2) + 5]}{' ' * 6}/"
                            minus += 7 + len(ms[:(len(ms) // 2) + 5])
                    elif ti == 2:
                        if both_brackets:
                            results += f"{' ' * 7}\\"
                            minus += 8
                    elif ti == 5:
                        if both_brackets:
                            results += f"{' ' * 7}/"
                            minus += 8
                    elif ti == 6:
                        if both_brackets:
                            results += f"{ms[:(len(ms) // 2) + 5]}{' ' * 6}\\"
                            minus += 7 + len(ms[:(len(ms) // 2) + 5])
                else:
                    results += f"{ms[:len(ms) - (2 + minus)]}{suf}" + team_line_r.format(CO=co_, DO=do_, DT=dt_, PT=pt_,
                                                                                         T=tn_, N=n_)
                    minus = 0

            if i == 4:
                results += f"\n{lm}{ms[:(len(ms) // 2) - 8]}= ___ vs. ___ ="
            else:
                results += f"\n{lm}"
            if ti % 2 == 0:
                if ti == 0 or ti == 6:
                    results += f"= ___{ms[:(len(ms) // 2) + 15]}___ ="
                else:
                    if ti == 2:
                        results += f"= ___{' ' * 10}\\{ms[:(len(ms) // 4) + 6]}/{' ' * 10}___ ="
                    else:
                        results += f"= ___{' ' * 10}/{ms[:(len(ms) // 4) + 6]}\\{' ' * 10}___ ="
            elif ti % 4 == 1:
                results += f"{' ' * 8}= ___{ms[:(len(ms) // 4) + 12]}___ ="
            results += f"\n"
            ti += 1

    return results


class Conference(Enum):
    EASTERN: str = "eastern"
    WESTERN: str = "western"


class Division(Enum):
    ATLANTIC: tuple[Conference, str] = (Conference.EASTERN, "atlantic")
    METROPOLITAN: tuple[Conference, str] = (Conference.EASTERN, "metropolitan")
    CENTRAL: tuple[Conference, str] = (Conference.WESTERN, "central")
    PACIFIC: tuple[Conference, str] = (Conference.WESTERN, "pacific")

    def __eq__(self, other):
        if not isinstance(other, Division):
            return False
        return other.value == self.value


class Team:
    def __init__(self, team_name, acronym, city, mascot, division, wikipedia_link):
        self.team_name = team_name
        self.acronym = acronym
        self.city_full = city
        self.city, self.province_state, self.country = self.city_full.split(",")
        self.mascot = mascot
        self.division_obj = division
        self.division_full = self.division_obj.value
        self.conference, self.division = self.division_full
        self.conference = self.conference.value
        self.wikipedia_link = wikipedia_link

    def __repr__(self):
        return f"{self.acronym}"


class Season:
    def __init__(self, league, start_date, end_date, n_games=82, max_points_per_game=2):

        self.league = league
        self.n_games = n_games
        self.max_points_per_game = max_points_per_game

        self.start_date = start_date
        self.end_date = end_date
        self.year = self.start_date.year

        self.teams_list = self.league.history[self.year]["teams"]
        print(f"tl={self.teams_list}")
        print(f"tl={[t.division_full for t in self.teams_list]}")

        self.u_confs = {t.conference: "" for t in self.teams_list}
        self.u_divs = {t.division: "" for t in self.teams_list}

        self.divisions_list = list(self.u_divs.keys())
        self.conferences_list = list(self.u_confs.keys())

        # hardcoded this:
        self.metropolitan_teams_list = [t for t in self.teams_list if t.division_obj == Division.METROPOLITAN]
        self.atlantic_teams_list = [t for t in self.teams_list if t.division_obj == Division.ATLANTIC]
        self.central_teams_list = [t for t in self.teams_list if t.division_obj == Division.CENTRAL]
        self.pacific_teams_list = [t for t in self.teams_list if t.division_obj == Division.PACIFIC]

        self.dates_range_list = [d.to_pydatetime() for d in pd.date_range(self.start_date, self.end_date)]
        keep_trying = True
        while keep_trying:
            try:
                self.schedule = self.gen_schedule()
            except ValueError as ve:
                # print(f"{ve=}")
                # raise ve
                pass
            else:
                keep_trying = False

        self.n_games_played = 0


        # self.league_data = {
        #     "eastern": {
        #         "metropolitan": [t.acronym for t in self.metropolitan_teams_list],
        #         "atlantic": [atlantic[t]["acr"] for t in atlantic]
        #     },
        #     "western": {
        #         "central": [central[t]["acr"] for t in central],
        #         "pacific": [pacific[t]["acr"] for t in pacific]
        #     }
        # }
        #
        # def team_conf(team):
        #     for conf, conf_data in league.items():
        #         for div, div_data in conf_data.items():
        #             for t in div_data:
        #                 if team == t or team in t:
        #                     return conf
        #
        # def team_div(team):
        #     for conf, conf_data in league.items():
        #         for div, div_data in conf_data.items():
        #             for t in div_data:
        #                 if team == t or team in t:
        #                     return div

        self.season_standings = {
            team: {t: "" if t != team else "-" for t in ["#", *self.teams_list]}
            for team in self.teams_list
        }

        for i, team in enumerate(self.teams_list):
            self.season_standings[team].update({
                "#": i,
                " ": " ",
                "GP": 0,
                "PTS": 0,
                "W": 0,
                "L": 0,
                "OTW": 0,
                "OTL": 0,
                "GL": self.n_games,
                "MP": self.n_games * self.max_points_per_game
            })

    def gen_schedule(self):

        # Define the teams by division
        # metropolitan_teams = ["Carolina", "New Jersey", "NY Rangers", "Washington", "NY Islanders", "Pittsburgh",
        #                       "Philadelphia", "Columbus"]
        # atlantic_teams = ["Boston", "Toronto", "Tampa Bay", "Buffalo", "Florida", "Detroit", "Ottawa", "Montreal"]
        # central_teams = ["Winnipeg", "Dallas", "Minnesota", "Colorado", "St. Louis", "Nashville", "Arizona", "Chicago"]
        # pacific_teams = ["Vegas", "Seattle", "Los Angeles", "Edmonton", "Calgary", "Vancouver", "San Jose", "Anaheim"]

        metropolitan_teams = self.metropolitan_teams_list
        atlantic_teams = self.atlantic_teams_list
        central_teams = self.central_teams_list
        pacific_teams = self.pacific_teams_list

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
            non_division_teams = set(all_teams) - set(division_teams) - {team, }
            for non_division_team in non_division_teams:
                for i in range(num_non_division_games):
                    opponents.append(non_division_team)

            # opponents.sort()

            # Add the schedule to the dictionary
            schedule[team] = opponents

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

            non_division_teams = list(set(tt) - set(division_teams) - {team, })
            k = clamp(0, 82 - len(schedule[team]), 6)
            print(f"{str(team).ljust(12)}, l={len(non_division_teams)}, {k=}, {non_division_teams=}")
            opponents = random.sample(non_division_teams, k=k)
            print(f"\t{str(team).ljust(12)}, l={len(opponents)}, {opponents=}")
            schedule[team] = schedule[team] + opponents
            for t in opponents:
                schedule[t] = schedule[t] + [team]
                if len(schedule[t]) >= 82:
                    print(f"{str(t).rjust(12)} l={len(schedule[t])} FINISHED B")
                    tt.remove(t)
            tt.remove(team)
            print(f"{str(team).rjust(12)} l={len(schedule[team])} FINISHED A")

        u_games = []
        v_teams = set()
        for team, opponents in schedule.items():
            print(f"{str(team).ljust(14)}: l={str(len(opponents)).ljust(4)} | {opponents}")
            for opp in opponents:
                if opp not in v_teams:
                    u_games.append((team, opp))
            v_teams.add(team)

        print(f"length: l={len(u_games)}\n{u_games}")
        # with open("2023-04-04 Season Output.txt", "w") as f:
        # for team_a, team_b in u_games:
        #     print(f"'{team_a}', '{team_b}'")

        random.shuffle(u_games)
        games_per_day = len(u_games) / len(self.dates_range_list)
        gpd = int(games_per_day - 1), int(games_per_day)
        games_used = 0
        days_skipped = 0
        shuffled_schedule = {}
        min_day, max_day = (float("inf"), None), (0, None)
        ccgpd = lambda i: len(u_games) // (len(self.dates_range_list) - i)
        cgpd = lambda i: (ccgpd(i), (ccgpd(i) + 1))
        for i, d in enumerate(self.dates_range_list):
            # if i % 7 == 0:
            #     chance no games today
            high, low = maxmin(*cgpd(i))
            if random.choices([True, False], weights=[1, 3], k=1)[0]:
                # 6 % chance of no game today
                days_skipped += 1
                print(f"{low=}, {high=}, games_today=0 SKIPP")
                continue

            games_today = random.randint(low, high)
            while not games_today:
                games_today = random.randint(low, high)
            print(f"{low=}, {high=}, {games_today=}")
            if i == len(self.dates_range_list) - 1:
                if (games_used + games_today) < len(u_games):
                    games_left = len(u_games) - games_used
                    games_today += games_left

            games_used += games_today
            for j in range(games_today):
                if j == 0:
                    shuffled_schedule[d] = []
                shuffled_schedule[d] += random.sample(u_games, k=1)
                u_games.remove(shuffled_schedule[d][-1])

            if (nl := len(shuffled_schedule[d])) < min_day[0]:
                min_day = (nl, d)
            if (nl := len(shuffled_schedule[d])) > max_day[0]:
                max_day = (nl, d)

        print(dict_print(shuffled_schedule, "Schedule"))
        print(f"# games scheduled:\n\tDays Scheduled: {len(shuffled_schedule)}\n\tGames scheduled: {games_used=}\n\tMin day: #:{min_day[0]} d: {min_day[1]:%Y-%m-%d}\n\tMax day: #:{max_day[0]} d: {max_day[1]:%Y-%m-%d}")
        return shuffled_schedule

    def print_play_off_standings(self):

        if self.n_games_played == 0:
            print(f"No games have been played yet this season.\nPlease start this season first.")
            return

        sorted_standings_list = sorted(self.season_standings.keys(), key=lambda x: self.season_standings[x]['PTS'], reverse=True)
        sorted_standings = {team: self.season_standings[team] for team in sorted_standings_list}
        # if i == len(self.schedule) - 1:
        # print(dict_print(sorted_standings, f"season standings GP = {len(self.schedule)}\n\t\t\tMatchup: '{team_a}' VS '{team_b}'"))

        in_playoffs = set()
        standings = {}
        standings_t = []
        for div in self.divisions_list:
            print(f"\nTop 3 {div}:")
            print(f"{sorted_standings=}")

            # raise ValueError("STOPPP!")
            # for i, t in enumerate([t for t in sorted_standings if team_div(t) == div][:3]):
            for i, t in enumerate([t for t in sorted_standings if t.division == div][:3]):
                print(f"\t{t}")
                in_playoffs.add(t)
                conf = t.conference
                data = {
                    "div": div,
                    "conf": conf,
                    "seed": f"{div[0].upper()}__{conf[0].upper()}_{i}",
                    "place": i,
                    "pts": self.season_standings[t]["PTS"]
                }
                standings[t] = data
                standings_t.append([t, *list(data.values())])

        for conf in ["eastern", "western"]:
            print(f"\nWild card {conf[:4].title()}:")
            for i, t in enumerate([t for t in sorted_standings if t not in in_playoffs and t.conference == conf][:2]):
                print(f"\t{t}")
                in_playoffs.add(t)
                data = {
                    "div": t.division,
                    "conf": conf,
                    "seed": f"WC_{conf[0].upper()}_{i}",
                    "place": 6 + i,
                    "pts": self.season_standings[t]["PTS"]
                }
                standings[t] = data
                standings_t.append([t, *list(data.values())])

        # standings by conference, seed
        # standings_t.sort(key=lambda tup: (tup[2], tup[3], tup[4]))
        # standings_t.sort(key=lambda tup: (tup[2], -tup[5]))
        standings_t.sort(key=lambda tup: (tup[2], tup[4], -tup[5]))
        print(dict_print(standings, "Standings"))

        # print(f"\nWild card East:")
        # print("\t" + "\n\t".join([t for t in sorted_standings if t not in in_playoffs and team_conf(t) == "eastern"][:2]))
        # print(f"\nWild card West:")
        # print("\t" + "\n\t".join([t for t in sorted_standings if t not in in_playoffs and team_conf(t) == "western"][:2]))

        print_by_line(standings_t)

        playoff_schedule = [
            (standings_t[0], standings_t[7]),
            (standings_t[1], standings_t[6]),
            (standings_t[2], standings_t[4]),
            (standings_t[3], standings_t[5]),

            (standings_t[8], standings_t[15]),
            (standings_t[9], standings_t[14]),
            (standings_t[10], standings_t[12]),
            (standings_t[11], standings_t[13])
        ]

        print(f"Playoff Schedule")
        print_by_line(playoff_schedule)


class League:
    def __init__(self, league_name):
        self.league_name = league_name
        self.history = {}

    def add_team(self, year: int, team: Team):
        if year not in self.history:
            self.history[year] = {"season": None, "teams": [], "is_complete": False}
        if team not in self.history[year]["teams"]:
            self.history[year]["teams"].append(team)

    def init_season(self, year: int):
        year_title = f"{str(year)[-2:]} - {str(year + 1)[-2:]}"
        if year not in self.history:
            raise AttributeError(f"Error, year={year} has not been initialized in this league yet. Please add some teams first.")
        if self.history[year]["is_complete"]:
            raise ValueError(f"Error, the season {year_title} is already complete, cannot re-start.")
        if len(self.history[year]["teams"]) < 2:
            raise ValueError(f"Error, cannot begin {year_title} season without at least 2 teams.")

        print(f"Starting the {year}-{year+1} regular season!")
        season = Season(self, datetime.datetime(year, 10, 6), datetime.datetime(year + 1, 4, 10))
        self.history[year].update({"season": season})
        print(f"{self.history=}")
        return season

    def play_regular_season_game(self, year):
        if (year not in self.history) or (self.history[year].get("season", None) is None):
            raise KeyError("Error, this season has not been initialized yet.")


    def standings(self, year):
        if (year not in self.history) or (self.history[year].get("season", None) is None):
            raise KeyError("Error, this season has not been initialized yet.")
        self.history[year]["season"].print_play_off_standings()


NHL_TEAMS_LIST_2023 = [Team(*vals) for vals in [
        ("Carolina Hurricanes", "CAR", "Raleigh, North Carolina, USA", "Canes", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Carolina_Hurricanes"),
        ("New Jersey Devils", "NJD", "Newark, New Jersey, USA", "Devils", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/New_Jersey_Devils"),
        ("New York Rangers", "NYR", "Manhattan, New York, USA", "Rangers", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/New_York_Rangers"),
        ("Washington Capitals", "WSH", "Washington D.C., D.C., USA", "Caps", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Washington_Capitals"),
        ("New York Islanders", "NYI", "Elmont, New York, USA", "Isles", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/New_York_Islanders"),
        ("Pittsburgh Penguins", "PIT", "Pittsburgh, Pennsylvania, USA", "Pens", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Pittsburgh_Penguins"),
        ("Philadelphia Flyers", "PHI", "Philadelphia, Pennsylvania, USA", "Flyers", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Philadelphia_Flyers"),
        ("Columbus Blue Jackets", "CBJ", "Columbus, Ohio, USA", "Blue Jackets", Division.METROPOLITAN, r"https://en.wikipedia.org/wiki/Columbus_Blue_Jackets"),

        ("Boston Bruins", "BOS", "Boston, Massachusetts, USA", "Bruins", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Boston_Bruins"),
        ("Toronto Maple Leafs", "TOR", "Toronto, Ontario, Canada", "Leafs", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Toronto_Maple_Leafs"),
        ("Tampa Bay Lighting", "TBL", "Tampa, Florida, USA", "Bolts", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Tampa_Bay_Lightning"),
        ("Buffalo Sabres", "BUF", "Buffalo, New York, USA", "Sabres", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Buffalo_Sabres"),
        ("Florida Panthers", "FLA", "Sunrise, Florida, USA", "Panthers", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Florida_Panthers"),
        ("Detroit Red Wings", "DET", "Detroit, Michigan, USA", "Red Wings", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Detroit_Red_Wings"),
        ("Ottawa Senators", "OTT", "Ottawa, Ontario, Canada", "Sens", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Ottawa_Senators"),
        ("Montreal Canadiens", "MTL", "Montreal, Quebec, Canada", "Habs", Division.ATLANTIC, r"https://en.wikipedia.org/wiki/Montreal_Canadiens"),

        ("Winnipeg Jets", "WPG", "Winnipeg, Manitoba, Canada", "Jets", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Winnipeg_Jets"),
        ("Dallas Stars", "DAL", "Dallas, Texas, USA", "Stars", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Dallas_Stars"),
        ("Minnesota Wild", "MIN", "Saint Paul, Minnesota, USA", "WILD", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Minnesota_Wild"),
        ("Colorado Avalanche", "COL", "Denver, Colorado, USA", "Avs", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Colorado_Avalanche"),
        ("St. Louis Blues", "STL", "St. Louis, Missouri, USA", "Blues", Division.CENTRAL, r"https://en.wikipedia.org/wiki/St._Louis_Blues"),
        ("Nashville Predators", "NSH", "Nashville, Tennessee, USA", "Preds", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Nashville_Predators"),
        ("Arizona Coyotes", "ARI", "Phoenix, Arizona, USA", "Yotes", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Arizona_Coyotes"),
        ("Chicago Blackhawks", "CHI", "Chicago, Illinois, USA", "Hawks", Division.CENTRAL, r"https://en.wikipedia.org/wiki/Chicago_Blackhawks"),

        ("Las Vegas Golden Knights", "VGK", "Las Vegas, Nevada, USA", "Knights", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Vegas_Golden_Knights"),
        ("Seattle Kraken", "SEA", "Seattle, Washington, USA", "Kraken", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Seattle_Kraken"),
        ("Los Angeles Kings", "LAK", "Los Angeles, California, USA", "Kings", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Los_Angeles_Kings"),
        ("Edmonton Oilers", "EDM", "Edmonton, Alberta, Canada", "Oilers", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Edmonton_Oilers"),
        ("Calgary Flames", "CGY", "Calgary, Alberta, Canada", "Flames", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Calgary_Flames"),
        ("Vancouver Canucks", "VAN", "Vancouver, British-Columbia, Canada", "Canucks", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Vancouver_Canucks"),
        ("San Jose Sharks", "SJS", "San Jose, California, USA", "Sharks", Division.PACIFIC, r"https://en.wikipedia.org/wiki/San_Jose_Sharks"),
        ("Anaheim Ducks", "ANA", "Anaheim, California, USA", "Ducks", Division.PACIFIC, r"https://en.wikipedia.org/wiki/Anaheim_Ducks")
]]

print(NHL_TEAMS_LIST_2023)

nhl = League("NHL")



if __name__ == '__main__':
    # # print(draw_shedule(data, half="eastern"))
    # data_1.sort(key=lambda tup: (tup[2], tup[-1]))
    # lines = template_1.split("\n")
    # result = lines[0] + "\n"
    # for i in range(1, len(lines)):
    #     co_ = str(data_1[i][4]).center(5)
    #     do_ = str(data_1[i][-1]).center(5)
    #     dt_ = str(data_1[i][3]).center(5)
    #     pt_ = str(data_1[i][5]).center(5)
    #     tn_ = str(data_1[i][0]).center(5)
    #     n_ = str(data_1[i][6] + 1).center(5)
    #     result += lines[i].format(CO=co_, DO=do_, DT=dt_, PT=pt_, T=tn_, N=n_) + "\n"
    # print(template_1)
    # print(result)

    print("\n\n\tSCHED\n\n\n")
    print(sched())
    for t in NHL_TEAMS_LIST_2023:
        nhl.add_team(2022, t)

    nhl.init_season(2022)
    nhl.standings(2022)

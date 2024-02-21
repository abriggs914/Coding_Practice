import io
import json
import os
import tkinter
from urllib.request import urlopen

import requests
import datetime
from typing import Literal
import pandas as pd
from PIL import Image, ImageTk
# from cairosvg import svg2png
# import cairosvg
# import cairo
import pyvips

import nhl_utility
from json_utility import jsonify
from nhl_utility import *

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
	NHL API Handler class and utility
	Version..............1.01
	Date...........2024-01-09
	Author(s)....Avery Briggs
	"""


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(),
                                      "%Y-%m-%dictionary")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if
            w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


game_state_full = {
    "REG": "Regulation",
    "OT": "Overtime",
    "SO": "Shootout",
    "FINAL": "Final",
    "OFF": "Final"
}


class NHLAPIHandler:
    # 2024-01-09 0036

    HOST_NAME = f"https://api-web.nhle.com"

    def __init__(self, view_only: bool = False, max_query_hold_time: int = 21600):
        # default re-query time-out time = 6 Hours = 21600s
        self.history = {}
        self.view_only = view_only
        self.max_query_hold_time = max_query_hold_time
        self.file_history = r"./nhl_api_utility_history.json"
        self.now = datetime.datetime.now()
        print(f"Loading Data...", end="")
        with open(self.file_history, "r") as f:
            self.history = {k: [eval(v[0]), v[1]] for k, v in eval(json.load(f)).items()}

        if not isinstance(self.history, dict):
            raise ValueError(f"json format in the history file is not a valid dict")

        TOL = 1e-6
        self.reported_requerying = False
        self.number_queries = [0, len(self.history)]
        self.number_queries.append(100.0 / self.number_queries[1])  # dots per query
        self.first_query_time = self.now
        self.n_requeries = []
        for url, url_data in self.history.items():
            time, result = url_data
            if (self.now - time).total_seconds() > self.max_query_hold_time:
                self.n_requeries.append(url)
        # print(f"{self.number_queries=}")
        if not self.view_only:
            print(f" # Queries: {self.number_queries[1]}")
            query_times = [[None, None]] * 2
            # for url, url_data in self.history.items():
            for url in self.n_requeries:
                url_data = self.history[url]
                self.now = datetime.datetime.now()
                time, result = url_data
                # print(f"{time=}, {result=}")
                # time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                if (self.now - time).total_seconds() > self.max_query_hold_time:
                    # requery this url, it is too old
                    if not self.reported_requerying:
                        print(f"Need to requery {len(self.n_requeries)} resource(s) because they are too old.")
                        print(("|iiiiliiii" * 10) + "|")
                        print(f".", end="")  # this is 0
                        self.reported_requerying = True
                        self.first_query_time = self.now
                    result = self.query_url(url)
                    self.history[url] = (self.now, result)
                    eqt = datetime.datetime.now()
                    lqt = (eqt - self.now).total_seconds()
                    if query_times[0][0] is None:
                        query_times[0] = [url, lqt]
                    else:
                        if lqt < query_times[0][1]:
                            query_times[0] = [url, lqt]
                    if query_times[1][0] is None:
                        query_times[1] = [url, lqt]
                    else:
                        if lqt > query_times[1][1]:
                            query_times[1] = [url, lqt]
                self.number_queries[0] += self.number_queries[2]
                if (self.number_queries[0] + TOL) >= 1:
                    print(f"." * int(self.number_queries[0]), end="")
                    self.number_queries[0] = 0

            self.now = datetime.datetime.now()
            self.total_query_time = (self.now - self.first_query_time).total_seconds()
            tqt = f"{self.total_query_time:,.2f}"
            if self.reported_requerying:
                tpq = f"{self.total_query_time / self.number_queries[1]:,.2f}"
                print(f"Total Query Time:\n\t{tqt} seconds\n\t{self.number_queries[1]} queries\n\t{tpq} seconds / query\n\tMin Time: {query_times[0][1]} seconds for url '{query_times[0][0]}'\n\tMax Time: {query_times[1][1]} seconds for url '{query_times[1][0]}'")
            else:
                print(f"Loaded {self.number_queries[1]} total queries in {tqt} seconds.")
        else:
            self.now = datetime.datetime.now()
            self.total_query_time = (self.now - self.first_query_time).total_seconds()
            tqt = f"{self.total_query_time:,.2f}"
            print(f"\nNHLAPIHandler is in 'view-only' mode. No changes will be saved to the history json.\nLoaded {self.number_queries[1]} total queries in {tqt} seconds.")

    def save_data(self):
        if not self.view_only:
            with open(self.file_history, "w") as f:
                json.dump(jsonify(self.history), f)
        else:
            print(f"NHLAPIHandler is set to 'view-only', saving cannot be completed.")

    def query_url(self, url, do_print=False, check_history=True) -> dict | None:
        if do_print:
            print(f"{url=}")

        if check_history or self.view_only:
            if url in self.history:
                # for url_, url_data in self.history.items():
                #     if url == url_:
                if self.view_only or (not (self.now - self.history[url][0]).total_seconds() > self.max_query_hold_time):
                    # self.history[url] = (self.now, self.query_url(url, do_print=False))
                    return self.history[url][1]

        if self.view_only:
            print(f"Need to fetch '{url}'. The results will not be saved, 'view-only' is enabled.")

        now = datetime.datetime.now()
        response = requests.get(url)
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204:
            ct = response.headers["Content-Type"].lower()
            if ct.startswith("application/json"):
                self.history[url] = (now, response.json())
            elif ct.startswith("text/javascript"):
                self.history[url] = (now, eval(response.text.replace("jsonFeed(", "")[:-2]))

        return self.history.get(url, None)[1]

    def get_calendar_schedule(self, date: datetime.date, do_print=False) -> dict | None:
        url = f"{NHLAPIHandler.HOST_NAME}/v1/schedule-calendar/{date:%Y-%m-%d}"
        if do_print:
            print(f"{url=}")
        # schedule keys
        # ['endDate', 'nextStartDate', 'previousStartDate', 'startDate', 'teams']
        # teams list keys
        # ['id', 'seasonId', 'commonName', 'abbrev', 'name', 'placeName', 'logo', 'darkLogo', 'isNhl', 'french']
        return self.query_url(url)

    def get_schedule(self, date: datetime.date, do_print=False) -> dict | None:
        """Get 1 week's schedule of games"""
        url = f"{NHLAPIHandler.HOST_NAME}/v1/schedule/{date:%Y-%m-%d}"
        if do_print:
            print(f"{url=}")
        # schedule keys
        # ['nextStartDate', 'previousStartDate', 'gameWeek', 'oddsPartners', 'preSeasonStartDate', 'regularSeasonStartDate', 'regularSeasonEndDate', 'playoffEndDate', 'numberOfGames']
        return self.query_url(url)

    def is_game_ongoing_now(self, include_pregames: bool = True,
                            r_type: Literal["bool", "dict", "next_games"] = "bool") -> bool | dict:
        """Return True if a game is in the 'LIVE' state or optionally 'PRE' state NOW!"""
        valid = ["LIVE"] + ([] if not include_pregames else ["PRE"])
        now = datetime.datetime.now()

        # check yesterday first since east coast means late night games
        gy = self.get_score((now + datetime.timedelta(days=-1)).date())
        gsy = [g["gameState"] in valid for g in gy["games"]]
        print(f"{gy=}\n{gsy=}")
        if any(gsy):
            return True if r_type == "bool" else gy

        # check today's games
        gt = self.get_score(now.date())
        gst = [g["gameState"] in valid for g in gt["games"]]
        print(f"{gt=}\n{gst=}")
        if any(gst):
            return True if r_type == "bool" else gt
        return False if r_type == "bool" else (gt if r_type == "next_games" else {})

    def are_games_going_on_today(self, include_finals: bool = True,
                                 r_type: Literal["bool", "dict", "next_games"] = "bool") -> bool | dict:
        """Return True if a game is on the 'LIVE' state or optionally 'PRE' state NOW!"""
        valid = ["FUT", "PRE", "LIVE"]
        now = datetime.datetime.now()

        # check yesterday first since east coast means late night games
        gy = self.get_score((now + datetime.timedelta(days=-1)).date())
        if any([g["gameState"] in valid for g in gy["games"]]):
            return True if r_type == "bool" else gy

        valid += ([] if not include_finals else ["FINAL", "OFF"])

        # check today's games
        gt = self.get_score(now.date())
        if any([g["gameState"] in valid for g in gt["games"]]):
            return True if r_type == "bool" else gt
        return False if r_type == "bool" else (gt if r_type == "next_games" else {})

    def get_geolocation(self, do_print=False) -> dict | None:
        url = "https://geolocation.onetrust.com/cookieconsentpub/v1/geo/location"
        if do_print:
            print(f"{url=}")
        return self.query_url(url)

    def get_country(self, do_print=False) -> dict | None:
        url = f"{NHLAPIHandler.HOST_NAME}/v1/location"
        if do_print:
            print(f"{url=}")
        return self.query_url(url)

    def get_score(self, date: datetime.date, do_print=False) -> dict | None:
        """Get scores for a particular date"""
        # score keys:
        # ['prevDate', 'currentDate', 'nextDate', 'gameWeek', 'oddsPartners', 'games']
        url = f"{NHLAPIHandler.HOST_NAME}/v1/score/{date:%Y-%m-%d}"
        if do_print:
            print(f"{url=}")
        return self.query_url(url)

    def get_standings(self, date: datetime.date, do_print=False) -> dict | None:
        """Get standings up to a particular date"""
        # standings keys:
        # ['wildCardIndicator', 'standings']
        url = f"{NHLAPIHandler.HOST_NAME}/v1/standings/{date:%Y-%m-%d}"
        if do_print:
            print(f"{url=}")
        return self.query_url(url)

    def get_player_info(self, player_id: int, do_print=False) -> dict | None:
        """Get data on a specific player"""
        # standings keys:
        # ['wildCardIndicator', 'standings']
        url = f"{NHLAPIHandler.HOST_NAME}/v1/player/{player_id}/landing"
        if do_print:
            print(f"{url=}")
        return self.query_url(url)

    def get_team_roster(self, team_acr, season: str = "20232024"):
        # return requests.get(f"https://api-web.nhle.com/v1/roster/{team_acr}/{season}").json()
        return self.query_url(f"{NHLAPIHandler.HOST_NAME}/v1/roster/{team_acr}/{season}")

    def get_player_stats(self, player_id: str):
        return self.query_url(f"{NHLAPIHandler.HOST_NAME}/v1/player/{player_id}/landing")


def playoff_pool_sheet_view_only(
        n_forward_boxes: int = 7,
        n_defence_boxes: int = 3,
        n_forwards_per_boxes: int = 6,
        n_defence_per_boxes: int = 6,
        kwargs_nhl_api_utility: dict | None = None,
        do_save_api_handler: bool = False,
        pool_texts: bool = False
):
    if (kwargs_nhl_api_utility is None) or (not isinstance(kwargs_nhl_api_utility, dict)):
        kwargs_nhl_api_utility = {
            "view_only": False,
            "max_query_hold_time": 60 * 60 * 24  # 1 day
        }
    # nhl_api = NHLAPIHandler(view_only=True)
    nhl_api = NHLAPIHandler(**kwargs_nhl_api_utility)
    today = datetime.datetime.today()
    standings_today = nhl_api.get_standings(today)
    print(f"{standings_today=}")
    standings_data = {}

    top_east = []
    top_west = []
    top_atl = []
    top_met = []
    top_cen = []
    top_pac = []
    wc_east = []
    wc_west = []

    # w = '/stats/rest/en/skater/summary', h = 'http://api.nhle.com', t = '/stats/rest/en/leaders/skaters/goals', HOST_NAME = 'https://api-web.nhle.com'

    for standings_data_ in standings_today["standings"]:
        # print(f"{standings_data_=}")
        conf_abbrev = standings_data_.get("conferenceAbbrev")
        conf_name = standings_data_.get("conferenceName")
        div_abbrev = standings_data_.get("divisionAbbrev")
        div_name = standings_data_.get("divisionName")

        league_place = standings_data_.get("leagueSequence")
        conf_place = standings_data_.get("conferenceSequence")
        div_place = standings_data_.get("divisionSequence")

        league_place_home = standings_data_.get("leagueHomeSequence")
        league_place_road = standings_data_.get("leagueRoadSequence")
        league_place_l10 = standings_data_.get("leagueL10Sequence")

        conf_place_home = standings_data_.get("conferenceHomeSequence")
        div_place_home = standings_data_.get("divisionHomeSequence")
        conf_place_road = standings_data_.get("conferenceRoadSequence")
        div_place_road = standings_data_.get("divisionRoadSequence")
        conf_place_l10 = standings_data_.get("conferenceL10Sequence")
        div_place_l10 = standings_data_.get("divisionL10Sequence")
        wc_place = standings_data_.get("wildcardSequence")

        team_name = standings_data_.get("teamName", {}).get("default")
        team_name_common = standings_data_.get("teamCommonName", {}).get("default")
        team_name_abbrev = standings_data_.get("teamAbbrev", {}).get("default")
        team_name_fr = standings_data_.get("teamName", {}).get("fr")
        team_name_common_fr = standings_data_.get("teamCommonName", {}).get("fr")
        team_name_abbrev_fr = standings_data_.get("teamAbbrev", {}).get("fr")
        team_logo = standings_data_.get("teamLogo")

        streak_count = standings_data_.get("streakCount", 0)
        streak_code = standings_data_.get("streakCode")
        games_played = standings_data_.get("gamesPlayed", 0)
        points = standings_data_.get("points", 0)
        win_pctg = standings_data_.get("winPctg", 0)
        wins = standings_data_.get("wins", 0)
        losses = standings_data_.get("losses", 0)
        wins_ot = standings_data_.get("shootoutWins", 0)
        losses_ot = standings_data_.get("otLosses", 0)
        losses_so = standings_data_.get("shootoutLosses", 0)
        wins_reg = standings_data_.get("regulationWins", 0)
        wins_reg_ot = standings_data_.get("regulationPlusOtWins", 0)
        wins_reg_ot_pctg = standings_data_.get("regulationPlusOtWinsPctg", 0)

        point_pctg = standings_data_.get("pointsPctg", 0)
        goal_diff = standings_data_.get("goalDifferential", 0)
        goal_diff_pctg = standings_data_.get("goalDifferentialPctg", 0)
        goals_for = standings_data_.get("goalsFor", 0)
        goals_against = standings_data_.get("goalsAgainst", 0)
        goals_per_game = standings_data_.get("goalsForPctg", 0)

        games_played_home = standings_data_.get("homeGamesPlayed", 0)
        goal_diff_home = standings_data_.get("homeGoalDifferential", 0)
        goals_against_home = standings_data_.get("homeGoalsAgainst", 0)
        goals_for_home = standings_data_.get("homeGoalsFor", 0)
        losses_home = standings_data_.get("homeLosses", 0)
        ot_losses_home = standings_data_.get("homeOtLosses", 0)
        wins_home = standings_data_.get("homeWins", 0)
        points_home = standings_data_.get("homePoints", 0)
        wins_reg_ot_home = standings_data_.get("homeRegulationPlusOtWins", 0)
        wins_reg_home = standings_data_.get("homeRegulationWins", 0)

        games_played_l10 = standings_data_.get("l10GamesPlayed", 0)
        goal_diff_l10 = standings_data_.get("l10GoalDifferential", 0)
        goals_against_l10 = standings_data_.get("l10GoalsAgainst", 0)
        goals_for_l10 = standings_data_.get("l10GoalsFor", 0)
        losses_l10 = standings_data_.get("l10Losses", 0)
        ot_losses_l10 = standings_data_.get("l10OtLosses", 0)
        wins_l10 = standings_data_.get("l10Wins", 0)
        points_l10 = standings_data_.get("l10Points", 0)
        wins_reg_ot_l10 = standings_data_.get("l10RegulationPlusOtWins", 0)
        wins_reg_l10 = standings_data_.get("l10RegulationWins", 0)

        games_played_road = standings_data_.get("roadGamesPlayed", 0)
        goal_diff_road = standings_data_.get("roadGoalDifferential", 0)
        goals_against_road = standings_data_.get("roadGoalsAgainst", 0)
        goals_for_road = standings_data_.get("roadGoalsFor", 0)
        losses_road = standings_data_.get("roadLosses", 0)
        ot_losses_road = standings_data_.get("roadOtLosses", 0)
        wins_road = standings_data_.get("roadWins", 0)
        points_road = standings_data_.get("roadPoints", 0)
        wins_reg_ot_road = standings_data_.get("roadRegulationPlusOtWins", 0)
        wins_reg_road = standings_data_.get("roadRegulationWins", 0)

        if conf_abbrev == "W":
            top_west.insert(conf_place, standings_data_)
            if div_abbrev == "P":
                top_pac.insert(div_place, standings_data_)
            else:
                top_cen.insert(div_place, standings_data_)
        else:
            top_east.insert(conf_place, standings_data_)
            if div_abbrev == "A":
                top_atl.insert(div_place, standings_data_)
            else:
                top_met.insert(div_place, standings_data_)

    top_atl = top_atl[:3]
    top_met = top_met[:3]
    top_cen = top_cen[:3]
    top_pac = top_pac[:3]

    for team_data in top_east:
        div = team_data["divisionAbbrev"]
        if div == "A":
            if team_data in top_atl:
                continue
            else:
                wc_east.append(team_data)
        else:
            if team_data in top_met:
                continue
            else:
                wc_east.append(team_data)

        if len(wc_east) == 2:
            break

    for team_data in top_west:
        div = team_data["divisionAbbrev"]
        if div == "P":
            if team_data in top_pac:
                continue
            else:
                wc_west.append(team_data)
        else:
            if team_data in top_cen:
                continue
            else:
                wc_west.append(team_data)

        if len(wc_west) == 2:
            break

    fmt_final_results = [
        f"\nTop East",
        f"\nTop Atlantic:",
        top_atl,
        f"\nTop Metropolitan:",
        top_met,
        f"\nWildcard East:",
        wc_east,
        f"\nTop West:",
        f"\nTop Central:",
        top_cen,
        f"\nTop Pacific:",
        top_pac,
        f"\nWildcard West:",
        wc_west
    ]

    lpk_keys = ["div", "conf", "team_id", "position", "name", "number"]
    list_of_players_and_keys = {}  # div, conf, teamid, position,
    list_of_players_and_teams = {}
    list_of_teams = {"E": [], "W": []}
    list_id_pts_skaters = {"E": [], "W": []}
    list_id_sv_pctg_goalies = {"E": [], "W": []}
    team_div, team_conf, team_id, player_position, player_name, player_number = [None] * 6
    for line in fmt_final_results:
        if isinstance(line, list):
            for team_data in line:
                if isinstance(team_data, dict):
                    team_conf = team_data["conferenceAbbrev"]
                    team_div = team_data["divisionAbbrev"]
                    team_points = team_data["points"]
                    mascot = team_data['teamCommonName']['default']
                    nhl_util_k = nhl_utility.name_from_mascot(mascot)
                    acronym = nhl_utility.team_attribute(nhl_util_k, "acr")
                    roster = nhl_api.get_team_roster(acronym)
                    print(f"\t{mascot}, {acronym}")
                    for position, position_data in roster.items():
                        print(f"\t\t{position=}")
                        for player in position_data:
                            player_id = player.get("id", "")
                            if player_id:
                                player_position = player.get("positionCode", "")
                                player_number = player.get("sweaterNumber", "")
                                player_name = player.get("firstName", {}).get("default", "") + " " + player.get(
                                    "lastName", {}).get("default", "")
                                stats = nhl_api.get_player_stats(player_id)
                                team_id = stats["currentTeamId"]
                                if team_id not in [t[0] for t in list_of_teams[team_conf]]:
                                    list_of_teams[team_conf].append((team_id, acronym, team_points))
                                if player_id not in list_of_players_and_teams:
                                    list_of_players_and_teams[player_id] = acronym
                                    list_of_players_and_keys[player_id] = {k: v for k, v in zip(lpk_keys,
                                                                                                [team_div,
                                                                                                 team_conf,
                                                                                                 team_id,
                                                                                                 player_position,
                                                                                                 player_name,
                                                                                                 player_number])}
                                if player_position == "G":
                                    save_pctg = stats.get("featuredStats", {}).get("regularSeason", {}).get(
                                        "subSeason",
                                        {}).get(
                                        "points", 0)
                                    list_id_sv_pctg_goalies[team_conf].append((stats["playerId"], save_pctg))
                                else:
                                    pts_this_season = stats.get("featuredStats", {}).get("regularSeason", {}).get(
                                        "subSeason", {}).get("points", 0)
                                    list_id_pts_skaters[team_conf].append((stats["playerId"], pts_this_season))
                            else:
                                stats = "N/A"
                            team_data["stats"] = stats
                            print("\t\t\t" + ", ".join([f"{k}: {v}" for k, v in zip(lpk_keys,
                                                                                    [team_div, team_conf, team_id,
                                                                                     player_position, player_name,
                                                                                     player_number])]))
                            # print(f"\t\t\t{player=}")
                            # print(f"\t\t\t\t{stats=}")
                            # i = 14/0

                    list_id_pts_skaters["E"].sort(key=lambda tup: tup[1], reverse=True)
                    list_id_pts_skaters["W"].sort(key=lambda tup: tup[1], reverse=True)

                    # print(f"\t\t{roster=}")
        else:
            print(line)

    list_of_teams["E"].sort(key=lambda tup: tup[2], reverse=True)
    list_of_teams["W"].sort(key=lambda tup: tup[2], reverse=True)
    print(f"{list_of_teams=}")

    top_players_on_team = {}
    for conf, conf_data in list_id_pts_skaters.items():
        for player_id, pts in conf_data:
            player_team = list_of_players_and_teams[player_id]
            if player_team not in top_players_on_team:
                top_players_on_team[player_team] = []
            p_div, p_conf, p_team, p_pos, p_name, p_num = list_of_players_and_keys[player_id].values()
            top_players_on_team[player_team].append(list_of_players_and_keys[player_id].values())
            print(
                f"{pts=}, {player_id=}, {player_team=}, {p_div=}, {p_conf=}, {p_team=}, {p_pos=}, {p_name=}, {p_num=}")

    # box_num = 0
    pool_sheet_boxes = {"E": {"F": [], "D": [], "T": []}, "W": {"F": [], "D": [], "T": []}}
    pool_sheet_team_counts = {"F": {}, "D": {}, "T": {}}
    for t in list_of_teams["E"] + list_of_teams["W"]:
        team_id, team_acr, team_pts = t
        for k in pool_sheet_team_counts:
            pool_sheet_team_counts[k][team_acr] = 0
    max_same_team_per_box = 4
    for conf in ["E", "W"]:
        for i in range(n_forward_boxes):
            team_picks_per_box = {}
            box = []
            for j in range(n_forwards_per_boxes):
                k = 0
                chx_player_id, chx_player_pts, chx_player_team = None, None, None
                # lens = {t: len(t) for t in pool_sheet_team_counts["F"]}

                while k < len(list_id_pts_skaters[conf]):
                    chx_player_id, chx_player_pts = list_id_pts_skaters[conf][k]
                    chx_player_team = list_of_players_and_teams[chx_player_id]
                    chx_player_pos = list_of_players_and_keys[chx_player_id]["position"]
                    if chx_player_pos in ("C", "L", "R"):
                        w_lens = {t: len(t) for t in pool_sheet_team_counts["F"]}
                        if w_lens.get(chx_player_team, None) is None:
                            w_lens[chx_player_team] = 0
                        w_lens[chx_player_team] += 1
                        if abs(min(w_lens.values()) - max(w_lens.values())) <= 1:
                            # begin selecting
                            if chx_player_team not in team_picks_per_box:
                                team_picks_per_box[chx_player_team] = 0
                            if team_picks_per_box[chx_player_team] <= max_same_team_per_box:
                                team_picks_per_box[chx_player_team] += 1
                                del list_id_pts_skaters[conf][k]
                                break
                    k += 1

                box.append((chx_player_id, chx_player_pts, chx_player_team))
                if chx_player_team not in pool_sheet_team_counts["F"]:
                    pool_sheet_team_counts["F"][chx_player_team] = 0
                pool_sheet_team_counts["F"][chx_player_team] += 1
            pool_sheet_boxes[conf]["F"].append(box)

        for i in range(n_defence_boxes):
            team_picks_per_box = {}
            box = []
            for j in range(n_defence_per_boxes):
                k = 0
                chx_player_id, chx_player_pts, chx_player_team = None, None, None
                while k < len(list_id_pts_skaters[conf]):
                    chx_player_id, chx_player_pts = list_id_pts_skaters[conf][k]
                    chx_player_team = list_of_players_and_teams[chx_player_id]
                    chx_player_pos = list_of_players_and_keys[chx_player_id]["position"]
                    if chx_player_pos == "D":
                        w_lens = {t: len(t) for t in pool_sheet_team_counts["F"]}
                        if w_lens.get(chx_player_team, None) is None:
                            w_lens[chx_player_team] = 0
                        w_lens[chx_player_team] += 1
                        if abs(min(w_lens.values()) - max(w_lens.values())) <= 1:
                            # begin selecting
                            if chx_player_team not in team_picks_per_box:
                                team_picks_per_box[chx_player_team] = 0
                            if team_picks_per_box[chx_player_team] <= max_same_team_per_box:
                                team_picks_per_box[chx_player_team] += 1
                                del list_id_pts_skaters[conf][k]
                                break
                    k += 1

                box.append((chx_player_id, chx_player_pts, chx_player_team))
                if chx_player_team not in pool_sheet_team_counts["D"]:
                    pool_sheet_team_counts["D"][chx_player_team] = 0
                pool_sheet_team_counts["D"][chx_player_team] += 1
            pool_sheet_boxes[conf]["D"].append(box)

        for i in range(2):
            box = []
            for team_data in list_of_teams[conf]:
                team_id, team_acr, team_pts = team_data
                box.append((team_id, team_pts, team_acr))
                if team_acr not in pool_sheet_team_counts["T"]:
                    pool_sheet_team_counts["T"][team_acr] = 0
                pool_sheet_team_counts["T"][team_acr] += 1
            pool_sheet_boxes[conf]["T"].append(box)

    pool_sheet_boxes_text = {}
    print(f"pool_sheet_boxes")
    print(f"{list_of_players_and_keys=}")
    print(f"{list_of_players_and_teams=}")
    for conf, position_boxes in pool_sheet_boxes.items():
        pool_sheet_boxes_text[conf] = {}
        print(f"\tConference: '{conf}'")
        for position, boxes in position_boxes.items():
            pool_sheet_boxes_text[conf][position] = []
            print(f"\t\tPosition: '{position}'")
            for i, box in enumerate(boxes):
                pool_sheet_boxes_text[conf][position].append([])
                print(f"\t\t\tBox {i + 1}")
                if position != "T":
                    for player_id, player_pts, player_team in box:
                        p_name = list_of_players_and_keys[player_id]["name"]
                        p_name_s = p_name.split(" ")
                        p_name_l = p_name_s[-1].title()
                        p_name_f = p_name_s[0][0].upper()
                        gp = 1
                        ppg = player_pts / gp
                        print(f"\t\t\t\t{player_pts=}, {player_id=}, {player_team}, {p_name}")
                        pool_sheet_boxes_text[conf][position][i].append(f"{p_name_l}, {p_name_f} ({player_team}) : {ppg:.2f}")
                else:
                    for team_id, team_pts, team_team in box:
                        print(f"\t\t\t\t{team_pts=}, {team_id=}, {team_team}")
                        gp = 1
                        ppg = team_pts / gp
                        pool_sheet_boxes_text[conf][position][i].append(f"{team_team} ({team_team}) : {ppg:.2f}")
    print(f"{pool_sheet_team_counts=}")
    print(f"{list_id_pts_skaters=}")
    for conf, team_data in list_of_teams.items():
        print(f"{conf=}")
        for team_dat in team_data:
            print(f"\t{team_dat=}")

    if do_save_api_handler:
        nhl_api.save_data()

    return pool_sheet_boxes if (not pool_texts) else pool_sheet_boxes_text


def playoff_pool_sheet(
        n_forward_boxes: int = 7,
        n_defence_boxes: int = 3,
        n_forwards_per_boxes: int = 6,
        n_defence_per_boxes: int = 6
):
    nhl_api = NHLAPIHandler(max_query_hold_time=3 * 24 * 3600)
    today = datetime.datetime.today()
    standings_today = nhl_api.get_standings(today)
    print(f"{standings_today=}")
    standings_data = {}

    top_east = []
    top_west = []
    top_atl = []
    top_met = []
    top_cen = []
    top_pac = []
    wc_east = []
    wc_west = []

    # w = '/stats/rest/en/skater/summary', h = 'http://api.nhle.com', t = '/stats/rest/en/leaders/skaters/goals', HOST_NAME = 'https://api-web.nhle.com'

    for standings_data_ in standings_today["standings"]:
        # print(f"{standings_data_=}")
        conf_abbrev = standings_data_.get("conferenceAbbrev")
        conf_name = standings_data_.get("conferenceName")
        div_abbrev = standings_data_.get("divisionAbbrev")
        div_name = standings_data_.get("divisionName")

        league_place = standings_data_.get("leagueSequence")
        conf_place = standings_data_.get("conferenceSequence")
        div_place = standings_data_.get("divisionSequence")

        league_place_home = standings_data_.get("leagueHomeSequence")
        league_place_road = standings_data_.get("leagueRoadSequence")
        league_place_l10 = standings_data_.get("leagueL10Sequence")

        conf_place_home = standings_data_.get("conferenceHomeSequence")
        div_place_home = standings_data_.get("divisionHomeSequence")
        conf_place_road = standings_data_.get("conferenceRoadSequence")
        div_place_road = standings_data_.get("divisionRoadSequence")
        conf_place_l10 = standings_data_.get("conferenceL10Sequence")
        div_place_l10 = standings_data_.get("divisionL10Sequence")
        wc_place = standings_data_.get("wildcardSequence")

        team_name = standings_data_.get("teamName", {}).get("default")
        team_name_common = standings_data_.get("teamCommonName", {}).get("default")
        team_name_abbrev = standings_data_.get("teamAbbrev", {}).get("default")
        team_name_fr = standings_data_.get("teamName", {}).get("fr")
        team_name_common_fr = standings_data_.get("teamCommonName", {}).get("fr")
        team_name_abbrev_fr = standings_data_.get("teamAbbrev", {}).get("fr")
        team_logo = standings_data_.get("teamLogo")

        streak_count = standings_data_.get("streakCount", 0)
        streak_code = standings_data_.get("streakCode")
        games_played = standings_data_.get("gamesPlayed", 0)
        points = standings_data_.get("points", 0)
        win_pctg = standings_data_.get("winPctg", 0)
        wins = standings_data_.get("wins", 0)
        losses = standings_data_.get("losses", 0)
        wins_ot = standings_data_.get("shootoutWins", 0)
        losses_ot = standings_data_.get("otLosses", 0)
        losses_so = standings_data_.get("shootoutLosses", 0)
        wins_reg = standings_data_.get("regulationWins", 0)
        wins_reg_ot = standings_data_.get("regulationPlusOtWins", 0)
        wins_reg_ot_pctg = standings_data_.get("regulationPlusOtWinsPctg", 0)

        point_pctg = standings_data_.get("pointsPctg", 0)
        goal_diff = standings_data_.get("goalDifferential", 0)
        goal_diff_pctg = standings_data_.get("goalDifferentialPctg", 0)
        goals_for = standings_data_.get("goalsFor", 0)
        goals_against = standings_data_.get("goalsAgainst", 0)
        goals_per_game = standings_data_.get("goalsForPctg", 0)

        games_played_home = standings_data_.get("homeGamesPlayed", 0)
        goal_diff_home = standings_data_.get("homeGoalDifferential", 0)
        goals_against_home = standings_data_.get("homeGoalsAgainst", 0)
        goals_for_home = standings_data_.get("homeGoalsFor", 0)
        losses_home = standings_data_.get("homeLosses", 0)
        ot_losses_home = standings_data_.get("homeOtLosses", 0)
        wins_home = standings_data_.get("homeWins", 0)
        points_home = standings_data_.get("homePoints", 0)
        wins_reg_ot_home = standings_data_.get("homeRegulationPlusOtWins", 0)
        wins_reg_home = standings_data_.get("homeRegulationWins", 0)

        games_played_l10 = standings_data_.get("l10GamesPlayed", 0)
        goal_diff_l10 = standings_data_.get("l10GoalDifferential", 0)
        goals_against_l10 = standings_data_.get("l10GoalsAgainst", 0)
        goals_for_l10 = standings_data_.get("l10GoalsFor", 0)
        losses_l10 = standings_data_.get("l10Losses", 0)
        ot_losses_l10 = standings_data_.get("l10OtLosses", 0)
        wins_l10 = standings_data_.get("l10Wins", 0)
        points_l10 = standings_data_.get("l10Points", 0)
        wins_reg_ot_l10 = standings_data_.get("l10RegulationPlusOtWins", 0)
        wins_reg_l10 = standings_data_.get("l10RegulationWins", 0)

        games_played_road = standings_data_.get("roadGamesPlayed", 0)
        goal_diff_road = standings_data_.get("roadGoalDifferential", 0)
        goals_against_road = standings_data_.get("roadGoalsAgainst", 0)
        goals_for_road = standings_data_.get("roadGoalsFor", 0)
        losses_road = standings_data_.get("roadLosses", 0)
        ot_losses_road = standings_data_.get("roadOtLosses", 0)
        wins_road = standings_data_.get("roadWins", 0)
        points_road = standings_data_.get("roadPoints", 0)
        wins_reg_ot_road = standings_data_.get("roadRegulationPlusOtWins", 0)
        wins_reg_road = standings_data_.get("roadRegulationWins", 0)

        if conf_abbrev == "W":
            top_west.insert(conf_place, standings_data_)
            if div_abbrev == "P":
                top_pac.insert(div_place, standings_data_)
            else:
                top_cen.insert(div_place, standings_data_)
        else:
            top_east.insert(conf_place, standings_data_)
            if div_abbrev == "A":
                top_atl.insert(div_place, standings_data_)
            else:
                top_met.insert(div_place, standings_data_)

    top_atl = top_atl[:3]
    top_met = top_met[:3]
    top_cen = top_cen[:3]
    top_pac = top_pac[:3]

    for team_data in top_east:
        div = team_data["divisionAbbrev"]
        if div == "A":
            if team_data in top_atl:
                continue
            else:
                wc_east.append(team_data)
        else:
            if team_data in top_met:
                continue
            else:
                wc_east.append(team_data)

        if len(wc_east) == 2:
            break

    for team_data in top_west:
        div = team_data["divisionAbbrev"]
        if div == "P":
            if team_data in top_pac:
                continue
            else:
                wc_west.append(team_data)
        else:
            if team_data in top_cen:
                continue
            else:
                wc_west.append(team_data)

        if len(wc_west) == 2:
            break

    fmt_final_results = [
        f"\nTop East",
        f"\nTop Atlantic:",
        top_atl,
        f"\nTop Metropolitan:",
        top_met,
        f"\nWildcard East:",
        wc_east,
        f"\nTop West:",
        f"\nTop Central:",
        top_cen,
        f"\nTop Pacific:",
        top_pac,
        f"\nWildcard West:",
        wc_west
    ]

    lpk_keys = ["div", "conf", "team_id", "position", "name", "number"]
    list_of_players_and_keys = {}  # div, conf, teamid, position,
    list_of_players_and_teams = {}
    list_of_teams = {"E": [], "W": []}
    list_id_pts_skaters = {"E": [], "W": []}
    list_id_sv_pctg_goalies = {"E": [], "W": []}
    team_div, team_conf, team_id, player_position, player_name, player_number = [None for _ in range(6)]
    for line in fmt_final_results:
        if isinstance(line, list):
            for team_data in line:
                if isinstance(team_data, dict):
                    team_conf = team_data["conferenceAbbrev"]
                    team_div = team_data["divisionAbbrev"]
                    team_points = team_data["points"]
                    mascot = team_data['teamCommonName']['default']
                    nhl_util_k = nhl_utility.name_from_mascot(mascot)
                    acronym = nhl_utility.team_attribute(nhl_util_k, "acr")
                    roster = nhl_api.get_team_roster(acronym)
                    print(f"\t{mascot}, {acronym}")
                    for position, position_data in roster.items():
                        print(f"\t\t{position=}")
                        for player in position_data:
                            player_id = player.get("id", "")
                            if player_id:
                                player_position = player.get("positionCode", "")
                                player_number = player.get("sweaterNumber", "")
                                player_name = player.get("firstName", {}).get("default", "") + " " + player.get(
                                    "lastName", {}).get("default", "")
                                stats = nhl_api.get_player_stats(player_id)
                                team_id = stats["currentTeamId"]
                                if team_id not in [t[0] for t in list_of_teams[team_conf]]:
                                    list_of_teams[team_conf].append((team_id, acronym, team_points))
                                if player_id not in list_of_players_and_teams:
                                    list_of_players_and_teams[player_id] = acronym
                                    list_of_players_and_keys[player_id] = {k: v for k, v in zip(lpk_keys,
                                                                                                [team_div, team_conf,
                                                                                                 team_id,
                                                                                                 player_position,
                                                                                                 player_name,
                                                                                                 player_number])}
                                if player_position == "G":
                                    save_pctg = stats.get("featuredStats", {}).get("regularSeason", {}).get("subSeason",
                                                                                                            {}).get(
                                        "points", 0)
                                    list_id_sv_pctg_goalies[team_conf].append((stats["playerId"], save_pctg))
                                else:
                                    pts_this_season = stats.get("featuredStats", {}).get("regularSeason", {}).get(
                                        "subSeason", {}).get("points", 0)
                                    list_id_pts_skaters[team_conf].append((stats["playerId"], pts_this_season))
                            else:
                                stats = "N/A"
                            team_data["stats"] = stats
                            print("\t\t\t" + ", ".join([f"{k}: {v}" for k, v in zip(lpk_keys,
                                                                                    [team_div, team_conf, team_id,
                                                                                     player_position, player_name,
                                                                                     player_number])]))
                            # print(f"\t\t\t{player=}")
                            # print(f"\t\t\t\t{stats=}")
                            # i = 14/0

                    list_id_pts_skaters["E"].sort(key=lambda tup: tup[1], reverse=True)
                    list_id_pts_skaters["W"].sort(key=lambda tup: tup[1], reverse=True)

                    # print(f"\t\t{roster=}")
        else:
            print(line)

    list_of_teams["E"].sort(key=lambda tup: tup[2], reverse=True)
    list_of_teams["W"].sort(key=lambda tup: tup[2], reverse=True)
    print(f"{list_of_teams=}")

    top_players_on_team = {}
    for conf, conf_data in list_id_pts_skaters.items():
        for player_id, pts in conf_data:
            player_team = list_of_players_and_teams[player_id]
            if player_team not in top_players_on_team:
                top_players_on_team[player_team] = []
            p_div, p_conf, p_team, p_pos, p_name, p_num = list_of_players_and_keys[player_id].values()
            top_players_on_team[player_team].append(list_of_players_and_keys[player_id].values())
            print(
                f"{pts=}, {player_id=}, {player_team=}, {p_div=}, {p_conf=}, {p_team=}, {p_pos=}, {p_name=}, {p_num=}")

    # box_num = 0
    pool_sheet_boxes = {"E": {"F": [], "D": [], "T": []}, "W": {"F": [], "D": [], "T": []}}
    pool_sheet_team_counts = {"F": {}, "D": {}, "T": {}}
    for t in list_of_teams["E"] + list_of_teams["W"]:
        team_id, team_acr, team_pts = t
        for k in pool_sheet_team_counts:
            pool_sheet_team_counts[k][team_acr] = 0
    max_same_team_per_box = 4
    for conf in ["E", "W"]:
        for i in range(n_forward_boxes):
            team_picks_per_box = {}
            box = []
            for j in range(n_forwards_per_boxes):
                k = 0
                chx_player_id, chx_player_pts, chx_player_team = None, None, None
                # lens = {t: len(t) for t in pool_sheet_team_counts["F"]}

                while k < len(list_id_pts_skaters[conf]):
                    chx_player_id, chx_player_pts = list_id_pts_skaters[conf][k]
                    chx_player_team = list_of_players_and_teams[chx_player_id]
                    chx_player_pos = list_of_players_and_keys[chx_player_id]["position"]
                    if chx_player_pos in ("C", "L", "R"):
                        w_lens = {t: len(t) for t in pool_sheet_team_counts["F"]}
                        if w_lens.get(chx_player_team, None) is None:
                            w_lens[chx_player_team] = 0
                        w_lens[chx_player_team] += 1
                        if abs(min(w_lens.values()) - max(w_lens.values())) <= 1:
                            # begin selecting
                            if chx_player_team not in team_picks_per_box:
                                team_picks_per_box[chx_player_team] = 0
                            if team_picks_per_box[chx_player_team] <= max_same_team_per_box:
                                team_picks_per_box[chx_player_team] += 1
                                del list_id_pts_skaters[conf][k]
                                break
                    k += 1

                box.append((chx_player_id, chx_player_pts, chx_player_team))
                if chx_player_team not in pool_sheet_team_counts["F"]:
                    pool_sheet_team_counts["F"][chx_player_team] = 0
                pool_sheet_team_counts["F"][chx_player_team] += 1
            pool_sheet_boxes[conf]["F"].append(box)

        for i in range(n_defence_boxes):
            team_picks_per_box = {}
            box = []
            for j in range(n_defence_per_boxes):
                k = 0
                chx_player_id, chx_player_pts, chx_player_team = None, None, None
                while k < len(list_id_pts_skaters[conf]):
                    chx_player_id, chx_player_pts = list_id_pts_skaters[conf][k]
                    chx_player_team = list_of_players_and_teams[chx_player_id]
                    chx_player_pos = list_of_players_and_keys[chx_player_id]["position"]
                    if chx_player_pos == "D":
                        w_lens = {t: len(t) for t in pool_sheet_team_counts["F"]}
                        if w_lens.get(chx_player_team, None) is None:
                            w_lens[chx_player_team] = 0
                        w_lens[chx_player_team] += 1
                        if abs(min(w_lens.values()) - max(w_lens.values())) <= 1:
                            # begin selecting
                            if chx_player_team not in team_picks_per_box:
                                team_picks_per_box[chx_player_team] = 0
                            if team_picks_per_box[chx_player_team] <= max_same_team_per_box:
                                team_picks_per_box[chx_player_team] += 1
                                del list_id_pts_skaters[conf][k]
                                break
                    k += 1

                box.append((chx_player_id, chx_player_pts, chx_player_team))
                if chx_player_team not in pool_sheet_team_counts["D"]:
                    pool_sheet_team_counts["D"][chx_player_team] = 0
                pool_sheet_team_counts["D"][chx_player_team] += 1
            pool_sheet_boxes[conf]["D"].append(box)

        for i in range(2):
            box = []
            for team_data in list_of_teams[conf]:
                team_id, team_acr, team_pts = team_data
                box.append((team_id, team_pts, team_acr))
                if team_acr not in pool_sheet_team_counts["T"]:
                    pool_sheet_team_counts["T"][team_acr] = 0
                pool_sheet_team_counts["T"][team_acr] += 1
            pool_sheet_boxes[conf]["T"].append(box)

    print(f"pool_sheet_boxes")
    for conf, position_boxes in pool_sheet_boxes.items():
        print(f"\tConference: '{conf}'")
        for position, boxes in position_boxes.items():
            print(f"\t\tPosition: '{position}'")
            for i, box in enumerate(boxes):
                print(f"\t\t\tBox {i + 1}")
                if position != "T":
                    for player_id, player_pts, player_team in box:
                        p_name = list_of_players_and_keys[player_id]["name"]
                        print(f"\t\t\t\t{player_pts=}, {player_id=}, {player_team}, {p_name}")
                else:
                    for team_id, team_pts, team_team in box:
                        print(f"\t\t\t\t{team_pts=}, {team_id=}, {team_team}")
    print(f"{pool_sheet_team_counts=}")
    print(f"{list_id_pts_skaters=}")
    for conf, team_data in list_of_teams.items():
        print(f"{conf=}")
        for team_dat in team_data:
            print(f"\t{team_dat=}")

    # save queries to json output for quicker access on re-run
    nhl_api.save_data()

    # print(f"\nTop East")
    # print(f"\nTop Atlantic:")
    # for team_data in top_atl:
    #     mascot = team_data['teamCommonName']['default']
    #     nhl_util_k = nhl_utility.name_from_mascot(mascot)
    #     acronym = nhl_utility.team_attribute(nhl_util_k, "acr")
    #     print(f"{mascot}, {acronym}")
    # print(f"\nTop Metropolitan:")
    # for team_data in top_met:
    #     mascot = team_data['teamCommonName']['default']
    #     nhl_util_k = nhl_utility.name_from_mascot(mascot)
    #     acronym = nhl_utility.team_attribute(nhl_util_k, "acr")
    #     print(f"{mascot}, {acronym}")
    #
    # print(f"\nWildcard East:")
    # for team_data in wc_east:
    #     mascot = team_data['teamCommonName']['default']
    #     nhl_util_k = nhl_utility.name_from_mascot(mascot)
    #     acronym = nhl_utility.team_attribute(nhl_util_k, "acr")
    #     print(f"{mascot}, {acronym}")
    #
    # print(f"\nTop West:")
    # print(f"\nTop Central:")
    # for team_data in top_cen:
    #     mascot = team_data['teamCommonName']['default']
    #     nhl_util_k = nhl_utility.name_from_mascot(mascot)
    #     acronym = nhl_utility.team_attribute(nhl_util_k, "acr")
    #     print(f"{mascot}, {acronym}")
    # print(f"\nTop Pacific:")
    # for team_data in top_pac:
    #     mascot = team_data['teamCommonName']['default']
    #     nhl_util_k = nhl_utility.name_from_mascot(mascot)
    #     acronym = nhl_utility.team_attribute(nhl_util_k, "acr")
    #     print(f"{mascot}, {acronym}")
    #
    # print(f"\nWildcard West:")
    # for team_data in wc_west:
    #     mascot = team_data['teamCommonName']['default']
    #     nhl_util_k = nhl_utility.name_from_mascot(mascot)
    #     acronym = nhl_utility.team_attribute(nhl_util_k, "acr")
    #     print(f"{mascot}, {acronym}")

    # print(f"{nhl_api.get_schedule(today)}")


def bracket_challenge():
    app = tkinter.Tk()

    nhl_api = NHLAPIHandler(max_query_hold_time=3 * 24 * 3600)
    today = datetime.datetime.today()
    standings_today = nhl_api.get_standings(today)
    print(f"{standings_today=}")
    standings_data = {}

    top_east = []
    top_west = []
    top_atl = []
    top_met = []
    top_cen = []
    top_pac = []
    wc_east = []
    wc_west = []

    # w = '/stats/rest/en/skater/summary', h = 'http://api.nhle.com', t = '/stats/rest/en/leaders/skaters/goals', HOST_NAME = 'https://api-web.nhle.com'

    for standings_data_ in standings_today["standings"]:
        # print(f"{standings_data_=}")
        conf_abbrev = standings_data_.get("conferenceAbbrev")
        conf_name = standings_data_.get("conferenceName")
        div_abbrev = standings_data_.get("divisionAbbrev")
        div_name = standings_data_.get("divisionName")

        league_place = standings_data_.get("leagueSequence")
        conf_place = standings_data_.get("conferenceSequence")
        div_place = standings_data_.get("divisionSequence")

        league_place_home = standings_data_.get("leagueHomeSequence")
        league_place_road = standings_data_.get("leagueRoadSequence")
        league_place_l10 = standings_data_.get("leagueL10Sequence")

        conf_place_home = standings_data_.get("conferenceHomeSequence")
        div_place_home = standings_data_.get("divisionHomeSequence")
        conf_place_road = standings_data_.get("conferenceRoadSequence")
        div_place_road = standings_data_.get("divisionRoadSequence")
        conf_place_l10 = standings_data_.get("conferenceL10Sequence")
        div_place_l10 = standings_data_.get("divisionL10Sequence")
        wc_place = standings_data_.get("wildcardSequence")

        team_name = standings_data_.get("teamName", {}).get("default")
        team_name_common = standings_data_.get("teamCommonName", {}).get("default")
        team_name_abbrev = standings_data_.get("teamAbbrev", {}).get("default")
        team_name_fr = standings_data_.get("teamName", {}).get("fr")
        team_name_common_fr = standings_data_.get("teamCommonName", {}).get("fr")
        team_name_abbrev_fr = standings_data_.get("teamAbbrev", {}).get("fr")
        team_logo = standings_data_.get("teamLogo")

        streak_count = standings_data_.get("streakCount", 0)
        streak_code = standings_data_.get("streakCode")
        games_played = standings_data_.get("gamesPlayed", 0)
        points = standings_data_.get("points", 0)
        win_pctg = standings_data_.get("winPctg", 0)
        wins = standings_data_.get("wins", 0)
        losses = standings_data_.get("losses", 0)
        wins_ot = standings_data_.get("shootoutWins", 0)
        losses_ot = standings_data_.get("otLosses", 0)
        losses_so = standings_data_.get("shootoutLosses", 0)
        wins_reg = standings_data_.get("regulationWins", 0)
        wins_reg_ot = standings_data_.get("regulationPlusOtWins", 0)
        wins_reg_ot_pctg = standings_data_.get("regulationPlusOtWinsPctg", 0)

        point_pctg = standings_data_.get("pointsPctg", 0)
        goal_diff = standings_data_.get("goalDifferential", 0)
        goal_diff_pctg = standings_data_.get("goalDifferentialPctg", 0)
        goals_for = standings_data_.get("goalsFor", 0)
        goals_against = standings_data_.get("goalsAgainst", 0)
        goals_per_game = standings_data_.get("goalsForPctg", 0)

        games_played_home = standings_data_.get("homeGamesPlayed", 0)
        goal_diff_home = standings_data_.get("homeGoalDifferential", 0)
        goals_against_home = standings_data_.get("homeGoalsAgainst", 0)
        goals_for_home = standings_data_.get("homeGoalsFor", 0)
        losses_home = standings_data_.get("homeLosses", 0)
        ot_losses_home = standings_data_.get("homeOtLosses", 0)
        wins_home = standings_data_.get("homeWins", 0)
        points_home = standings_data_.get("homePoints", 0)
        wins_reg_ot_home = standings_data_.get("homeRegulationPlusOtWins", 0)
        wins_reg_home = standings_data_.get("homeRegulationWins", 0)

        games_played_l10 = standings_data_.get("l10GamesPlayed", 0)
        goal_diff_l10 = standings_data_.get("l10GoalDifferential", 0)
        goals_against_l10 = standings_data_.get("l10GoalsAgainst", 0)
        goals_for_l10 = standings_data_.get("l10GoalsFor", 0)
        losses_l10 = standings_data_.get("l10Losses", 0)
        ot_losses_l10 = standings_data_.get("l10OtLosses", 0)
        wins_l10 = standings_data_.get("l10Wins", 0)
        points_l10 = standings_data_.get("l10Points", 0)
        wins_reg_ot_l10 = standings_data_.get("l10RegulationPlusOtWins", 0)
        wins_reg_l10 = standings_data_.get("l10RegulationWins", 0)

        games_played_road = standings_data_.get("roadGamesPlayed", 0)
        goal_diff_road = standings_data_.get("roadGoalDifferential", 0)
        goals_against_road = standings_data_.get("roadGoalsAgainst", 0)
        goals_for_road = standings_data_.get("roadGoalsFor", 0)
        losses_road = standings_data_.get("roadLosses", 0)
        ot_losses_road = standings_data_.get("roadOtLosses", 0)
        wins_road = standings_data_.get("roadWins", 0)
        points_road = standings_data_.get("roadPoints", 0)
        wins_reg_ot_road = standings_data_.get("roadRegulationPlusOtWins", 0)
        wins_reg_road = standings_data_.get("roadRegulationWins", 0)

        if conf_abbrev == "W":
            top_west.insert(conf_place, standings_data_)
            if div_abbrev == "P":
                top_pac.insert(div_place, standings_data_)
            else:
                top_cen.insert(div_place, standings_data_)
        else:
            top_east.insert(conf_place, standings_data_)
            if div_abbrev == "A":
                top_atl.insert(div_place, standings_data_)
            else:
                top_met.insert(div_place, standings_data_)

    top_atl = top_atl[:3]
    top_met = top_met[:3]
    top_cen = top_cen[:3]
    top_pac = top_pac[:3]

    for team_data in top_east:
        div = team_data["divisionAbbrev"]
        if div == "A":
            if team_data in top_atl:
                continue
            else:
                wc_east.append(team_data)
        else:
            if team_data in top_met:
                continue
            else:
                wc_east.append(team_data)

        if len(wc_east) == 2:
            break

    for team_data in top_west:
        div = team_data["divisionAbbrev"]
        if div == "P":
            if team_data in top_pac:
                continue
            else:
                wc_west.append(team_data)
        else:
            if team_data in top_cen:
                continue
            else:
                wc_west.append(team_data)

        if len(wc_west) == 2:
            break

    fmt_final_results = [
        f"\nTop East",
        f"\nTop Atlantic:",
        top_atl,
        f"\nTop Metropolitan:",
        top_met,
        f"\nWildcard East:",
        wc_east,
        f"\nTop West:",
        f"\nTop Central:",
        top_cen,
        f"\nTop Pacific:",
        top_pac,
        f"\nWildcard West:",
        wc_west
    ]

    # lpk_keys = ["div", "conf", "team_id", "position", "name", "number"]
    # list_of_players_and_keys = {}  # div, conf, teamid, position,
    # list_of_players_and_teams = {}
    # list_of_teams = {"E": [], "W": []}
    # list_id_pts_skaters = {"E": [], "W": []}
    # list_id_sv_pctg_goalies = {"E": [], "W": []}
    # team_div, team_conf, team_id, player_position, player_name, player_number = [None for _ in range(6)]

    logos = {}
    logo_size = 60, 60
    logo_root = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Web SVGs"
    known_logos = {}
    for pth in os.listdir(logo_root):
        if pth.endswith(".png"):
            splt1 = pth.split("logo_")
            splt2 = splt1[-1].split("_")
            acronym = splt2[0].upper()
            when = splt2[-1][:-4]
            when = datetime.datetime(int(f"20{when[:2]}"), int(f"{when[2:4]}"), int(f"{when[4:]}"))
            known_logos[acronym] = when

    print(f"{known_logos=}")

    for line in fmt_final_results:
        if isinstance(line, list):
            for team_data in line:
                if isinstance(team_data, dict):
                    team_conf = team_data["conferenceAbbrev"]
                    team_div = team_data["divisionAbbrev"]
                    team_points = team_data["points"]
                    team_logo = team_data["teamLogo"]
                    team_games_played = team_data["gamesPlayed"]
                    team_points_per_game = team_points / (1 if team_games_played == 0 else (2 * team_games_played))
                    mascot = team_data['teamCommonName']['default']
                    conf_place = team_data["conferenceSequence"]
                    nhl_util_k = nhl_utility.name_from_mascot(mascot)
                    acronym = nhl_utility.team_attribute(nhl_util_k, "acr")
                    # roster = nhl_api.get_team_roster(acronym)
                    print(f"\t{mascot}, {acronym}, pts={team_points}, gp={team_games_played}, ppg={team_points_per_game}, logo={team_logo}")
                    # logos[acronym] = ImageTk.PhotoImage(Image.open(team_logo).resize(logo_size))

                    if acronym not in known_logos:

                        logo_path_name = f"logo_{acronym.lower()}_{datetime.datetime.now():%Y%m%d}.png"
                        print(f"{logo_path_name=}")
                        my_page = urlopen(team_logo)
                        svg_code = my_page.read()
                        pyvip_img = pyvips.Image.svgload_buffer(svg_code)
                        pyvip_img.write_to_file(logo_path_name)
                        # cairosvg.svg2png(bytestring=svg_code, write_to=logo_path_name)

                    # # create an image file object
                    # print(f"{my_page=}\n{my_page.read()=}")
                    # my_picture = io.BytesIO(my_page.read())
                    # # use PIL to open image formats like .jpg  .png  .gif  etc.
                    # pil_img = Image.open(my_picture).resize(logo_size)
                    # tk_img = ImageTk.PhotoImage(pil_img)
                    # logos[acronym] = tk_img

                    wwww=44
                    # for position, position_data in roster.items():
                    #     print(f"\t\t{position=}")
                    #     for player in position_data:
                    #         player_id = player.get("id", "")
                    #         if player_id:
                    #             player_position = player.get("positionCode", "")
                    #             player_number = player.get("sweaterNumber", "")
                    #             player_name = player.get("firstName", {}).get("default", "") + " " + player.get(
                    #                 "lastName", {}).get("default", "")
                    #             stats = nhl_api.get_player_stats(player_id)
                    #             team_id = stats["currentTeamId"]
                    #             if team_id not in [t[0] for t in list_of_teams[team_conf]]:
                    #                 list_of_teams[team_conf].append((team_id, acronym, team_points, conf_place))
                    #             if player_id not in list_of_players_and_teams:
                    #                 list_of_players_and_teams[player_id] = acronym
                    #                 list_of_players_and_keys[player_id] = {k: v for k, v in zip(lpk_keys,
                    #                                                                             [team_div, team_conf,
                    #                                                                              team_id,
                    #                                                                              player_position,
                    #                                                                              player_name,
                    #                                                                              player_number])}
                    #             if player_position == "G":
                    #                 save_pctg = stats.get("featuredStats", {}).get("regularSeason", {}).get("subSeason",
                    #                                                                                         {}).get(
                    #                     "points", 0)
                    #                 list_id_sv_pctg_goalies[team_conf].append((stats["playerId"], save_pctg))
                    #             else:
                    #                 pts_this_season = stats.get("featuredStats", {}).get("regularSeason", {}).get(
                    #                     "subSeason", {}).get("points", 0)
                    #                 list_id_pts_skaters[team_conf].append((stats["playerId"], pts_this_season))
                    #         else:
                    #             stats = "N/A"
                    #         team_data["stats"] = stats
                    #         print("\t\t\t" + ", ".join([f"{k}: {v}" for k, v in zip(lpk_keys,
                    #                                                                 [team_div, team_conf, team_id,
                    #                                                                  player_position, player_name,
                    #                                                                  player_number])]))
                    #         # print(f"\t\t\t{player=}")
                    #         # print(f"\t\t\t\t{stats=}")
                    #         # i = 14/0
                    #
                    # list_id_pts_skaters["E"].sort(key=lambda tup: tup[1], reverse=True)
                    # list_id_pts_skaters["W"].sort(key=lambda tup: tup[1], reverse=True)
                    #
                    # # print(f"\t\t{roster=}")
        else:
            print(line)

    # list_of_teams["E"].sort(key=lambda tup: tup[3])
    # list_of_teams["W"].sort(key=lambda tup: tup[3])
    # print(f"{list_of_teams=}")

    positions = [
        [
            [],
            []
        ]
    ]

    app.mainloop()



if __name__ == "__main__":
    # nhl_api = NHLAPIHandler()

    # today = datetime.datetime.today()
    # # scores_today = nhl_api.get_score(today + datetime.timedelta(days=-1))
    # scores_today = nhl_api.is_game_ongoing_now(r_type="next_games")  # fetches the newest data
    #
    # # scores_today = nhl_api.get_score(today)
    #
    # print(f"{type(scores_today)=} {scores_today=}")
    #
    # df_scores_today_gameWeek = pd.DataFrame(scores_today.get("gameWeek", {}))
    # df_scores_today_oddsPartners = pd.DataFrame(scores_today.get("oddsPartners", {}))
    # scores_today_dict = scores_today.get("games", [])
    # df_scores_today_games = pd.DataFrame(scores_today_dict)
    #
    # print(f"{nhl_api.get_standings(today)=}")

    # playoff_pool_sheet()
    # playoff_pool_sheet_view_only()

    bracket_challenge()

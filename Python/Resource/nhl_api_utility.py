import requests
import datetime
from typing import Literal
import pandas as pd

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

    def __init__(self):
        self.history = {}

    def query_url(self, url, do_print=False, check_history=True) -> dict | None:
        if do_print:
            print(f"{url=}")

        if check_history:
            if url in self.history:
                return self.history[url]

        response = requests.get(url)
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204:
            ct = response.headers["Content-Type"].lower()
            if ct.startswith("application/json"):
                self.history[url] = response.json()
            elif ct.startswith("text/javascript"):
                self.history[url] = eval(response.text.replace("jsonFeed(", "")[:-2])

        return self.history.get(url, None)

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


def playoff_pool_sheet(
        n_forwards: int = 7,
        n_defence: int = 3
):
    nhl_api = NHLAPIHandler()
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

    print(f"\nTop East")
    print(f"\nTop Atlantic:")
    for team_data in top_atl:
        print(f"{team_data['teamCommonName']['default']}")
    print(f"\nTop Metropolitan:")
    for team_data in top_met:
        print(f"{team_data['teamCommonName']['default']}")

    print(f"\nWildcard East:")
    for team_data in wc_east:
        print(f"{team_data['teamCommonName']['default']}")

    print(f"\nTop West:")
    print(f"\nTop Central:")
    for team_data in top_cen:
        print(f"{team_data['teamCommonName']['default']}")
    print(f"\nTop Pacific:")
    for team_data in top_pac:
        print(f"{team_data['teamCommonName']['default']}")

    print(f"\nWildcard West:")
    for team_data in wc_west:
        print(f"{team_data['teamCommonName']['default']}")

    print(f"{nhl_api.get_schedule(today)}")


if __name__ == "__main__":
    nhl_api = NHLAPIHandler()

    today = datetime.datetime.today()
    # scores_today = nhl_api.get_score(today + datetime.timedelta(days=-1))
    scores_today = nhl_api.is_game_ongoing_now(r_type="next_games")  # fetches the newest data

    # scores_today = nhl_api.get_score(today)

    print(f"{type(scores_today)=} {scores_today=}")

    df_scores_today_gameWeek = pd.DataFrame(scores_today.get("gameWeek", {}))
    df_scores_today_oddsPartners = pd.DataFrame(scores_today.get("oddsPartners", {}))
    scores_today_dict = scores_today.get("games", [])
    df_scores_today_games = pd.DataFrame(scores_today_dict)

    print(f"{nhl_api.get_standings(today)=}")

    playoff_pool_sheet()

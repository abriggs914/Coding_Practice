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

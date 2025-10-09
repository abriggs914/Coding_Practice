import os.path

import pandas as pd
import streamlit

from streamlit_utility import *

import requests
import datetime
from dateutil import tz
import pause
import json


NHL_ASSET_API_URL: str = "https://assets.nhle.com/"
NHL_STATS_API_URL: str = "https://api.nhle.com/stats/rest/en/"
NHL_API_URL: str = "https://api-web.nhle.com/"
NHL_PLAYER_API_URL: str = "{0}v1/player/".format(NHL_API_URL)
PATH_UNKNOWN_IMAGE: str = r"C:\Users\abrig\Documents\Coding_Practice\Resources\Flags\unknown_flag.png"


def f_season(season_str: int) -> str:
    ss = str(season_str)
    return f"{ss[:4]}-{ss[-4:]}"


class NHLStandings:

    def __init__(self, s_data):
        self.s_data = s_data
        self.wild_card_indicator = s_data.get("wild_card_indicator")
        self.standings_datetime_utc = s_data.get("standingsDateTimeUtc")
        self.df_standings: pd.DataFrame = pd.DataFrame(s_data.get("standings", []))
        self.df_standings["team_name"] = ""
        self.df_standings["t_id"] = None
        for i, row in self.df_standings.iterrows():
            self.df_standings.loc[i, "team_name"] = row.get("teamName", {}).get("default")


class NHLTeam:

    def __init__(self, t_data):

        self.t_data = t_data
        self.t_id: str = t_data["id"]
        self.franchise_id: str = t_data["franchiseId"]
        self.league_id: str = t_data["leagueId"]
        self.full_name = t_data.get("fullName")
        self.raw_tri_code = t_data.get("rawTriCode")
        self.tri_code = t_data.get("triCode")

    def __eq__(self, other):
        return self.t_id == other.t_id

    def __repr__(self):
        return f"{self.tri_code}"


class NHLCountry:

    def __init__(self, c_data):

        self.c_data = c_data
        self.c_id: str = c_data["id"]
        self.country_3_code = c_data.get("country3Code")
        self.country_code = c_data.get("countryCode")
        self.country_name = c_data.get("countryName")
        self.has_player_stats = c_data.get("hasPlayerStats")
        self._image_url = c_data.get("imageUrl")
        self.ioc_code = c_data.get("iocCode")
        self.is_active = c_data.get("isActive")
        self.nationality_name = c_data.get("nationalityName")
        self.olympic_url = c_data.get("olympicUrl")
        self._thumbnail_url = c_data.get("thumbnailUrl")

    def __eq__(self, other):
        return self.c_id == other.c_id

    def __repr__(self):
        return f"{self.country_name}"

    def get_image_url(self):
        return "{0}{1}".format(NHL_ASSET_API_URL, self._image_url.removeprefix("/"))

    def set_image_url(self, image_url_in):
        self._image_url = image_url_in

    def del_image_url(self):
        del self._image_url

    def get_thumbnail_url(self):
        return "{0}{1}".format(NHL_ASSET_API_URL, self._thumbnail_url.removeprefix("/"))

    def set_thumbnail_url(self, thumbnail_url_in):
        self._thumbnail_url = thumbnail_url_in

    def del_thumbnail_url(self):
        del self._thumbnail_url

    image_url = property(get_image_url, set_image_url, del_image_url)
    thumbnail_url = property(get_thumbnail_url, set_thumbnail_url, del_thumbnail_url)


class NHLPlayer:

    def __init__(self, p_data):
        self.data = p_data
        self.p_id: int = p_data.get("playerId")
        self.path_team_logo = p_data.get("teamLogo", PATH_UNKNOWN_IMAGE)
        self.path_headshot_logo = p_data.get("headshot", PATH_UNKNOWN_IMAGE)
        self.path_hero_shot_logo = p_data.get("heroImage", PATH_UNKNOWN_IMAGE)

        self.name_first = p_data.get("firstName", dict()).get("default")
        self.name_last = p_data.get("lastName", dict()).get("default")
        # print(f" {self.name_first=}, {self.name_last=}")

        self.number = p_data.get("sweaterNumber")
        self.position = p_data.get("position")
        self.shoots_catches = p_data.get("shootsCatches")
        self.height_inch = p_data.get("heightInInches")
        self.height_cent = p_data.get("heightInCentimeters")
        self.weight_lb = p_data.get("weightInPounds")
        self.weight_kg = p_data.get("weightInKilograms")
        self.is_active = p_data.get("isActive")
        self.dob = p_data.get("birthDate")
        self.birth_city = p_data.get("birthCity", dict()).get("default")
        self.birth_province = p_data.get("birthStateProvince", dict()).get("default")
        self.birth_country: NHLCountry = p_data.get("birthCountry")

        self.in_HHOF = p_data.get("inHHOF")

        self.draft_year = p_data.get("draftDetails", dict()).get("year")
        self.draft_team_abbrev = p_data.get("draftDetails", dict()).get("teamAbbrev")
        self.draft_round = p_data.get("draftDetails", dict()).get("round")
        self.draft_pick_in_round = p_data.get("draftDetails", dict()).get("pickInRound")
        self.draft_overall_pick = p_data.get("draftDetails", dict()).get("overallPick")

        self.team: NHLTeam = None
        self.team_id = p_data.get("currentTeamId")
        self.team_abbrev = p_data.get("currentTeamAbbrev")
        self.team_name = p_data.get("fullTeamName", dict()).get("default")
        self.team_name_fr = p_data.get("fullTeamName", dict()).get("fr", self.team_name)
        self.team_common_name = p_data.get("teamCommonName", dict()).get("default", self.team_name)
        self.team_place_name = p_data.get("teamPlaceNameWithPreposition", dict()).get("default")
        self.team_place_name_fr = p_data.get("teamPlaceNameWithPreposition", dict()).get("fr", self.team_place_name)

        self._featured_stats = p_data.get("featuredStats", dict())
        self.career_totals: pd.DataFrame = pd.DataFrame(p_data.get("careerTotals", dict()))
        self.last_5_games = p_data.get("last5Games", list())
        self.season_totals: pd.DataFrame = pd.DataFrame(p_data.get("seasonTotals", list()))
        self.current_team_roster = p_data.get("currentTeamRoster", list())

        # self.career_totals["total"] = self.career_totals["regularSeason"] + self.career_totals["playoffs"]

        # for k, v in self.data.items():
        #     setattr(self, k, v)

    def to_df_row(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if type(v) not in (list, tuple, dict, pd.DataFrame)}

    def get_featured_stats(self) -> tuple[int, pd.DataFrame]:
        featured_stats_season = self._featured_stats["season"]
        obj_featured_stats = pd.DataFrame({
            "regularSeason_sub_season": self._featured_stats.get("regularSeason", {}).get("subSeason"),
            "regularSeason_career": self._featured_stats.get("regularSeason", {}).get("career"),
            "playoffs_sub_season": self._featured_stats.get("playoffs", {}).get("subSeason"),
            "playoffs_career": self._featured_stats.get("playoffs", {}).get("career")
        })
        return featured_stats_season, obj_featured_stats

    def set_featured_stats(self, featured_stats_in):
        self._featured_stats = featured_stats_in

    def del_featured_stats(self):
        del self._featured_stats

    def __eq__(self, other):
        return self.p_id == other.p_id

    def __repr__(self):
        return f"#{self.p_id} {self.name_first} {self.name_last}"

    featured_stats = property(get_featured_stats, set_featured_stats, del_featured_stats)

    # def get_id(self) -> int:
    #     return getattr(self, "playerId")
    #
    # def set_id(self, p_id: int):
    #     setattr(self, "playerId", p_id)
    #
    # def del_id(self):
    #     delattr(self, "playerId")
    #
    # def get_first_name(self) -> int:
    #     return getattr(self, "firstName", {}).get("default")
    #
    # def set_first_name(self, first_name: str):
    #     getattr(self, "firstName", {})["default"] = first_name
    #
    # def del_first_name(self):
    #     delattr(getattr(self, "firstName", {}), "default")
    #
    # def get_last_name(self) -> int:
    #     return getattr(self, "lastName", {}).get("default")
    #
    # def set_last_name(self, last_name: str):
    #     getattr(self, "lastName", {})["default"] = last_name
    #
    # def del_last_name(self):
    #     delattr(getattr(self, "lastName", {}), "default")
    #
    # def __repr__(self):
    #     return f"#{self.p_id} {self.first_name} {self.last_name}"
    #
    # p_id = property(get_id, set_id, del_id)
    # first_name = property(get_first_name, set_first_name, del_first_name)
    # last_name = property(get_last_name, set_last_name, del_last_name)


class NHLAPIHandler:

    def __init__(self):
        # self.NHL_API_URL: str = "http://statsapi.web.nhl.com/api/v1/"
        self.save_file = "nhl_api_handler_save.json"

        self.max_secs_get_teams: int = 60 * 60 * 24          # every day
        self.max_secs_get_glossary: int = 60 * 60 * 24       # every day
        self.max_secs_get_player_landing: int = 60 * 60 * 4  # every 4 hours
        self.max_secs_get_country: int = 60 * 60 * 24        # every day
        self.max_secs_get_roster = 60 * 60 * 12              # every 12 hours

        self.save_file_df_columns = ["url", "date", "result"]

        if os.path.exists(self.save_file):
            with open(self.save_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
            self.df_saved_data = pd.DataFrame(data, columns=self.save_file_df_columns)
            if "date" in self.df_saved_data.columns and not self.df_saved_data.empty:
                self.df_saved_data["date"] = pd.to_datetime(self.df_saved_data["date"], errors="coerce")
        else:
            self.df_saved_data = pd.DataFrame(columns=self.save_file_df_columns)
            self._flush_to_disk()

        self.df_teams: pd.DataFrame = pd.DataFrame()
        self.df_glossary: pd.DataFrame = pd.DataFrame()
        self.df_countries: pd.DataFrame = pd.DataFrame()
        self.df_players: pd.DataFrame = pd.DataFrame(columns=["p_id"])

    def _flush_to_disk(self):
        # Serialize datetimes as ISO strings
        out_df = self.df_saved_data.copy()
        if "date" in out_df.columns and not out_df.empty:
            out_df["date"] = out_df["date"].astype("datetime64[ns]").dt.tz_localize(None).dt.strftime(
                "%Y-%m-%dT%H:%M:%S")
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(out_df.to_dict(orient="records"), f, ensure_ascii=False)

    def create_save_file(self, overwrite: bool = False):
        if overwrite or not os.path.exists(self.save_file):
            with open(self.save_file, "w") as f:
                f.write(json.dumps([]))

    def query(self, url: str, hold_time_secs: int = 0):
        now = datetime.datetime.now()
        self.create_save_file(overwrite=False)
        url = url.strip().lower()
        if not url:
            raise ValueError("url cannot be empty")

        # Find rows matching this URL
        mask = self.df_saved_data["url"] == url
        if mask.any():
            # Get the most recent row for this URL
            latest_idx = self.df_saved_data.loc[mask, "date"].idxmax()
            last_date = self.df_saved_data.at[latest_idx, "date"]
            last_result = self.df_saved_data.at[latest_idx, "result"]

            if pd.notnull(last_date) and hold_time_secs > 0:
                if (now - last_date).total_seconds() < hold_time_secs:
                    return last_result

        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            pref = "jsonFeed("
            suff = ");"
            if response.text.startswith(pref) and response.text.endswith(suff):
                results = eval(response.text.replace(pref, "").replace(suff, "").strip())
            else:
                results = response.json()
        else:
            results = {}

        if mask.any():
            idx = self.df_saved_data.loc[mask].index
            self.df_saved_data.loc[idx, ["date", "result"]] = [now, results]
        else:
            new_row = pd.DataFrame([{"url": url, "date": now, "result": results}])
            self.df_saved_data = pd.concat([self.df_saved_data, new_row], ignore_index=True)

        # Persist to disk
        self._flush_to_disk()

        return results

    def get_team_data(self) -> pd.DataFrame:
        url = '{0}team'.format(NHL_STATS_API_URL)
        max_t = self.max_secs_get_teams
        results = self.query(url, max_t)
        self.df_teams = pd.DataFrame(results.get("data", []))
        return self.df_teams.copy()

    def get_glossary_data(self) -> pd.DataFrame:
        url = '{0}glossary'.format(NHL_STATS_API_URL)
        max_t = self.max_secs_get_glossary
        results = self.query(url, max_t)
        self.df_glossary = pd.DataFrame(results.get("data", []))
        return self.df_glossary.copy()

    def get_player_data(self, pid: int) -> NHLPlayer:
        if not len(str(pid)) == 7:
            raise ValueError(f"param 'pid' must be an integer of length 7, got '{pid}'.")

        result = self.query("{0}{1}/landing".format(NHL_PLAYER_API_URL, pid), self.max_secs_get_player_landing)
        player = NHLPlayer(result)
        player.birth_country = self.lookup_country(player.birth_country)
        player.team = self.lookup_team(player.team_id)
        self.df_players = self.df_players[~(self.df_players["p_id"] == pid)]
        df_new_player = pd.DataFrame([{k: v for k, v in player.__dict__.items() if type(v) not in (list, tuple, dict, pd.DataFrame)}])
        self.df_players = pd.concat([self.df_players, df_new_player], ignore_index=True)
        return player

    def get_country_data(self):
        url = "{0}country".format(NHL_STATS_API_URL)
        max_t = self.max_secs_get_country
        results = self.query(url, max_t)
        self.df_countries = pd.DataFrame(results.get("data", []))
        return self.df_countries.copy()

    def get_team_roster(self, team_tri_code, season=None):
        if season is None:
            season = self.get_this_season()
        # return requests.get(f"https://api-web.nhle.com/v1/roster/{team_tri_code}/{season}").json()
        results = self.query("{0}/v1/roster/{1}/{2}".format(NHL_API_URL, team_tri_code, season), self.max_secs_get_roster)
        data = []
        for pos, pl_lst in results.items():
            for i, pl_data in enumerate(pl_lst):
                pl_data["position"] = pos
                p_id = pl_data["id"]
                pl = self.get_player_data(p_id)
                data.append(pl.to_df_row())

        return pd.DataFrame(data)

    def get_standings(self, date: datetime.date = None) -> NHLStandings:
        """Get df_standings up to a particular date"""
        # df_standings keys:
        # ['wildCardIndicator', 'df_standings']
        if date is None:
            date = datetime.date.today()
        url = f"{NHL_API_URL}v1/standings/{date:%Y-%m-%d}"
        standings = NHLStandings(self.query(url))
        st.write(standings.s_data)
        for i, row in self.df_teams.iterrows():
            f_name = row.get("full_name", "").lower()
            standings.df_standings.loc[
                standings.df_standings["team_name"].str.lower() == f_name,
                "t_id"
            ] = row["id"]
        return standings

    def get_country(self) -> dict | None:
        url = f"{NHL_API_URL}/v1/location"
        return self.query(url)

    def get_geolocation(self) -> dict | None:
        url = "https://geolocation.onetrust.com/cookieconsentpub/v1/geo/location"
        return self.query(url)

    # def get_team_score(self, team_id: str):
    #
    #     """ Function to get the score of the game depending on the chosen team.
    #     Inputs the team ID and returns the score found on web. """
    #
    #     # Get current time
    #     now = datetime.datetime.now()
    #
    #     # HOST_NAME = f"https://api-web.nhle.com"
    #     # url = f"{NHLAPIHandler.HOST_NAME}/v1/schedule/{date:%Y-%m-%d}"
    #     # # Set URL depending on team selected
    #     url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    #
    #     st.write(self.query(url))
    #
    #     # # Avoid request errors (might still not catch errors)
    #     # try:
    #     #     score = requests.get(url).json()
    #     #
    #     #     #game_time = str(score['dates'][0]['games'][0]['df_teams'])
    #     #     #print (game_time)
    #     #
    #     #     if int(team_id) == int(score['dates'][0]['games'][0]['df_teams']['home']['team']['id']):
    #     #         score = int(score['dates'][0]['games'][0]['df_teams']['home']['score'])
    #     #
    #     #     else:
    #     #         score = int(score['dates'][0]['games'][0]['df_teams']['away']['score'])
    #     #
    #     #     # Print score for test
    #     #     print("Score: {0} Time: {1}:{2}:{3}".format(score, now.hour, now.minute, now.second),end='\r')
    #     #
    #     #     return score
    #     #
    #     # except requests.exceptions.RequestException:
    #     #     print("Error encountered, returning 0 for score")
    #     #     return 0

    def lookup_country(self, player_birth_country):
        if self.df_countries.empty:
            self.get_country_data()
        df_c = self.df_countries
        df_same_c: pd.DataFrame = df_c.loc[
            (df_c["id"].str.lower() == player_birth_country.lower())
            | (df_c["country3Code"].str.lower() == player_birth_country.lower())
            | (df_c["countryCode"].str.lower() == player_birth_country.lower())
            | (df_c["countryName"].str.lower() == player_birth_country.lower())
            | (df_c["iocCode"].str.lower() == player_birth_country.lower())
            | (df_c["nationalityName"].str.lower() == player_birth_country.lower())
        ]

        if df_same_c.empty:
            return player_birth_country

        return NHLCountry(dict(df_same_c.iloc[0]))

    def lookup_team(self, team_id_country):
        if self.df_teams.empty:
            self.get_country_data()
        df_t = self.df_teams
        df_same_t: pd.DataFrame = df_t.loc[
            (df_t["id"].astype(str).str.lower() == str(team_id_country).lower())
            | (df_t["fullName"].astype(str).str.lower() == str(team_id_country).lower())
            | (df_t["rawTricode"].astype(str).str.lower() == str(team_id_country).lower())
            | (df_t["triCode"].astype(str).str.lower() == str(team_id_country).lower())
        ]

        if df_same_t.empty:
            return team_id_country

        return NHLTeam(dict(df_same_t.iloc[0]))

    def get_this_season(self) -> str:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        if month < 7 or 8 < month:
            return f"{year}{year+1}"
        else:
            return "off"


# def get_team_id(team_name):
#     """ Function to get team of user and return NHL team ID"""
#
#     url = '{0}df_teams'.format(NHL_API_URL)
#     response = requests.get(url)
#     results = response.json()
#
#     for team in results['df_teams']:
#         if team['franchise']['teamName'] == team_name:
#             return team['id']
#
#     raise Exception("Could not find ID for team {0}".format(team_name))
#
#
# def fetch_score(team_id):
#     """ Function to get the score of the game depending on the chosen team.
#     Inputs the team ID and returns the score found on web. """
#
#     # Get current time
#     now = datetime.datetime.now()
#
#     # Set URL depending on team selected
#     url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
#     # Avoid request errors (might still not catch errors)
#     try:
#         score = requests.get(url).json()
#
#         #game_time = str(score['dates'][0]['games'][0]['df_teams'])
#         #print (game_time)
#
#         if int(team_id) == int(score['dates'][0]['games'][0]['df_teams']['home']['team']['id']):
#             score = int(score['dates'][0]['games'][0]['df_teams']['home']['score'])
#
#         else:
#             score = int(score['dates'][0]['games'][0]['df_teams']['away']['score'])
#
#         # Print score for test
#         print("Score: {0} Time: {1}:{2}:{3}".format(score, now.hour, now.minute, now.second),end='\r')
#
#         return score
#
#     except requests.exceptions.RequestException:
#         print("Error encountered, returning 0 for score")
#         return 0
#
#
# def check_game_status(team_id,date):
#     """ Function to check if there is a game now with chosen team. Returns True if game, False if NO game. """
#     # Set URL depending on team selected and date
#     url = '{0}schedule?teamId={1}&date={2}'.format(NHL_API_URL, team_id,date)
#
#     try:
#         #get game state from API (no state when no games on date)
#         game_status = requests.get(url).json()
#         game_status = game_status['dates'][0]['games'][0]['status']['detailedState']
#         return game_status
#
#     except IndexError:
#         #Return No Game when no state available on API since no game
#         return 'No Game'
#
#     except requests.exceptions.RequestException:
#         # Return No Game to keep going
#         return 'No Game'
#
#
# def get_next_game_date(team_id):
#     "get the time of the next game"
#     date_test = datetime.date.today()
#     gameday = check_game_status(team_id,date_test)
#
#     #Keep going until game day found
#     while ("Scheduled" not in gameday):
#         date_test = date_test + datetime.timedelta(days=1)
#         gameday = check_game_status(team_id,date_test)
#
#     #Get start time of next game
#     url = '{0}schedule?teamId={1}&date={2}'.format(NHL_API_URL, team_id,date_test)
#     utc_game_time = requests.get(url).json()
#     utc_game_time = utc_game_time['dates'][0]['games'][0]['gameDate']
#     next_game_time = convert_to_local_time(utc_game_time) - datetime.timedelta(seconds=30)
#
#     return next_game_time
#
#
# def convert_to_local_time(utc_game_time):
#     "convert to local time from UTC"
#     utc_game_time = datetime.datetime.strptime(utc_game_time, '%Y-%m-%dT%H:%M:%SZ')
#     utc_game_time = utc_game_time.replace(tzinfo=tz.tzutc())
#     local_game_time = utc_game_time.astimezone(tz.tzlocal())
#
#     return local_game_time


k_nhl_api_handler: str = "key_nhl_api_handler"
if k_nhl_api_handler not in st.session_state:
    st.session_state[k_nhl_api_handler] = NHLAPIHandler()
nhl: NHLAPIHandler = st.session_state[k_nhl_api_handler]

display_df(
    nhl.df_saved_data,
"nhl.df_saved_data"
)

teams = nhl.get_team_data()

display_df(teams, "Teams")
display_df(nhl.get_country_data(), "Countries")
display_df(nhl.get_glossary_data(), "Glossary:")

pl_id = 8478864
pl_obj: NHLPlayer = nhl.get_player_data(pl_id)
pl_team: NHLTeam = pl_obj.team
st.write(f"Player ID# {pl_id}")
st.write(pl_obj)
image_cols = st.columns(4)
image_cols[0].image(pl_obj.path_team_logo, width=300)
image_cols[1].image(pl_obj.birth_country.image_url, width=300)
image_cols[2].image(pl_obj.path_headshot_logo, width=300)
image_cols[3].image(pl_obj.path_hero_shot_logo, width=300)

pl_obj_featured_stats_season, df_pl_obj_featured_stats = pl_obj.featured_stats
display_df(df_pl_obj_featured_stats, f"Featured Stats {f_season(pl_obj_featured_stats_season)}")
display_df(pl_obj.career_totals, "Career Totals")
display_df(pl_obj.season_totals, "Season Totals")

display_df(
    nhl.df_players,
    "Known NHL Players"
)

st.write(pl_team.full_name)
display_df(
    nhl.get_team_roster(pl_team.tri_code),
    f"{pl_team.full_name} {f_season(nhl.get_this_season())} Team Roster"
)

st.write(nhl.get_country())
st.write(nhl.get_geolocation())

standings_now = nhl.get_standings()

display_df(
    standings_now.df_standings,
    "Standings as of now:"
)
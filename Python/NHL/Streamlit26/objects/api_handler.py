import os
import json
import datetime
from typing import Any, Optional

import requests
import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from objects.team import NHLTeam
from resources.resource import NHL_STATS_API_URL, NHL_PLAYER_API_URL, NHL_API_URL, DATE_FMT, DEFAULT_SEASON_END_DATE
from utils.utility import percent
from objects.game import NHLGame, NHLGameDate, NHLBoxScore, NHLGameLanding
from objects.league import NHLSchedule, NHLStandings, NHLSeason, NHLCountry, NHLScoreboard
from objects.player import NHLPlayer
from utils.utils import get_this_season_str, f_standing_record


class NHLAPIHandler:

    def __init__(self, init: bool = False):
        print("NHLAPIHandler")
        # self.NHL_API_URL: str = "http://statsapi.web.nhl.com/api/v1/"
        self.init: bool = init
        self.save_file = "nhl_api_handler_save.json"

        self.max_secs_get_teams: int = 60 * 60 * 24  # every day
        self.max_secs_get_glossary: int = 60 * 60 * 24  # every day
        self.max_secs_get_player_landing: int = 60 * 60 * 4  # every 4 hours
        self.max_secs_get_country: int = 60 * 60 * 24 * 7  # every week
        self.max_secs_get_roster: int = 60 * 60 * 12  # every 12 hours
        self.max_secs_get_seasons: int = 60 * 60 * 24 * 7  # every week
        self.max_secs_get_standings: int = 60 * 5  # every 5 minutes
        self.max_secs_get_schedule: int = 60 * 60 * 24  # every day
        self.max_secs_get_game_box_score: int = 60  # every minute
        self.max_secs_get_game_landing: int = 60  # every minute

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

        self.games: dict[int: dict[str: NHLGame]] = {}
        self.df_games_boxscore: pd.DataFrame = pd.DataFrame(columns=["g_id"])
        self.df_games_scoreboard: pd.DataFrame = pd.DataFrame(columns=["g_id"])
        self.df_games_landing: pd.DataFrame = pd.DataFrame(columns=["g_id"])
        self.df_teams: pd.DataFrame = pd.DataFrame(columns=["t_id"])
        self.df_glossary: pd.DataFrame = pd.DataFrame()
        self.df_countries: pd.DataFrame = pd.DataFrame(columns=["c_id"])
        self.df_players: pd.DataFrame = pd.DataFrame(columns=["p_id"])
        self.df_seasons: pd.DataFrame = pd.DataFrame(columns=["s_id"])
        # self.df_schedule: pd.DataFrame = pd.DataFrame(columns=["g_id"])

        self.get_team_data()

        if self.init:
            self.get_seasons_data()
            self.get_standings()
            schedule: NHLSchedule = self.get_schedule()
            d1: datetime.date = schedule.regular_season_start_date
            d2: datetime.date = d1
            ed: datetime.date = schedule.regular_season_end_date
            # st.write(f"{d1=}, {d2=}, {ed=}")
            while d1 <= ed:
                d2 = d1
                # st.write(f"{d1=}, {d2=}")
                schedule: NHLSchedule = self.get_schedule(d1)
                d1 = schedule.next_start_date
                if d2 == d1 or d1 is None:
                    break

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
        print(f"{now:%Y-%m-%d %H:%M:%S} - {url}")
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
            if self.df_saved_data.empty:
                self.df_saved_data = new_row.copy()
            else:
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
        df_new_player = pd.DataFrame(
            [{k: v for k, v in player.__dict__.items() if type(v) not in (list, tuple, dict, pd.DataFrame)}])
        if self.df_players.empty:
            self.df_players = df_new_player.copy()
        else:
            self.df_players = pd.concat([self.df_players, df_new_player], ignore_index=True)
        return player

    def get_country_data(self) -> pd.DataFrame:
        url = "{0}country".format(NHL_STATS_API_URL)
        max_t = self.max_secs_get_country
        results = self.query(url, max_t)
        self.df_countries = pd.DataFrame(results.get("data", []))
        return self.df_countries.copy()

    def get_seasons_data(self) -> pd.DataFrame:
        url = "{0}v1/standings-season".format(NHL_API_URL)
        max_t = self.max_secs_get_seasons
        results = self.query(url, max_t)
        current_date: datetime.date = datetime.datetime.strptime(
            results.get("currentDate", datetime.datetime.now().strftime(DATE_FMT)), DATE_FMT).date()
        self.df_seasons = pd.DataFrame(results.get("seasons", []))
        self.df_seasons = self.df_seasons.rename(columns={"id": "s_id"})
        self.df_seasons["standingsEnd"] = self.df_seasons["standingsEnd"].apply(
            lambda dv: datetime.datetime.strptime(dv, DATE_FMT).date())
        self.df_seasons["standingsStart"] = self.df_seasons["standingsStart"].apply(
            lambda dv: datetime.datetime.strptime(dv, DATE_FMT).date())
        self.df_seasons["playoffsStart"] = self.df_seasons["standingsEnd"] + datetime.timedelta(days=1)
        self.df_seasons["playoffsEnd"] = self.df_seasons["standingsEnd"] + datetime.timedelta(days=7 * 14)
        before_christmas = current_date.month > 8
        if current_date < datetime.datetime(current_date.year + (1 if before_christmas else 0),
                                            DEFAULT_SEASON_END_DATE.month, DEFAULT_SEASON_END_DATE.day).date():
            # this season is ongoing
            l_idx: int = self.df_seasons.index.tolist()[-1]
            print(f"{l_idx=}")
            self.df_seasons.loc[l_idx, "standingsEnd"] = datetime.date(
                current_date.year + (1 if before_christmas else 0), DEFAULT_SEASON_END_DATE.month,
                DEFAULT_SEASON_END_DATE.day + 1)
            self.df_seasons.loc[l_idx, "playoffsStart"] = self.df_seasons.loc[
                                                              l_idx, "standingsEnd"] + datetime.timedelta(days=1)
            self.df_seasons.loc[l_idx, "playoffsEnd"] = self.df_seasons.loc[l_idx, "standingsEnd"] + datetime.timedelta(
                days=7 * 14)
        return self.df_seasons.copy()

    def get_team_roster(self, team_tri_code, season=None, pb=None, pb_text=None) -> pd.DataFrame:
        if season is None:
            season = get_this_season_str()
        # return requests.get(f"https://api-web.nhle.com/v1/roster/{team_tri_code}/{season}").json()
        results = self.query("{0}/v1/roster/{1}/{2}".format(NHL_API_URL, team_tri_code, season),
                             self.max_secs_get_roster)
        data = []
        use_pb: bool = isinstance(pb, DeltaGenerator)
        n = sum([len(pl_lst) for pl_lst in results.values()]) if use_pb else 0
        c = 0
        for pos, pl_lst in results.items():
            for i, pl_data in enumerate(pl_lst):
                pl_data["position"] = pos
                p_id = pl_data["id"]
                pl = self.get_player_data(p_id)
                data.append(pl.to_df_row())
                if use_pb:
                    c += 1
                    pb.progress(value=c / n, text=f"{pb_text if pb_text else ''}{percent(c / n)}")

        if use_pb:
            pb.empty()

        return pd.DataFrame(data)

    def get_standings(self, date_in: datetime.date = None) -> NHLStandings:
        """Get df_standings up to a particular date"""
        print("self.get_standings")
        # df_standings keys:
        # ['wildCardIndicator', 'df_standings']
        if date_in is None:
            date_in = datetime.date.today()
        url = f"{NHL_API_URL}v1/standings/{date_in:%Y-%m-%d}"
        max_t = self.max_secs_get_standings
        standings = NHLStandings(self.query(url, hold_time_secs=max_t))
        # st.write(standings.s_data)
        for i, row in self.df_teams.iterrows():
            f_name = row.get("fullName", "").lower()
            standings.df_standings.loc[
                standings.df_standings["team_name"].str.lower() == f_name,
                "t_id"
            ] = row["id"]
        return standings

    def get_schedule(self, date_in: datetime.date = None) -> NHLSchedule:
        print("self.get_schedule")
        # df_standings keys:
        # ['wildCardIndicator', 'df_standings']
        if date_in is None:
            date_in = datetime.date.today()
        url = f"{NHL_API_URL}v1/schedule/{date_in:%Y-%m-%d}"
        max_t = self.max_secs_get_schedule
        schedule = NHLSchedule(self.query(url, hold_time_secs=max_t))
        for game_week in schedule.game_week:
            assert isinstance(game_week,
                              NHLGameDate), f"game_week must be an instance of NHLBoxScore, got '{type(game_week)}'"
            for game_box_score in game_week.games:
                df_games = self.df_games_boxscore.loc[self.df_games_boxscore["g_id"] == game_box_score.g_id]
                if df_games.empty:
                    self.df_games_boxscore = pd.concat([
                        self.df_games_boxscore,
                        pd.DataFrame([game_box_score.to_df_row()])
                    ], ignore_index=True)
                else:
                    # st.write("df_games")
                    # st.write(df_games)
                    # st.write("df_games.index")
                    # st.write(df_games.index)
                    # st.write("self.df_games_boxscore")
                    # st.write(self.df_games_boxscore)
                    # st.write("game_box_score.to_df_row()")
                    # st.write(game_box_score.to_df_row())
                    self.df_games_boxscore.loc[
                        self.df_games_boxscore["g_id"] == game_box_score.g_id] = game_box_score.to_df_row().values()
        return schedule

    # def get_season_dates(self, date_in: datetime.date) -> tuple[Any, Any]:

    def get_season(self, date_in: datetime.date = None) -> NHLSeason | None:
        if date_in is None:
            date_in = datetime.datetime.now().date()
        df_season = self.df_seasons.loc[
            (self.df_seasons["standingsStart"] <= date_in)
            & (date_in <= self.df_seasons["playoffsEnd"])
            ]
        if not df_season.empty:
            ser_season = df_season.iloc[0]
            season = NHLSeason(ser_season)
            season.df_season = df_season.copy()
            return season
        return None

    def standings_by_day(self, dates):
        teams_data = []
        # for i, date in enumerate(dates):
        #     if date <= datetime.date.today():
        #         df_standings: pd.DataFrame = self.get_standings(date).df_standings
        #         if i == 0:
        #             teams_data.append({})
        #         "team_name": df_standings["team_name"].iloc[0],
        return teams_data

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

    def lookup_team(self, team_id) -> NHLTeam:
        if self.df_teams.empty:
            self.get_team_data()
        df_t = self.df_teams
        # st.write(f"df_t, {team_id=}")
        # st.write(df_t)
        df_same_t: pd.DataFrame = df_t.loc[
            (df_t["id"].astype(str).str.lower() == str(team_id).lower())
            | (df_t["fullName"].astype(str).str.lower() == str(team_id).lower())
            | (df_t["rawTricode"].astype(str).str.lower() == str(team_id).lower())
            | (df_t["triCode"].astype(str).str.lower() == str(team_id).lower())
            ]

        if df_same_t.empty:
            return None

        team: NHLTeam = NHLTeam(dict(df_same_t.iloc[0]))
        return team

    def load_game_boxscore(self, game_id: int) -> NHLBoxScore:
        # return requests.get(f"https://statsapi.web.nhl.com/api/v1/game/{game_id}/boxscore").json()
        print(f"New Game Boxscore {game_id=}, {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        url: str = "{0}v1/gamecenter/{1}/boxscore".format(NHL_API_URL, game_id)
        max_t: int = self.max_secs_get_game_box_score
        data = self.query(url, max_t)
        boxscore: NHLBoxScore = NHLBoxScore(data)
        boxscore.away_team = self.lookup_team(boxscore.away_team_id)
        boxscore.home_team = self.lookup_team(boxscore.home_team_id)
        df_standings_all: NHLStandings = self.get_standings()
        df_standings_all: pd.DataFrame = df_standings_all.df_standings.rename(columns=df_standings_all.show_cols())

        g_id: int = boxscore.g_id
        g_data = boxscore.bx_data

        self.df_games_boxscore = self.df_games_boxscore.loc[
            self.df_games_boxscore["g_id"] != g_id
            ]

        self.df_games_boxscore = pd.concat([
            self.df_games_boxscore,
            pd.DataFrame([boxscore.to_df_row()])
        ])

        return boxscore

        # for date, g_datas in scoreboard.game_dates.items():
        #     for g_data in g_datas:
        #         g_id: int = g_data.g_id
        #
        #         self.df_games_scoreboard = self.df_games_scoreboard.loc[
        #             self.df_games_scoreboard["g_id"] != g_id
        #             ]
        #
        #         self.df_games_scoreboard = pd.concat([
        #             self.df_games_scoreboard,
        #             pd.DataFrame([g_data.to_df_row()])
        #         ])
        #
        # return data

    def load_game_landing(self, game_id: int) -> dict[str: Any]:
        print(f"New Game Landing {game_id=}, {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        url: str = "{0}v1/gamecenter/{1}/landing".format(NHL_API_URL, game_id)
        data = self.query(url, self.max_secs_get_game_landing)
        # st.write(data)
        gl = NHLGameLanding(data)
        if self.df_games_landing.empty:
            self.df_games_landing = pd.DataFrame(gl.to_df_row(), index=[0])
        else:
            g_id = gl.g_id
            df_already_exists = self.df_games_landing.loc[self.df_games_landing["g_id"] == g_id]
            if df_already_exists.empty:
                self.df_games_landing = pd.concat([
                    self.df_games_landing,
                    pd.DataFrame(gl.to_df_row(), index=[0])
                ])
        return gl

    def load_scoreboard(self, date_str: Optional[str] = None):
        print(f"New Scoreboard data")
        if date_str is None:
            url = "{0}v1/scoreboard/now".format(NHL_API_URL)
        else:
            url = "{0}v1/score/{1}".format(NHL_API_URL, date_str)

        data = self.query(url)
        scoreboard: NHLScoreboard = NHLScoreboard(data)
        df_standings_all: NHLStandings = self.get_standings()
        df_standings_all: pd.DataFrame = df_standings_all.df_standings.rename(columns=df_standings_all.show_cols())

        for date, g_datas in scoreboard.game_dates.items():
            for g_data in g_datas:
                assert isinstance(g_data, NHLGame)
                # st.write(f"{date=}, {len(g_datas)=}, {g_data=}")
                # st.write(f"{date=}, {len(g_datas)=}, g_data.g_data:")
                # st.write(g_data.g_data)
                g_data.home_team = self.lookup_team(g_data.home_team_id)
                g_data.away_team = self.lookup_team(g_data.away_team_id)

                if g_data.home_team is None:
                    g_data.home_team = NHLTeam(g_data.home_team_data)

                if g_data.away_team is None:
                    g_data.away_team = NHLTeam(g_data.away_team_data)

                g_data.away_team.url_logo = g_data.away_team_logo
                g_data.home_team.url_logo = g_data.home_team_logo

                # print("--- df_standings")
                # print(df_standings_all)
                # ser_away: pd.Series = df_standings_all.loc[df_standings_all["t_id"] == g_data.away_team_id].iloc[0]
                df_away: pd.DataFrame = df_standings_all.loc[df_standings_all["t_id"] == g_data.away_team_id]
                if not df_away.empty:
                    ser_away: pd.Series = df_away.iloc[0]
                    record_away = f_standing_record(
                        ser_away[NHLStandings.Abbr.W.value],
                        ser_away[NHLStandings.Abbr.L.value],
                        ser_away[NHLStandings.Abbr.OTL.value] + ser_away[NHLStandings.Abbr.SOL.value]
                    )
                else:
                    record_away = None
                # ser_home: pd.Series = df_standings_all.loc[df_standings_all["t_id"] == g_data.home_team_id].iloc[0]
                df_home: pd.DataFrame = df_standings_all.loc[df_standings_all["t_id"] == g_data.home_team_id]
                if not df_home.empty:
                    ser_home: pd.Series = df_home.iloc[0]
                    record_home = f_standing_record(
                        ser_home[NHLStandings.Abbr.W.value],
                        ser_home[NHLStandings.Abbr.L.value],
                        ser_home[NHLStandings.Abbr.OTL.value] + ser_home[NHLStandings.Abbr.SOL.value]
                    )
                else:
                    record_home = None
                g_data.away_team.record = record_away
                g_data.home_team.record = record_home

                g_id: int = g_data.g_id

                self.df_games_scoreboard = self.df_games_scoreboard.loc[
                    self.df_games_scoreboard["g_id"] != g_id
                    ]

                self.df_games_scoreboard = pd.concat([
                    self.df_games_scoreboard,
                    pd.DataFrame([g_data.to_df_row()])
                ])

                if g_id not in self.games:
                    self.games[g_id] = {
                        "scoreboard": g_data,
                        "boxscore": None
                    }

        return scoreboard

    def check_game_status(self, team_id, date):
        """ Function to check if there is a game now with chosen team. Returns True if game, False if NO game. """
        # Set URL depending on team selected and date
        url = '{0}schedule?teamId={1}&date={2}'.format(NHL_API_URL, team_id, date)
        # st.write(url)
        # st.link_button(
        #     label="URL",
        #     url=url,
        # )
        data = self.query(url)
        return data

        # try:
        #     #get game state from API (no state when no games on date)
        #     game_status = requests.get(url).json()
        #     game_status = game_status['dates'][0]['games'][0]['status']['detailedState']
        #     return game_status
        #
        # except IndexError:
        #     #Return No Game when no state available on API since no game
        #     return 'No Game'
        #
        # except requests.exceptions.RequestException:
        #     # Return No Game to keep going
        #     return 'No Game'
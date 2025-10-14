import enum
import os.path
import random

import pandas as pd
import streamlit
from decorator import append
from streamlit_pills import pills

from streamlit_utility import *

import numpy as np
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
PATH_FOLDER_JERSEY_COLLECTION: str = r"D:\NHL jerseys\Jerseys 20250927"

UTC_FMT: str = "%Y-%m-%dT%H:%M:%SZ"


def utc_offset_to_seconds(offset_str: str) -> float:
    spl = offset_str.split(":")
    hours = int(spl[0])
    mins = int(spl[1])
    return (hours * 60 * 60) + (mins + 60)


def get_this_season() -> str:
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    if month < 7 or 8 < month:
        return f"{year}{year+1}"
    else:
        return "off"


def f_season(season_str) -> str:
    ss = str(season_str)
    return f"{ss[:4]}-{ss[-4:]}"


def f_standing_record(w, l, so_otl) -> str:
    return f"{w}-{l}-{so_otl}"


def game_state_translate(game_state: str) -> str:
    match game_state:
        case "FUT":
            return "Upcoming"
        case "OFF":
            return "Final"
        case _:
            return game_state


class Jersey:
    def __init__(self, j_data: dict | pd.Series):
        self.j_data: dict = j_data if isinstance(j_data, dict) else j_data.to_dict()
        self.j_id: int = j_data["ID"]
        self.image_folder: str = os.path.join(PATH_FOLDER_JERSEY_COLLECTION, f"J_{('000' + str(self.j_id))[-3:]}")
        if not os.path.exists(self.image_folder):
            self.image_folder = ""
            self.n_images: int = 0
        else:
            self.n_images: int = len(os.listdir(self.image_folder))

        self.cancelled: bool = j_data.get("Cancelled", False)
        self.league: str = j_data.get("League", "NHL")
        self.team: str = j_data.get("Team")
        self.tournament: str = j_data.get("Tournament")
        self.conference: str = j_data.get("Conference")
        self.division: str = j_data.get("Division")
        self.c_patch: bool = j_data.get("CPatch")
        self.a_patch: bool = j_data.get("APatch")
        self.number: int = None if pd.isna(j_data.get("Number")) else int(j_data.get("Number"))
        self.player_first: str = None if pd.isna(j_data.get("PlayerFirst")) else j_data.get("PlayerFirst")
        self.player_last: str = None if pd.isna(j_data.get("PlayerLast")) else j_data.get("PlayerLast")
        self.colour_1: str = j_data.get("Colour_1")
        self.colour_2: str = j_data.get("Colour_2")
        self.colour_3: str = j_data.get("Colour_3")
        self.order_date: datetime.date = j_data.get("OrderDate")
        self.receive_date: datetime.date = j_data.get("ReceiveDate")
        self.open_date: datetime.date = j_data.get("OpenDate")
        self.manufacture_date: str = j_data.get("ManufactureDate")
        self.brand: str = None if pd.isna(j_data.get("Brand")) else j_data.get("Brand")
        self.make: str = None if pd.isna(j_data.get("Make")) else j_data.get("Make")
        self.model: str = None if pd.isna(j_data.get("Model")) else j_data.get("Model")
        self.size: str = j_data.get("Size")
        self.supplier: str = j_data.get("Supplier")
        self.us_sale: bool = j_data.get("USSale", False)
        self.exchange_rate: float = j_data.get("ExchangeRate")
        self.sticker_price_cdn: float = j_data.get("StickerPriceCDN")
        self.sticker_price_us: float = j_data.get("USStickerPriceUS")
        self.duty: float = j_data.get("Duty")
        self.shipping: float = j_data.get("Shipping")
        self.discount: float = j_data.get("Discount")
        self.discount_reason: str = j_data.get("DiscountReason")
        self.tax: float = j_data.get("Tax")
        self.price_c: float = j_data.get("PriceC")
        self.price_m: float = j_data.get("PriceM")
        self.nhl_id: str = j_data.get("NHLID")
        self.position: str = j_data.get("Position")
        self.nationality: str = j_data.get("Nationality")
        self.dob: datetime.date = j_data.get("DOB")
        self.retire_date: str = j_data.get("RetireDate")
        self.first_season: str = j_data.get("FirstSeason")
        self.last_season: str = j_data.get("LastSeason")
        self.nhl_uniform_link: str = j_data.get("NHLUniformLink")
        self.notes: str = j_data.get("Notes")

    def is_blank(self) -> bool:
        return (self.number is None) and (self.player_last is None)

    def to_string(
            self,
            inc_team: bool = None,
            inc_brand: bool = None,
            inc_make: bool = None,
            inc_model: bool = None,
            inc_num: bool = None,
            inc_fname: bool = None,
            inc_lname: bool = None,
            inc_size: bool = None
    ) -> str:
        res = []
        if inc_team is None:
            inc_team = True
        if inc_brand is None:
            inc_brand = True
        if inc_make is None:
            inc_make = True
        if inc_model is None:
            inc_model = True

        if inc_num is None:
            inc_num = not self.is_blank()
        if inc_fname is None:
            inc_fname = not self.is_blank()
        if inc_lname is None:
            inc_lname = not self.is_blank()

        if inc_size is None:
            inc_size = True

        if inc_team and bool(self.team):
            res.append(self.team)
        if inc_brand and bool(self.brand):
            res.append(self.brand)
        if inc_make and bool(self.make):
            res.append(self.make)
        if inc_model and bool(self.model):
            res.append(self.model)
        if inc_num and bool(self.number):
            res.append(f"#{self.number}")
        if inc_fname and bool(self.player_first):
            res.append(self.player_first)
        if inc_lname and bool(self.player_last):
            res.append(self.player_last)
        if inc_size and bool(self.size):
            res.append(self.size)
        return " ".join(map(str, res))


class NHLJersey(Jersey):
    def __init__(self, j_data: dict | pd.Series):
        super().__init__(j_data)


class NHLGame:

    def __init__(self, g_data: dict | pd.Series):
        self.g_data: dict = g_data if isinstance(g_data, dict) else g_data.to_dict()
        self.g_id: int = g_data.get("id")
        self.season: str = g_data.get("season")
        self.game_type: str = g_data.get("gameType")
        self.game_date: str = g_data.get("gameDate")
        self.game_center_link: str = g_data.get("gameCenterLink")
        self.venue: str = g_data.get("venue", {}).get("default")
        self.start_time_utc: datetime.datetime = datetime.datetime.strptime(g_data.get("startTimeUTC"), UTC_FMT)
        self.game_eastern_utc_offset: str = g_data.get("easternUTCOffset", "00:00")
        self.game_eastern_utc_offset_sec: datetime.timedelta = datetime.timedelta(seconds=utc_offset_to_seconds(self.game_eastern_utc_offset))
        self.start_time_atl: datetime.datetime = self.start_time_utc + self.game_eastern_utc_offset_sec + datetime.timedelta(hours=1)
        self.game_venue_utc_offset: str = g_data.get("venueUTCOffset")
        self.game_tv_broadcasts: list[dict[str: Any]] = g_data.get("tvBroadcasts")

        self.game_state: str = g_data.get("gameState")
        self.game_schedule_state: str = g_data.get("gameScheduleState")

        self.away_team: NHLTeam = None
        self.away_team_id: int = g_data.get("awayTeam", {}).get("id")
        self.away_team_name_full: str = g_data.get("awayTeam", {}).get("name", {}).get("default")
        self.away_team_name_fr: str = g_data.get("awayTeam", {}).get("name", {}).get("fr")
        self.away_team_name_short: str = g_data.get("awayTeam", {}).get("commonName", {}).get("default")
        self.away_team_place_name_prep: str = g_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get("default")
        self.away_team_place_name_prep_fr: str = g_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get("fr")
        self.away_team_name_abbrev: str = g_data.get("awayTeam", {}).get("abbrev")
        self.away_team_score: int = g_data.get("awayTeam", {}).get("score", 0)
        self.away_team_logo: str = g_data.get("awayTeam", {}).get("logo")

        self.home_team: NHLTeam = None
        self.home_team_id: int = g_data.get("homeTeam", {}).get("id")
        self.home_team_name_full: str = g_data.get("homeTeam", {}).get("name", {}).get("default")
        self.home_team_name_fr: str = g_data.get("homeTeam", {}).get("name", {}).get("fr")
        self.home_team_name_short: str = g_data.get("homeTeam", {}).get("commonName", {}).get("default")
        self.home_team_place_name_prep: str = g_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get("default")
        self.home_team_place_name_prep_fr: str = g_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get("fr")
        self.home_team_name_abbrev: str = g_data.get("homeTeam", {}).get("abbrev")
        self.home_team_score: int = g_data.get("homeTeam", {}).get("score", 0)
        self.home_team_logo: str = g_data.get("homeTeam", {}).get("logo")

        self.game_tickets_link: str = g_data.get("ticketsLink")
        self.game_tickets_link_fr: str = g_data.get("ticketsLinkFr")
        self.game_period: int = g_data.get("period", 1)
        self.game_period_desc_number: int = g_data.get("periodDescriptor", {}).get("number", 1)
        self.game_period_desc_type: str = g_data.get("periodDescriptor", {}).get("periodType")
        self.game_period_desc_max_reg_periods: int = g_data.get("periodDescriptor", {}).get("maxRegulationPeriods", 3)
        self.game_three_min_recap: str = g_data.get("threeMinRecap")
        self.game_three_min_recap_fr: str = g_data.get("threeMinRecapFr")

        self.show_game: bool = g_data.get("showGame", False)

    def is_over(self):
        return self.game_state == "OFF"

    def is_future(self):
        return self.game_state == "FUT"

    def start_date(self) -> datetime.datetime:
        return self.start_time_utc + self.game_eastern_utc_offset

    def to_df_row(self) -> dict:
        res = {k: v for k, v in self.__dict__.items() if not isinstance(v, (list, tuple, dict))}
        res["str"] = str(self)
        return res

    def st_scoreboard_card(self):
        bg: Colour = Colour("#CACACA")
        fg: Colour = Colour("#000000")
        left_to_right = True
        jc = "flex-start" if left_to_right else "flex-end"
        card_away: str = self.away_team.st_card(show_record=self.show_game)
        card_home: str = self.home_team.st_card(show_record=self.show_game)
        card_away_f = f"<div>"
        card_away_f += card_away
        card_away_f += "</div>"
        card_home_f = f"<div>"
        card_home_f += card_home
        card_home_f += "</div>"
        html = f"""<div class='card_scoreboard_{self.g_id}', style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"""
        html += card_away_f
        html += "<h4>@</h4>"
        html += card_home_f

        game_state_fmt: str = game_state_translate(self.game_state)
        html += f"<h5>{game_state_fmt}<h5>"

        html += "</div>"
        return html

    def st_boxscore_card(self):
        bg: Colour = Colour("#CACACA")
        fg: Colour = Colour("#000000")
        left_to_right = True
        jc = "flex-start" if left_to_right else "flex-end"
        card_away: str = self.away_team.st_card()
        card_home: str = self.home_team.st_card()
        card_away_f = f"<div>"
        card_away_f += card_away
        card_away_f += "</div>"
        card_home_f = f"<div>"
        card_home_f += card_home
        card_home_f += "</div>"
        html = f"""<div class='card_scoreboard_{self.g_id}', style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"""
        html += card_away_f
        html += "<h4>@</h4>"
        html += card_home_f

        game_state_fmt: str = game_state_translate(self.game_state)
        html += f"<h5>{game_state_fmt}<h5>"
        # if self.show_game and (game_state_fmt != game_state_translate("FUT")):
        #     if game_state_fmt != "FINAL":
        #         # game_state_fmt += f" {seconds_to_clock(bs_game_clock_seconds_remaining)}"
        #         if bs_game_clock_running:
        #             game_state_fmt += f" {E_html_STOPPAGE}"
        #         else:
        #             game_state_fmt += f" {E_html_PLAYING}"
        #         game_state_fmt += f" {bs_game_clock_time_remaining}"
        #         game_state_fmt += f" {bs_game_period_num}{number_suffix(bs_game_period_num)}"
        #         if bs_game_clock_in_intermission:
        #             game_state_fmt += f" intermission"
        #         else:
        #             game_state_fmt += f" period"
        #     else:
        #         game_state_fmt += f" - {bs_game_period_type}"
        #     #     game_state_fmt += f" {E_strl_RUNNING}"
        # elif game_state_fmt == game_state_translate("FUT"):
        #     starts_in_h, starts_in_m = divmod((game_start_time_atl - now).total_seconds(), 3600)
        #     a__, b__ = starts_in_h, starts_in_m
        #     starts_in_h = int(round(starts_in_h, 0))
        #     starts_in_m = int(round(starts_in_m / 60, 0))
        #     # game_state_fmt += f" {game_start_time_atl=} {now=}, {game_start_time_atl.tzinfo=} {now.tzinfo=}, {starts_in_h=}, {starts_in_m=}, {a__=}, {b__=}"
        #     # game_state_fmt += f" {game_start_time_atl:%Y-%m-%d %H:%M} -- "
        #     if starts_in_h:
        #         game_state_fmt += f" -- {starts_in_h} hour{'' if starts_in_h == 1 else 's'},"
        #     else:
        #         game_state_fmt += f" --"
        #     game_state_fmt += f" {starts_in_m} minute{'' if starts_in_m == 1 else 's'}"

        html += "</div>"
        return html

    def __repr__(self):
        return f"NHLGAME#{self.g_id} {self.start_time_utc:{UTC_FMT}} {self.away_team} @ {self.home_team}"


class NHLBoxScore:
    def __init__(self, bx_data: dict | pd.Series):
        self.bx_data: dict = bx_data if isinstance(bx_data, dict) else bx_data.to_dict()
        self.g_id: int = self.bx_data.get("id")
        self.game_season: int = self.bx_data.get("season")
        self.game_type: int = self.bx_data.get("gameType")
        self.game_limited_scoring: bool = self.bx_data.get("limitedScoring")
        self.game_date: int = self.bx_data.get("gameDate")
        self.game_venue: str = self.bx_data.get("venue", {}).get("default")
        self.game_venue_fr: str = self.bx_data.get("venue", {}).get("fr")
        self.game_venue_location: str = self.bx_data.get("venueLocation", {}).get("default")
        self.game_venue_location_fr: str = self.bx_data.get("venueLocation", {}).get("fr")
        self.game_start_time_utc: datetime.datetime = datetime.datetime.strptime(self.bx_data.get("startTimeUTC"), UTC_FMT)
        self.game_eastern_utc_offset: str = self.bx_data.get("easternUTCOffset")
        self.game_eastern_utc_offset_sec: datetime.timedelta = datetime.timedelta(seconds=utc_offset_to_seconds(self.game_eastern_utc_offset))
        self.start_time_atl: datetime.datetime = self.game_start_time_utc + self.game_eastern_utc_offset_sec + datetime.timedelta(hours=1)
        self.game_venue_utc_offset: int = self.bx_data.get("venueUTCOffset")
        self.game_broadcasts: list[dict[str: Any]] = self.bx_data.get("tvBroadcasts", [])

        self.game_away_team: dict[str: Any] = self.bx_data.get("awayTeam", {})
        self.game_away_team_id: int = self.game_away_team.get("id")
        self.game_away_team_score: int = self.game_away_team.get("score", 0)
        self.game_away_team_name: str = self.game_away_team.get("name", {}).get("default")
        self.game_away_team_name_fr: str = self.game_away_team.get("name", {}).get("fr")
        self.game_away_team_abbrev: str = self.game_away_team.get("abbrev")
        self.game_away_team_logo: str = self.game_away_team.get("logo")
        self.game_away_team_dark_logo: str = self.game_away_team.get("darkLogo")
        self.game_away_team_place_name: str = self.game_away_team.get("placeName", {}).get("default")
        self.game_away_team_place_name_fr: str = self.game_away_team.get("placeName", {}).get("fr")
        self.game_away_team_place_name_prep: str = self.game_away_team.get("placeNameWithPreposition", {}).get("default")
        self.game_away_team_place_name_prep_fr: str = self.game_away_team.get("placeNameWithPreposition", {}).get("fr")

        self.game_home_team: dict[str: Any] = self.bx_data.get("homeTeam", {})
        self.game_home_team_id: int = self.game_home_team.get("id")
        self.game_home_team_score: int = self.game_home_team.get("score", 0)
        self.game_home_team_name: str = self.game_home_team.get("name", {}).get("default")
        self.game_home_team_name_fr: str = self.game_home_team.get("name", {}).get("fr")
        self.game_home_team_abbrev: str = self.game_home_team.get("abbrev")
        self.game_home_team_logo: str = self.game_home_team.get("logo")
        self.game_home_team_dark_logo: str = self.game_home_team.get("darkLogo")
        self.game_home_team_place_name: str = self.game_home_team.get("placeName", {}).get("default")
        self.game_home_team_place_name_fr: str = self.game_home_team.get("placeName", {}).get("fr")
        self.game_home_team_place_name_prep: str = self.game_home_team.get("placeNameWithPreposition", {}).get("default")
        self.game_home_team_place_name_prep_fr: str = self.game_home_team.get("placeNameWithPreposition", {}).get("fr")

        self.game_clock: dict[str: Any] = self.bx_data.get("clock", {})
        self.game_clock_time_remaining: str = self.game_clock.get("timeRemaining")
        self.game_clock_seconds_remaining: int = int(self.game_clock.get("secondsRemaining"))
        self.game_clock_running: str = self.game_clock.get("running")
        self.game_clock_in_intermission: str = self.game_clock.get("inIntermission")
        self.game_period_num: int = self.bx_data.get("periodDescriptor", {}).get("number", 1)
        self.game_period_type: int = self.bx_data.get("periodDescriptor", {}).get("periodType", 1)

        self.game_state: str = self.bx_data.get("gameState")
        self.game_schedule_state: str = self.bx_data.get("gameScheduleState")
        self.game_reg_periods: int = self.bx_data.get("regPeriods")

    def to_df_row(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if type(v) not in (list, tuple, dict, pd.DataFrame)}


class NHLScoreboard:
    def __init__(self, sc_data: dict | pd.Series):
        print("NHLScoreboard")
        self.sc_data: dict = sc_data if isinstance(sc_data, dict) else sc_data.to_dict()
        self.focusedDate: datetime.date = self.sc_data.get("focusedDate")
        self.focusedDateCount: int = sc_data.get("focusedDateCount", 0)
        self.game_dates: dict[datetime.date: list[NHLGame]] = {}
        for date_g_data in self.sc_data.get("gamesByDate", []):
            date = date_g_data.get("date")
            for g_data in date_g_data.get("games", []):
                if date not in self.game_dates:
                    self.game_dates[date] = []
                # for data in g_data:
                #     print(f"{date=}, {data=}")
                self.game_dates[date].append(NHLGame(g_data))


class NHLJerseyCollection:
    def __init__(self, excel_path: str):
        self.df_jc_data: pd.DataFrame = pd.read_excel(excel_path)

        date_cols = [
            "OrderDate",
            "ReceiveDate",
            "OpenDate",
            "DOB"
        ]
        for col in date_cols:
            self.df_jc_data[col] = pd.to_datetime(self.df_jc_data[col])

        self.df_jerseys: pd.DataFrame = self.df_jc_data.loc[
            ~self.df_jc_data["Cancelled"]
        ]
        self.df_cancelled_jerseys: pd.DataFrame = self.df_jc_data.loc[
            self.df_jc_data["Cancelled"]
        ]

        self.first_date: datetime.date = self.df_jerseys["OrderDate"].min().date()
        self.last_date: datetime.date = self.df_jerseys["OrderDate"].max().date()

        self.jerseys: dict[int: Jersey] = {}
        for i, row in self.df_jerseys.iterrows():
            j_id = row["ID"]
            league: str = row["League"]
            is_nhl: bool = league == "NHL"
            if is_nhl:
                self.jerseys[j_id] = NHLJersey(row)
            else:
                self.jerseys[j_id] = Jersey(row)

    def __repr__(self):
        return f"NHLJerseyCollection: {self.df_jerseys.shape[0]} jerseys between {self.first_date} and {self.last_date}"


class NHLStandings:

    class Abbr(enum.Enum):
        GP: str = "GP"        # games played
        GD: str = "GD"        # goal differential
        GA: str = "GA"        # goals against
        GF: str = "GF"        # goals for
        L: str = "L"          # losses
        W: str = "W"          # wins
        SOL: str = "SOL"      # shootout losses
        OTL: str = "OTL"      # overtime losses
        WPCTG: str = "W%"     # overtime losses
        STRKC: str = "STRKC"  # streak indicator
        STRKN: str = "STRKN"  # streak indicator count
        PTS: str = "PTS"      # points
        LURL: str = "LURL"    # team logo url

    def __init__(self, s_data):
        print("NHLStandings")
        self.s_data = s_data

        self.wild_card_indicator = s_data.get("wild_card_indicator")
        self.standings_datetime_utc = s_data.get("standingsDateTimeUtc")

        self.df_standings: pd.DataFrame = pd.DataFrame(s_data.get("standings", []))
        self.df_standings["team_name"] = ""
        self.df_standings["t_id"] = None
        for i, row in self.df_standings.iterrows():
            self.df_standings.loc[i, "team_name"] = row.get("teamName", {}).get("default")

    def show_cols(self, mode: int = None) -> dict[str: str]:
        cols = {
            "teamLogo": NHLStandings.Abbr.LURL.value,
            "gamesPlayed": NHLStandings.Abbr.GP.value,
            "points": NHLStandings.Abbr.PTS.value,
            "wins": NHLStandings.Abbr.W.value,
            "losses": NHLStandings.Abbr.L.value,
            "otLosses": NHLStandings.Abbr.OTL.value,
            "shootoutLosses": NHLStandings.Abbr.SOL.value,
            "winPctg": NHLStandings.Abbr.WPCTG.value,
            "goalFor": NHLStandings.Abbr.GF.value,
            "goalAgainst": NHLStandings.Abbr.GA.value,
            "goalDifferential": NHLStandings.Abbr.GD.value,
            "streakCode": NHLStandings.Abbr.STRKC.value,
            "streakCount": NHLStandings.Abbr.STRKN.value
        }
        return cols


class NHLTeam:

    def __init__(self, t_data):

        self.t_data = t_data
        self.t_id: str = t_data["id"]
        self.franchise_id: str = t_data["franchiseId"]
        self.league_id: str = t_data["leagueId"]
        self.full_name: str = t_data.get("fullName")
        self.raw_tri_code: str = t_data.get("rawTriCode")
        self.tri_code: str = t_data.get("triCode")
        self.url_logo: str = None
        self.record: str = None

    def st_card(
            self,
            show_record: bool = True,
            logo_width: int = 75,
            bg: Colour = Colour("#676767"),
            fg: Colour = Colour("#000000")
    ) -> str:
        html = f"<div class='card_team_{self.t_id}, style='background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"
        html += f"<img src='{self.url_logo}', width='{logo_width}'>"
        if show_record:
            html += f"<h6>{self.record}</h6>"
        html += "</div>"
        return html

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
        print("NHLAPIHandler")
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

        self.games: dict[int: dict[str: NHLGame]] = {}
        self.df_games_boxscore: pd.DataFrame = pd.DataFrame(columns=["g_id"])
        self.df_games_scoreboard: pd.DataFrame = pd.DataFrame(columns=["g_id"])
        self.df_teams: pd.DataFrame = pd.DataFrame(columns=["t_id"])
        self.df_glossary: pd.DataFrame = pd.DataFrame()
        self.df_countries: pd.DataFrame = pd.DataFrame(columns=["c_id"])
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

    def get_country_data(self) -> pd.DataFrame:
        url = "{0}country".format(NHL_STATS_API_URL)
        max_t = self.max_secs_get_country
        results = self.query(url, max_t)
        self.df_countries = pd.DataFrame(results.get("data", []))
        return self.df_countries.copy()

    def get_team_roster(self, team_tri_code, season=None) -> pd.DataFrame:
        if season is None:
            season = get_this_season()
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
        print("self.get_standings")
        # df_standings keys:
        # ['wildCardIndicator', 'df_standings']
        if date is None:
            date = datetime.date.today()
        url = f"{NHL_API_URL}v1/standings/{date:%Y-%m-%d}"
        standings = NHLStandings(self.query(url))
        st.write(standings.s_data)
        for i, row in self.df_teams.iterrows():
            f_name = row.get("fullName", "").lower()
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

    def lookup_team(self, team_id) -> NHLTeam:
        if self.df_teams.empty:
            self.get_country_data()
        df_t = self.df_teams
        df_same_t: pd.DataFrame = df_t.loc[
            (df_t["id"].astype(str).str.lower() == str(team_id).lower())
            | (df_t["fullName"].astype(str).str.lower() == str(team_id).lower())
            | (df_t["rawTricode"].astype(str).str.lower() == str(team_id).lower())
            | (df_t["triCode"].astype(str).str.lower() == str(team_id).lower())
        ]

        if df_same_t.empty:
            return team_id

        team: NHLTeam = NHLTeam(dict(df_same_t.iloc[0]))
        return team

    def load_game_boxscore(self, game_id: int) -> dict[str: Any]:
        # return requests.get(f"https://statsapi.web.nhl.com/api/v1/game/{game_id}/boxscore").json()
        print(f"New Game Boxscore {game_id=}, {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        url: str = "{0}v1/gamecenter/{1}/boxscore".format(NHL_API_URL, game_id)
        data = self.query(url)
        boxscore: NHLBoxScore = NHLBoxScore(data)
        df_standings_all: NHLStandings = self.get_standings()
        df_standings_all: pd.DataFrame = df_standings_all.df_standings.rename(columns=df_standings_all.show_cols())

        g_id: int = boxscore.g_id
        g_data = boxscore.bx_data

        self.df_games_boxscore = self.df_games_boxscore.loc[
            self.df_games_boxscore["g_id"] != g_id
        ]

        self.df_games_boxscore = pd.concat([
            self.df_games_boxscore,
            pd.DataFrame([g_data.to_df_row()])
        ])

        return data

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
        data = self.query(url)
        return data

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
                g_data.home_team = self.lookup_team(g_data.home_team_id)
                g_data.away_team = self.lookup_team(g_data.away_team_id)

                g_data.away_team.url_logo = g_data.away_team_logo
                g_data.home_team.url_logo = g_data.home_team_logo

                # print(f"{date=}, {len(g_datas)=}, {g_data=}")
                # print("--- df_standings")
                # print(df_standings_all)
                ser_away: pd.Series = df_standings_all.loc[df_standings_all["t_id"] == g_data.away_team_id].iloc[0]
                record_away = f_standing_record(
                    ser_away[NHLStandings.Abbr.W.value],
                    ser_away[NHLStandings.Abbr.L.value],
                    ser_away[NHLStandings.Abbr.OTL.value] + ser_away[NHLStandings.Abbr.SOL.value]
                )
                ser_home: pd.Series = df_standings_all.loc[df_standings_all["t_id"] == g_data.home_team_id].iloc[0]
                record_home = f_standing_record(
                    ser_home[NHLStandings.Abbr.W.value],
                    ser_home[NHLStandings.Abbr.L.value],
                    ser_home[NHLStandings.Abbr.OTL.value] + ser_home[NHLStandings.Abbr.SOL.value]
                )
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
        url = '{0}schedule?teamId={1}&date={2}'.format(NHL_API_URL, team_id,date)
        st.write(url)
        st.link_button(
            label="URL",
            url=url,
        )
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


st.set_page_config(layout="wide")

k_nhl_jersey_collection: str = "key_nhl_jersey_collection"
path_jersey_collection_data: str = r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\Jerseys_20251011.xlsx"
if k_nhl_jersey_collection not in st.session_state:
    st.session_state[k_nhl_jersey_collection] = NHLJerseyCollection(path_jersey_collection_data)
nhl_jc: NHLJerseyCollection = st.session_state[k_nhl_jersey_collection]

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
    f"{pl_team.full_name} {f_season(get_this_season())} Team Roster"
)

st.write(nhl.get_country())
st.write(nhl.get_geolocation())

standings_now = nhl.get_standings()
df_standings_now: pd.DataFrame = standings_now.df_standings

df_standings_now = df_standings_now.merge(
    nhl.df_teams,
    left_on="t_id",
    right_on="id",
    suffixes=["", "_df_teams"]
)

display_df(
    df_standings_now,
    "Standings as of now:"
)

# cols_standings: dict = {
#     "triCode": "Team"
# }
# cols_standings.update(standings_now.show_cols())
cols_standings = standings_now.show_cols()
df_standings_now.rename(columns=cols_standings, inplace=True)
df_standings_now["STRK"] = df_standings_now["STRKC"].astype(str) + df_standings_now["STRKN"].astype(str)
df_standings_now["GPP"] = df_standings_now[NHLStandings.Abbr.GP.value]
df_standings_now["REC"] = df_standings_now.apply(
    lambda row:
        f_standing_record(
            row[NHLStandings.Abbr.W.value],
            row[NHLStandings.Abbr.L.value],
            row[NHLStandings.Abbr.OTL.value] + row[NHLStandings.Abbr.SOL.value]
        ),
    axis=1
)

delta = df_standings_now[NHLStandings.Abbr.GD.value]
symbols = np.where(delta > 0, "▲", np.where(delta < 0, "▼", "—"))
df_standings_now["Δ"] = symbols

df_standings_now_league: pd.DataFrame = df_standings_now.copy()
df_standings_now_west = df_standings_now_league.loc[
    df_standings_now_league["conferenceAbbrev"] == "W"
].sort_values(by="conferenceSequence", ascending=True)
df_standings_now_east = df_standings_now_league.loc[
    df_standings_now_league["conferenceAbbrev"] == "E"
].sort_values(by="conferenceSequence", ascending=True)
df_standings_now_pac = df_standings_now_west.loc[
    df_standings_now_west["divisionAbbrev"] == "P"
].sort_values(by="divisionSequence", ascending=True)
df_standings_now_cen = df_standings_now_west.loc[
    df_standings_now_west["divisionAbbrev"] == "C"
].sort_values(by="divisionSequence", ascending=True)
df_standings_now_atl = df_standings_now_east.loc[
    df_standings_now_east["divisionAbbrev"] == "A"
].sort_values(by="divisionSequence", ascending=True)
df_standings_now_met = df_standings_now_east.loc[
    df_standings_now_east["divisionAbbrev"] == "M"
].sort_values(by="divisionSequence", ascending=True)

cols_standings.update({
    "STRK": "STRK",
    "GPP": "GPP",
    "REC": "REC",
    "Δ": "Δ"
})
cols_standings = {
    k: v
    for k, v in cols_standings.items()
    if v not in (
        "STRKC", "STRKN"
    )
}

options_standings = [
    "League",
    "Conference",
    "Division",
    "Wildcard"
]
k_pills_standings: str = "key_pills_standings"
pills_standings = pills(
    label="Standings",
    key=k_pills_standings,
    options=options_standings
)
standings_heights = {
    1: 1160,
    2: 600,
    4: 315
}

if pills_standings == options_standings[3]:
    # Wildcard
    df_standings_to_show: dict[str: pd.DataFrame] = {"League": df_standings_now_league.copy()}
elif pills_standings == options_standings[2]:
    # Division
    df_standings_to_show: dict[str: pd.DataFrame] = {
        "Atlantic": df_standings_now_atl.copy(),
        "Metropolitan": df_standings_now_met.copy(),
        "Central": df_standings_now_cen.copy(),
        "Pacific": df_standings_now_pac.copy()
    }
elif pills_standings == options_standings[1]:
    # Conference
    df_standings_to_show: dict[str: pd.DataFrame] = {
        "Eastern": df_standings_now_east.copy(),
        "Western": df_standings_now_west.copy()
    }
else:
    df_standings_to_show: dict[str: pd.DataFrame] = {"League": df_standings_now_league.copy()}

k_toggle_horizontal: str = "key_toggle_horizontal"
st.session_state.setdefault(k_toggle_horizontal, True)
toggle_horizontal = st.toggle(
    label="Horizontal?",
    key=k_toggle_horizontal,
)
cols_dfs_to_show = st.columns(len(df_standings_to_show)) if toggle_horizontal else [st.container(border=True) for i in range(len(df_standings_to_show))]
for i, k_df in enumerate(df_standings_to_show):
    df: pd.DataFrame = df_standings_to_show[k_df]
    with cols_dfs_to_show[i]:
        display_df(
            df=df[list(cols_standings.values())],
            title=f"{k_df} Standings as of now:",
            column_config={
                NHLStandings.Abbr.LURL.value: st.column_config.ImageColumn(
                    label="Team",
                    width="small"
                ),
                "GPP": st.column_config.ProgressColumn(
                    label="Season %",
                    min_value=0,
                    max_value=82,
                    width=100
                ),
                "Δ": st.column_config.TextColumn(
                    "Δ",
                    help="▲ up, ▼ down, — no change",
                    width="small"
                )
            },
            height=standings_heights[len(df_standings_to_show)],
        )


st.write(nhl_jc)
lst_jerseys = sorted(list(nhl_jc.jerseys))
k_selectbox_jersey = "key_selectbox_jersey"
st.session_state.setdefault(k_selectbox_jersey, random.choice(lst_jerseys))
selectbox_jersey = st.selectbox(
    label="Select a Jersey:",
    key=k_selectbox_jersey,
    options=lst_jerseys
)

if str(selectbox_jersey):
    sel_jersey: Jersey = nhl_jc.jerseys[selectbox_jersey]
    # streamlit.write(sel_jersey.__dict__)
    # st.write(sel_jersey.is_blank())
    toggle_blank = st.toggle(
        "Blank",
        value=sel_jersey.is_blank(),
        disabled=True
    )
    if sel_jersey.n_images == 0:
        st.info(f"No images found for this jersey.")
    else:
        cols_jersey_images = st.columns(sel_jersey.n_images)
        for i, path in enumerate(os.listdir(sel_jersey.image_folder)):
            with cols_jersey_images[i]:
                st.image(os.path.join(sel_jersey.image_folder, path))


for i, j_id in enumerate(nhl_jc.jerseys):
    j = nhl_jc.jerseys[j_id]
    st.write(f"#{j_id} {j.to_string()}")


# k_selectbox_team: str = "key_selectbox_team"
# selectbox_team = st.selectbox(
#     label="Select a Team:",
#     key=k_selectbox_team,
#     options=nhl.df_teams["triCode"]
# )
# if selectbox_team:
#     ser_team: pd.Series = nhl.df_teams.loc[nhl.df_teams["triCode"] == selectbox_team].iloc[0]
#     t_id = ser_team["id"]
#     sel_team: NHLTeam = nhl.lookup_team(t_id)
#     st.write(sel_team)
#     # cgs = nhl.check_game_status(sel_team.t_id, date=datetime.date.today())
#     st.write(cgs)

scoreboard_now: NHLScoreboard = nhl.load_scoreboard()
boxscore_now = nhl.load_game_boxscore(2025020048)
st.write(boxscore_now)
scoreboard_now_game_dates = scoreboard_now.game_dates
scoreboard_now_games = {}
for date, games in scoreboard_now_game_dates.items():
    for game in games:
        scoreboard_now_games[str(game)] = date
# st.write(scoreboard_now.sc_data)
# st.write("game_dates")
# st.write(scoreboard_now.game_dates)

st.write(nhl.df_games_scoreboard)

k_selectbox_investigate_game: str = "key_selectbox_investigate_game"
selectbox_investigate_game = st.selectbox(
    label="Investigate a game:",
    key=k_selectbox_investigate_game,
    options=list(scoreboard_now_games.keys())
)
if selectbox_investigate_game:
    date = scoreboard_now_games[selectbox_investigate_game]
    st.write(selectbox_investigate_game)
    st.write(date)
    df_game: pd.DataFrame = nhl.df_games_scoreboard.loc[
        nhl.df_games_scoreboard["str"] == selectbox_investigate_game
    ]
    st.write(df_game)


options_pills_scoreboard_dates = list(scoreboard_now.game_dates)
k_pills_scoreboard_dates: str = "key_pills_scoreboard_dates"
st.session_state.setdefault(k_pills_scoreboard_dates, 0)
pills_scoreboard_dates = pills(
    label="Standings by Date:",
    key=k_pills_scoreboard_dates,
    options=options_pills_scoreboard_dates
)
for i, date in enumerate(scoreboard_now.game_dates):
    if date != pills_scoreboard_dates:
        continue
    for j, game in enumerate(scoreboard_now.game_dates[date]):
        st.markdown(game.st_scoreboard_card(), unsafe_allow_html=True)

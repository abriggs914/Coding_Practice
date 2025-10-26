import enum
import os.path
import random

import pandas as pd
import streamlit
from decorator import append
from streamlit.delta_generator import DeltaGenerator
from streamlit_pills import pills
from streamlit_calendar import calendar

from datetime_utility import is_leap_year
from streamlit_utility import *

import numpy as np
import requests
import datetime
from dateutil import tz
import pause
import json
from PIL import Image, ImageDraw
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from collections import Counter
import matplotlib.pyplot as plt

from utility import percent, number_suffix

NHL_ASSET_API_URL: str = "https://assets.nhle.com/"
NHL_STATS_API_URL: str = "https://api.nhle.com/stats/rest/en/"
NHL_URL: str = "https://www.nhl.com/"
NHL_API_URL: str = "https://api-web.nhle.com/"
NHL_API_URL_V1: str = "{0}v1/".format(NHL_API_URL)
NHL_PLAYER_API_URL: str = "{0}player/".format(NHL_API_URL_V1)
PATH_UNKNOWN_IMAGE: str = r"C:\Users\abrig\Documents\Coding_Practice\Resources\Flags\unknown_flag.png"
PATH_FOLDER_JERSEY_COLLECTION: str = r"D:\NHL jerseys\Jerseys 20250927"
PATH_JERSEY_COLLECTION_DATA: str = r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\Jerseys_20251017.xlsx"
JERSEY_COLOUR_SAVE_FILE: str = "new_colours_save.json"

UTC_FMT: str = "%Y-%m-%dT%H:%M:%SZ"
DATE_FMT: str = "%Y-%m-%d"

DEFAULT_SEASON_END_DATE: datetime.date = datetime.date(datetime.datetime.now().year + (1 if 8 < datetime.datetime.now().month else 0), 4, 16)

E_strl_RUNNING: str = f":ice_hockey_stick_and_puck:"
E_strl_STOPWATCH: str = f":stopwatch:"
E_html_STOPPAGE: str = f"&#128721"
E_html_PLAYING: str = f"&#127954"

def utc_offset_to_seconds(offset_str: str) -> float:
    spl = offset_str.split(":")
    hours = int(spl[0])
    mins = int(spl[1])
    return (hours * 60 * 60) + (mins + 60)


def get_this_season_str() -> str:
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


def game_state_translate(game_state: str) -> tuple[str, Colour, Colour]:
    bg = Colour("#525252")
    fg = Colour("#FFFFFF")
    match game_state:
        case "FUT":
            bg = Colour("#52F252")
            fg = Colour("#0823FF")
            return "Upcoming", bg, fg
        case "OFF":
            bg = Colour("#9292F2")
            fg = Colour("#FF0000")
            return "Final", bg, fg
        case _:
            return game_state.title(), bg, fg


def quantize_image_colors(image_array, n_bins=10):
    """Reduce the number of colors via rounding to unify similar tones"""
    return (image_array // (256 // n_bins)) * (256 // n_bins)


def remove_background(image_array, bg_threshold=25):
    """Remove near-black background from pixels"""
    return image_array[
        (image_array[:, 0] > bg_threshold) |
        (image_array[:, 1] > bg_threshold) |
        (image_array[:, 2] > bg_threshold)
    ]


def merge_similar_clusters(cluster_centers, proportions, threshold=20):
    merged = []
    used = set()

    for i, center in enumerate(cluster_centers):
        if i in used:
            continue
        merged_color = center
        merged_prop = proportions[i]
        for j in range(i + 1, len(cluster_centers)):
            if j in used:
                continue
            dist = np.linalg.norm(center - cluster_centers[j])
            if dist < threshold:
                merged_color = (merged_color * merged_prop + cluster_centers[j] * proportions[j]) / (merged_prop + proportions[j])
                merged_prop += proportions[j]
                used.add(j)
        used.add(i)
        merged.append((merged_color, merged_prop))
    return merged


def get_color_at_position(gradient_img: Image.Image, position: float) -> str:
    """Sample the color from a horizontal gradient image at a given relative position (0–1)."""
    width = gradient_img.width
    x = min(int(position * width), width - 1)
    rgb = gradient_img.getpixel((x, 0))
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


# def extract_dominant_colours(image_path, num_colours=3, resize=True):
#     image = Image.open(image_path)
#
#     if resize:
#         image = image.resize((300, 300))  # Speed up processing
#
#     # Convert image to array and reshape
#     image_array = np.array(image)
#     image_array = image_array.reshape((-1, 3))
#
#     # Remove black background or near-black
#     image_array = image_array[(image_array[:, 0] > 20) |
#                               (image_array[:, 1] > 20) |
#                               (image_array[:, 2] > 20)]
#
#     # KMeans clustering
#     kmeans = KMeans(n_clusters=num_colours, random_state=42)
#     labels = kmeans.fit_predict(image_array)
#     counts = Counter(labels)
#
#     # Sort colors by frequency
#     total_pixels = sum(counts.values())
#     center_colours = kmeans.cluster_centers_
#
#     hex_colours = ['#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))
#                   for r, g, b in center_colours]
#
#     proportions = [count / total_pixels for count in counts.values()]
#     colours = list(zip(hex_colours, proportions))
#     colours.sort(key=lambda z: z[1], reverse=True)
#     return colours


@st.cache_data
def extract_dominant_colours(image_path, num_colours=3, resize=True):
    image = Image.open(image_path)

    if resize:
        image = image.resize((300, 300))  # Speed up processing

    # Convert to numpy and reshape
    image_array = np.array(image)
    image_array = image_array.reshape((-1, 3))

    # Preprocess: remove background and quantize
    image_array = remove_background(image_array, bg_threshold=60)
    image_array = quantize_image_colors(image_array, n_bins=32)

    # KMeans clustering
    kmeans = KMeans(n_clusters=num_colours, random_state=42)
    labels = kmeans.fit_predict(image_array)
    counts = Counter(labels)

    total_pixels = sum(counts.values())
    center_colours = kmeans.cluster_centers_
    proportions = [counts[i] / total_pixels for i in range(len(center_colours))]

    # Merge similar clusters
    merged = merge_similar_clusters(center_colours, proportions, threshold=30)

    # Convert to hex + sort
    colours = []
    for rgb, prop in merged:
        hex_colour = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        colours.append((hex_colour, prop))

    colours.sort(key=lambda x: x[1], reverse=True)
    return colours


def generate_color_gradient(colour_data, width=600, height=50):
    """
    Create a horizontal color gradient bar from the dominant colors.
    :param colour_data: List of (hex_color, proportion)
    :param width: Total width of the image
    :param height: Height of the gradient bar
    :return: PIL Image object
    """
    gradient = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(gradient)

    current_x = 0
    for hex_color, proportion in colour_data:
        color_width = int(proportion * width)
        draw.rectangle([current_x, 0, current_x + color_width, height], fill=hex_color)
        current_x += color_width

    return gradient


def seconds_to_clock(seconds_left: int) -> str:
    t_sec: int = 20*60  # 20 minutes
    p_sec: float = 1 - (seconds_left / t_sec)
    # (hour : 1/2 hour) === (x : x + 12)
    clocks = [
        ("0100", "&#128336"),
        ("0130", "&#128348"),
        ("0200", "&#128337"),
        ("0230", "&#128349"),
        ("0300", "&#128338"),
        ("0330", "&#128350"),
        ("0400", "&#128339"),
        ("0430", "&#128351"),
        ("0500", "&#128340"),
        ("0530", "&#128352"),
        ("0600", "&#128341"),
        ("0630", "&#128353"),
        ("0700", "&#128342"),
        ("0730", "&#128354"),
        ("0800", "&#128343"),
        ("0830", "&#128355"),
        ("0900", "&#128344"),
        ("0930", "&#128356"),
        ("1000", "&#128345"),
        ("1030", "&#128357"),
        ("1100", "&#128346"),
        ("1130", "&#128358"),
        ("1200", "&#128347"),
        ("1230", "&#128359")
    ]
    # 24 segments
    p_sec: int = int(round(p_sec * len(clocks)))
    print(f"sl={seconds_left}, ts={t_sec}, ps={p_sec}, lc={len(clocks)}")
    if (p_sec == 0) or (p_sec == len(clocks)):
        # default show 1200
        return clocks[-2][1]
    return clocks[p_sec][1]


def date_to_this_year(date_in: datetime.date | datetime.datetime, to_year: Optional[int] = None) -> datetime.date | datetime.datetime:
    date_now = datetime.datetime.now() if to_year is None else datetime.datetime(to_year, 1, 1)
    leap_in = is_leap_year(date_in)
    leap_now = is_leap_year(date_now)
    if leap_in and not leap_now:
        if date_in.month == 2 and date_in.day == 29:
            date_in = date_in - datetime.timedelta(days=1)

    date_in = date_in.replace(year=date_now.year)
    return date_in


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
        self.colour_1: str = j_data.get("Colour1")
        self.colour_2: str = j_data.get("Colour2")
        self.colour_3: str = j_data.get("Colour3")
        self.order_date: datetime.date = j_data.get("OrderDate").date()
        self.receive_date: datetime.date = j_data.get("ReceiveDate").date()
        self.open_date: datetime.date = j_data.get("OpenDate").date()
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

        if self.j_id is None:
            raise ValueError(f"{self.j_id} cannot be None")

    def get_colours(self):
        return list(map(Colour, [c for c in [self.colour_1, self.colour_2, self.colour_3] if not pd.isna(c)]))

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

    def __repr__(self) -> str:
        return self.to_string()


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
        self.start_time_atl: datetime.datetime = (self.start_time_utc + self.game_eastern_utc_offset_sec + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
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

    def st_scoreboard_card_p0(self, show_score: bool = True, show_clock: bool = True) -> str:
        show_score = show_score and self.show_game
        show_clock = show_clock and self.show_game
        bg_a: Colour = Colour("#CA7AFF")
        fg_a: Colour = Colour("#000000")
        bg_h: Colour = Colour("#CA7AFF")
        fg_h: Colour = Colour("#000000")
        left_to_right = True
        jc = "flex-start" if left_to_right else "flex-end"
        card_away: str = self.away_team.st_card(show_record=self.show_game)
        card_home: str = self.home_team.st_card(show_record=self.show_game)
        card_away_f = f"<div style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg_a.hex_code}; color: {fg_a.hex_code}'>"
        if show_score:
            card_away_f += f"<div><h6>{self.away_team_score}</h6></div>"
        card_away_f += card_away
        card_away_f += "</div>"
        card_home_f = f"<div style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg_h.hex_code}; color: {fg_h.hex_code}'>"
        card_home_f += card_home
        if show_score:
            card_home_f += f"<h6>{self.home_team_score}</h6>"
        card_home_f += "</div>"
        html = card_away_f
        html += "<h4>@</h4>"
        html += card_home_f

        game_state_fmt, bg_game_state, fg_game_state = game_state_translate(self.game_state)
        html += f"<h5 style='background-color: {bg_game_state.hex_code}; color: {fg_game_state.hex_code}'>{game_state_fmt}<h5>"
        return html

    def st_scoreboard_card(self, show_score: bool = True, show_clock: bool = True) -> str:
        show_score = show_score and self.show_game
        show_clock = show_clock and self.show_game
        bg: Colour = Colour("#CACACA")
        fg: Colour = Colour("#000000")
        left_to_right = True
        jc = "flex-start" if left_to_right else "flex-end"

        # html = f"""<div class='card_scoreboard_{self.g_id}', style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"""
        html = f"""<div class='card_scoreboard_{self.g_id}', style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg.hex_code}; color: {fg.hex_code}'>"""
        html += self.st_scoreboard_card_p0(show_score, show_clock)
        html += "</div>"
        # print(f"{html}")
        # st.code(html, language="html", line_numbers=True)
        return html

    # def st_boxscore_card(self):
    #     bg: Colour = Colour("#CACACA")
    #     fg: Colour = Colour("#000000")
    #     left_to_right = True
    #     jc = "flex-start" if left_to_right else "flex-end"
    #     card_away: str = self.away_team.st_card()
    #     card_home: str = self.home_team.st_card()
    #     card_away_f = f"<div>"
    #     card_away_f += card_away
    #     card_away_f += "</div>"
    #     card_home_f = f"<div>"
    #     card_home_f += card_home
    #     card_home_f += "</div>"
    #     html = f"""<div class='card_scoreboard_{self.g_id}', style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"""
    #     html += card_away_f
    #     html += "<h4>@</h4>"
    #     html += card_home_f
    #
    #     game_state_fmt: str = game_state_translate(self.game_state)
    #     html += f"<h5>{game_state_fmt}<h5>"
    #     # if self.show_game and (game_state_fmt != game_state_translate("FUT")):
    #     #     if game_state_fmt != "FINAL":
    #     #         # game_state_fmt += f" {seconds_to_clock(bs_game_clock_seconds_remaining)}"
    #     #         if bs_game_clock_running:
    #     #             game_state_fmt += f" {E_html_STOPPAGE}"
    #     #         else:
    #     #             game_state_fmt += f" {E_html_PLAYING}"
    #     #         game_state_fmt += f" {bs_game_clock_time_remaining}"
    #     #         game_state_fmt += f" {bs_game_period_num}{number_suffix(bs_game_period_num)}"
    #     #         if bs_game_clock_in_intermission:
    #     #             game_state_fmt += f" intermission"
    #     #         else:
    #     #             game_state_fmt += f" period"
    #     #     else:
    #     #         game_state_fmt += f" - {bs_game_period_type}"
    #     #     #     game_state_fmt += f" {E_strl_RUNNING}"
    #     # elif game_state_fmt == game_state_translate("FUT"):
    #     #     starts_in_h, starts_in_m = divmod((game_start_time_atl - now).total_seconds(), 3600)
    #     #     a__, b__ = starts_in_h, starts_in_m
    #     #     starts_in_h = int(round(starts_in_h, 0))
    #     #     starts_in_m = int(round(starts_in_m / 60, 0))
    #     #     # game_state_fmt += f" {game_start_time_atl=} {now=}, {game_start_time_atl.tzinfo=} {now.tzinfo=}, {starts_in_h=}, {starts_in_m=}, {a__=}, {b__=}"
    #     #     # game_state_fmt += f" {game_start_time_atl:%Y-%m-%d %H:%M} -- "
    #     #     if starts_in_h:
    #     #         game_state_fmt += f" -- {starts_in_h} hour{'' if starts_in_h == 1 else 's'},"
    #     #     else:
    #     #         game_state_fmt += f" --"
    #     #     game_state_fmt += f" {starts_in_m} minute{'' if starts_in_m == 1 else 's'}"
    #
    #     html += "</div>"

    def __repr__(self):
        return f"NHLGAME#{self.g_id} {self.start_time_utc:{UTC_FMT}} {self.away_team} @ {self.home_team}"


class NHLBoxScore(NHLGame):
    def __init__(self, bx_data: dict | pd.Series):
        super().__init__(bx_data)
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
        self.start_time_atl: datetime.datetime = (self.game_start_time_utc + self.game_eastern_utc_offset_sec + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
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
        self.game_clock_seconds_remaining: int = int(self.game_clock.get("secondsRemaining", 1200))
        self.game_clock_running: str = self.game_clock.get("running")
        self.game_clock_in_intermission: str = self.game_clock.get("inIntermission")
        self.game_period_num: int = self.bx_data.get("periodDescriptor", {}).get("number", 1)
        self.game_period_type: int = self.bx_data.get("periodDescriptor", {}).get("periodType", 1)

        self.game_state: str = self.bx_data.get("gameState")
        self.game_schedule_state: str = self.bx_data.get("gameScheduleState")
        self.game_reg_periods: int = self.bx_data.get("regPeriods")

        self.game_last_period_type: str = self.bx_data.get("gameOutcome", {}).get("lastPeriodType")
        self.winning_goalie_p_id: str = self.bx_data.get("winningGoalie", {}).get("playerId")
        self.winning_goalie_first_initial: str = self.bx_data.get("winningGoalie", {}).get("firstInitial", {}).get("default")
        self.winning_goalie_last_name: str = self.bx_data.get("winningGoalie", {}).get("lastName", {}).get("default")

        self.winning_goal_scorer_p_id: str = self.bx_data.get("winningGoalScorer", {}).get("playerId")
        self.winning_goal_scorer_first_initial: str = self.bx_data.get("winningGoalScorer", {}).get("firstInitial", {}).get("default")
        self.winning_goal_scorer_last_name: str = self.bx_data.get("winningGoalScorer", {}).get("lastName", {}).get("default")


    def to_df_row(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if type(v) not in (list, tuple, dict, pd.DataFrame)}

    def st_boxscore_card(self, show_score: bool = True, show_clock: bool = True) -> str:
        show_score = show_score and self.show_game
        show_clock = show_clock and self.show_game
        bg: Colour = Colour("#CACACA")
        fg: Colour = Colour("#000000")
        left_to_right = True
        jc = "flex-start" if left_to_right else "flex-end"

        # html = f"""<div class='card_boxscore_{self.g_id}', style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"""
        html = f"""<div class='card_boxscore_{self.g_id}', style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg.hex_code};'>"""
        html += self.st_scoreboard_card_p0(show_score, show_clock)

        html += "<div>"
        game_state_fmt, game_state_bg, game_state_fg = game_state_translate(self.game_state)
        if show_clock:
            if game_state_fmt == "Live":
                html += f"<div>"
                game_state_fmt += f" {seconds_to_clock(self.game_clock_seconds_remaining)}"
                if self.game_clock_running:
                    game_state_fmt += f" {E_html_STOPPAGE}"
                else:
                    game_state_fmt += f" {E_html_PLAYING}"
                game_state_fmt += f" {self.game_clock_time_remaining}"
                game_state_fmt += f" {self.game_period_num}{number_suffix(self.game_period_num)}"
                if self.game_clock_in_intermission:
                    game_state_fmt += f" intermission"
                else:
                    game_state_fmt += f" period"
                html += f"</div>"
            elif game_state_fmt == game_state_translate("FUT"):
                starts_in_h, starts_in_m = divmod((self.start_time_atl - datetime.datetime.now()).total_seconds(), 3600)
                a__, b__ = starts_in_h, starts_in_m
                starts_in_h = int(round(starts_in_h, 0))
                starts_in_m = int(round(starts_in_m / 60, 0))
                # game_state_fmt += f" {game_start_time_atl=} {now=}, {game_start_time_atl.tzinfo=} {now.tzinfo=}, {starts_in_h=}, {starts_in_m=}, {a__=}, {b__=}"
                # game_state_fmt += f" {game_start_time_atl:%Y-%m-%d %H:%M} -- "
                if starts_in_h:
                    game_state_fmt += f" -- {starts_in_h} hour{'' if starts_in_h == 1 else 's'},"
                else:
                    game_state_fmt += f" --"
                game_state_fmt += f" {starts_in_m} minute{'' if starts_in_m == 1 else 's'}"

        html += f"<H5>{game_state_fmt}</H5>"
        html += "</div>"
        html += "</div>"
        # print(f"{html}")
        # st.code(html, language="html", line_numbers=True)
        return html


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


class NHLGameDate:
    def __init__(self, gd_date: dict):
        self.gd_date: dict = gd_date

        self.date: str = self.gd_date.get("date")
        self.date: datetime.date = datetime.datetime.strptime(self.date, DATE_FMT).date() if self.date else None
        self.dayAbbrev: str = self.gd_date.get("dayAbbrev")
        self.number_of_games: int = self.gd_date.get("numberOfGames", 0)
        self.date_promo: str = self.gd_date.get("datePromo")
        self.games: list[NHLBoxScore] = [NHLBoxScore(bx) for bx in self.gd_date.get("games", [])]


class NHLSchedule:
    def __init__(self, sc_data: dict | pd.Series):
        self.sc_data: dict = sc_data if isinstance(sc_data, dict) else sc_data.to_dict()

        self.next_start_date: str = self.sc_data.get("nextStartDate")
        self.next_start_date: datetime.date = datetime.datetime.strptime(self.next_start_date, DATE_FMT).date() if self.next_start_date else None

        self.previous_start_date: str = self.sc_data.get("previousStartDate")
        self.previous_start_date: datetime.date = datetime.datetime.strptime(self.previous_start_date, DATE_FMT).date() if self.next_start_date else None

        self.pre_season_start_date: str = self.sc_data.get("preSeasonStartDate")
        self.pre_season_start_date: datetime.date = datetime.datetime.strptime(self.pre_season_start_date, DATE_FMT).date() if self.pre_season_start_date else None

        self.regular_season_start_date: str = self.sc_data.get("regularSeasonStartDate")
        self.regular_season_start_date: datetime.date = datetime.datetime.strptime(self.regular_season_start_date, DATE_FMT).date() if self.pre_season_start_date else None

        self.regular_season_end_date: str = self.sc_data.get("regularSeasonEndDate")
        self.regular_season_end_date: datetime.date = datetime.datetime.strptime(self.regular_season_end_date, DATE_FMT).date() if self.pre_season_start_date else None

        self.playoff_end_date: str = self.sc_data.get("playoffEndDate")
        self.playoff_end_date: datetime.date = datetime.datetime.strptime(self.playoff_end_date, DATE_FMT).date() if self.pre_season_start_date else None

        self.game_week: list[NHLGameDate] = [NHLGameDate(gd) for gd in sc_data.get("gameWeek", [])]

    def __repr__(self):
        return f"NHLSchedule {self.next_start_date:{DATE_FMT}}, {self.previous_start_date:{DATE_FMT}}"


class NHLJerseyCollection:
    def __init__(self, excel_path: str, colour_edits_save_file: str = None):
        self.df_jc_data: pd.DataFrame = pd.read_excel(excel_path)
        self.df_jc_data = self.df_jc_data.loc[~pd.isna(self.df_jc_data["ID"])]
        self.df_jc_data["ID"] = self.df_jc_data["ID"].astype(int)
        self.df_jc_data.sort_values(by="ID", ascending=True, inplace=True)

        date_cols = [
            "OrderDate",
            "ReceiveDate",
            "OpenDate",
            "DOB"
        ]
        for col in date_cols:
            self.df_jc_data[col] = pd.to_datetime(self.df_jc_data[col])

        int_cols = ["ID", "NHLID"]
        for col in int_cols:
            self.df_jc_data[col] = self.df_jc_data[col].apply(lambda x: f"{int(x):.0f}" if not pd.isna(x) else None)

        if colour_edits_save_file is not None:
            self.correct_colours(colour_edits_save_file)

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

        self.df_jerseys["JerseyToString"] = self.df_jerseys.apply(lambda row: self.jerseys[row["ID"]].to_string(), axis=1)

    def __repr__(self):
        return f"NHLJerseyCollection: {self.df_jerseys.shape[0]} jerseys between {self.first_date} and {self.last_date}"

    def correct_colours(self, colour_edits_save_file):
        print(f"correct_colours")
        if os.path.exists(os.path.join(os.getcwd(), colour_edits_save_file)):
            print(f"found file")
            with open(colour_edits_save_file, "r") as f:
                colour_edits: dict[str: list[str]] = json.load(f)
            for j_id, lst_colours in colour_edits.items():
                print(f"{j_id=}")
                df_id = self.df_jc_data.loc[self.df_jc_data["ID"] == int(j_id)]
                print(df_id)
                if not df_id.empty:
                    for i, row in df_id.iterrows():
                        for j, col in enumerate(lst_colours):
                            self.df_jc_data.loc[i, f"Colour{j+1}"] = col


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
        left_to_right = True
        jc = "flex-start" if left_to_right else "flex-end"
        html = f"<div class='card_team_{self.t_id}, style='background-color: {bg.hex_code}; foreground-color: {fg.hex_code}; display: flex; justify-content: {jc}; align-items: center;'>"
        html += f"<img src='{self.url_logo}', width='{logo_width}'>"
        if show_record:
            html += f"<h6>{self.record}</h6>"
        html += "</div>"
        return html

    def __eq__(self, other):
        return self.t_id == other.t_id

    def __repr__(self):
        return f"{self.tri_code}"


class NHLSeason:
    def __init__(self, s_data: dict | pd.Series):
        self.s_data: dict = s_data if isinstance(s_data, dict) else s_data.to_dict()
        self.s_id: int = self.s_data.get("id")
        self.conferences_in_use: bool = self.s_data.get("conferencesInUse")
        self.divisions_in_use: bool = self.s_data.get("divisionsInUse")
        self.point_for_ot_loss_in_use: bool = self.s_data.get("pointForOTlossInUse")
        self.regulation_wins_in_use: bool = self.s_data.get("regulationWinsInUse")
        self.row_in_use: bool = self.s_data.get("rowInUse")
        # self.standings_end: datetime.date = datetime.datetime.strptime(self.s_data.get("standingsEnd"), DATE_FMT).date()
        # self.standings_start: datetime.date = datetime.datetime.strptime(self.s_data.get("standingsStart"), DATE_FMT).date()
        self.standings_end: datetime.date = self.s_data.get("standingsEnd")
        self.standings_start: datetime.date = self.s_data.get("standingsStart")
        self.ties_in_use: bool = self.s_data.get("tiesInUse")
        self.wild_card_in_use: bool = self.s_data.get("wildcardInUse")

        self.df_season: pd.DataFrame = None

    def get_season_dates(self) -> pd.DatetimeIndex:
        return pd.date_range(self.standings_start, self.standings_end)

    def __eq__(self, other):
        return self.s_id == other.s_id

    def __repr__(self):
        return f"NHL Season {self.s_id}"


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

    def __init__(self, init: bool = False):
        print("NHLAPIHandler")
        # self.NHL_API_URL: str = "http://statsapi.web.nhl.com/api/v1/"
        self.init: bool = init
        self.save_file = "nhl_api_handler_save.json"

        self.max_secs_get_teams: int = 60 * 60 * 24          # every day
        self.max_secs_get_glossary: int = 60 * 60 * 24       # every day
        self.max_secs_get_player_landing: int = 60 * 60 * 4  # every 4 hours
        self.max_secs_get_country: int = 60 * 60 * 24 * 7    # every week
        self.max_secs_get_roster: int = 60 * 60 * 12         # every 12 hours
        self.max_secs_get_seasons: int = 60 * 60 * 24 * 7    # every week
        self.max_secs_get_standings: int = 60 * 5            # every 5 minutes
        self.max_secs_get_schedule: int = 60 * 60 * 24       # every day
        self.max_secs_get_game_box_score: int = 60           # every minute

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
        self.df_seasons: pd.DataFrame = pd.DataFrame(columns=["s_id"])
        # self.df_schedule: pd.DataFrame = pd.DataFrame(columns=["g_id"])

        if self.init:
            self.get_team_data()
            self.get_seasons_data()
            self.get_standings()
            schedule: NHLSchedule = self.get_schedule()
            d1: datetime.date = schedule.regular_season_start_date
            d2: datetime.date = d1
            ed: datetime.date = schedule.regular_season_end_date
            st.write(f"{d1=}, {d2=}, {ed=}")
            while d1 <= ed:
                d2 = d1
                st.write(f"{d1=}, {d2=}")
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
        df_new_player = pd.DataFrame([{k: v for k, v in player.__dict__.items() if type(v) not in (list, tuple, dict, pd.DataFrame)}])
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
        current_date: datetime.date = datetime.datetime.strptime(results.get("currentDate", datetime.datetime.now().strftime(DATE_FMT)), DATE_FMT).date()
        self.df_seasons = pd.DataFrame(results.get("seasons", []))
        self.df_seasons = self.df_seasons.rename(columns={"id": "s_id"})
        self.df_seasons["standingsEnd"] = self.df_seasons["standingsEnd"].apply(lambda dv: datetime.datetime.strptime(dv, DATE_FMT).date())
        self.df_seasons["standingsStart"] = self.df_seasons["standingsStart"].apply(lambda dv: datetime.datetime.strptime(dv, DATE_FMT).date())
        self.df_seasons["playoffsStart"] = self.df_seasons["standingsEnd"] + datetime.timedelta(days=1)
        self.df_seasons["playoffsEnd"] = self.df_seasons["standingsEnd"] + datetime.timedelta(days=7*14)
        before_christmas = current_date.month > 8
        if current_date < datetime.datetime(current_date.year + (1 if before_christmas else 0), DEFAULT_SEASON_END_DATE.month, DEFAULT_SEASON_END_DATE.day).date():
            # this season is ongoing
            l_idx: int = self.df_seasons.index.tolist()[-1]
            print(f"{l_idx=}")
            self.df_seasons.loc[l_idx, "standingsEnd"] = datetime.date(current_date.year + (1 if before_christmas else 0), DEFAULT_SEASON_END_DATE.month, DEFAULT_SEASON_END_DATE.day + 1)
            self.df_seasons.loc[l_idx, "playoffsStart"] = self.df_seasons.loc[l_idx, "standingsEnd"] + datetime.timedelta(days=1)
            self.df_seasons.loc[l_idx, "playoffsEnd"] = self.df_seasons.loc[l_idx, "standingsEnd"] + datetime.timedelta(days=7*14)
        return self.df_seasons.copy()

    def get_team_roster(self, team_tri_code, season=None, pb=None, pb_text=None) -> pd.DataFrame:
        if season is None:
            season = get_this_season_str()
        # return requests.get(f"https://api-web.nhle.com/v1/roster/{team_tri_code}/{season}").json()
        results = self.query("{0}/v1/roster/{1}/{2}".format(NHL_API_URL, team_tri_code, season), self.max_secs_get_roster)
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
                    pb.progress(value=c/n , text=f"{pb_text if pb_text else ''}{percent(c/n)}")

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
            assert isinstance(game_week, NHLGameDate), f"game_week must be an instance of NHLBoxScore, got '{type(game_week)}'"
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
                    self.df_games_boxscore.loc[self.df_games_boxscore["g_id"] == game_box_score.g_id] = game_box_score.to_df_row().values()
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


#  https://api-web.nhle.com/v1/gamecenter/2024020735/play-by-play


st.set_page_config(layout="wide")

k_nhl_jersey_collection: str = "key_nhl_jersey_collection"
nhl_jc: NHLJerseyCollection = st.session_state.setdefault(k_nhl_jersey_collection, NHLJerseyCollection(PATH_JERSEY_COLLECTION_DATA, JERSEY_COLOUR_SAVE_FILE))

k_nhl_api_handler: str = "key_nhl_api_handler"
if k_nhl_api_handler not in st.session_state:
    st.session_state[k_nhl_api_handler] = NHLAPIHandler(True)
nhl: NHLAPIHandler = st.session_state[k_nhl_api_handler]

teams: pd.DataFrame = nhl.get_team_data()
seasons: pd.DataFrame = nhl.get_seasons_data()
seasons.sort_values(by="standingsEnd", ascending=False, inplace=True)
nhl_season_now: NHLSeason = nhl.get_season()

options_pills_mode: list[str] = [
    "Jerseys",
    "Scores",
    "League Data",
    "Test"
]
k_pills_mode: str = "key_pills_mode"
st.session_state.setdefault(k_pills_mode, 1)
pills_mode = pills(
    label="Mode",
    options=options_pills_mode,
    key=k_pills_mode,
    index=1
)

if pills_mode == options_pills_mode[2]:
    # League Data
    st.write(nhl.get_country())
    st.write(nhl.get_geolocation())
    display_df(
        nhl.df_saved_data,
    "nhl.df_saved_data"
    )
    display_df(
        teams,
        "Teams"
    )
    display_df(
        seasons,
        "Seasons"
    )
    display_df(
        nhl.get_country_data(),
        "Countries"
    )
    display_df(
        nhl.df_players,
        "Known NHL Players"
    )
    with st.container(border=True):
        df_nhl_glossary: pd.DataFrame = nhl.get_glossary_data()
        lst_nhl_glossary_abbrevs: list[str] = df_nhl_glossary["abbreviation"].tolist()
        k_selectbox_nhl_glossary: str = "key_selectbox_nhl_glossary"
        st.session_state.setdefault(k_selectbox_nhl_glossary, random.choice(lst_nhl_glossary_abbrevs))
        selectbox_nhl_glossary = st.selectbox(
            label="Glossary:",
            options=lst_nhl_glossary_abbrevs,
            key=k_selectbox_nhl_glossary
        )
        if selectbox_nhl_glossary:
            df_sel_glossary: pd.Series = \
            df_nhl_glossary.loc[df_nhl_glossary["abbreviation"] == selectbox_nhl_glossary].iloc[0]
            id_ = df_sel_glossary["id"]
            full_name = df_sel_glossary["fullName"]
            definition = df_sel_glossary["definition"]
            first_season_for_stat = df_sel_glossary["firstSeasonForStat"]
            last_updated = df_sel_glossary["lastUpdated"]
            cols_glossary_info = st.columns([0.25, 0.5, 0.25])
            cols_glossary_info[0].text_input(
                label="ID:",
                value=id_,
                disabled=True
            )
            cols_glossary_info[0].text_input(
                label="Full Name:",
                value=full_name,
                disabled=True
            )
            cols_glossary_info[2].text_input(
                label="First Season For Stat",
                value=first_season_for_stat,
                disabled=True
            )
            cols_glossary_info[2].text_input(
                label="Last Updated:",
                value=last_updated,
                disabled=True
            )
            st.text_area(
                label="Definition:",
                value=definition,
                disabled=True
            )

elif pills_mode == options_pills_mode[1]:
    # Scores
    # st.write(nhl_season_now.df_season)
    # st.write(nhl_season_now.get_season_dates())
    # st.write(nhl.standings_by_day(nhl_season_now.get_season_dates()))

    standings_now = nhl.get_standings()
    df_standings_now: pd.DataFrame = standings_now.df_standings

    df_standings_now = df_standings_now.merge(
        nhl.df_teams,
        left_on="t_id",
        right_on="id",
        suffixes=["", "_df_teams"]
    )

    df_current_teams: pd.DataFrame = df_standings_now[["fullName", "t_id"]].dropna(axis=0, how="any")
    lst_teams: list[str] = df_current_teams["fullName"].unique().tolist()

    k_selectbox_team_calendar: str = "key_selectbox_team_calendar"
    selectbox_team_calendar = st.selectbox(
        label="Select a Team",
        key="k_selectbox_team_calendar",
        options=lst_teams
    )
    if selectbox_team_calendar:
        team_events = []
        team_tri_code: str = nhl.df_teams.loc[nhl.df_teams["fullName"].str.lower() == selectbox_team_calendar.lower()].iloc[0]["triCode"]
        df_team_games: pd.DataFrame = nhl.df_games_boxscore.loc[
            (nhl.df_games_boxscore["home_team_name_abbrev"] == team_tri_code)
            | (nhl.df_games_boxscore["away_team_name_abbrev"] == team_tri_code)
        ]
        display_df(
            df_team_games,
            f"{selectbox_team_calendar} Games:"
        )
        for i, row in df_team_games.iterrows():
            is_home: bool = row["home_team_name_abbrev"] == team_tri_code
            opp: str = row['away_team_name_abbrev'] if is_home else row['home_team_name_abbrev']
            team_events.append({
                "id": row["g_id"],
                "title": f"{'vs' if is_home else '@'} {opp}",
                "start": row["start_time_atl"].strftime(UTC_FMT).removesuffix("Z"),
                "end": (row["start_time_atl"] + datetime.timedelta(minutes=60)).strftime(UTC_FMT).removesuffix("Z")
                # ,
                # "url": NHL_URL.removesuffix("/") + row["game_center_link"]
            })

        print(team_events)
        st.write(team_events)

        calendar(
            events=team_events,
            options={
                "height": 500
            }
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
    st.session_state.setdefault(k_pills_standings, 2)
    pills_standings = pills(
        label="Standings",
        key=k_pills_standings,
        options=options_standings,
        index=2
    )
    standings_heights = {
        1: 1160,
        2: 600,
        4: 315,
        6: 140
    }

    cont_0 = st.container()
    cont_1 = st.container()
    use_cont_1: bool = False

    if pills_standings == options_standings[3]:
        # Wildcard
        df_standings_to_show: dict[str: pd.DataFrame] = {
            "Atlantic": df_standings_now_atl.head(3).copy(),
            "Metropolitan": df_standings_now_met.head(3).copy(),
            "Central": df_standings_now_cen.head(3).copy(),
            "Pacific": df_standings_now_pac.head(3).copy(),
            "East WC": df_standings_now_east.loc[(1 <= df_standings_now_east["wildcardSequence"]) & (df_standings_now_east["wildcardSequence"] < 3)].copy(),
            "West WC": df_standings_now_west.loc[(1 <= df_standings_now_west["wildcardSequence"]) & (df_standings_now_west["wildcardSequence"] < 3)].copy()
        }
        use_cont_1 = True
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
    toggle_horizontal = cont_0.toggle(
        label="Horizontal?",
        key=k_toggle_horizontal,
    )
    cols_dfs_to_show = cont_0.columns(len(df_standings_to_show)) if toggle_horizontal else [st.container(border=True) for i in range(len(df_standings_to_show))]
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

    scoreboard_now: NHLScoreboard = nhl.load_scoreboard()
    boxscore_now = nhl.load_game_boxscore(2025020048)
    # st.write(boxscore_now)
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
    st.session_state.setdefault(k_pills_scoreboard_dates)
    pills_scoreboard_dates = pills(
        label="Standings by Date:",
        key=k_pills_scoreboard_dates,
        options=options_pills_scoreboard_dates,
        index=options_pills_scoreboard_dates.index(datetime.date.today().strftime(DATE_FMT))
    )

    cols_commands = st.container(border=True).columns(2)
    if cols_commands[0].button(
        label="show all live games",
        key="key_button_show_all_live_games"
    ):
        lst_games = scoreboard_now.game_dates[scoreboard_now.game_dates.index(list(pills_scoreboard_dates.keys()))]
        for i, game in enumerate(lst_games):
            key = f"key_toggle_show_{scoreboard_now.game_dates.index(list(pills_scoreboard_dates.keys()))}_{i}"
            st.session_state.update({key: True})
        st.rerun()

    show_timer(seconds="indefinite", count_down=False)

    for i, date in enumerate(scoreboard_now.game_dates):
        if date != pills_scoreboard_dates:
            continue
        for j, game in enumerate(scoreboard_now.game_dates[date]):
            cols_scoreboard_table = st.columns([0.18, 0.82])
            k_toggle_show: str = f"key_toggle_show_{i}_{j}"
            show_game: bool = st.session_state.setdefault(k_toggle_show, False)
            game.show_game = show_game
            with cols_scoreboard_table[0].container(height=50, gap=None):
                st.toggle(
                    "Show?",
                    key=k_toggle_show
                )
            if show_game:
                game_box: NHLBoxScore = nhl.load_game_boxscore(game.g_id)
                game_box.show_game = game.show_game
                game_box.away_team = game.away_team
                game_box.home_team = game.home_team
                cols_scoreboard_table[1].markdown(game_box.st_boxscore_card(), unsafe_allow_html=True)
            else:
                cols_scoreboard_table[1].markdown(game.st_scoreboard_card(), unsafe_allow_html=True)

    schedule = nhl.get_schedule()
    st.write(schedule)
    display_df(
        nhl.df_games_boxscore
    )


elif pills_mode == options_pills_mode[0]:

    # Jerseys
    k_pl_id: str = "key_pl_id"
    display_df(
        nhl_jc.df_jerseys,
        "nhl_jc.df_jerseys"
    )
    # lst_selectbox_player = nhl_jc.df_jerseys.loc[~pd.isna(nhl_jc.df_jerseys["PlayerLast"]), "JerseyToString"].dropna().unique().tolist()
    lst_selectbox_player = nhl_jc.df_jerseys["JerseyToString"].dropna().unique().tolist()
    st.session_state.setdefault(k_pl_id, random.choice(lst_selectbox_player))

    pl_to_string = st.selectbox(
        label="Select a player",
        key=k_pl_id,
        options=lst_selectbox_player
    )
    df_selected_jersey_orig: pd.DataFrame = nhl_jc.df_jerseys.loc[nhl_jc.df_jerseys["JerseyToString"] == pl_to_string]
    df_selected_jersey: pd.DataFrame = df_selected_jersey_orig.copy()
    j_idx = df_selected_jersey_orig.index.tolist()[0]
    display_df(
        df_selected_jersey,
        "A df_selected_jersey"
    )
    # df_selected_jersey = df_selected_jersey.merge(
    #     nhl.df_players,
    #     left_on="NHLID",
    #     right_on="p_id",
    #     how="inner"
    # )
    # if df_selected_jersey.empty:
    #     # pla
    #
    # display_df(
    #     df_selected_jersey,
    #     "B df_selected_jersey"
    # )
    df_selected_jersey = df_selected_jersey.merge(
        nhl.df_teams.rename(columns={"id": "t_id"}),
        left_on="Team",
        right_on="fullName",
        how="inner"
    )
    st.write(nhl_jc)
    st.write(nhl_jc.jerseys)
    lst_jerseys = sorted(list(nhl_jc.jerseys))
    j_id = df_selected_jersey_orig.loc[j_idx, "ID"]
    if not df_selected_jersey.empty:
        display_df(
            df_selected_jersey,
            "C df_selected_jersey"
        )
        ser_selected_jersey: pd.Series = df_selected_jersey.iloc[0]
        pl_id = ser_selected_jersey["NHLID"]
        pl_obj: NHLPlayer = nhl.get_player_data(pl_id)
        st.write(pl_obj)
        pl_team: NHLTeam = pl_obj.team
        st.write(f"Player ID# {pl_id}")
        st.write(pl_obj)
        st.write(pl_team)

        if pl_team is None:
            display_df(ser_selected_jersey, "ser_selected_jersey")
            pl_team = nhl.lookup_team(ser_selected_jersey["t_id"])
            # pl_obj.team = pl_team

        image_cols = st.columns(4)
        image_cols[0].image(pl_obj.path_team_logo, width=300)
        image_cols[1].image(pl_obj.birth_country.image_url, width=300)
        image_cols[2].image(pl_obj.path_headshot_logo, width=300)
        image_cols[3].image(pl_obj.path_hero_shot_logo, width=300)

        pl_obj_featured_stats_season, df_pl_obj_featured_stats = pl_obj.featured_stats
        display_df(df_pl_obj_featured_stats, f"Featured Stats {f_season(pl_obj_featured_stats_season)}")
        display_df(pl_obj.career_totals, "Career Totals")
        display_df(pl_obj.season_totals, "Season Totals")

        options_pills_jersey_mode = [
            "Landing",
            "Team Stats",
            "Colour Editing"
        ]
        k_pills_jersey_mode: str = "key_pills_jersey_mode"
        st.session_state.setdefault(k_pills_jersey_mode, 0)
        pills_jersey_mode = pills(
            label="Sub-mode",
            key=k_pills_jersey_mode,
            options=options_pills_jersey_mode,
            label_visibility="hidden",
            index=0
        )

        if pills_jersey_mode == options_pills_jersey_mode[1]:
            load_player_progress = st.progress(value=0, text=f"Loading {pl_team.full_name} Roster -- 0%")
            display_df(
                nhl.get_team_roster(pl_team.tri_code, pb=load_player_progress, pb_text=f"Loading {pl_team.full_name} Roster -- "),
                f"{pl_team.full_name} {f_season(get_this_season_str())} Team Roster"
            )

        # k_selectbox_jersey = "key_selectbox_jersey"
        # st.session_state.setdefault(k_selectbox_jersey, random.choice(lst_jerseys))
        # selectbox_jersey = st.selectbox(
        #     label="Select a Jersey:",
        #     key=k_selectbox_jersey,
        #     options=lst_jerseys
        # )
        #
        # if str(selectbox_jersey):
        elif pills_jersey_mode == options_pills_jersey_mode[2]:
            with st.expander(label="Edit Jersey Colours", expanded=False):
                k_j_editing: str = "key_j_editing"
                j_editing: int = st.session_state.setdefault(k_j_editing, None)
                for i, j_id in enumerate(nhl_jc.jerseys):
                    j_c_cols = st.columns([0.7, 0.1, 0.1, 0.1])
                    j_obj: Jersey = nhl_jc.jerseys[j_id]
                    colours_lst = j_obj.get_colours()
                    # j_c_cols[0].write(f"#{j_id} {j_obj.to_string()}")
                    lst_images: list[str] = os.listdir(j_obj.image_folder)
                    if lst_images:
                        colours = extract_dominant_colours(
                            os.path.join(j_obj.image_folder, lst_images[0]),
                            num_colours=10
                        )
                        gradient_img = generate_color_gradient(colours, width=int(0.7 * 1600), height=50)
                        j_c_cols[0].image(gradient_img, caption=j_obj.to_string())

                        if j_c_cols[0].button(
                                "edit",
                                key=f"key_button_edit_jersey_colours_{i}"
                        ):
                            st.session_state.update({k_j_editing: i})
                            st.rerun()

                        if i == j_editing:
                            num_selectors = j_c_cols[0].slider("How many colours to define?", 1, 5, 3)
                            selected_positions = []
                            selected_colours = []

                            for i in range(num_selectors):
                                pos = j_c_cols[0].slider(f"Position for Colour {i + 1}", 0.0, 1.0, step=0.01,
                                                         key=f"slider_{i}")
                                selected_positions.append(pos)
                                sampled_hex = get_color_at_position(gradient_img, pos)
                                selected_colours.append(sampled_hex)

                                j_c_cols[i + 1].markdown(
                                    f"<div style='display: flex; align-items: center;'>"
                                    f"<div style='width: 40px; height: 20px; background-color: {sampled_hex}; "
                                    f"border: 1px solid #000; margin-right: 10px;'></div>"
                                    f"Selected Colour {i + 1}: {sampled_hex}"
                                    f"</div>", unsafe_allow_html=True)
                            if j_c_cols[0].button(
                                    label="save",
                                    key=f"key_button_save_jersey_colours_{i}"
                            ):
                                if os.path.exists(os.path.join(os.getcwd(), JERSEY_COLOUR_SAVE_FILE)):
                                    with open(JERSEY_COLOUR_SAVE_FILE, "r") as f:
                                        saved_data = json.load(f)
                                else:
                                    saved_data = {}
                                saved_data[f"{j_id}"] = selected_colours
                                with open(JERSEY_COLOUR_SAVE_FILE, "w") as f:
                                    f.write(json.dumps(saved_data, indent=4))
                                st.toast("Changes saved successfully!")
                                st.session_state.update({k_j_editing: None})
                                st.rerun()
                            j_c_cols[0].divider()


                    else:
                        j_c_cols[0].write("No images on file.")
                    # j_c_cols[1].write(colours_lst)
                    for j, c in enumerate(colours_lst, start=1):
                        k_cp: str = f"{j_id}_{j}_cp"
                        st.session_state.update({k_cp: c.hex_code})
                        j_c_cols[j].color_picker(
                            label=f"Colour{i}",
                            key=k_cp
                        )
                        # j_c_cols[j].markdown(f"""
                        # <div style='background-color: {c.hex_code}'>
                        #     <h3>{c.hex_code}</h3>
                        # </div>
                        # """.strip(), unsafe_allow_html=True)
        else:
            sel_jersey: Jersey = nhl_jc.jerseys[j_id]
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
                lst_images: list[str] = os.listdir(sel_jersey.image_folder)
                for i, path in enumerate(lst_images):
                    with cols_jersey_images[i]:
                        st.image(os.path.join(sel_jersey.image_folder, path))

                colours = extract_dominant_colours(
                    os.path.join(sel_jersey.image_folder, lst_images[0]),
                    num_colours=10
                )

                # for hex_colour, proportion in colours:
                #     st.markdown(
                #         f"<div style='display: flex; align-items: center;'>"
                #         f"<div style='width: 40px; height: 20px; background-color: {hex_colour}; "
                #         f"border: 1px solid #000; margin-right: 10px;'></div>"
                #         f"{hex_colour} — {proportion * 100:.2f}%"
                #         f"</div>", unsafe_allow_html=True)
                #
                # st.write(colours)

                gradient_img = generate_color_gradient(colours, width=600, height=50)
                st.image(gradient_img, caption="Dominant Colour Gradient")

    jc_events = []
    colour_order_tile: Colour = Colour("#451212")
    colour_receive_tile: Colour = Colour("#124512")
    colour_open_tile: Colour = Colour("#121245")
    colour_birthday_tile: Colour = Colour("#124545")
    k_check_combine: str = "key_check_combine"
    st.session_state.setdefault(k_check_combine, False)
    check_combine = st.checkbox(
        label="combine all years",
        key=k_check_combine
    )
    with st.columns([0.8, 0.2])[1]:
        for k, c in {
            "Ordered": colour_order_tile,
            "Received": colour_receive_tile,
            "Opened": colour_open_tile,
            "Birthday": colour_birthday_tile
        }.items():
            st.markdown(coloured_block(
                label=f"{k}: {c.hex_code}",
                bg=c
            ), unsafe_allow_html=True)
    covered_player_birthdays = []
    for i, row in nhl_jc.df_jerseys.iterrows():
        j_obj: Jersey = nhl_jc.jerseys[row["ID"]]
        order_date_og: datetime.date = j_obj.order_date
        receive_date_og: datetime.date = j_obj.receive_date
        open_date_og: datetime.date = j_obj.open_date
        dob_og: datetime.date = j_obj.dob
        order_date = date_to_this_year(order_date_og) if check_combine else order_date_og
        receive_date = date_to_this_year(receive_date_og) if check_combine else receive_date_og
        open_date = date_to_this_year(open_date_og) if check_combine else open_date_og
        dob = date_to_this_year(dob_og) if check_combine else dob_og
        if not pd.isna(j_obj.order_date):
            jc_events.append({
                "id": f"jc_event_order_date_{i}",
                "groupId": f"order_date",
                "title": f"{j_obj.to_string()}" + (f" - {order_date_og.year}" if check_combine else ""),
                "backgroundColor": colour_order_tile.hex_code,
                "start": order_date.strftime(DATE_FMT)
            })
        if not pd.isna(j_obj.receive_date):
            jc_events.append({
                "id": f"jc_event_receive_date_{i}",
                "groupId": f"receive_date",
                "title": f"{j_obj.to_string()}" + (f" - {receive_date_og.year}" if check_combine else ""),
                "backgroundColor": colour_receive_tile.hex_code,
                "start": receive_date.strftime(DATE_FMT)
            })
        if not pd.isna(j_obj.open_date):
            jc_events.append({
                "id": f"jc_event_open_date_{i}",
                "groupId": f"open_date",
                "title": f"{j_obj.to_string()}" + (f" - {open_date_og.year}" if check_combine else ""),
                "backgroundColor": colour_open_tile.hex_code,
                "start": open_date.strftime(DATE_FMT)
            })
        if not pd.isna(j_obj.dob):
            cpb = f"{j_obj.player_first} {j_obj.player_last}".lower()
            if cpb not in covered_player_birthdays:
                jc_events.append({
                    "id": f"jc_event_dob_{i}",
                    "groupId": f"dob",
                    "title": f"Birthday! {j_obj.player_first} {j_obj.player_last} - {dob_og.year}",
                    "backgroundColor": colour_birthday_tile.hex_code,
                    "start": dob.strftime(DATE_FMT)
                })
                covered_player_birthdays.append(cpb)

    if check_combine:
        jc_events.sort(key=lambda event: (event["title"][-4:], event["start"]))
    else:
        jc_events.sort(key=lambda event: event["start"])

    cal = calendar(
        events=jc_events,
        options={
            "initialView": "multiMonthYear",
            "multiMonthMaxColumns": 3,
            "height": 1800,
            "contentHeight": 500,
            "expandRows": True,
            "dayMaxEventRows": 10,  # unlimited rows per day (or set an int)
            "eventDisplay": "block",
            "displayEventTime": False
            # ,
            # "moreLinkClick": "popover",  # still works without callbacks
        }
        # ,
        # custom_css=custom_css,
    )

    st.write(cal)


else:
    options_pills_testing_mode = ["Jersey Colour Analyzer", "NHL API Probe"]
    k_pills_testing_mode: str = "key_pills_testing_mode"
    st.session_state.setdefault(k_pills_testing_mode, len(options_pills_testing_mode) - 1)
    pills_testing_mode = pills(
        label="Mode",
        key=k_pills_testing_mode,
        options=options_pills_testing_mode
    )

    if pills_testing_mode == options_pills_testing_mode[0]:

        st.title("🏒 Hockey Jersey Colour Analyzer")

        uploaded_file = st.file_uploader("Upload a jersey image", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Jersey")

            st.write("🎨 Extracting dominant colours...")

            num_colours = st.slider("Number of dominant colours", 1, 10, 4)

            colours = extract_dominant_colours(uploaded_file, num_colours=num_colours)

            for hex_colour, proportion in colours:
                st.markdown(
                    f"<div style='display: flex; align-items: center;'>"
                    f"<div style='width: 40px; height: 20px; background-color: {hex_colour}; "
                    f"border: 1px solid #000; margin-right: 10px;'></div>"
                    f"{hex_colour} — {proportion * 100:.2f}%"
                    f"</div>", unsafe_allow_html=True)

            st.write(colours)

            gradient_img = generate_color_gradient(colours, width=600, height=50)
            st.image(gradient_img, caption="Dominant Colour Gradient")

            # Extract hex colors and proportions
            hex_colour_labels = [f"{color} - {percent(p)}" for color, p in colours]
            hex_colours = [color for color, p in colours]
            proportions = [p for _, p in colours]
            fig, ax = plt.subplots()
            ax.pie(proportions, labels=hex_colour_labels, colors=hex_colours, startangle=90, counterclock=False)
            ax.axis('equal')
            st.pyplot(fig)
    else:
        known_endpoints = {
            NHL_PLAYER_API_URL: "",
            NHL_ASSET_API_URL: "",
            NHL_STATS_API_URL: "",
            NHL_API_URL: ""
        }

        df_known_urls: pd.DataFrame = nhl.df_saved_data.copy()
        display_df(
            df_known_urls,
            "df_known_urls"
        )

        k_text_url: str = "key_text_url"

        cols_known_endpoints = st.columns(len(known_endpoints))
        for i, ke in enumerate(known_endpoints):
            with cols_known_endpoints[i]:
                if st.button(
                    ke,
                    key=f"key_known_endpoint_{i}"
                ):
                    st.session_state.update({k_text_url: ke})
                st.write(known_endpoints[ke])

        text_url_v: str = st.session_state.setdefault(k_text_url, "")
        text_url = st.text_input(
            label="URL",
            key=f"tu{k_text_url}",
            value=text_url_v
        )
        cols_submission = st.columns(2)
        with cols_submission[0]:
            if st.button(
                label="clear",
                key=f"key_button_clear_text_url"
            ):
                st.session_state.update({k_text_url: ""})
                text_url_v = ""
        with cols_submission[1]:
            if st.button(
                label="check",
                key=f"key_button_check_text_url",
                disabled=not bool(st.session_state.get(k_text_url))
            ):
                url: str = st.session_state.get(k_text_url)
                st.session_state.update({k_text_url: url})

        if text_url_v:
            st.subheader("Results:")
            st.code(text_url_v)
            data = nhl.query(text_url_v)
            st.write(data)



# show_timer(10, count_down=True)
# show_timer(10, count_down=False)
#
# # # k_selectbox_team: str = "key_selectbox_team"
# # # selectbox_team = st.selectbox(
# # #     label="Select a Team:",
# # #     key=k_selectbox_team,
# # #     options=nhl.df_teams["triCode"]
# # # )
# # # if selectbox_team:
# # #     ser_team: pd.Series = nhl.df_teams.loc[nhl.df_teams["triCode"] == selectbox_team].iloc[0]
# # #     t_id = ser_team["id"]
# # #     sel_team: NHLTeam = nhl.lookup_team(t_id)
# # #     st.write(sel_team)
# # #     # cgs = nhl.check_game_status(sel_team.t_id, date=datetime.date.today())
# # #     st.write(cgs)


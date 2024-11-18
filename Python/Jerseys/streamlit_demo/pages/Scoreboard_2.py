import datetime
import os.path

import dateutil.tz
import pytz
from typing import Any, Literal, List, Optional

import pandas as pd
import requests
import streamlit as st
from st_click_detector import click_detector
from streamlit_extras.let_it_rain import rain

from colour_utility import Colour, gradient
from utility import number_suffix
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# from streamlit_demo.streamlit_utility import aligned_text
# from utility import Dict2Class



# Game IDs
# will look like this: 2023020001
# The first 4 digits identify the season of the game
# (ie. 2017 for the 2017-2018 season).
# Always refer to a season with the starting year.
# A game played in March 2018 would still have a game ID that starts with 2017
# The next 2 digits give the type of game, where
#   01 = preseason,
#   02 = regular season,
#   03 = playoffs,
#   04 = all-star
# The final 4 digits identify the specific game number.
# For regular season and preseason games,
# this ranges from 0001 to the number of games played.
# (1353 for seasons with 32 teams (2022 - Present),
# 1271 for seasons with 31 teams (2017 - 2020)
# and 1230 for seasons with 30 teams).
# For playoff games,
# the 2nd digit of the specific number gives the round of the playoffs,
# the 3rd digit specifies the matchup,
# and the 4th digit specifies the game (out of 7).

# d = not True
# e = False
# d==e

# Hold times in seconds
TIME_APP_REFRESH: float = 1000 * 60
SCOREBOARD_HOLD_TIME: float = 60 * 30  # hold scoreboard data for 30 min
GAME_HOLD_TIME: float = 60 * 1.5  # recheck game data every 1.5 min
SHOW_SPINNERS: bool = True
TIMEZONE_OFFSET: int = -60 * 60 * 4
width_image_logo: int = 64


E_strl_RUNNING: str = f":ice_hockey_stick_and_puck:"
E_strl_STOPWATCH: str = f":stopwatch:"
E_html_STOPPAGE: str = f"&#128721"
E_html_PLAYING: str = f"&#127954"

# Replace this

def aligned_text(
        txt: str,
        tag_style: Literal["h1", "h2", "h3", "h4", "h5", "h6", "p", "span"] = "h1",
        h_align: Literal["left", "center", "right"] = "center",
        colour: str = "#FFFFFF",
        line_height: int | float = 1,
        font_size: int = 12,
        id_: str = None
) -> str:
    """
    Return formatted HTML, and in-line CSS to h_align a given text in a container.
    Use with streamlit's markdown function and with 'unsafe_allow_html' set to True.
    See coloured_text() for streamlined-colour-only functionality.
    """
    if isinstance(line_height, float):
        line_height = f"{line_height}%"
    if id_:
        id_ = f" id='{id_}',"
    else:
        id_ = ""
    return f"<{tag_style}{id_} style='line-height: {line_height}; text-align: {h_align}; color: {colour}; font-size: {font_size}px'>{txt}</{tag_style}>"


st.set_page_config(layout="wide", page_title="NHL Scoreboard")
st.title("NHL Scoreboard")
st.session_state.setdefault("affected_games", {})


@st.cache_data(show_spinner=SHOW_SPINNERS)
def load_team_excel() -> dict[str: pd.DataFrame]:
    path = r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHL Jerseys as of 202411101523.xlsm"
    if not os.path.exists(path):
        path = r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\NHL Jerseys as of 202411101523.xlsm"
    return pd.read_excel(path, sheet_name=["NHLTeams", "Conferences", "Divisions"])


@st.cache_data(show_spinner=SHOW_SPINNERS, ttl=GAME_HOLD_TIME)
def load_game_boxscore(game_id: int) -> dict[str: Any]:
    # return requests.get(f"https://statsapi.web.nhl.com/api/v1/game/{game_id}/boxscore").json()
    print(f"New Game Boxscore {game_id=}, {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    return requests.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore").json()


@st.cache_data(show_spinner=SHOW_SPINNERS, ttl=GAME_HOLD_TIME)
def load_game_landing(game_id: int) -> dict[str: Any]:
    print(f"New Game Landing {game_id=}, {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    return requests.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/landing").json()


@st.cache_data(show_spinner=SHOW_SPINNERS, ttl=SCOREBOARD_HOLD_TIME)
def load_scoreboard(date_str: Optional[str] = None):
    print(f"New Scoreboard data")
    if date_str is None:
        return requests.get(f"https://api-web.nhle.com/v1/scoreboard/now").json()
    else:
        return requests.get(f"https://api-web.nhle.com/v1/score/{date_str}").json()


@st.cache_data(show_spinner=SHOW_SPINNERS, ttl=SCOREBOARD_HOLD_TIME)
def load_standings(date_str: Optional[str] = None):
    print(f"New Standings data")
    url: str = "https://api-web.nhle.com/v1/standings/now"
    if date_str is not None:
        url += f"/{date_str}"
    return requests.get(url).json()


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


def game_state_translate(game_state: str) -> str:
    match game_state:
        case "FUT": return "Upcoming"
        case "OFF": return "FINAL"
        case _: return game_state


def team_colour(team_id: int, style: str = "bg", dark_mode: bool = True) -> Colour:
    # return Colour(gradient(team_id, 42, "#343434", "#676767", rgb=False))
    df_team = df_nhl_teams.loc[df_nhl_teams["NHL_ID"] == team_id].reset_index()
    if df_team.empty:
        return Colour("#FF0000")
    df_team = df_team.iloc[0]
    colours = [df_team[f"Colour_{i}"] for i in range(1, 7)]
    colours = [Colour(v) for v in colours if not pd.isna(v)]
    # colours_v = sorted([(c.hex_code, c) for c in colours], reverse=dark_mode, key=lambda tup: tup[0])
    colours_v = [(c, c) for c in colours]
    bg_idx, fg_idx = 0, 1  # len(colours_v) - 1
    # if dark_mode:
    #     bg_idx, fg_idx = fg_idx, bg_idx
    # # print(f"{df_team['ShortTeamName']} {team_id=}")
    # # return Colour(df_team["Colour_1"])
    if style == "fg":
        return colours_v[fg_idx][1].brighten(0.15)
    else:
        return colours_v[bg_idx][1]


def handle_button_click():
    print(f"handle_button_click")
    query_params = st.experimental_get_query_params()
    if 'clicked_button' in query_params:
        clicked = query_params['clicked_button'][0]
        st.session_state['clicked_button'] = clicked
        st.write(f"Button clicked: {clicked}")
        # Update the interface or logic based on the clicked button
        if clicked == "team1":
            st.write("You clicked on Team 1!")
        elif clicked == "team2":
            st.write("You clicked on Team 2!")


def team_info_card(team_data: dict[str:Any], left_to_right: bool = True, show_points: bool = True) -> str:
    
    name_short: str = team_data.get('teamAbbrev', {}).get('default')
    team_logo: str = team_data.get("teamLogo")
    team_points: int = None
    if show_points:
        team_points = team_data.get("points")
    # st.write(f"{name_short}")
    # st.write(f"{team_logo}")
    #if team_logo:
    #    st.image(team_logo, width=40)
    df_team: pd.DataFrame = df_nhl_teams.loc[df_nhl_teams["ShortTeamName"] == name_short].reset_index()
    team_id: int = -1
    if not df_team.empty:
        df_team: pd.DataFrame = df_team.iloc[0]
        team_id = df_team["NHL_ID"]
   
    fg: Colour = team_colour(team_id, "fg")
    bg: Colour = team_colour(team_id, "bg")
    #flt = "left" if left_to_right else "right"
    jc = "flex-start" if left_to_right else "flex-end"
    #jc = "center"
   
    html = ""
    # html += f"<div id='team_{team_id}', style='display: flex; justify-content: space-around; background-color: {bg.hex_code}; foreground-color: {fg.hex_code}';>"
    # html += f"""<div id='team_{team_id}', style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg.hex_code}; foreground-color: {fg.hex_code};', onclick="sendToStreamlit('{name_short}')">"""
    html += f"""<div id='div_team_{team_id}', style='display: flex; justify-content: {jc}; align-items: center; background-color: {bg.hex_code}; foreground-color: {fg.hex_code};'>"""
    # html += f"<div id='team_{team_id}'; style='background-color: {bg.hex_code}; foreground-color: {fg.hex_code}';>"
    # html += aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size)
    # html += aligned_text(score, tag_style="span", colour=fg.hex_code, font_size=font_size)
    x = """
    html_lines = [
        aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size) if team_points is not None else "",
        f"<img src='{team_logo}', alt='{name_short}', width='{width_image_logo}', height='{width_image_logo}'>",
        aligned_text(name_short, tag_style="span", colour=fg.hex_code, font_size=font_size)
    ]
    """
    html_lines = [
        aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size, id_=f"pts_team_{team_id}") if team_points is not None else "",
        # f"""<input type='image' src='{team_logo}', alt='{name_short}', width='{width_image_logo}', height='{width_image_logo}', onclick="sendToStreamlit('{name_short}')">""",
        # f"""<input id='img_team_{team_id}', type='image' src='{team_logo}', alt='{name_short}', width='{width_image_logo}', height='{width_image_logo}'>""",
        # f"""<button id='btn_team_{team_id}', width='{width_image_logo}', height='{width_image_logo}'><img src='{team_logo}', alt='{name_short}'/></button>""",
        f"""<a href='#' id='img_team_{team_id}'><img width='{width_image_logo}', height='{width_image_logo}' src='{team_logo}'></a>""",
        aligned_text(name_short, tag_style="span", colour=fg.hex_code, font_size=font_size, id_=f"name_team_{team_id}")
    ]
    
    if not left_to_right:
        html_lines = html_lines[::-1]
    
    w = """
    if left_to_right:
        if points is not None:
            html += aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += f"<img src='{team_logo}', alt='{name_short}', width='{width_image_logo}', height='{width_image_logo}'>"
        html += aligned_text(name_short, tag_style="span", colour=fg.hex_code, font_size=font_size)
    else:
        html += aligned_text(name_short, tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += f"<img src='{team_logo}', alt='{name_short}', width='{width_image_logo}', height='{width_image_logo}'>"
        if points is not None:
            html += aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size)
    # html += f" " + aligned_text(team_record, tag_style="span", colour=fg.hex_code, font_size=font_size)
    # if show_game:
    #     html += aligned_text(f" SOG: {bs_shots_on_goal}", tag_style="span", colour=fg.hex_code, font_size=font_size)
    """
    html += "".join(html_lines).strip()
    html += f"</div>"
    return html
    

# def game_summary_card():


def game_team_card(game_data: dict[str: Any], game_box_score: dict[str: Any], game_landing: dict[str: Any], team_id: int) -> str:
    bg: Colour = team_colour(team_id)
    fg: Colour = team_colour(team_id, "fg")

    away_team_id: int = game_data.get("awayTeam", {}).get("id")
    home_team_id: int = game_data.get("homeTeam", {}).get("id")
    team_key = "awayTeam" if away_team_id == team_id else "homeTeam"
    bs_game_team: dict[str: Any] = game_box_score.get(team_key, {})
    bs_game_team_id: int = bs_game_team.get("id")
    bs_game_team_name: str = bs_game_team.get("name", {}).get("default")
    bs_game_team_name_fr: str = bs_game_team.get("name", {}).get("fr")
    bs_game_team_abbrev: str = bs_game_team.get("abbrev")
    bs_game_team_logo: str = bs_game_team.get("logo")
    bs_game_team_dark_logo: str = bs_game_team.get("darkLogo")
    bs_game_team_place_name: str = bs_game_team.get("placeName", {}).get("default")
    bs_game_team_place_name_fr: str = bs_game_team.get("placeName", {}).get("fr")
    bs_game_team_place_name_prep: str = bs_game_team.get("placeNameWithPreposition", {}).get("default")
    bs_game_team_place_name_prep_fr: str = bs_game_team.get("placeNameWithPreposition", {}).get("fr")
    bs_game_team_score: int = bs_game_team.get("score", 0)

    bs_shots_on_goal: int = game_landing.get(team_key, {}).get("sog", 0)

    font_size: int = 24
    key_toggle: str = f"toggle_show_game_{game_id}"
    show_game: bool = st.session_state.get(key_toggle)
    bs_shots_on_goal: str = str(bs_shots_on_goal) if show_game else "?"
    score: str = str(bs_game_team_score) if show_game else "?"
    logo: str = bs_game_team_dark_logo
    team_name_abbrev: str = bs_game_team_abbrev

    data_team: dict[str: Any] = json_standings.get("standings", [])[standings_indexer[team_name_abbrev]]
    team_wins: int = data_team.get("wins", 0)
    team_losses: int = data_team.get("losses", 0)
    team_otl: int = data_team.get("otLosses", 0)
    team_sol: int = data_team.get("shootoutLosses", 0)
    team_otl_sol: int = team_otl + team_sol
    team_record: str = f"({team_wins}-{team_losses}-{team_otl_sol})"

    html = ""
    html += f"<div id='team_{team_id}', style='background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"
    html += aligned_text(score, tag_style="span", colour=fg.hex_code, font_size=font_size)
    html += f"<img src='{logo}', alt='{team_name_abbrev}', width='{width_image_logo}', height='{width_image_logo}'>"
    html += aligned_text(team_name_abbrev, tag_style="span", colour=fg.hex_code, font_size=font_size)
    html += f" " + aligned_text(team_record, tag_style="span", colour=fg.hex_code, font_size=font_size)
    if show_game:
        html += aligned_text(f" SOG: {bs_shots_on_goal}", tag_style="span", colour=fg.hex_code, font_size=font_size)
    html += f"</div>"
    return html


def game_card(game_data: dict[str: Any]) -> str:

    colour_bg_div0: Colour = Colour("#424242")
    font_size: int = 24

    game_id: int = game_data.get("id")
    game_season: int = game_data.get("season")
    game_type: int = game_data.get("gameType")
    game_date: str = game_data.get("gameDate")
    game_center_link: str = game_data.get("gameCenterLink")
    game_venue: str = game_data.get("venue", {}).get("default")
    game_start_time_utc: str = game_data.get("startTimeUTC")
    game_eastern_utc_offset: str = game_data.get("easternUTCOffset")
    game_venue_utc_offset: str = game_data.get("venueUTCOffset")
    game_tv_broadcasts: list[dict[str: Any]] = game_data.get("tvBroadcasts")

    game_state: str = game_data.get("gameState")
    game_schedule_state: str = game_data.get("gameScheduleState")
    away_team_id: int = game_data.get("awayTeam", {}).get("id")
    away_team_name_full: str = game_data.get("awayTeam", {}).get("name", {}).get("default")
    away_team_name_fr: str = game_data.get("awayTeam", {}).get("name", {}).get("fr")
    away_team_name_short: str = game_data.get("awayTeam", {}).get("commonName", {}).get("default")
    away_team_place_name_prep: str = game_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get("default")
    away_team_place_name_prep_fr: str = game_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get("fr")
    away_team_name_abbrev: str = game_data.get("awayTeam", {}).get("abbrev")
    away_team_score: int = game_data.get("awayTeam", {}).get("score", 0)
    away_team_logo: str = game_data.get("awayTeam", {}).get("logo")

    home_team_id: int = game_data.get("homeTeam", {}).get("id")
    home_team_name_full: str = game_data.get("homeTeam", {}).get("name", {}).get("default")
    home_team_name_fr: str = game_data.get("homeTeam", {}).get("name", {}).get("fr")
    home_team_name_short: str = game_data.get("homeTeam", {}).get("commonName", {}).get("default")
    home_team_place_name_prep: str = game_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get("default")
    home_team_place_name_prep_fr: str = game_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get("fr")
    home_team_name_abbrev: str = game_data.get("homeTeam", {}).get("abbrev")
    home_team_score: int = game_data.get("homeTeam", {}).get("score", 0)
    home_team_logo: str = game_data.get("homeTeam", {}).get("logo")

    game_tickets_link: str = game_data.get("ticketsLink")
    game_tickets_link_fr: str = game_data.get("ticketsLinkFr")
    game_period: int = game_data.get("period", 1)
    game_period_desc_number: int = game_data.get("periodDescriptor", {}).get("number", 1)
    game_period_desc_type: str = game_data.get("periodDescriptor", {}).get("periodType")
    game_period_desc_max_reg_periods: int = game_data.get("periodDescriptor", {}).get("maxRegulationPeriods", 3)
    game_three_min_recap: str = game_data.get("threeMinRecap")
    game_three_min_recap_fr: str = game_data.get("threeMinRecapFr")

    game_box_score: dict[str: Any] = load_game_boxscore(game_id)
    bs_game_id: int = game_box_score.get("id")
    bs_game_season: int = game_box_score.get("season")
    bs_game_type: int = game_box_score.get("gameType")
    bs_game_limited_scoring: bool = game_box_score.get("limitedScoring")
    bs_game_date: int = game_box_score.get("gameDate")
    bs_game_venue: str = game_box_score.get("venue", {}).get("default")
    bs_game_venue_fr: str = game_box_score.get("venue", {}).get("fr")
    bs_game_venue_location: str = game_box_score.get("venueLocation", {}).get("default")
    bs_game_venue_location_fr: str = game_box_score.get("venueLocation", {}).get("fr")
    bs_game_start_time_utc: int = game_box_score.get("startTimeUTC")
    bs_game_eastern_utc_offset: int = game_box_score.get("easternUTCOffset")
    bs_game_venue_utc_offset: int = game_box_score.get("venueUTCOffset")
    bs_game_broadcasts: list[dict[str: Any]] = game_box_score.get("tvBroadcasts", [])

    bs_game_away_team: dict[str: Any] = game_box_score.get("awayTeam", {})
    bs_game_away_team_id: int = bs_game_away_team.get("id")
    bs_game_away_team_score: int = bs_game_away_team.get("score", 0)
    bs_game_away_team_name: str = bs_game_away_team.get("name", {}).get("default")
    bs_game_away_team_name_fr: str = bs_game_away_team.get("name", {}).get("fr")
    bs_game_away_team_abbrev: str = bs_game_away_team.get("abbrev")
    bs_game_away_team_logo: str = bs_game_away_team.get("logo")
    bs_game_away_team_dark_logo: str = bs_game_away_team.get("darkLogo")
    bs_game_away_team_place_name: str = bs_game_away_team.get("placeName", {}).get("default")
    bs_game_away_team_place_name_fr: str = bs_game_away_team.get("placeName", {}).get("fr")
    bs_game_away_team_place_name_prep: str = bs_game_away_team.get("placeNameWithPreposition", {}).get("default")
    bs_game_away_team_place_name_prep_fr: str = bs_game_away_team.get("placeNameWithPreposition", {}).get("fr")

    bs_game_home_team: dict[str: Any] = game_box_score.get("homeTeam", {})
    bs_game_home_team_id: int = bs_game_home_team.get("id")
    bs_game_home_team_score: int = bs_game_home_team.get("score", 0)
    bs_game_home_team_name: str = bs_game_home_team.get("name", {}).get("default")
    bs_game_home_team_name_fr: str = bs_game_home_team.get("name", {}).get("fr")
    bs_game_home_team_abbrev: str = bs_game_home_team.get("abbrev")
    bs_game_home_team_logo: str = bs_game_home_team.get("logo")
    bs_game_home_team_dark_logo: str = bs_game_home_team.get("darkLogo")
    bs_game_home_team_place_name: str = bs_game_home_team.get("placeName", {}).get("default")
    bs_game_home_team_place_name_fr: str = bs_game_home_team.get("placeName", {}).get("fr")
    bs_game_home_team_place_name_prep: str = bs_game_home_team.get("placeNameWithPreposition", {}).get("default")
    bs_game_home_team_place_name_prep_fr: str = bs_game_home_team.get("placeNameWithPreposition", {}).get("fr")

    bs_game_clock: dict[str: Any] = game_box_score.get("clock", {})
    bs_game_clock_time_remaining: str = bs_game_clock.get("timeRemaining")
    bs_game_clock_seconds_remaining: int = int(bs_game_clock.get("secondsRemaining"))
    bs_game_clock_running: str = bs_game_clock.get("running")
    bs_game_clock_in_intermission: str = bs_game_clock.get("inIntermission")
    bs_game_period_num: int = game_box_score.get("periodDescriptor", {}).get("number", 1)
    bs_game_period_type: int = game_box_score.get("periodDescriptor", {}).get("periodType", 1)

    bs_game_state: str = game_box_score.get("gameState")
    bs_game_schedule_state: str = game_box_score.get("gameScheduleState")
    bs_game_reg_periods: int = game_box_score.get("regPeriods")

    game_landing: dict[str: Any] = load_game_landing(game_id)
    away_shots_on_goal: int = game_landing.get("awayTeam", {}).get("sog", 0)
    home_shots_on_goal: int = game_landing.get("homeTeam", {}).get("sog", 0)

    game_start_time_atl = datetime.datetime.strptime(game_start_time_utc, "%Y-%m-%dT%H:%M:%SZ")
    game_start_time_atl = game_start_time_atl.replace(tzinfo=pytz.UTC)
    game_start_time_atl = game_start_time_atl.astimezone(tz)
    # st.write(f"{game_start_time_atl}, {game_start_time_atl.tzinfo=}")

    key_toggle: str = f"toggle_show_game_{game_id}"
    key_toggle_scoring: str = f"toggle_show_game_{game_id}_s"
    key_toggle_penalties: str = f"toggle_show_game_{game_id}_p"
    show_game: bool = st.session_state.get(key_toggle)
    show_game_scoring: bool = st.session_state.get(key_toggle_scoring)
    show_game_penalties: bool = st.session_state.get(key_toggle_penalties)

    game_state_fmt: str = game_state_translate(bs_game_state)
    if show_game and (game_state_fmt != game_state_translate("FUT")):
        if game_state_translate(bs_game_state) != "FINAL":
            game_state_fmt += f" {seconds_to_clock(bs_game_clock_seconds_remaining)}"
            if bs_game_clock_running:
                game_state_fmt += f" {E_html_STOPPAGE}"
            else:
                game_state_fmt += f" {E_html_PLAYING}"
            game_state_fmt += f" {bs_game_clock_time_remaining}"
            game_state_fmt += f" {bs_game_period_num}{number_suffix(bs_game_period_num)}"
            if bs_game_clock_in_intermission:
                game_state_fmt += f" intermission"
            else:
                game_state_fmt += f" period"
        else:
            game_state_fmt += f" - {bs_game_period_type}"
        #     game_state_fmt += f" {E_strl_RUNNING}"
    elif game_state_fmt == game_state_translate("FUT"):
        starts_in_h, starts_in_m = divmod((game_start_time_atl - now).total_seconds(), 3600)
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

    print(f"{away_team_name_abbrev} @ {home_team_name_abbrev}")
    # colour_bg_div1: Colour = team_colour(away_team_id, "bg")
    # colour_bg_div2: Colour = team_colour(home_team_id, "bg")

    html = f"<div id='div0', style='background-color: {colour_bg_div0.hex_code};'>"
    html += f"<H5>{game_state_fmt}</H5>"
    html += game_team_card(game_data, game_box_score, game_landing, away_team_id)
    # html += f"<div id='div1', style='background-color: {colour_bg_div1.hex_code}'>"
    # html += f"<img src='{away_team_logo}', alt='{away_team_name_abbrev}', width='{width_image_logo}', height='{width_image_logo}'>"
    # html += f"</div>"

    # html += f"<div id='div2', style='background-color: {colour_bg_div2.hex_code}'>"
    # html += f"<img src='{home_team_logo}', alt='{home_team_name_abbrev}', width='{width_image_logo}', height='{width_image_logo}'>"
    # html += f"</div>"
    html += game_team_card(game_data, game_box_score, game_landing, home_team_id)
    html += f"</div>"

    scoring: list[dict[str: Any]] = game_landing.get("summary", {}).get("scoring", [])
    penalties: list[dict[str: Any]] = game_landing.get("summary", {}).get("penalties", [])
    # print(f"{scoring=}")
    if show_game_scoring:
        html_s: str = f"<div>"
        html_s += aligned_text(
            f"Scoring:",
            "h3",
            font_size=font_size,
            h_align="left"
        )
        for i, period_data in enumerate(scoring):
            # print(f"{i=}, {period_data=}")
            html_s += f"<div id='G_{game_id}_{i}'>"
            html_s += aligned_text(
                f"{i+1}{number_suffix(i+1)} period",
                "h3",
                font_size=font_size
            )
            for j, goal_data in enumerate(scoring[i].get("goals", [])):
                # print(f"{j=}")

                strength: str = goal_data.get("strength")
                scorer_player_id: int = goal_data.get("playerID")
                scorer_player_name_first: str = goal_data.get("firstName", {}).get("default")
                scorer_player_name_last: str = goal_data.get("lastName", {}).get("default")
                scorer_player_name_short: str = goal_data.get("name", {}).get("default")
                scorer_team_name_short: str = goal_data.get("teamAbbrev", {}).get("default")
                scorer_head_shot: str = goal_data.get("headshot")
                scorer_highlight_clip: str = goal_data.get("highlightClipSharingUrl")
                scorer_goals_to_date: int = goal_data.get("goalsToDate", 0)
                curr_away_score: int = goal_data.get("awayScore", 0)
                curr_home_score: int = goal_data.get("homeScore", 0)
                leading_team_abbrev: str = goal_data.get("leadingTeamAbbrev")
                time_in_period: str = goal_data.get("timeInPeriod")
                shot_type: str = goal_data.get("shotType")
                goal_modifier: str = goal_data.get("goalModifier")
                goal_modifier_fmt: str = f", {goal_modifier}" if goal_modifier != "none" else ""
                df_team: pd.DataFrame = df_nhl_teams.loc[df_nhl_teams["ShortTeamName"] == scorer_team_name_short].reset_index()
                bg: Colour = Colour("#464646")
                fg: Colour = Colour("#FFFFFF")
                if not df_team.empty:
                    bg: Colour = team_colour(df_team["NHL_ID"].iloc[0], "bg")
                    fg: Colour = team_colour(df_team["NHL_ID"].iloc[0], "fg")
                assists: list[dict[str: Any]] = goal_data.get("assists", [])
                html_s += f"<div style='background-color: {bg.hex_code};'>"
                html_s += f"<img src='{scorer_head_shot}', alt='{scorer_player_name_short}', width='{width_image_logo}', height='{width_image_logo}'>"
                html_s += aligned_text(
                    f"{time_in_period} {scorer_player_name_short}({scorer_goals_to_date}), {curr_away_score}-{curr_home_score}, {strength}, {shot_type}{goal_modifier_fmt}, ",
                    "span",
                    font_size=font_size,
                    colour=fg.hex_code
                )
                for k, assist_data in enumerate(assists):
                    assist_player_id: int = assists[k]["playerId"]
                    assist_player_name_first: str = assists[k].get("firstName", {}).get("default")
                    assist_player_name_first: str = assists[k].get("lastName", {}).get("default")
                    assist_player_name_short: str = assists[k].get("lastName", {}).get("default")
                    assist_player_assists_to_date: int = assists[k].get("assistsToDate", 0)
                    html_s += aligned_text(
                        (", " * (1 if k > 0 else 0)) + f"{assist_player_name_short}({assist_player_assists_to_date})",
                        "span",
                        font_size=font_size,
                        colour=fg.hex_code
                    )
                if not assists:
                    html_s += aligned_text(
                        f"Un-assisted",
                        "span",
                        font_size=font_size,
                        colour=fg.hex_code
                    )
                html_s += "</div>"
            if not scoring[i].get("goals", []):
                html_s += aligned_text(
                    f"None",
                    "h3",
                    font_size=font_size
                )

            html_s += "</div>"
        html_s += "</div>"
        html += f"<br>{html_s}"

    if show_game_penalties:

        html_p: str = f"<div>"
        html_p += aligned_text(
            f"Penalties:",
            "h3",
            font_size=font_size,
            h_align="left"
        )
        for i, period_data in enumerate(penalties):
            html_p += f"<div id='G_{game_id}_{i}'>"
            html_p += aligned_text(
                f"{i+1}{number_suffix(i+1)} period",
                "h3",
                font_size=font_size
            )
            for j, penalty_data in enumerate(penalties[i].get("penalties", [])):
                p_time_in_period: str = penalty_data.get("timeInPeriod")
                p_type: str = penalty_data.get("type")
                p_duration: int = penalty_data.get("duration", 2)
                p_committed_by_player: str = penalty_data.get("committedByPlayer", "None")
                p_team_abbrev: str = penalty_data.get("teamAbbrev", {}).get("default")
                p_drawn_by: str = penalty_data.get("drawnBy", "None")
                p_desc_key: str = penalty_data.get("descKey")
                df_team: pd.DataFrame = df_nhl_teams.loc[
                    df_nhl_teams["ShortTeamName"] == p_team_abbrev].reset_index()
                bg: Colour = Colour("#464646")
                fg: Colour = Colour("#FFFFFF")
                if not df_team.empty:
                    bg: Colour = team_colour(df_team["NHL_ID"].iloc[0], "bg")
                    fg: Colour = team_colour(df_team["NHL_ID"].iloc[0], "fg")
                html_p += f"<div style='background-color: {bg.hex_code};'>"
                p_txt1: str = f" {p_committed_by_player}"
                p_txt2: str = f"{p_desc_key} on {p_drawn_by}"
                if p_desc_key == "fighting":
                    p_txt2 = f"{p_desc_key} with {p_drawn_by}"
                elif p_drawn_by == "None":
                    p_txt2 = f"{p_desc_key}"

                if p_committed_by_player == "None":
                    p_txt1 = f""

                html_p += aligned_text(
                    f"{p_time_in_period} {p_team_abbrev}{p_txt1} {p_duration} min {p_txt2}",
                    "h3",
                    font_size=font_size,
                    colour=fg.hex_code
                )
                html_p += "</div>"
            if not penalties[i].get("penalties", []):
                html_p += aligned_text(
                    f"None",
                    "h3",
                    font_size=font_size
                )

        html_p += "</div>"
        html += f"<br>{html_p}"

    html += f"</div>"

    # st.write(html)
    return html


def show_goal(str_id: str):
    print(f"SG {str_id}")
    # rain(
    #     emoji=E_strl_RUNNING,
    #     font_size=54,
    #     falling_speed=5,
    #     animation_length=5,
    # )
    st.session_state.update({str_id: True})


def change_show_toggle(game_id, val: Optional[bool] = None):
    print(f"change_show_toggle({game_id}, {val})")
    key_toggle: str = f"toggle_show_game_{game_id}"
    key_toggle_scoring: str = f"toggle_show_game_{game_id}_s"
    key_toggle_penalties: str = f"toggle_show_game_{game_id}_p"

    if not st.session_state.get(key_toggle) or (isinstance(val, bool) and not val):
        st.session_state.update({
            key_toggle_scoring: False,
            key_toggle_penalties: False
        })
    if val is not None:
        st.session_state.update({key_toggle: val})


def change_toggle_show_all():
    show_all: bool = st.session_state.get("toggle_show_all_games")
    print(f"change_toggle_show_all {show_all=}")
    if not show_all:
        for game_id in st.session_state.get("affected_games", {}).get(date_in, []):
            change_show_toggle(game_id, False)
        # st.rerun()


font_size: int = 24

# tz: pytz.timezone = pytz.timezone("Canada/Atlantic") # "-04:14" ..? wtf
tz: pytz.timezone = dateutil.tz.gettz("Canada/Atlantic")
now: datetime.datetime = datetime.datetime.now().replace(tzinfo=tz)
today: datetime.date = (now + datetime.timedelta(seconds=TIMEZONE_OFFSET)).date()
yesterday: datetime.date = (now + datetime.timedelta(seconds=TIMEZONE_OFFSET) + datetime.timedelta(days=-1)).date()
st.write(f"as of :red[{now}]")

json_scoreboard = load_scoreboard()
json_standings = load_standings()
excel_team_data: dict[str: pd.DataFrame] = load_team_excel()
df_nhl_teams: pd.DataFrame = excel_team_data["NHLTeams"]
df_nhl_confs: pd.DataFrame = excel_team_data["Conferences"]
df_nhl_divs: pd.DataFrame = excel_team_data["Divisions"]
standings_indexer: dict[str: int] = {s_dat.get("teamAbbrev", {}).get("default"): i for i, s_dat in enumerate(json_standings.get("standings", []))}
# class_scoreboard = Dict2Class(json_scoreboard)

# st.write(class_scoreboard.__dict__)


# st.write(today)
date_in = st.date_input(
    "Date",
    key="date_input",
    label_visibility="hidden"
)

toggle_show_all = st.toggle(
    label="Show All:",
    key="toggle_show_all_games",
    on_change=change_toggle_show_all
)

# st.write(f"today= {today}")
# st.write(f"date_in= {date_in}")

games_key: str = "gamesByDate"
game_date_key: str = "date"
days_this_week: list[dict] = json_scoreboard.get(games_key, [])
# st.write("days_this_week BEGIN")
# st.write(days_this_week)
week_dates_in: list[datetime.date] = [datetime.datetime.strptime(wgd.get(game_date_key), "%Y-%m-%d").date() for wgd in days_this_week]
if date_in not in week_dates_in:
    json_scoreboard = load_scoreboard(f"{date_in:%Y-%m-%d}")
    # st.write("json_scoreboard BEGIN AGAIN")
    # st.write(json_scoreboard)
    games_key = "games"
    game_date_key = "gameDate"
    days_this_week: list[dict] = [{
        "games": json_scoreboard[games_key],
        game_date_key: json_scoreboard["currentDate"]
    }]
    # st.write("days_this_week")
    # st.write(days_this_week)
    # # week_dates_in: list[datetime.date] = [
    # #     datetime.datetime.strptime(
    # #         wgd.get(game_date_key),
    # #         "%Y-%m-%d"
    # #     ).date() for wgd in days_this_week
    # # ]
    # # # days_this_week = [days_this_week]

# st.write(days_this_week)
# st.write("days_this_week FINAL")
# st.write(json_scoreboard)
# # grid = {
# #     "content_0": st.columns(len(days_this_week))
# # }

for i, week_game_data in enumerate(days_this_week):

    week_date: datetime.date = datetime.datetime.strptime(week_game_data.get(game_date_key), "%Y-%m-%d").date()
    # if week_date != yesterday:
    # if week_date != today:
    if week_date != date_in:
        # print(f"SKIP {week_date=}, {yesterday=}, {today=}")
        # st.write(f"SKIP {week_date=}, {yesterday=}, {today=}")
        continue

    # with grid["content_0"][i]:
    st.write(f"{i=}, week_date => {week_date}")
    # if i == 0:
    #     st.write("week_game_date")
    #     st.write(week_game_data)

    for j, game_data in enumerate(week_game_data.get("games", [])):
        game_id: int = game_data.get("id")
        if date_in not in st.session_state.get("affected_games"):
            st.session_state["affected_games"].update({date_in: []})
        if game_id not in st.session_state["affected_games"][date_in]:
            st.session_state["affected_games"][date_in].append(game_id)
        game_season: int = game_data.get("season")
        game_type: int = game_data.get("gameType")
        game_date: str = game_data.get("gameDate")
        game_center_link: str = game_data.get("gameCenterLink")
        game_venue: str = game_data.get("venue", {}).get("default")
        game_start_time_utc: str = game_data.get("startTimeUTC")
        game_eastern_utc_offset: str = game_data.get("easternUTCOffset")
        game_venue_utc_offset: str = game_data.get("venueUTCOffset")
        game_tv_broadcasts: list[dict[str: Any]] = game_data.get("tvBroadcasts")

        game_state: str = game_data.get("gameState")
        game_schedule_state: str = game_data.get("gameScheduleState")
        away_team_id: int = game_data.get("awayTeam", {}).get("id")
        away_team_name_full: str = game_data.get("awayTeam", {}).get("name", {}).get("default")
        away_team_name_fr: str = game_data.get("awayTeam", {}).get("name", {}).get("fr")
        away_team_name_short: str = game_data.get("awayTeam", {}).get("commonName", {}).get("default")
        away_team_place_name_prep: str = game_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get("default")
        away_team_place_name_prep_fr: str = game_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get("fr")
        away_team_name_abbrev: str = game_data.get("awayTeam", {}).get("abbrev")
        away_team_score: int = game_data.get("awayTeam", {}).get("score", 0)
        away_team_logo: str = game_data.get("awayTeam", {}).get("logo")

        home_team_id: int = game_data.get("homeTeam", {}).get("id")
        home_team_name_full: str = game_data.get("homeTeam", {}).get("name", {}).get("default")
        home_team_name_fr: str = game_data.get("homeTeam", {}).get("name", {}).get("fr")
        home_team_name_short: str = game_data.get("homeTeam", {}).get("commonName", {}).get("default")
        home_team_place_name_prep: str = game_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get("default")
        home_team_place_name_prep_fr: str = game_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get("fr")
        home_team_name_abbrev: str = game_data.get("homeTeam", {}).get("abbrev")
        home_team_score: int = game_data.get("homeTeam", {}).get("score", 0)
        home_team_logo: str = game_data.get("homeTeam", {}).get("logo")

        game_tickets_link: str = game_data.get("ticketsLink")
        game_tickets_link_fr: str = game_data.get("ticketsLinkFr")
        game_period: int = game_data.get("period", 1)
        game_period_desc_number: int = game_data.get("periodDescriptor", {}).get("number", 1)
        game_period_desc_type: str = game_data.get("periodDescriptor", {}).get("periodType")
        game_period_desc_max_reg_periods: int = game_data.get("periodDescriptor", {}).get("maxRegulationPeriods", 3)
        game_three_min_recap: str = game_data.get("threeMinRecap")
        game_three_min_recap_fr: str = game_data.get("threeMinRecapFr")

        key_toggle: str = f"toggle_show_game_{game_id}"
        key_toggle_scoring: str = f"toggle_show_game_{game_id}_s"
        key_toggle_penalties: str = f"toggle_show_game_{game_id}_p"
        key_away_goal_score: str = f"{game_id}_{away_team_id}_score"
        key_home_goal_score: str = f"{game_id}_{home_team_id}_score"
        key_away_goal_shown: str = f"{game_id}_{away_team_id}_shown"
        key_home_goal_shown: str = f"{game_id}_{home_team_id}_shown"
        if st.session_state.get("toggle_show_all_games", False):
            st.write(f"SHOW ALL {game_id=}")
            st.session_state.update({key_toggle: True})
        show_game: bool = st.session_state.get(key_toggle)

        old_away_score: int = st.session_state.setdefault(key_away_goal_score, 0)
        old_home_score: int = st.session_state.setdefault(key_home_goal_score, 0)
        if old_away_score != away_team_score:
            st.write(f"{away_team_name_abbrev} GOAL! {away_team_name_abbrev} {old_away_score}-{old_home_score} => {away_team_score}-{home_team_score} {home_team_name_abbrev}")
            # st.session_state.set
            show_goal(key_away_goal_shown)
            st.session_state.update({key_away_goal_score: away_team_score})
        if old_home_score != home_team_score:
            st.write(f"{home_team_name_abbrev} GOAL! {away_team_name_abbrev} {old_away_score}-{old_home_score} => {away_team_score}-{home_team_score} {home_team_name_abbrev}")
            # st.session_state.set
            show_goal(key_home_goal_shown)
            st.session_state.update({key_home_goal_score: home_team_score})

        # with grid["content_0"][i]:
        # show_cols = st.columns([0.05, 0.125, 0.1, 0.025, 0.125, 0.125, 0.45])

        cols_row_0 = st.columns([0.05, 0.95], vertical_alignment="center")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)
        # with cols_row_0[0]:
        #     st.write(f"{game_state=}")
        # with cols_row_0[1]:
        #     st.write(f"{game_period_desc_number=} {game_period_desc_type=}")
        with cols_row_0[0]:
            st.toggle(
                label=f"Show",
                key=key_toggle,
                label_visibility="hidden",
                on_change=lambda gi=game_id: change_show_toggle(gi)
            )

            if st.session_state.get(key_toggle):
                toggle_324 = st.toggle(
                    label=f"Scoring",
                    key=key_toggle_scoring
                    # ,
                    # label_visibility="hidden"
                )
                st.toggle(
                    label=f"Penalties",
                    key=key_toggle_penalties
                    # ,
                    # label_visibility="hidden"
                )

        # cols_row_1 = st.columns([0.15, 0.15, 0.55, 0.15], vertical_alignment="center")
        # with cols_row_1[0]:
        #     st.image(
        #         image=away_team_logo,
        #         width=width_image_logo
        #     )
        # with cols_row_1[1]:
        #     st.write(f"{away_team_name_short}")
        #     st.write(f"{{SOG}} {{PP_STATUS}}")
        #
        # with cols_row_1[3]:
        #     if show_game:
        #         st.write(f"{away_team_score}")
        #     else:
        #         st.write(f"?")
        #
        # cols_row_2 = st.columns([0.15, 0.15, 0.55, 0.15], vertical_alignment="center")
        # with cols_row_2[0]:
        #     st.image(
        #         image=home_team_logo,
        #         width=width_image_logo
        #     )
        # with cols_row_2[1]:
        #     st.write(f"{home_team_name_short}")
        #     st.write(f"{{SOG}} {{PP_STATUS}}")
        #
        # with cols_row_2[3]:
        #     if show_game:
        #         st.write(f"{home_team_score}")
        #     else:
        #         st.write(f"?")

        with cols_row_0[1]:
            st.markdown(game_card(game_data), unsafe_allow_html=True)

        # with show_cols[0]:
        #     st.toggle(
        #         label=f"Show",
        #         key=key_toggle,
        #         label_visibility="hidden"
        #     )
        # with show_cols[2]:
        #     st.image(
        #         image=away_team_logo
        #         # ,
        #         # caption=away_team_name_full
        #         ,
        #         width=width_image_logo
        #     )
        # with show_cols[4]:
        #     # st.write(aligned_text("@", h_align="right", line_height=0.05, font_size=12))
        #     st.markdown(aligned_text("@", h_align="right", line_height=0.05, font_size=12), unsafe_allow_html=True)
        # with show_cols[5]:
        #     st.image(
        #         image=home_team_logo
        #         # ,
        #         # caption=home_team_name_full
        #         ,
        #         width=width_image_logo
        #     )
    if not week_game_data.get("games", []):
        st.markdown(
            aligned_text(
                "No Games",
                font_size=font_size
            ),
            unsafe_allow_html=True
        )


conference_cols = st.columns(2, vertical_alignment="center")
division_cols = st.columns(4, vertical_alignment="center")
standings = json_standings.get("standings", [])
list_divs: list[str] = ["P", "C", "M", "A"]
standings_by_div = {d: sorted([team_data for team_data in standings if team_data.get("divisionAbbrev") == d], key=lambda data: data.get("leagueSequencer", 0), reverse=False) for d in list_divs}
#standings_atl = sorted([team_data for team_data in standings if team_data.get("divisionAbbrev") == "A"], key=lambda data: data.get("points", 0), reverse=True)
#standings_met = sorted([team_data for team_data in standings if team_data.get("divisionAbbrev") == "M"], key=lambda data: data.get("points", 0), reverse=True)
#standings_cen = sorted([team_data for team_data in standings if team_data.get("divisionAbbrev") == "C"], key=lambda data: data.get("points", 0), reverse=True)
#standings_pac = sorted([team_data for team_data in standings if team_data.get("divisionAbbrev") == "P"], key=lambda data: data.get("points", 0), reverse=True)
tops = [standings_by_div["P"][0], standings_by_div["C"][0], standings_by_div["M"][0], standings_by_div["A"][0]]
# tops.sort(key=lambda data: data.get("points", 0), reverse=True)
top_conf = standings[0].get("conferenceAbbrev")
top_div = standings[0].get("divisionAbbrev")
st.write(standings[0])
div_order = [top_div]
if top_conf == "E":
    div_order.append("A" if top_div == "M" else "M")
    div_order.extend(["C", "P"] if standings_by_div["C"][0].get("leagueSequence") < standings_by_div["P"][0].get("leagueSequence") else ["P", "C"])
else:
    div_order.append("C" if top_div == "P" else "P")
    div_order.extend(["A", "M"] if standings_by_div["A"][0].get("leagueSequence") < standings_by_div["M"][0].get("leagueSequence") else ["M", "A"])
   
# st.write(div_order)
tops.sort(key=lambda data: div_order.index(data.get("divisionAbbrev")))

for i, top in enumerate(tops):
    conf_name: str = tops[i].get('conferenceName')
    div_name: str = tops[i].get('divisionName')
    conf: str = tops[i].get('conferenceAbbrev')
    div: str = tops[i].get('divisionAbbrev')
    if i % 2 == 0:
        with conference_cols[i // 2]:
            # st.write(f"{tops[i].get('conferenceName')}")
            st.markdown(aligned_text(
                    f"{conf_name}"
                ),
                unsafe_allow_html=True
            )
    with division_cols[i]:
        #st.write(f"{tops[i].get('divisionName')}")
        st.markdown(aligned_text(
                f"{div_name}"
            ),
            unsafe_allow_html=True
        )
        
        for j, team_data in enumerate(standings_by_div[div]):
            # name_short: str = team_data.get('teamAbbrev', {}).get('default')
            # team_logo: str = team_data.get("teamLogo")
            # team_points: int = team_data.get("points")
            # # st.write(f"{name_short}")
            # # st.write(f"{team_logo}")
            # #if team_logo:
            # #    st.image(team_logo, width=40)
            # df_team: pd.DataFrame = df_nhl_teams.loc[df_nhl_teams["ShortTeamName"] == name_short].reset_index()
            # team_id: int = -1
            # if not df_team.empty:
            #     df_team: pd.DataFrame = df_team.iloc[0]
            #     team_id = df_team["NHL_ID"]
            #
            # fg: Colour = team_colour(team_id, "fg")
            # bg: Colour = team_colour(team_id, "bg")
            #
            # html = ""
            # html += f"<div id='team_{team_id}', style='background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"
            # html += aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size)
            # # html += aligned_text(score, tag_style="span", colour=fg.hex_code, font_size=font_size)
            # html += f"<img src='{team_logo}', alt='{name_short}', width='{width_image_logo}', height='{width_image_logo}'>"
            # html += aligned_text(name_short, tag_style="span", colour=fg.hex_code, font_size=font_size)
            # # html += f" " + aligned_text(team_record, tag_style="span", colour=fg.hex_code, font_size=font_size)
            # # if show_game:
            # #     html += aligned_text(f" SOG: {bs_shots_on_goal}", tag_style="span", colour=fg.hex_code, font_size=font_size)
            # html += f"</div>"
            html = team_info_card(team_data)
            st.markdown(html, unsafe_allow_html=True)
            if j == 2:
                st.markdown("---")
     
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(aligned_text(f"Playoff Bracket {now:%Y-%m-%d}", font_size=font_size), unsafe_allow_html=True)

#top_west = sorted(standings_by_div["P"] + standings_by_div["C"], key=lambda t_data: t_data.get("conferenceSequence"))[:8]
#top_east = sorted(standings_by_div["M"] + standings_by_div["A"], key=lambda t_data: t_data.get("conferenceSequence"))[:8]
#second_wc_west = top_west.pop(-1)
#second_wc_east = top_east.pop(-1)
#top_west.insert(0, second_wc_west)
#top_east.insert(0, second_wc_east)
#teams_l, teams_r = [top_west, top_east] if top_conf == "W" else [top_east, top_west]
top_l = standings_by_div[div_order[0]][:3] + standings_by_div[div_order[1]][:3][::-1]
top_r = standings_by_div[div_order[2]][:3] + standings_by_div[div_order[3]][:3][::-1]
bottom_l = sorted([*standings_by_div[div_order[0]][3:5], *standings_by_div[div_order[1]][3:5]], key=lambda t_data: t_data.get("conferenceSequence"))[:2]
bottom_r = sorted([*standings_by_div[div_order[2]][3:5], *standings_by_div[div_order[3]][3:5]], key=lambda t_data: t_data.get("conferenceSequence"))[:2]
# teams_l = bottom_l[-1:] + top_l + 
teams_l = bottom_l[-1:] + top_l + bottom_l[:1]
teams_r = bottom_r[-1:] + top_r + bottom_r[:1]

w = """
st.write(top_l)
st.write(top_r)
st.write(bottom_l)
st.write(bottom_r)
st.write(teams_l)
st.write(teams_r)
"""


po_grid = [st.columns(12) for _ in range(9)]

with po_grid[0][0]:
    st.markdown(aligned_text(f"{top_conf}"), unsafe_allow_html=True)
with po_grid[0][-1]:
    st.markdown(aligned_text(f"{'E' if top_conf == 'W' else 'W'}"), unsafe_allow_html=True)
    
for i in range(1, 9):
    with po_grid[i][0]:
        st.markdown(aligned_text(f"{i}"), unsafe_allow_html=True)
    with po_grid[i][-1]:
        st.markdown(aligned_text(f"{i}"), unsafe_allow_html=True)
        

# wewwe = """
# <script>
#     function sendToStreamlit(buttonId) {
#         // Post the buttonId to Streamlit
#         console.log(buttonId)
#         //window.parent.postMessage(
#         //    {isStreamlitMessage: true, type: "streamlit:setState", key: "clicked_button", value: buttonId},
#         //    "*"
#         //);
#     }
#     //function sendToStreamlit(buttonId) {
#     //    // Set the query parameter to communicate with Streamlit
#     //    const currentUrl = new URL(window.location.href);
#     //    currentUrl.searchParams.set('clicked_button', buttonId);
#     //    window.location.href = currentUrl; // Reload the page with updated query params
#     //    console.log(buttonId)
#     //}
# </script>
# """
#
# components.html("""
# <script>
#     function sendToStreamlit(buttonId) {
#         // Post the buttonId to Streamlit
#         console.log('Button clicked:', buttonId);
#         //window.parent.postMessage(
#         //    {isStreamlitMessage: true, type: "streamlit:setState", key: "clicked_button", value: buttonId},
#         //    "*"
#         //);
#     }
#     //function sendToStreamlit(buttonId) {
#     //    // Set the query parameter to communicate with Streamlit
#     //    const currentUrl = new URL(window.location.href);
#     //    currentUrl.searchParams.set('clicked_button', buttonId);
#     //    window.location.href = currentUrl; // Reload the page with updated query params
#     //    console.log(buttonId)
#     //}
# </script>
# """)

# components.html("""
# <script>
#     function sendToStreamlit(buttonId) {
#         // Post the buttonId to Streamlit
#         console.log('Button clicked:', buttonId);
# }
# </script>
# """)

clicked = {}
for i in range(1, 9):
    j = 1
    # st.write(f"{i=} {j=}")
    with po_grid[i][1]:
        team_data = teams_l[i - 1]
        w = """
        name_short: str = team_data.get('teamAbbrev', {}).get('default')
        team_logo: str = team_data.get("teamLogo")
        team_points: int = team_data.get("points")
        # st.write(f"{name_short}")
        # st.write(f"{team_logo}")
        #if team_logo:
        #    st.image(team_logo, width=40)
        df_team: pd.DataFrame = df_nhl_teams.loc[df_nhl_teams["ShortTeamName"] == name_short].reset_index()
        team_id: int = -1
        if not df_team.empty:
            df_team: pd.DataFrame = df_team.iloc[0]
            team_id = df_team["NHL_ID"]
       
        fg: Colour = team_colour(team_id, "fg")
        bg: Colour = team_colour(team_id, "bg")
       
        html = ""
        html += f"<div id='team_{team_id}', style='background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"
        # html += aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size)
        # html += aligned_text(score, tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += f"<img src='{team_logo}', alt='{name_short}', width='{width_image_logo}', height='{width_image_logo}'>"
        html += aligned_text(name_short, tag_style="span", colour=fg.hex_code, font_size=font_size)
        # html += f" " + aligned_text(team_record, tag_style="span", colour=fg.hex_code, font_size=font_size)
        # if show_game:
        #     html += aligned_text(f" SOG: {bs_shots_on_goal}", tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += f"</div>"
        """
        html = team_info_card(team_data, show_points=False)
        # st.write(html)
        k_clicked = f"clicked_ps_{(i, j)}"
        is_clicked = st.session_state.get(k_clicked, False)
        if not is_clicked:
            clicked[(i, j)] = click_detector(html, key=f"({i}, {j})")
        else:
            st.markdown(html, unsafe_allow_html=True)
            clicked[(i, j)] = "1"
        # st.markdown(html, unsafe_allow_html=True)

    j = len(po_grid[0]) - 2
    # st.write(f"{i=} {j=}")
    with po_grid[i][-2]:
        team_data = teams_r[i - 1]
        w = """
        name_short: str = team_data.get('teamAbbrev', {}).get('default')
        team_logo: str = team_data.get("teamLogo")
        team_points: int = team_data.get("points")
        # st.write(f"{name_short}")
        # st.write(f"{team_logo}")
        #if team_logo:
        #    st.image(team_logo, width=40)
        df_team: pd.DataFrame = df_nhl_teams.loc[df_nhl_teams["ShortTeamName"] == name_short].reset_index()
        team_id: int = -1
        if not df_team.empty:
            df_team: pd.DataFrame = df_team.iloc[0]
            team_id = df_team["NHL_ID"]

        fg: Colour = team_colour(team_id, "fg")
        bg: Colour = team_colour(team_id, "bg")

        html = ""
        html += f"<div id='team_{team_id}', style='background-color: {bg.hex_code}; foreground-color: {fg.hex_code}'>"
        # html += aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size)
        # html += aligned_text(score, tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += aligned_text(name_short, tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += f"<img src='{team_logo}', alt='{name_short}', width='{width_image_logo}', height='{width_image_logo}'>"
        # html += f" " + aligned_text(team_record, tag_style="span", colour=fg.hex_code, font_size=font_size)
        # if show_game:
        #     html += aligned_text(f" SOG: {bs_shots_on_goal}", tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += f"</div>"
        """
        html = team_info_card(team_data, left_to_right=False, show_points=False)
        # if i == 1:
        #     st.write(html)
        k_clicked = f"clicked_ps_{(i, j)}"
        is_clicked = st.session_state.get(k_clicked, False)
        if not is_clicked:
            clicked[(i, j)] = click_detector(html, key=f"({i}, {j})")
        else:
            st.markdown(html, unsafe_allow_html=True)
            clicked[(i, j)] = "1"
        # st.markdown(html, unsafe_allow_html=True)


for i in range(1, 9, 2):
    j = 2
    # st.write(f"{i=} {j=}")
    with po_grid[i + 1][j]:
        team_data_0 = teams_l[i - 1]
        team_data_1 = teams_l[i]

        k0 = i, j - 1
        k1 = i + 1, j - 1
        k_0 = f"clicked_ps_{k0}"
        k_1 = f"clicked_ps_{k1}"
        clicked_0 = clicked[k0] not in ("", "1")
        clicked_1 = clicked[k1] not in ("", "1")
        clicked_0_prev = clicked[k0] == "1"
        clicked_1_prev = clicked[k1] == "1"
        # clicked_0_prev = st.session_state.get(k_0, False)
        # clicked_1_prev = st.session_state.get(k_1, False)
        # if clicked_0_prev and clicked_1_prev:
        #     # only 1 can be on
        #     clicked[k1] = ""
        #     clicked_1_prev = False
        #     st.session_state.update({k_1: False})
        # else:
        #     if clicked_0_prev:
        #         st.session_state.update({})

        w = """
        name_short_0: str = team_data_0.get('teamAbbrev', {}).get('default')
        team_logo_0: str = team_data_0.get("teamLogo")
        team_points_0: int = team_data_0.get("points")
        # st.write(f"{name_short}")
        # st.write(f"{team_logo}")
        #if team_logo:
        #    st.image(team_logo, width=40)
        df_team_0: pd.DataFrame = df_nhl_teams.loc[df_nhl_teams["ShortTeamName"] == name_short_0].reset_index()
        team_id_0: int = -1
        if not df_team_0.empty:
            df_team_0: pd.DataFrame = df_team_0.iloc[0]
            team_id_0 = df_team_0["NHL_ID"]

        fg_0: Colour = team_colour(team_id_0, "fg")
        bg_0: Colour = team_colour(team_id_0, "bg")

        html = ""
        html += f"<div id='team_{team_id_0}', style='background-color: {bg_0.hex_code}; foreground-color: {fg_0.hex_code}'>"
        # html += aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size)
        # html += aligned_text(score, tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += aligned_text(name_short_0, tag_style="span", colour=fg_0.hex_code, font_size=font_size)
        html += f"<img src='{team_logo_0}', alt='{name_short_0}', width='{width_image_logo}', height='{width_image_logo}'>"
        # html += f" " + aligned_text(team_record, tag_style="span", colour=fg.hex_code, font_size=font_size)
        # if show_game:
        #     html += aligned_text(f" SOG: {bs_shots_on_goal}", tag_style="span", colour=fg.hex_code, font_size=font_size)
        #html += f"</div>"

        name_short_1: str = team_data_1.get('teamAbbrev', {}).get('default')
        team_logo_1: str = team_data_1.get("teamLogo")
        team_points_1: int = team_data_1.get("points")
        # st.write(f"{name_short}")
        # st.write(f"{team_logo}")
        #if team_logo:
        #    st.image(team_logo, width=40)
        df_team_1: pd.DataFrame = df_nhl_teams.loc[df_nhl_teams["ShortTeamName"] == name_short_1].reset_index()
        team_id_1: int = -1
        if not df_team_1.empty:
            df_team_1: pd.DataFrame = df_team_1.iloc[0]
            team_id_1 = df_team_1["NHL_ID"]

        fg_1: Colour = team_colour(team_id_1, "fg")
        bg_1: Colour = team_colour(team_id_1, "bg")

        #html += f"<div id='team_{team_id_0}', style='background-color: {bg_0.hex_code}; foreground-color: {fg_0.hex_code}'>"
        # html += aligned_text(team_points, tag_style="span", colour=fg.hex_code, font_size=font_size)
        # html += aligned_text(score, tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += aligned_text(name_short_1, tag_style="span", colour=fg_1.hex_code, font_size=font_size)
        html += f"<img src='{team_logo_1}', alt='{name_short_1}', width='{width_image_logo}', height='{width_image_logo}'>"
        # html += f" " + aligned_text(team_record, tag_style="span", colour=fg.hex_code, font_size=font_size)
        # if show_game:
        #     html += aligned_text(f" SOG: {bs_shots_on_goal}", tag_style="span", colour=fg.hex_code, font_size=font_size)
        html += f"</div>"
        """

        if not clicked_0 and not clicked_1:
            if not clicked_0_prev and not clicked_1_prev:
                st.markdown(f"{team_data_0.get('teamAbbrev', {}).get('default')} vs {team_data_1.get('teamAbbrev', {}).get('default')}")
            elif clicked_0_prev:
                st.markdown(team_info_card(team_data_0), unsafe_allow_html=True)
                st.session_state.update({k_1: False})
            else:
                st.markdown(team_info_card(team_data_1), unsafe_allow_html=True)
                st.session_state.update({k_0: False})
        elif clicked_0:
            st.markdown(team_info_card(team_data_0), unsafe_allow_html=True)
            st.session_state.update({k_1: False})
        else:
            st.markdown(team_info_card(team_data_1), unsafe_allow_html=True)
            st.session_state.update({k_0: False})


# st.write(list(clicked.keys()))
for k, clk in clicked.items():
    st.markdown(f"'{k}' clicked '{clk}'" if clk != "" else f"'{k}' No click '{clk}'")
    st.session_state.update({f"clicked_ps_{k}": clk != ""})


count = st_autorefresh(interval=TIME_APP_REFRESH, limit=None, key="ProductionOverview")

# content = """<p><a href='#' id='Link 1'>First link</a></p>
#     <p><a href='#' id='Link 2'>Second link</a></p>
#     <a href='#' id='Image 1'><img width='20%' src='https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=200'></a>
#     <a href='#' id='Image 2'><img width='20%' src='https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=200'></a>
#     """
# clicked = click_detector(content)
#
# st.markdown(f"**{clicked} clicked**" if clicked != "" else "**No click**")
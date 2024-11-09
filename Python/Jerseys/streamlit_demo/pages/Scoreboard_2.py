import datetime
from typing import Any, Literal

import requests
import streamlit as st

from colour_utility import Colour
from utility import number_suffix

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



# Hold times in seconds
SCOREBOARD_HOLD_TIME: float = 60 * 90
GAME_HOLD_TIME: float = 60 * 1.5
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
        font_size: int = 12
) -> str:
    """
    Return formatted HTML, and in-line CSS to h_align a given text in a container.
    Use with streamlit's markdown function and with 'unsafe_allow_html' set to True.
    See coloured_text() for streamlined-colour-only functionality.
    """
    if isinstance(line_height, float):
        line_height = f"{line_height}%"
    return f"<{tag_style} style='line-height: {line_height}; text-align: {h_align}; color: {colour}; font-size: {font_size}px'>{txt}</{tag_style}>"


st.set_page_config(layout="wide")
st.title("Scoreboard")


@st.cache_data(show_spinner=SHOW_SPINNERS, ttl=GAME_HOLD_TIME)
def load_game(game_id: int):
    # return requests.get(f"https://statsapi.web.nhl.com/api/v1/game/{game_id}/boxscore").json()
    print(f"New Game Data {game_id=}, {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    return requests.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore").json()


@st.cache_data(show_spinner=SHOW_SPINNERS, ttl=SCOREBOARD_HOLD_TIME)
def load_scoreboard():
    print(f"New Scoreboard data")
    return requests.get("https://api-web.nhle.com/v1/scoreboard/now").json()


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
    if p_sec == 0:
        # default show 1200
        return clocks[-2][1]
    # 24 segments
    p_sec: int = int(round(p_sec * len(clocks)))
    # print(f"sl={seconds_left}, ts={t_sec}, ps={p_sec}")
    return clocks[p_sec][1]


def game_state_translate(game_state: str) -> str:
    match game_state:
        case "FUT": return "Upcoming"
        case _: return game_state


def game_card(game_data: dict[str: Any]) -> str:

    colour_bg_div0: Colour = Colour("#424242")

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

    game_box_score: dict[str: Any] = load_game(game_id)
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

    bs_game_state: str = game_box_score.get("gameState")
    bs_game_schedule_state: str = game_box_score.get("gameScheduleState")
    bs_game_reg_periods: int = game_box_score.get("regPeriods")

    game_state_fmt: str = game_state_translate(bs_game_state)
    if game_state_fmt != game_state_translate("FUT"):
        game_state_fmt += f" {seconds_to_clock(bs_game_clock_seconds_remaining)}"
        if bs_game_clock_running:
            game_state_fmt += f" {E_html_STOPPAGE}"
        else:
            game_state_fmt += f" {E_html_PLAYING}"
        game_state_fmt += f" {bs_game_clock_time_remaining}"
        game_state_fmt += f" {game_period_desc_number}{number_suffix(game_period_desc_number)}"
        if bs_game_clock_in_intermission:
            game_state_fmt += f" intermission"
        else:
            game_state_fmt += f" period"
        #     game_state_fmt += f" {E_strl_RUNNING}"

    html = f"<div id='div0', style='background-color: {colour_bg_div0.hex_code};'>"
    html += f"<H5>{game_state_fmt}</H5>"
    html += f"<img src='{away_team_logo}', alt='{away_team_name_abbrev}', width='{width_image_logo}', height='{width_image_logo}'>"
    html += f"<img src='{home_team_logo}', alt='{home_team_name_abbrev}', width='{width_image_logo}', height='{width_image_logo}'>"
    html += f"</div>"
    return html


st.write(":streamlit:")

json_scoreboard = load_scoreboard()
# class_scoreboard = Dict2Class(json_scoreboard)

st.write(json_scoreboard)
# st.write(class_scoreboard.__dict__)

today: datetime.date = (datetime.datetime.now() + datetime.timedelta(seconds=TIMEZONE_OFFSET)).date()
yesterday: datetime.date = (datetime.datetime.now() + datetime.timedelta(seconds=TIMEZONE_OFFSET) + datetime.timedelta(days=-1)).date()

st.write(today)

days_this_week: list[dict] = json_scoreboard.get("gamesByDate", [])
# grid = {
#     "content_0": st.columns(len(days_this_week))
# }

for i, week_game_data in enumerate(days_this_week):

    week_date: datetime.date = datetime.datetime.strptime(week_game_data.get("date"), "%Y-%m-%d").date()
    # if week_date != yesterday:
    if week_date != today:
        # print(f"SKIP {week_date=}, {yesterday=}, {today=}")
        continue

    # with grid["content_0"][i]:
    st.write(week_date)

    for j, game_data in enumerate(week_game_data.get("games", [])):
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

        key_toggle: str = f"toggle_show_game_{game_id}"
        show_game: bool = st.session_state.get(key_toggle)

        # with grid["content_0"][i]:
        # show_cols = st.columns([0.05, 0.125, 0.1, 0.025, 0.125, 0.125, 0.45])

        cols_row_0 = st.columns([0.15, 0.45, 0.25, 0.15], vertical_alignment="center")
        with cols_row_0[0]:
            st.write(f"{game_state=}")
        with cols_row_0[1]:
            st.write(f"{game_period_desc_number=} {game_period_desc_type=}")
        with cols_row_0[3]:
            st.toggle(
                label=f"Show",
                key=key_toggle,
                label_visibility="hidden"
            )

        cols_row_1 = st.columns([0.15, 0.15, 0.55, 0.15], vertical_alignment="center")
        with cols_row_1[0]:
            st.image(
                image=away_team_logo,
                width=width_image_logo
            )
        with cols_row_1[1]:
            st.write(f"{away_team_name_short}")
            st.write(f"{{SOG}} {{PP_STATUS}}")

        with cols_row_1[3]:
            if show_game:
                st.write(f"{away_team_score}")
            else:
                st.write(f"?")

        cols_row_2 = st.columns([0.15, 0.15, 0.55, 0.15], vertical_alignment="center")
        with cols_row_2[0]:
            st.image(
                image=home_team_logo,
                width=width_image_logo
            )
        with cols_row_2[1]:
            st.write(f"{home_team_name_short}")
            st.write(f"{{SOG}} {{PP_STATUS}}")

        with cols_row_2[3]:
            if show_game:
                st.write(f"{home_team_score}")
            else:
                st.write(f"?")

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

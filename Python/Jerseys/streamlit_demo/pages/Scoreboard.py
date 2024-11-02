import datetime
from typing import Any, Literal

import requests
import streamlit as st

# from streamlit_demo.streamlit_utility import aligned_text
from utility import Dict2Class





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






SCOREBOARD_HOLD_TIME: int = 1000 * 90
SHOW_SPINNERS: bool = True
TIMEZONE_OFFSET = -60 * 60 * 4
width_image_logo: int = 42


st.set_page_config(layout="wide")
st.title("Scoreboard")


@st.cache_data(show_spinner=SHOW_SPINNERS, ttl=SCOREBOARD_HOLD_TIME)
def load_scoreboard():
    print(f"New Scoreboard data")
    return requests.get("https://api-web.nhle.com/v1/scoreboard/now").json()


json_scoreboard = load_scoreboard()
# class_scoreboard = Dict2Class(json_scoreboard)

st.write(json_scoreboard)
# st.write(class_scoreboard.__dict__)

today = (datetime.datetime.now() + datetime.timedelta(seconds=TIMEZONE_OFFSET)).date()

st.write(today)

days_this_week: list[dict] = json_scoreboard.get("gamesByDate", [])
grid = {
    "content_0": st.columns(len(days_this_week))
}

for i, week_game_data in enumerate(days_this_week):

    week_date = week_game_data.get("date")
    with grid["content_0"][i]:
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

        with grid["content_0"][i]:
            show_cols = st.columns([0.05, 0.125, 0.1, 0.025, 0.125, 0.125, 0.45])
            with show_cols[0]:
                st.toggle(
                    label=f"Show",
                    key=key_toggle,
                    label_visibility="hidden"
                )
            with show_cols[2]:
                st.image(
                    image=away_team_logo
                    # ,
                    # caption=away_team_name_full
                    ,
                    width=width_image_logo
                )
            with show_cols[4]:
                # st.write(aligned_text("@", h_align="right", line_height=0.05, font_size=12))
                st.markdown(aligned_text("@", h_align="right", line_height=0.05, font_size=12), unsafe_allow_html=True)
            with show_cols[5]:
                st.image(
                    image=home_team_logo
                    # ,
                    # caption=home_team_name_full
                    ,
                    width=width_image_logo
                )

            if st.session_state.get(key_toggle):
                st.write(f"{away_team_score} {home_team_score} {game_state}")

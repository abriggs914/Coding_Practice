import datetime
from typing import Any
import pandas as pd

from objects.team import NHLTeam
from utils.colour_utility import Colour
from utils.utility import utc_offset_to_seconds, number_suffix
from utils.utils import game_state_translate, seconds_to_clock
from utils.datetime_utility import date_str_format
from resources.resource import DATE_FMT, UTC_FMT, E_html_STOPPAGE, E_html_PLAYING


class NHLGameDate:
    def __init__(self, gd_date: dict):
        self.gd_date: dict = gd_date

        self.date: str = self.gd_date.get("date")
        self.date: datetime.date = datetime.datetime.strptime(self.date, DATE_FMT).date() if self.date else None
        self.dayAbbrev: str = self.gd_date.get("dayAbbrev")
        self.number_of_games: int = self.gd_date.get("numberOfGames", 0)
        self.date_promo: str = self.gd_date.get("datePromo")
        self.games: list[NHLBoxScore] = [NHLBoxScore(bx) for bx in self.gd_date.get("games", [])]


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
        self.away_team_data: dict = g_data.get("awayTeam", {})
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
        self.home_team_data: dict = g_data.get("homeTeam", {})
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

    def is_game_over(self) -> bool:
        return self.game_state.lower() == "off"

    def is_game_live(self) -> bool:
        return self.game_state.lower() == "live"

    def is_game_future(self) -> bool:
        return self.game_state.lower() == "fut"

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

    def short_repr(self):
        return f"{date_str_format(self.start_time_atl, include_time=True, include_weekday=True, short_weekday=True, short_month=True, short_time=True)} {self.away_team} @ {self.home_team}"

    def __repr__(self):
        return f"NHLGAME#{self.g_id} {self.start_time_atl:{UTC_FMT}} {self.away_team} @ {self.home_team}"


class NHLBoxScore(NHLGame):
    def __init__(self, bx_data: dict | pd.Series):
        super().__init__(bx_data)
        self.bx_data: dict = bx_data if isinstance(bx_data, dict) else bx_data.to_dict()
        self.g_id: int = self.bx_data.get("id")
        self.game_season: int = self.bx_data.get("season")
        self.game_type: int = self.bx_data.get("gameType")
        self.game_limited_scoring: bool = self.bx_data.get("limitedScoring")
        self.game_date: datetime.date = datetime.datetime.strptime(self.bx_data.get("gameDate"), DATE_FMT).date() if self.bx_data.get("gameDate") else (datetime.datetime.strptime(self.bx_data.get("start_time_atl"), DATE_FMT).date() if self.bx_data.get("start_time_atl") else None)
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
        self.game_away_team_place_name_prep: str = self.game_away_team.get("placeNameWithPreposition", {}).get(
            "default")
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
        self.game_home_team_place_name_prep: str = self.game_home_team.get("placeNameWithPreposition", {}).get(
            "default")
        self.game_home_team_place_name_prep_fr: str = self.game_home_team.get("placeNameWithPreposition", {}).get("fr")

        # re-key some items

        self.away_team: NHLTeam = None
        self.away_team_id: int = bx_data.get("awayTeam", {}).get("id")
        self.away_team_name_full: str = bx_data.get("awayTeam", {}).get("name", {}).get("default")
        self.away_team_name_fr: str = bx_data.get("awayTeam", {}).get("name", {}).get("fr")
        self.away_team_name_short: str = bx_data.get("awayTeam", {}).get("commonName", {}).get("default")
        self.away_team_place_name_prep: str = bx_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get(
            "default")
        self.away_team_place_name_prep_fr: str = bx_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get(
            "fr")
        self.away_team_name_abbrev: str = bx_data.get("awayTeam", {}).get("abbrev")
        self.away_team_score: int = bx_data.get("awayTeam", {}).get("score", 0)
        self.away_team_logo: str = bx_data.get("awayTeam", {}).get("logo")

        self.home_team: NHLTeam = None
        self.home_team_id: int = bx_data.get("homeTeam", {}).get("id")
        self.home_team_name_full: str = bx_data.get("homeTeam", {}).get("name", {}).get("default")
        self.home_team_name_fr: str = bx_data.get("homeTeam", {}).get("name", {}).get("fr")
        self.home_team_name_short: str = bx_data.get("homeTeam", {}).get("commonName", {}).get("default")
        self.home_team_place_name_prep: str = bx_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get(
            "default")
        self.home_team_place_name_prep_fr: str = bx_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get(
            "fr")
        self.home_team_name_abbrev: str = bx_data.get("homeTeam", {}).get("abbrev")
        self.home_team_score: int = bx_data.get("homeTeam", {}).get("score", 0)
        self.home_team_logo: str = bx_data.get("homeTeam", {}).get("logo")

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

    def is_game_over(self) -> bool:
        return self.game_state.lower() == "off"

    def is_game_live(self) -> bool:
        return self.game_state.lower() == "live"

    def is_game_future(self) -> bool:
        return self.game_state.lower() == "fut"

    def __repr__(self) -> str:
        if self.game_date is not None:
            return f"NHLBoxScore(ID={self.g_id}, date={self.game_date:%Y-%m-%d %H:%M:%S} {self.away_team} @ {self.home_team})"
        return f"NHLBoxScore(ID={self.g_id}, ({self.away_team_id}) {self.away_team_name_short} @ {self.home_team_name_short} ({self.home_team_id}))"


class NHLGameLanding:
    def __init__(self, l_data: dict | pd.Series):
        self.l_data = l_data.copy()
        self.g_id: int = self.l_data.get("id")
        self.game_season: int = self.l_data.get("season")
        self.game_type: int = self.l_data.get("gameType")
        self.game_limited_scoring: bool = self.l_data.get("limitedScoring")
        self.game_date: datetime.date = datetime.datetime.strptime(self.l_data.get("gameDate"),
                                                                   DATE_FMT).date() if self.l_data.get(
            "gameDate") else (
            datetime.datetime.strptime(self.l_data.get("start_time_atl"), DATE_FMT).date() if self.l_data.get(
                "start_time_atl") else None)
        self.game_venue: str = self.l_data.get("venue", {}).get("default")
        self.game_venue_fr: str = self.l_data.get("venue", {}).get("fr")
        self.game_venue_location: str = self.l_data.get("venueLocation", {}).get("default")
        self.game_venue_location_fr: str = self.l_data.get("venueLocation", {}).get("fr")
        self.game_start_time_utc: datetime.datetime = datetime.datetime.strptime(self.l_data.get("startTimeUTC"),
                                                                                 UTC_FMT)
        self.game_eastern_utc_offset: str = self.l_data.get("easternUTCOffset")
        self.game_eastern_utc_offset_sec: datetime.timedelta = datetime.timedelta(
            seconds=utc_offset_to_seconds(self.game_eastern_utc_offset))
        self.start_time_atl: datetime.datetime = (
                    self.game_start_time_utc + self.game_eastern_utc_offset_sec + datetime.timedelta(hours=1)).replace(
            minute=0, second=0, microsecond=0)
        self.game_venue_utc_offset: int = self.l_data.get("venueUTCOffset")
        self.game_broadcasts: list[dict[str: Any]] = self.l_data.get("tvBroadcasts", [])

        self.game_state: str = self.l_data.get("gameState")
        self.game_schedule_state: str = self.l_data.get("gameScheduleState")
        self.game_reg_periods: int = self.l_data.get("regPeriods")

        self.away_team: NHLTeam = None
        self.away_team_id: int = self.l_data.get("awayTeam", {}).get("id")
        self.away_team_name_full: str = self.l_data.get("awayTeam", {}).get("name", {}).get("default")
        self.away_team_name_fr: str = self.l_data.get("awayTeam", {}).get("name", {}).get("fr")
        self.away_team_name_short: str = self.l_data.get("awayTeam", {}).get("commonName", {}).get("default")
        self.away_team_place_name_prep: str = self.l_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get(
            "default")
        self.away_team_place_name_prep_fr: str = self.l_data.get("awayTeam", {}).get("placeNameWithPreposition", {}).get(
            "fr")
        self.away_team_name_abbrev: str = self.l_data.get("awayTeam", {}).get("abbrev")
        self.away_team_score: int = self.l_data.get("awayTeam", {}).get("score", 0)
        self.away_team_sog: int = self.l_data.get("awayTeam", {}).get("sog", 0)
        self.away_team_logo: str = self.l_data.get("awayTeam", {}).get("logo")
        self.away_team_radio_link: str = self.l_data.get("awayTeam", {}).get("radioLink")

        self.home_team: NHLTeam = None
        self.home_team_id: int = self.l_data.get("homeTeam", {}).get("id")
        self.home_team_name_full: str = self.l_data.get("homeTeam", {}).get("name", {}).get("default")
        self.home_team_name_fr: str = self.l_data.get("homeTeam", {}).get("name", {}).get("fr")
        self.home_team_name_short: str = self.l_data.get("homeTeam", {}).get("commonName", {}).get("default")
        self.home_team_place_name_prep: str = self.l_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get(
            "default")
        self.home_team_place_name_prep_fr: str = self.l_data.get("homeTeam", {}).get("placeNameWithPreposition", {}).get(
            "fr")
        self.home_team_name_abbrev: str = self.l_data.get("homeTeam", {}).get("abbrev")
        self.home_team_score: int = int(float(self.l_data.get("homeTeam", {}).get("score", 0)))
        self.home_team_sog: int = int(float(self.l_data.get("homeTeam", {}).get("sog", 0)))
        self.home_team_logo: str = self.l_data.get("homeTeam", {}).get("logo")
        self.home_team_radio_link: str = self.l_data.get("awayTeam", {}).get("radioLink")

        self.shoot_out_in_use: bool = self.l_data.get("shootoutInUse")
        self.max_periods: int = self.l_data.get("maxPeriods")
        self.reg_periods: int = self.l_data.get("regPeriods")
        self.ot_in_use: bool = self.l_data.get("otInUse")
        self.ties_in_use: bool = self.l_data.get("tiesInUse")

        self.summary: dict = self.l_data.get("summary", {})
        self.ice_surface: dict = self.summary.get("iceSurface", {})
        self.ice_surface_away_forwards: list = self.ice_surface.get("awayTeam", {}).get("forwards", [])
        self.ice_surface_away_defensemen: list = self.ice_surface.get("awayTeam", {}).get("defensemen", [])
        self.ice_surface_away_goalies: list = self.ice_surface.get("awayTeam", {}).get("goalies", [])
        self.ice_surface_away_penalty_box: list = self.ice_surface.get("awayTeam", {}).get("penaltyBox", [])
        self.ice_surface_home_forwards: list = self.ice_surface.get("homeTeam", {}).get("forwards", [])
        self.ice_surface_home_defensemen: list = self.ice_surface.get("homeTeam", {}).get("defensemen", [])
        self.ice_surface_home_goalies: list = self.ice_surface.get("homeTeam", {}).get("goalies", [])
        self.ice_surface_home_penalty_box: list = self.ice_surface.get("homeTeam", {}).get("penaltyBox", [])
        self.scoring: list = self.summary.get("scoring", [])
        self.penalties: list = self.summary.get("penalties", [])

        self.game_clock: dict[str: Any] = self.l_data.get("clock", {})
        self.game_clock_time_remaining: str = self.game_clock.get("timeRemaining")
        self.game_clock_seconds_remaining: int = int(self.game_clock.get("secondsRemaining", 1200))
        self.game_clock_running: str = self.game_clock.get("running")
        self.game_clock_in_intermission: str = self.game_clock.get("inIntermission")

    def is_game_over(self) -> bool:
        return self.game_state.lower() == "off"

    def is_game_live(self) -> bool:
        return self.game_state.lower() == "live"

    def is_game_future(self) -> bool:
        return self.game_state.lower() == "fut"

    def to_df_row(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if type(v) not in (list, tuple, dict, pd.DataFrame)}

    def __repr__(self):
        return f"<NHLGameLanding {self.g_id} {self.start_time_atl:{UTC_FMT}} {self.away_team_name_short} @ {self.home_team_name_short}>"


if __name__ == "__main__":
    import requests
    url = "https://api-web.nhle.com/v1/gamecenter/2025020910/landing"
    data: dict = requests.get(url).json()
    gl = NHLGameLanding(data)
    print(gl)

    game_over: bool = gl.is_game_over()
    scoring: list[dict] = gl.scoring
    clock = gl.game_clock
    print(f"{game_over=}")
    print(f"{clock=}")
    print(f"{scoring=}")

    for period_desc_dict in scoring:
        period_desc: dict = period_desc_dict.get("periodDescriptor", {})
        period_goals: list = period_desc_dict.get("goals", [])
        period_num: int = period_desc.get("number", 1)
        period_type: str = period_desc.get("periodType", "REG")
        max_reg_periods: int = period_desc.get("maxRegulationPeriods", 3)
        print(f"P# {period_num}")
        # print(period_goals)
        for i, goal_dict in enumerate(period_goals):
            situation: str = goal_dict.get("situationCode")
            event: int = goal_dict.get("eventId")
            strength: int = goal_dict.get("strength", "ev")
            player_id: int = goal_dict.get("playerId")
            player_name_first: str = goal_dict.get("firstName", {}).get("default")
            player_name_last: str = goal_dict.get("lastName", {}).get("default")
            player_name_short: str = goal_dict.get("name", {}).get("default")
            team_abbrev: str = goal_dict.get("teamAbbrev", {}).get("default")
            headshot: str = goal_dict.get("headshot")
            highlight_clip_url: str = goal_dict.get("highlightClipSharingUrl")
            highlight_clip_id: int = goal_dict.get("highlightClip")
            discrete_clip: int = goal_dict.get("discreteClip")
            discrete_clip_fr: int = goal_dict.get("discreteClipFr")
            player_goals_to_date: int = goal_dict.get("goalsToDate")
            away_team_score: int = goal_dict.get("awayScore", 0)
            home_team_score: int = goal_dict.get("homeScore", 0)
            leading_team_abbrev: str = goal_dict.get("leadingTeamAbbrev", {}).get("default")
            time_in_period: str = goal_dict.get("timeInPeriod")
            shot_type: str = goal_dict.get("shotType")
            goal_modifier: str = goal_dict.get("goalModifier")
            ppt_replay_url: str = goal_dict.get("pptReplayUrl")
            home_defending_side: str = goal_dict.get("homeTeamDefendingSide")
            is_home: bool = goal_dict.get("isHome")
            assists: list[dict] = goal_dict.get("assists", [])

            fs = home_team_score if is_home else away_team_score
            ss = away_team_score if is_home else home_team_score

            g_text: str = f"{time_in_period} {team_abbrev}({fs}-{ss}) {player_name_short}({player_goals_to_date}) {strength}"
            if assists:
                g_text += f" from "
            else:
                g_text += f" Unassisted"

            for j, assist_dict in enumerate(assists):
                a_player_id: int = assist_dict.get("playerId")
                a_player_name_first: str = assist_dict.get("firstName", {}).get("default")
                a_player_name_last: str = assist_dict.get("lastName", {}).get("default")
                a_player_name_short: str = assist_dict.get("name", {}).get("default")
                a_player_assists_to_date: int = assist_dict.get("assistsToDate")
                a_player_num: int = assist_dict.get("sweaterNumber")

                g_text += f"#{a_player_num} {a_player_name_short}({a_player_assists_to_date}) and "

            g_text = g_text.strip().removesuffix("and").strip()
            print(g_text)

    # df_data = pd.DataFrame(data, index=[0])

from __future__ import annotations

import datetime
import json
import math
import html
import uuid
import os
import random
from typing import Optional, List, Dict
from dateutil import tz

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd

from typing import Any, Mapping, Optional, Sequence, Union
from streamlit_pills import pills
from streamlit_calendar import calendar
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

from objects.api_handler import NHLAPIHandler
from objects.game import NHLBoxScore, NHLGameLanding
from objects.jersey import NHLJerseyCollection, Jersey
from objects.league import NHLSeason, NHLStandings, NHLScoreboard
from objects.player import NHLPlayer
from objects.team import NHLTeam
from resources.resource import PATH_JERSEY_COLLECTION_DATA, JERSEY_COLOUR_SAVE_FILE, DEFAULT_TEAM, UTC_FMT, NHL_URL, \
    DATE_FMT, NHL_PLAYER_API_URL, NHL_ASSET_API_URL, NHL_STATS_API_URL, NHL_API_URL
from utils.colour_utility import Colour, gradient_merge
from utils.datetime_utility import date_str_format
from utils.streamlit_utility import display_df_paginated, coloured_block, show_timer
from utils.utility import money, percent, number_suffix, try_index
from utils.utils import f_standing_record, f_season, get_this_season_str, extract_dominant_colours, \
    generate_color_gradient, get_color_at_position, date_to_this_year

st.set_page_config(layout="wide")

with st.sidebar:
    if st.button(
            label="Clear Cache & Rerun",
            key=f"k_clear_cache_rerun"
    ):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    with st.popover("session_state"):
        simple = {
            bool: lambda x: str(x),
            str: lambda x: str(x)[:20] + ("..." if len(x) > 20 else ""),
            int: lambda x: str(x),
            float: lambda x: str(x),
            datetime.date: lambda x: f"{x:%Y-%m-%d}",
            datetime.datetime: lambda x: f"{x:%Y-%m-%d %H:%M:%S}",
            pd.DataFrame: lambda x: f"DataFrame {x.shape}",
        }
        info_dict = {k: simple.get(type(v), lambda x: type(x))(v) for k, v in st.session_state.items()}
        st.write(info_dict)

RowLike = Union[Mapping[str, Any], "pd.Series", "pd.DataFrame"]


def format_game_header(state: str, result: str, period: int, time_left: str, start_time: str, debug: bool = False) -> \
tuple[str, str]:
    s = (state or "").lower().strip()
    r = (result or "").upper().strip()
    if debug:
        st.write(f"{s=}, {r=}, {state=}, {result=}, {period=}, {time_left=}, {start_time=}, {debug=}")

    # FINAL
    if s in {"off", "final", "finished"}:
        if debug:
            st.write(f"final")
        if r in {"OT", "SO"}:
            return ("Final", r)
        return ("Final", "")

    # NOT STARTED
    if s in {"pre", "preview", "future", "scheduled", "fut"}:
        # show start time if you have it
        if debug:
            st.write(f"not started")
        s_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        s_th = s_time.hour % 12
        if s_th == 0:
            s_th = 12
        s_time = f"{s_th} {s_time:%p}"
        return ((s_time or "—"), "")

    # LIVE
    # (most nhle feeds use "live"/"inprogress" variants)
    if s in {"live", "inprogress", "progress", "on"}:
        if debug:
            st.write(f"live")
        return (f"{period}{number_suffix(period).upper()}", time_left or "—")

    # fallback
    if debug:
        st.write(f"fallback")
    return (f"{period}{number_suffix(period).upper()}", time_left or "—")


def build_goal_cards_from_landing(
        gl,
        *,
        theme_bg: str = "#FFFFFF",
        theme_fg: str = "#000000",
        theme_border: str = "#212121",
        debug=False
) -> List[str]:
    """
    Reads gl.scoring from NHLGameLanding
    Returns a list of HTML goal-scorer cards (chronological order).
    """

    goal_cards: List[str] = []

    scoring: list[dict] = gl.scoring or []

    for period_desc_dict in scoring:
        period_desc: dict = period_desc_dict.get("periodDescriptor", {})
        period_num: int = period_desc.get("number", 1)

        period_goals: list = period_desc_dict.get("goals", [])

        for goal_dict in period_goals:

            # --- Basic goal info ---
            strength = goal_dict.get("strength", "EV")
            is_home = goal_dict.get("isHome", False)

            player_first = goal_dict.get("firstName", {}).get("default", "")
            player_last = goal_dict.get("lastName", {}).get("default", "")
            player_short = goal_dict.get("name", {}).get("default", "")
            player_goals_to_date = goal_dict.get("goalsToDate", "")
            headshot = goal_dict.get("headshot", "")

            team_abbrev = goal_dict.get("teamAbbrev", {}).get("default", "")
            time_in_period = goal_dict.get("timeInPeriod", "")

            home_score = goal_dict.get("homeScore", 0)
            away_score = goal_dict.get("awayScore", 0)

            # Score from perspective of scoring team
            fs = home_score if is_home else away_score
            ss = away_score if is_home else home_score

            # --- Assists (0–2) ---
            assists = goal_dict.get("assists", [])

            a1 = ""
            a2 = ""

            if len(assists) >= 1:
                a1_dict = assists[0]
                a1_name = a1_dict.get("name", {}).get("default", "")
                a1_total = a1_dict.get("assistsToDate", "")
                a1 = f"{a1_name} ({a1_total})"

            if len(assists) >= 2:
                a2_dict = assists[1]
                a2_name = a2_dict.get("name", {}).get("default", "")
                a2_total = a2_dict.get("assistsToDate", "")
                a2 = f"{a2_name} ({a2_total})"

            # --- Build card payload ---
            goal_payload: Dict[str, Any] = {
                "headshotUrl": headshot,
                "fName": player_first,
                "lName": player_last,
                "goalNum": player_goals_to_date,
                "strength": strength.upper(),
                "scorer": f"{player_short} ({player_goals_to_date})",
                "a1": a1,
                "a2": a2,
                "time": time_in_period,
                "period": period_num,
            }

            if debug:
                st.write("goal_payload")
                st.write(goal_payload)

            # Build HTML card (uses your earlier helper)
            card_html = goal_scorer_card_html(
                goal_payload,
                theme_bg=theme_bg,
                theme_fg=theme_fg,
                theme_border=theme_border,
                debug=debug
            )

            goal_cards.append(card_html)

    return goal_cards


def goal_scorer_card_html(
        g: Mapping[str, Any],
        *,
        width_px: int = 330,
        height_px: int = 64,
        theme_bg: str = "#FFFFFF",
        theme_fg: str = "#000000",
        theme_border: str = "#212121",
        debug: bool = False
) -> str:
    """
    Streamlit-ready HTML for ONE goal-scorer card (no JS).

    Expected keys (suggested):
      headshotUrl (optional)
      fName, lName
      goalNum (e.g., 12)               # shown in the small "G" box
      strength (e.g., "EV", "PP", "SH")
      scorer (e.g., "A. Tkachuk (12)")
      a1 (optional), a2 (optional)     # assists 0-2
      time (e.g., "12:34")
    """

    def s(key: str, default: str = "") -> str:
        v = g.get(key, default)
        return default if v is None else str(v)

    def esc(key: str, default: str = "") -> str:
        return html.escape(s(key, default))

    headshot = s("headshotUrl", "").strip()
    headshot_html = (
        f'<img class="gs-headshot" src="{html.escape(headshot)}" alt="" />'
        if headshot
        else '<div class="gs-headshot gs-ph"></div>'
    )

    # assists: 0-2, compacted
    a1 = s("a1", "").strip()
    a2 = s("a2", "").strip()
    assists_parts = [x for x in (a1, a2) if x]
    assists_text = " / ".join(assists_parts)

    assists_html = (
        f'<div class="gs-assists">{html.escape(assists_text)}</div>'
        if assists_text
        else '<div class="gs-assists gs-assists-empty">Unassisted</div>'
    )

    if debug:
        st.code(assists_html, language="html", line_numbers=True)

    return f"""
<div class="gs-card" style="--gs-w:{int(width_px)}px; --gs-h:{int(height_px)}px; --gs-bg:{theme_bg}; --gs-fg:{theme_fg}; --gs-bd:{theme_border};">
  <style>
    .gs-card {{
      width: var(--gs-w);
      height: var(--gs-h);
      background: var(--gs-bg);
      border: 1px solid var(--gs-bd);
      border-radius: 10px;
      box-sizing: border-box;
      display: grid;
      grid-template-columns: 56px 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 6px 8px;
      padding: 2px;
      color: var(--gs-fg);
      font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
      overflow: hidden;
    }}

    .gs-headshot {{
      grid-row: 1 / span 2;
      width: 56px;
      height: calc(var(--gs-h) - 12px);
      object-fit: cover;
      border-radius: 8px;
      display:block;
      background: rgba(255,255,255,0.10);
    }}
    .gs-ph {{
      background: rgba(0,0,0,0.18);
      border: 1px solid rgba(255,255,255,0.18);
    }}

    .gs-top {{
      display: grid;
      grid-template-columns: 1fr 44px;
      gap: 6px;
      align-items: stretch;
      min-width: 0;
    }}
    .gs-name {{
      border: 1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.10);
      border-radius: 8px;
      padding: 1px 2px;
      font-weight: 800;
      font-size: 12px;
      line-height: 1.05;
      display:flex;
      align-items:center;
      justify-content:flex-start;
      text-align:left;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .gs-g {{
      border: 1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.10);
      border-radius: 8px;
      font-weight: 900;
      font-size: 12px;
      display:flex;
      align-items:center;
      justify-content:center;
    }}
    .gs-str {{
      border: 1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.10);
      border-radius: 8px;
      font-weight: 900;
      font-size: 12px;
      display:flex;
      align-items:center;
      justify-content:center;
      letter-spacing: 0.2px;
    }}

    .gs-bot {{
      display: grid;
      grid-template-columns: 195px 42px;
      gap: 8px;
      align-items: stretch;
      min-width: 0;
    }}
    .gs-scorer, .gs-assists, .gs-time {{
      border: 1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.10);
      border-radius: 8px;
      padding: 1px 2px;
      font-weight: 800;
      font-size: 11px;
      line-height: 1.05;
      display:flex;
      align-items:left;
      justify-content:flex-start;
      text-align:left;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      min-width: 0;
    }}
    .gs-time {{
      font-weight: 900;
      justify-content: flex-end;
      text-align: right;
      padding-left 10px;
      padding-right 10px;
    }}

    /* If no assists, keep the box but visually soften it */
    .gs-assists-empty {{
      opacity: 0.55;
    }}
  </style>

  {headshot_html}

  <div class="gs-top">
  <div class="gs-name">
    {esc("fName", "F")} {esc("lName", "L")} (<span class="gs-goalnum">{esc("goalNum", "0")})</span>
  </div>
  <div class="gs-str">{esc("strength", "EV")}</div>
</div>

  <div class="gs-bot">
    {assists_html}
    <div class="gs-time">{esc("time", "time")}</div>
  </div>
</div>
""".strip()


def hockey_game_block_html(
        row: RowLike,
        *,
        block_id: Optional[str] = None,
        width_px: int = 525,
        # allow passing richer HTML for scorer cards later
        # safe_html_keys: Sequence[str] = ("goalScorer_1", "goalScorer_2"),
        # optional: override/alias incoming keys -> canonical keys
        key_aliases: Optional[Mapping[str, Sequence[str]]] = None,
        debug: bool = False,
) -> str:
    """
    Cleaner game card with a horizontally scrollable goal-scorer strip.

    Canonical keys (recommended):
      period, time
      awayLogo, awayTeamName, awaySoG, awayScore
      homeLogo, homeTeamName, homeSoG, homeScore
      goalScorer_1, goalScorer_2        (or provide as HTML strings later)
      streamUrl, gamecenterUrl
      networkLogo_1, networkLogo_2      (optional)

    Notes:
    - Key lookup is case-insensitive and supports aliases (see default_aliases below).
    - safe_html_keys are injected raw; everything else is escaped.
    """

    # -------- normalize input to dict --------
    if pd is not None and hasattr(row, "iloc") and hasattr(row, "shape"):  # DataFrame
        if row.shape[0] != 1:
            raise ValueError("DataFrame input must have exactly 1 row.")
        data: dict[str, Any] = row.iloc[0].to_dict()
    elif pd is not None and hasattr(row, "to_dict"):  # Series
        data = row.to_dict()  # type: ignore[assignment]
    else:
        data = dict(row)  # type: ignore[arg-type]

    # preserve original keys, build case-insensitive map
    data_ci = {str(k).lower(): v for k, v in data.items()}

    bid = block_id or uuid.uuid4().hex[:10]
    scope = f"hg2-{bid}"
    goals_scroller_id = f"{scope}-goals"

    # -------- key aliasing (fixes AwayScore vs awayScore, etc.) --------
    default_aliases: dict[str, Sequence[str]] = {
        "startTime": ("start_time_atl",),
        "state": ("game_state", "gameState"),
        "result": ("game_period_desc_type",),
        "awayScore": ("awayScore", "AwayScore", "away_score", "away_team_score", "awayscore"),
        "homeScore": ("homeScore", "HomeScore", "home_score", "home_team_score", "homescore"),
        "awaySoG": ("awaySoG", "awaySOG", "AwaySoG", "AwaySOG", "away_sog", "away_team_sog"),
        "homeSoG": ("homeSoG", "homeSOG", "HomeSoG", "HomeSOG", "home_sog", "home_team_sog"),
        # "awayTeamName": ("awayTeamName", "away_team_name", "AwayTeamName"),
        # "homeTeamName": ("homeTeamName", "home_team_name", "HomeTeamName"),
        "awayTeamName": ("away_team_name_short",),
        "homeTeamName": ("home_team_name_short",),
        "awayLogo": ("awayLogo", "away_logo", "away_team_logo", "AwayLogo"),
        "homeLogo": ("homeLogo", "home_logo", "home_team_logo", "HomeLogo"),
        "period": ("period", "Period", "game_period"),
        # "time": ("time", "Time", "game_clock_seconds_remaining"),
        "time": ("game_clock_time_remaining",),
        "streamUrl": ("streamUrl", "stream", "StreamUrl", "stream_url"),
        "recapUrl": ("game_three_min_recap",),
        "gamecenterUrl": ("game_center_link",),
        "networkLogo_1": ("networkLogo_1", "network1", "NetworkLogo1", "network_logo_1"),
        "networkLogo_2": ("networkLogo_2", "network2", "NetworkLogo2", "network_logo_2")
    }
    for i in range(1, 26):
        default_aliases.update({f"goalScorer_{i}": (f"goalScorer_{i}", f"goal_scorer_{i}", f"GoalScorer_{i}")})
    if key_aliases:
        # merge user aliases over defaults
        for k, aliases in key_aliases.items():
            default_aliases[k] = tuple(aliases)

    def _get_raw(canonical: str, default: Any = "") -> Any:
        # try exact canonical key first (original dict)
        if canonical in data:
            return data.get(canonical, default)

        # then try aliases
        for a in default_aliases.get(canonical, (canonical,)):
            # exact match
            if a in data:
                return data.get(a, default)
            # case-insensitive match
            v = data_ci.get(str(a).lower(), None)
            if v is not None:
                return v

        # finally case-insensitive canonical
        v = data_ci.get(canonical.lower(), None)
        return default if v is None else v

    def get_str(canonical: str, default: str = "") -> str:
        v = _get_raw(canonical, default)
        if v is None:
            return default
        return str(v)

    def esc(canonical: str, default: str = "") -> str:
        return html.escape(get_str(canonical, default))

    def val_html(canonical: str, default: str = "") -> str:
        if canonical in gs_keys:
            return get_str(canonical, default)  # raw HTML
        return html.escape(get_str(canonical, default))

    def maybe_img(canonical_src: str, *, cls: str = "") -> str:
        src = get_str(canonical_src, "").strip()
        if src:
            return f'<img class="{cls}" src="{html.escape(src)}" alt="" />'
        # If not provided, keep the layout but show nothing (or you can show placeholder)
        return f'<div class="{cls} hg2-imgph"></div>'

    # -------- values --------
    period = int(float(esc("period", "1")))
    time_ = esc("time", "20:00")
    # time_ = int(float(esc("time", str(20*60))))
    # time_ = ":".join(map(lambda v: str(v).rjust(2, "0"), divmod(time_, 60)))
    state = esc("state", "").lower()
    result = esc("result", "")
    game_over: bool = state == "off"
    result_str = "Final" if game_over and result.lower() == "reg" else f"/{result}"
    start_time = esc("startTime", "")
    left_pill, right_pill = format_game_header(state, result, period, time_, start_time, debug=True)

    away_team = esc("awayTeamName", "Away")
    away_sog = esc("awaySoG", "SoG: —")
    away_score = int(float(esc("awayScore", "0")))

    home_team = esc("homeTeamName", "Home")
    home_sog = esc("homeSoG", "SoG: —")
    home_score = int(float(esc("homeScore", "0")))

    stream_url = get_str("streamUrl", "").strip()
    gc_url = f"{NHL_URL}{get_str('gamecenterUrl', '').strip().removeprefix("/")}"
    recap_url = f"{NHL_URL}{get_str('recapUrl').strip().removeprefix("/")}"
    stream_recap_url = recap_url if game_over else stream_url
    stream_recap = "Recap" if game_over else "Stream"

    net1 = maybe_img("networkLogo_1", cls="hg2-net")
    net2 = maybe_img("networkLogo_2", cls="hg2-net")

    away_logo = maybe_img("awayLogo", cls="hg2-logo")
    home_logo = maybe_img("homeLogo", cls="hg2-logo")

    # Scorer “cards” (for now just text/html); later you’ll pass richer HTML
    gs_keys = [k for k in default_aliases.keys() if k.lower().startswith("goalscorer")]
    goal_items = [val_html(k) for k in gs_keys]
    goal_items = [gi for gi in goal_items if gi]

    dot_count = len(goal_items)
    dots_html = ""
    for i in range(dot_count):
        active = " active" if i == 0 else ""
        dots_html += f'<div id="{scope}-dot{i}" class="hg2-dot{active}"></div>'

    if debug:
        st.write("gs_keys")
        st.write(gs_keys)
        st.write(f"n goals {len(goal_items)=}")

    # -------- HTML --------
    html_str = f"""
<div id="{scope}" class="hg2-card" style="--hg2-w:{int(width_px)}px;">
  <style>
    #{scope}.hg2-card {{
      width: var(--hg2-w);
      max-width: 100%;
      background: #fff;
      border: 1px solid #e7e7e7;
      border-radius: 14px;
      overflow: hidden;
      padding: 4px;
      box-sizing: border-box;
      font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
    }}

    #{scope} .hg2-top {{
      display:flex; align-items:center; gap:10px;
    }}

    #{scope} .hg2-pill {{
      border: 1px solid #d9d9d9;
      border-radius: 10px;
      padding: 1px 2px;
      font-weight: 700;
      font-size: 13px;
      color: #1a1a1a;
      background: #fafafa;
      white-space: nowrap;
    }}

    #{scope} .hg2-spacer {{ flex: 1; }}

    #{scope} .hg2-nets {{
      display:flex; align-items:center; gap:10px;
    }}
    #{scope} .hg2-net {{
      height: 18px; width:auto; display:block;
    }}
    #{scope} .hg2-imgph {{
      height: 18px; width: 36px;
    }}

    #{scope} .hg2-teams {{
      display:grid;
      grid-template-columns: 44px 1fr 56px;
      gap: 10px 12px;
      margin-top: 12px;
      align-items:center;
    }}

    #{scope} .hg2-logo {{
      width: 44px; height: 44px;
      object-fit: contain;
      border-radius: 10px;
      border: 1px solid #e1e1e1;
      background: #fff;
      display:block;
    }}
    #{scope} .hg2-row {{
      display:flex;
      flex-direction: column;
      gap: 4px;
    }}
    #{scope} .hg2-name {{
      font-weight: 800;
      font-size: 14px;
      color:#121212;
      line-height: 1.1;
    }}
    #{scope} .hg2-sub {{
      font-weight: 650;
      font-size: 12px;
      color:#6b6b6b;
    }}
    #{scope} .hg2-score {{
      justify-self:end;
      font-weight: 900;
      font-size: 20px;
      color:#111;
      width: 56px;
      text-align:right;
    }}
    #{scope} .hg2-divider {{
      grid-column: 1 / -1;
      height: 1px;
      background: #efefef;
      margin: 4px 0;
    }}

    #{scope} .hg2-section-title {{
      margin-top: 12px;
      font-weight: 900;
      font-size: 13px;
      color:#121212;
    }}

    #{scope} .hg2-goalswrap {{
      margin-top: 6px;
      border: 1px solid #efefef;
      border-radius: 12px;
      padding: 10px;
    }}

    #{scope} .hg2-goalsbar {{
      display:flex;
      align-items:center;
      justify-content:center;
      gap: 10px;
      margin-top: 8px;
      user-select:none;
      color:#b3b3b3;
    }}

    #{scope} .hg2-arrow {{
      border: 0;
      background: transparent;
      font-weight: 900;
      font-size: 18px;
      color:#9b9b9b;
      cursor: pointer;
      padding: 1px 2px;
    }}
    #{scope} .hg2-arrow:hover {{
      color:#6f6f6f;
    }}

    #{scope} .hg2-dots {{
      display:flex; gap: 3px; align-items:center;
    }}
    #{scope} .hg2-dot {{
      width: 22px;
      height: 3px;
      border-radius: 3px;
      background: #d9d9d9;
      opacity: 0.9;
    }}
    #{scope} .hg2-dot.active {{
      background: #2d6cdf;
    }}

    #{scope} .hg2-scroller {{
      display:flex;
      gap: 10px;
      overflow-x: auto;
      scroll-snap-type: x mandatory;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }}
    #{scope} .hg2-scroller::-webkit-scrollbar {{
      display:none;
    }}

    #{scope} .hg2-goalcard {{
      flex: 0 0 72%;
      min-width: 240px;
      border: 1px solid #e8e8e8;
      border-radius: 12px;
      padding: 2px;
      background: #fff;
      scroll-snap-align: start;
      box-sizing:border-box;
    }}

    #{scope} .hg2-actions {{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 12px;
    }}
    #{scope} .hg2-btn {{
      display:flex;
      align-items:center;
      justify-content:center;
      border: 1px solid #e1e1e1;
      border-radius: 12px;
      padding: 1px 2px;
      text-decoration:none;
      font-weight: 850;
      color: #2d6cdf;
      background: #fff;
    }}
    #{scope} .hg2-btn:hover {{
      border-color:#cfcfcf;
    }}
  </style>
  """

    html_str += f"""
    <!-- top row -->
    <div class="hg2-pill">{left_pill} {right_pill if right_pill else ''}
    <div class="hg2-spacer"></div>
    <div class="hg2-nets">
      {net1}
      {net2}
    </div>
    </div>
    """
    # if game_over:
    #     html_str += f"""
    #     <!-- top row -->
    #     <div class="hg2-pill">{left_pill}{right_pill if right_pill else ''}
    #     <div class="hg2-spacer"></div>
    #     <div class="hg2-nets">
    #       {net1}
    #       {net2}
    #     </div>
    #     </div>
    #     """
    # else:
    #     html_str += f"""
    #     <!-- top row -->
    #     <div class="hg2-top">
    #     <div class="hg2-pill">{period}{number_suffix(period).upper()}</div>
    #     <div class="hg2-pill">{time_}</div>
    #     <div class="hg2-spacer"></div>
    #     <div class="hg2-nets">
    #       {net1}
    #       {net2}
    #     </div>
    #     </div>
    #     """
    html_str += f"""
  <!-- teams -->
  <div class="hg2-teams">
    {away_logo}
    <div class="hg2-row">
      <div class="hg2-name">{away_team}</div>
      <div class="hg2-sub">SOG: {away_sog}</div>
    </div>
    <div class="hg2-score">{away_score}</div>

    <div class="hg2-divider"></div>

    {home_logo}
    <div class="hg2-row">
      <div class="hg2-name">{home_team}</div>
      <div class="hg2-sub">SOG: {home_sog}</div>
    </div>
    <div class="hg2-score">{home_score}</div>
  </div>

"""

    if goal_items:
        html_str += f"""
            <!-- goals -->
      <div class="hg2-section-title">Goals</div>
      <div class="hg2-goalswrap">
        <div id="{goals_scroller_id}" class="hg2-scroller">
        """
        for goal in goal_items:
            html_str += f"""<div class="hg2-goalcard">{goal}</div>"""
        html_str += f"""
        </div>

        <div class="hg2-goalsbar">
          <button class="hg2-arrow" type="button" onclick="(function(){{
            const sc = document.getElementById('{goals_scroller_id}');
            sc && sc.scrollBy({{ left: -Math.max(240, sc.clientWidth*0.75), behavior: 'smooth' }});
          }})()">‹</button>

          <div class="hg2-dots" aria-hidden="true">
            {dots_html}
          </div>

          <button class="hg2-arrow" type="button" onclick="(function(){{
            const sc = document.getElementById('{goals_scroller_id}');
            sc && sc.scrollBy({{ left:  Math.max(240, sc.clientWidth*0.75), behavior: 'smooth' }});
          }})()">›</button>
        </div>
      </div>
        """

    html_str += f"""

      <!-- actions -->
      <div class="hg2-actions">
        <a class="hg2-btn" href="{html.escape(stream_recap_url) if stream_recap_url else "#"}" target="_blank" rel="noopener">{stream_recap}</a>
        <a class="hg2-btn" href="{html.escape(gc_url) if gc_url else "#"}" target="_blank" rel="noopener">Gamecenter</a>
      </div>

      <script>
        (function() {{
          const sc = document.getElementById("{goals_scroller_id}");
          if (!sc) return;

          const dots = [];
          for (let i = 0; i < {dot_count}; i++) {{
            const d = document.getElementById("{scope}-dot" + i);
            if (d) dots.push(d);
          }}

          function setActive(idx) {{
            dots.forEach((d, i) => d.classList.toggle("active", i === idx));
          }}

          function updateFromScroll() {{
            // find the nearest card index based on scroll position
            const cards = sc.querySelectorAll(".hg2-goalcard");
            if (!cards || cards.length === 0) return;

            let bestIdx = 0;
            let bestDist = Infinity;

            for (let i = 0; i < cards.length; i++) {{
              const c = cards[i];
              const dist = Math.abs(c.offsetLeft - sc.scrollLeft);
              if (dist < bestDist) {{
                bestDist = dist;
                bestIdx = i;
              }}
            }}

            setActive(bestIdx);
          }}

          sc.addEventListener("scroll", function() {{
            window.requestAnimationFrame(updateFromScroll);
          }});

          updateFromScroll();
        }})();
      </script>
    </div>
    """.strip()
    return html_str


def hockey_game_block_html_0(
        row: RowLike,
        *,
        block_id: Optional[str] = None,
        width_px: int = 510,
        safe_html_keys: Sequence[str] = ("goalScorer_1", "goalScorer_2"),
) -> str:
    """
    Build a Streamlit-ready HTML block for a hockey game card.

    Expected keys (your placeholders):
      period, time
      awayLogo, awayTeamName, awaySoG, awayScore
      homeLogo, homeTeamName, homeSoG, homeScore
      goalScorer_1, goalScorer_2
      streamUrl, gamecenterUrl
      networkLogo_1, networkLogo_2   (optional; top-right)

    Notes:
    - Any keys in `safe_html_keys` are injected as raw HTML (for your future player card HTML).
      Everything else is HTML-escaped.
    - Logos are treated as <img src="..."> if non-empty; otherwise the placeholder text is shown.
    """

    st.write(f"row")
    st.write(row)
    st.write(f"{type(row)=}")

    # ---- normalize input to dict ----
    data: dict[str, Any]
    if pd is not None and hasattr(row, "iloc") and hasattr(row, "shape"):  # DataFrame
        if getattr(row, "shape", (0, 0))[0] != 1:
            raise ValueError("DataFrame input must have exactly 1 row.")
        data = row.iloc[0].to_dict()
    elif pd is not None and hasattr(row, "to_dict"):  # Series
        data = row.to_dict()  # type: ignore[assignment]
    else:  # dict-like
        data = dict(row)  # type: ignore[arg-type]

    # ---- helpers ----
    bid = block_id or uuid.uuid4().hex[:10]
    scope = f"hg-{bid}"

    def get(k: str, default: str = "") -> str:
        v = data.get(k, default)
        if v is None:
            return default
        return str(v)

    def esc(k: str, default: str = "") -> str:
        return html.escape(get(k, default))

    def maybe_img(src_key: str, fallback_text_key: Optional[str] = None, *, cls: str = "") -> str:
        src = get(src_key, "").strip()
        if src:
            return f'<img class="{cls}" src="{html.escape(src)}" alt="" />'
        # if no src, show the key name (or a provided fallback text field)
        fallback = fallback_text_key or src_key
        return f'<div class="{cls} hg-ph">{html.escape(get(fallback, fallback))}</div>'

    def val_html(k: str, default: str = "") -> str:
        if k in safe_html_keys:
            return get(k, default)  # raw
        return html.escape(get(k, default))

    # ---- values ----
    period = esc("period", "period")
    time_ = esc("time", "time")

    away_team = esc("awayTeamName", "awayTeamName")
    away_sog = esc("awaySoG", "awaySoG")
    away_score = esc("awayScore", "AwayScore")

    home_team = esc("homeTeamName", "homeTeamName")
    home_sog = esc("homeSoG", "homeSoG")
    home_score = esc("homeScore", "homeScore")

    goal1 = val_html("goalScorer_1", "goalScorer_1")
    goal2 = val_html("goalScorer_2", "goalScorer_2")

    stream_url = get("streamUrl", "").strip()
    gc_url = get("gamecenterUrl", "").strip()

    net1 = maybe_img("networkLogo_1", cls="hg-netimg")
    net2 = maybe_img("networkLogo_2", cls="hg-netimg")

    away_logo = maybe_img("awayLogo", cls="hg-teamlogo")
    home_logo = maybe_img("homeLogo", cls="hg-teamlogo")

    # ---- html ----
    return f"""
<div id="{scope}" class="hg-card" style="--hg-w:{int(width_px)}px;">
  <style>
    /* Scoped styles so multiple cards can live on the same page */
    #{scope}.hg-card {{
      width: var(--hg-w);
      max-width: 100%;
      background: #ffffff;
      border: 1px solid #e6e6e6;
      border-radius: 10px;
      padding: 14px;
      box-sizing: border-box;
      font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
    }}

    #{scope} .hg-row {{ display:flex; align-items:center; gap:10px; }}
    #{scope} .hg-spacer {{ flex: 1; }}

    #{scope} .hg-box {{
      background: #3f6fb4;
      border: 2px solid #2c4d7d;
      color: #fff;
      font-weight: 600;
      border-radius: 0px;
      padding: 10px 12px;
      line-height: 1.05;
      text-align: center;
      box-sizing: border-box;
    }}
    #{scope} .hg-box.small {{ width: 64px; }}
    #{scope} .hg-box.time  {{ width: 76px; }}

    #{scope} .hg-nets {{ display:flex; gap:14px; align-items:center; justify-content:flex-end; }}
    #{scope} .hg-netimg {{ height: 22px; width:auto; display:block; }}
    #{scope} .hg-ph {{ font-size: 12px; opacity: 0.95; }}

    #{scope} .hg-teams {{
      display: grid;
      grid-template-columns: 64px 1fr 76px;
      grid-auto-rows: minmax(64px, auto);
      gap: 10px 12px;
      margin-top: 12px;
      align-items: stretch;
    }}

    #{scope} .hg-teamlogo {{
      width: 64px;
      height: 64px;
      object-fit: contain;
      display:block;
      background: #3f6fb4;
      border: 2px solid #2c4d7d;
      box-sizing: border-box;
    }}

    #{scope} .hg-teaminfo {{
      display: grid;
      grid-template-rows: 1fr 1fr;
      gap: 6px;
      align-content: stretch;
    }}

    #{scope} .hg-teamname, #{scope} .hg-teamsog {{
      background: #3f6fb4;
      border: 2px solid #2c4d7d;
      color: #fff;
      font-weight: 650;
      padding: 8px 10px;
      box-sizing: border-box;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      min-height: 28px;
    }}

    #{scope} .hg-score {{
      background: #3f6fb4;
      border: 2px solid #2c4d7d;
      color: #fff;
      font-weight: 750;
      font-size: 16px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      box-sizing: border-box;
    }}

    #{scope} .hg-goals-title {{
      margin-top: 10px;
      font-weight: 700;
      color: #111;
      font-size: 15px;
    }}

    #{scope} .hg-goals {{
      display: grid;
      grid-template-columns: 1.6fr 0.6fr;
      gap: 12px;
      margin-top: 6px;
      align-items: stretch;
    }}

    #{scope} .hg-goalbox {{
      background: #3f6fb4;
      border: 2px solid #2c4d7d;
      color: #fff;
      font-weight: 650;
      padding: 10px;
      box-sizing: border-box;
      min-height: 86px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
    }}

    #{scope} .hg-nav {{
      display:flex;
      align-items:center;
      justify-content:center;
      gap: 12px;
      margin-top: 10px;
      user-select: none;
      color: #9a9a9a;
      font-weight: 700;
    }}
    #{scope} .hg-dotbar {{
      display:flex; gap:6px; align-items:center;
    }}
    #{scope} .hg-dot {{
      width: 26px; height: 3px; background:#d6d6d6; border-radius: 2px;
    }}
    #{scope} .hg-dot.active {{ background:#2d6cdf; }}

    #{scope} .hg-actions {{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 12px;
    }}
    #{scope} .hg-btn {{
      display:flex;
      align-items:center;
      justify-content:center;
      border: 1px solid #e0e0e0;
      border-radius: 10px;
      padding: 10px 12px;
      text-decoration:none;
      font-weight: 700;
      color: #2d6cdf;
      background: #ffffff;
    }}
    #{scope} .hg-btn:focus, #{scope} .hg-btn:hover {{
      border-color: #c9c9c9;
    }}

    /* Make the card shrink nicely */
    @media (max-width: 560px) {{
      #{scope}.hg-card {{ --hg-w: 100%; }}
    }}
  </style>

  <!-- header -->
  <div class="hg-row">
    <div class="hg-box small">{period}</div>
    <div class="hg-box time">{time_}</div>
    <div class="hg-spacer"></div>
    <div class="hg-nets">
      {net1}
      {net2}
    </div>
  </div>

  <!-- teams -->
  <div class="hg-teams">
    <div>{away_logo}</div>
    <div class="hg-teaminfo">
      <div class="hg-teamname">{away_team}</div>
      <div class="hg-teamsog">{away_sog}</div>
    </div>
    <div class="hg-score">{away_score}</div>

    <div>{home_logo}</div>
    <div class="hg-teaminfo">
      <div class="hg-teamname">{home_team}</div>
      <div class="hg-teamsog">{home_sog}</div>
    </div>
    <div class="hg-score">{home_score}</div>
  </div>

  <!-- goals -->
  <div class="hg-goals-title">Goals</div>
  <div class="hg-goals">
    <div class="hg-goalbox">{goal1}</div>
    <div class="hg-goalbox">{goal2}</div>
  </div>

  <!-- little nav indicator (placeholder like your mock) -->
  <div class="hg-nav">
    <div style="font-size:22px; line-height: 1;">‹</div>
    <div class="hg-dotbar">
      <div class="hg-dot active"></div>
      <div class="hg-dot active"></div>
      <div class="hg-dot"></div>
    </div>
    <div style="font-size:22px; line-height: 1;">›</div>
  </div>

  <!-- actions -->
  <div class="hg-actions">
    <a class="hg-btn" href="{html.escape(stream_url) if stream_url else "#"}" target="_blank" rel="noopener">Stream</a>
    <a class="hg-btn" href="{html.escape(gc_url) if gc_url else "#"}" target="_blank" rel="noopener">Gamecenter</a>
  </div>
</div>
""".strip()


k_nhl_jersey_collection: str = "key_nhl_jersey_collection"
nhl_jc: NHLJerseyCollection = st.session_state.setdefault(k_nhl_jersey_collection,
                                                          NHLJerseyCollection(PATH_JERSEY_COLLECTION_DATA,
                                                                              JERSEY_COLOUR_SAVE_FILE))

k_nhl_api_handler: str = "key_nhl_api_handler"
if k_nhl_api_handler not in st.session_state:
    st.session_state[k_nhl_api_handler] = NHLAPIHandler(False)
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
start_page = options_pills_mode.index("Scores")
st.session_state.setdefault(k_pills_mode, start_page)
pills_mode = pills(
    label="Mode",
    options=options_pills_mode,
    key=k_pills_mode,
    index=start_page
)

if pills_mode == options_pills_mode[2]:
    # League Data
    st.write(nhl.get_country())
    st.write(nhl.get_geolocation())
    display_df_paginated(
        nhl.df_saved_data,
        "nhl.df_saved_data",
        key=f"nhl.df_saved_data"
    )
    display_df_paginated(
        teams,
        "Teams",
        key=f"Teams"
    )
    display_df_paginated(
        seasons,
        "Seasons",
        key=f"Seasons"
    )
    display_df_paginated(
        nhl.get_country_data(),
        "Countries",
        key=f"Countries"
    )
    display_df_paginated(
        nhl.df_players,
        "Known NHL Players",
        key=f"Known NHL Players"
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
    st.session_state.setdefault(k_selectbox_team_calendar, DEFAULT_TEAM)
    selectbox_team_calendar = st.selectbox(
        label="Select a Team",
        key=k_selectbox_team_calendar,
        options=lst_teams
    )
    if selectbox_team_calendar:
        team_events = []
        team_tri_code: str = \
        nhl.df_teams.loc[nhl.df_teams["fullName"].str.lower() == selectbox_team_calendar.lower()].iloc[0]["triCode"]
        if not nhl.df_games_boxscore.empty:
            df_team_games: pd.DataFrame = nhl.df_games_boxscore.loc[
                (nhl.df_games_boxscore["home_team_name_abbrev"] == team_tri_code)
                | (nhl.df_games_boxscore["away_team_name_abbrev"] == team_tri_code)
                ]
            st.write(f"{selectbox_team_calendar} Games:")
            st.write(
                df_team_games
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

    display_df_paginated(
        df_standings_now,
        "Standings as of now:",
        key="Standings as of now:"
    )

    # cols_standings: dict = {
    #     "triCode": "Team"
    # }
    # cols_standings.update(standings_now.show_cols())
    cols_standings = standings_now.show_cols()
    df_standings_now.rename(columns=cols_standings, inplace=True)
    df_standings_now["STRK"] = df_standings_now["STRKC"].astype(str) + df_standings_now["STRKN"].astype(str)
    df_standings_now["GPP"] = df_standings_now[NHLStandings.Abbr.GP.value] / 82
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
            "East WC": df_standings_now_east.loc[(1 <= df_standings_now_east["wildcardSequence"]) & (
                        df_standings_now_east["wildcardSequence"] < 3)].copy(),
            "West WC": df_standings_now_west.loc[(1 <= df_standings_now_west["wildcardSequence"]) & (
                        df_standings_now_west["wildcardSequence"] < 3)].copy()
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
    cols_dfs_to_show = cont_0.columns(len(df_standings_to_show)) if toggle_horizontal else [st.container(border=True)
                                                                                            for i in range(
            len(df_standings_to_show))]
    for i, k_df in enumerate(df_standings_to_show):
        df: pd.DataFrame = df_standings_to_show[k_df]
        with cols_dfs_to_show[i]:
            display_df_paginated(
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
                        max_value=1,
                        width=100
                    ),
                    "Δ": st.column_config.TextColumn(
                        "Δ",
                        help="▲ up, ▼ down, — no change",
                        width="small"
                    )
                },
                height=standings_heights[len(df_standings_to_show)],
                key=f"{k_df} Standings as of now:"
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
        # st.write(selectbox_investigate_game)
        st.write(date)
        ser_game: pd.Series = nhl.df_games_scoreboard.loc[
            nhl.df_games_scoreboard["str"] == selectbox_investigate_game
            ].iloc[0]
        ax = ser_game.axes[0].tolist()
        for a in [
            "home_team",
            "away_team"
        ]:
            if a in ax:
                ax.remove(a)
        sg: pd.Series = ser_game[ax]
        df_g: pd.DataFrame = pd.DataFrame(sg).transpose()
        # st.write("sg:")
        # st.write(sg)
        # st.write("dfg:")
        # st.write(df_g)
        display_df_paginated(
            df_g,
            "ser_game",
            key="ser_game"
        )
        g_id: str = df_g.loc[0, "g_id"]

        st.subheader(f"Scoreboard")
        html_block = hockey_game_block_html(df_g, width_px=510)
        # st.markdown(html_block, unsafe_allow_html=True)
        components.html(html_block, height=420, scrolling=False)

        df_g_bx = nhl.df_games_boxscore[nhl.df_games_boxscore["g_id"] == g_id]
        # print("nhl.df_games_boxscore")
        # print(nhl.df_games_boxscore)
        # # display_df_paginated(nhl.df_games_boxscore, "df_boxscores", key="df_boxscores")
        df_g_bx = nhl.df_games_boxscore[nhl.df_games_boxscore["g_id"] == g_id]
        # print("df_g_bx")
        # print(df_g_bx)
        # print(df_g_bx.columns.tolist())
        # print(df_g_bx.dtypes)
        if df_g_bx.empty:
            df_g_bx = pd.DataFrame(nhl.load_game_boxscore(g_id).to_df_row(), index=[0])
        # # display_df_paginated(df_g_bx, "df_g_bx", key="df_g_bx")
        # st.write("df_g_bx")
        # st.write(df_g_bx.to_dict())
        # # display_df_paginated(df_g_bx, "df_g_bx", key="df_g_bx")

        st.subheader(f"BoxScore")
        html_block = hockey_game_block_html(df_g_bx, width_px=510)
        # st.markdown(html_block, unsafe_allow_html=True)
        components.html(html_block, height=420, scrolling=False)

        # st.write("nhl.df_games_landing")
        # st.write(nhl.df_games_landing.head())
        # st.write(nhl.df_games_landing.columns.tolist())
        # st.write(list(nhl.df_games_landing.dtypes))
        df_g_lg = nhl.df_games_landing[nhl.df_games_landing["g_id"] == g_id]

        # print("df_g_lg")
        # print(df_g_lg)
        # print(df_g_lg.columns.tolist())
        # print(df_g_lg.dtypes)
        if df_g_lg.empty:
            gl: NHLGameLanding = nhl.load_game_landing(g_id)
            row_dict: dict = gl.to_df_row()
            df_g_lg = pd.DataFrame(row_dict, index=[0])
        else:
            gl: NHLGameLanding = nhl.load_game_landing(g_id)

        goal_cards = build_goal_cards_from_landing(gl, debug=False)
        n_goals = len(goal_cards)
        # st.write(f"{n_goals=}")
        for i in range(n_goals):
            gc = goal_cards[i]
            if not gc:
                break
            df_g_lg[f"goalScorer_{i + 1}"] = gc

        st.subheader(f"Landing")
        # st.write(gl.__dict__)
        # st.write(gl.scoring)

        html_block = hockey_game_block_html(
            df_g_lg,
            width_px=510
        )
        # st.markdown(html_block, unsafe_allow_html=True)
        components.html(html_block, height=420, scrolling=False)

        url_game_center: str = ser_game["game_center_link"]
        if url_game_center:
            url_game_center = f"{NHL_URL}{url_game_center.removeprefix("/")}"
            btn = st.link_button(
                label=f"gamecenter",
                url=url_game_center
            )
        else:
            st.write("no recap video found")

        url_3_min_recap: str = ser_game["game_three_min_recap"]
        if url_3_min_recap:
            url_3_min_recap = f"{NHL_URL}{url_3_min_recap.removeprefix("/")}"
            btn = st.link_button(
                label=f"recap",
                url=url_3_min_recap
            )
        else:
            st.write("no recap video found")

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

    g_ids_today = []
    idx_today = try_index(scoreboard_now.game_dates, pills_scoreboard_dates)
    if idx_today is not None:
        g_ids_today = [game.g_id for game in scoreboard_now.game_dates[idx_today]]
    games_per_row = 3
    grid = [st.columns(games_per_row) for i in range(math.ceil(len(g_ids_today) / games_per_row))]
    for i, g_id in enumerate(g_ids_today):
        g_i, g_j = divmod(i, games_per_row)
        with grid[g_i][g_j]:
            df_g_lg = nhl.df_games_landing[nhl.df_games_landing["g_id"] == g_id]

            # print("df_g_lg")
            # print(df_g_lg)
            # print(df_g_lg.columns.tolist())
            # print(df_g_lg.dtypes)
            if df_g_lg.empty:
                gl: NHLGameLanding = nhl.load_game_landing(g_id)
                row_dict: dict = gl.to_df_row()
                df_g_lg = pd.DataFrame(row_dict, index=[0])
            else:
                gl: NHLGameLanding = nhl.load_game_landing(g_id)

            goal_cards = build_goal_cards_from_landing(gl, debug=False)
            n_goals = len(goal_cards)
            # st.write(f"{n_goals=}")
            for i in range(n_goals):
                gc = goal_cards[i]
                if not gc:
                    break
                df_g_lg[f"goalScorer_{i + 1}"] = gc

            # st.subheader(f"Landing")
            # st.write(gl.__dict__)
            # st.write(gl.scoring)

            html_block = hockey_game_block_html(
                df_g_lg,
                width_px=510
            )
            # st.markdown(html_block, unsafe_allow_html=True)
            components.html(html_block, height=420, scrolling=False)

    for i, date in enumerate(scoreboard_now.game_dates):
        if date != pills_scoreboard_dates:
            continue
        timeline_events = []
        for j, game in enumerate(scoreboard_now.game_dates[date]):
            # assert isinstance(game, NHLGame), f"game must be a NHLGame, got '{type(game)=}'"
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

            timeline_events.append({
                # "start": game.start_time_atl.strftime(UTC_FMT).removesuffix("Z"),
                "Start Date": game.start_time_atl,
                # "end": (game.start_time_atl + datetime.timedelta(minutes=165)).strftime(UTC_FMT).removesuffix("Z"),
                "End Date": game.start_time_atl + datetime.timedelta(minutes=165),
                "Event": game.short_repr(),
                "State": game.game_state.lower()
            })

        # def cc_game_state(row: pd.Series):
        #     # now = datetime.datetime.now()
        #     # sd = row["Start Date"]
        #     # ed = row["End Date"]
        #     # if now > ed:
        #     #     "Over"
        #     # ["Start Date"] <= datetime.datetime.now() <= row["End Date"]
        #     return row[""]

        df_timeline_games = pd.DataFrame(timeline_events)
        # df_timeline_games["State"] = df_timeline_games.apply(
        #     lambda row: cc_game_state(row), axis=1)

        # Create a Gantt-like timeline using Plotly
        fig_timeline_games = px.timeline(
            df_timeline_games,
            x_start='Start Date',
            x_end='End Date',
            y='Event',
            title='Games today:',
            color='State',
            color_discrete_map={
                'crit': Colour('red').hex_code,
                'fut': Colour('#ECC868').hex_code,
                'off': Colour('dark-green').hex_code,
                'live': Colour('green').hex_code,
                'final': Colour('dark-green').hex_code,
                'pre': Colour('light-blue').hex_code
            }
        )

        # Update layout to make it more readable
        fig_timeline_games.update_layout(xaxis_title="Date", yaxis_title="Concurrent Games")

        # Display in Streamlit
        st.plotly_chart(fig_timeline_games)

    schedule = nhl.get_schedule()
    st.write(schedule)

    ax = nhl.df_games_boxscore.columns.tolist()
    for a in [
        "home_team",
        "away_team"
    ]:
        if a in ax:
            ax.remove(a)
    sg = nhl.df_games_boxscore[ax]

    display_df_paginated(
        sg,
        title="nhl.df_games_boxscore",
        key="nhl.df_games_boxscore"
    )

    df_games_yet_to_play: pd.DataFrame = nhl.df_games_boxscore[nhl.df_games_boxscore["game_state"] != "OFF"]

    df_games_yet_to_play = df_games_yet_to_play.merge(
        df_standings_now,
        left_on="game_home_team_id",
        right_on="t_id",
        how="left",
        suffixes=("", "_HT")
    ).merge(
        df_standings_now,
        left_on="game_away_team_id",
        right_on="t_id",
        how="left",
        suffixes=("", "_AT")
    )

    df_games_yet_to_play.sort_values(
        by="start_time_atl",
        inplace=True
    )

    display_df_paginated(
        df_games_yet_to_play,
        "df_games_yet_to_play",
        key="df_games_yet_to_play"
    )

    if selectbox_team_calendar:
        team_events = []
        df_sel_team: pd.DataFrame = nhl.df_teams.merge(
            df_standings_now,
            left_on="id",
            right_on="t_id",
            suffixes=("", "_Standings")
        )
        ser_sel_team: pd.Series = \
        df_sel_team.loc[df_sel_team["fullName"].str.lower() == selectbox_team_calendar.lower()].iloc[0]
        st.write(ser_sel_team)
        sel_team_id: int = ser_sel_team["id"]
        df_sel_team_games_left = df_games_yet_to_play[
            (df_games_yet_to_play["game_home_team_id"] == sel_team_id)
            | (df_games_yet_to_play["game_away_team_id"] == sel_team_id)
            ].reset_index(drop=True)

        display_df_paginated(
            df_sel_team_games_left,
            f"Games left for {selectbox_team_calendar}:",
            key=f"Games left for {selectbox_team_calendar}:",
            hide_index=False
        )


        def calc_leg(df: pd.DataFrame, t_id: Optional[int] = None) -> pd.DataFrame:
            if t_id is None:
                t_id: bool = df.loc[0, "game_home_team_id"]
                at_home = True
            else:
                at_home: bool = df.loc[0, "game_home_team_id"] == t_id
            g_count: int = 0
            df["Leg"] = None
            df["LegCount"] = 0
            for i, row in df.iterrows():
                if at_home:
                    if row["game_home_team_id"] == t_id:
                        g_count += 1
                    else:
                        g_count = 1
                        at_home = False
                else:
                    if row["game_away_team_id"] == t_id:
                        g_count += 1
                    else:
                        g_count = 1
                        at_home = True
                df.loc[i, ["Leg", "LegCount"]] = ["H" if at_home else "A", g_count]

            return df


        display_df_paginated(
            calc_leg(df_sel_team_games_left),
            "df_sel_team_games_left_legs",
            key="df_sel_team_games_left_legs",
            hide_index=False
        )

        df_sel_team_games_left_same_conf: pd.DataFrame = df_sel_team_games_left[
            df_sel_team_games_left["conferenceAbbrev"] == df_sel_team_games_left["conferenceAbbrev_AT"]
            ]

        display_df_paginated(
            df_sel_team_games_left_same_conf,
            "df_sel_team_games_left_same_conf",
            key="df_sel_team_games_left_same_conf"
        )

        df_sel_team_games_left_same_div: pd.DataFrame = df_sel_team_games_left_same_conf[
            df_sel_team_games_left_same_conf["divisionAbbrev"] == df_sel_team_games_left_same_conf["divisionAbbrev_AT"]
            ]

        display_df_paginated(
            df_sel_team_games_left_same_div,
            "df_sel_team_games_left_same_div",
            key="df_sel_team_games_left_same_div"
        )

        df_sel_team_games_left_adj_div: pd.DataFrame = df_sel_team_games_left_same_conf[
            ~df_sel_team_games_left_same_conf.index.isin(df_sel_team_games_left_same_div.index.tolist())]

        display_df_paginated(
            df_sel_team_games_left_adj_div,
            "df_sel_team_games_left_adj_div",
            key="df_sel_team_games_left_adj_div"
        )

        sel_team_conf = ser_sel_team["conferenceAbbrev"]
        df_sel_team_games_left_opp_conf: pd.DataFrame = df_sel_team_games_left[
            (df_sel_team_games_left["conferenceAbbrev"] != sel_team_conf)
            | (df_sel_team_games_left["conferenceAbbrev_AT"] != sel_team_conf)
            ]

        display_df_paginated(
            df_sel_team_games_left_opp_conf,
            "df_sel_team_games_left_opp_conf",
            key="df_sel_team_games_left_opp_conf"
        )


elif pills_mode == options_pills_mode[0]:

    # Jerseys
    k_pl_id: str = "key_pl_id"
    display_df_paginated(
        nhl_jc.df_jerseys,
        "nhl_jc.df_jerseys",
        key="nhl_jc.df_jerseys"
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
    display_df_paginated(
        df_selected_jersey,
        "A df_selected_jersey",
        key="A df_selected_jersey"
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
    # display_df_paginated(
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
        display_df_paginated(
            df_selected_jersey,
            "C df_selected_jersey",
            key="C df_selected_jersey"
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
            display_df_paginated(ser_selected_jersey, "ser_selected_jersey", key="ser_selected_jersey")
            pl_team = nhl.lookup_team(ser_selected_jersey["t_id"])
            # pl_obj.team = pl_team

        image_cols = st.columns(4)
        image_cols[0].image(pl_obj.path_team_logo, width=300)
        image_cols[1].image(pl_obj.birth_country.image_url, width=300)
        image_cols[2].image(pl_obj.path_headshot_logo, width=300)
        image_cols[3].image(pl_obj.path_hero_shot_logo, width=300)

        pl_obj_featured_stats_season, df_pl_obj_featured_stats = pl_obj.featured_stats
        display_df_paginated(df_pl_obj_featured_stats, f"Featured Stats {f_season(pl_obj_featured_stats_season)}",
                             key=f"Featured Stats {f_season(pl_obj_featured_stats_season)}")
        display_df_paginated(pl_obj.career_totals, "Career Totals", key="Career Totals")
        display_df_paginated(pl_obj.season_totals, "Season Totals", key="Season Totals")

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
            display_df_paginated(
                nhl.get_team_roster(pl_team.tri_code, pb=load_player_progress,
                                    pb_text=f"Loading {pl_team.full_name} Roster -- "),
                f"{pl_team.full_name} {f_season(get_this_season_str())} Team Roster",
                key=f"{pl_team.full_name} {f_season(get_this_season_str())} Team Roster"
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

    df_nhl_jerseys_w = nhl_jc.df_jerseys.copy()

    avg_spent_per_jersey_est: float = df_nhl_jerseys_w["PriceCalc"].mean()

    k_checkbox_use_avg_instead_actual: str = "key_checkbox_use_avg_instead_actual"
    st.session_state.setdefault(k_checkbox_use_avg_instead_actual, False)
    checkbox_use_avg_instead_actual = st.checkbox(
        label=f"Use {money(avg_spent_per_jersey_est)} instead of {money(0)}?",
        key=k_checkbox_use_avg_instead_actual
    )

    df_nhl_jerseys_w = df_nhl_jerseys_w.loc[df_nhl_jerseys_w["Cancelled"] != 1]
    df_nhl_jerseys_w["PriceCalc"] = df_nhl_jerseys_w["PriceCalc"].fillna(
        0 if not checkbox_use_avg_instead_actual else avg_spent_per_jersey_est)
    df_nhl_jerseys_w["PriceCalcSum"] = df_nhl_jerseys_w["PriceCalc"].cumsum()
    df_nhl_jerseys_w['Colours'] = df_nhl_jerseys_w.apply(
        lambda row: f"{row['Colour1']} {row['Colour2']} {row['Colour3']}", axis=1)
    cols_timeline_order_open = ["OrderDate", "OpenDate", "ID", "Colours", "JerseyToString"]
    df_timeline_order_open = df_nhl_jerseys_w[cols_timeline_order_open]
    st.dataframe(df_timeline_order_open)
    # df_timeline_order_receive["Event"] = df_timeline_order_receive.apply(lambda row: print(f"{row=}"))
    # df_timeline_order_receive["Event"] = df_timeline_order_receive.apply(lambda row: print(f"{row=}"))
    df_timeline_order_open = df_timeline_order_open.rename(
        columns={"OrderDate": "Start Date", "OpenDate": "End Date"})

    df_timeline_order_open['Start Date'] = pd.to_datetime(df_timeline_order_open['Start Date'])
    df_timeline_order_open["Category"] = df_timeline_order_open.apply(
        lambda row: "Yet To Open" if pd.isna(row["End Date"]) else "Opened", axis=1)
    df_timeline_order_open['Not Open'] = pd.isna(df_timeline_order_open['End Date'])
    df_timeline_order_open['End Date'] = pd.to_datetime(df_timeline_order_open['End Date']).fillna(pd.Timestamp.now())
    df_timeline_order_open['End Date'] = df_timeline_order_open['End Date'].apply(lambda ed: ed + pd.Timedelta(days=1))
    df_timeline_order_open["DDiff"] = df_timeline_order_open.apply(
        lambda row: (row["End Date"] - row["Start Date"]).days, axis=1)

    avg_ddiff = df_timeline_order_open.loc[df_timeline_order_open["Not Open"] == False, "DDiff"].mean()
    st.metric(
        label="Average Days Order to Open:",
        value=avg_ddiff
    )

    st.divider()

    k_check_opened_only: str = "key_check_opened_only"
    st.session_state.setdefault(k_check_opened_only, True)
    check_opened_only = st.checkbox(
        label="Opened Only?",
        key=k_check_opened_only
    )
    k_check_include_blanks: str = "key_check_include_blanks"
    st.session_state.setdefault(k_check_include_blanks, True)
    check_include_blanks = st.checkbox(
        label="Include Blanks?",
        key=k_check_include_blanks
    )
    lst_jersey_leagues = df_nhl_jerseys_w["League"].dropna().unique().tolist()
    k_multiselect_leagues: str = "key_multiselect_leagues"
    st.session_state.setdefault(k_multiselect_leagues, lst_jersey_leagues)
    multiselect_leagues = st.multiselect(
        label="Leagues:",
        key=k_multiselect_leagues,
        options=lst_jersey_leagues
    )

    df_jerseys_stats: pd.DataFrame = nhl_jc.df_jerseys.copy()
    df_jerseys_stats["PriceCalc"] = df_jerseys_stats["PriceCalc"].fillna(
        0 if not checkbox_use_avg_instead_actual else avg_spent_per_jersey_est)
    df_jerseys_stats["PriceCalcSum"] = df_jerseys_stats["PriceCalc"].cumsum()
    df_jerseys_stats = df_jerseys_stats[df_jerseys_stats["League"].isin(multiselect_leagues)]
    if check_opened_only:
        df_jerseys_stats = df_jerseys_stats[~df_jerseys_stats["OpenDate"].isna()]
    if not check_include_blanks:
        df_jerseys_stats = df_jerseys_stats[~df_jerseys_stats["Number"].isna()]

    cont_metrics = st.container(border=True)
    with cont_metrics.expander("Data"):
        display_df_paginated(
            df_jerseys_stats,
            "Jerseys:",
            key="Jerseys:"
        )
    n_met_cols = 4
    # cols_metrics_0 = cont_metrics.columns(5)
    # cols_metrics_1 = cont_metrics.columns(5)

    ttl_number_jerseys = df_jerseys_stats.shape[0]
    ttl_number_blank_jerseys = df_jerseys_stats[df_jerseys_stats["Number"].isna()].shape[0]
    ttl_number_jerseys_to_open = df_jerseys_stats[pd.isna(df_jerseys_stats["OpenDate"])].shape[0]
    ttl_number_jerseys_ordered = df_jerseys_stats[pd.isna(df_jerseys_stats["ReceiveDate"])].shape[0]
    ttl_number_jerseys_no_price = df_jerseys_stats[df_jerseys_stats["PriceCalc"].isna()].shape[0]
    ttl_spent_on_jerseys = df_jerseys_stats["PriceCalc"].sum()
    avg_spent_per_jersey = df_jerseys_stats["PriceCalc"].mean()
    est_missing_price = ttl_number_jerseys_no_price * avg_spent_per_jersey
    est_total_price = ttl_spent_on_jerseys + est_missing_price
    first_order_date = df_jerseys_stats["OrderDate"].min()
    last_order_date = df_jerseys_stats["OrderDate"].max()
    ttl_days = (datetime.datetime.now() - first_order_date).days
    days_since_last_order = (datetime.datetime.now() - last_order_date).days
    est_spent_per_day = est_total_price / ttl_days
    est_savings_since_last_order = days_since_last_order * est_spent_per_day
    est_dollars_per_day_if_no_spending = -1
    est_dollars_saved_if_no_spending_today = -1

    metrics = [
        {
            "label": "Total # Jerseys",
            "value": ttl_number_jerseys
        },
        {
            "label": "Total # Blank Jerseys:",
            "value": ttl_number_blank_jerseys
        },
        {
            "label": "Total # Jerseys To Open:",
            "value": ttl_number_jerseys_to_open
        },
        {
            "label": "Total # Jerseys Ordered:",
            "value": ttl_number_jerseys_ordered
        },
        {
            "label": "Total # Jerseys No Price:",
            "value": ttl_number_jerseys_no_price
        },
        {
            "label": "Total Spent:",
            "value": money(ttl_spent_on_jerseys)
        },
        {
            "label": "Average Spent:",
            "value": money(avg_spent_per_jersey)
        },
        {
            "label": "Estimated Missing Price:",
            "value": money(est_missing_price)
        },
        {
            "label": "Estimated Total Price:",
            "value": money(est_total_price)
        },
        {
            "label": "First Order Date:",
            "value": date_str_format(first_order_date)
        },
        {
            "label": "Last Order Date:",
            "value": date_str_format(last_order_date)
        },
        {
            "label": "Total Days:",
            "value": ttl_days
        },
        {
            "label": "Days Since Last Order:",
            "value": days_since_last_order
        },
        {
            "label": "Estimated $ / Day:",
            "value": money(est_spent_per_day)
        },
        {
            "label": "Estimated Savings Since Last Order:",
            "value": money(est_savings_since_last_order)
        },
        {
            "label": "Estimated $ / Day If No Spending:",
            "value": money(est_dollars_per_day_if_no_spending)
        },
        {
            "label": "Estimated $ Saved If No Spending Today:",
            "value": money(est_dollars_saved_if_no_spending_today)
        }
    ]

    met_cols = [
        cont_metrics.columns(n_met_cols)
        for i in range(int(math.ceil(len(metrics) / n_met_cols)))
    ]
    for i, met_data in enumerate(metrics):
        r_idx = i // n_met_cols
        c_idx = i % n_met_cols
        with met_cols[r_idx][c_idx]:
            st.metric(
                **met_data,
                border=True
            )

    # with cols_metrics_0[0]:
    #     st.metric(
    #         label="Total # Jerseys:",
    #         value=ttl_number_jerseys,
    #         border=True
    #     )
    #
    # with cols_metrics_0[1]:
    #     st.metric(
    #         label="Total # Blank Jerseys:",
    #         value=ttl_number_blank_jerseys,
    #         border=True
    #     )
    #
    # with cols_metrics_0[2]:
    #     st.metric(
    #         label="Total # Jerseys No Price:",
    #         value=ttl_number_jerseys_no_price,
    #         border=True
    #     )
    #
    # with cols_metrics_0[3]:
    #     st.metric(
    #         label="Total Spent:",
    #         value=money(ttl_spent_on_jerseys),
    #         border=True
    #     )
    #
    # with cols_metrics_0[4]:
    #     st.metric(
    #         label="Average Spent:",
    #         value=money(avg_spent_per_jersey),
    #         border=True
    #     )
    #
    # with cols_metrics_1[0]:
    #     st.metric(
    #         label="Estimated Missing Price:",
    #         value=money(est_missing_price),
    #         border=True
    #     )
    #
    # with cols_metrics_1[1]:
    #     st.metric(
    #         label="Estimated Total Price:",
    #         value=money(est_total_price),
    #         border=True
    #     )
    #
    # with cols_metrics_1[2]:
    #     st.metric(
    #         label="First Order Date:",
    #         value=date_str_format(first_order_date),
    #         border=True
    #     )
    #
    # with cols_metrics_1[3]:
    #     st.metric(
    #         label="Last Order Date:",
    #         value=date_str_format(last_order_date),
    #         border=True
    #     )
    #
    # with cols_metrics_1[4]:
    #     st.metric(
    #         label="Total Days:",
    #         value=ttl_days,
    #         border=True
    #     )

    with st.expander("Timeline of Jerseys"):
        # df_timeline_order_open["Event"] = df_timeline_order_open.apply(
        #     lambda row:
        #     ", ".join(map(str, df_nhl_jerseys_w.loc[
        #         df_nhl_jerseys_w["ID"] == row["ID"],
        #         ["Number", "PlayerFirst", "PlayerLast", "Team", "Brand", "Make", "Colours"]
        #     ].iloc[0].values)) + " Dates between: " + str(row["DDiff"]),
        #     axis=1
        # )
        df_timeline_order_open["Event"] = df_timeline_order_open["JerseyToString"]
        del df_timeline_order_open["ID"]
        df_timeline_order_open.sort_values(
            by=["End Date", "DDiff"],
            inplace=True
        )

        # Create a Gantt-like timeline using Plotly
        fig_timeline_order_open = px.timeline(
            df_timeline_order_open,
            x_start='Start Date',
            x_end='End Date',
            y='Event',
            title='Time Between Order to Open date',
            color='Category',
            color_discrete_map={
                'Yet To Open': 'red',
                'Medium': 'orange',
                'Opened': 'green'
            }
        )

        # Update layout to make it more readable
        fig_timeline_order_open.update_layout(xaxis_title="Date", yaxis_title="Order Date to Open Date", height=2000)

        # Display in Streamlit
        st.plotly_chart(fig_timeline_order_open)

    with st.expander("Total Spent By Day"):
        df_nhl_jerseys_w["PriceCalcSum2"] = df_nhl_jerseys_w["PriceCalc"].fillna(0).replace(0,
                                                                                            avg_spent_per_jersey_est).cumsum()
        df_nhl_jerseys_w["PriceCalcSum3"] = df_nhl_jerseys_w["PriceCalc"].fillna(0).replace(0, avg_spent_per_jersey_est)
        # chart1 = px.area(
        #     df_nhl_jerseys_w,
        #     x="OrderDate",
        #     y="PriceCalcSum"
        # )
        # chart2 = px.area(
        #     df_nhl_jerseys_w,
        #     x="OrderDate",
        #     y="PriceCalcSum2"
        # )
        # st.plotly_chart(chart1 + chart2)
        x_vals = df_nhl_jerseys_w["OrderDate"]
        y1 = df_nhl_jerseys_w["PriceCalcSum"]
        y2 = df_nhl_jerseys_w["PriceCalcSum2"]

        fig = go.Figure()
        # Area 1
        fig.add_trace(go.Scatter(
            x=x_vals, y=y1,
            mode='lines',
            name='Actual Spend',
            fill='tozeroy',
            line=dict(color='royalblue')
        ))

        # Area 2
        fig.add_trace(go.Scatter(
            x=x_vals, y=y2,
            mode='lines',
            name='Estimated Spend',
            fill='tozeroy',
            line=dict(color='orange')
        ))

        # --- Trendlines ---
        # Fit polynomials or linear trendlines (or use your own logic)
        z1 = np.polyfit(pd.to_numeric(x_vals), y1, 1)
        z2 = np.polyfit(pd.to_numeric(x_vals), y2, 1)

        trendline1 = np.poly1d(z1)(pd.to_numeric(x_vals))
        trendline2 = np.poly1d(z2)(pd.to_numeric(x_vals))

        fig.add_trace(go.Scatter(
            x=x_vals, y=trendline2,
            mode='lines',
            name='Trend (Estimated)',
            line=dict(dash='dash', color='darkorange')
        ))

        fig.add_trace(go.Scatter(
            x=x_vals, y=trendline1,
            mode='lines',
            name='Trend (Actual)',
            line=dict(dash='dash', color='blue')
        ))

        fig.update_layout(
            title="Total Spent Over Time",
            xaxis_title="Order Date",
            yaxis_title="Cumulative Spend",
            hovermode="x unified",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

        #############################

        k_checkbox_center_rolling: str = "key_checkbox_center_rolling"
        st.session_state.setdefault(k_checkbox_center_rolling, False)
        checkbox_center_rolling = st.checkbox(
            label="Center Rolling Averages?",
            key=k_checkbox_center_rolling
        )

        df_nhl_jerseys_w_d: pd.DataFrame = df_nhl_jerseys_w.copy()
        df_dates = pd.DataFrame({"date": pd.date_range(df_nhl_jerseys_w_d["OrderDate"].min(),
                                                       datetime.datetime.now().date() + datetime.timedelta(days=1))})

        df_nhl_jerseys_w_d = df_dates.merge(
            df_nhl_jerseys_w_d.groupby(
                by="OrderDate"
            ).agg({
                "PriceCalcSum3": "sum"
            }),
            left_on="date",
            right_on="OrderDate",
            how="left"
        ).rename(columns={
            "PriceCalcSum3": "SumPrice_Date",
            "date": "Date"
        })

        df_nhl_jerseys_w_d["SumPrice_Date"] = df_nhl_jerseys_w_d["SumPrice_Date"].fillna(0)
        df_nhl_jerseys_w_d["SumPrice"] = df_nhl_jerseys_w_d["SumPrice_Date"].cumsum()
        df_nhl_jerseys_w_d = df_nhl_jerseys_w_d[["Date", "SumPrice_Date", "SumPrice"]]
        ys = []
        x_vals = df_nhl_jerseys_w_d["Date"]
        fig = go.Figure()
        # colours_grad = gradient_merge(["royalblue", "teal", "seafoam-green", "green"], as_hex=True)
        windows = [3, 7, 28, 90, 180, 365, 730, 1100, 1460, 1825]
        colours_to_use = ["orangered", "green", "royalblue"]
        colours_grad = gradient_merge(colours_to_use, steps=-(-len(windows) // len(colours_to_use)), as_hex=True)
        st.write("colours_grad")
        st.write(colours_grad)
        for i, wind in enumerate(windows):
            n_col = f"RollAvg_{wind}"
            df_nhl_jerseys_w_d[n_col] = df_nhl_jerseys_w_d["SumPrice_Date"].rolling(
                window=wind,
                center=checkbox_center_rolling
            ).mean()
            ys.append(df_nhl_jerseys_w_d[n_col])
            fig.add_trace(go.Scatter(
                x=x_vals, y=ys[-1],
                mode='lines',
                name=f'Rolling Avg {wind} days',
                fill='tozeroy',
                line=dict(color=colours_grad[i])
            ))

            z1 = np.polyfit(pd.to_numeric(x_vals), ys[-1], 1)
            trendline = np.poly1d(z1)(pd.to_numeric(x_vals))

            fig.add_trace(go.Scatter(
                x=x_vals, y=trendline,
                mode='lines',
                name=f'Trend {wind} days',
                line=dict(dash='dash', color=Colour(colours_grad[i]).darken(0.25).hex_code)
            ))

        fig.update_layout(
            title="Rolling Average Spent Over Time",
            xaxis_title="Order Date",
            yaxis_title="Average Spend",
            hovermode="x unified",
            template="plotly_dark"
        )

        # fig.show(
        #     config={
        #         "scrollZoom": True
        #     }
        # )
        st.plotly_chart(fig, use_container_width=True)

        display_df_paginated(
            df_nhl_jerseys_w_d,
            "df_nhl_jerseys_w_d",
            key="df_nhl_jerseys_w_d"
        )

else:

    # Test

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
        display_df_paginated(
            df_known_urls,
            "df_known_urls",
            key="df_known_urls"
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

#
# fu = st.file_uploader(
#     label="files",
#     type=["png", "jpeg"],
#     accept_multiple_files=True,
#     key="fu"
# )
#
# if fu:
#     for f in fu:
#         dst = os.path.join(r"D:\3D Prints\QMJHL Logos", f.name)
#         print(f"{dst=}")
#         st.write(f"{dst=}")
#         if not os.path.exists(dst):
#             with open(dst, "wb") as out:
#                 out.write(f.getvalue())
#
#
# st.download_button(
#     "download",
#     data=open(r"D:\Important documents\Bills\crv_registration_2026.pdf", "rb").read(),
#     file_name="crv_2026.pdf",
#     mime="application/pdf",
#     key=f"drive_1"
# )

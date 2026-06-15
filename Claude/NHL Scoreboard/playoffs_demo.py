from streamlit_utility import display_df, get_selected_rows
from datetime_utility import date_str_format
import plotly.graph_objects as go
from utility import flatten
import plotly.express as px
from io import BytesIO
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import cairosvg
import requests
import glob
import os


st.set_page_config(layout="wide")


path_excel_playoffs = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\2026\My Predictions2026.xlsm.xlsx"
MAX_GOALS_PER_GAME = 18

TEAM_META = {
    "ANA": {"name": "Anaheim Ducks",       "conf": "Western", "div": "Pacific",    "id": 24, "active": True},
    # "ARI": {"name": "Utah Hockey Club",     "conf": "Western", "div": "Central",    "id": 53, "active": False},
    "UTA": {"name": "Utah Hockey Club",     "conf": "Western", "div": "Central",    "id": 59, "active": True},
    "BOS": {"name": "Boston Bruins",        "conf": "Eastern", "div": "Atlantic",   "id": 6, "active": True},
    "BUF": {"name": "Buffalo Sabres",       "conf": "Eastern", "div": "Atlantic",   "id": 7, "active": True},
    "CGY": {"name": "Calgary Flames",       "conf": "Western", "div": "Pacific",    "id": 20, "active": True},
    "CAR": {"name": "Carolina Hurricanes",  "conf": "Eastern", "div": "Metropolitan","id": 12, "active": True},
    "CHI": {"name": "Chicago Blackhawks",   "conf": "Western", "div": "Central",    "id": 16, "active": True},
    "COL": {"name": "Colorado Avalanche",   "conf": "Western", "div": "Central",    "id": 21, "active": True},
    "CBJ": {"name": "Columbus Blue Jackets","conf": "Eastern", "div": "Metropolitan","id": 29, "active": True},
    "DAL": {"name": "Dallas Stars",         "conf": "Western", "div": "Central",    "id": 25, "active": True},
    "DET": {"name": "Detroit Red Wings",    "conf": "Eastern", "div": "Atlantic",   "id": 17, "active": True},
    "EDM": {"name": "Edmonton Oilers",      "conf": "Western", "div": "Pacific",    "id": 22, "active": True},
    "FLA": {"name": "Florida Panthers",     "conf": "Eastern", "div": "Atlantic",   "id": 13, "active": True},
    "LAK": {"name": "Los Angeles Kings",    "conf": "Western", "div": "Pacific",    "id": 26, "active": True},
    "MIN": {"name": "Minnesota Wild",       "conf": "Western", "div": "Central",    "id": 30, "active": True},
    "MTL": {"name": "Montréal Canadiens",   "conf": "Eastern", "div": "Atlantic",   "id": 8, "active": True},
    "NSH": {"name": "Nashville Predators",  "conf": "Western", "div": "Central",    "id": 18, "active": True},
    "NJD": {"name": "New Jersey Devils",    "conf": "Eastern", "div": "Metropolitan","id": 1, "active": True},
    "NYI": {"name": "New York Islanders",   "conf": "Eastern", "div": "Metropolitan","id": 2, "active": True},
    "NYR": {"name": "New York Rangers",     "conf": "Eastern", "div": "Metropolitan","id": 3, "active": True},
    "OTT": {"name": "Ottawa Senators",      "conf": "Eastern", "div": "Atlantic",   "id": 9, "active": True},
    "PHI": {"name": "Philadelphia Flyers",  "conf": "Eastern", "div": "Metropolitan","id": 4, "active": True},
    "PIT": {"name": "Pittsburgh Penguins",  "conf": "Eastern", "div": "Metropolitan","id": 5, "active": True},
    "SJS": {"name": "San Jose Sharks",      "conf": "Western", "div": "Pacific",    "id": 28, "active": True},
    "SEA": {"name": "Seattle Kraken",       "conf": "Western", "div": "Pacific",    "id": 55, "active": True},
    "STL": {"name": "St. Louis Blues",      "conf": "Western", "div": "Central",    "id": 19, "active": True},
    "TBL": {"name": "Tampa Bay Lightning",  "conf": "Eastern", "div": "Atlantic",   "id": 14, "active": True},
    "TOR": {"name": "Toronto Maple Leafs",  "conf": "Eastern", "div": "Atlantic",   "id": 10, "active": True},
    "VAN": {"name": "Vancouver Canucks",    "conf": "Western", "div": "Pacific",    "id": 23, "active": True},
    "VGK": {"name": "Vegas Golden Knights", "conf": "Western", "div": "Pacific",    "id": 54, "active": True},
    "WSH": {"name": "Washington Capitals",  "conf": "Eastern", "div": "Metropolitan","id": 15, "active": True},
    "WPG": {"name": "Winnipeg Jets",        "conf": "Western", "div": "Central",    "id": 52, "active": True},
}


@st.cache_data
def load_scores() -> tuple[dict, pd.DataFrame]:
    df = pd.read_excel(path_excel_playoffs)
    cols_to_drop = [c for c in df.columns if c.lower().startswith("unnamed")]
    df = df.drop(columns=cols_to_drop)
    col_dict = {col.lower(): col for col in df.columns}
    df.columns = [col.lower() for col in df.columns]
    df = df[~pd.isna(df["gameid"])]
    yn_cols = [
        "correct", "gameover", "awaywon", "homewon",
        "hasot", "awaywasshutout", "homewasshutout"
    ]
    int_cols = [
        "gameid", "seriesid", "roundnum", "gamenum",
        "topseedwins", "lowseedwins", "pawayscore",
        "phomescore", "aawayscore", "ahomescore",
        "otroundnum", "timeinseconds", 
        "diffawaygoals", "diffhomegoals", 
    ]
    for col in yn_cols:
        df[col] = df[col].apply(lambda v: bool(v) if not pd.isna(v) else False)
    for col in int_cols:
        df[col] = df[col].apply(lambda v: int(v) if not pd.isna(v) else 0)
    return col_dict, df


@st.cache_data()
def fetch_game_landing(g_id) -> dict:
    """Load NHL game landing for given game ID"""
    try:
        url = f"https://api-web.nhle.com/v1/gamecenter/{g_id}/landing"
        # st.write(url)
        return requests.get(url).json()
    except Exception:
        return {}


@st.cache_data
def fetch_team_logo(team_abbr: str, dark: bool = True, err_on_not_found: bool = False) -> str:
    """Get NHL team logo URL from NHL API."""
    if str(team_abbr).upper() not in TEAM_META:
        if err_on_not_found:
            raise ValueError(f"{team_abbr=} not found in TEAM_META")        
        return ""
    return f"https://assets.nhle.com/logos/nhl/svg/{team_abbr.upper()}_{'dark' if dark else 'light'}.svg"


@st.cache_data(show_spinner=False)
def fetch_team_logo_png_image(
    team_abbr: str,
    dark: bool = True,
    output_width: int = 256,
    output_height: int = 256,
) -> Image.Image | None:
    try:
        url = fetch_team_logo(team_abbr, dark=dark)

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        png_bytes = cairosvg.svg2png(
            bytestring=response.content,
            output_width=output_width,
            output_height=output_height,
        )

        img = Image.open(BytesIO(png_bytes)).convert("RGBA")
        return img
    
    except Exception as e:
        st.warning(f"Could not load logo for {team_abbr}: {e}")
        return None


def g_key(num, mode: str = "i") -> str:
    if mode == "p":
        return f"g{str(num).rjust(2, '0')}_playername"
    elif mode == "t":
        return f"g{str(num).rjust(2, '0')}_team"
    else:
        return f"g{str(num).rjust(2, '0')}_playerid"


def a_key(num, a_num: int = 1, mode: str = "i") -> str:
    if mode == "p":
        return f"g{str(num).rjust(2, '0')}_a{a_num}_playername"
    elif mode == "t":
        return f"g{str(num).rjust(2, '0')}_a{a_num}_team"
    else:
        return f"g{str(num).rjust(2, '0')}_a{a_num}_playerid"


def extract_scoring(game_data: dict) -> pd.DataFrame:
    
    # score_cols = ["gameid"] + flatten([
    #     [
    #         f"g{str(i).rjust(2, '0')}_team", f"g{str(i).rjust(2, '0')}_playerid", f"g{str(i).rjust(2, '0')}_playername",
    #         f"g{str(i).rjust(2, '0')}_a1_playerid", f"g{str(i).rjust(2, '0')}_a1_playername",
    #         f"g{str(i).rjust(2, '0')}_a2_playerid", f"g{str(i).rjust(2, '0')}_a2_playername"
    #     ]
    #     for i in range(1, MAX_GOALS_PER_GAME + 1)
    # ])
    
    score_cols = ["gameid", "seriescode", "round", "gamenum"] + flatten([
        [
            g_key(i, "t"), g_key(i, "i"), g_key(i, "p"),
            a_key(i, 1, "i"), a_key(i, 1, "p"),
            a_key(i, 2, "i"), a_key(i, 2, "p"),
        ]
        for i in range(1, MAX_GOALS_PER_GAME + 1)
    ])
    
    # st.write(score_cols)
    
    df = pd.DataFrame([{col: None for col in score_cols}])
    id_ = game_data.get("id")
    roundnum, seriescode, gamenum = str(id_)[-3:]
    summary = game_data.get("summary", {})
    g_num = 0
    if summary:
        df.loc[0, ["gameid", "seriescode", "round", "gamenum"]] = id_, seriescode, roundnum, gamenum
        scoring = summary.get("scoring", [])
        for i, score_data in enumerate(scoring):
            goals = score_data.get("goals", [])
            for j, goal_data in enumerate(goals):
                g_num += 1
                goal_key = f"g{str(g_num).rjust(2, '0')}_"
                scorer_id = goal_data.get("playerId")
                scorer_team = goal_data.get("teamAbbrev", {}).get("default")
                scorer_name = goal_data.get("name", {}).get("default")
                assists = goal_data.get("assists", [])
                df.loc[0, f"{goal_key}team"] = scorer_team
                df.loc[0, f"{goal_key}playerid"] = scorer_id
                df.loc[0, f"{goal_key}playername"] = scorer_name
                for k, assist_data in enumerate(assists, start=1):
                    assist_key = f"{goal_key}a{k}_"
                    assist_id = assist_data.get("playerId")
                    # assist_team = assist_data.get("teamAbbrev", {}).get("default")
                    assist_name = assist_data.get("name", {}).get("default")
                    df.loc[0, f"{assist_key}playerid"] = assist_id
                    df.loc[0, f"{assist_key}playername"] = assist_name
        
    return df


def extract_player_scoring(df_game_scoring) -> pd.DataFrame:
    debug = False
    
    goal_id_cols = flatten([
        [g_key(i, "i"), a_key(i, 1, "i"), a_key(i, 2, "i")]
        for i in range(1, MAX_GOALS_PER_GAME + 1)
    ])
    
    df = pd.DataFrame(columns=["player", "team", "id", "g", "a", "pts", "gp"])
    idx = 0
    for j, row in df_game_scoring.iterrows():
        if debug:
            st.divider()
        for i in range(1, MAX_GOALS_PER_GAME + 1):    
            gk_i, gk_p, gk_t = map(lambda m: g_key(i, m), ["i", "p", "t"])
            a1k_i, a1k_p = map(lambda m: a_key(i, 1, m), ["i", "p"])
            a2k_i, a2k_p = map(lambda m: a_key(i, 2, m), ["i", "p"])
            
            g_i, g_p, g_t = row[[gk_i, gk_p, gk_t]]
            a1_i, a1_p = row[[a1k_i, a1k_p]]
            a2_i, a2_p = row[[a2k_i, a2k_p]]
            
            if debug:
                if "M. Marner" not in [g_p, a1_p, a2_p]:
                    continue
            
            df_g = df[df["id"] == g_i]
            df_a1 = df[df["id"] == a1_i]
            df_a2 = df[df["id"] == a2_i]
            if g_i:
                if debug:
                    st.write(f"{g_i=}, {g_p=}, {g_t=}")
                if df_g.empty:
                    df.loc[idx, ["player", "team", "id", "g", "a", "gp"]] = [g_p, g_t, g_i, 1, 0, 0]
                    idx += 1
                else:
                    if debug:
                        with st.container(horizontal=True):
                            st.write(df_g.index.tolist())
                            display_df(df, "Goals DF {j=}, {i=}")
                    df.loc[df_g.index, "g"] += 1
            if a1_i:
                if debug:
                    st.write(f"{a1_i=}, {a1_p=}, {g_t=}")
                if df_a1.empty:
                    df.loc[idx, ["player", "team", "id", "g", "a", "gp"]] = [a1_p, g_t, a1_i, 0, 1, 0]
                    idx += 1
                else:
                    if debug:
                        st.write(df_a1.index.tolist())
                    df.loc[df_a1.index, "a"] += 1
            if a2_i:
                if debug:
                    st.write(f"{a2_i=}, {a2_p=}, {g_t=}")
                if df_a2.empty:
                    df.loc[idx, ["player", "team", "id", "g", "a", "gp"]] = [a2_p, g_t, a2_i, 0, 1, 0]
                    idx += 1
                else:
                    if debug:
                        st.write(df_a2.index.tolist())
                    df.loc[df_a2.index, "a"] += 1

        game_pts_ids = list(set([row[col] for col in goal_id_cols if not pd.isna(row[col])]))
        df.loc[df["id"].isin(game_pts_ids), "gp"] += 1
    
    df["pts"] = df["g"] + df["a"]
    df["ppg"] = df["pts"] / df["gp"]
    
    # for i, row in df.iterrows():
    #     df["gp"] = sum(map(len, flatten(df_game_scoring[goal_id_cols].values.tolist())))
    df = df.sort_values(["pts", "g", "a"], ascending=False)
    df_m = pd.DataFrame(TEAM_META)
    for col in df_m.columns:
        df_m.loc["div", col] = df_m.loc["div", col][:1].upper()
        df_m.loc["conf", col] = df_m.loc["conf", col][:1].upper()
    df_m = df_m.transpose().reset_index(names="team")
    # display_df(
    #     df_m,
    #     "df_m",
    #     hide_index=False
    # )
    df = df.merge(
        df_m[["team", "conf", "div"]],
        "inner",
        on="team"
    )
    return df
        

    # keys_goals_names = [g_key(i, "p") for i in range(1, MAX_GOALS_PER_GAME + 1)]
    # keys_assists_names = flatten([[a_key(i, 1, "p"), a_key(i, 2, "p")] for i in range(1, MAX_GOALS_PER_GAME + 1)])
    # players_goals = [p for p in flatten(df_game_scoring[keys_goals_names].values.tolist()) if not pd.isna(p)]
    # players_assists = [p for p in flatten(df_game_scoring[keys_assists_names].values.tolist()) if not pd.isna(p)]
    # players = players_goals + players_assists
    # players = list(set(players))
    # players.sort()
    # df = pd.DataFrame([{"player": p, "goals": 0, "assists": 0} for p in players])
    # df_g = pd.DataFrame({"player": players_goals})
    # df_g_c = df_g.value_counts().reset_index()
    # df_a = pd.DataFrame({"player": players_assists})
    # df_a_c = df_a.value_counts().reset_index()
    # display_df(df_g_c, "df_g_c")
    # display_df(df_a_c, "df_a_c")
    
    # for i, row in df.copy().iterrows():
    #     p = row["player"]
    #     df_g_p = df_g_c[df_g_c["player"] == p].reset_index()
    #     df_a_p = df_a_c[df_a_c["player"] == p].reset_index()
    #     if not df_g_p.empty:
    #         df.loc[i, "goals"] = df_g_p.iloc[0]["count"]
    #     if not df_a_p.empty:
    #         df.loc[i, "assists"] = df_a_p.iloc[0]["count"]
    # df["points"] = df["goals"] + df["assists"]
    # return df


def scoring_summaries(df_playoffs, df_game_scoring) -> pd.DataFrame:
    cols = [
        "gameid", "awayteam", "hometeam", "winner",
        "seriescode", "round", "gamenum",
    ] + int_record_cols + team_cols_b
    
    # st.write(score_cols)
    # st.write("df_game_scoring")
    # st.write(df_game_scoring)
    
    df = pd.DataFrame([{col: None for col in cols}])
    idx = 0
    
    for i, row in df_game_scoring.iterrows():
        s_code, roundnum, gamenum = row[["seriescode", "round", "gamenum"]]
        # st.write(f"X {i=}, {s_code=}, {roundnum=}, {gamenum=}")
        df_p = df_playoffs[
            (df_playoffs["seriesid"].fillna(0).astype(int) == int(s_code))
            & (df_playoffs["roundnum"].fillna(0).astype(int) == int(roundnum))
            & (df_playoffs["gamenum"].fillna(0).astype(int) == int(gamenum))
        ].reset_index()
        # display_df(df_p, f"{i=}, {s_code=}, {roundnum=}, {gamenum=}")
        g_id, away_team, home_team = df_p.iloc[0][["gameid", "awayteam", "hometeam"]]
        # st.write(f"{i=}, {g_id=}, {away_team=}, {home_team=}")
        df.loc[idx, ["gameid", "seriescode", "round", "gamenum"]] = [g_id, s_code, roundnum, gamenum]
        df.loc[idx, "awayteam"] = away_team
        df.loc[idx, "hometeam"] = home_team
        
        scores = {t: {c: 0 for c in int_record_cols} for t in [away_team, home_team]}
        
        for col in team_cols_b:
            score_team = row[col]
            if pd.isna(score_team):
                break
            is_home = score_team == home_team
            scored_on_team = away_team if is_home else home_team
            scores[score_team]["gf_h" if is_home else "gf_a"] += 1
            scores[scored_on_team]["ga_a" if is_home else "ga_h"] += 1
            df.loc[idx, col] = score_team
        
        winner = home_team if scores[home_team]["gf_h"] > scores[away_team]["gf_a"] else away_team
        df.loc[idx, "winner"] = winner
        scores[away_team]["w_a" if winner == away_team else "l_a"] += 1
        scores[home_team]["w_h" if winner == home_team else "l_h"] += 1
        
        # st.write(f"scores: {winner=}")
        # st.write(pd.DataFrame(scores))
        
        for col in int_record_cols:
            df.loc[idx, col] = scores[away_team if col.endswith("_a") else home_team][col]
        
        idx += 1
        
    for col in int_record_cols:
        df[col] = df[col].apply(lambda v: int(v) if not pd.isna(v) else 0)
        
    return df


col_translation, df_playoffs = load_scores()

team_cols_a = ["topseed", "lowseed", "awayteam", "hometeam", "mychoice", "winner"]
team_cols_b = [
    g_key(i, "t")
    for i in range(1, MAX_GOALS_PER_GAME + 1)
]
int_record_cols = [
    "w_a", "l_a", "gf_a", "ga_a",
    "w_h", "l_h", "gf_h", "ga_h",
]

df_series = df_playoffs.groupby(["seriescode", "seriesid", "roundnum", "conf", "lowseed", "topseed"]).agg({"gamenum": "count"}).reset_index().sort_values(["roundnum", "seriesid"])

display_df(
    df_series,
    "df_series",
)
btns_pr = 8
image_size = 45
cols_btns = [st.columns(btns_pr) if (i % 2) == 0 else st.container() for i in range(9)]
keys_cb = {
    i: f"key_checkbox_conf={row['conf']}_round={row['roundnum']}_series={row['seriesid']}_top={row['topseed']}_low={row['lowseed']}"
    for i, row in df_series.iterrows()
}
c = 0
cr = None

with st.container(horizontal=True):
    with st.container(border=True, horizontal=True):
        if st.button("Clear Checkboxes"):
            st.session_state.update({k: False for k in keys_cb.values()})

        if st.button("All Checkboxes"):
            st.session_state.update({k: False for k in keys_cb.values()})
            st.session_state.update({k: True for k in keys_cb.values()})
        
    with st.container(border=True, horizontal=True):
        for i in range(4):
            if st.button(f"All Round {i+1}"):
                st.session_state.update({k: False for k in keys_cb.values()})
                st.session_state.update({k: True for k in keys_cb.values() if f"round={i+1}" in k})
            
    with st.container(border=True, horizontal=True):
        for i, team in enumerate(sorted(list(set(df_series[["lowseed", "topseed"]].values.flatten())))):
            if st.button(f"All Team {team}"):
                st.session_state.update({k: False for k in keys_cb.values()})
                st.session_state.update({k: True for k in keys_cb.values() if (f"top={team}" in k) or (f"low={team}" in k)})

for i, row in df_series.iterrows():
    seriesid = row["seriesid"]
    roundnum = row["roundnum"]
    conf = row["conf"]
    low_seed = row["lowseed"]
    top_seed = row["topseed"]
    k_cb = keys_cb[i]
    st.session_state.setdefault(k_cb, True)
    if cr != roundnum:
        cr = roundnum
        with cols_btns[(2 * roundnum) - 1]:
            st.divider()
            st.subheader(f"Round {roundnum}")
    with cols_btns[2 * roundnum][c % btns_pr]:
        with st.container(border=True):
            st.subheader(f"{conf.title()}")
            with st.container(horizontal=True):
                st.image(fetch_team_logo(top_seed), width=image_size)
                st.write("VS")
                st.image(fetch_team_logo(low_seed), width=image_size)
                st.checkbox(
                    label="label",
                    key=k_cb,
                    label_visibility="hidden",
                    # on_change=lambda id_=k_cb: st.session_state.update({k_cb_sel: id_})
                )
    c += 1

# st.write([i for i, k in keys_cb.items() if st.session_state.get(k)])
df_use_series = df_series.loc[[i for i, k in keys_cb.items() if st.session_state.get(k)]]

display_df(
    df_use_series,
    "df_use_series"
)

display_df(
    df_playoffs[df_playoffs["seriescode"].isin(df_use_series["seriescode"])],
    "XXX"
)

df_game_scoring = []
with st.spinner(text="Loading game data", show_time=True):
    for i, row in df_playoffs[df_playoffs["seriescode"].isin(df_use_series["seriescode"])].iterrows():
        g_id = row["gameid"]
        seriescode = row["seriescode"]
        my_away_name = row["awayteam"]
        my_home_name = row["hometeam"]
        my_away_score = row["aawayscore"]
        my_home_score = row["ahomescore"]
        my_result = row["otroundnum"]
        my_result = "REG" if my_result == 0 else f"OT{my_result}"
        results = fetch_game_landing(g_id)
        # st.write("results")
        # st.write(results)
        e_score = extract_scoring(results)
        if not pd.isna(e_score.loc[0, "gameid"]):
            df_game_scoring.append(e_score)
        # if results:
            
        #     away = results.get("awayTeam", {})
        #     home = results.get("homeTeam", {})
        #     away_name = away.get("abbrev", "")
        #     home_name = home.get("abbrev", "")
        #     away_score = int(away.get("score", "0"))
        #     home_score = int(home.get("score", "0"))
        #     game_result = results.get("periodDescriptor", {}).get("periodType", "REG")
    
df_game_scoring = pd.concat(df_game_scoring, ignore_index=True) if df_game_scoring else pd.DataFrame(
    columns=["seriescode", "seriesid", "round", "lowseed", "highseed", "gamenum"] + team_cols_b
)

# for each game extract goals and assists
df_player_scoring = extract_player_scoring(df_game_scoring)

df_by_team = df_player_scoring.groupby(
    ["team", "conf", "div"]
    ).agg({
        "player": "count",
        "g": "sum",
        "a": "sum",
        "pts": "sum",
        "gp": "max",
        "ppg": "mean"
    }).rename(columns={
        "player": "count"
    }).reset_index().sort_values(
        ["pts", "ppg"],
        ascending=False
    )
    
df_scoring_summaries = scoring_summaries(df_playoffs, df_game_scoring)

df_ss_gb = df_scoring_summaries.groupby([
    "awayteam", "hometeam"
]).agg({col: "sum" for col in int_record_cols}).reset_index(
    names=["awayteam", "hometeam"]
)
df_ss_away = df_ss_gb.groupby("awayteam").agg({col: "sum" for col in int_record_cols}).reset_index(names="team")
df_ss_home = df_ss_gb.groupby("hometeam").agg({col: "sum" for col in int_record_cols}).reset_index(names="team")
df_ss = df_ss_home.merge(df_ss_away, "inner", "team", suffixes=["_h", "_a"])
for col in int_record_cols:
    t_col = col.removesuffix("_a").removesuffix("_h")
    a_col = f"{t_col}_a"
    h_col = f"{t_col}_h"
    if t_col not in df_ss.columns:
        df_ss[t_col] = 0
    if a_col not in df_ss.columns:
        df_ss[a_col] = 0
    if h_col not in df_ss.columns:
        df_ss[h_col] = 0
    # for c in ["h", "a"]:
    df_ss[t_col] += df_ss[f"{col}_{col[-1]}"]
    if "_a_" in col:
        df_ss[a_col] += df_ss[col]
    if "_h_" in col:
        df_ss[h_col] += df_ss[col]
        
        
# # CREATE HEAD-TO-HEAD CHARTS FOR EACH COLUMN OF DF_SS COMPARING ROW 1 VS ROW 2
# # PSEUDOCODE
# df_ss.index = df.columns[0]  # make column 0 'team' the index
# fig = px.comparison(df_ss, cols, index=df_ss.index)
# st.plotly_chart(fig)

# choose columns to compare
compare_cols = [
    c for c in df_ss.columns
    if c not in ["team", "conf", "div"]
    and pd.api.types.is_numeric_dtype(df_ss[c])
]

# convert from wide -> long format
df_compare = df_ss.melt(
    id_vars="team",
    value_vars=compare_cols,
    var_name="stat",
    value_name="value"
)

fig = px.bar(
    df_compare,
    x="value",
    y="stat",
    color="team",
    barmode="group",
    text_auto=True,
    title=f"{df_ss.iloc[0]['team']} vs {df_ss.iloc[1]['team']}"
)

fig.update_layout(
    xaxis_title="Statistic",
    yaxis_title="Value",
    legend_title="Team",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

fig = go.Figure()

for _, row in df_ss.iterrows():

    fig.add_trace(go.Scatterpolar(
        r=[row[c] for c in compare_cols],
        theta=compare_cols,
        fill='toself',
        name=row["team"]
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

cols = st.columns(4)

for i, stat in enumerate(compare_cols):

    with cols[i % 4]:

        fig = px.bar(
            df_ss,
            x="team",
            y=stat,
            color="team",
            title=stat.upper()
        )

        st.plotly_chart(fig, use_container_width=True)
        
        
team_col = "team"
title = "Head to Head"
stat_cols = [
    c for c in df_ss.columns
    if c != team_col and pd.api.types.is_numeric_dtype(df_ss[c])
]

team_1 = df_ss.iloc[0][team_col]
team_2 = df_ss.iloc[1][team_col]

rows = []

for stat in stat_cols:
    v1 = float(df_ss.iloc[0][stat] or 0)
    v2 = float(df_ss.iloc[1][stat] or 0)
    total = v1 + v2

    if total == 0:
        p1 = 0
        p2 = 0
    else:
        p1 = (v1 / total) * 100
        p2 = (v2 / total) * 100

    rows.append({
        "stat": stat.upper(),
        team_1: v1,
        team_2: v2,
        f"{team_1}_pct": p1,
        f"{team_2}_pct": p2,
        f"{team_1}_label": f"{v1:g} ({p1:.1f}%)",
        f"{team_2}_label": f"{v2:g} ({p2:.1f}%)",
    })

df_plot = pd.DataFrame(rows)

fig = go.Figure()

fig.add_trace(go.Bar(
    y=df_plot["stat"],
    x=df_plot[f"{team_1}_pct"],
    name=team_1,
    orientation="h",
    text=df_plot[f"{team_1}_label"],
    textposition="inside",
    hovertemplate=(
        f"<b>{team_1}</b><br>"
        "Stat: %{y}<br>"
        "Share: %{x:.1f}%<br>"
        "Value: %{customdata:g}"
        "<extra></extra>"
    ),
    customdata=df_plot[team_1],
))

fig.add_trace(go.Bar(
    y=df_plot["stat"],
    x=df_plot[f"{team_2}_pct"],
    name=team_2,
    orientation="h",
    text=df_plot[f"{team_2}_label"],
    textposition="inside",
    hovertemplate=(
        f"<b>{team_2}</b><br>"
        "Stat: %{y}<br>"
        "Share: %{x:.1f}%<br>"
        "Value: %{customdata:g}"
        "<extra></extra>"
    ),
    customdata=df_plot[team_2],
))

fig.update_layout(
    title=title,
    barmode="stack",
    xaxis=dict(
        title="Share of Total",
        range=[0, 100],
        ticksuffix="%",
    ),
    yaxis=dict(
        title="",
        autorange="reversed",
    ),
    legend_title="Team",
    height=max(400, 45 * len(stat_cols)),
    margin=dict(l=120, r=40, t=80, b=60),
)
st.plotly_chart(fig, True)


@st.cache_data(show_spinner=False)
def load_logo_image(team_abbr: str):
    url = fetch_team_logo(team_abbr)

    if not url:
        return None

    response = requests.get(url)

    if response.status_code != 200:
        return None

    return Image.open(BytesIO(response.content))


# def make_h2h_stat_graphic(
#     df_ss: pd.DataFrame,
#     stat_cols: list[str],
#     stat_labels: dict[str, str] | None = None,
#     team_col: str = "team",
#     title: str = "Head to Head Comparison",
#     left_color: str = "#003087",
#     right_color: str = "#A6192E",
#     height_per_stat: int = 82,
# ):
#     if len(df_ss) != 2:
#         raise ValueError("df_ss must contain exactly 2 rows.")

#     stat_labels = stat_labels or {}

#     left_team = str(df_ss.iloc[0][team_col])
#     right_team = str(df_ss.iloc[1][team_col])

#     n = len(stat_cols)
#     height = max(500, 120 + (height_per_stat * n))

#     fig = go.Figure()

#     # Coordinate system:
#     # x = 0 to 1
#     # y = 0 to n
#     for i, stat in enumerate(stat_cols):
#         y = n - i

#         label = stat_labels.get(stat, stat.upper())

#         left_val = float(df_ss.iloc[0][stat] or 0)
#         right_val = float(df_ss.iloc[1][stat] or 0)
#         total = left_val + right_val

#         if total == 0:
#             left_pct = 0.5
#             right_pct = 0.5
#         else:
#             left_pct = left_val / total
#             right_pct = right_val / total

#         # Half-bar scaling:
#         # left bar grows from center leftward
#         # right bar grows from center rightward
#         center_x = 0.5
#         left_start = center_x - (left_pct * 0.46)
#         left_end = center_x - 0.012

#         right_start = center_x + 0.012
#         right_end = center_x + (right_pct * 0.46)

#         bar_y = y - 0.43
#         bar_height = 0.075

#         # Left bar
#         fig.add_shape(
#             type="rect",
#             x0=left_start,
#             x1=left_end,
#             y0=bar_y,
#             y1=bar_y + bar_height,
#             fillcolor=left_color,
#             line=dict(width=0),
#         )

#         # Right bar
#         fig.add_shape(
#             type="rect",
#             x0=right_start,
#             x1=right_end,
#             y0=bar_y,
#             y1=bar_y + bar_height,
#             fillcolor=right_color,
#             line=dict(width=0),
#         )

#         # Optional angled center tips
#         fig.add_shape(
#             type="path",
#             path=(
#                 f"M {left_end} {bar_y} "
#                 f"L {center_x - 0.004} {bar_y} "
#                 f"L {left_end + 0.012} {bar_y + bar_height} "
#                 f"L {left_end} {bar_y + bar_height} Z"
#             ),
#             fillcolor=left_color,
#             line=dict(width=0),
#         )

#         fig.add_shape(
#             type="path",
#             path=(
#                 f"M {right_start} {bar_y} "
#                 f"L {center_x + 0.004} {bar_y} "
#                 f"L {right_start - 0.012} {bar_y + bar_height} "
#                 f"L {right_start} {bar_y + bar_height} Z"
#             ),
#             fillcolor=right_color,
#             line=dict(width=0),
#         )

#         left_pct_label = f"{left_pct * 100:.1f}%"
#         right_pct_label = f"{right_pct * 100:.1f}%"

#         # Left value
#         fig.add_annotation(
#             x=0.045,
#             y=y - 0.06,
#             text=f"<b>{left_val:g}</b>",
#             showarrow=False,
#             xanchor="left",
#             font=dict(size=25, color="black"),
#         )

#         # Right value
#         fig.add_annotation(
#             x=0.955,
#             y=y - 0.06,
#             text=f"<b>{right_val:g}</b>",
#             showarrow=False,
#             xanchor="right",
#             font=dict(size=25, color="black"),
#         )

#         # Center category label
#         fig.add_annotation(
#             x=0.5,
#             y=y - 0.1,
#             text=label,
#             showarrow=False,
#             xanchor="center",
#             font=dict(size=15, color="#444"),
#         )

#         # Percent labels below bars
#         fig.add_annotation(
#             x=0.045,
#             y=y - 0.62,
#             text=f"<b>{left_pct_label}</b>",
#             showarrow=False,
#             xanchor="left",
#             font=dict(size=14, color=left_color),
#         )

#         fig.add_annotation(
#             x=0.955,
#             y=y - 0.62,
#             text=f"<b>{right_pct_label}</b>",
#             showarrow=False,
#             xanchor="right",
#             font=dict(size=14, color=right_color),
#         )

#     # Title
#     fig.add_annotation(
#         x=0.5,
#         y=n + 0.55,
#         text=f"<b>{title}</b>",
#         showarrow=False,
#         xanchor="center",
#         font=dict(size=30, color="black"),
#     )

#     # Team labels / legend
#     # left_logo = load_logo_image(left_team)
#     img_p = [1.0, 2.5]
#     # img_p = [0.1, 0.5]
#     left_logo = fetch_team_logo_png_image(left_team, dark=True)
#     right_logo = fetch_team_logo_png_image(right_team, dark=True)
#     if left_logo is not None:
#         fig.add_layout_image(
#             dict(
#                 source=left_logo,
#                 xref="x",
#                 yref="y",
#                 x=0.08,
#                 y=n + 0.38,
#                 # sizex=0.09,
#                 # sizey=0.5,
#                 sizex=img_p[0],
#                 sizey=img_p[1],
#                 xanchor="center",
#                 yanchor="middle",
#                 layer="above",
#             )
#         )
#     fig.add_annotation(
#         x=0.08,
#         y=n + 0.25,
#         text=f"<b>{left_team}</b>",
#         showarrow=False,
#         xanchor="left",
#         font=dict(size=15, color=left_color),
#     )

#     if right_logo is not None:
#         fig.add_layout_image(
#             dict(
#                 source=right_logo,
#                 xref="x",
#                 yref="y",
#                 x=0.95,
#                 y=n + 0.38,
#                 # sizex=0.09,
#                 # sizey=0.5,
#                 sizex=img_p[0],
#                 sizey=img_p[1],
#                 xanchor="center",
#                 yanchor="middle",
#                 layer="above",
#             )
#         )
#     fig.add_annotation(
#         x=0.92,
#         y=n + 0.25,
#         text=f"<b>{right_team}</b>",
#         showarrow=False,
#         xanchor="right",
#         font=dict(size=15, color=right_color),
#     )

#     fig.update_layout(
#         height=height,
#         width=None,
#         paper_bgcolor="white",
#         plot_bgcolor="white",
#         margin=dict(l=20, r=20, t=40, b=20),
#         xaxis=dict(
#             range=[0, 1],
#             visible=False,
#             fixedrange=True,
#         ),
#         yaxis=dict(
#             range=[0.2, n + 0.85],
#             visible=False,
#             fixedrange=True,
#         ),
#     )

#     return fig


def make_h2h_stat_graphic(
    df_ss: pd.DataFrame,
    stat_cols: list[str],
    stat_labels: dict[str, str] | None = None,
    team_col: str = "team",
    title: str = "Head to Head Comparison",
    left_color: str = "#003087",
    right_color: str = "#A6192E",
    bg_color: str = "#F7F8FA",
    card_color: str = "white",
    height_per_stat: int = 92,
    bar_height: float = 0.102,
    logo_size_x: float = 0.64,
    logo_size_y: float = 1.42,
):
    if len(df_ss) != 2:
        raise ValueError("df_ss must contain exactly 2 rows.")

    stat_labels = stat_labels or {}

    left_team = str(df_ss.iloc[0][team_col])
    right_team = str(df_ss.iloc[1][team_col])

    n = len(stat_cols)
    height = max(620, 170 + (height_per_stat * n))

    fig = go.Figure()

    center_x = 0.5
    gap = 0.012
    max_half_width = 0.455

    # Background card
    fig.add_shape(
        type="rect",
        x0=0.015,
        x1=0.985,
        y0=0.05,
        y1=n + 1.28,
        fillcolor=card_color,
        line=dict(color="rgba(0,0,0,0.08)", width=1),
        layer="below",
    )

    for i, stat in enumerate(stat_cols):
        y = n - i
        label = stat_labels.get(stat, stat.upper())

        left_val = float(df_ss.iloc[0][stat] or 0)
        right_val = float(df_ss.iloc[1][stat] or 0)
        total = left_val + right_val

        if total == 0:
            left_pct = 0.5
            right_pct = 0.5
        else:
            left_pct = left_val / total
            right_pct = right_val / total

        left_bar_x0 = center_x - (left_pct * max_half_width)
        left_bar_x1 = center_x - gap

        right_bar_x0 = center_x + gap
        right_bar_x1 = center_x + (right_pct * max_half_width)

        bar_y0 = y - 0.48
        bar_y1 = bar_y0 + bar_height

        # faint full guide bars
        fig.add_shape(
            type="rect",
            x0=center_x - max_half_width,
            x1=center_x - gap,
            y0=bar_y0,
            y1=bar_y1,
            fillcolor="rgba(0,48,135,0.12)",
            line=dict(width=0),
            layer="below",
        )

        fig.add_shape(
            type="rect",
            x0=center_x + gap,
            x1=center_x + max_half_width,
            y0=bar_y0,
            y1=bar_y1,
            fillcolor="rgba(166,25,46,0.12)",
            line=dict(width=0),
            layer="below",
        )

        # actual left bar
        fig.add_shape(
            type="rect",
            x0=left_bar_x0,
            x1=left_bar_x1,
            y0=bar_y0,
            y1=bar_y1,
            fillcolor=left_color,
            line=dict(width=0),
        )

        # actual right bar
        fig.add_shape(
            type="rect",
            x0=right_bar_x0,
            x1=right_bar_x1,
            y0=bar_y0,
            y1=bar_y1,
            fillcolor=right_color,
            line=dict(width=0),
        )

        # # angled center points
        # fig.add_shape(
        #     type="path",
        #     path=(
        #         f"M {left_bar_x1} {bar_y0} "
        #         f"L {center_x - 0.002} {bar_y0} "
        #         f"L {left_bar_x1 - 0.010} {bar_y1} "
        #         f"L {left_bar_x1} {bar_y1} Z"
        #     ),
        #     fillcolor=left_color,
        #     line=dict(width=0),
        # )
        #
        # fig.add_shape(
        #     type="path",
        #     path=(
        #         f"M {right_bar_x0} {bar_y0} "
        #         f"L {center_x + 0.002} {bar_y0} "
        #         f"L {right_bar_x0 + 0.010} {bar_y1} "
        #         f"L {right_bar_x0} {bar_y1} Z"
        #     ),
        #     fillcolor=right_color,
        #     line=dict(width=0),
        # )
        
        # angled center points
        fig.add_shape(
            type="path",
            path=(
                f"M {left_bar_x1} {bar_y0} "
                f"L {center_x} {bar_y0} "
                f"L {left_bar_x1} {bar_y1} "
                f"L {left_bar_x1} {bar_y1} Z"
            ),
            fillcolor=left_color,
            line=dict(width=0),
        )
        
        fig.add_shape(
            type="path",
            path=(
                f"M {right_bar_x0} {bar_y0} "
                f"L {center_x} {bar_y0} "
                f"L {right_bar_x0} {bar_y1} "
                f"L {right_bar_x0} {bar_y1} Z"
            ),
            fillcolor=right_color,
            line=dict(width=0),
        )

        # left raw value
        fig.add_annotation(
            x=0.055,
            y=y - 0.12,
            text=f"<b>{left_val:g}</b>",
            showarrow=False,
            xanchor="left",
            font=dict(size=28, color="#111"),
        )

        # right raw value
        fig.add_annotation(
            x=0.945,
            y=y - 0.12,
            text=f"<b>{right_val:g}</b>",
            showarrow=False,
            xanchor="right",
            font=dict(size=28, color="#111"),
        )

        # centered stat label
        fig.add_annotation(
            x=center_x,
            y=y - 0.17,
            text=f"<b>{label}</b>",
            showarrow=False,
            xanchor="center",
            font=dict(size=15, color="#444"),
        )

        # percent labels
        fig.add_annotation(
            x=0.055,
            y=y - 0.68,
            text=f"<b>{left_pct * 100:.1f}%</b>",
            showarrow=False,
            xanchor="left",
            font=dict(size=14, color=left_color),
        )

        fig.add_annotation(
            x=0.945,
            y=y - 0.68,
            text=f"<b>{right_pct * 100:.1f}%</b>",
            showarrow=False,
            xanchor="right",
            font=dict(size=14, color=right_color),
        )

    # title
    fig.add_annotation(
        x=0.5,
        y=n + 1.02,
        text=f"<b>{title}</b>",
        showarrow=False,
        xanchor="center",
        font=dict(size=30, color="#111"),
    )

    # logos
    left_logo = fetch_team_logo_png_image(left_team, dark=True)
    right_logo = fetch_team_logo_png_image(right_team, dark=True)

    if left_logo is not None:
        fig.add_layout_image(
            dict(
                source=left_logo,
                xref="x",
                yref="y",
                x=0.07,
                y=n + 0.84,
                sizex=logo_size_x,
                sizey=logo_size_y,
                xanchor="center",
                yanchor="middle",
                layer="above",
            )
        )

    if right_logo is not None:
        fig.add_layout_image(
            dict(
                source=right_logo,
                xref="x",
                yref="y",
                x=0.93,
                y=n + 0.84,
                sizex=logo_size_x,
                sizey=logo_size_y,
                xanchor="center",
                yanchor="middle",
                layer="above",
            )
        )

    # team labels under logos
    fig.add_annotation(
        x=0.145,
        y=n + 0.74,
        text=f"<b>{left_team}</b>",
        showarrow=False,
        xanchor="left",
        font=dict(size=17, color=left_color),
    )

    fig.add_annotation(
        x=0.855,
        y=n + 0.74,
        text=f"<b>{right_team}</b>",
        showarrow=False,
        xanchor="right",
        font=dict(size=17, color=right_color),
    )

    fig.update_layout(
        height=height,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        margin=dict(l=16, r=16, t=20, b=20),
        xaxis=dict(
            range=[0, 1],
            visible=False,
            fixedrange=True,
        ),
        yaxis=dict(
            range=[0, n + 1.35],
            visible=False,
            fixedrange=True,
        ),
    )

    return fig


stat_cols = [
    "w", "l", "gf", "ga",
    "w_h", "l_h", "gf_h", "ga_h",
    "w_a", "l_a", "gf_a", "ga_a",
]

stat_labels = {
    "w": "Wins",
    "l": "Losses",
    "gf": "Goals For",
    "ga": "Goals Against",
    "w_h": "Wins at Home",
    "l_h": "Losses at Home",
    "gf_h": "Goals For at Home",
    "ga_h": "Goals Against at Home",
    "w_a": "Wins Away",
    "l_a": "Losses Away",
    "gf_a": "Goals For Away",
    "ga_a": "Goals Against Away",
}

if len(df_ss) == 2:
    fig = make_h2h_stat_graphic(
        df_ss=df_ss,
        stat_cols=stat_cols,
        stat_labels=stat_labels,
        title="Head to Head Comparison",
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select exactly 2 teams for the head-to-head chart.")


#######################################################################################################################
#######################################################################################################################
    
df_playoffs_ = df_playoffs.copy()
df_game_scoring_ = df_game_scoring.copy()
df_by_team_ = df_by_team.copy()
df_player_scoring_ = df_player_scoring.copy()
df_scoring_summaries_ = df_scoring_summaries.copy()

for col in team_cols_a:
    df_playoffs_[col] = df_playoffs_[col].apply(fetch_team_logo)
for col in team_cols_b:
    df_game_scoring_[col] = df_game_scoring_[col].apply(lambda t: fetch_team_logo(t))
for col in ["awayteam", "hometeam", "winner"] + team_cols_b:
    df_scoring_summaries_[col] = df_scoring_summaries_[col].apply(lambda t: fetch_team_logo(t))
df_by_team_["team"] = df_by_team_["team"].apply(lambda t: fetch_team_logo(t))
df_player_scoring_["team"] = df_player_scoring_["team"].apply(lambda t: fetch_team_logo(t))

#######################################################################################################################
#######################################################################################################################

display_df(
    df_playoffs_.rename(columns=col_translation),
    "Scores",
    column_config={
        col_translation[col]: st.column_config.ImageColumn(col_translation[col], width=80)
        for col in team_cols_a
    },
    row_height=40
)
display_df(
    df_game_scoring_,
    "Scoring",
    column_config={
        col: st.column_config.ImageColumn(col, width=80)
        for col in team_cols_b
    },
    row_height=40
)
    
with st.container(horizontal=True):
    display_df(
        df_player_scoring_,
        "Scoring",
        column_config={
            "team": st.column_config.ImageColumn("team", width=80)
        },
        row_height=40
    )
    display_df(
        df_by_team_,
        "Scoring by Team",
        column_config={
            "team": st.column_config.ImageColumn("team", width=80)
        },
        row_height=40
    )
    display_df(
        df_scoring_summaries_,
        "df_scoring_summaries",
        column_config={
            col: st.column_config.ImageColumn(col, width=80)
            for col in ["awayteam", "hometeam", "winner"] + team_cols_b
        },
        row_height=40
    )

with st.container(horizontal=True):
    display_df(
        df_ss_gb,
        "df_ss_gb"
    )
    display_df(
        df_ss_away,
        "df_ss_away"
    )
    display_df(
        df_ss_home,
        "df_ss_home"
    )

display_df(
    df_ss,
    "df_ss"
)
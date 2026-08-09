import datetime

import streamlit as st
import pandas as pd
from typing import Optional, Literal, Any, Iterable

from streamlit_utility import display_df, local_image_thumbnail_data_url
from datetime_utility import is_date


# ─────────────────────────────────────────────────────────
# NHL TEAM METADATA
# ─────────────────────────────────────────────────────────
TEAM_META = {
    "ANA": {"name": "Anaheim Ducks",       "conf": "Western", "div": "Pacific",    "id": 24, "active": True},
    # "ARI": {"name": "Utah Hockey Club",     "conf": "Western", "div": "Central",    "id": 53, "active": False},
    "UTA": {"name": "Utah Mammoth",         "conf": "Western", "div": "Central",    "id": 59, "active": True},
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


PWHL_META = [
    {"name": "Ottawa Charge", "acronym": "OTT", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\ottawa_charge.png",},
    {"name": "Montreal Victoire", "acronym": "MTL", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\montreal_victoire.png",},
    {"name": "Toronto Sceptres", "acronym": "TOR", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\toronto_sceptres.png",},
    {"name": "Vancouver Goldeneyes", "acronym": "VAN", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\vancouver_goldeneyes.png",},
    {"name": "New York Sirens", "acronym": "NY", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\new_york_sirens.png",},
    {"name": "Seattle Torrent", "acronym": "SEA", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\seattle_torrent.png",},
    {"name": "Boston Fleet", "acronym": "BOS", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\boston_fleet.png",},
    {"name": "Minnesota Frost", "acronym": "MIN", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\minnesota_frost.png",},
]

QMJHL_META = [
    {"name": "Baie-Comeau Drakkar", "acronym": "BAC", "logo": r"D:\3D Prints\QMJHL Logos\Baie-Comeau Drakkar\Baie-Comeau_Drakkar.png",},
    {"name": "Blainville-Broisbriand Armada", "acronym": "BLB", "logo": r"D:\3D Prints\QMJHL Logos\Blainville-Broisbriand Armada\ARMADAlogos-04.jpg",},
    {"name": "Cape Breton Screaming Eagles", "acronym": "CAP", "logo": r"D:\3D Prints\QMJHL Logos\Cape Breton Screaming Eagles\Cape-Breton-Eagles-Logo-Main-01-1.png",},
    {"name": "Charlottetown Islanders", "acronym": "CHA", "logo": r"D:\3D Prints\QMJHL Logos\Charlottetown Islanders\Charlottetown_Islanders.png",},
    {"name": "Chicoutimi Sagueneens", "acronym": "CHI", "logo": r"D:\3D Prints\QMJHL Logos\Chicoutimi Sagueneens\Chicoutimi_Saguenéens.svg.png",},
    {"name": "Drummondville Voltigeurs", "acronym": "DRU", "logo": r"D:\3D Prints\QMJHL Logos\Drummondville Voltigeurs\Drummondville_Voltigeurs.svg.png",},
    {"name": "Gatineau Olympiques", "acronym": "GAT", "logo": r"D:\3D Prints\QMJHL Logos\Gatineau Olympiques\Logo_PNG.png",},
    {"name": "Halifax Mooseheads", "acronym": "HAL", "logo": r"D:\3D Prints\QMJHL Logos\Halifax Mooseheads\Halifax_Mooseheads_logo_September_2022.png",},
    {"name": "Moncton Wildcats", "acronym": "MON", "logo": r"D:\3D Prints\QMJHL Logos\Moncton Wildcats\Moncton-wildcats-logo-2021.jpg",},
    {"name": "Newfoundland Regiment", "acronym": "NFL", "logo": r"D:\3D Prints\QMJHL Logos\Newfoundland Regiment\nfl_regiment.png",},
    {"name": "Quebec Remparts", "acronym": "QUE", "logo": r"D:\3D Prints\QMJHL Logos\Quebec Remparts\Quebec_Remparts.png",},
    {"name": "Rimouski Oceanic", "acronym": "RIM", "logo": r"D:\3D Prints\QMJHL Logos\Rimouski Oceanic\rimouski.jpg",},
    {"name": "Rouyn-Noranda Huskies", "acronym": "ROU", "logo": r"D:\3D Prints\QMJHL Logos\Rouyn-Noranda Huskies\LOGO_2019.png",},
    {"name": "Saint John Seadogs", "acronym": "SNB", "logo": r"D:\3D Prints\QMJHL Logos\Saint John SeaDogs\logo.jpg",},
    {"name": "Shawinigan Cataractes", "acronym": "SHA", "logo": r"D:\3D Prints\QMJHL Logos\Shawinigan Cataractes\Shawinigan_Cataractes.png",},
    {"name": "Sherbrooke Phoenix", "acronym": "SHE", "logo": r"D:\3D Prints\QMJHL Logos\Sherbrooke Phoenix\MBC-Logo-PhoenixSherbrooke.png",},
    {"name": "Val Dor Foreurs", "acronym": "VDO", "logo": r"D:\3D Prints\QMJHL Logos\Val Dor Foreurs\Logo-des-Foreurs.png",},
    {"name": "Victoriaville Tigres", "acronym": "VIC", "logo": r"D:\3D Prints\QMJHL Logos\Victoriaville Tigres\logo.png",},
]


@st.cache_data
def load_df_teams():
    df_pwhl = pd.DataFrame(PWHL_META)
    df_qmjhl = pd.DataFrame(QMJHL_META)
    df_pwhl[["league", "active"]] = ["PWHL", True]
    df_qmjhl[["league", "active"]] = ["QMJHL", True]
    df_pwhl = df_pwhl.rename(columns={"acronym": "team"})
    df_qmjhl = df_qmjhl.rename(columns={"acronym": "team"})
    # df_pwhl["logo"] = df_pwhl["logo"].apply(lambda l: local_image_to_data_url(l))
    df_pwhl["logo"] = df_pwhl["logo"].apply(lambda p: local_image_thumbnail_data_url(p, max_size=200, quality=100))
    df_qmjhl["logo"] = df_qmjhl["logo"].apply(lambda p: local_image_thumbnail_data_url(p, max_size=200, quality=100))

    df_teams = pd.DataFrame(TEAM_META).T.reset_index(names="team")
    df_teams["league"] = "NHL"
    for team, name, league in [
        ("ARI", "Arizona Coyotes", "NHL"),
        
        ("CAN", "Team Canada", "IIHF"),
        ("USA", "Team United States", "IIHF"),
        ("SWE", "Team Sweden", "IIHF"),
        ("FIN", "Team Finland", "IIHF"),
        ("SVK", "Team Slovakia", "IIHF"),
    ]:
        df_teams.loc[len(df_teams), df_teams.columns] = [team, name, None, None, None, True, league]
        
    df_teams.loc[df_teams["team"] == "ARI", ["active", "conf", "div"]] = [False, "Western", "Central"]

    df_teams["alt"] = None
    for t, a in [
        ("LAK", "LA"),
        ("TBL", "TB"),
        ("NJD", "NJ"),
        ("SJS", "SJ"),
        ("WSH", "WAS"),
    ]:
        df_teams.loc[df_teams["team"] == t, "alt"] = a

    return pd.concat([df_teams, df_pwhl, df_qmjhl], ignore_index=True)


def team_fmt(s):
    return str(s).replace(" ", "").upper().replace("É", "E").replace("UNITEDSTATES", "USA").strip()


def player_headshot_url(
    player: str | None,
    team_abbrev: str,
    season_id: str | int | None,
    debug: bool = False,
) -> str:
    if not player:
        return ""

    # direct_url = first_present(
    #     player,
    #     "headshot",
    #     "headshotUrl",
    #     "mugshot",
    #     "image",
    # )
    #
    # if direct_url:
    #     return str(direct_url)
    #
    # player_id = first_present(
    #     player,
    #     "playerId",
    #     "id",
    # )
    #
    # if not player_id or not season_id:
    #     return ""
    
    if not season_id:
        t = datetime.datetime.now()
        y, m, d = t.year, t.month, t.day
        if m < 7:
            y -= 1
        season_id = f"{y}"

    default = "https://assets.nhle.com/mugs/nhl/default-skater.png"
    url = (
        "https://assets.nhle.com/mugs/nhl/"
        f"{season_id}/{team_abbrev}/{player}.png"
    )
    if debug:
        st.write(f"{url=}")
    return url

 
def find_team(team, league: str | None = "NHL", debug: bool = False):
    df_teams = load_df_teams()
    tf = team_fmt(team)
    unk_l = league is None
    sl = str(league).replace("None", "NHL").upper()
    if debug:
        st.write(f"find_team {team=}, {tf=}, {sl=}")
    for i, row in df_teams.sort_values("name").iterrows():
        rl = str(row["league"]).upper()
        rt = row["team"]
        c = st.container(border=True, horizontal=True, width=500) if debug else st
        cont = (sl != rl) and (not unk_l) and (not tf.startswith("TEAM"))
        # cont = (not unk_l) and (not tf.startswith("TEAM"))
        # with st.container(border=debug):
        if debug:
            c.write(f"{i=}, {rl=}, {sl=}, {rt=}, rn={row['name']}, cont={cont}")
        # if cont:
        #     continue
        if debug:
            c.write(f"{team_fmt(row['team'])=}, {team_fmt(row['name'])=}, {team_fmt(row['alt'])=}")
        if (tf == team_fmt(row["team"])):
            if debug:
                c.write(f"A {i=}, {rt=}")
            return rt
        elif tf == team_fmt(row["name"]):
            if debug:
                c.write(f"B {i=}, {rt=}")
            return rt
        elif not pd.isna(row["alt"]):
            if tf == team_fmt(row["alt"]):
                if debug:
                    c.write(f"C {i=}, {rt=}, {row['alt']}")
                return rt
        # elif any([team_fmt(row["name"]) == team_fmt("Montréal Canadiens"), team_fmt(row["team"]) == team_fmt("Montréal Canadiens"), team_fmt(row["alt"]) == team_fmt("Montréal Canadiens")]):
        elif any([team_fmt(row["name"]) == tf, team_fmt(row["team"]) == tf, team_fmt(row["alt"]) == tf]):
            if debug:
                c.write(f"D {i=}, {rt=}, Montréal Canadiens")
            return rt
        elif (sl == "IIHF") and (tf.removeprefix("TEAM") in [team_fmt(row["name"]), team_fmt(row["team"]), team_fmt(row["alt"])]):
            if debug:
                c.write(f"E {i=}, {rt=}, {row['alt']}")
            return rt
        else:
            if debug:
                c.write(f"F SKIP {i=}, {team=}, {league=}, {tf=}, {sl=}")


def ddn(
    df: pd.DataFrame | pd.Series,
    title: Optional[str] = None,
    hide_index: str | bool = "if_int",
    show_shape: Literal[True, False, "separate", "below"] = True,
    fail_safe: Optional[Any] = True,
    border: bool = False,

    # params for st.dataframe 20250325
    width: int | None = "stretch",
    height: int | None = "auto",
    use_container_width: bool = False,
    column_order: Iterable[str] | None = None,
    column_config: Any | None = None,
    key: Any | None = None,
    on_select: Literal["ignore", "rerun"] | Any = "ignore",
    selection_mode: Any = "multi-row",
 
     # params for st.dataframe 20260514
    selection_default: dict | None = None,
    row_height: int | None = None,
    placeholder: str | None = None,
    
    image_cols: list | None = None,
    non_image_cols: list | None = None,
    image_col_width: int = 40,
    mode: Literal["team", "player"] = "team",
    
    debug: bool = False
):
    return display_df_nhl(
        df=df,
        title=title,
        hide_index=hide_index,
        show_shape=show_shape,
        fail_safe=fail_safe,
        border=border,

        # params for st.dataframe 20250325
        width=width,
        height=height,
        use_container_width=use_container_width,
        column_order=column_order,
        column_config=column_config,
        key=key,
        on_select=on_select,
        selection_mode=selection_mode,
    
        # params for st.dataframe 20260514
        selection_default=selection_default,
        row_height=row_height,
        placeholder=placeholder,        
        
        image_cols = image_cols,
        non_image_cols = non_image_cols,
        image_col_width = image_col_width,
        mode=mode,
        
        debug = debug
    )


def display_df_nhl(
    df: pd.DataFrame | pd.Series,
    title: Optional[str] = None,
    hide_index: str | bool = "if_int",
    show_shape: Literal[True, False, "separate", "below"] = True,
    fail_safe: Optional[Any] = True,
    border: bool = False,

    # params for st.dataframe 20250325
    width: int | None = "stretch",
    height: int | None = "auto",
    use_container_width: bool = False,
    column_order: Iterable[str] | None = None,
    column_config: Any | None = None,
    key: Any | None = None,
    on_select: Literal["ignore", "rerun"] | Any = "ignore",
    selection_mode: Any = "multi-row",
 
     # params for st.dataframe 20260514
    selection_default: dict | None = None,
    row_height: int | None = None,
    placeholder: str | None = None,
    
    image_cols: list | None = None,
    non_image_cols: list | None = None,
    image_col_width: int = 40,
    mode: Literal["team", "player"] = "team",
    
    debug: bool = False
):
    
    team_cols = ["", "away", "home", "abbr", "abbrev", "name"]
    team_cols += [f"{t}team" for t in team_cols] + [f"team{t}" for t in team_cols] + [f"team_{t}" for t in team_cols] + [f"{t}_team" for t in team_cols]
    team_cols += ["mychoice", "winner", "loser", "lowseed", "topseed", "top", "low", "high", "opponent"]
    
    player_cols = ["", "first", "last", "second", "name", "full", "short",]
    for pc in ["player", "name", "nhlid"]:
        player_cols += [f"{t}{pc}" for t in player_cols] + [f"{pc}{t}" for t in player_cols] + [f"{pc}_{t}" for t in player_cols] + [f"{t}_{pc}" for t in player_cols]
        
    if debug:
        st.write(f"{df.columns.tolist()}")
        # st.write(f"{df['team'].unique().tolist()}")
    # df_cols = {str(c).lower().strip(): c for c in df.columns}
    column_config = column_config if column_config else {}
    
    t_cols = []
    for col in df.columns:
        col_t = str(col).lower().strip()
        if (col not in column_config) and (col_t in team_cols):
            t_cols.append(col)
            
    p_cols = []
    for col in df.columns:
        col_p = str(col).lower().strip()
        if (col not in column_config) and (col_p in player_cols):
            p_cols.append(col)
            
    if mode == "player":
        t_cols = [c for c in t_cols if c not in p_cols]
    else:
        p_cols = [c for c in p_cols if c not in t_cols]
            
    image_cols = image_cols if image_cols else []
    
    for c in image_cols:
        if c not in t_cols:
            t_cols.append(c)
    
    if debug:
        with st.container(horizontal=True):
            st.header("A")
            with st.expander("team_cols"):
                st.write(team_cols)
            # with st.expander("df_cols"):
            #     st.write(df_cols)
            with st.expander("t_cols"):
                st.write(t_cols)
            with st.expander("p_cols"):
                st.write(p_cols)
            with st.expander("column_config"):
                st.write(column_config)
            with st.expander("df.columns"):
                st.write(df.columns.tolist())
            with st.expander("image_cols"):
                st.write(image_cols)
    
    t_cols += [c for c in column_config.keys() if c in team_cols]
    if non_image_cols is not None:
        for c in non_image_cols:
            if c in t_cols:
                t_cols.remove(c)
            elif c.lower() in t_cols:
                t_cols.remove(c.lower())
            elif c.upper() in t_cols:
                t_cols.remove(c.upper())
            elif c.title() in t_cols:
                t_cols.remove(c.title())
                
    df_ = df.copy()
    # with st.container(border=True):
    #     st.subheader("df_")
    #     st.dataframe(df_)
    
    def get_player_like(cols, df_, debug: bool = False):
        if debug:
            with st.container(horizontal=True):
                with st.container():
                    st.write("cols")
                    st.write(cols)
                with st.container():
                    st.write("df_")
                    st.write(df_)
        if not df_.empty:
            dtypes = df_[cols].dtypes
            cols_ = [c for c in cols if df_[c].dtypes in [int, float]]
            if not cols_:
                pass
            else:
                cols = cols_
        
        # val = row[col]
        return cols
        
        
    def get_team_like(row, cols):
        cols_t = set(t_cols).intersection(set(cols))
        if cols_t:
            cols_t = list(cols_t)
            t_col = cols_t[0]
            df_teams = load_df_teams()
            val = str(row[t_col]).lower().strip()
            df_teams = df_teams[
                (df_teams["team"].str.lower().str.lower() == val)
                | (df_teams["name"].str.lower().str.lower() == val)
            ]
            if not df_teams.empty:
                return df_teams.iloc[0]["team"]
            return row[t_col]
        
        
    def get_season_like(row, cols):
        d_cols = ["date", "season"]
        d_cols_ = []
        for c in cols:
            if str(c).lower().strip() in d_cols:
                d_cols_.append(c)
        d_cols = d_cols_
        cols_d = set(d_cols).intersection(set(cols))
        # with st.container(horizontal=True):
        #     with st.container():
        #         st.write(f"cols_d")
        #         st.write(cols_d)
        #     with st.container():
        #         st.write(f"d_cols")
        #         st.write(d_cols)
        #     with st.container():
        #         st.write(f"cols")
        #         st.write(cols)
        if cols_d:
            cols_d = list(cols_d)
            d_col = cols_d[0]
            val = row[d_col]
            if (not pd.isna(val)) and bool(val):
                date = is_date(val)
                st.write(f"{date=}, {val=}")
                if date:
                    val = date.year
                    val = f"{val}{val + 1}"
                else:
                    if isinstance(val, str):
                        val = str(val).replace("-").strip()
                        if len(val) != 8:
                            # 20262027
                            val = val[:8]
                return val
        else:
            return f"{datetime.datetime.now().year - 1}{datetime.datetime.now().year}"
    
    p_cols = get_player_like(p_cols, df_, debug=debug)
    for c in p_cols:
        if c not in df_.columns:
            if debug:
                st.write(f"skip {c}")
            continue
        df_[c] = df_.apply(lambda row: player_headshot_url(row[c], get_team_like(row, df_.columns.tolist()), get_season_like(row, df_.columns.tolist()), debug=debug), axis=1)
        column_config[c] = st.column_config.ImageColumn(c, width=image_col_width * 2)
        
    # https://assets.nhle.com/mugs/nhl/20242025/TOR/8477939.png
    
    for c in t_cols:
        if c not in df_.columns:
            if debug:
                st.write(f"skip {c}")
            continue
        df_[c] = df_.apply(lambda row: fetch_team_logo(row[c], league=row.get("league", row.get("League")), debug=debug), axis=1)
        column_config[c] = st.column_config.ImageColumn(c, width=image_col_width)
    
    if debug:
        with st.container(horizontal=True):
            st.header("B")
            # with st.expander("df_cols"):
            #     st.write(df_cols)
            with st.expander("t_cols"):
                st.write(t_cols)
            with st.expander("p_cols"):
                st.write(p_cols)
            with st.expander("column_config"):
                st.write(column_config)
            with st.expander("df.columns"):
                st.write(df.columns.tolist())
    
        with st.container():
            st.write("df_HERE")
            st.write(df_)
    
    return display_df(
        df=df_,
        title=title,
        hide_index=hide_index,
        show_shape=show_shape,
        fail_safe=fail_safe,
        border=border,

        # params for st.dataframe 20250325
        width=width,
        height=height,
        use_container_width=use_container_width,
        column_order=column_order,
        column_config=column_config,
        key=key,
        on_select=on_select,
        selection_mode=selection_mode,
    
        # params for st.dataframe 20260514
        selection_default=selection_default,
        row_height=row_height,
        placeholder=placeholder
    )
    

@st.cache_data
def fetch_team_logo(team_abbr: str, dark: bool = True, err_on_not_found: bool = False, league: str | None = None, debug: bool = False, season_id: int = None) -> str:
    """Get NHL team logo URL from NHL API."""
    
    df_teams = load_df_teams()
    
    with st.container(border=debug, horizontal=True):
        
        prefix = "https://assets.nhle.com/logos/nhl/svg/" + " ".strip()
        suffix = ".svg"
        d, l = "_dark", "_light"
        team_abbr_s = str(team_abbr).lower().strip().removeprefix(prefix).removesuffix(suffix).removesuffix(d).removesuffix(l)
        
        # debug = debug and (str(datetime.now().second).endswith("1") or str(datetime.now().second).endswith("4") or str(datetime.now().second).endswith("7") or str(datetime.now().second).endswith("0") or str(datetime.now().second).endswith("3"))
        
        if debug:
            st.write(f"team='{team_abbr}', team_s='{team_abbr_s}', {league=}, {dark=} ")
            
        if league is None:
            if str(team_abbr).lower().startswith("team"):
                league = "IIHF"
            # else:
            #     league = "NHL"
        
        s_t = team_fmt(find_team(team_abbr_s, league=league, debug=debug,))
        s_l = team_fmt(str(league))
        if debug:
            st.write(f"ftl: {s_t=}, {s_l=}")
        df_s = df_teams.copy()
        df_s["team_s"] = df_s["team"].apply(team_fmt)
        df_s["league_s"] = df_s["league"].apply(team_fmt)
        # df_s = df_s[(df_s["team_s"] == s_t) & (df_s["league_s"] == s_l)].reset_index()
        df_s = df_s[df_s["team_s"] == s_t]
        if debug:
            display_df(
                df_s,
                f"A df_s {team_abbr=}, {dark=}, err={err_on_not_found}, {league=}",
                hide_index=False,
                show_shape="below"
            )
        if s_l != "NONE":
            df_s_ = df_s[df_s["league_s"] == s_l]
            if not df_s_.empty:
                df_s = df_s_.copy()
        df_s = df_s.reset_index()
        c = len(df_s)
        if debug:
            display_df(
                df_s,
                f"B df_s {team_abbr=}, {dark=}, err={err_on_not_found}, {league=}",
                hide_index=False,
                show_shape="below"
            )
            if df_s.empty:
                st.error(f"No teams found")
        if c > 0:
            url = ""
            s_l = df_s.loc[0, "league"]
            if s_l == team_fmt("NHL"):
                if debug:
                    st.write(f"A {s_l=}")
                if season_id:
                    url = f"{prefix}{df_s.loc[0, 'team'].upper()}_{'dark' if dark else 'light'}{suffix}?season={season_id}"
                else:
                    url = f"{prefix}{df_s.loc[0, 'team'].upper()}_{'dark' if dark else 'light'}{suffix}"
            elif s_l in [team_fmt("PWHL"), team_fmt("QMJHL")]:
                if debug:
                    st.write(f"B {s_l=}")
                url = df_s.iloc[0]["logo"]
            elif (s_l == team_fmt("IIHF")) or ((s_l == team_fmt("NHL") and (s_t.startswith("TEAM")))):
                s_t = s_t.removeprefix("TEAM")
                if debug:
                    st.write(f"C {s_t=}")
                url_tmpl = "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/{CC}.svg"
                if s_t in ["CAN", "CANADA"]:
                    url = url_tmpl.format(CC="ca")
                elif s_t in ["FIN", "FINLAND"]:
                    url = url_tmpl.format(CC="fi")
                elif s_t in ["SWE", "SWEDEN"]:
                    url = url_tmpl.format(CC="se")
                elif s_t in ["SVK", "SLOVAKIA"]:
                    url = url_tmpl.format(CC="sk")
                elif s_t in ["USA", "UNITEDSTATES"]:
                    url = url_tmpl.format(CC="us")
            else:
                st.write(f"-> SKIP {s_t=}, {s_l=}, {team_abbr=}")
            if debug:
                st.write(f"{url=}")
            return url
        else:  #(c == 0) and err_on_not_found:
            if err_on_not_found:
                raise ValueError(f"{team_abbr=} not found in df_teams")
            else:
                return ""
        # elif c > 0:
        #     raise ValueError(f"Multiple teams found matching {team_abbr=} found in df_teams")
        
        return ""
        
            
        # if str(find_team(team_abbr)).upper() not in TEAM_META:
        #     if err_on_not_found:
        #         raise ValueError(f"{team_abbr=} not found in TEAM_META")        
        #     return ""
        # return f"https://assets.nhle.com/logos/nhl/svg/{team_abbr.upper()}_{'dark' if dark else 'light'}.svg"

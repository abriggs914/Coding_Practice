import base64
import datetime
import json
import os.path
from pathlib import Path

from typing import Any, Optional

import pandas as pd
from streamlit_sortables import sort_items
from streamlit_pills import pills
from streamlit_float import *

import streamlit as st

from colour_utility import Colour
from icons_8_refs import image_refs_htmls


import streamlit_nested_layout


st.set_page_config(layout="wide")

# # initialize float feature/capability
# float_init()


def create_html_table(
    df: pd.DataFrame,
    column_config: Optional[dict[str: Any]] = None,
    table_id: Optional[str] = None
) -> str:
    """
    Create a custom HTML table with alternate row backgrounds.

    LAST UPDATED 2024-12-22 15:57

    Args:
        df (pd.DataFrame): The DataFrame to render as an HTML table.

    Returns:
        str: The HTML string representing the table.
    """
    # Initialize the HTML table with styles
    t_id: str = "" if table_id is None else f'id="{table_id}" '
    html = f'<table {t_id}style="border-collapse: collapse; width: 100%;">'

    valid_configs = {
        "image": {
            # "func": lambda img, img_width="100", img_height="100": f'<td style="border: 1px solid #ddd; padding: 8px;"><img src="{img}" alt="{img}" width="{img_width}" height="{img_height}"></td>',
            "func": lambda img, img_width="100",
                           img_height="100": f'<img src="{img}" alt="{img}" width="{img_width}" height="{img_height}">',
            "args": ["img_width", "img_height"]
        }
    }

    columns = df.columns

    if column_config is None:
        column_config = {}
    else:
        to_remove = []
        for col in column_config:
            if col not in columns:
                # to_remove.append(col)
                raise ValueError(f"Unrecognized column '{col}'.")
            else:
                config_type: str = column_config[col].get("config_type")
                if config_type is None:
                    raise ValueError(
                        f"You must specify how to configure column '{col}'. Include 'config_type' as a keyword and set to one of {' '.join(list(valid_configs))}")
                config_args: list[Any] | dict[str: Any] = column_config.get("args", [])
                v_args: list[str] = valid_configs[config_type]["args"]

                if isinstance(config_args, dict):
                    for k, v in config_args.items():
                        if k not in v_args:
                            raise ValueError(
                                f"unrecognized kwarg '{k}' for {config_type=}, expected one of {' '.join(v_args)}")

                # func = valid_configs[config_type]["func"]

                # l_args = len(v_args)
                # for i, kw in enumerate(column_config[col]):
                #     val = column_config[col][kw]
                #     if i > l_args:
                #         raise ValueError(f"Got too many arguments to configure this column type ({})")

        for col in to_remove:
            del column_config[col]

    # print(f"{df=}")

    # Add table headers
    html += '<thead style="background-color: #2f2f2f; font-weight: bold;">'
    html += '<tr>'
    for col in columns:
        html += f'<th style="border: 1px solid #ddd; padding: 8px;">{col}</th>'
    html += '</tr>'
    html += '</thead>'

    # Add table rows with alternate-row styling
    html += '<tbody>'
    for i, row in df.iterrows():
        # Determine row background color
        # print(f"{i=}, {list(row)=}")
        i: int = int(i)
        bg_color = '#4f4f4f' if i % 2 == 0 else '#9f9f9f'
        html += f'<tr style="background-color: {bg_color};">'
        for j, col in enumerate(columns):
            value = row[col]
            if col in column_config:
                config_type: str = column_config[col]["config_type"]
                func = valid_configs[config_type]["func"]
                args = column_config[col].get("args", [])
                if isinstance(args, dict):
                    value = func(value, **args)
                else:
                    value = func(value, *args)
            html += f'<td style="border: 1px solid #ddd; padding: 8px;">{value}</td>'
        html += '</tr>'
    html += '</tbody>'

    # Close the table
    html += '</table>'

    return html


@st.cache_data(show_spinner=True)
def load_data_file():
    with open(r"./wjc_2025.json", "r") as f:
        return json.load(f)


@st.cache_data(show_spinner=True)
def load_flags():
    pictures = os.listdir(root_image_folder)
    flags = {}
    for i, team_data in enumerate(teams):
        team_id: int = team_data.get("id")
        name_long: str = team_data.get("name_long")
        name: str = team_data.get("name")
        n: str = name_long.lower()
        match n:
            case "united states of america": n = "usa"
            case "czechia": n = "czech-republic"
            case _: pass
        j: int = 0
        found: bool = False
        for j, picture in enumerate(pictures):
            p: str = picture.lower().replace("icons8-", "").replace("-flag-96", "").replace("-96.png", ".png").strip()
            print(f"\t{p=}, {n=}")
            if picture.endswith(".png") and (n in p):
                flags[i] = os.path.join(root_image_folder, picture)
                found = True
                break
        if found:
            pictures.pop(j)
        else:
            print(f"No image found for '{n}'")

    flags[None] = os.path.join(root_image_folder, "unknown_flag.png")

    return flags


@st.cache_data(show_spinner=True)
def load_flags_64(flag_paths):
    flags_64 = []
    for image_path in flag_paths.values():
        if image_path is not None:
            with open(image_path, "rb") as img_file:
                flags_64.append(f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}")
    return flags_64


root_image_folder = r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags"
if not os.path.exists(root_image_folder):
    root_image_folder = r"C:\Users\abrig\Documents\Coding_Practice\Resources\Flags"


default_bg_team_col: Colour = Colour("#151530")


initial_data: dict[str: Any] = load_data_file()
teams: list[dict] = initial_data["teams"]
rounds: list[str] = initial_data["rounds"]
# rounds_pills: list[str] = initial_data["rounds"]
rounds_pills: list[str] = rounds[:-2] + ["Medal"]
games: list[dict] = initial_data["schedule"]["games"]
games_per_round: dict[int: int] = {}
list_groups: list[str] = ["A", "B"]
teams_by_group: dict[str: list[int]] = {g: [t for t in teams if t["group"] == g] for g in list_groups}
game_id_to_idx: dict[int: int] = {g["game_id"]: i for i, g in enumerate(games)}
flags = load_flags()
flags_64 = load_flags_64(flags)
flag_w, flag_h = 100, 50

st.write(flags)
st.json(initial_data)

cols_per_row: int = 2

for i, g in enumerate(games):
    rnd: int = g["round"]
    if rnd not in games_per_round:
        games_per_round[rnd] = 0
    games_per_round[rnd] += 1
    games[i].update({
        "date": datetime.datetime.strptime(games[i]["date"], "%Y-%m-%d %H:%M")
    })

n_rows = int(round(len(games) / cols_per_row))
games_chosen: dict[int: dict[int: bool]] = {}
st.session_state.setdefault("team_records", {
    t.get("id"): {
        "times_chosen": 0
    }
    for t in teams
})


def select_team(team_id: int, toggle_key: str, toggle_key_d: str):
    st.session_state.update({
        toggle_key_d: datetime.datetime.now()
    })
    is_sel = st.session_state.get(toggle_key)
    tr = st.session_state.get("team_records", {})
    if team_id not in tr:
        tr.update({team_id: {"times_chosen": int(is_sel)}})
    else:
        chg = 1 if is_sel else -1
        tr[team_id].update({"times_chosen": tr[team_id]["times_chosen"] + chg})
    st.session_state.update({"team_records": tr})


def game_points(game_id: int | list[int], team_id: int, stats: Optional[list[str]] = None) -> dict[str: int]:

    # print(f"GAMEPOINTS -> {game_id=}, {team_id=}")

    if isinstance(game_id, list):
        # return sum([game_points(gid, team_id) for gid in game_id])
        st.write(f"{game_id=}")
        res = {}
        for gid in game_id:
            g_res = game_points(gid, team_id=team_id, stats=stats)
            st.write(f'{g_res=}')
            if not res:
                res.update(g_res)
            else:
                for k in g_res:
                    res.setdefault(k, g_res[k])
                for k in res:
                    res[k] = res[k] + g_res[k]
        st.write(f'{res=}')
        return res

    valid_stats = ["pts", "w", "l", "otl/sol"]
    if stats is None:
        stats = ["pts"]

    idx: int = game_id_to_idx[game_id]
    game_data = games[idx]
    game_away_id: int = game_data.get("away")
    game_home_id: int = game_data.get("home")
    v_teams: list[int] = [game_away_id, game_home_id]

    if team_id not in v_teams:
        raise ValueError(f"{team_id=} not found in available teams for {game_id=}. Got {v_teams}")

    away_group: Optional[str] = None
    home_group: Optional[str] = None
    group: Optional[str] = None
    away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
    home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
    if away_team_data:
        a_data = away_team_data[0]
        away_name = a_data.get("name")
        away_group = a_data.get("group")
        away_flag_id = a_data.get("id")
    if home_team_data:
        h_data = home_team_data[0]
        home_name = h_data.get("name")
        home_group = h_data.get("group")
        home_flag_id = h_data.get("id")
    if away_group or home_group:
        group = "".join(list({away_group, home_group}))

    t_key_ot = f"toggle_{game_id}_{group}_OT"
    t_key_away = f"toggle_{game_id}_{group}_Away"
    t_key_home = f"toggle_{game_id}_{group}_Home"
    t_key_away_d = f"{t_key_away}_d"
    t_key_home_d = f"{t_key_home}_d"

    sel_away: bool = st.session_state.get(t_key_away, False)
    sel_home: bool = st.session_state.get(t_key_home, False)
    sel_date_away: Optional[datetime.datetime.now()] = st.session_state.get(t_key_away_d, datetime.datetime.now())
    sel_date_home: Optional[datetime.datetime.now()] = st.session_state.get(t_key_home_d, datetime.datetime.now())
    ot_or_so: bool = st.session_state.get(t_key_ot, False)

    if sel_away and sel_home:
        # not possible
        raise ValueError("This is not a valid state")

    if (sel_away and (game_away_id != team_id)) or (sel_home and (game_home_id != team_id)):
        # choose the losing team
        res = {
            "pts": 1 if ot_or_so else 0,
            "w": 0,
            "l": 0 if ot_or_so else 1,
            "otl/sol": 1 if ot_or_so else 0
        }
        # return 1 if ot_or_so else 0
    else:
        res = {
            "pts": 2 if ot_or_so else 3,
            "w": 1,
            "l": 0,
            "otl/sol": 0
        }

    for k in res:
        if k not in stats:
            st.write(f"pop {k}")
            res.pop(k)

    return res
    # return 2 if ot_or_so else 3


for i, rnd in enumerate(rounds):
    games_chosen[i] = {}
    for j, game_data in enumerate([g for g in games if g.get("round") == i]):
        game_id: int = game_data.get("game_id")
        games_chosen[i][game_id] = False


for i, game_data in enumerate(games):
    game_id: int = game_data.get("game_id")
    game_round: int = game_data.get("round")
    round_name: str = rounds[game_round]
    game_away_id: int = game_data.get("away")
    game_home_id: int = game_data.get("home")
    away_group: Optional[str] = None
    home_group: Optional[str] = None
    group: Optional[str] = None
    away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
    home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
    if away_team_data:
        a_data = away_team_data[0]
        away_name = a_data.get("name")
        away_group = a_data.get("group")
        away_flag_id = a_data.get("id")
    if home_team_data:
        h_data = home_team_data[0]
        home_name = h_data.get("name")
        home_group = h_data.get("group")
        home_flag_id = h_data.get("id")
    t_key: str = f"{round_name}_title"
    g_key_par: str = f"{round_name}_groups_parent"
    g_key: str = f"{round_name}_groups"
    g_num: int = i - sum([gpr for r, gpr in games_per_round.items() if r < game_round])

    if away_group or home_group:
        group = "".join(list({away_group, home_group}))

    t_key_ot = f"toggle_{game_id}_{group}_OT"
    t_key_away = f"toggle_{game_id}_{group}_Away"
    t_key_home = f"toggle_{game_id}_{group}_Home"
    t_key_away_d = f"{t_key_away}_d"
    t_key_home_d = f"{t_key_home}_d"

    # for k in [
    #     t_key_ot,
    #     t_key_away,
    #     t_key_home,
    #     t_key_away_d,
    #     t_key_home_d
    # ]:
    #     st.write(f"AA {k=}, {st.session_state.get(k)=}")

    sel_away: bool = st.session_state.get(t_key_away, False)
    sel_home: bool = st.session_state.get(t_key_home, False)
    sel_date_away: Optional[datetime.datetime.now()] = st.session_state.get(t_key_away_d, datetime.datetime.now())
    sel_date_home: Optional[datetime.datetime.now()] = st.session_state.get(t_key_home_d, datetime.datetime.now())

    # print(f"R{game_round}, {group}, {g_num}, {sel_away}, {sel_home}, {t_key_away=}, {t_key_home=}")

    if sel_away and sel_home:
        # cant select both teams
        change_away: bool = sel_date_away <= sel_date_home
        change = t_key_away if change_away else t_key_home
        change_d = f"{change}_d"
        st.session_state.update({
            change: False,
            change_d: None
        })
        tr = st.session_state.get("team_records", {})
        tr.setdefault(game_away_id, {"times_chosen": 0})
        tr.setdefault(game_home_id, {"times_chosen": 0})
        tc_away: int = tr[game_away_id].get("times_chosen", 0)
        tc_home: int = tr[game_home_id].get("times_chosen", 0)
        tr[game_away_id].update({
            "times_chosen": tc_away + (-1 if change_away else 0)
        })
        tr[game_home_id].update({
            "times_chosen": tc_home + (0 if change_away else -1)
        })
        st.session_state.update({"team_records": tr})
        st.write(f"FIX {change}, {change_away=}, {tc_away=}, {tc_home=}, {tr[game_away_id]['times_chosen']=}, {tr[game_home_id]['times_chosen']=}")

    if game_id is not None:
        games_chosen[game_round][game_id] = sel_away or sel_home


top_df_cols: list[str] = ["Team", "Name", "id", "tc", "pts", "w", "l", "otl/sol"]
top_df_cols_show: list[str] = ["Team", "Name", "pts", "w", "l", "otl/sol"]
df_calc_cols: list[str] = ["pts", "w", "l", "otl/sol"]
empty_data_a = [{"Team": flags_64[t["id"]], "Name": t["name"]} for t in sorted(teams_by_group[list_groups[0]], key=lambda t: t["name"])]
empty_data_b = [{"Team": flags_64[t["id"]], "Name": t["name"]} for t in sorted(teams_by_group[list_groups[1]], key=lambda t: t["name"])]

for empty_data in [empty_data_a, empty_data_b]:
    for i, ej in enumerate(empty_data):
        ej.update({col: 0 for col in top_df_cols[2:]})

df_top_a: pd.DataFrame = pd.DataFrame(data=empty_data_a, columns=top_df_cols)
df_top_b: pd.DataFrame = pd.DataFrame(data=empty_data_b, columns=top_df_cols)
relegation_a: list[int] = []
relegation_b: list[int] = []
prelim_games_chosen: bool = all(games_chosen[0].values())
# if prelim_games_chosen:
#     # all preliminary round games picked
tr = st.session_state.get("team_records", {})
game_ids_first_round: list[int] = [g["game_id"] for g in games if g["round"] == 0]
st.write("game_ids_first_round")
st.write(game_ids_first_round)
st.write("teams_by_group")
st.write(teams_by_group)
st.write("teams_by_group[list_groups[0]]")
st.write([t_["id"] for t_ in teams_by_group[list_groups[0]]])
st.write("games[game_id_to_idx[gid]]['away']['id']")
st.write(games[game_id_to_idx[0]]["away"])
tops = {
    g: [
        {
            "id": t["id"],
            "tc": tr[t["id"]]["times_chosen"],
            **game_points(
                game_id=[
                    gid for gid in game_ids_first_round
                    if (games_chosen[0][gid]) and (t["id"] in [
                        games[game_id_to_idx[gid]]["away"],
                        games[game_id_to_idx[gid]]["home"]
                    ])
                ],
                team_id=t["id"],
                stats=df_calc_cols
            )
        }
        for t in teams if t["id"] in [t_["id"] for t_ in teams_by_group[list_groups[i]]]
    ]
    for i, g in enumerate(list_groups)
}
top_a = tops["A"]
top_b = tops["B"]
st.write("top_a")
st.write(top_a)
st.write("top_b")
st.write(top_b)
top_a.sort(key=lambda t: t.get("pts", 0), reverse=True)
top_b.sort(key=lambda t: t.get("pts", 0), reverse=True)
lowest_pts_a: int = top_a[-1].get("pts", 0)
lowest_pts_b: int = top_b[-1].get("pts", 0)

relegation_a: list[int] = [t["id"] for t in top_a if t.get("pts", 0) == lowest_pts_a]
relegation_b: list[int] = [t["id"] for t in top_b if t.get("pts", 0) == lowest_pts_b]

st.write(f"Top {list_groups[0]}")
st.write(top_a)
st.write(f"Top {list_groups[1]}")
st.write(top_b)
st.write(f"{top_a[0]['id']}")
df_top_a = pd.DataFrame(top_a, columns=top_df_cols)
df_top_b = pd.DataFrame(top_b, columns=top_df_cols)
# df_top_a = pd.DataFrame(top_a, columns=["id"] + top_df_cols)
# df_top_b = pd.DataFrame(top_b, columns=["id"] + top_df_cols)
# df_top_a.columns = ["id", "tc", "Team", "Name", "pts", "w", "l", "otl/sol"]
# df_top_b.columns = ["id", "tc", "Team", "Name", "pts", "w", "l", "otl/sol"]
for col in top_df_cols:
    if col not in df_top_a:
        df_top_a[col] = 0
    if col not in df_top_b:
        df_top_b[col] = 0

df_top_a.fillna(0, inplace=True)
df_top_b.fillna(0, inplace=True)

for df in [df_top_a, df_top_b]:
    for col in df_calc_cols:
        df[col] = df[col].apply(lambda v: int(v))

st.write("df_top_a")
st.write(df_top_a)
st.write("df_top_b")
st.write(df_top_b)

for i in range(df_top_a.shape[0]):
    st.write(f"{i=}, {df_top_a.iloc[i]['id']=}")

print(f"{df_top_a}")

# df_top_a["Team"] = df_top_a.apply(lambda row: Path(flags[row["id"]]).resolve().as_uri(), axis=1)
# df_top_a["Team"] = df_top_a.apply(lambda row: flags[row["id"]], axis=1)
df_top_a["Team"] = df_top_a.apply(lambda row: flags_64[int(row["id"])], axis=1)
df_top_a["Name"] = df_top_a.apply(lambda row: teams[int(row["id"])]["name"], axis=1)
# df_top_b["Team"] = df_top_b.apply(lambda row: Path(flags[row["id"]]).resolve().as_uri(), axis=1)
# df_top_b["Team"] = df_top_b.apply(lambda row: flags[row["id"]], axis=1)
df_top_b["Team"] = df_top_b.apply(lambda row: flags_64[int(row["id"])], axis=1)
df_top_b["Name"] = df_top_b.apply(lambda row: teams[int(row["id"])]["name"], axis=1)

df_top_a.sort_values(by="Name", ascending=True, inplace=True, ignore_index=True)
df_top_a.sort_values(by="pts", ascending=False, inplace=True, ignore_index=True)
df_top_b.sort_values(by="Name", ascending=True, inplace=True, ignore_index=True)
df_top_b.sort_values(by="pts", ascending=False, inplace=True, ignore_index=True)

st.write("relegation_a")
st.write(relegation_a)
st.write("relegation_b")
st.write(relegation_b)

# st.write(f"All {rounds[0]} games chosen!")
st.write([f"{t['name']}" for t in teams])
st.write(tr)
# else:
#     st.write(f"Still need to select all {rounds[0]} games first")
#     st.write(games_chosen[0])


float_container = st.container(height=2000)
nav_container = st.container()


with nav_container:
    nav_tabs = st.tabs(
        tabs=rounds_pills
    )
    # nav_pills = pills(
    #     label="Rounds",
    #     options=rounds_pills
    # )

# with float_container:
html_table_a: str = create_html_table(
    df_top_a[top_df_cols_show],
    column_config={
        "Team": {
            "config_type": "image",
            "args": {
                "img_width": "50",
                "img_height": "40"
            }
        }
    }
)
# st.markdown(html_table_a, unsafe_allow_html=True)
# st.write("Group B")
html_table_b: str = create_html_table(
    df_top_b[top_df_cols_show],
    column_config={
        "Team": {
            "config_type": "image",
            "args": {
                "img_width": "50",
                "img_height": "40"
            }
        }
    }
)
# html = f'<div id="floating_standings_parent" style="position: relative;">'
# html = f'<div id="floating_standings_child" style="position: absolute; right: 5px; top: 5px;">'
html = f'<div id="floating_standings_child">'
html += f'<h3>Group A</h3>'
html += html_table_a
html += f'</div>'
html += f'</div>'
html += f'<h3>Group B</h3>'
html += html_table_b
html += f'</div>'
html += f'</div>'
html += f'</div>'
# st.markdown(html, unsafe_allow_html=True)

vid_y_pos = "2rem"
float_box(
    html,
    width="29rem",
    right="2rem",
    bottom=vid_y_pos,
    css="padding: 0;transition-property: all;transition-duration: .5s;transition-timing-function: cubic-bezier(0, 1, 0.5, 1);",
    shadow=12
)
    # float_parent()


# tables_css = float_css_helper(width="2.2rem", right="2rem", bottom=button_b_pos, transition=0)
# float_container.float(tables_css)


with nav_container:
    with nav_tabs[0]:
        # Preliminary
        rnd_games = [g for g in games if g["round"] == 0]
        rnd_games.sort(key=lambda gd: (gd["date"]))
        rnd_games_a = [g for g in rnd_games if (teams[g["away"]]["group"] == "A") and (teams[g["home"]]["group"] == "A")]
        rnd_games_b = [g for g in rnd_games if (teams[g["away"]]["group"] == "B") and (teams[g["home"]]["group"] == "B")]
        cols_groups = st.columns(2)
        # games_a = [g for g in rnd_games if ]
        for i in range(max(len(rnd_games_a), len(rnd_games_b))):
            # game_a, game_b = None, None
            rnd_games_lsts = [rnd_games_a, rnd_games_b]
            for j, group in enumerate(list_groups):
                if i < len(rnd_games_lsts[j]):
                    game_data = rnd_games_lsts[j][i]
                    game_id = game_data["game_id"]
                    away_id = game_data["away"]
                    home_id = game_data["home"]
                    date = game_data["date"]
                    cols_group_game = cols_groups[j].columns([0.4, 0.2, 0.4])

                    t_key_ot = f"toggle_{game_id}_{group}_OT"
                    t_key_away = f"toggle_{game_id}_{group}_Away"
                    t_key_home = f"toggle_{game_id}_{group}_Home"
                    t_key_away_d = f"{t_key_away}_d"
                    t_key_home_d = f"{t_key_home}_d"

                    # for k in [
                    #     t_key_ot,
                    #     t_key_away,
                    #     t_key_home,
                    #     t_key_away_d,
                    #     t_key_home_d
                    # ]:
                    #     st.write(f"BB {k=}, {st.session_state.get(k)=}")

                    cols_group_game[0].image(flags[away_id], width=flag_w)
                    # val = st.session_state.get(t_key_away, False)
                    # del st.session_state[t_key_away]
                    cols_group_game[0].toggle(
                        label="toggle",
                        # value=val,
                        # key=t_key_away,
                        key=t_key_away,
                        label_visibility="hidden",
                        on_change=lambda
                            t_=away_id,
                            tka_=t_key_away,
                            tkad=t_key_away_d:
                        select_team(t_, tka_, tkad)
                    )

                    cols_group_game[1].write(f"{group} - {date}")
                    # val = st.session_state.get(t_key_ot, False)
                    # del st.session_state[t_key_ot]
                    cols_group_game[1].toggle(
                        label="OT / SO",
                        # value=val,
                        key=t_key_ot
                        # key=f"{t_key_ot}_t"
                    )

                    cols_group_game[2].image(flags[home_id], width=flag_w)
                    # val = st.session_state.get(t_key_home, False)
                    # del st.session_state[t_key_home]
                    cols_group_game[2].toggle(
                        label="toggle",
                        # value=val,
                        key=t_key_home,
                        label_visibility="hidden",
                        on_change=lambda
                            t_=home_id,
                            tkh_=t_key_home,
                            tkhd=t_key_home_d:
                        select_team(t_, tkh_, tkhd)
                    )
            if i < len(rnd_games_b):
                game_b = rnd_games_b[i]

    with nav_tabs[1]:
        # Relegation
        if prelim_games_chosen:
            # st.write("Need to make relegation picks")
            relegation_cols = st.columns(2)
            with relegation_cols[0]:
                st.subheader("Group A")
                if len(relegation_a) > 1:
                    items = [
                        {"header": "save", "items": [t["name"] for t in teams if t["id"] in relegation_a]},
                        {"header": "relegate", "items": []}
                    ]
                    st.write("Please choose a team to relegate:")
                    relegation_a_sort = sort_items(
                        items,
                        key=f"sortable_relegation_a",
                        multi_containers=True
                    )

                    saved_a: list[int] = [t["id"] for t in teams if t["name"] in relegation_a_sort[0]["items"][:-1]]
                    if len(relegation_a_sort[0]["items"]) == 0:
                        saved_a = [teams[relegation_a_sort[0]["items"][0]]["id"]]
                    relegated_a: list[int] = [t["id"] for t in teams if t["name"] in relegation_a_sort[-1]["items"]]
                    if not relegated_a:
                        relegated_a = [t["id"] for t in teams if t["name"] in relegation_a_sort[0]["items"][-1:]]
                        # relegation_cols[0].info(f"You must select a team for the relegation game, {' '.join([t['name'] for t in teams if t["id"] in relegated_a])} chosen.")
                        st.info(f"You must select a team for the relegation game, {' '.join([t['name'] for t in teams if t['id'] in relegated_a])} chosen.")
                    if not saved_a:
                        saved_a = relegated_a[1:]
                        relegated_a = relegated_a[:1]
                        # relegation_cols[0].info(f"You can only relegate one team, {' '.join([t['name'] for t in teams if t["id"] in saved_a])} saved.")
                        st.info(f"You can only relegate one team, {' '.join([t['name'] for t in teams if t['id'] in saved_a])} saved.")
                else:
                    saved_a = []
                    relegated_a = relegation_a[-1:]
                    st.write(f"{teams[relegated_a[0]]['name']} chosen by record in preliminary round")

            with relegation_cols[1]:
                st.subheader("Group B")
                if len(relegation_b) > 1:
                    items = [
                        {"header": "save", "items": [t["name"] for t in teams if t["id"] in relegation_b]},
                        {"header": "relegate", "items": []}
                    ]
                    # with relegation_cols[0]:
                    st.write("Please choose a team to relegate:")
                    relegation_b_sort = sort_items(
                        items,
                        key=f"sortable_relegation_b",
                        multi_containers=True
                    )

                    saved_b: list[int] = [t["id"] for t in teams if t["name"] in relegation_b_sort[0]["items"][:-1]]
                    if len(relegation_b_sort[0]["items"]) == 0:
                        saved_b = [teams[relegation_b_sort[0]["items"][0]]["id"]]
                    relegated_b: list[int] = [t["id"] for t in teams if t["name"] in relegation_b_sort[-1]["items"]]
                    if not relegated_b:
                        relegated_b = [t["id"] for t in teams if t["name"] in relegation_b_sort[0]["items"][-1:]]
                        # relegation_cols[0].info(f"You must select a team for the relegation game, {' '.join([t['name'] for t in teams if t["id"] in relegated_a])} chosen.")
                        st.info(f"You must select a team for the relegation game, {' '.join([t['name'] for t in teams if t['id'] in relegated_b])} chosen.")
                    if not saved_b:
                        saved_b = relegated_b[1:]
                        relegated_b = relegated_b[:1]
                        # relegation_cols[0].info(f"You can only relegate one team, {' '.join([t['name'] for t in teams if t["id"] in saved_a])} saved.")
                        st.info(f"You can only relegate one team, {' '.join([t['name'] for t in teams if t['id'] in saved_b])} saved.")
                else:
                    saved_b = []
                    relegated_b = relegation_b[-1:]
                    st.write(f"{teams[relegated_b[0]]['name']} chosen by record in preliminary round")

        else:
            st.write(f"Please choose all games in the preliminary round first.")

    with nav_tabs[2]:
        # Quarters
        st.write("coming soon")

    with nav_tabs[3]:
        # Semis
        st.write("coming soon")

    with nav_tabs[4]:
        # Medal
        st.write("coming soon")

#
#
#
# def select_team(team_id: int, toggle_key: str, toggle_key_d: str):
#     st.session_state.update({
#         toggle_key_d: datetime.datetime.now()
#     })
#     is_sel = st.session_state.get(toggle_key)
#     tr = st.session_state.get("team_records", {})
#     if team_id not in tr:
#         tr.update({team_id: {"times_chosen": int(is_sel)}})
#     else:
#         chg = 1 if is_sel else -1
#         tr[team_id].update({"times_chosen": tr[team_id]["times_chosen"] + chg})
#     st.session_state.update({"team_records": tr})
#
#
# def game_points(game_id: int | list[int], team_id: int) -> int:
#
#     # print(f"GAMEPOINTS -> {game_id=}, {team_id=}")
#
#     if isinstance(game_id, list):
#         return sum([game_points(gid, team_id) for gid in game_id])
#
#     idx: int = game_id_to_idx[game_id]
#     game_data = games[idx]
#     game_away_id: int = game_data.get("away")
#     game_home_id: int = game_data.get("home")
#     v_teams: list[int] = [game_away_id, game_home_id]
#
#     if team_id not in v_teams:
#         raise ValueError(f"{team_id=} not found in available teams for {game_id=}. Got {v_teams}")
#
#     away_group: Optional[str] = None
#     home_group: Optional[str] = None
#     group: Optional[str] = None
#     away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
#     home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
#     if away_team_data:
#         a_data = away_team_data[0]
#         away_name = a_data.get("name")
#         away_group = a_data.get("group")
#         away_flag_id = a_data.get("id")
#     if home_team_data:
#         h_data = home_team_data[0]
#         home_name = h_data.get("name")
#         home_group = h_data.get("group")
#         home_flag_id = h_data.get("id")
#     if away_group or home_group:
#         group = "".join(list({away_group, home_group}))
#
#     t_key_ot = f"toggle_{game_id}_{group}_OT"
#     t_key_away = f"toggle_{game_id}_{group}_Away"
#     t_key_home = f"toggle_{game_id}_{group}_Home"
#     t_key_away_d = f"{t_key_away}_d"
#     t_key_home_d = f"{t_key_home}_d"
#
#     sel_away: bool = st.session_state.get(t_key_away, False)
#     sel_home: bool = st.session_state.get(t_key_home, False)
#     sel_date_away: Optional[datetime.datetime.now()] = st.session_state.get(t_key_away_d, datetime.datetime.now())
#     sel_date_home: Optional[datetime.datetime.now()] = st.session_state.get(t_key_home_d, datetime.datetime.now())
#     ot_or_so: bool = st.session_state.get(t_key_ot, False)
#
#     if sel_away and sel_home:
#         # not possible
#         raise ValueError("This is not a valid state")
#
#     if (sel_away and (game_away_id != team_id)) or (sel_home and (game_home_id != team_id)):
#         # choose the losing team
#         return 1 if ot_or_so else 0
#     return 2 if ot_or_so else 3
#
#
# grid = {
#     "title": st.container()
# }
#
#
# # grid.update({rnd: st.container() for rnd in rounds})
# for i, rnd in enumerate(rounds):
#     t_key: str = f"{rnd}_title"
#     g_key_par: str = f"{rnd}_groups_parent"
#     g_key: str = f"{rnd}_groups"
#     if i == 0:
#         # preliminary
#         grid[t_key] = st.container()
#         # grid[g_key_par] = st.container()
#         grid[g_key] = dict(zip(list_groups, [{}, {}]))
#         grid[g_key_par] = grid[t_key].columns(2)
#         for j in range(games_per_round[i]):
#             for k, group in enumerate(list_groups):
#                 grid[g_key][group][None] = grid[g_key_par][k].container()
#                 grid[g_key][group][j] = grid[g_key_par][k].columns([0.4, 0.2, 0.4])
#
#         # grid[g_key_par] = st.container()
#         # grid[g_key] = dict(zip(["A", "B"], grid[g_key_par].columns(2)))
#         # # grid[g_key] = {}
#         # grid[f"{g_key}_{t_key}_A"] = grid[g_key]["A"].container()
#         # grid[f"{g_key}_{t_key}_B"] = grid[g_key]["B"].container()
#         # grid[f"{g_key}_A"] = grid[g_key]["A"].columns([0.4, 0.2, 0.4])
#         # grid[f"{g_key}_B"] = grid[g_key]["B"].columns([0.4, 0.2, 0.4])
#         # elif i == 1:
#         #     # relegation
#     else:
#         grid[t_key] = st.container()
#         grid[g_key_par] = st.container()
#         grid[g_key] = {}
#         # grid[g_key] = st.container()
#         # grid[g_key] = st.columns([0.4, 0.2, 0.4])
#         for j in range(games_per_round[i]):
#             # jk: int = j + sum([gpr for r, gpr in games_per_round.items() if r < i])
#             jk = j
#             grid[g_key][None] = st.container()
#             grid[g_key][jk] = st.columns([0.4, 0.2, 0.4])
#
#     games_chosen[i] = {}
#     for j, game_data in enumerate([g for g in games if g.get("round") == i]):
#         game_id: int = game_data.get("game_id")
#         games_chosen[i][game_id] = False
#
# st.write(list(grid.keys()))
# # st.write(grid)
# # st.write(st.session_state)
#
# print(f"\n")
#
# for i, game_data in enumerate(games):
#     game_id: int = game_data.get("game_id")
#     game_round: int = game_data.get("round")
#     round_name: str = rounds[game_round]
#     game_away_id: int = game_data.get("away")
#     game_home_id: int = game_data.get("home")
#     away_group: Optional[str] = None
#     home_group: Optional[str] = None
#     group: Optional[str] = None
#     away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
#     home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
#     if away_team_data:
#         a_data = away_team_data[0]
#         away_name = a_data.get("name")
#         away_group = a_data.get("group")
#         away_flag_id = a_data.get("id")
#     if home_team_data:
#         h_data = home_team_data[0]
#         home_name = h_data.get("name")
#         home_group = h_data.get("group")
#         home_flag_id = h_data.get("id")
#     t_key: str = f"{round_name}_title"
#     g_key_par: str = f"{round_name}_groups_parent"
#     g_key: str = f"{round_name}_groups"
#     g_num: int = i - sum([gpr for r, gpr in games_per_round.items() if r < game_round])
#
#     if away_group or home_group:
#         group = "".join(list({away_group, home_group}))
#
#     t_key_ot = f"toggle_{game_id}_{group}_OT"
#     t_key_away = f"toggle_{game_id}_{group}_Away"
#     t_key_home = f"toggle_{game_id}_{group}_Home"
#     t_key_away_d = f"{t_key_away}_d"
#     t_key_home_d = f"{t_key_home}_d"
#     sel_away: bool = st.session_state.get(t_key_away, False)
#     sel_home: bool = st.session_state.get(t_key_home, False)
#     sel_date_away: Optional[datetime.datetime.now()] = st.session_state.get(t_key_away_d, datetime.datetime.now())
#     sel_date_home: Optional[datetime.datetime.now()] = st.session_state.get(t_key_home_d, datetime.datetime.now())
#
#     # print(f"R{game_round}, {group}, {g_num}, {sel_away}, {sel_home}, {t_key_away=}, {t_key_home=}")
#
#     if sel_away and sel_home:
#         # cant select both teams
#         change_away: bool = sel_date_away <= sel_date_home
#         change = t_key_away if change_away else t_key_home
#         change_d = f"{change}_d"
#         st.session_state.update({
#             change: False,
#             change_d: None
#         })
#         tr = st.session_state.get("team_records", {})
#         tr.setdefault(game_away_id, {"times_chosen": 0})
#         tr.setdefault(game_home_id, {"times_chosen": 0})
#         tc_away: int = tr[game_away_id].get("times_chosen", 0)
#         tc_home: int = tr[game_home_id].get("times_chosen", 0)
#         tr[game_away_id].update({
#             "times_chosen": tc_away + (-1 if change_away else 0)
#         })
#         tr[game_home_id].update({
#             "times_chosen": tc_home + (0 if change_away else -1)
#         })
#         st.session_state.update({"team_records": tr})
#         st.write(f"FIX {change}, {change_away=}, {tc_away=}, {tc_home=}, {tr[game_away_id]['times_chosen']=}, {tr[game_home_id]['times_chosen']=}")
#
#     if game_id is not None:
#         games_chosen[game_round][game_id] = sel_away or sel_home
#     # if game_away_id is not None:
#     #     print(f"ADJ {game_away_id} => {int(sel_away)}", end="")
#     #     team_records[game_away_id]["times_chosen"] += int(sel_away)
#     # if game_home_id is not None:
#     #     print(f", ADJ {game_home_id} => {int(sel_home)}", end="")
#     #     team_records[game_home_id]["times_chosen"] += int(sel_home)
#     # print(f"")
#
#
# df_top_a: pd.DataFrame = pd.DataFrame()
# df_top_b: pd.DataFrame = pd.DataFrame()
# relegation_a: list[int] = []
# relegation_b: list[int] = []
# prelim_games_chosen: bool = all(games_chosen[0].values())
# if prelim_games_chosen:
#     # all preliminary round games picked
#     tr = st.session_state.get("team_records", {})
#     game_ids_first_round: list[int] = [g["game_id"] for g in games if g["round"] == 0]
#     st.write("teams_by_group")
#     st.write(teams_by_group)
#     st.write("teams_by_group[list_groups[0]]")
#     st.write([t_["id"] for t_ in teams_by_group[list_groups[0]]])
#     st.write("games[game_id_to_idx[gid]]['away']['id']")
#     st.write(games[game_id_to_idx[0]]["away"])
#     tops = {
#         g: [
#             {
#                 "id": t["id"],
#                 "tc": tr[t["id"]]["times_chosen"],
#                 "pts": game_points(
#                     game_id=[
#                         gid for gid in game_ids_first_round
#                         if t["id"] in [
#                             games[game_id_to_idx[gid]]["away"],
#                             games[game_id_to_idx[gid]]["home"]
#                         ]
#                     ],
#                     team_id=t["id"])
#             }
#             for t in teams if t["id"] in [t_["id"] for t_ in teams_by_group[list_groups[i]]]
#         ]
#         for i, g in enumerate(list_groups)
#     }
#     top_a = tops["A"]
#     top_b = tops["B"]
#     top_a.sort(key=lambda t: t["pts"], reverse=True)
#     top_b.sort(key=lambda t: t["pts"], reverse=True)
#     lowest_pts_a: int = top_a[-1]["pts"]
#     lowest_pts_b: int = top_b[-1]["pts"]
#
#     relegation_a: list[int] = [t["id"] for t in top_a if t["pts"] == lowest_pts_a]
#     relegation_b: list[int] = [t["id"] for t in top_b if t["pts"] == lowest_pts_b]
#
#     st.write(f"Top {list_groups[0]}")
#     st.write(top_a)
#     st.write(f"Top {list_groups[1]}")
#     st.write(top_b)
#     df_top_a = pd.DataFrame(top_a)
#     df_top_b = pd.DataFrame(top_b)
#     # df_top_a["Team"] = df_top_a.apply(lambda row: Path(flags[row["id"]]).resolve().as_uri(), axis=1)
#     # df_top_a["Team"] = df_top_a.apply(lambda row: flags[row["id"]], axis=1)
#     df_top_a["Team"] = df_top_a.apply(lambda row: flags_64[row["id"]], axis=1)
#     df_top_a["Name"] = df_top_a.apply(lambda row: teams[row["id"]]["name"], axis=1)
#     # df_top_b["Team"] = df_top_b.apply(lambda row: Path(flags[row["id"]]).resolve().as_uri(), axis=1)
#     # df_top_b["Team"] = df_top_b.apply(lambda row: flags[row["id"]], axis=1)
#     df_top_b["Team"] = df_top_b.apply(lambda row: flags_64[row["id"]], axis=1)
#     df_top_b["Name"] = df_top_b.apply(lambda row: teams[row["id"]]["name"], axis=1)
#
#     st.write("relegation_a")
#     st.write(relegation_a)
#     st.write("relegation_b")
#     st.write(relegation_b)
#
#     st.write(f"All {rounds[0]} games chosen!")
#     st.write([f"{t['name']}" for t in teams])
#     st.write(tr)
# else:
#     st.write(f"Still need to select all {rounds[0]} games first")
#     st.write(games_chosen[0])
#
#
# last_round: Optional[str] = None
# shown_dates: dict[str: set] = {}
# shown_groups: dict[str: set] = {}
#
# for i, game_data in enumerate(games):
#     # r_idx = i // cols_per_row
#     # c_idx = i % cols_per_row
#     game_id: int = game_data.get("game_id")
#     game_round: int = game_data.get("round")
#     round_name: str = rounds[game_round]
#     game_date_s: str = game_data.get("date")
#     game_location: str = game_data.get("location")
#     game_away_code: str = game_data.get("away_code")
#     game_home_code: str = game_data.get("home_code")
#     game_away_id: int = game_data.get("away")
#     game_home_id: int = game_data.get("home")
#
#     away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
#     home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
#     a_data: dict[str: Any] = {}
#     h_data: dict[str: Any] = {}
#     home_name: str = game_home_code
#     away_name: str = game_away_code
#     away_group: Optional[str] = None
#     home_group: Optional[str] = None
#     away_flag_id: Optional[int] = None
#     home_flag_id: Optional[int] = None
#
#     bg_away: Colour = default_bg_team_col
#
#     if away_team_data:
#         a_data = away_team_data[0]
#         away_name = a_data.get("name")
#         away_group = a_data.get("group")
#         away_flag_id = a_data.get("id")
#     if home_team_data:
#         h_data = home_team_data[0]
#         home_name = h_data.get("name")
#         home_group = h_data.get("group")
#         home_flag_id = h_data.get("id")
#
#     group: Optional[str] = None
#     t_key: str = f"{round_name}_title"
#     g_key_par: str = f"{round_name}_groups_parent"
#     g_key: str = f"{round_name}_groups"
#     g_num: int = i - sum([gpr for r, gpr in games_per_round.items() if r < game_round])
#
#     if away_group or home_group:
#         group = "".join(list({away_group, home_group}))
#     # st.write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}, {group=}, {game_round=}, {round_name=}")
#     if (last_round is None) or (round_name != last_round):
#         grid[t_key].write(f"---")
#         grid[t_key].write(f"{round_name}")
#         last_round = round_name
#
#     st.write(f"{i=}, {g_num=}, {g_key=}, {group=}")
#     if game_round == 0:
#         gpr: int = games_per_round[game_round]
#         shown_groups.setdefault(round_name, set())
#         if group not in shown_groups[round_name]:
#             # # grid[g_key][group].write(f"Group {group} - {game_location}")
#             # # grid[f"{g_key}_{group}"][1 if group == "B" else 0].write(f"Group {group} - {game_location}")
#             # grid[f"{g_key}_{t_key}_{group}"].write(f"Group {group} - {game_location}")
#             shown_groups[round_name].add(group)
#             # for j in range(gpr):
#             # grid[g_key][group][j].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
#
#         t_key_ot = f"toggle_{game_id}_{group}_OT"
#         t_key_away = f"toggle_{game_id}_{group}_Away"
#         t_key_home = f"toggle_{game_id}_{group}_Home"
#         t_key_away_d = f"{t_key_away}_d"
#         t_key_home_d = f"{t_key_home}_d"
#
#         grid[g_key][group][g_num][0].image(flags[away_flag_id], width=flag_w)
#         grid[g_key][group][None].write("I AM THE NONE")
#         grid[g_key][group][g_num][0].toggle(
#             label="toggle",
#             key=t_key_away,
#             label_visibility="hidden",
#             on_change=lambda
#                 t_=game_away_id,
#                 r_=game_round,
#                 g_=group,
#                 gn_=g_num,
#                 tka_=t_key_away,
#                 tkad=t_key_away_d:
#             select_team(t_, r_, g_, gn_, tka_, tkad)
#         )
#
#         grid[g_key][group][g_num][1].write(f"{group} - {game_date_s}")
#         grid[g_key][group][g_num][1].toggle(
#             label="OT / SO",
#             key=t_key_ot
#         )
#
#         grid[g_key][group][g_num][2].image(flags[home_flag_id], width=flag_w)
#         grid[g_key][group][g_num][2].toggle(
#             label="toggle",
#             key=t_key_home,
#             label_visibility="hidden",
#             on_change=lambda
#                 t_=game_home_id,
#                 r_=game_round,
#                 g_=group,
#                 gn_=g_num,
#                 tkh_=t_key_home,
#                 tkhd=t_key_home_d:
#             select_team(t_, r_, g_, gn_, tkh_, tkhd)
#         )
#         print(f"{away_name} => {st.session_state.get(t_key_away)} || {home_name} <= {st.session_state.get(t_key_home)} == {t_key_away=}, {t_key_home=}")
#
#         # # grid[g_key][group].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
#         # # grid[g_key][group].image(flags[away_flag_id])
#         # # grid[g_key][group].image(flags[home_flag_id])
#         # grid[f"{g_key}_{group}"][0].image(flags[away_flag_id], width=flag_w)
#         # grid[f"{g_key}_{group}"][1].write(f"{game_date_s}")
#         # grid[f"{g_key}_{group}"][2].image(flags[home_flag_id], width=flag_w)
#         # # grid[f"{g_key_par}"].write("---")
#         # # grid[g_key][group].write("---")
#         # grid[f"{g_key}_{t_key}_{group}"].write("---")
#     else:
#         # # grid[g_key].write(f"{game_location}")
#         # # grid[g_key].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
#         # grid[g_key][0].image(flags[away_flag_id], width=flag_w)
#         # grid[g_key][1].write(f"{game_date_s}")
#         # grid[g_key][2].image(flags[away_flag_id], width=flag_w)
#
#         if game_round == 1:
#             if prelim_games_chosen:
#
#                 relegation_cols = grid[g_key_par].columns(2)
#
#                 # st.dataframe(df_top_a[["Team", "Name", "tc", "pts"]])
#                 # st.markdown(df_top_a[["Team", "Name", "tc", "pts"]].to_html(), unsafe_allow_html=True)
#
#                 # local images dont work in a browser:
#                 # st.data_editor(
#                 #     df_top_a[["Team", "Name", "tc", "pts"]],
#                 #     hide_index=True,
#                 #     column_config={
#                 #         "Team": st.column_config.ImageColumn(
#                 #             "Team",
#                 #             width="large"
#                 #         )
#                 #     },
#                 #     disabled=True,
#                 #     key=f"df_top_teams_A"
#                 # )
#
#                 # instead use the base64 embedding approach and a custom html table
#                 html_table_a: str = create_html_table(
#                     df_top_a[["Team", "Name", "tc", "pts"]],
#                     column_config={
#                         "Team": {
#                             "config_type": "image",
#                             "args": {
#                                 "img_width": "125",
#                                 "img_height": "125"
#                             }
#                         }
#                     }
#                 )
#                 relegation_cols[0].markdown(
#                     html_table_a,
#                     unsafe_allow_html=True
#                 )
#
#                 if len(relegation_a) > 1:
#                     items = [
#                         {"header": "save", "items": [t["name"] for t in teams if t["id"] in relegation_a]},
#                         {"header": "relegate", "items": []}
#                     ]
#                     with relegation_cols[0]:
#                         st.write("Please choose a team to relegate:")
#                         relegation_a_sort = sort_items(
#                             items,
#                             key=f"sortable_relegation_a",
#                             multi_containers=True
#                         )
#
#                     saved_a: list[int] = [t["id"] for t in teams if t["name"] in relegation_a_sort[0]["items"][:-1]]
#                     if len(relegation_a_sort[0]["items"]) == 0:
#                         saved_a = [teams[relegation_a_sort[0]["items"][0]]["id"]]
#                     relegated_a: list[int] = [t["id"] for t in teams if t["name"] in relegation_a_sort[-1]["items"]]
#                     if not relegated_a:
#                         relegated_a = [t["id"] for t in teams if t["name"] in relegation_a_sort[0]["items"][-1:]]
#                         relegation_cols[0].info(f"You must select a team for the relegation game, {' '.join([t['name'] for t in teams if t["id"] in relegated_a])} chosen.")
#                     if not saved_a:
#                         saved_a = relegated_a[1:]
#                         relegated_a = relegated_a[:1]
#                         relegation_cols[0].info(f"You can only relegate one team, {' '.join([t['name'] for t in teams if t["id"] in saved_a])} saved.")
#                 else:
#                     saved_a = []
#                     relegated_a = relegation_a[-1:]
#
#                 html_table_b: str = create_html_table(
#                     df_top_b[["Team", "Name", "tc", "pts"]],
#                     column_config={
#                         "Team": {
#                             "config_type": "image",
#                             "args": {
#                                 "img_width": "125",
#                                 "img_height": "125"
#                             }
#                         }
#                     }
#                 )
#                 relegation_cols[1].markdown(
#                     html_table_b,
#                     unsafe_allow_html=True
#                 )
#
#                 if len(relegation_b) > 1:
#                     items = [
#                         {"header": "save", "items": [t["name"] for t in teams if t["id"] in relegation_b]},
#                         {"header": "relegate", "items": []}
#                     ]
#                     with relegation_cols[1]:
#                         st.write("Please choose a team to relegate:")
#                         relegation_b_sort = sort_items(
#                             items,
#                             key=f"sortable_relegation_b",
#                             multi_containers=True
#                         )
#
#                     saved_b: list[int] = [t["id"] for t in teams if t["name"] in relegation_b_sort[0]["items"][:-1]]
#                     if len(relegation_b_sort[0]["items"]) == 0:
#                         saved_b = [teams[relegation_b_sort[0]["items"][0]]["id"]]
#                     relegated_b: list[int] = [t["id"] for t in teams if t["name"] in relegation_b_sort[-1]["items"]]
#                     if not relegated_b:
#                         relegation_cols[1].info(f"You must select a team for the relegation game, {' '.join([t['name'] for t in teams if t["id"] in relegated_b])} chosen.")
#                         relegated_b = [t["id"] for t in teams if t["name"] in relegation_b_sort[0]["items"][-1:]]
#                     if not saved_b:
#                         saved_b = relegated_b[1:]
#                         relegated_b = relegated_b[:1]
#                         relegation_cols[1].info(f"You can only relegate one team, {' '.join([t['name'] for t in teams if t["id"] in saved_b])} saved.")
#                 else:
#                     saved_b = []
#                     relegated_b = relegation_b[-1:]
#
#                 relegation_cols[0].write("saved_a")
#                 relegation_cols[0].write(saved_a)
#                 relegation_cols[0].write("relegated_a")
#                 relegation_cols[0].write(relegated_a)
#
#                 relegation_cols[1].write("saved_b")
#                 relegation_cols[1].write(saved_b)
#                 relegation_cols[1].write("relegated_b")
#                 relegation_cols[1].write(relegated_b)
#
#                 if relegated_a:
#                     away_team_data: list[dict] = [t for t in teams if t["id"] == relegated_a[0]]
#                     if away_team_data:
#                         a_data = away_team_data[0]
#                         away_name = a_data.get("name")
#                         away_group = a_data.get("group")
#                         away_flag_id = a_data.get("id")
#
#                 if relegated_b:
#                     home_team_data: list[dict] = [t for t in teams if t["id"] == relegation_b[0]]
#                     if home_team_data:
#                         h_data = home_team_data[0]
#                         home_name = h_data.get("name")
#                         home_group = h_data.get("group")
#                         home_flag_id = h_data.get("id")
#
#         grid[g_key][g_num][0].image(flags[away_flag_id], width=flag_w)
#         grid[g_key][g_num][1].write(f"{game_date_s}")
#         grid[g_key][g_num][2].image(flags[home_flag_id], width=flag_w)
#
#     # container = grid[round_name]
#     # if game_round < 2:
#     #     container = grid[f"{game_round}_groups"]
#
#     # grid.append(st.columns(cols_per_row))
#     # grid[r_idx][c_idx].write(f"{away_name} VS {home_name}")
#
#
# for i, flag_key in enumerate(flags):
#     if flag_key:
#         flag_path: str = flags[flag_key]
#         flag_path: str = os.path.basename(flag_path)
#         if flag_path in image_refs_htmls:
#             html_ = image_refs_htmls[flag_path]
#             st.markdown(html_, unsafe_allow_html=True)
#         else:
#             st.write(f"skip {flag_path=}")
#
#
#
# # import base64
# # import datetime
# # import json
# # import os.path
# # from pathlib import Path
# #
# # from typing import Any, Optional
# #
# # import pandas as pd
# # from streamlit_sortables import sort_items
# #
# # import streamlit as st
# #
# # from colour_utility import Colour
# # from icons_8_refs import image_refs_htmls
# #
# #
# # st.set_page_config(layout="wide")
# #
# #
# # def create_html_table(
# #     df: pd.DataFrame,
# #     column_config: Optional[dict[str: Any]] = None
# # ) -> str:
# #     """
# #     Create a custom HTML table with alternate row backgrounds.
# #
# #     LAST UPDATED 2024-12-19 20:41
# #
# #     Args:
# #         df (pd.DataFrame): The DataFrame to render as an HTML table.
# #
# #     Returns:
# #         str: The HTML string representing the table.
# #     """
# #     # Initialize the HTML table with styles
# #     html = '<table style="border-collapse: collapse; width: 100%;">'
# #
# #     valid_configs = {
# #         "image": {
# #             # "func": lambda img, img_width="100", img_height="100": f'<td style="border: 1px solid #ddd; padding: 8px;"><img src="{img}" alt="{img}" width="{img_width}" height="{img_height}"></td>',
# #             "func": lambda img, img_width="100",
# #                            img_height="100": f'<img src="{img}" alt="{img}" width="{img_width}" height="{img_height}">',
# #             "args": ["img_width", "img_height"]
# #         }
# #     }
# #
# #     columns = df.columns
# #
# #     if column_config is None:
# #         column_config = {}
# #     else:
# #         to_remove = []
# #         for col in column_config:
# #             if col not in columns:
# #                 # to_remove.append(col)
# #                 raise ValueError(f"Unrecognized column '{col}'.")
# #             else:
# #                 config_type: str = column_config[col].get("config_type")
# #                 if config_type is None:
# #                     raise ValueError(
# #                         f"You must specify how to configure column '{col}'. Include 'config_type' as a keyword and set to one of {' '.join(list(valid_configs))}")
# #                 config_args: list[Any] | dict[str: Any] = column_config.get("args", [])
# #                 v_args: list[str] = valid_configs[config_type]["args"]
# #
# #                 if isinstance(config_args, dict):
# #                     for k, v in config_args.items():
# #                         if k not in v_args:
# #                             raise ValueError(
# #                                 f"unrecognized kwarg '{k}' for {config_type=}, expected one of {' '.join(v_args)}")
# #
# #                 # func = valid_configs[config_type]["func"]
# #
# #                 # l_args = len(v_args)
# #                 # for i, kw in enumerate(column_config[col]):
# #                 #     val = column_config[col][kw]
# #                 #     if i > l_args:
# #                 #         raise ValueError(f"Got too many arguments to configure this column type ({})")
# #
# #         for col in to_remove:
# #             del column_config[col]
# #
# #     # print(f"{df=}")
# #
# #     # Add table headers
# #     html += '<thead style="background-color: #2f2f2f; font-weight: bold;">'
# #     html += '<tr>'
# #     for col in columns:
# #         html += f'<th style="border: 1px solid #ddd; padding: 8px;">{col}</th>'
# #     html += '</tr>'
# #     html += '</thead>'
# #
# #     # Add table rows with alternate-row styling
# #     html += '<tbody>'
# #     for i, row in df.iterrows():
# #         # Determine row background color
# #         # print(f"{i=}, {list(row)=}")
# #         i: int = int(i)
# #         bg_color = '#4f4f4f' if i % 2 == 0 else '#9f9f9f'
# #         html += f'<tr style="background-color: {bg_color};">'
# #         for j, col in enumerate(columns):
# #             value = row[col]
# #             if col in column_config:
# #                 config_type: str = column_config[col]["config_type"]
# #                 func = valid_configs[config_type]["func"]
# #                 args = column_config[col].get("args", [])
# #                 if isinstance(args, dict):
# #                     value = func(value, **args)
# #                 else:
# #                     value = func(value, *args)
# #             html += f'<td style="border: 1px solid #ddd; padding: 8px;">{value}</td>'
# #         html += '</tr>'
# #     html += '</tbody>'
# #
# #     # Close the table
# #     html += '</table>'
# #
# #     return html
# #
# #
# # @st.cache_data(show_spinner=True)
# # def load_data_file():
# #     with open(r"./wjc_2025.json", "r") as f:
# #         return json.load(f)
# #
# #
# # @st.cache_data(show_spinner=True)
# # def load_flags():
# #     pictures = os.listdir(root_image_folder)
# #     flags = {}
# #     for i, team_data in enumerate(teams):
# #         team_id: int = team_data.get("id")
# #         name_long: str = team_data.get("name_long")
# #         name: str = team_data.get("name")
# #         n: str = name_long.lower()
# #         match n:
# #             case "united states of america": n = "usa"
# #             case "czechia": n = "czech-republic"
# #             case _: pass
# #         j: int = 0
# #         found: bool = False
# #         for j, picture in enumerate(pictures):
# #             p: str = picture.lower().replace("icons8-", "").replace("-flag-96", "").replace("-96.png", ".png").strip()
# #             print(f"\t{p=}, {n=}")
# #             if picture.endswith(".png") and (n in p):
# #                 flags[i] = os.path.join(root_image_folder, picture)
# #                 found = True
# #                 break
# #         if found:
# #             pictures.pop(j)
# #         else:
# #             print(f"No image found for '{n}'")
# #
# #     flags[None] = os.path.join(root_image_folder, "unknown_flag.png")
# #
# #     return flags
# #
# #
# # @st.cache_data(show_spinner=True)
# # def load_flags_64(flag_paths):
# #     flags_64 = []
# #     for image_path in flag_paths.values():
# #         if image_path is not None:
# #             with open(image_path, "rb") as img_file:
# #                 flags_64.append(f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}")
# #     return flags_64
# #
# #
# # root_image_folder = r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags"
# # if not os.path.exists(root_image_folder):
# #     root_image_folder = r"C:\Users\abrig\Documents\Coding_Practice\Resources\Flags"
# #
# #
# # default_bg_team_col: Colour = Colour("#151530")
# #
# #
# # initial_data: dict[str: Any] = load_data_file()
# # teams: list[dict] = initial_data["teams"]
# # rounds: list[str] = initial_data["rounds"]
# # games: list[dict] = initial_data["schedule"]["games"]
# # games_per_round: dict[int: int] = {}
# # list_groups: list[str] = ["A", "B"]
# # teams_by_group: dict[str: list[int]] = {g: [t for t in teams if t["group"] == g] for g in list_groups}
# # game_id_to_idx: dict[int: int] = {g["game_id"]: i for i, g in enumerate(games)}
# # flags = load_flags()
# # flags_64 = load_flags_64(flags)
# # flag_w, flag_h = 100, 50
# #
# # st.write(flags)
# # st.json(initial_data)
# #
# # cols_per_row: int = 2
# #
# # for i, g in enumerate(games):
# #     rnd: int = g["round"]
# #     if rnd not in games_per_round:
# #         games_per_round[rnd] = 0
# #     games_per_round[rnd] += 1
# #
# # n_rows = int(round(len(games) / cols_per_row))
# # games_chosen: dict[int: dict[int: bool]] = {}
# # st.session_state.setdefault("team_records", {
# #     t.get("id"): {
# #         "times_chosen": 0
# #     }
# #     for t in teams
# # })
# #
# #
# # def select_team(team_id: int, round_num: int, group: str, game_num: int, toggle_key: str, toggle_key_d: str):
# #     st.session_state.update({
# #         toggle_key_d: datetime.datetime.now()
# #     })
# #     is_sel = st.session_state.get(toggle_key)
# #     tr = st.session_state.get("team_records", {})
# #     if team_id not in tr:
# #         tr.update({team_id: {"times_chosen": int(is_sel)}})
# #     else:
# #         chg = 1 if is_sel else -1
# #         tr[team_id].update({"times_chosen": tr[team_id]["times_chosen"] + chg})
# #     st.session_state.update({"team_records": tr})
# #
# #
# # def game_points(game_id: int | list[int], team_id: int) -> int:
# #
# #     # print(f"GAMEPOINTS -> {game_id=}, {team_id=}")
# #
# #     if isinstance(game_id, list):
# #         return sum([game_points(gid, team_id) for gid in game_id])
# #
# #     idx: int = game_id_to_idx[game_id]
# #     game_data = games[idx]
# #     game_away_id: int = game_data.get("away")
# #     game_home_id: int = game_data.get("home")
# #     v_teams: list[int] = [game_away_id, game_home_id]
# #
# #     if team_id not in v_teams:
# #         raise ValueError(f"{team_id=} not found in available teams for {game_id=}. Got {v_teams}")
# #
# #     away_group: Optional[str] = None
# #     home_group: Optional[str] = None
# #     group: Optional[str] = None
# #     away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
# #     home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
# #     if away_team_data:
# #         a_data = away_team_data[0]
# #         away_name = a_data.get("name")
# #         away_group = a_data.get("group")
# #         away_flag_id = a_data.get("id")
# #     if home_team_data:
# #         h_data = home_team_data[0]
# #         home_name = h_data.get("name")
# #         home_group = h_data.get("group")
# #         home_flag_id = h_data.get("id")
# #     if away_group or home_group:
# #         group = "".join(list({away_group, home_group}))
# #
# #     t_key_ot = f"toggle_{game_id}_{group}_OT"
# #     t_key_away = f"toggle_{game_id}_{group}_Away"
# #     t_key_home = f"toggle_{game_id}_{group}_Home"
# #     t_key_away_d = f"{t_key_away}_d"
# #     t_key_home_d = f"{t_key_home}_d"
# #
# #     sel_away: bool = st.session_state.get(t_key_away, False)
# #     sel_home: bool = st.session_state.get(t_key_home, False)
# #     sel_date_away: Optional[datetime.datetime.now()] = st.session_state.get(t_key_away_d, datetime.datetime.now())
# #     sel_date_home: Optional[datetime.datetime.now()] = st.session_state.get(t_key_home_d, datetime.datetime.now())
# #     ot_or_so: bool = st.session_state.get(t_key_ot, False)
# #
# #     if sel_away and sel_home:
# #         # not possible
# #         raise ValueError("This is not a valid state")
# #
# #     if (sel_away and (game_away_id != team_id)) or (sel_home and (game_home_id != team_id)):
# #         # choose the losing team
# #         return 1 if ot_or_so else 0
# #     return 2 if ot_or_so else 3
# #
# #
# # grid = {
# #     "title": st.container()
# # }
# #
# #
# # # grid.update({rnd: st.container() for rnd in rounds})
# # for i, rnd in enumerate(rounds):
# #     t_key: str = f"{rnd}_title"
# #     g_key_par: str = f"{rnd}_groups_parent"
# #     g_key: str = f"{rnd}_groups"
# #     if i == 0:
# #         # preliminary
# #         grid[t_key] = st.container()
# #         # grid[g_key_par] = st.container()
# #         grid[g_key] = dict(zip(list_groups, [{}, {}]))
# #         grid[g_key_par] = grid[t_key].columns(2)
# #         for j in range(games_per_round[i]):
# #             for k, group in enumerate(list_groups):
# #                 grid[g_key][group][None] = grid[g_key_par][k].container()
# #                 grid[g_key][group][j] = grid[g_key_par][k].columns([0.4, 0.2, 0.4])
# #
# #         # grid[g_key_par] = st.container()
# #         # grid[g_key] = dict(zip(["A", "B"], grid[g_key_par].columns(2)))
# #         # # grid[g_key] = {}
# #         # grid[f"{g_key}_{t_key}_A"] = grid[g_key]["A"].container()
# #         # grid[f"{g_key}_{t_key}_B"] = grid[g_key]["B"].container()
# #         # grid[f"{g_key}_A"] = grid[g_key]["A"].columns([0.4, 0.2, 0.4])
# #         # grid[f"{g_key}_B"] = grid[g_key]["B"].columns([0.4, 0.2, 0.4])
# #         # elif i == 1:
# #         #     # relegation
# #     else:
# #         grid[t_key] = st.container()
# #         grid[g_key_par] = st.container()
# #         grid[g_key] = {}
# #         # grid[g_key] = st.container()
# #         # grid[g_key] = st.columns([0.4, 0.2, 0.4])
# #         for j in range(games_per_round[i]):
# #             # jk: int = j + sum([gpr for r, gpr in games_per_round.items() if r < i])
# #             jk = j
# #             grid[g_key][None] = st.container()
# #             grid[g_key][jk] = st.columns([0.4, 0.2, 0.4])
# #
# #     games_chosen[i] = {}
# #     for j, game_data in enumerate([g for g in games if g.get("round") == i]):
# #         game_id: int = game_data.get("game_id")
# #         games_chosen[i][game_id] = False
# #
# # st.write(list(grid.keys()))
# # # st.write(grid)
# # # st.write(st.session_state)
# #
# # print(f"\n")
# #
# # for i, game_data in enumerate(games):
# #     game_id: int = game_data.get("game_id")
# #     game_round: int = game_data.get("round")
# #     round_name: str = rounds[game_round]
# #     game_away_id: int = game_data.get("away")
# #     game_home_id: int = game_data.get("home")
# #     away_group: Optional[str] = None
# #     home_group: Optional[str] = None
# #     group: Optional[str] = None
# #     away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
# #     home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
# #     if away_team_data:
# #         a_data = away_team_data[0]
# #         away_name = a_data.get("name")
# #         away_group = a_data.get("group")
# #         away_flag_id = a_data.get("id")
# #     if home_team_data:
# #         h_data = home_team_data[0]
# #         home_name = h_data.get("name")
# #         home_group = h_data.get("group")
# #         home_flag_id = h_data.get("id")
# #     t_key: str = f"{round_name}_title"
# #     g_key_par: str = f"{round_name}_groups_parent"
# #     g_key: str = f"{round_name}_groups"
# #     g_num: int = i - sum([gpr for r, gpr in games_per_round.items() if r < game_round])
# #
# #     if away_group or home_group:
# #         group = "".join(list({away_group, home_group}))
# #
# #     t_key_ot = f"toggle_{game_id}_{group}_OT"
# #     t_key_away = f"toggle_{game_id}_{group}_Away"
# #     t_key_home = f"toggle_{game_id}_{group}_Home"
# #     t_key_away_d = f"{t_key_away}_d"
# #     t_key_home_d = f"{t_key_home}_d"
# #     sel_away: bool = st.session_state.get(t_key_away, False)
# #     sel_home: bool = st.session_state.get(t_key_home, False)
# #     sel_date_away: Optional[datetime.datetime.now()] = st.session_state.get(t_key_away_d, datetime.datetime.now())
# #     sel_date_home: Optional[datetime.datetime.now()] = st.session_state.get(t_key_home_d, datetime.datetime.now())
# #
# #     # print(f"R{game_round}, {group}, {g_num}, {sel_away}, {sel_home}, {t_key_away=}, {t_key_home=}")
# #
# #     if sel_away and sel_home:
# #         # cant select both teams
# #         change_away: bool = sel_date_away <= sel_date_home
# #         change = t_key_away if change_away else t_key_home
# #         change_d = f"{change}_d"
# #         st.session_state.update({
# #             change: False,
# #             change_d: None
# #         })
# #         tr = st.session_state.get("team_records", {})
# #         tr.setdefault(game_away_id, {"times_chosen": 0})
# #         tr.setdefault(game_home_id, {"times_chosen": 0})
# #         tc_away: int = tr[game_away_id].get("times_chosen", 0)
# #         tc_home: int = tr[game_home_id].get("times_chosen", 0)
# #         tr[game_away_id].update({
# #             "times_chosen": tc_away + (-1 if change_away else 0)
# #         })
# #         tr[game_home_id].update({
# #             "times_chosen": tc_home + (0 if change_away else -1)
# #         })
# #         st.session_state.update({"team_records": tr})
# #         st.write(f"FIX {change}, {change_away=}, {tc_away=}, {tc_home=}, {tr[game_away_id]['times_chosen']=}, {tr[game_home_id]['times_chosen']=}")
# #
# #     if game_id is not None:
# #         games_chosen[game_round][game_id] = sel_away or sel_home
# #     # if game_away_id is not None:
# #     #     print(f"ADJ {game_away_id} => {int(sel_away)}", end="")
# #     #     team_records[game_away_id]["times_chosen"] += int(sel_away)
# #     # if game_home_id is not None:
# #     #     print(f", ADJ {game_home_id} => {int(sel_home)}", end="")
# #     #     team_records[game_home_id]["times_chosen"] += int(sel_home)
# #     # print(f"")
# #
# #
# # df_top_a: pd.DataFrame = pd.DataFrame()
# # df_top_b: pd.DataFrame = pd.DataFrame()
# # relegation_a: list[int] = []
# # relegation_b: list[int] = []
# # prelim_games_chosen: bool = all(games_chosen[0].values())
# # if prelim_games_chosen:
# #     # all preliminary round games picked
# #     tr = st.session_state.get("team_records", {})
# #     game_ids_first_round: list[int] = [g["game_id"] for g in games if g["round"] == 0]
# #     st.write("teams_by_group")
# #     st.write(teams_by_group)
# #     st.write("teams_by_group[list_groups[0]]")
# #     st.write([t_["id"] for t_ in teams_by_group[list_groups[0]]])
# #     st.write("games[game_id_to_idx[gid]]['away']['id']")
# #     st.write(games[game_id_to_idx[0]]["away"])
# #     tops = {
# #         g: [
# #             {
# #                 "id": t["id"],
# #                 "tc": tr[t["id"]]["times_chosen"],
# #                 "pts": game_points(
# #                     game_id=[
# #                         gid for gid in game_ids_first_round
# #                         if t["id"] in [
# #                             games[game_id_to_idx[gid]]["away"],
# #                             games[game_id_to_idx[gid]]["home"]
# #                         ]
# #                     ],
# #                     team_id=t["id"])
# #             }
# #             for t in teams if t["id"] in [t_["id"] for t_ in teams_by_group[list_groups[i]]]
# #         ]
# #         for i, g in enumerate(list_groups)
# #     }
# #     top_a = tops["A"]
# #     top_b = tops["B"]
# #     top_a.sort(key=lambda t: t["pts"], reverse=True)
# #     top_b.sort(key=lambda t: t["pts"], reverse=True)
# #     lowest_pts_a: int = top_a[-1]["pts"]
# #     lowest_pts_b: int = top_b[-1]["pts"]
# #
# #     relegation_a: list[int] = [t["id"] for t in top_a if t["pts"] == lowest_pts_a]
# #     relegation_b: list[int] = [t["id"] for t in top_b if t["pts"] == lowest_pts_b]
# #
# #     st.write(f"Top {list_groups[0]}")
# #     st.write(top_a)
# #     st.write(f"Top {list_groups[1]}")
# #     st.write(top_b)
# #     df_top_a = pd.DataFrame(top_a)
# #     df_top_b = pd.DataFrame(top_b)
# #     # df_top_a["Team"] = df_top_a.apply(lambda row: Path(flags[row["id"]]).resolve().as_uri(), axis=1)
# #     # df_top_a["Team"] = df_top_a.apply(lambda row: flags[row["id"]], axis=1)
# #     df_top_a["Team"] = df_top_a.apply(lambda row: flags_64[row["id"]], axis=1)
# #     df_top_a["Name"] = df_top_a.apply(lambda row: teams[row["id"]]["name"], axis=1)
# #     # df_top_b["Team"] = df_top_b.apply(lambda row: Path(flags[row["id"]]).resolve().as_uri(), axis=1)
# #     # df_top_b["Team"] = df_top_b.apply(lambda row: flags[row["id"]], axis=1)
# #     df_top_b["Team"] = df_top_b.apply(lambda row: flags_64[row["id"]], axis=1)
# #     df_top_b["Name"] = df_top_b.apply(lambda row: teams[row["id"]]["name"], axis=1)
# #
# #     st.write("relegation_a")
# #     st.write(relegation_a)
# #     st.write("relegation_b")
# #     st.write(relegation_b)
# #
# #     st.write(f"All {rounds[0]} games chosen!")
# #     st.write([f"{t['name']}" for t in teams])
# #     st.write(tr)
# # else:
# #     st.write(f"Still need to select all {rounds[0]} games first")
# #     st.write(games_chosen[0])
# #
# #
# # last_round: Optional[str] = None
# # shown_dates: dict[str: set] = {}
# # shown_groups: dict[str: set] = {}
# #
# # for i, game_data in enumerate(games):
# #     # r_idx = i // cols_per_row
# #     # c_idx = i % cols_per_row
# #     game_id: int = game_data.get("game_id")
# #     game_round: int = game_data.get("round")
# #     round_name: str = rounds[game_round]
# #     game_date_s: str = game_data.get("date")
# #     game_location: str = game_data.get("location")
# #     game_away_code: str = game_data.get("away_code")
# #     game_home_code: str = game_data.get("home_code")
# #     game_away_id: int = game_data.get("away")
# #     game_home_id: int = game_data.get("home")
# #
# #     away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
# #     home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
# #     a_data: dict[str: Any] = {}
# #     h_data: dict[str: Any] = {}
# #     home_name: str = game_home_code
# #     away_name: str = game_away_code
# #     away_group: Optional[str] = None
# #     home_group: Optional[str] = None
# #     away_flag_id: Optional[int] = None
# #     home_flag_id: Optional[int] = None
# #
# #     bg_away: Colour = default_bg_team_col
# #
# #     if away_team_data:
# #         a_data = away_team_data[0]
# #         away_name = a_data.get("name")
# #         away_group = a_data.get("group")
# #         away_flag_id = a_data.get("id")
# #     if home_team_data:
# #         h_data = home_team_data[0]
# #         home_name = h_data.get("name")
# #         home_group = h_data.get("group")
# #         home_flag_id = h_data.get("id")
# #
# #     group: Optional[str] = None
# #     t_key: str = f"{round_name}_title"
# #     g_key_par: str = f"{round_name}_groups_parent"
# #     g_key: str = f"{round_name}_groups"
# #     g_num: int = i - sum([gpr for r, gpr in games_per_round.items() if r < game_round])
# #
# #     if away_group or home_group:
# #         group = "".join(list({away_group, home_group}))
# #     # st.write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}, {group=}, {game_round=}, {round_name=}")
# #     if (last_round is None) or (round_name != last_round):
# #         grid[t_key].write(f"---")
# #         grid[t_key].write(f"{round_name}")
# #         last_round = round_name
# #
# #     st.write(f"{i=}, {g_num=}, {g_key=}, {group=}")
# #     if game_round == 0:
# #         gpr: int = games_per_round[game_round]
# #         shown_groups.setdefault(round_name, set())
# #         if group not in shown_groups[round_name]:
# #             # # grid[g_key][group].write(f"Group {group} - {game_location}")
# #             # # grid[f"{g_key}_{group}"][1 if group == "B" else 0].write(f"Group {group} - {game_location}")
# #             # grid[f"{g_key}_{t_key}_{group}"].write(f"Group {group} - {game_location}")
# #             shown_groups[round_name].add(group)
# #             # for j in range(gpr):
# #             # grid[g_key][group][j].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
# #
# #         t_key_ot = f"toggle_{game_id}_{group}_OT"
# #         t_key_away = f"toggle_{game_id}_{group}_Away"
# #         t_key_home = f"toggle_{game_id}_{group}_Home"
# #         t_key_away_d = f"{t_key_away}_d"
# #         t_key_home_d = f"{t_key_home}_d"
# #
# #         grid[g_key][group][g_num][0].image(flags[away_flag_id], width=flag_w)
# #         grid[g_key][group][None].write("I AM THE NONE")
# #         grid[g_key][group][g_num][0].toggle(
# #             label="toggle",
# #             key=t_key_away,
# #             label_visibility="hidden",
# #             on_change=lambda
# #                 t_=game_away_id,
# #                 r_=game_round,
# #                 g_=group,
# #                 gn_=g_num,
# #                 tka_=t_key_away,
# #                 tkad=t_key_away_d:
# #             select_team(t_, r_, g_, gn_, tka_, tkad)
# #         )
# #
# #         grid[g_key][group][g_num][1].write(f"{group} - {game_date_s}")
# #         grid[g_key][group][g_num][1].toggle(
# #             label="OT / SO",
# #             key=t_key_ot
# #         )
# #
# #         grid[g_key][group][g_num][2].image(flags[home_flag_id], width=flag_w)
# #         grid[g_key][group][g_num][2].toggle(
# #             label="toggle",
# #             key=t_key_home,
# #             label_visibility="hidden",
# #             on_change=lambda
# #                 t_=game_home_id,
# #                 r_=game_round,
# #                 g_=group,
# #                 gn_=g_num,
# #                 tkh_=t_key_home,
# #                 tkhd=t_key_home_d:
# #             select_team(t_, r_, g_, gn_, tkh_, tkhd)
# #         )
# #         print(f"{away_name} => {st.session_state.get(t_key_away)} || {home_name} <= {st.session_state.get(t_key_home)} == {t_key_away=}, {t_key_home=}")
# #
# #         # # grid[g_key][group].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
# #         # # grid[g_key][group].image(flags[away_flag_id])
# #         # # grid[g_key][group].image(flags[home_flag_id])
# #         # grid[f"{g_key}_{group}"][0].image(flags[away_flag_id], width=flag_w)
# #         # grid[f"{g_key}_{group}"][1].write(f"{game_date_s}")
# #         # grid[f"{g_key}_{group}"][2].image(flags[home_flag_id], width=flag_w)
# #         # # grid[f"{g_key_par}"].write("---")
# #         # # grid[g_key][group].write("---")
# #         # grid[f"{g_key}_{t_key}_{group}"].write("---")
# #     else:
# #         # # grid[g_key].write(f"{game_location}")
# #         # # grid[g_key].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
# #         # grid[g_key][0].image(flags[away_flag_id], width=flag_w)
# #         # grid[g_key][1].write(f"{game_date_s}")
# #         # grid[g_key][2].image(flags[away_flag_id], width=flag_w)
# #
# #         if game_round == 1:
# #             if prelim_games_chosen:
# #
# #                 relegation_cols = grid[g_key_par].columns(2)
# #
# #                 # st.dataframe(df_top_a[["Team", "Name", "tc", "pts"]])
# #                 # st.markdown(df_top_a[["Team", "Name", "tc", "pts"]].to_html(), unsafe_allow_html=True)
# #
# #                 # local images dont work in a browser:
# #                 # st.data_editor(
# #                 #     df_top_a[["Team", "Name", "tc", "pts"]],
# #                 #     hide_index=True,
# #                 #     column_config={
# #                 #         "Team": st.column_config.ImageColumn(
# #                 #             "Team",
# #                 #             width="large"
# #                 #         )
# #                 #     },
# #                 #     disabled=True,
# #                 #     key=f"df_top_teams_A"
# #                 # )
# #
# #                 # instead use the base64 embedding approach and a custom html table
# #                 html_table_a: str = create_html_table(
# #                     df_top_a[["Team", "Name", "tc", "pts"]],
# #                     column_config={
# #                         "Team": {
# #                             "config_type": "image",
# #                             "args": {
# #                                 "img_width": "125",
# #                                 "img_height": "125"
# #                             }
# #                         }
# #                     }
# #                 )
# #                 relegation_cols[0].markdown(
# #                     html_table_a,
# #                     unsafe_allow_html=True
# #                 )
# #
# #                 if len(relegation_a) > 1:
# #                     items = [
# #                         {"header": "save", "items": [t["name"] for t in teams if t["id"] in relegation_a]},
# #                         {"header": "relegate", "items": []}
# #                     ]
# #                     with relegation_cols[0]:
# #                         st.write("Please choose a team to relegate:")
# #                         relegation_a_sort = sort_items(
# #                             items,
# #                             key=f"sortable_relegation_a",
# #                             multi_containers=True
# #                         )
# #
# #                     saved_a: list[int] = [t["id"] for t in teams if t["name"] in relegation_a_sort[0]["items"][:-1]]
# #                     if len(relegation_a_sort[0]["items"]) == 0:
# #                         saved_a = [teams[relegation_a_sort[0]["items"][0]]["id"]]
# #                     relegated_a: list[int] = [t["id"] for t in teams if t["name"] in relegation_a_sort[-1]["items"]]
# #                     if not relegated_a:
# #                         relegated_a = [t["id"] for t in teams if t["name"] in relegation_a_sort[0]["items"][-1:]]
# #                         relegation_cols[0].info(f"You must select a team for the relegation game, {' '.join([t['name'] for t in teams if t["id"] in relegated_a])} chosen.")
# #                     if not saved_a:
# #                         saved_a = relegated_a[1:]
# #                         relegated_a = relegated_a[:1]
# #                         relegation_cols[0].info(f"You can only relegate one team, {' '.join([t['name'] for t in teams if t["id"] in saved_a])} saved.")
# #                 else:
# #                     saved_a = []
# #                     relegated_a = relegation_a[-1:]
# #
# #                 html_table_b: str = create_html_table(
# #                     df_top_b[["Team", "Name", "tc", "pts"]],
# #                     column_config={
# #                         "Team": {
# #                             "config_type": "image",
# #                             "args": {
# #                                 "img_width": "125",
# #                                 "img_height": "125"
# #                             }
# #                         }
# #                     }
# #                 )
# #                 relegation_cols[1].markdown(
# #                     html_table_b,
# #                     unsafe_allow_html=True
# #                 )
# #
# #                 if len(relegation_b) > 1:
# #                     items = [
# #                         {"header": "save", "items": [t["name"] for t in teams if t["id"] in relegation_b]},
# #                         {"header": "relegate", "items": []}
# #                     ]
# #                     with relegation_cols[1]:
# #                         st.write("Please choose a team to relegate:")
# #                         relegation_b_sort = sort_items(
# #                             items,
# #                             key=f"sortable_relegation_b",
# #                             multi_containers=True
# #                         )
# #
# #                     saved_b: list[int] = [t["id"] for t in teams if t["name"] in relegation_b_sort[0]["items"][:-1]]
# #                     if len(relegation_b_sort[0]["items"]) == 0:
# #                         saved_b = [teams[relegation_b_sort[0]["items"][0]]["id"]]
# #                     relegated_b: list[int] = [t["id"] for t in teams if t["name"] in relegation_b_sort[-1]["items"]]
# #                     if not relegated_b:
# #                         relegation_cols[1].info(f"You must select a team for the relegation game, {' '.join([t['name'] for t in teams if t["id"] in relegated_b])} chosen.")
# #                         relegated_b = [t["id"] for t in teams if t["name"] in relegation_b_sort[0]["items"][-1:]]
# #                     if not saved_b:
# #                         saved_b = relegated_b[1:]
# #                         relegated_b = relegated_b[:1]
# #                         relegation_cols[1].info(f"You can only relegate one team, {' '.join([t['name'] for t in teams if t["id"] in saved_b])} saved.")
# #                 else:
# #                     saved_b = []
# #                     relegated_b = relegation_b[-1:]
# #
# #                 relegation_cols[0].write("saved_a")
# #                 relegation_cols[0].write(saved_a)
# #                 relegation_cols[0].write("relegated_a")
# #                 relegation_cols[0].write(relegated_a)
# #
# #                 relegation_cols[1].write("saved_b")
# #                 relegation_cols[1].write(saved_b)
# #                 relegation_cols[1].write("relegated_b")
# #                 relegation_cols[1].write(relegated_b)
# #
# #                 if relegated_a:
# #                     away_team_data: list[dict] = [t for t in teams if t["id"] == relegated_a[0]]
# #                     if away_team_data:
# #                         a_data = away_team_data[0]
# #                         away_name = a_data.get("name")
# #                         away_group = a_data.get("group")
# #                         away_flag_id = a_data.get("id")
# #
# #                 if relegated_b:
# #                     home_team_data: list[dict] = [t for t in teams if t["id"] == relegation_b[0]]
# #                     if home_team_data:
# #                         h_data = home_team_data[0]
# #                         home_name = h_data.get("name")
# #                         home_group = h_data.get("group")
# #                         home_flag_id = h_data.get("id")
# #
# #         grid[g_key][g_num][0].image(flags[away_flag_id], width=flag_w)
# #         grid[g_key][g_num][1].write(f"{game_date_s}")
# #         grid[g_key][g_num][2].image(flags[home_flag_id], width=flag_w)
# #
# #     # container = grid[round_name]
# #     # if game_round < 2:
# #     #     container = grid[f"{game_round}_groups"]
# #
# #     # grid.append(st.columns(cols_per_row))
# #     # grid[r_idx][c_idx].write(f"{away_name} VS {home_name}")
# #
# #
# # for i, flag_key in enumerate(flags):
# #     if flag_key:
# #         flag_path: str = flags[flag_key]
# #         flag_path: str = os.path.basename(flag_path)
# #         if flag_path in image_refs_htmls:
# #             html_ = image_refs_htmls[flag_path]
# #             st.markdown(html_, unsafe_allow_html=True)
# #         else:
# #             st.write(f"skip {flag_path=}")
# #
# # # for i, html_ in enumerate([
# # #     """<a target="_blank" href="https://icons8.com/icon/37274/kazakhstan">Kazakhstan</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>"""
# # # ]):
# # #     st.markdown(html_, unsafe_allow_html=True)
# #
# #
# #
# # # import json
# # # import os.path
# # # from typing import Any, Optional
# # # from icons_8_refs import image_refs_htmls
# # #
# # # import streamlit as st
# # #
# # #
# # # @st.cache_data(show_spinner=True)
# # # def load_data_file():
# # #     with open(r"./wjc_2025.json", "r") as f:
# # #         return json.load(f)
# # #
# # #
# # # @st.cache_data(show_spinner=True)
# # # def load_flags():
# # #     pictures = os.listdir(root_image_folder)
# # #     flags = {}
# # #     for i, team_data in enumerate(teams):
# # #         team_id: int = team_data.get("id")
# # #         name_long: str = team_data.get("name_long")
# # #         name: str = team_data.get("name")
# # #         n: str = name_long.lower()
# # #         match n:
# # #             case "united states of america": n = "usa"
# # #             case "czechia": n = "czech-republic"
# # #             case _: pass
# # #         j: int = 0
# # #         found: bool = False
# # #         for j, picture in enumerate(pictures):
# # #             p: str = picture.lower().replace("icons8-", "").replace("-flag-96", "").replace("-96.png", ".png").strip()
# # #             print(f"\t{p=}, {n=}")
# # #             if picture.endswith(".png") and (n in p):
# # #                 flags[i] = os.path.join(root_image_folder, picture)
# # #                 found = True
# # #                 break
# # #         if found:
# # #             pictures.pop(j)
# # #         else:
# # #             print(f"No image found for '{n}'")
# # #
# # #     flags[None] = os.path.join(root_image_folder, "unknown_flag.png")
# # #
# # #     return flags
# # #
# # #
# # # root_image_folder = r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags"
# # # if not os.path.exists(root_image_folder):
# # #     root_image_folder = r"C:\Users\abrig\Documents\Coding_Practice\Coding_Practice\Resources\Flags"
# # #
# # #
# # # initial_data: dict[str: Any] = load_data_file()
# # # teams: list[dict] = initial_data["teams"]
# # # rounds: list[str] = initial_data["rounds"]
# # # games: list[dict] = initial_data["schedule"]["games"]
# # # games_per_round: dict[int: int] = {}
# # # flags = load_flags()
# # # flag_w, flag_h = 100, 50
# # # list_groups = ["A", "B"]
# # #
# # # st.write(flags)
# # # st.json(initial_data)
# # #
# # # cols_per_row: int = 2
# # #
# # # for i, g in enumerate(games):
# # #     rnd: int = g["round"]
# # #     if rnd not in games_per_round:
# # #         games_per_round[rnd] = 0
# # #     games_per_round[rnd] += 1
# # #
# # # n_rows = int(round(len(games) / cols_per_row))
# # # grid = {
# # #     "title": st.container()
# # # }
# # # # grid.update({rnd: st.container() for rnd in rounds})
# # # for i, rnd in enumerate(rounds):
# # #     t_key: str = f"{rnd}_title"
# # #     g_key_par: str = f"{rnd}_groups_parent"
# # #     g_key: str = f"{rnd}_groups"
# # #     if i == 0:
# # #         grid[t_key] = st.container()
# # #         # grid[g_key_par] = st.container()
# # #         grid[g_key] = dict(zip(list_groups, [{}, {}]))
# # #         for j, group in enumerate(list_groups):
# # #             for k in range(games_per_round[i]):
# # #                 grid[g_key][group][None] = st.container()
# # #                 grid[g_key][group][k] = st.columns([0.4, 0.2, 0.4])
# # #
# # #         # grid[g_key_par] = st.container()
# # #         # grid[g_key] = dict(zip(["A", "B"], grid[g_key_par].columns(2)))
# # #         # # grid[g_key] = {}
# # #         # grid[f"{g_key}_{t_key}_A"] = grid[g_key]["A"].container()
# # #         # grid[f"{g_key}_{t_key}_B"] = grid[g_key]["B"].container()
# # #         # grid[f"{g_key}_A"] = grid[g_key]["A"].columns([0.4, 0.2, 0.4])
# # #         # grid[f"{g_key}_B"] = grid[g_key]["B"].columns([0.4, 0.2, 0.4])
# # #     else:
# # #         grid[t_key] = st.container()
# # #         grid[g_key] = {}
# # #         # grid[g_key] = st.container()
# # #         # grid[g_key] = st.columns([0.4, 0.2, 0.4])
# # #         for j in range(games_per_round[i]):
# # #             # jk: int = j + sum([gpr for r, gpr in games_per_round.items() if r < i])
# # #             jk = j
# # #             grid[g_key][None] = st.container()
# # #             grid[g_key][jk] = st.columns([0.4, 0.2, 0.4])
# # #
# # # st.write(list(grid.keys()))
# # # st.write(grid)
# # #
# # # last_round: Optional[str] = None
# # # shown_dates: dict[str: set] = {}
# # # shown_groups: dict[str: set] = {}
# # #
# # # for i, game_data in enumerate(games):
# # #     r_idx = i // cols_per_row
# # #     c_idx = i % cols_per_row
# # #     game_id: int = game_data.get("game_id")
# # #     game_round: int = game_data.get("round")
# # #     round_name: str = rounds[game_round]
# # #     game_date_s: str = game_data.get("date")
# # #     game_location: str = game_data.get("location")
# # #     game_away_code: str = game_data.get("away_code")
# # #     game_home_code: str = game_data.get("home_code")
# # #     game_away_id: int = game_data.get("away")
# # #     game_home_id: int = game_data.get("home")
# # #
# # #     away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
# # #     home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
# # #     a_data: dict[str: Any] = {}
# # #     h_data: dict[str: Any] = {}
# # #     home_name: str = game_home_code
# # #     away_name: str = game_away_code
# # #     away_group: Optional[str] = None
# # #     home_group: Optional[str] = None
# # #     away_flag_id: Optional[int] = None
# # #     home_flag_id: Optional[int] = None
# # #     if away_team_data:
# # #         a_data = away_team_data[0]
# # #         away_name = a_data.get("name")
# # #         away_group = a_data.get("group")
# # #         away_flag_id = a_data.get("id")
# # #     if home_team_data:
# # #         h_data = home_team_data[0]
# # #         home_name = h_data.get("name")
# # #         home_group = h_data.get("group")
# # #         home_flag_id = h_data.get("id")
# # #
# # #     group: Optional[str] = None
# # #     t_key: str = f"{round_name}_title"
# # #     g_key_par: str = f"{round_name}_groups_parent"
# # #     g_key: str = f"{round_name}_groups"
# # #     g_num: int = i - sum([gpr for r, gpr in games_per_round.items() if r < game_round])
# # #
# # #     if away_group or home_group:
# # #         group = "".join(list({away_group, home_group}))
# # #     # st.write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}, {group=}, {game_round=}, {round_name=}")
# # #     if (last_round is None) or (round_name != last_round):
# # #         grid[t_key].write(f"---")
# # #         grid[t_key].write(f"{round_name}")
# # #         last_round = round_name
# # #
# # #     st.write(f"{i=}, {g_num=}, {g_key=}, {group=}")
# # #     if game_round == 0:
# # #         gpr: int = games_per_round[game_round]
# # #         shown_groups.setdefault(round_name, set())
# # #         if group not in shown_groups[round_name]:
# # #             # # grid[g_key][group].write(f"Group {group} - {game_location}")
# # #             # # grid[f"{g_key}_{group}"][1 if group == "B" else 0].write(f"Group {group} - {game_location}")
# # #             # grid[f"{g_key}_{t_key}_{group}"].write(f"Group {group} - {game_location}")
# # #             shown_groups[round_name].add(group)
# # #             # for j in range(gpr):
# # #             # grid[g_key][group][j].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
# # #         grid[g_key][group][g_num][0].image(flags[away_flag_id], width=flag_w)
# # #         grid[g_key][group][g_num][1].write(f"{group} - {game_date_s}")
# # #         grid[g_key][group][g_num][2].image(flags[home_flag_id], width=flag_w)
# # #
# # #         # # grid[g_key][group].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
# # #         # # grid[g_key][group].image(flags[away_flag_id])
# # #         # # grid[g_key][group].image(flags[home_flag_id])
# # #         # grid[f"{g_key}_{group}"][0].image(flags[away_flag_id], width=flag_w)
# # #         # grid[f"{g_key}_{group}"][1].write(f"{game_date_s}")
# # #         # grid[f"{g_key}_{group}"][2].image(flags[home_flag_id], width=flag_w)
# # #         # # grid[f"{g_key_par}"].write("---")
# # #         # # grid[g_key][group].write("---")
# # #         # grid[f"{g_key}_{t_key}_{group}"].write("---")
# # #     else:
# # #         # # grid[g_key].write(f"{game_location}")
# # #         # # grid[g_key].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
# # #         # grid[g_key][0].image(flags[away_flag_id], width=flag_w)
# # #         # grid[g_key][1].write(f"{game_date_s}")
# # #         # grid[g_key][2].image(flags[away_flag_id], width=flag_w)
# # #         grid[g_key][g_num][0].image(flags[away_flag_id], width=flag_w)
# # #         grid[g_key][g_num][1].write(f"{game_date_s}")
# # #         grid[g_key][g_num][2].image(flags[home_flag_id], width=flag_w)
# # #
# # #     # container = grid[round_name]
# # #     # if game_round < 2:
# # #     #     container = grid[f"{game_round}_groups"]
# # #
# # #     # grid.append(st.columns(cols_per_row))
# # #     # grid[r_idx][c_idx].write(f"{away_name} VS {home_name}")
# # #
# # #
# # # for i, flag_key in enumerate(flags):
# # #     if flag_key:
# # #         flag_path: str = flags[flag_key]
# # #         flag_path: str = os.path.basename(flag_path)
# # #         if flag_path in image_refs_htmls:
# # #             html_ = image_refs_htmls[flag_path]
# # #             st.markdown(html_, unsafe_allow_html=True)
# # #         else:
# # #             st.write(f"skip {flag_path=}")
# # #
# # # # for i, html_ in enumerate([
# # # #     """<a target="_blank" href="https://icons8.com/icon/37274/kazakhstan">Kazakhstan</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>"""
# # # # ]):
# # # #     st.markdown(html_, unsafe_allow_html=True)

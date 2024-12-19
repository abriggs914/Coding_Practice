import json
import os.path
from typing import Any, Optional
from icons_8_refs import image_refs_htmls

import streamlit as st


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


root_image_folder = r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags"
if not os.path.exists(root_image_folder):
    root_image_folder = r"C:\Users\abrig\Documents\Coding_Practice\Coding_Practice\Resources\Flags"


initial_data: dict[str: Any] = load_data_file()
teams: list[dict] = initial_data["teams"]
rounds: list[str] = initial_data["rounds"]
games: list[dict] = initial_data["schedule"]["games"]
games_per_round: dict[int: int] = {}
flags = load_flags()
flag_w, flag_h = 100, 50
list_groups = ["A", "B"]

st.write(flags)
st.json(initial_data)

cols_per_row: int = 2

for i, g in enumerate(games):
    rnd: int = g["round"]
    if rnd not in games_per_round:
        games_per_round[rnd] = 0
    games_per_round[rnd] += 1

n_rows = int(round(len(games) / cols_per_row))
grid = {
    "title": st.container()
}
# grid.update({rnd: st.container() for rnd in rounds})
for i, rnd in enumerate(rounds):
    t_key: str = f"{rnd}_title"
    g_key_par: str = f"{rnd}_groups_parent"
    g_key: str = f"{rnd}_groups"
    if i == 0:
        grid[t_key] = st.container()
        # grid[g_key_par] = st.container()
        grid[g_key] = dict(zip(list_groups, [{}, {}]))
        for j, group in enumerate(list_groups):
            for k in range(games_per_round[i]):
                grid[g_key][group][None] = st.container()
                grid[g_key][group][k] = st.columns([0.4, 0.2, 0.4])

        # grid[g_key_par] = st.container()
        # grid[g_key] = dict(zip(["A", "B"], grid[g_key_par].columns(2)))
        # # grid[g_key] = {}
        # grid[f"{g_key}_{t_key}_A"] = grid[g_key]["A"].container()
        # grid[f"{g_key}_{t_key}_B"] = grid[g_key]["B"].container()
        # grid[f"{g_key}_A"] = grid[g_key]["A"].columns([0.4, 0.2, 0.4])
        # grid[f"{g_key}_B"] = grid[g_key]["B"].columns([0.4, 0.2, 0.4])
    else:
        grid[t_key] = st.container()
        grid[g_key] = {}
        # grid[g_key] = st.container()
        # grid[g_key] = st.columns([0.4, 0.2, 0.4])
        for j in range(games_per_round[i]):
            # jk: int = j + sum([gpr for r, gpr in games_per_round.items() if r < i])
            jk = j
            grid[g_key][None] = st.container()
            grid[g_key][jk] = st.columns([0.4, 0.2, 0.4])

st.write(list(grid.keys()))
st.write(grid)

last_round: Optional[str] = None
shown_dates: dict[str: set] = {}
shown_groups: dict[str: set] = {}

for i, game_data in enumerate(games):
    r_idx = i // cols_per_row
    c_idx = i % cols_per_row
    game_id: int = game_data.get("game_id")
    game_round: int = game_data.get("round")
    round_name: str = rounds[game_round]
    game_date_s: str = game_data.get("date")
    game_location: str = game_data.get("location")
    game_away_code: str = game_data.get("away_code")
    game_home_code: str = game_data.get("home_code")
    game_away_id: int = game_data.get("away")
    game_home_id: int = game_data.get("home")

    away_team_data: list[dict] = [t for t in teams if t["id"] == game_away_id]
    home_team_data: list[dict] = [t for t in teams if t["id"] == game_home_id]
    a_data: dict[str: Any] = {}
    h_data: dict[str: Any] = {}
    home_name: str = game_home_code
    away_name: str = game_away_code
    away_group: Optional[str] = None
    home_group: Optional[str] = None
    away_flag_id: Optional[int] = None
    home_flag_id: Optional[int] = None
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

    group: Optional[str] = None
    t_key: str = f"{round_name}_title"
    g_key_par: str = f"{round_name}_groups_parent"
    g_key: str = f"{round_name}_groups"
    g_num: int = i - sum([gpr for r, gpr in games_per_round.items() if r < game_round])

    if away_group or home_group:
        group = "".join(list({away_group, home_group}))
    # st.write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}, {group=}, {game_round=}, {round_name=}")
    if (last_round is None) or (round_name != last_round):
        grid[t_key].write(f"---")
        grid[t_key].write(f"{round_name}")
        last_round = round_name

    st.write(f"{i=}, {g_num=}, {g_key=}")
    if game_round == 0:
        gpr: int = games_per_round[game_round]
        shown_groups.setdefault(round_name, set())
        if group not in shown_groups[round_name]:
            # # grid[g_key][group].write(f"Group {group} - {game_location}")
            # # grid[f"{g_key}_{group}"][1 if group == "B" else 0].write(f"Group {group} - {game_location}")
            # grid[f"{g_key}_{t_key}_{group}"].write(f"Group {group} - {game_location}")
            shown_groups[round_name].add(group)
            # for j in range(gpr):
            # grid[g_key][group][j].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
        grid[g_key][group][g_num][0].image(flags[away_flag_id], width=flag_w)
        grid[g_key][group][g_num][1].write(f"{game_date_s}")
        grid[g_key][group][g_num][2].image(flags[home_flag_id], width=flag_w)

        # # grid[g_key][group].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
        # # grid[g_key][group].image(flags[away_flag_id])
        # # grid[g_key][group].image(flags[home_flag_id])
        # grid[f"{g_key}_{group}"][0].image(flags[away_flag_id], width=flag_w)
        # grid[f"{g_key}_{group}"][1].write(f"{game_date_s}")
        # grid[f"{g_key}_{group}"][2].image(flags[home_flag_id], width=flag_w)
        # # grid[f"{g_key_par}"].write("---")
        # # grid[g_key][group].write("---")
        # grid[f"{g_key}_{t_key}_{group}"].write("---")
    else:
        # # grid[g_key].write(f"{game_location}")
        # # grid[g_key].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
        # grid[g_key][0].image(flags[away_flag_id], width=flag_w)
        # grid[g_key][1].write(f"{game_date_s}")
        # grid[g_key][2].image(flags[away_flag_id], width=flag_w)
        grid[g_key][g_num][0].image(flags[away_flag_id], width=flag_w)
        grid[g_key][g_num][1].write(f"{game_date_s}")
        grid[g_key][g_num][2].image(flags[home_flag_id], width=flag_w)

    # container = grid[round_name]
    # if game_round < 2:
    #     container = grid[f"{game_round}_groups"]

    # grid.append(st.columns(cols_per_row))
    # grid[r_idx][c_idx].write(f"{away_name} VS {home_name}")


for i, flag_key in enumerate(flags):
    if flag_key:
        flag_path: str = flags[flag_key]
        flag_path: str = os.path.basename(flag_path)
        if flag_path in image_refs_htmls:
            html_ = image_refs_htmls[flag_path]
            st.markdown(html_, unsafe_allow_html=True)
        else:
            st.write(f"skip {flag_path=}")

# for i, html_ in enumerate([
#     """<a target="_blank" href="https://icons8.com/icon/37274/kazakhstan">Kazakhstan</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>"""
# ]):
#     st.markdown(html_, unsafe_allow_html=True)

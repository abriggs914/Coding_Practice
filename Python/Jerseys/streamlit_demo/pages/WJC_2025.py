import json
from typing import Any, Optional

import streamlit as st


@st.cache_data(show_spinner=True)
def load_data_file():
    with open(r"./wjc_2025.json", "r") as f:
        return json.load(f)


initial_data: dict[str: Any] = load_data_file()
teams: list[dict] = initial_data["teams"]
rounds: list[str] = initial_data["rounds"]
games: list[dict] = initial_data["schedule"]["games"]

st.json(initial_data)

cols_per_row: int = 2

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
        grid[g_key_par] = st.container()
        grid[g_key] = dict(zip(["A", "B"], grid[g_key_par].columns(2)))
    else:
        grid[t_key] = st.container()
        grid[g_key] = st.container()

st.write(list(grid.keys()))

last_round: Optional[str] = None
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
    if away_team_data:
        a_data = away_team_data[0]
        away_name = a_data.get("name")
        away_group = a_data.get("group")
    if home_team_data:
        h_data = home_team_data[0]
        home_name = h_data.get("name")
        home_group = h_data.get("group")

    group: Optional[str] = None
    t_key: str = f"{round_name}_title"
    g_key_par: str = f"{round_name}_groups_parent"
    g_key: str = f"{round_name}_groups"

    if away_group or home_group:
        group = "".join(list({away_group, home_group}))
    # st.write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}, {group=}, {game_round=}, {round_name=}")
    if (last_round is None) or (round_name != last_round):
        grid[t_key].write(f"{round_name}")
        last_round = round_name
    if game_round == 0:
        shown_groups.setdefault(round_name, set())
        if group not in shown_groups[round_name]:
            grid[g_key][group].write(f"Group {group} - {game_location}")
            shown_groups[round_name].add(group)
        grid[g_key][group].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")
    else:
        grid[g_key].write(f"{game_location}")
        grid[g_key].write(f"{away_name} VS {home_name}, {home_group=}, {away_group=}")

    # container = grid[round_name]
    # if game_round < 2:
    #     container = grid[f"{game_round}_groups"]

    # grid.append(st.columns(cols_per_row))
    # grid[r_idx][c_idx].write(f"{away_name} VS {home_name}")

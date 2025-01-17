import datetime
import random
from copy import copy, deepcopy

import streamlit as st
from streamlit_autorefresh import st_autorefresh

n_rows: int = 10
n_cols: int = 10

sym_ship: str = "B"
sym_hit: str = ":large_green_circle:"  # "H"
sym_miss: str = ":red_circle:"  # "M"
sym_empty: str = " "
sym_my_turn: str = ":arrow_backward:"
sym_pc_turn: str = ":arrow_forward:"


def new_empty_grid():
    return [[sym_empty for j in range(n_cols)] for i in range(n_rows)]


def gen_random_grid(ships_to_make=(5, 4, 3, 2, 2, 1)) -> tuple[list, list]:
    tg = [[sym_empty for j in range(n_cols)] for i in range(n_rows)]
    ships = []

    max_tries = 2 ** 20

    # for ls in [5, 4, 3, 2, 2, 1]:
    for bn, ls in enumerate(ships_to_make):

        try_place = True

        while try_place:
            try_place = False
            r_i0 = random.choice(range(n_rows))
            r_j0 = random.choice(range(n_cols))
            r_dir = random.choice(["u", "r", "d", "l"])

            di = 1 if r_dir == "d" else (-1 if r_dir == "u" else 0)
            dj = 1 if r_dir == "r" else (-1 if r_dir == "l" else 0)
            idxs = []

            if not (-1 < r_i0 + (ls * di) < n_rows):
                # too close to edge
                try_place = True

            if not (-1 < r_j0 + (ls * dj) < n_cols):
                # too close to edge
                try_place = True

            if not try_place:
                if r_dir in ("u", "d"):
                    for i in range(r_i0, r_i0 + (ls * di), di):
                        if tg[i][r_j0] != sym_empty:
                            # occupied space, or would cross.
                            try_place = True
                        else:
                            idxs.append((i, r_j0))
                else:
                    for j in range(r_j0, r_j0 + (ls * dj), dj):
                        if tg[r_i0][j] != sym_empty:
                            # occupied space, or would cross.
                            try_place = True
                        else:
                            idxs.append((r_i0, j))

            # print(f"Tried {ls=}, {r_i0=}, {r_j0=}, {r_dir=}, {di=}, {dj=}, {try_place=}")
            if not try_place:
                # print(f"=> {idxs=}")
                for i, j in idxs:
                    tg[i][j] = f"{sym_ship}{ls}"
                ships.append(idxs)
            
            max_tries -= 1
            if max_tries <= 0:
                raise ValueError(f"Could not place ships.")
    print(f"{ships=}")
    return tg, ships


def reset_game():
    for k in [
        "playing",
        "turn_number",
        "first_turn_user",
        "my_grid_ans",
        "my_grid_ans_ships",
        "pc_grid_ans",
        "pc_grid_ans_ships",
        "my_grid_guesses",
        "pc_grid_guesses"
    ]:
        st.session_state.pop(k)


def click_cell(i, j, guesser: str = "me"):
    
    guesser = guesser.lower()
    guesser = "my" if guesser == "me" else guesser
    
    ga = my_grid_ans if guesser == "pc" else pc_grid_ans
    gg = pc_grid_guesses if guesser == "pc" else my_grid_guesses
    sh = my_grid_ans_ships if guesser == "pc" else pc_grid_ans_ships
    
    act = ga[i][j]
    hit = act.startswith(sym_ship)
    print(f"{i=}, {j=}, {act=}, {hit=}")
    gg[i][j] = sym_hit if hit else sym_miss
    st.session_state.update({
        f"{guesser}_grid_guesses": gg,
        "turn_number": turn_number + 1
    })
    
    for k, lst_ship_idxs in enumerate(sh):
        if (i, j) in lst_ship_idxs:
            lst_ship_idxs.remove((i, j))
        if not lst_ship_idxs:
            if guesser == "pc":
                toast_msg = f"The computer sank your ship!"
            else:
                toast_msg = f"You successfully sank a pc ship!"
            st.toast(toast_msg)
            
    if not any(sh):
        if guesser == "pc":
            toast_msg = "The computer sank all of your battleships, You Lose."
        else:
            toast_msg = "You sank all he computer's battleships, You Win!"
        st.toast(toast_msg)
        st.session_state.update({"playing": "game over"})
                
    if guesser == "pc":
        interval = 500
    else:
        interval = 100
    
    st.rerun()
    
    #st_autorefresh(
    #    interval=interval,
    #    limit=1,
    #    key=f"auto_refresh_{datetime.datetime.now():%Y_%m_%d_%H_%M_%S_%f}",
    #    debounce=False
    #)


st.set_page_config(layout="wide")

row_controls = st.container(border=1)
game_container = st.container(border=1)

my_grid_ans = st.session_state.setdefault("my_grid_ans", new_empty_grid())
my_grid_ans_ships = st.session_state.setdefault("my_grid_ans_ships", [])
pc_grid_ans = st.session_state.setdefault("pc_grid_ans", new_empty_grid())
pc_grid_ans_ships = st.session_state.setdefault("pc_grid_ans_ships", [])
my_grid_guesses = st.session_state.setdefault("my_grid_guesses", new_empty_grid())
pc_grid_guesses = st.session_state.setdefault("pc_grid_guesses", new_empty_grid())
playing = st.session_state.setdefault("playing", "idle") == "playing"

# my_grid = st.session_state.setdefault("my_grid", [[sym_empty for j in range(n_cols)] for i in range(n_rows)])
# pc_grid = st.session_state.setdefault("pc_grid", [[sym_empty for j in range(n_cols)] for i in range(n_rows)])


first_turn_user = st.session_state.setdefault("first_turn_user", random.choice([0, 1]))
turn_number = st.session_state.setdefault("turn_number", 0)
user_turn = (turn_number % 2) != first_turn_user
sym_turn = sym_my_turn if user_turn else sym_pc_turn

if not my_grid_ans_ships:
    with row_controls:
        if st.button("random grid", key="btn_random_grid"):
            my_grid_ans, my_grid_ans_ships = gen_random_grid()

            st.button(
                label="save grid",
                key=f"btn_save_grid",
                on_click=lambda: st.session_state.update({
                    "my_grid_ans": my_grid_ans,
                    "my_grid_ans_ships": my_grid_ans_ships
                })
            )
else:
    with row_controls:
        if not playing:
            if st.button("start game", key="btn_start_game"):
                pc_grid_ans, pc_grid_ans_ships = gen_random_grid()
                st.session_state.update({
                    "pc_grid_ans": pc_grid_ans,
                    "pc_grid_ans_ships": pc_grid_ans_ships,
                    "my_grid_guesses": new_empty_grid(),
                    "pc_grid_guesses": new_empty_grid(),
                    "playing": "playing"
                })
                st.rerun()

            if st.button("new game", key="btn_new_game"):
                reset_game()
                st.rerun()
        else:
            if st.button("quit"):
                reset_game()
                st.rerun()

            # play game turn
            if user_turn:
                st.write("It's your turn!")
            else:
                st.write("It's the computer's turn")
                ri = random.choice(range(n_rows))
                rj = random.choice(range(n_cols))
                
                while pc_grid_guesses[ri][rj] != sym_empty:                
                    ri = random.choice(range(n_rows))
                    rj = random.choice(range(n_cols))
                    st.write(f"{ri=}, {rj=}")
                    
                click_cell(ri, rj, guesser="pc")
            st.write(f"Game State: {st.session_state.get('playing').title()}")

# Render the game grids

w_space_cell = 100 / 10
w_cell = (100 - w_space_cell) / (2 * n_cols)

cols_control = game_container.columns([(100 - w_space_cell) / 2, w_space_cell, (100 - w_space_cell) / 2], border=1)

game_grid = [
    game_container.columns(
        [w_cell for j in range(n_cols + 1)]
        + [w_space_cell]
        + [w_cell for j in range(n_cols + 1)]
        , border=1
    ) for i in range(n_rows + 1)
]
# my_game_grid = game_grid[:n_cols + 1]
my_game_grid = [row[:n_cols + 1] for row in game_grid]

if playing:
    cols_control[1].write(sym_turn)
    game_grid[0][n_cols + 1].write(turn_number)

cols_control[0].subheader("My Grid")

for i in range(1, n_rows + 1):
    my_game_grid[i][0].write(f"{i}")

for j in range(1, n_cols + 1):
    my_game_grid[0][j].write(f"{chr(64 + j)}")

for i in range(n_rows):
    for j in range(n_cols):
        act = pc_grid_guesses[i][j]
        sym = my_grid_ans[i][j]
        if act != sym_empty:
            sym = act
        my_game_grid[i + 1][j + 1].write(sym)
    # my_game_grid[i + 1][j + 1].write(pc_grid_guesses[i][j])

cols_control[2].subheader("PC Grid")
# pc_game_grid = [game_container.columns(n_cols + 1, border=1) for i in range(n_rows + 1)]
# pc_game_grid = game_grid[n_cols + 2:]
pc_game_grid = [row[n_cols + 2:] for row in game_grid]

for i in range(1, n_rows + 1):
    pc_game_grid[i][0].write(f"{i}")

for j in range(1, n_cols + 1):
    pc_game_grid[0][j].write(f"{chr(64 + j)}")

for i in range(n_rows):
    for j in range(n_cols):
        # pc_game_grid[i + 1][j + 1].write(pc_grid_ans[i][j])
        # act = pc_grid_ans[i][j]
        sym = my_grid_guesses[i][j]
        # print(f"{i=}, {j=}, {sym=}")
        if playing and (sym == sym_empty):
            sym = f"{chr(64 + 1 + j)}{i + 1}"
            pc_game_grid[i + 1][j + 1].button(
                label=sym,
                key=f"btn_pc_grid_{i}_{j}",
                type="tertiary",
                on_click=lambda i_=i, j_=j: click_cell(i_, j_),
                disabled=not user_turn
            )
        else:
            pc_game_grid[i + 1][j + 1].write(sym)

# st.write(my_grid_guesses)
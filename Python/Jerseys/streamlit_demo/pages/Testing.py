import random
from copy import copy, deepcopy

import streamlit as st


n_rows: int = 10
n_cols: int = 10

sym_ship: str = "B"
sym_hit: str = ":large_green_circle:"  # "H"
sym_miss: str = ":red_circle:"  # "M"
sym_empty: str = " "


def new_empty_grid():
	return [[sym_empty for j in range(n_cols)] for i in range(n_rows)]


def gen_random_grid(ships_to_make=(5, 4, 3, 2, 2, 1)) -> tuple[list, list]:
	tg = [[sym_empty for j in range(n_cols)] for i in range(n_rows)]
	ships = []

	max_tries = 2**20

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


def click_cell(i, j):
	act = pc_grid_ans[i][j]
	hit = act.startswith(sym_ship)
	print(f"{i=}, {j=}, {act=}, {hit=}")
	my_grid_guesses[i][j] = sym_hit if hit else sym_miss
	st.session_state.update({"my_grid_guesses": my_grid_guesses})


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

			if st.button("new game", key="btn_new_game"):
				reset_game()
				st.rerun()
		else:
			if st.button("quit"):
				reset_game()
				st.rerun()

			# play game turn
			first_turn_user = st.session_state.setdefault("first_turn_user", random.choice([0, 1]))
			turn_number = st.session_state.setdefault("turn_number", 0)
			user_turn = (turn_number % 2) != first_turn_user


game_container.subheader("My Grid")
my_game_grid = [game_container.columns(n_cols + 1, border=1) for i in range(n_rows + 1)]

for i in range(1, n_rows + 1):
	my_game_grid[i][0].write(f"{i}")

for j in range(1, n_cols + 1):
	my_game_grid[0][j].write(f"{chr(64 + j)}")

for i in range(n_rows):
	for j in range(n_cols):
		my_game_grid[i + 1][j + 1].write(my_grid_ans[i][j])
		# my_game_grid[i + 1][j + 1].write(pc_grid_guesses[i][j])


game_container.subheader("PC Grid")
pc_game_grid = [game_container.columns(n_cols + 1, border=1) for i in range(n_rows + 1)]

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
		if sym == sym_empty:
			sym = f"{chr(64 + 1 + j)}{i + 1}"
			pc_game_grid[i + 1][j + 1].button(
				label=sym,
				key=f"btn_pc_grid_{i}_{j}",
				type="tertiary",
				on_click=lambda i_=i, j_=j: click_cell(i_, j_)
			)
		else:
			pc_game_grid[i + 1][j + 1].write(sym)

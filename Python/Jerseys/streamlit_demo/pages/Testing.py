import random

import streamlit as st


n_rows: int = 10
n_cols: int = 10

sym_ship: str = "B"
sym_hit: str = "H"
sym_miss: str = "M"
sym_empty: str = " "


def gen_random_grid() -> list[list[str]]:
	tg = [[sym_empty for j in range(n_cols)] for i in range(n_rows)]

	# for ls in [5, 4, 3, 2, 2, 1]:
	for bn, ls in enumerate([5, 4, 3, 2, 2, 1]):

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
						if tg[i][dj] != sym_empty:
							# occupied space, or would cross.
							try_place = True
						else:
							idxs.append((i, r_j0))
				else:
					for j in range(r_j0, r_j0 + (ls * dj), dj):
						if tg[di][j] != sym_empty:
							# occupied space, or would cross.
							try_place = True
						else:
							idxs.append((r_i0, j))

			print(f"Tried {ls=}, {r_i0=}, {r_j0=}, {r_dir=}, {di=}, {dj=}, {try_place=}")
			if not try_place:
				print(f"=> {idxs=}")
				for i, j in idxs:
					tg[i][j] = f"{sym_ship}{ls}"

	return tg


st.set_page_config(layout="wide")

row_controls = st.container(border=1)
game_container = st.container(border=1)
game_container.subheader("My Grid")
my_game_grid = [game_container.columns(n_cols + 1, border=1) for i in range(n_rows + 1)]

my_grid_ans = st.session_state.get("my_grid_ans")

my_grid = st.session_state.setdefault("my_grid", [[sym_empty for j in range(n_cols)] for i in range(n_rows)])
pc_grid = st.session_state.setdefault("pc_grid", [[sym_empty for j in range(n_cols)] for i in range(n_rows)])

if not my_grid_ans:
	my_grid_ans = [[sym_empty for j in range(n_cols)] for i in range(n_rows)]

	with row_controls:
		if st.button("random grid", key="btn_random_grid"):
			my_grid_ans = gen_random_grid()

	for i in range(1, n_rows + 1):
		my_game_grid[i][0].write(f"{i}")

	for j in range(1, n_cols + 1):
		my_game_grid[0][j].write(f"{chr(64 + j)}")

	for i in range(n_rows):
		for j in range(n_cols):
			my_game_grid[i + 1][j + 1].write(my_grid_ans[i][j])

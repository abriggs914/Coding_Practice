
import os
import math
from utility import *


clear = lambda: os.system('cls')  # on Windows System


N_ROWS = 42
N_COLS = 85

def new_grid():
	return [[" " for j in range(N_COLS)] for i in range(N_ROWS)]
blank_grid = new_grid()
grid_str = lambda grid: "\n".join(list(map(str, ["".join([str(col) for col in row]) for row in grid])))
blank_grid_str = grid_str(blank_grid)
# print(blank_grid_str)
	
num_waves = int(input("How many waves?\n\t").strip())

t = (num_waves * 2 * math.pi) / N_COLS
it = round(1 / t)
a = N_ROWS / 2

it = 1

cos_points = []
sin_points = []
for i in range(0, num_waves * 360, it):
	cos_v = cos_x(i, period=t, amplitude=a)
	sin_v = sin_x(i, period=t, amplitude=a)
	# print("i / it:", i / it, "cos_x:", cos_v, "sin_x:", sin_v)
	cos_points.append((int(round(cos_v)), min(N_COLS - 1, int(round(i / it)))))
	sin_points.append((int(round(sin_v)), min(N_COLS - 1, int(round(i / it)))))
# print("t:", t, "a:", a, "1 / t:", it)

cos_grid = new_grid()
for pt in cos_points:
	r, c = pt
	if c == N_COLS - 1:
		continue
	# print("pt:", pt)
	cos_grid[r][c] = "#"
print("\n\n\tCosine graph:\n\n", grid_str(cos_grid))

sin_grid = new_grid()
for pt in sin_points:
	r, c = pt
	if c == N_COLS - 1:
		continue
	# print("pt:", pt)
	sin_grid[r][c] = "#"
print("\n\n\tSine graph:\n\n", grid_str(sin_grid))
	
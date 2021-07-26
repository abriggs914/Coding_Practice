import random
from battleship import Battleship

from utility import *
import numpy as np
from copy import copy


class BattleshipGrid:

    SYM_HIT = "HIT"
    SYM_MISS = "MIS"
    SYM_SHIP = "SHP"
    SYM_BLANK = "BLK"

    def __init__(self, n, m, random_ship_lengths=None, rnd_shp_max_size=False, ships=None):
        self.random_ship_lengths = [1, 2, 3, 4, 5]
        self.rnd_shp_max_size = rnd_shp_max_size
        if random_ship_lengths is not None:
            if isinstance(random_ship_lengths, list):
                self.random_ship_lengths += random_ship_lengths
            else:
                raise ValueError("Cannot initialize \"random_ship_lengths\" with the param: \"{}\".".format(random_ship_lengths))
        if rnd_shp_max_size:
            if n not in self.random_ship_lengths:
                self.random_ship_lengths += [n]
            if m not in self.random_ship_lengths:
                self.random_ship_lengths += [m]
        self.n = n
        self.m = m
        if (26 * 26) < n:
            raise ValueError("Too many rows to initialize a grid.")
        if 100 < m:
            raise ValueError("Too many columns to initialize a grid.")
        self.grid = [[None for j in range(self.m)] for i in range(self.n)]
        print("IN:", ships)
        if not isinstance(ships, list):
            ships = [ships]

        # not players or all([isinstance(p, BattleshipPlayer) for p in players])
        print("BEFORE:", ships)
        if ships and not all([isinstance(s, Battleship) for s in ships]):
            ships = []
        self.battleships = ships if ships is not None else []
        print("CREATING BATTLESHIPS:", self.battleships)
        for ship in self.battleships:
            print("adding battleship:", ship)
            self.add_battleship(ship)
        # self.grid = [[None, 1, None, None, 2], [3, 4, None, None, 5]]
        # self.grid = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
        # self.grid = [list(range(i * 5, (i * 5) + 5)) for i in range(8)]
        # self.n = len(self.grid)
        # self.m = len(self.grid[0])
        print("grid:", self.grid)

        if m < n:
            self.grid = np.transpose(self.grid).tolist()
            self.n, self.m, = m, n

    def open_cell(self, i, j):
        return self.grid[i][j] is None

    def hit_cell(self, i, j):
        return self.grid[i][j] == BattleshipGrid.SYM_HIT

    def miss_cell(self, i, j):
        return self.grid[i][j] == BattleshipGrid.SYM_BLANK

    def gen_random_cell(self):
        i, j, v = choice(self.lines(filter_vals=True, filter_unique=True))
        return i, j

    def add_battleship(self, battleship):
        self.battleships.append(battleship)
        print(battleship)
        for c_i, c_j in battleship.get_ij():
            self.place(c_i, c_j, BattleshipGrid.SYM_SHIP)

    def gen_ship(self, i=None, j=None, length=None, number=1):
        if self.is_playable():
            available = self.lines(filter_vals=True)
            max_length = max([len([line]) for line in available])
            print("max_length", max_length, "\navailable:", available)
            print("STUFF", list(map(len, available)))
            max_length, max_line = max_idx(list(map(len, available)))
            available_ship_lens = [sl for sl in self.random_ship_lengths if sl <= max_line]
            remaining_lines = [line for line in available if len(line) <= max_line and len(line) in available_ship_lens]
            if not remaining_lines:
                raise ValueError("Not enough space to spawn a new ship.")

            chosen_line = choice(remaining_lines)
            print(dict_print({
                "available": available,
                "max_length_idx": max_length,
                "available[max_length]": available[max_length],
                "available_ships": available_ship_lens,
                "max_line": max_line,
                "remaining_lines": remaining_lines,
                "choice_idx": chosen_line,
            }, "Generating Ship"))

            battleship = Battleship(
                "Battleship #{}".format(str(len(self.battleships) + 1).rjust(2, "0")),
                chosen_line
            )
            self.add_battleship(battleship)
        else:
            raise ValueError("Unable to generate a new battleship on current grid. No available cells.")
        if 1 < number:
            self.gen_ship(i=i, j=j, length=length, number=number - 1)

    def is_playable(self):
        if self.grid:
            for row in self.grid:
                if None in row:
                    return True
        return False

    def place(self, i, j, val):
        print("placing: {} in ({}, {})".format(val, i, j))
        print("self.grid({}):".format(len(self.grid)), self.grid)
        self.grid[i][j] = val

    def lines(self, filter_none=False, filter_vals=False, filter_syms=None, filter_unique=False):
        """
        Return a list of all possible cell lines.
        :param filter_none: Remove any cells with a None entry. => 2D List OR 1D List
        :param filter_vals: Remove any cells with a non_None entry. => 2D List OR 1D List
        :param filter_syms: Remove any cells with matching symbols. => 2D List OR 1D List
        :param filter_unique: Return each filtered cell only once. => 1D List ONLY
        :return: List of lines formed by filtered cells OR List of filtered cells
        """
        print(dict_print({
            "filter_none": filter_none,
            "filter_vals": filter_vals,
            "filter_syms": filter_syms,
            "filter_unique": filter_unique
        }))

        PAD = "PAD"
        n = self.n
        m = self.m
        grid = self.grid
        res = [row.copy() for row in grid]
        temp_grid = [[grid[j][i] for j in range(n)] for i in range(m)]
        # print("1 grid     :", grid)
        # print("1 temp_grid:", temp_grid)
        if m < n:
            grid, temp_grid = temp_grid, grid
            n, m = m, n
        # print("2 grid     :", grid)
        # print("2 temp_grid:", temp_grid)
        res += temp_grid
        oo = (n + m) % 2
        di = abs(n - m) + 1 + oo
        ts = int(((n + m - 1) - di) / 2) + oo
        a = ts - 1

        lc = 0
        cc = 0
        e = 0
        t = (3 * n) + (3 * m) - 2
        temp = [[] for i in range(t)]
        # print("3 grid     :", grid)
        # print("3 temp_grid:", temp_grid)
        # print("3 temp:", temp)

        if filter_syms and not isinstance(filter_syms, list):
            filter_syms = [filter_syms]
        else:
            filter_syms = []

        # print("N x M: ({} x {})".format(n, m))
        tally = 0
        for i in range(n):
            for j in range(m):
                v = grid[i][j]
                if v in filter_syms:
                    tally += 1
                    continue
                s = min(i, j)
                npl = i - s, j - s
                d1 = (npl[0] + npl[1])
                if (j - s) == 0 and (i - s) != 0:
                    d1 += m - 1
                d1 += n + m

                f = max(0, min(i, m - j - 1))
                npr = i - f, j + f
                d2 = n + m + (npr[0] + npr[1])
                # print("npr:", npr, "f:", f)
                if (j + f) == m and (i - f) != 0:
                    d2 += m - 1
                d2 += (n + m - 1)
                # print("i:", i, "| j:", j, "| v:", v, "| d1:", d1, "| d2:", d2, "| di:", (n+m-1))
                temp[i].append((i, j, v))
                temp[j + n].append((i, j, v))
                temp[d1].append((i, j, v))
                temp[d2].append((i, j, v))
        # print("4 grid     :", grid)
        # print("4 temp_grid:", temp_grid)
        # print("4 temp:", tem                                                                                                                                                                                                                                                    p)

        temp = temp[:len(temp) - tally]

        # print("ts:", ts, "\nd:", di, "\ntemp2:", temp)
        if filter_none or filter_vals:
            filtered_temp = []
            for line in temp:
                has_none = False
                filtered_line = []
                # print("line", line)
                for i, j, v in line:
                    # print("fn?: {} fv?: {} fl: {}".format(filter_none, filter_vals, filtered_line))
                    if filter_none:
                        if filtered_line and v is None:
                            filtered_temp.append(filtered_line)
                            filtered_line = []
                        elif v is not None:
                            filtered_line.append((i, j, v))
                    if filter_vals:
                        if filtered_line and v is not None:
                            filtered_temp.append(filtered_line)
                            filtered_line = []
                        elif v is None:
                            filtered_line.append((i, j, v))
                        # if filtered_line and v is not None:
                        #     filtered_temp.append(filtered_line)
                        #     filtered_line = []
                        # elif v is None:
                        #     filtered_line.append((i, j, v))
                if filtered_line:
                    filtered_temp.append(filtered_line)

            temp = [ft.copy() for ft in filtered_temp]

        if filter_unique:
            checked_cells = {}
            valid_cells = []
            for line in temp:
                for cell in line:
                    i, j, v = cell
                    key = "{}X{}".format(i, j)
                    if key not in checked_cells:
                        checked_cells[key] = v
                        valid_cells.append(cell)
            temp = valid_cells.copy()

        # for tt in temp:
        #     if isinstance(tt, list):
        #         print("Line:\t\t", [ttt for ttt in tt])
        #     else:
        #         print("Line:\t{}".format(tt))
        return temp

    # def lines(self, filter_none=False):
    #     n = self.n
    #     m = self.m
    #     grid = self.grid
    #     res = [row.copy() for row in grid]
    #     temp = [[grid[j][i] for j in range(n)] for i in range(m)]
    #     print("grid:", grid)
    #     print("temp:", temp)
    #     if m < n:
    #         grid, temp = temp, grid
    #     res += temp
    #     d = abs(n - m) + 1
    #     ts = int(((n + m - 1) - d) / 2)
    #
    #     lc = 0
    #     cc = 0
    #     e = 0
    #     temp = [[] for i in range(d + (2 * ts))]
    #     while e < d:
    #         c = 0
    #         while c < min(n, m):
    #             temp[e].append((c, c + e, grid[c][c + e]))
    #             c += 1
    #         e += 1
    #
    #     print("temp1:", temp)
    #     for p1 in range(ts):
    #         for p2 in range(p1 + 1, ts + 1):
    #             temp[e].append((p2, p2 - p1 - 1, grid[p2][p2 - p1 - 1]))
    #             temp[e + ts].append((p2 - p1 - 1, p2 + ts - 1, grid[p2 - p1 - 1][p2 + ts - 1]))
    #             print("e: {}, ts: {}, e + ts: {}".format(e, ts, e + ts))
    #         e += 1
    #
    #     print("ts:", ts, "\nd:", d, "\ntemp2:", temp)
    #     if filter_none:
    #         filtered_temp = []
    #         for line in temp:
    #             has_none = False
    #             filtered_line = []
    #             print("line", line)
    #             for i, j, v in line:
    #                 if filtered_line and v is None:
    #                     filtered_temp.append(filtered_line)
    #                     filtered_line = []
    #                 elif v is not None:
    #                     filtered_line.append((i, j, v))
    #             if filtered_line:
    #                 filtered_temp.append(filtered_line)
    #         temp = filtered_temp.copy()
    #     return temp

    # def lines(self, filter_none=False):
    #     PAD = "PAD"
    #     n = self.n
    #     m = self.m
    #     grid = self.grid
    #     res = [row.copy() for row in grid]
    #     temp_grid = [[grid[j][i] for j in range(n)] for i in range(m)]
    #     print("1 grid     :", grid)
    #     print("1 temp_grid:", temp_grid)
    #     if m < n:
    #         grid, temp_grid = temp_grid, grid
    #     print("2 grid     :", grid)
    #     print("2 temp_grid:", temp_grid)
    #     res += temp_grid
    #     oo = (n + m) % 2
    #     d = abs(n - m) + 1 + oo
    #     ts = int(((n + m - 1) - d) / 2) + oo
    #     a = ts - 1
    #
    #     lc = 0
    #     cc = 0
    #     e = 0
    #     temp = [[] for i in range(d + (4 * ts))]
    #     print("len[]({}), len[0]({})".format(len(temp), len(temp[0])))
    #     while e < d:
    #         c = 0
    #         while c < min(n, m):
    #             print("e", e, "c", c)
    #             temp[e].append((c, c, grid[c][c]))
    #             c += 1
    #         e += 1
    #     print("temp:", temp)
    #
    #     for i in range(self.n):
    #         temp_grid[i] = [PAD for p in range(a)] + temp_grid[i] + [PAD for p in range(a)]
    #
    #     for i, row in enumerate(temp_grid):
    #         if 0 <= (i - a):
    #             v = temp_grid[i][i]
    #             print("v:", v)
    #         # for j, v in enumerate(row):
    #
    #     print("ts:", ts, "\nd:", d, "\ntemp2:", temp)
    #     if filter_none:
    #         filtered_temp = []
    #         for line in temp:
    #             has_none = False
    #             filtered_line = []
    #             print("line", line)
    #             for i, j, v in line:
    #                 if filtered_line and v is None:
    #                     filtered_temp.append(filtered_line)
    #                     filtered_line = []
    #                 elif v is not None:
    #                     filtered_line.append((i, j, v))
    #             if filtered_line:
    #                 filtered_temp.append(filtered_line)
    #         temp = filtered_temp.copy()
    #     return temp

    def __copy__(self):
        for bs in self.battleships:
            print("bs:\t", bs)
        return BattleshipGrid(self.n, self.m, self.random_ship_lengths, self.rnd_shp_max_size, ships=[copy.copy(bs) for bs in self.battleships])

    def max_length_available(self):
        if self.grid:
            for row in self.grid:
                if None in row:
                    pass

    def __repr__(self):
        return "\n\tGrid\n\n" + "\n".join(["|" + "|".join([pad_centre(ln, 5) for ln in list(map(str, line))]) + "|" for line in self.grid]) + "\n"


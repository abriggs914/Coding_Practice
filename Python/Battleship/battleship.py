import random


class Battleship:

    def __init__(self, n, m, random_ship_lengths=None):
        self.random_ship_lengths = [1, 2, 3, 4, 5] if random_ship_lengths is None else random_ship_lengths
        self.n = n
        self.m = m
        self.grid = [[None for j in range(self.m)] for i in range(self.n)]
        # self.grid = [[None, 1, None, None, 2], [3, 4, None, None, 5]]
        # self.grid = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
        # self.grid = [list(range(i * 5, (i * 5) + 5)) for i in range(8)]
        # self.n = len(self.grid)
        # self.m = len(self.grid[0])
        self.grid[1][1] = 1
        print("grid:", self.grid)

    def gen_ship(self, i=None, j=None, length=None):
        if self.is_playable():
            available = self.lines(True)
            max_length = max([len([])])
            length = random.choice(self.random_ship_lengths) if length is None else length

    def is_playable(self):
        if self.grid:
            for row in self.grid:
                if None in row:
                    return True
        return False

    def lines(self, filter_none=False, filter_vals=False, filter_unique=False):
        """
        Return a list of all possible cell lines.
        :param filter_none: Remove any cells with a None entry. => 2D List OR 1D List
        :param filter_vals: Remove any cells with a non_None entry. => 1D List ONLY
        :param filter_unique: Return each filtered cell only once. => 2D List OR 1D List
        :return: List of lines formed by filtered cells OR List of filtered cells
        """
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

        # print("N x M: ({} x {})".format(n, m))
        for i in range(n):
            for j in range(m):
                v = grid[i][j]
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
                    elif filter_vals:
                        if filtered_line and v is not None:
                            filtered_temp.append(filtered_line)
                            filtered_line = []
                        elif v is None:
                            filtered_line.append((i, j, v))
                if filtered_line:
                    filtered_temp.append(filtered_line)
            temp = filtered_temp.copy()

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

        for tt in temp:
            if isinstance(tt, list):
                print("\t\t", [ttt[2] for ttt in tt])
            else:
                print("\t{}".format(tt))
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

    def max_length_available(self):
        if self.grid:
            for row in self.grid:
                if None in row:
                    pass


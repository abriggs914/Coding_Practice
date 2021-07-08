import random


class Battleship:

    def __init__(self, n, m, random_ship_lengths=None):
        self.random_ship_lengths = [1, 2, 3, 4, 5] if random_ship_lengths is None else random_ship_lengths
        self.n = n
        self.m = m
        self.grid = [[None for j in range(self.m)] for i in range(self.n)]
        self.grid = [[None, 1, None, None, 2], [3, 4, None, None, 5]]
        # self.grid = [list(range(i * 5, (i * 5) + 5)) for i in range(8)]
        print("grid:", self.grid)
        self.n = len(self.grid)
        self.m = len(self.grid[0])

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

    def lines(self, filter_none=False):
        n = self.n
        m = self.m
        grid = self.grid
        res = [row.copy() for row in grid]
        temp = [[grid[j][i] for j in range(n)] for i in range(m)]
        print("grid:", grid)
        print("temp:", temp)
        if m < n:
            grid, temp = temp, grid
        res += temp
        d = abs(n - m) + 1
        ts = int(((n + m - 1) - d) / 2)

        lc = 0
        cc = 0
        e = 0
        temp = [[] for i in range(d + (2 * ts))]
        while e < d:
            c = 0
            while c < min(n, m):
                temp[e].append((c, c + e, grid[c][c + e]))
                c += 1
            e += 1

        print("temp1:", temp)
        for p1 in range(ts):
            for p2 in range(p1 + 1, ts + 1):
                temp[e].append((p2, p2 - p1 - 1, grid[p2][p2 - p1 - 1]))
                temp[e + ts].append((p2 - p1 - 1, p2 + ts - 1, grid[p2 - p1 - 1][p2 + ts - 1]))
                print("e: {}, ts: {}, e + ts: {}".format(e, ts, e + ts))
            e += 1

        print("ts:", ts, "\nd:", d, "\ntemp2:", temp)
        if filter_none:
            filtered_temp = []
            for line in temp:
                has_none = False
                filtered_line = []
                print("line", line)
                for i, j, v in line:
                    if filtered_line and v is None:
                        filtered_temp.append(filtered_line)
                        filtered_line = []
                    elif v is not None:
                        filtered_line.append((i, j, v))
                if filtered_line:
                    filtered_temp.append(filtered_line)
            temp = filtered_temp.copy()
        return temp

    def max_length_available(self):
        if self.grid:
            for row in self.grid:
                if None in row:
                    pass


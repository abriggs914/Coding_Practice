import random


class Battleship:

    def __init__(self, n, m, random_ship_lengths=None):
        self.random_ship_lengths = [1, 2, 3, 4, 5] if random_ship_lengths is None else random_ship_lengths
        self.n = n
        self.m = m
        self.grid = [[None for j in range(self.m)] for i in range(self.n)]
        # self.grid = [[None, 1, None, None, 2], [3, 4, None, None, 5]]
        self.grid = [list(range(i * 5, (i * 5) + 5)) for i in range(8)]
        print("grid:", self.grid)
        self.n = len(self.grid)
        self.m = len(self.grid[0])

    def gen_ship(self, i=None, j=None, length=None):
        if self.is_playable():
            length = random.choice(self.random_ship_lengths) if length is None else length

    def is_playable(self):
        if self.grid:
            for row in self.grid:
                if None in row:
                    return True
        return False

    def lines(self):
        n = self.n
        m = self.m
        grid = self.grid
        res = [row.copy() for row in grid]
        temp = [[grid[j][i] for j in range(n)] for i in range(m)]
        print("grid:", grid)
        print("temp:", temp)
        res += temp
        d = abs(n - m) + 1
        ts = ((n + m - 1) - d) / 2

        lc = 0
        cc = 0
        e = 0
        temp = [[] for i in range(d + int(2 * ts))]
        while e < d:
            c = 0
            while c < min(n, m):
                print("(e, c): ({}, {})".format(e, c), "v:", grid[c][e])
                temp[e].append(grid[c][e])
                c += 1
            e += 1
        print("ts:", ts, "\nd:", d, "\ntemp:", temp)

    def max_length_available(self):
        if self.grid:
            for row in self.grid:
                if None in row:
                    pass


from utility import *
from time import sleep
import random
import os

clear = lambda: os.system('cls') #on Windows System

class GridDimensionException(Exception):
    def __init__(self, msg=""):
        msg = "Grid dimension is out of bounds.\n" + msg
        super().__init__(msg)

class SnakeCrossingException(Exception):
    def __init__(self, msg=""):
        msg = "Snakes cannot cross each other.\n" + msg
        super().__init__(msg)

# angle must be a positive multiple of 45 degrees
def rotate(d, a, clockwise=True):
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    if not clockwise:
        dirs.reverse()
    i = dirs.index(d.upper())
    a /= 45
    i = (i + a) % 8


directions = {
    "N": {
        "dir": "north",
        "i": -1,
        "j": 0,
        "opp": "S",
        "bounce": "S",
        "mirror_x": "S",
        "mirror_y": "N"
    },
    "NE": {
        "dir": "north-east",
        "i": -1,
        "j": 1,
        "opp": "SW",
        "bounce": "NW",
        "mirror_x": "SE",
        "mirror_y": "NW"
    },
    "E": {
        "dir": "east",
        "i": 0,
        "j": 1,
        "opp": "W",
        "bounce": "W",
        "mirror_x": "E",
        "mirror_y": "W"
    },
    "SE": {
        "dir": "south-east",
        "i": 1,
        "j": 1,
        "opp": "NW",
        "bounce": "SW",
        "mirror_x": "NE",
        "mirror_y": "SW"
    },
    "S": {
        "dir": "south",
        "i": 1,
        "j": 0,
        "opp": "N",
        "bounce": "N",
        "mirror_x": "N",
        "mirror_y": "S"
    },
    "SW": {
        "dir": "south-west",
        "i": 1,
        "j": -1,
        "opp": "NE",
        "bounce": "SE",
        "mirror_x": "NW",
        "mirror_y": "SE"
    },
    "W": {
        "dir": "west",
        "i": 0,
        "j": -1,
        "opp": "E",
        "bounce": "E",
        "mirror_x": "W",
        "mirror_y": "E"
    },
    "NW": {
        "dir": "north-west",
        "i": -1,
        "j": -1,
        "opp": "SE",
        "bounce": "NE",
        "mirror_x": "SW",
        "mirror_y": "NE"
    }
}
DEFAULT_FOOD_SYMBOL = "O"
DEFAULT_SNAKESEGMENT_SYMBOL = "I"

# Important: v > 0
# Important: type(food) == Food
def food_to_segment(food, snake):
    segments = []
    v = food.val
    i, j = food.ij
    n, m = snake.n, snake.m
    w = snake.wrap
    d = snake.direction
    segs = snake.line()
    next_ij = snake.next_segment()
    ni, nj = next_ij
    if v == 1:
        segments.append(SnakeSegment(ni, nj, snake.default_segment_symbol))
    elif v < 1:
        raise ValueError("Food object cannot have a value less than 1")
    else:
        si, sj = snake.segments[0].ij
        s = Snake(snake.name, snake.n, snake.m, si, sj, snake.direction, snake.wrap, len(snake.line()))
        f = Food(ni, nj, food.val - 1)
        s.eat_food(f)
        segments += food_to_segment(f, s)
    print("ni: {ni}, nj: {nj}, segments: {seg}".format(ni=ni, nj=nj, seg=segments))

    # for k in range(v):
    #     next_ij = snake.next_segment()
    #     if next_ij != None:
    #         ni, nj = next_ij
    #         segments.append(SnakeSegment(ni, nj, symbol=food_symbol))
    return segments

class Food:
    def __init__(self, i, j, val, symbol=DEFAULT_FOOD_SYMBOL):
        self.ij = i, j
        self.val = val
        self.symbol = symbol

class SnakeSegment:
    def __init__(self, i, j, symbol=DEFAULT_SNAKESEGMENT_SYMBOL):
        self.ij = i, j
        self.symbol = symbol

    def set(self, i, j):
        self.ij = i, j
    
    def __repr__(self):
        return "SnakeSegment (" + str(self.ij[0]) + ", " + str(self.ij[1]) + ")"

class Snake:
    # name              -   string: name
    # n                 -   int: number grid rows
    # m                 -   int: number grid columns
    # start_i           -   int: row position of snake head
    # start_j           -   int: column position of snake head
    # start_direction   -   string: member of the directions dict
    # wrap              -   boolean: T if snake can wrap the grid
    # start_length      -   int: populate segments with n segments
    # Important: start_length > 0
    def __init__(self, name, n, m, start_i, start_j, start_direction, wrap, start_length=1, default_segment_symbol=DEFAULT_SNAKESEGMENT_SYMBOL):
        self.name = name
        self.n = n
        self.m = m
        self.start_i = start_i
        self.start_j = start_j
        self.ij = start_i, start_j
        self.direction = start_direction
        self.length = start_length
        self.wrap = wrap
        self.default_segment_symbol = default_segment_symbol
        self.segments = [SnakeSegment(start_i, start_j, default_segment_symbol)]
        self.distance_travelled = 0
        if start_length > 1:
            self.init_segments(start_length - 1)
        self.hidden_segments = []

    # return i and j for the next segment
    def next_segment(self, force=False):
        d = self.direction
        o = directions[directions[d]["opp"]]
        segs = self.line()
        i, j = segs[-1]
        r = (i + o["i"]) % self.n if self.wrap else i + o["i"]
        c = (j + o["j"]) % self.m if self.wrap else j + o["j"]
        if (r, c) not in segs:
            return r, c
        elif force:
            valid = []
            for dr, dat in directions.items():
                r = (i + dat["i"]) % self.n if self.wrap else i + dat["i"]
                c = (j + dat["j"]) % self.m if self.wrap else j + dat["j"]
                if (r, c) not in segs:
                    valid.append(dr)
            if valid:
                return random.choice(valid)
        return None

        # d = self.direction
        # o = directions[d]["opp"]
        # segs = self.line()
        # last = segs[-1]
        # i, j = last.ij
        # valid = []
        # for dr, dat in directions.items():
        #     r = (i + dat["i"]) % self.n if self.wrap else i + dat["i"]
        #     c = (j + dat["j"]) % self.m if self.wrap else j + dat["j"]
        #     if (r, c) % self.m) not in segs:
        #         valid.append(dr)
        # if o in valid:
        #     return i + directions[o]["i"], i + directions[o]["i"]
        # return None


    def init_segments(self, start_length):
        segs = []
        for i in range(start_length):
            ns = self.next_segment()
            if ns == None:
                break
            ns = SnakeSegment(*ns, self.default_segment_symbol)
            self.segments.append(ns)

    def line(self):
        return [seg.ij for seg in self.segments]

    # def set_direction(self, d):
    #     self.direction = d

    # Important: type(food) == Food
    def eat_food(self, food):
        segments = food_to_segment(food, self)
        print("new segments", segments)
        if food.ij in self.line():
            for seg in segments:
                self.hidden_segments.append(seg)
        else:
            for seg in segments:
                self.segments.append(seg)

    def shift(self):
        # print("self.direction", self.direction)
        # print("segs B:", self.segments)
        self.distance_travelled += 1
        d = directions[self.direction]
        pi, pj = self.segments[0].ij
        di, dj = d["i"], d["j"]
        # self.segments[0].set(pi + di, pj + dj)
        # print("line: ", self.line())
        ni, nj = pi + di, pj + dj

        if self.wrap:
            ni %= self.n
            nj %= self.m
        else:
            if (ni < 0 or ni >= self.n or nj < 0 or nj >= self.m) and len(self.direction) == 2:
                if ni < 0 or ni >= self.n:
                    self.change_direction(d["mirror_x"])
                elif nj < 0 or nj >= self.m:
                    self.change_direction(d["mirror_y"])
                else:
                    self.change_direction(d["bounce"])
                d = directions[self.direction]
                ni, nj = pi + d["i"], pj + d["j"]
            ti, tj = ni, nj
            ni = max(0, min(ni, self.n - 1))
            nj = max(0, min(nj, self.m - 1))
            if ti != ni or tj != nj:
                return

        if ni < 0 or ni >= self.n or nj < 0 or nj >= self.m:
            raise GridDimensionException("i: " + str(ni) + ", j: " + str(nj))

        self.segments[0].set(ni, nj)
        for i in range(1, len(self.segments)):
            ci, cj = self.segments[i].ij
            # pi, pj = ci + di, cj + dj
            self.segments[i].set(pi, pj)
            pi, pj = ci, cj
        # print("line: ", self.line())
        # print("segs A:", self.segments)

    # def shift(self):
    #     print("segs B:", self.segments)
    #     self.distance_travelled += 1
    #     d = directions[self.direction]
    #     pi, pj = self.segments[0].ij
    #     di, dj = d["i"], d["j"]
    #     # self.segments[0].set(pi + di, pj + dj)
    #     for i in range(len(self.segments)):
    #         ci, cj = self.segments[i].ij
    #         pi, pj = ci + di, cj + dj
    #         self.segments[i].set(pi, pj)
    #     print("segs A:", self.segments)

    def change_direction(self,  d):
        self.direction = d

    def __repr__(self):
        lsegs = len(self.segments)
        s = "-<8" + "".join(["=" for i in range(lsegs)]) + "-"
        return self.name + ", traversed " + str(self.distance_travelled) + " { (\'" + str(self.default_segment_symbol) +  "\') " + s + " (" + str(lsegs) + ") }"

class SnakeGame:

    def __init__(self, name, n, m, start_snakes=None, start_food=None):
        self.name = name
        self.n = n
        self.m = m
        self.grid = [[None for j in range(m)] for i in range(n)]
        self.snakes = []
        self.food = []

        if start_snakes != None:
            start_snakes = start_snakes if type(start_snakes) == list else [start_snakes]
            self.snakes = start_snakes
        if start_food != None:
            start_food = start_food if type(start_food) == list else [start_food]
            self.food = start_food

    def __repr__(self):
        res = "\n"
        segments = {}
        keyify = lambda i, j: str(i) + "," + str(j)
        for snake in self.snakes:
            segs = snake.segments
            for seg in segs:
                i, j = seg.ij
                segments[keyify(i, j)] = seg.symbol
                
        # print("PRINTING {" + str(segments) + "}\n" + dict_print(segments, "segments", number=True) + "\n")
        for i in range(self.n):
            for j in range(self.m):
                k = keyify(i, j)
                if k in segments:
                    v = segments[k]
                else:
                    v = self.grid[i][j]
                if v == None:
                    v = "-"
                res += v
            res += "\n"
        res += "\n"

        return res

def crossing(s1, s2=None):
    if s2 is None and type(s1) == list:
        crosses = []
        for i in range(len(s1)):
            for j in range(i + 1, len(s1)):
                cross = crossing(s1[i], s1[j])
                if cross:
                    return cross
        return False
    else:
        a = s1.line()
        b = s2.line()
        # print("a", a)
        # print("b", b)
        for ij in a:
            if ij in b:
                return str(s1) + "\n\t\tcrosses\n" + str(s2)
        return False

if __name__ == "__main__":
    rows = 16
    cols = 20

    snake_1 = Snake(name="snake 1", n=rows, m=cols, start_i=10, start_j=12, start_direction="W", wrap=False, start_length=1, default_segment_symbol="1")
    snake_2 = Snake(name="snake 2", n=rows, m=cols, start_i=8, start_j=12, start_direction="NE", wrap=False, start_length=1, default_segment_symbol="2")
    snake_3 = Snake(name="snake 3", n=rows, m=cols, start_i=2, start_j=2, start_direction="SE", wrap=True, start_length=1, default_segment_symbol="3")
    food_1 = Food(i=10, j=13, val=8)
    snake_game = SnakeGame(name="game 1", n=rows, m=cols, start_snakes=[snake_1, snake_2, snake_3], start_food=food_1)
    # print(snake)
    # print(snake.next_segment())
    # snake.eat_food(food_1)
    # print(snake)
    # print(snake.next_segment())
    print("SnakeGame:", snake_game)
    snake_1.change_direction("S")
    for i in range(60):
        snake_1.shift()
        snake_2.shift()
        snake_3.shift()
        cross = crossing(snake_game.snakes)
        if cross:
            raise SnakeCrossingException(cross)
        if i % 3 == 0:
            for s in snake_game.snakes:
                new_dir = random.choice(list(directions.keys()))
                print("New direction " + new_dir)
                s.change_direction(new_dir)

        clear()
        print("SnakeGame:", snake_game)
        sleep(0.2)
    print("SnakeGame:", snake_game)
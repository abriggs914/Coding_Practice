from utility import *
import random

directions = {
    "N": {
        "dir": "north",
        "i": -1,
        "j": 0,
        "opp": "S"
    },
    "NE": {
        "dir": "north-east",
        "i": -1,
        "j": 1,
        "opp": "SW"
    },
    "E": {
        "dir": "east",
        "i": 0,
        "j": 1,
        "opp": "W"
    },
    "SE": {
        "dir": "south-east",
        "i": 1,
        "j": 1,
        "opp": "NW"
    },
    "S": {
        "dir": "south",
        "i": 1,
        "j": 0,
        "opp": "N"
    },
    "SW": {
        "dir": "south-west",
        "i": 1,
        "j": -1,
        "opp": "NE"
    },
    "W": {
        "dir": "west",
        "i": 0,
        "j": -1,
        "opp": "E"
    },
    "NW": {
        "dir": "north-west",
        "i": -1,
        "j": -1,
        "opp": "SE"
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
        print("segs B:", self.segments)
        self.distance_travelled += 1
        d = directions[self.direction]
        pi, pj = self.segments[0].ij
        di, dj = d["i"], d["j"]
        # self.segments[0].set(pi + di, pj + dj)
        for i in range(len(self.segments)):
            ci, cj = self.segments[i].ij
            pi, pj = ci + di, cj + dj
            self.segments[i].set(pi, pj)
        print("segs A:", self.segments)

    def change_direction(self, d):
        self.direction = d

    def __repr__(self):
        return self.name + ", " + str(len(self.segments)) + " segments long, traversed " + str(self.distance_travelled)

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

if __name__ == "__main__":
    snake_1 = Snake(name="snake 1", n=20, m=20, start_i=10, start_j=12, start_direction="W", wrap=True, start_length=8, default_segment_symbol="1")
    snake_2 = Snake(name="snake 1", n=20, m=20, start_i=8, start_j=12, start_direction="NE", wrap=True, start_length=3, default_segment_symbol="2")
    food_1 = Food(i=10, j=13, val=8)
    snake_game = SnakeGame(name="game 1", n=20, m=20, start_snakes=[snake_1, snake_2], start_food=food_1)
    # print(snake)
    # print(snake.next_segment())
    # snake.eat_food(food_1)
    # print(snake)
    # print(snake.next_segment())
    print("SnakeGame:", snake_game)
    for i in range(4):
        snake_2.shift()
        if i % 2 == 0:
            new_dir = random.choice(list(directions.keys()))
            print("New direction " + new_dir)
            snake_2.change_direction(new_dir)
    print("SnakeGame:", snake_game)

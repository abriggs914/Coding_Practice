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
def food_to_segment(food, snake, food_symbol=DEFAULT_FOOD_SYMBOL):
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
        segments.append(SnakeSegment(ni, nj, symbol=food_symbol))
    else:
        s = Snake(snake.name, snake.n, snake.m, snake.start_i, snake.start_j, snake.direction, snake.wrap, len(snake.line()))
        f = Food(ni, nj, food.val - 1)
        s.eat_food(f)
        segments += food_to_segment(f, s, food_symbol)

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
    def __init__(self, name, n, m, start_i, start_j, start_direction, wrap, start_length=1):
        self.name = name
        self.n = n
        self.m = m
        self.start_i = start_i
        self.start_j = start_j
        self.ij = start_i, start_j
        self.direction = start_direction
        self.length = start_length
        self.wrap = wrap
        self.segments = self.init_segments(start_length)
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
        return [SnakeSegment(self.ij[0], self.ij[1])]

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

if __name__ == "__main__":
    snake = Snake(name="snake 1", n=20, m=20, start_i=10, start_j=12, start_direction="W", wrap=True, start_length=1)
    food_1 = Food(i=10, j=13, val=8)
    print(snake)
    print(snake.next_segment())
    snake.eat_food(food_1)
    print(snake)
    print(snake.next_segment())

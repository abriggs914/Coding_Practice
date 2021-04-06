directions = {
    "N": "north",
    "NE": "north-east",
    "E": "east",
    "SE": "south-east",
    "S": "south",
    "SW": "south-west",
    "W": "west",
    "NN": "north-west",
}

class Food:
    def __init__(self, i, j, val, symbol="O"):
        self.ij = i, j
        self.val = val
        self.symbol = symbol

class SnakeSegment:
    def __init__(self, i, j, symbol="I")
        self.name = name
        self.ij = i, j

class Snake:
    def __init__(self, name, start_i, start_j, start_direction, start_length=1)
        self.name = name
        self.direction = start_direction
        self.length = start_length
        self.segments = [SnakeSegment(start_i, start_j)
        self.hidden_segments = []

    def eat_food(food):
        fi, fd = food.ij
        for s in self.segments:
            si, sj = s.ij
            if fi == si and fj == sj:
                self.hidden_segments.append(food)
                return
        self.segments.append(food_to_segment(food))

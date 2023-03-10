from enum import Enum
import random


class CellVal(Enum):
    # Walls
    WALL = ("#", True, False, False)

    # Objects
    OBJ_A = ("1", False, True, False)
    OBJ_B = ("2", False, True, False)
    OBJ_C = ("3", False, True, False)
    OBJ_D = ("4", False, True, False)
    OBJ_E = ("5", False, True, False)
    OBJ_F = ("6", False, True, False)
    OBJ_G = ("7", False, True, False)
    OBJ_H = ("8", False, True, False)
    OBJ_I = ("9", False, True, False)
    OBJ_J = ("0", False, True, False)
    OBJ_K = ("a", False, True, False)
    OBJ_L = ("b", False, True, False)
    OBJ_M = ("c", False, True, False)
    OBJ_N = ("d", False, True, False)
    OBJ_O = ("e", False, True, False)
    OBJ_P = ("f", False, True, False)

    # Creatures
    CREATURE_A = ("!", False, False, True)
    CREATURE_B = ("@", False, False, True)
    CREATURE_C = ("#", False, False, True)
    CREATURE_D = ("$", False, False, True)
    CREATURE_E = ("%", False, False, True)
    CREATURE_F = ("^", False, False, True)
    CREATURE_G = ("&", False, False, True)
    CREATURE_H = ("*", False, False, True)
    CREATURE_I = ("(", False, False, True)
    CREATURE_J = (")", False, False, True)

    # Nothing
    NOTHING = (" ", False, False, False)

    def __new__(cls, value, is_wall=False, is_object=False, is_creature=False):
        member = object.__new__(cls)
        member._value_ = value
        member.is_wall = is_wall
        member.is_object = is_object
        member.is_creature = is_creature
        return member

    def __init__(self, value, is_wall=False, is_object=False, is_creature=False):
        self._value_ = value
        self.is_wall = is_wall
        self.is_object = is_object
        self.is_creature = is_creature


# class Grid:
#     def __init__(self, width, height, infill=0.3):
#         self.width = width
#         self.height = height
#         self.grid = [[CellVal.NOTHING for _ in range(width)] for _ in range(height)]
#
#         # Fill the edges with wall members
#         for x in range(width):
#             self.grid[0][x] = CellVal.WALL
#             self.grid[height - 1][x] = CellVal.WALL
#         for y in range(height):
#             self.grid[y][0] = CellVal.WALL
#             self.grid[y][width - 1] = CellVal.WALL
#
#         # Fill the interior with wall members
#         num_walls = int(infill * (width - 2) * (height - 2))
#         for i in range(num_walls):
#             x = random.randint(1, width - 2)
#             y = random.randint(1, height - 2)
#             self.grid[y][x] = CellVal.WALL
#
#     def __getitem__(self, index):
#         return self.grid[index]
#
#     def __str__(self):
#         return "\n".join(["".join([str(self.grid[y][x].value) for x in range(self.width)]) for y in range(self.height)])


class Grid:
    def __init__(self, width, height, infill=0.3, inside=True):
        self.width = width
        self.height = height
        self.grid = [[CellVal.NOTHING for _ in range(width)] for _ in range(height)]

        # Fill the edges with wall members
        for x in range(width):
            self.grid[0][x] = CellVal.WALL
            self.grid[height - 1][x] = CellVal.WALL
        for y in range(height):
            self.grid[y][0] = CellVal.WALL
            self.grid[y][width - 1] = CellVal.WALL

        # Fill the interior with wall members
        num_walls = int(infill * (width - 2) * (height - 2))
        for i in range(num_walls):
            if inside:
                x, y = self._get_strategic_wall_pos()
            else:
                x = random.randint(1, width - 2)
                y = random.randint(1, height - 2)
            self.grid[y][x] = CellVal.WALL

    def _get_strategic_wall_pos(self):
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            neighbors = self._get_neighbors(x, y)
            if len(neighbors) <= 1:  # Avoid placing walls on their own
                continue
            if all(n == CellVal.WALL for n in neighbors):  # Ensure walls create corridors and rooms
                continue
            if all(n == CellVal.NOTHING for n in neighbors):  # Ensure walls are not isolated
                continue
            if x > 1 and self.grid[y][x - 1] == self.grid[y][x - 2] == CellVal.WALL:  # Avoid placing parallel walls
                continue
            if y > 1 and self.grid[y - 1][x] == self.grid[y - 2][x] == CellVal.WALL:
                continue
            return x, y

    def _get_neighbors(self, x, y):
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                if nx < 0 or ny < 0 or nx >= self.width or ny >= self.height:
                    continue
                neighbors.append(self.grid[ny][nx])
        return neighbors

    def __getitem__(self, index):
        return self.grid[index]

    def __str__(self):
        return "\n".join(["".join([str(self.grid[y][x].value) for x in range(self.width)]) for y in range(self.height)])


if __name__ == '__main__':
    grid = Grid(18, 12, infill=0.14, inside=True)
    print(grid)

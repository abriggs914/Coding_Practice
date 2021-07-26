
# Battleship class

class Battleship:

    def __init__(self, name, cells=None):
        self.name = name
        cells = cells if cells is not None else []
        new_cells = []
        for cell in cells:
            c = cell
            if len(cell) != 3:
                c = (*cell, None)
            new_cells.append(c)
        self.cells = new_cells
        print("CELLS_IN:", self.cells)

    def get_ij(self):
        return [(i, j) for i, j, v in self.cells]

    def __copy__(self):
        return Battleship(self.name, self.cells.copy())

    def __repr__(self):
        return "\n\t-- {} --\n\t\t{}".format(self.name, "\n\t\t".join(list(map(str, self.cells))))
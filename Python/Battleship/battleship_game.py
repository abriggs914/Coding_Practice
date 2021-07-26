from battleship import Battleship
from battleship_player import BattleshipPlayer
from battleship_grid import BattleshipGrid

import copy

# Battleship Game class

class BattleshipGame:

    def __init__(self, name, players=None, grid=None, ships=None):
        assert isinstance(name, str)
        assert isinstance(players, list)
        assert not players or all([isinstance(p, BattleshipPlayer) for p in players])
        assert isinstance(grid, BattleshipGrid)
        assert isinstance(ships, list)
        assert not ships or all([isinstance(s, Battleship) for s in ships])
        self.name = name
        self.players = players
        self.ships = ships

        for ship in ships:
            grid.add_battleship(ship)
        self.grid = grid
        self.grids = [copy.copy(grid) for player in players]


        self.turn_number = 0

    def get_player_1_grid(self):
        return self.grids[0]

    def get_player_2_grid(self):
        return self.grids[1]

    def get_player_1(self):
        return self.players[0]

    def get_player_2(self):
        return self.players[1]

    def game_grid(self):
        t_cols = get_terminal_columns() + 100 #TODO: this isn't working right.
        n = self.grid.n
        m = self.grid.m
        left_margin = "    "
        orientation = "H"
        mid_space = "  "
        legend_x_w = lenstr(m)
        legend_y_w = lenstr(n)

        gg = ""

        C = 40
        w = (4 * (m + 2)) + C - len(left_margin) - 2
        if t_cols < w:
            orientation = "V"

        if orientation == "H":

            def line_gen(txt, new_line=True):
                return "{lm}#".format(lm=left_margin) + pad_centre(txt, w) + "#" + ("\n" if new_line else "")

            h_border = "".join(["#" for i in range(w + 2)])
            gg = "\n" + left_margin + h_border + "\n"
            gg += line_gen("Turn # {tn}".format(lm=left_margin, tn=self.turn_number))
            col_names = [str(i).rjust(2, "0") for i in range(1, m + 1)]
            header_div = ["__" for i in range(len(col_names))]
            row_names = [chr(i).rjust(2) for i in range(65, 65+n)]
            print("row_names", row_names)
            C -= 2
            gg += line_gen("Player 1" + "".join(" " for i in range(C)) + "Player 2`")
            gg += line_gen("  |" + "|".join(col_names) + "|" + "".join([" " for i in range(C - (2 * m))]) + "|" + "|".join(col_names) + "|")
            gg += line_gen("  |" + "|".join(header_div) + "|" + "".join([" " for i in range(C - (2 * m))]) + "|" + "|".join(header_div) + "|")
            for i in range(n):
                games_line = "".join([" " for i in range(w - 1)])
                for j in range(m):
                    cell_v1 = self.grids[0].grid[i][j] if self.grids[0].grid[i][j] is not None else ""
                    cell_v2 = self.grids[1].grid[i][j] if self.grids[1].grid[i][j] is not None else ""

                    cell_v1, cell_v2 = "T1", "T2"

                    txt_v1 = pad_centre(str(cell_v1)[:2], 2) + "|"
                    txt_v2 = pad_centre(str(cell_v2)[:2], 2) + "|"
                    ss = (j * 3) + 3
                    print("Cell({}, {}): Player 1: {}, Player 2: {}, ss: {}".format(i, j, cell_v1, cell_v2, ss))
                    if j == 0:
                        games_line = row_names[i] + "|" + games_line[:ss + m + C - 5] + row_names[i] + "|" + games_line[ss + m + C + 3:]
                    games_line = games_line[:ss] + txt_v1 + games_line[ss + 3:]
                    games_line = games_line[:ss + m + C + 1] + txt_v2 + games_line[ss + m + C + 4 + 1:]
                    # print("\t\tgames_line:", games_line)
                gg += line_gen(games_line)
            gg += left_margin + h_border + "\n"

        return gg



    def __repr__(self):
        # return "\n\tBattleship Game: {nm}\n\n\t\tTurn:\t\t\t{tn}\n\t\tPlayer 1:\t\t{p1}\n\t\tPlayer 2:\t\t{p2}\n{gd}".format(nm=self.name, tn=self.turn_number, p1 = self.players[0], p2=self.players[1], gd=self.grid)
        return "\n\tBattleship Game: {nm}\n\n\t\t{dp}\n{gd}".format(nm=self.name, dp=dict_print({
            "Turn #": self.turn_number,
            "Player 1": self.players[0],
            "Player 2": self.players[1]
        }, "Battleship Data", marker=" ", TAB="        "), gd=self.grid)


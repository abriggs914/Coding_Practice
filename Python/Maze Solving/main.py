import tkinter
from typing import Literal

from colour_utility import *
from tkinter_utility import button_factory
from utility import *


class Grid(tkinter.Canvas):

    def __init__(
            self,
            master,
            grid_path,
            width=600,
            height=400,
            colour_scheme=None,
            code_empty=" ",
            code_wall="1",
            code_start="0",
            code_goal="9",
            code_path="2",
            code_visited="3",
            code_visited_plus="4",
            draw_legend=True,
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        assert len({code_empty, code_wall, code_start, code_goal, code_path, code_visited}) == 6, f"Error, not all codes are unique.\n\t{code_empty=}\n\t{code_wall=}\n\t{code_start=}\n\t{code_goal=}\n\t{code_path=}\n\t{code_visited=}"

        self.grid_path = grid_path
        self.grid_lines = ""
        self.width, self.height = width, height

        self.code_empty = code_empty
        self.code_wall = code_wall
        self.code_start = code_start
        self.code_goal = code_goal
        self.code_path = code_path
        self.code_visited = code_visited
        self.code_visited_plus = code_visited_plus
        self.draw_legend = draw_legend

        self.colour_scheme = self.validate_colour_scheme(colour_scheme)
        with open(grid_path) as f:
            self.grid_lines = f.readlines()
        print(f"{self.grid_lines=}")

        if not self.grid_lines:
            raise ValueError("Maze not valid.")

        self.start_pos = None
        self.goal_pos = None

        self.h, self.w = len(self.grid_lines), len(self.grid_lines[0].strip())
        self.cells = []
        self.og_cell_colours = []
        self.traversed_values = []
        gc = grid_cells(self.width, self.w, self.height, self.h)
        # print(f"{len(self.grid_lines)=}, {len(self.grid_lines[0].strip())=}")
        # print(f"{self.w=}, {self.h=}")
        # print(f"{len(gc)=}, {len(gc[0])=}, {len(gc[0][0])=}")

        for i in range(self.h):
            row_cells = []
            row_colours = []
            for j in range(self.w):
                char = self.grid_lines[i][j]
                # print(f"{char=}")
                if char == self.code_start:
                    if self.start_pos is not None:
                        raise ValueError("Cannot have a maze with more than one start position.")
                    self.start_pos = (i, j)
                    colour = self.colour_scheme[self.code_start]
                elif char == self.code_wall:
                    colour = self.colour_scheme[self.code_wall]
                elif char == self.code_goal:
                    if self.goal_pos is not None:
                        raise ValueError("Cannot have a maze with more than one goal position.")
                    self.goal_pos = (i, j)
                    colour = self.colour_scheme[self.code_goal]
                else:
                    colour = rgb_to_hex(WHITE)

                dims = gc[i][j]
                row_cells.append(self.create_rectangle(*dims, fill=colour))
                row_colours.append(colour)
            self.og_cell_colours.append(row_colours)
            self.cells.append(row_cells)
            self.traversed_values.append([0 for _ in row_cells])

        self.traverse_direction = tkinter.StringVar(self, value=None)
        self.solving = tkinter.BooleanVar(self, value=False)
        self.solved = tkinter.BooleanVar(self, value=False)
        self.current = tkinter.Variable(self, value=(None, None))

        self.configure(
            width=self.width,
            height=self.height
        )

    def validate_colour_scheme(self, colour_scheme_in):
        if colour_scheme_in is None or not isinstance(colour_scheme_in, dict):
            colour_scheme_in = {}
        if self.code_empty not in colour_scheme_in:
            colour_scheme_in.update({self.code_empty: rgb_to_hex(WHITE)})
        if self.code_wall not in colour_scheme_in:
            colour_scheme_in.update({self.code_wall: rgb_to_hex(BLACK)})
        if self.code_start not in colour_scheme_in:
            colour_scheme_in.update({self.code_start: rgb_to_hex(LIMEGREEN)})
        if self.code_goal not in colour_scheme_in:
            colour_scheme_in.update({self.code_goal: rgb_to_hex(RED)})
        if self.code_path not in colour_scheme_in:
            colour_scheme_in.update({self.code_path: rgb_to_hex(ORANGE)})
        if self.code_visited not in colour_scheme_in:
            colour_scheme_in.update({self.code_visited: rgb_to_hex(FORESTGREEN)})
        if self.code_visited_plus not in colour_scheme_in:
            colour_scheme_in.update({self.code_visited_plus: rgb_to_hex((222, 117, 222))})
        return colour_scheme_in

    def reset_maze(self, force=False):
        if self.solving.get() and not force:
            raise ValueError("Error cannot reset this grid while solving")
        for i in range(self.h):
            for j in range(self.w):
                colour = self.og_cell_colours[i][j]
                self.itemconfigure(self.cells[i][j], fill=colour)
                self.traversed_values[i][j] = 0
        self.current.set(self.start_pos)

    def surrounding(self, ci, cj, direction=None):

        mi_i = clamp(0, ci - 1, self.h)
        ma_i = clamp(0, ci + 1, self.h)
        mi_j = clamp(0, cj - 1, self.w)
        ma_j = clamp(0, cj + 1, self.w)

        n = (mi_i, cj)
        e = (ci, ma_j)
        s = (ma_i, cj)
        w = (ci, mi_j)

        circle = [
            ((i, j), self.grid_lines[i][j])
            for i, j in [w, s, e, n]
        ]

        if direction == "e":
            circle = circle[1:] + circle[:1]
        elif direction == "n":
            circle = circle[2:] + circle[:2]
        elif direction == "w":
            circle = circle[3:] + circle[:3]

        circle = [(*circ, idx) for idx, circ in enumerate(circle)]

        # circle = [
        #     ((ci, mi_j), self.grid_lines[ci][mi_j], 0),
        #     ((ma_i, cj), self.grid_lines[ma_i][cj], 1),
        #     ((ci, ma_j), self.grid_lines[ci][ma_j], 2),
        #     ((mi_i, cj), self.grid_lines[mi_i][cj], 3)
        # ]
        #
        # if direction == "n":
        #     circle = [
        #         ((ci, ma_j), self.grid_lines[ci][ma_j], 0),
        #         ((mi_i, cj), self.grid_lines[mi_i][cj], 1),
        #         ((ci, mi_j), self.grid_lines[ci][mi_j], 2),
        #         ((ma_i, cj), self.grid_lines[ma_i][cj], 3)
        #     ]
        # elif direction == "e":
        #     circle = [
        #         ((ma_i, cj), self.grid_lines[ma_i][cj], 0),
        #         ((ci, ma_j), self.grid_lines[ci][ma_j], 1),
        #         ((mi_i, cj), self.grid_lines[mi_i][cj], 2),
        #         ((ci, mi_j), self.grid_lines[ci][mi_j], 3)
        #     ]
        # elif direction == "w":
        #     circle = [
        #         ((mi_i, cj), self.grid_lines[mi_i][cj], 0),
        #         ((ci, mi_j), self.grid_lines[ci][mi_j], 1),
        #         ((ma_i, cj), self.grid_lines[ma_i][cj], 2),
        #         ((ci, ma_j), self.grid_lines[ci][ma_j], 3)
        #     ]


        # circle = [k for k, v in circle.items() if k != (ci, cj) and v != self.code_wall]
        circle = [(k, p) for k, v, p in circle if k != (ci, cj) and v != self.code_wall]
        # print(f"{circle=}")

        return circle

        # print(f"\n({ci}, {cj}), i: ({mi_i}, {ma_i}), j: ({mi_j}, {ma_j})")
        # print(f"{self.grid_lines[mi_i: ma_i]=}")
        # # print(f"{self.grid_lines[mi_i: ma_i]=}")
        # circle = flatten([[(i, j) for j, char in enumerate(row[mi_j: ma_j]) if char != self.code_wall] for i, row in enumerate(self.grid_lines[mi_i: ma_i])])
        # # if circle:
        # #     print(f"{circle=}")
        # #     circle.remove((ci, cj))
        # return circle

    def iter_right_hand(self):
        print(f"{'#' * 120}")
        max_times = 3
        ci, cj = self.current.get()
        circle = self.surrounding(ci, cj, direction=self.traverse_direction.get())
        if not circle:
            raise ValueError("Error, nowhere to go!")

        # circle.sort(key=lambda tup: self.traversed_values[tup[0]][tup[1]])
        circle.sort(key=lambda tup: (self.traversed_values[tup[0][0]][tup[0][1]], tup[1]))        # circle.sort(key=lambda tup: (-tup[0], self.traversed_values[tup[0]][tup[1]]))
        # circle.sort(key=lambda tup: (-tup[0]))
        print(f"\tSorted: {ci=}, {cj=}\n{self.traverse_direction.get()=}\n{circle=}\n{[self.traversed_values[tup[0][0]][tup[0][1]] for tup in circle]}")
        next_move, rank = circle.pop(0)

        if next_move == (ci, cj) and len(circle) > 0:
            print(f"\tdouble pop")
            next_move, rank = circle.pop(0)
        print(f"{next_move=}")

        nmi, nmj = next_move
        if nmi < ci:
            self.traverse_direction.set("n")
        else:
            if nmj < cj:
                self.traverse_direction.set("w")
            elif nmj > cj:
                self.traverse_direction.set("e")
            else:
                self.traverse_direction.set("s")

        visited = self.traversed_values[ci][cj]
        if visited == 0:
            colour = self.colour_scheme[self.code_visited]
        else:
            colour = gradient(min(visited, max_times), max_times, self.colour_scheme[self.code_visited], self.colour_scheme[self.code_visited_plus], rgb=False)
        self.itemconfigure(self.cells[ci][cj], fill=colour)

        # old_colour = self.itemcget(self.cells[ci][cj], "fill")
        # self.itemconfigure(self.cells[ci][cj], fill=darken(old_colour, 0.25, rgb=False))

        self.traversed_values[ci][cj] += 1
        ci, cj = next_move
        self.current.set((ci, cj))

        if (ci, cj) == self.goal_pos:
            self.solved.set(True)
        else:
            self.after(150, self.iter_right_hand)
        # for i in range(self.h):
        #     for j in range(self.w):

    def solve_right_hand(self):
        print(f"solving by right hand method.")
        self.current.set(self.start_pos)
        self.traversed_values[self.start_pos[0]][self.start_pos[1]] = 1
        self.iter_right_hand()

        # while not self.solved.get():
        #     x = self.after(200, self.iter_right_hand, ci, cj)
        #     print(f"{x=}")

    def solve(self, algorithm: Literal["Right-Hand"]="Right-Hand"):
        self.reset_maze()
        self.solving.set(True)
        if algorithm == "Right-Hand":
            self.solve_right_hand()
        self.solved.set(True)
        self.solving.set(False)


def reset_maze():
    try:
        g1.reset_maze()
    except ValueError:
        print(f"Failed to reset this maze.")


def solve_maze():
    if not g1.solving.get():
        g1.solve()


if __name__ == '__main__':

    win = tkinter.Tk()
    win.geometry(f"800x800")
    # g1 = Grid(win, r"maze_1.txt")
    g1 = Grid(win, r"maze_3.txt")

    tv_btn_reset, btn_reset = button_factory(win, tv_btn="reset", kwargs_btn={"command": reset_maze})
    tv_btn_solve, btn_solve = button_factory(win, tv_btn="solve", kwargs_btn={"command": solve_maze})

    g1.pack()
    btn_reset.pack()
    btn_solve.pack()

    # win.after(3000, g1.solve)

    win.mainloop()

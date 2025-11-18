from typing import Any
import pandas as pd
import numpy as np
import streamlit as st


class Nonogram:

    BLANK: str = " "
    MARK: str = "X"
    NOTE: str = "*"

    def verify_grid(hints) -> bool | Exception:
        if not isinstance(hints, dict):
            return ValueError(f"hints must be a dict, got {type(hints)=}")
        r_hints = hints.get("r_hints", [])
        c_hints = hints.get("c_hints", [])
        if not c_hints:
            return ValueError(f"hints must contain {c_hints=}")
        if not r_hints:
            return ValueError(f"hints must contain {r_hints=}")
        for rh in r_hints:
            if not isinstance(rh, list):
                return ValueError(f"r_hints must be a list of integers, got {r_hints=}")
            for rh_v in rh:
                if not isinstance(rh_v, int):
                    return ValueError(f"r_hints must be a list of integers, got {r_hints=}")
        for ch in c_hints:
            if not isinstance(ch, list):
                return ValueError(f"c_hints must be a list of integers, got {c_hints=}")
            for ch_v in ch:
                if not isinstance(ch_v, int):
                    return ValueError(f"c_hints must be a list of integers, got {c_hints=}")
        return True

    def fillna(grid: list[list[int]], r_hints: list[list[int]], c_hints: list[list[int]]) -> list[list[int]]:
        for i, rh in enumerate(r_hints):
            if rh == [0]:
                for gi in range(len(grid)):
                    grid[i][gi] = Nonogram.NOTE
        for i, ch in enumerate(c_hints):
            if ch == [0]:
                for gi in range(len(grid[i])):
                    grid[gi][i] = Nonogram.NOTE
        return grid

    def mark(row: list[str], hints: list[int], is_row: bool = True):
        note_sep = Nonogram.note_separated(row)
        st.write(f"{note_sep=}")
        for i, sep_space in enumerate(note_sep):
            for j, hint in enumerate(hints):
                space = sep_space - (sum([v for jj, v in enumerate(hints) if jj != j]) + (len(hints) - 1))
                buffer = space - hint
                space_to_mark = hint - buffer
                if space_to_mark > 0:
                    start_pos = sum(hints[:j]) + len(hints[:j]) + buffer #+ int(bool(j))
                    st.write(f"{i=}, {j=}, {sep_space=}, {hint=}, {space=}, {buffer=}, {space_to_mark=}, {start_pos=}")
                    for ii in range(start_pos, start_pos + space_to_mark):
                        row[ii] = Nonogram.MARK
                    if space_to_mark == hint:
                        if (start_pos + space_to_mark) < (len(row) - 1):
                            row[start_pos + space_to_mark] = Nonogram.NOTE

    def note_separated(lst: list[int]) -> list[int]:
        res = []
        cnt = 0
        for i, val in enumerate(lst):
            if val == Nonogram.NOTE:
                res.append(cnt)
                cnt = 0
            else:
                cnt += 1

        if cnt > 0:
            res.append(cnt)

        return res

    def to_string(grid: list[list[int]], r_hints: list[list[int]], c_hints: list[list[int]]) -> str:
        max_h_c_hints = max([len(hc) for hc in c_hints])
        max_w_r_hints = max([len(hr) for hr in r_hints])
        n_rows = len(grid)
        n_cols = len(grid[0])
        space_left = (max_h_c_hints * 2) + 1
        res = " " * space_left

        # column hints
        for i in range(max_h_c_hints):
            for hj, hc in enumerate(c_hints):
                # st.write(f"{i=}, {hj=}, {hc=}, {max_h_c_hints=}")
                if i >= (max_h_c_hints - len(hc)):
                    idx = len(hc) - (max_h_c_hints - (i + 1)) - 1
                    # st.write(f"{idx=}")
                    res += str(hc[idx]).center(2, Nonogram.BLANK)
                else:
                    res += Nonogram.BLANK.center(2, Nonogram.BLANK)
            res += "\n"
            if i < (max_h_c_hints - 1):
                res += (" " * space_left)

        # row hints and grid 1 row at a time
        for i in range(n_rows):
            r_hints_c = ([Nonogram.BLANK.center(2, Nonogram.BLANK) for _ in range(max_w_r_hints)] + r_hints[i])[-max_h_c_hints:]
            res += "".join(list(map(lambda v: str(v).center(2, Nonogram.BLANK), r_hints_c)))
            res += Nonogram.BLANK
            res += "".join(list(map(lambda v: str(v).center(2, Nonogram.BLANK), grid[i])))
            res += "\n"

        return res


    def __init__(self, hints: dict[str: Any]):

        self.hints_og = hints.copy()
        v_grid = Nonogram.verify_grid(hints)
        if isinstance(v_grid, Exception):
            raise v_grid
        self.hints = hints.copy()

        self.r_hints: list[list[int]] = hints.get("r_hints")
        self.c_hints: list[list[int]] = hints.get("c_hints")
        self.n_rows = len(self.r_hints)
        self.n_cols = len(self.c_hints)

        self.grid_blank = [[Nonogram.BLANK for _ in range(self.n_cols)] for _ in range(self.n_rows)]
        self.grid_solved = None
        self.grid_working = self.grid_blank.copy()

        self.solve(resolve=True)

    # def count_marks(self) -> int:

    def reset(self):
        self.grid_working = self.grid_blank.copy()

    def solve(self, resolve=True):
        if resolve:
            self.reset()

        if self.solved:
            return

        self.grid_working = Nonogram.fillna(self.grid_working, self.r_hints, self.c_hints)

        r_hints = self.r_hints
        c_hints = self.c_hints
        grid_w = self.grid_working.copy()
        grid_t = self.grid_working.copy()
        t_passes = 0
        passes = 0
        while passes <= 2:
            passes += 1
            t_passes += 1

            for i, row_r_hint in enumerate(zip(grid_w, r_hints)):
                row, r_hint = row_r_hint
                st.write(f"{i=}, {row=}, {r_hint=}")
                Nonogram.mark(row, r_hint, is_row=True)
                
            t_grid_w = np.transpose(grid_w).tolist()
            tt_grid_w = []
            for j, col_c_hint in enumerate(zip(t_grid_w, c_hints)):
                col, c_hint = col_c_hint
                st.write(f"A {j=}, {col=}, {c_hint=}")
                Nonogram.mark(col, c_hint, is_row=False)
                st.write(f"B {j=}, {col=}, {c_hint=}")
                tt_grid_w.append(col)

            grid_w = np.transpose(tt_grid_w).tolist()

            #     lst_r = grid_w[i]
            #     lst_r_note_sep = Nonogram.note_separated(lst_r)
            #     for j in range(len(grid_w[i])):
            #         lst_c = [grid_w[ii][j] for ii in range(len(grid_w))]
            #         lst_c_note_sep = Nonogram.note_separated(lst_c)
            #         hints_ri = self.r_hints[i]
            #         hints_cj = self.c_hints[j]
            #         # st.write(f"\n{i=}, {j=}\n{lst_r=}, {lst_r_note_sep=}, {hints_ri=}\n{lst_c=}, {lst_c_note_sep=}, {hints_cj=}")

            #         for i in range(len(grid_w)):
            #             lst_r = grid_w[i]
            #             lst_r_note_sep = Nonogram.note_separated(lst_r)
            #             for j in range(len(grid_w[i])):
            #                 lst_c = [grid_w[ii][j] for ii in range(len(grid_w))]
            #                 lst_c_note_sep = Nonogram.note_separated(lst_c)
            #                 hints_ri = self.r_hints[i]
            #                 hints_cj = self.c_hints[j]
            #                 st.write(f"\n{t_passes=}, {passes=}, {i=}, {j=}\n{lst_r=}, {lst_r_note_sep=}, {hints_ri=}\n{lst_c=}, {lst_c_note_sep=}, {hints_cj=}")

            #                 for hi, hr in enumerate(hints_ri):
            #                     for ns_i, ns_r in enumerate(lst_r_note_sep):
            #                         if (ns_r // 2) <= hr:
            #                             stp = ns_r - hr
            #                             stm = hr - stp
            #                             start = sum(lst_r_note_sep[:ns_i]) + len(lst_r_note_sep[:ns_i]) + stp
            #                             st.write(f"\t{stm=}, {stp=}, {start=}")

            #                             for gi in range(start, start + stm):
            #                                 grid_w[i][gi] = Nonogram.MARK

            #                 for hj, hc in enumerate(hints_cj):
            #                     for ns_j, ns_c in enumerate(lst_c_note_sep):
            #                         if (ns_c // 2) <= hc:
            #                             stp = ns_c - hc
            #                             stm = hc - stp
            #                             start = sum(lst_c_note_sep[:ns_j]) + len(lst_c_note_sep[:ns_j]) + stp
            #                             st.write(f"\t{stm=}, {stp=}, {start=}")

            #                             for gj in range(start, start + stm):
            #                                 grid_w[gj][j] = Nonogram.MARK

            #         # # place middle of blocks
            #         # for hi, hr in enumerate(hints_ri):
            #         #     for ns_i, ns_r in enumerate(lst_r_note_sep):
            #         #         if (ns_r // 2) <= hr:
            #         #             stp = ns_r - hr
            #         #             stm = hr - stp
            #         #             start = sum(lst_r_note_sep[:ns_i]) + len(lst_r_note_sep[:ns_i]) + stp
            #         #             # print(f"\t{stm=}, {stp=}, {start=}")
            #         #
            #         #             for gi in range(start, start + stm):
            #         #                 grid_w[i][gi] = Nonogram.MARK
            #         #
            #         # for hj, hc in enumerate(hints_cj):
            #         #     for ns_j, ns_c in enumerate(lst_c_note_sep):
            #         #         if (ns_c // 2) <= hc:
            #         #             stp = ns_c - hc
            #         #             stm = hc - stp
            #         #             start = sum(lst_c_note_sep[:ns_i]) + len(lst_c_note_sep[:ns_i]) + stp
            #         #             # print(f"\t{stm=}, {stp=}, {start=}")
            #         #
            #         #             for gj in range(start, start + stm):
            #         #                 grid_w[gj][j] = Nonogram.MARK
            #         #
            #         #
            #         #

            # st.write("A")
            # st.code(Nonogram.text_grid(grid_w))

            # for i in range(len(grid_w)):
            #     r_hints = self.r_hints[i]
            #     for j in range(len(grid_w[0])):
            #         c_hints = self.c_hints[j]
            #         val = grid_w[i][j]
            #         if val == Nonogram.MARK:
            #             if i == 0:
            #                 c_hint_0 = c_hints[0]
            #                 for k in range(c_hint_0):
            #                     grid_w[i][k] = Nonogram.MARK
            #                 grid_w[i][c_hint_0] = Nonogram.NOTE
            #             elif i == len(grid_w) - 1:
            #                 c_hint_0 = c_hints[-1]
            #                 for k in range(c_hint_0):
            #                     grid_w[i][-(k+1)] = Nonogram.MARK
            #                 grid_w[i][-(c_hint_0 + 1)] = Nonogram.NOTE


            # st.write("B")
            # st.code(Nonogram.text_grid(grid_w))

            if grid_w != grid_t:
                passes = 0
            grid_t = grid_w.copy()
            break
        # while passes <= 2:
        #     passes += 1
        #     t_passes += 1

        #     for i in range(len(grid_w)):
        #         lst_r = grid_w[i]
        #         lst_r_note_sep = Nonogram.note_separated(lst_r)
        #         for j in range(len(grid_w[i])):
        #             lst_c = [grid_w[ii][j] for ii in range(len(grid_w))]
        #             lst_c_note_sep = Nonogram.note_separated(lst_c)
        #             hints_ri = self.r_hints[i]
        #             hints_cj = self.c_hints[j]
        #             # st.write(f"\n{i=}, {j=}\n{lst_r=}, {lst_r_note_sep=}, {hints_ri=}\n{lst_c=}, {lst_c_note_sep=}, {hints_cj=}")

        #             for i in range(len(grid_w)):
        #                 lst_r = grid_w[i]
        #                 lst_r_note_sep = Nonogram.note_separated(lst_r)
        #                 for j in range(len(grid_w[i])):
        #                     lst_c = [grid_w[ii][j] for ii in range(len(grid_w))]
        #                     lst_c_note_sep = Nonogram.note_separated(lst_c)
        #                     hints_ri = self.r_hints[i]
        #                     hints_cj = self.c_hints[j]
        #                     st.write(f"\n{t_passes=}, {passes=}, {i=}, {j=}\n{lst_r=}, {lst_r_note_sep=}, {hints_ri=}\n{lst_c=}, {lst_c_note_sep=}, {hints_cj=}")

        #                     for hi, hr in enumerate(hints_ri):
        #                         for ns_i, ns_r in enumerate(lst_r_note_sep):
        #                             if (ns_r // 2) <= hr:
        #                                 stp = ns_r - hr
        #                                 stm = hr - stp
        #                                 start = sum(lst_r_note_sep[:ns_i]) + len(lst_r_note_sep[:ns_i]) + stp
        #                                 st.write(f"\t{stm=}, {stp=}, {start=}")

        #                                 for gi in range(start, start + stm):
        #                                     grid_w[i][gi] = Nonogram.MARK

        #                     for hj, hc in enumerate(hints_cj):
        #                         for ns_j, ns_c in enumerate(lst_c_note_sep):
        #                             if (ns_c // 2) <= hc:
        #                                 stp = ns_c - hc
        #                                 stm = hc - stp
        #                                 start = sum(lst_c_note_sep[:ns_j]) + len(lst_c_note_sep[:ns_j]) + stp
        #                                 st.write(f"\t{stm=}, {stp=}, {start=}")

        #                                 for gj in range(start, start + stm):
        #                                     grid_w[gj][j] = Nonogram.MARK

        #             # # place middle of blocks
        #             # for hi, hr in enumerate(hints_ri):
        #             #     for ns_i, ns_r in enumerate(lst_r_note_sep):
        #             #         if (ns_r // 2) <= hr:
        #             #             stp = ns_r - hr
        #             #             stm = hr - stp
        #             #             start = sum(lst_r_note_sep[:ns_i]) + len(lst_r_note_sep[:ns_i]) + stp
        #             #             # print(f"\t{stm=}, {stp=}, {start=}")
        #             #
        #             #             for gi in range(start, start + stm):
        #             #                 grid_w[i][gi] = Nonogram.MARK
        #             #
        #             # for hj, hc in enumerate(hints_cj):
        #             #     for ns_j, ns_c in enumerate(lst_c_note_sep):
        #             #         if (ns_c // 2) <= hc:
        #             #             stp = ns_c - hc
        #             #             stm = hc - stp
        #             #             start = sum(lst_c_note_sep[:ns_i]) + len(lst_c_note_sep[:ns_i]) + stp
        #             #             # print(f"\t{stm=}, {stp=}, {start=}")
        #             #
        #             #             for gj in range(start, start + stm):
        #             #                 grid_w[gj][j] = Nonogram.MARK
        #             #
        #             #
        #             #

        #     st.write("A")
        #     st.code(Nonogram.text_grid(grid_w))

        #     for i in range(len(grid_w)):
        #         r_hints = self.r_hints[i]
        #         for j in range(len(grid_w[0])):
        #             c_hints = self.c_hints[j]
        #             val = grid_w[i][j]
        #             if val == Nonogram.MARK:
        #                 if i == 0:
        #                     c_hint_0 = c_hints[0]
        #                     for k in range(c_hint_0):
        #                         grid_w[i][k] = Nonogram.MARK
        #                     grid_w[i][c_hint_0] = Nonogram.NOTE
        #                 elif i == len(grid_w) - 1:
        #                     c_hint_0 = c_hints[-1]
        #                     for k in range(c_hint_0):
        #                         grid_w[i][-(k+1)] = Nonogram.MARK
        #                     grid_w[i][-(c_hint_0 + 1)] = Nonogram.NOTE


        #     st.write("B")
        #     st.code(Nonogram.text_grid(grid_w))

        #     if grid_w != grid_t:
        #         passes = 0
        #     grid_t = grid_w.copy()
        self.grid_working = grid_w

    def text_grid(self):
        return Nonogram.to_string(self.grid_working, self.r_hints, self.c_hints)

    def __repr__(self):
        return f"Nonogram({self.n_rows}x{self.n_cols})"

    def get_solved(self) -> bool:
        return self.grid_working == self.grid_solved

    def set_solved(self, solved_in):
        pass

    def del_solved(self):
        pass

    solved = property(get_solved, set_solved, del_solved)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    # Nonogram
    p0 = {
        "c_hints": [
            [6, 2],
            [5, 1, 1, 2],
            [5, 3, 1],
            [1, 3, 1, 1, 1],
            [2, 3, 3, 1],
            [2, 3, 1, 1, 1],
            [2, 4, 1, 1, 1],
            [2, 5, 1, 1, 1],
            [5, 2, 1, 1, 1],
            [7, 2, 1, 1],
            [4, 1, 3, 1],
            [6, 1, 1, 1],
            [6, 3, 1],
            [7, 1, 1, 1],
            [10, 3]
        ],
        "r_hints": [
            [4, 2],
            [10],
            [2, 7],
            [4, 8],
            [3, 9],
            [8, 1, 4],
            [15],
            [9, 1],
            [1, 1, 1],
            [15],
            [1, 1, 1, 1],
            [15],
            [1, 1],
            [1, 1],
            [13]
        ]
    }

    n0 = Nonogram(p0)
    st.write(n0)
    st.write(n0.grid_working)
    st.write(n0.r_hints)
    st.write(n0.c_hints)
    df_gw = pd.DataFrame(n0.grid_working)
    st.write(df_gw)
    st.code(n0.text_grid())
    st.code(Nonogram.to_string(np.transpose(n0.grid_working).tolist(), n0.r_hints, n0.c_hints))
from typing import Any, Optional, Literal
import pandas as pd
import numpy as np
import streamlit as st
import datetime
import asyncio
import time
from utility import percent
from datetime_utility import time_between


class Nonogram:

    BLANK: str = " "
    MARK: str = "X"
    NOTE: str = "*"
    WRONG: str = "%"
    MISSING: str = "_"

    def verify_grid(hints) -> bool | Exception:
        if not isinstance(hints, dict):
            return ValueError(f"hints must be a dict, got {type(hints)=}")
        r_hints = hints.get("r_hints", [])
        c_hints = hints.get("c_hints", [])
        answer = hints.get("answer", [])
        if not c_hints:
            return ValueError(f"hints must contain {c_hints=}")
        if not r_hints:
            return ValueError(f"hints must contain {r_hints=}")
        for rh in r_hints:
            if not isinstance(rh, list):
                return ValueError(f"r_hints must be a list of integers, got {r_hints=}")
            if not rh:
                return ValueError(f"r_hints must be a list of integers, got {r_hints=}")
            for rh_v in rh:
                if not isinstance(rh_v, int):
                    return ValueError(f"r_hints must be a list of integers, got {r_hints=}")
        for ch in c_hints:
            if not isinstance(ch, list):
                return ValueError(f"c_hints must be a list of integers, got {c_hints=}")
            if not ch:
                return ValueError(f"c_hints must be a list of integers, got {c_hints=}")
            for ch_v in ch:
                if not isinstance(ch_v, int):
                    return ValueError(f"c_hints must be a list of integers, got {c_hints=}")
        if answer:
            if (len(answer) != len(r_hints)) or (len(answer[0]) != len(c_hints)):
                return ValueError(f"answer does not match r_hints or c_hints dimensions, {len(answer)=}, {len(r_hints)=}")
            clean_ans = []
            for i, row in enumerate(answer):
                clean_row = []
                for j, val in enumerate(row):
                    if val in [1, "1", Nonogram.MARK]:
                        clean_row.append(Nonogram.MARK)
                    elif val in [0, "0", " ", "", Nonogram.BLANK]:
                        clean_row.append(Nonogram.BLANK)
                    elif val in [Nonogram.NOTE]:
                        clean_row.append(Nonogram.NOTE)
                    else:
                        return ValueError(f"invalid character in answer {i=}, {j=}, {val=}")
                clean_ans.append(clean_row)
            
            # st.write(f"clean_ans")
            # st.write(clean_ans)
            
            hints["answer"] = clean_ans
        else:
            hints["answer"] = None
                        
        return True

    def fillna(grid: list[list[str]], r_hints: list[list[int]], c_hints: list[list[int]]) -> list[list[int]]:
        for i, rh in enumerate(r_hints):
            if rh == [0]:
                for gi in range(len(c_hints)):
                    grid[i][gi] = Nonogram.NOTE
        for i, ch in enumerate(c_hints):
            if ch == [0]:
                for gi in range(len(r_hints)):
                    grid[gi][i] = Nonogram.NOTE
        return grid

    def mark(row: list[str], hints: list[int], is_row: bool = True, parent_cont = None):

        sum_hints = sum(hints)
        sum_marks = row.count(Nonogram.MARK)
        note_sep = Nonogram.note_separated(row)

        if sum_marks < sum_hints:

            hints_l = hints.copy()
            with parent_cont if parent_cont is not None else st.container():
                st.write(f"IN  {note_sep=}, {row=}, {hints=}")
                st.code(Nonogram.to_string([row], r_hints=[hints]))
            if len(note_sep) > 1:
                idx_first_mark = 0 + (row.index(Nonogram.MARK) if Nonogram.MARK in row else (row.index(Nonogram.BLANK) if Nonogram.BLANK in row else 0))
            else:
                idx_first_mark = row.index(Nonogram.BLANK) if Nonogram.BLANK in row else 0

            # idx_first_mark = min(row.index(Nonogram.MARK) if Nonogram.MARK in row else 0, row.index(Nonogram.BLANK) if Nonogram.BLANK in row else 0)
            for i, sep_space in enumerate(note_sep):
                hints_to_remove = []
                for j, hint in enumerate(hints_l):
                    space = sep_space - (sum([v for jj, v in enumerate(hints_l) if jj != j]) + (len(hints_l) - 1))
                    buffer = space - hint
                    space_to_mark = hint - buffer

                    if (hint != 0) and (row[:idx_first_mark].count(Nonogram.MARK) == hint):
                        idx_first_mark += 1
                        row[idx_first_mark] = Nonogram.BLANK

                    elif hint - space_to_mark > 0:
                        # start_pos = sum(hints_l[:j]) + len(hints_l[:j]) + buffer #+ int(bool(j))
                        start_pos = sum(hints_l[:j]) + len(hints_l[:j]) + buffer + idx_first_mark
                        # TODO startpos is off by left or right most notes.
                        cc = Nonogram.count_continuous(row, idx=start_pos)
                        with parent_cont if parent_cont is not None else st.container():
                            st.write(f"MA {i=}, {j=}, {sep_space=}, {hint=}, {space=}, {buffer=}, {space_to_mark=}, {start_pos=}, {idx_first_mark=}, {cc=}")
                        for ii in range(start_pos, start_pos + space_to_mark):
                            row[ii] = Nonogram.MARK
                        if space_to_mark == hint:
                            if (start_pos + space_to_mark) < (len(row) - 1):
                                row[start_pos + space_to_mark] = Nonogram.NOTE
                        hints_to_remove.append(j)
                    elif hint == space_to_mark:
                        # start_pos = sum(hints_l[:j]) + len(hints_l[:j]) + buffer + (idx_first_mark - hint)
                        start_pos = sum(hints_l[:j]) + len(hints_l[:j]) + buffer + idx_first_mark
                        cc = Nonogram.count_continuous(row, idx=start_pos)
                        with parent_cont if parent_cont is not None else st.container():
                            st.write(f"MB {i=}, {j=}, {sep_space=}, {hint=}, {space=}, {buffer=}, {space_to_mark=}, {start_pos=}, {idx_first_mark=}, {cc=}")
                        for ii in range(start_pos, start_pos + space_to_mark):
                            row[ii] = Nonogram.MARK

                for jj in hints_to_remove[::-1]:
                    del hints_l[jj]
                if hints_to_remove:
                    break
        else:
            for j in range(len(row)):
                val = row[j]
                if val != Nonogram.MARK:
                    row[j] = Nonogram.NOTE
            
        with parent_cont if parent_cont is not None else st.container():
            st.write(f"OUT {note_sep=}, {row=}, {hints=}")

        # i = 0
        # while i < len(row):
        #     i += 1

    def edge_in(row: list[str], hints: list[int], parent_cont=None):
        # forward to backward
        found_hint = None
        h0 = hints[0]
        cnt_marks = 0
        for i, val in enumerate(row):
            if (found_hint is None) and (val == Nonogram.MARK):
                found_hint = i
            # col_debug.write(f"FtB {i=}, {val=}, {h0=}, {found_hint=}, {cnt_marks=}")
            if found_hint is not None:
                if val == Nonogram.BLANK:
                    if (h0 - (i + 0)) > 0:
                        row[i] = Nonogram.MARK
                        with parent_cont if parent_cont is not None else st.container():
                            st.write(f"FtB_a {i=}, {val=}, {h0=}, {found_hint=}, {cnt_marks=}")
                            st.write(f"-- {i=} MARK ftb")
                        cnt_marks += 1
                    # # else:
                    # #     row[i] = Nonogram.NOTE
                    # #     if ((h0 - i) == 0) and (cnt_marks == h0):
                    # #         with parent_cont if parent_cont is not None else st.container():
                    # #             st.write(f"FtB_b {i=}, {val=}, {h0=}, {found_hint=}, {cnt_marks=}")
                    # #             st.write(f"-- {i=} NOTE ftb")
                    # #         break
                    # elif ((h0 - i) == 0) and (cnt_marks == h0):
                    #     row[i] = Nonogram.NOTE
                    #     with parent_cont if parent_cont is not None else st.container():
                    #         st.write(f"FtB_b {i=}, {val=}, {h0=}, {found_hint=}, {cnt_marks=}")
                    #         st.write(f"-- {i=} NOTE ftb")
                    #     break
                elif val == Nonogram.MARK:
                    cnt_marks += 1
            
        # backward to forward
        h_1 = hints[-1]
        found_hint = None
        cnt_marks = 0
        for i, val in enumerate(row[::-1]):
            if (found_hint is None) and (val == Nonogram.MARK):
                found_hint = i
            # st.write(f"BtF {i=}, {val=}, {h_1=}, {found_hint=}, {cnt_marks=}")
            if found_hint is not None:
                if val == Nonogram.BLANK:
                    if (h_1 - (i + 0)) > 0:
                        row[len(row) - (i + 1)] = Nonogram.MARK
                        with parent_cont if parent_cont is not None else st.container():
                            st.write(f"BtF_a {i=}, {val=}, {h_1=}, {found_hint=}, {cnt_marks=}")
                            st.write(f"-- i={len(row) - (i + 1)} MARK btf")
                        cnt_marks += 1
                    # elif ((h_1 - (i + 0)) == 0) and (cnt_marks == h_1):
                    #     row[len(row) - (i + 1)] = Nonogram.NOTE
                    #     with parent_cont if parent_cont is not None else st.container():
                    #         st.write(f"BtF_b {i=}, {val=}, {h_1=}, {found_hint=}, {cnt_marks=}")
                    #         st.write(f"-- i={len(row) - (i + 1)} NOTE btf")
                    #     break
                elif val == Nonogram.MARK:
                    cnt_marks += 1

    def fill_smalls(row: list[str], hints: list[int], parent_cont=None):
        small_hint = min(hints)
        for i in range(len(row)):
            val = row[i]
            c_val, val_idxs = Nonogram.count_continuous(row, m=val, idx=i)
            with parent_cont if parent_cont is not None else st.container():
                st.write(f"{i=}, {val=}, {c_val=}, {small_hint=}, {val_idxs=}")
            if c_val < small_hint:
                for idx in val_idxs:
                    row[idx] = Nonogram.NOTE

    def note_separated(lst: list[int]) -> list[int]:
        res = []
        cnt = 0
        for i, val in enumerate(lst):
            if val == Nonogram.NOTE:
                if (cnt != 0) and (len(res) != 0):
                    res.append(cnt)
                cnt = 0
            else:
                cnt += 1

        if cnt > 0:
            res.append(cnt)

        if not res:
            res = [0]

        return res

    def count_continuous(row: list[int], m: Optional[str] = None, idx: Optional[int] = None, direction: Literal["left", "right", None] = None) -> tuple[int, list[int]]:
        # st.write(f"CC {row=}, {m=}, {idx=}, {direction=}")
        if m is None:
            m = Nonogram.MARK
        
        if idx is None:
            idx = 0

        if idx < 0:
            # st.write(f"idx < 0")
            return 0, []
        elif idx >= len(row):
            # st.write(f"idx >= len(row)")
            return 0, []

        if row[idx] != m:
            # st.write(f"row[idx] != m")
            return 0, []

        if direction is None:
            left_s, left_i = Nonogram.count_continuous(row, m, idx - 1, "left")
            right_s, right_i = Nonogram.count_continuous(row, m, idx + 1, "right")
        else:
            left_s, left_i = (0, []) if direction == "right" else Nonogram.count_continuous(row, m, idx - 1, "left")
            right_s, right_i = (0, []) if direction == "left" else Nonogram.count_continuous(row, m, idx + 1, "right")

        # st.write(f"left={left}, right={right}, +1")
        return left_s + 1 + right_s, list(set(left_i).union(set(right_i)).union(set([idx])))
    
    def gen_horizontal_hints(grid: list[list[str]]) -> list[list[int]]:
        rows = len(grid)
        cols = len(grid[0])
        res = [[] for i in range(rows)]
        for r in range(rows):
            for c in range(cols):
                if (grid[r][c] == 1 and c == 0) or (grid[r][c] == 1 and grid[r][c - 1] == 0):
                    count = 1
                    temp = c
                    while temp < cols - 1 and grid[r][temp + 1] == 1:
                        count += 1
                        temp += 1
                    res[r].append(count)
        for r in range(rows):
            if len(res[r]) == 0:
                res[r] = [0]
        # print('h_hints', res)
        return res

    def gen_vertical_hints(grid: list[list[str]]) -> list[list[int]]:
        rows = len(grid)
        cols = len(grid[0])
        res = [[] for i in range(cols)]
        for r in range(rows):
            for c in range(cols):
                if (grid[r][c] == 1 and r == 0) or (grid[r][c] == 1 and grid[r - 1][c] == 0):
                    temp = r
                    count = 1
                    while (r < rows - 1) and (grid[r + 1][c] == 1):
                        count += 1
                        r += 1
                    r = temp
                    res[c].append(count)
        for c in range(cols):
            if len(res[c]) == 0:
                res[c] = [0]
        # print('v_hints', res)
        return res

    def to_string(
        grid: list[list[str]],
        r_hints: Optional[list[list[int]]] = None,
        c_hints: Optional[list[list[int]]] = None,
        answer: Optional[list[list[int]]] = None
    ) -> str:
        n_rows = len(grid)
        n_cols = len(grid[0])
        res = ""
        max_w_r_hints = 0 if r_hints is None else max([len(hr) for hr in r_hints])

        if c_hints is not None:
            max_h_c_hints = max([len(hc) for hc in c_hints])
            space_left = (max_w_r_hints * 2) + 1
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
        else:
            max_h_c_hints = 0

        # row hints and grid 1 row at a time
        for i in range(n_rows):
            if r_hints is not None:
                r_hints_c = ([Nonogram.BLANK.center(2, Nonogram.BLANK) for _ in range(max_w_r_hints)] + r_hints[i])[-max_w_r_hints:]
                res += "".join(list(map(lambda v: str(v).center(2, Nonogram.BLANK), r_hints_c)))
            res += Nonogram.BLANK
            for j, val in enumerate(grid[i]):
                if answer is not None:
                    if val == answer[i][j]:
                        res += val.center(2, Nonogram.BLANK)
                    else:
                        if val == Nonogram.MARK:
                            res += Nonogram.WRONG.center(2, Nonogram.BLANK)
                        elif answer[i][j] == Nonogram.MARK:
                            res += Nonogram.MISSING.center(2, Nonogram.BLANK)
                        else:
                            res += val.center(2, Nonogram.BLANK)
                else:
                    res += val.center(2, Nonogram.BLANK)
            # res += "".join(list(map(lambda v: str(v).center(2, Nonogram.BLANK), grid[i])))
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
        
        self.answer: list[list[int]] = hints.get("answer")

        self.grid_blank = [[Nonogram.BLANK for _ in range(self.n_cols)] for _ in range(self.n_rows)]
        self.grid_solved = None
        self.grid_working = self.grid_blank.copy()

        col_debug.write(f"-AA BK")
        col_debug.write(self.grid_blank)
        col_debug.write(f"-AA SV")
        col_debug.write(self.grid_solved)
        col_debug.write(f"-AA GW")
        col_debug.write(self.grid_working)

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

            col_debug.divider()
            col_debug.write(f"{passes=}, {t_passes=}")

            exp_0 = col_debug.expander(f"Mark Rows Pass# {t_passes}")
            with exp_0:
                st.write(f"grid_w")
                st.write(grid_w)
                for i, row_r_hint in enumerate(zip(grid_w, r_hints)):
                    row, r_hint = row_r_hint
                    st.write(f"ROWS A {i=}, {row=}, {r_hint=}")
                    Nonogram.mark(row, r_hint, is_row=True, parent_cont=exp_0)
                    st.write(f"ROWS B {i=}, {row=}, {r_hint=}")

            col_debug.write("After Rows")
            col_debug.code(Nonogram.to_string(grid_w, r_hints=r_hints, c_hints=c_hints))
            col_debug.write(f"AA {grid_w[0]=}")
                
            t_grid_w = np.transpose(grid_w).tolist()
            tt_grid_w = []
            exp_1 = col_debug.expander(f"Mark Cols Pass# {t_passes}")
            with exp_1:
                for j, col_c_hint in enumerate(zip(t_grid_w, c_hints)):
                    col, c_hint = col_c_hint
                    st.write(f"COLS A {j=}, {col=}, {c_hint=}")
                    Nonogram.mark(col, c_hint, is_row=False, parent_cont=exp_1)
                    st.write(f"COLS B {j=}, {col=}, {c_hint=}")
                    tt_grid_w.append(col)

            grid_w = np.transpose(tt_grid_w).tolist()
            col_debug.write("After Cols")
            col_debug.code(Nonogram.to_string(grid_w, r_hints=r_hints, c_hints=c_hints))

            exp_2 = col_debug.expander(f"Edge In Rows Pass# {t_passes}")
            with exp_2:
                for i, row_r_hint in enumerate(zip(grid_w, r_hints)):
                    row, r_hint = row_r_hint
                    st.write(f"EI ROW IN  {i=}, {row=}, {r_hint=}")
                    Nonogram.edge_in(row, r_hint, parent_cont=exp_2)
                    st.write(f"EI ROW OUT {i=}, {row=}, {r_hint=}")
            col_debug.write("After Edge In Rows")
            col_debug.code(Nonogram.to_string(grid_w, r_hints=r_hints, c_hints=c_hints))

            grid_w = np.transpose(grid_w).tolist()
            with col_debug.expander(f"Edge In Columns Pass# {t_passes}"):
                for i, row_c_hint in enumerate(zip(grid_w, c_hints)):
                    row, c_hint = row_c_hint
                    st.write(f"EI COL IN  {i=}, {row=}, {c_hint=}")
                    Nonogram.edge_in(row, c_hint)
                    st.write(f"EI COL OUT {i=}, {row=}, {c_hint=}")
            grid_w = np.transpose(grid_w).tolist()
            col_debug.write("After Edge In Cols")
            col_debug.code(Nonogram.to_string(grid_w, r_hints=r_hints, c_hints=c_hints))

            exp_3 = col_debug.expander(f"Fill In Smalls In Rows Pass# {t_passes}")
            with exp_3:
                for i, row_r_hint in enumerate(zip(grid_w, r_hints)):
                    row, r_hint = row_r_hint
                    st.write(f"FS ROW IN  {i=}, {row=}, {r_hint=}")
                    Nonogram.fill_smalls(row, r_hint, parent_cont=exp_3)
                    st.write(f"FS ROW OUT {i=}, {row=}, {r_hint=}")
            col_debug.write("After Fill In Smalls Rows")
            col_debug.code(Nonogram.to_string(grid_w, r_hints=r_hints, c_hints=c_hints))

            exp_4 = col_debug.expander(f"Fill In Smalls In Cols Pass# {t_passes}")
            grid_w = np.transpose(grid_w).tolist()
            with exp_4:
                for i, row_c_hint in enumerate(zip(grid_w, c_hints)):
                    row, c_hint = row_c_hint
                    st.write(f"FS ROW IN  {i=}, {row=}, {c_hint=}")
                    Nonogram.fill_smalls(row, c_hint, parent_cont=exp_4)
                    st.write(f"FS ROW OUT {i=}, {row=}, {c_hint=}")
            col_debug.write("After Fill In Smalls Cols")
            grid_w = np.transpose(grid_w).tolist()
            col_debug.code(Nonogram.to_string(grid_w, r_hints=r_hints, c_hints=c_hints))

            # for i, row_r_hint in enumerate(zip(grid_w, r_hints)):
            #     row, r_hint = row_r_hint
            #     need_marks = sum(r_hint)
            #     used_marks = row.count(Nonogram.MARK)
            #     st.write(f"{i=}, {row=}, {r_hint=}")
            #     if need_marks == used_marks:
            #         for j, val in enumerate(row):
            #             if val != Nonogram.MARK:
            #                 grid_w[i][j] = Nonogram.NOTE
            #     elif used_marks < need_marks:
            #         # Left to Right
            #         j = 0
            #         hint_v = r_hints[i][0]
            #         found_hint = False
            #         while j < len(row):
            #             if (row[j] == Nonogram.MARK) and (not found_hint):
            #                 found_hint = True
            #             if found_hint:
            #                 if row[j] == Nonogram.BLANK:
            #                     if j >= hint_v:
            #                         grid_w[i][j] = Nonogram.NOTE
            #                         break
            #                     else:
            #                         grid_w[i][j] = Nonogram.MARK
            #             j += 1

            #         # Right to Left
            #         j = len(row) - 1
            #         hint_v = r_hints[i][-1]
            #         found_hint = False
            #         while j >= 0:
            #             if (row[j] == Nonogram.MARK) and (not found_hint):
            #                 found_hint = True
            #             if found_hint:
            #                 if row[j] == Nonogram.BLANK:
            #                     if j >= hint_v:
            #                         grid_w[i][j] = Nonogram.NOTE
            #                         break
            #                     else:
            #                         grid_w[i][j] = Nonogram.MARK
            #             j -= 1
            #     # else:
            #     #     raise ValueError(f"Too many marks placed!")
            # st.write("After Row Edge Check")
            # st.code(Nonogram.to_string(grid_w, r_hints=r_hints, c_hints=c_hints))
            
            # grid_w = np.transpose(grid_w).tolist()
            # for i, row_r_hint in enumerate(zip(grid_w, c_hints)):
            #     row, r_hint = row_r_hint
            #     need_marks = sum(r_hint)
            #     used_marks = row.count(Nonogram.MARK)
            #     st.write(f"{i=}, {row=}, {r_hint=}")
            #     if need_marks == used_marks:
            #         for j, val in enumerate(row):
            #             if val != Nonogram.MARK:
            #                 grid_w[i][j] = Nonogram.NOTE
            #     elif used_marks < need_marks:
            #         # Top to Bottom
            #         j = 0
            #         hint_v = c_hints[i][0]
            #         found_hint = False
            #         while j < len(row):
            #             if (row[j] == Nonogram.MARK) and (not found_hint):
            #                 found_hint = True
            #             if found_hint:
            #                 if row[j] == Nonogram.BLANK:
            #                     if j >= hint_v:
            #                         grid_w[i][j] = Nonogram.NOTE
            #                         break
            #                     else:
            #                         grid_w[i][j] = Nonogram.MARK
            #             j += 1

            #         # Bottom to Top
            #         j = len(row) - 1
            #         hint_v = c_hints[i][-1]
            #         found_hint = False
            #         while j >= 0:
            #             if (row[j] == Nonogram.MARK) and (not found_hint):
            #                 found_hint = True
            #             if found_hint:
            #                 if row[j] == Nonogram.BLANK:
            #                     if j >= hint_v:
            #                         grid_w[i][j] = Nonogram.NOTE
            #                         break
            #                     else:
            #                         grid_w[i][j] = Nonogram.MARK
            #             j -= 1
            #     # else:
            #     #     raise ValueError(f"Too many marks placed!")
            

            # grid_w = np.transpose(grid_w).tolist()
            # st.write("After Row Edge Check")
            # st.code(Nonogram.to_string(grid_w, r_hints=r_hints, c_hints=c_hints))

            if grid_w != grid_t:
                passes = 0
            grid_t = grid_w.copy()
            # break
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

    def text_grid(self, show_answer: bool = False):
        return Nonogram.to_string(self.grid_working, self.r_hints, self.c_hints, answer=self.answer if show_answer and (self.answer is not None) else None)
    
    def st_grid(self):
        
        max_w_r_hints = 0 if self.r_hints is None else max([len(hr) for hr in self.r_hints])
        max_h_c_hints = max([len(hc) for hc in self.c_hints])
        grid = [st.columns(self.n_cols + max_w_r_hints) for _ in range(self.n_rows + max_h_c_hints + 1)]

        for i in range(max_h_c_hints - 1, -1, -1):
            for j, row in enumerate(self.c_hints):
                st.write(f"{i=}, {j=}, {row=}")
                if (len(row) - i) >= 0:
                    st.write(f" -> {i=}, {j=}, {row=}")
                    hint = self.c_hints[j][len(row) - (i + 1)]
                    with grid[max_h_c_hints - i][j + max_w_r_hints]:
                        # st.write(f"{hint}")
                        st.write(hint)

        for i, row in enumerate(self.r_hints):
            for j, hint in enumerate(row[::-1]):
                with grid[max_h_c_hints + i + 1][max_w_r_hints - (j + 1)]:
                    # st.write(f"{hint}")
                    st.write(hint)

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                gi = i + max_h_c_hints + 1
                gj = j + max_w_r_hints
                with grid[gi][gj]:
                    key_cb = f"check_{gi}_{gj}"
                    st.session_state.setdefault(key_cb, False)
                    cb = st.checkbox(
                        label=key_cb,
                        label_visibility="hidden",
                        key=key_cb
                    )


    def __repr__(self):
        return f"Nonogram({self.n_rows}x{self.n_cols})"

    def get_solved(self) -> bool:
        return self.grid_working == self.grid_solved

    def set_solved(self, solved_in):
        pass

    def del_solved(self):
        pass

    solved = property(get_solved, set_solved, del_solved)


async def run_day():
    now = datetime.datetime.now()
    start = now.replace(hour=6, minute=0, second=0, microsecond=0)
    end = datetime.datetime.now()
    end = end.replace(hour=16, minute=30, second=0, microsecond=0)
    t_sec = (end - start).total_seconds()
    
    now = now + datetime.timedelta(minutes=1)
    p_sec = max((now - start).total_seconds(), 0)
    v = min(1.0, max(0.0, p_sec / t_sec))
    pb_day.progress(v, text=f"{percent(v)} {int(round(t_sec - p_sec, 0))} second(s) left {time_between(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(seconds=t_sec - p_sec))}")
    
    while now < end:
        now = datetime.datetime.now()
        p_sec = max((now - start).total_seconds(), 0)
        await asyncio.sleep(1)
        v = min(1.0, max(0.0, p_sec / t_sec))
        pb_day.progress(v, text=f"{percent(v)} {int(round(t_sec - p_sec, 0))} second(s) left {time_between(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(seconds=t_sec - p_sec))}")
        # st.write(f"{end}, {p_sec=}, {v=}")
    # st.write(f"{start}")
    # st.write(f"{end}")


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    pb_day = st.progress(value=0)

    col_debug, col_results = st.columns(2)

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
        ],
        "answer": [
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        ]
    }

    p1 = {
        "r_hints": [
            [1],
            [2],
            [1, 1],
            [1, 1, 1],
            [1, 1],
            [2],
            [2],
            [2],
            [1, 1]
        ],
        "c_hints": [
            [1, 1],
            [2, 2],
            [2, 1],
            [1, 2, 1],
            [1, 1, 1],
            [2, 2],
            [2, 2],
            [1, 1],
            [1, 1]
        ]
    }

    p2 = {
        "c_hints": [
            [5],
            [2, 2],
            [2, 2],
            [1, 6],
            [1, 2],
            [3, 2],
            [1, 2],
            [4, 1],
            [3, 1],
            [1, 1, 2],
            [1, 1, 2],
            [1, 1, 4],
            [1, 1, 1, 2],
            [1, 2, 2],
            [6]
        ],
        "r_hints": [
            [0],
            [0],
            [0],
            [6],
            [4, 2, 1],
            [3, 10],
            [1, 1, 1, 1, 2],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1],
            [2, 1, 1, 1],
            [13],
            [5, 5],
            [0],
            [0],
            [0]
        ],
        "answer": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    }

    sample_smiley = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                     [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                     [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                     [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                     [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
                     [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                     [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]
    sample_smiley_r_hints = Nonogram.gen_horizontal_hints(sample_smiley)
    sample_smiley_c_hints = Nonogram.gen_vertical_hints(sample_smiley)
    sample_smiley = {
        "c_hints": sample_smiley_c_hints,
        "r_hints": sample_smiley_r_hints
    }

    nonogram_puzzles = [
        {
            "title": "p0",
            "nonogram_data": p0
        },
        {
            "title": "p1",
            "nonogram_data": p1
        },
        {
            "title": "p2",
            "nonogram_data": p2
        },
        {
            "title": "smiley",
            "nonogram_data": sample_smiley
        }
    ]

    k_selectbox_nonogram = "key_selectbox_nonogram"
    st.session_state.setdefault(k_selectbox_nonogram, nonogram_puzzles[0]["title"])
    selectbox_nonogram = col_results.selectbox(
        label="Puzzle",
        key=k_selectbox_nonogram,
        options=[p["title"] for p in nonogram_puzzles]
    )

    if selectbox_nonogram:

        puzzle_idx = [i for i in range(len(nonogram_puzzles)) if nonogram_puzzles[i]["title"] == selectbox_nonogram][0]
        puzzle_data = nonogram_puzzles[puzzle_idx]
        nonogram_data = puzzle_data["nonogram_data"]
        nonogram = Nonogram(nonogram_data)
        col_debug.divider()
        col_results.write(nonogram)
        with col_debug.expander("Grid Working"):
            st.write(nonogram.grid_working)
        with col_debug.expander("Row Hints"):
            st.write(nonogram.r_hints)
        with col_debug.expander("Col Hints"):
            st.write(nonogram.c_hints)
        df_gw = pd.DataFrame(nonogram.grid_working)
        col_debug.write(df_gw)

        key_checkbox_show_answer: str = "k_checkbox_show_answer"
        st.session_state.setdefault(key_checkbox_show_answer, True)
        checkbox_show_answer = col_results.checkbox(label="Show Answer?", key=key_checkbox_show_answer)
        col_results.code(nonogram.text_grid(show_answer=checkbox_show_answer))
        # # col_results.code(nonogram.st_grid())  # clunky spacing
        # # # st.code(Nonogram.to_string(np.transpose(n0.grid_working).tolist(), n0.r_hints, n0.c_hints))
        # # # st.code(Nonogram.to_string(n0.grid_working))
        # # # st.code(Nonogram.to_string(n0.grid_working, n0.r_hints))
        # # # st.code(Nonogram.to_string(n0.grid_working, None, n0.c_hints))
        # st.write(Nonogram.note_separated([
        #     Nonogram.NOTE,
        #     Nonogram.NOTE,
        #     Nonogram.NOTE,
        #     Nonogram.BLANK,
        #     Nonogram.BLANK,
        #     Nonogram.BLANK,
        #     Nonogram.BLANK,
        #     Nonogram.BLANK,
        #     Nonogram.BLANK,
        #     Nonogram.BLANK,
        #     Nonogram.BLANK,
        #     Nonogram.BLANK,
        #     Nonogram.MARK,
        #     Nonogram.BLANK,
        #     Nonogram.NOTE,
        #     Nonogram.NOTE,
        #     Nonogram.NOTE
        # ]))

        row = [Nonogram.BLANK for i in range(10)]
        row[1] = Nonogram.MARK
        row[2] = Nonogram.MARK
        with col_results:
            for i, val in enumerate(row):
                st.write(f"{i=}, {val=}, {Nonogram.count_continuous(row, val, i)}")
    
    asyncio.run(run_day())
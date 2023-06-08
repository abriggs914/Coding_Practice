import tkinter

from colour_utility import *
from tkinter_utility import *
from utility import minmax, maxmin, sort_2_lists


class App(tkinter.Tk):

    def __init__(self, array, zero_at_top=False):
        super().__init__()

        MAX_N = 25
        TOL_CANVAS = 3

        self.state_list_of_flashing_bars = []
        self.zero_at_top = zero_at_top
        self.original_array = list(array[:MAX_N])
        self.working_array = list(array[:MAX_N])
        self.n = len(self.original_array)
        self.geometry(f"700x500")
        self.title("")

        self.state = "IDLE"
        self.animation_time = 100 * self.n
        self.fps = 24

        self.background_canvas = Colour(SUN_YELLOW).hex_code
        self.width_canvas, self.height_canvas = 550, 200
        self.fc_bars, self.oc_bars = Colour(DODGERBLUE).hex_code, Colour(BLACK).hex_code
        self.fc_texts = Colour(BLACK).hex_code

        self.canvas = tkinter.Canvas(
            self,
            width=self.width_canvas,
            height=self.height_canvas,
            background=self.background_canvas
        )

        self.tv_btn_reset,\
        self.btn_reset=\
            button_factory(
                self,
                tv_btn="reset",
                command=self.reset
            )

        self.tv_btn_go,\
        self.btn_go=\
            button_factory(
                self,
                tv_btn="go",
                command=self.go
            )

        self.min_, self.max_ = minmax(self.original_array)
        self.spread = abs(self.max_) + abs(self.min_)
        self.has_negatives = self.spread != self.max_
        gc = grid_cells(self.width_canvas, self.n, self.height_canvas, 1, 1, 1)
        bar_dims = gc[0][0]  # x1, y1, x2, y2
        self.w_bar, self.h_bar = bar_dims[2] - bar_dims[0], bar_dims[3] - bar_dims[1]
        self.ypp = self.height_canvas / (self.spread if self.spread != 0 else 1)
        self.y_0 = clamp(TOL_CANVAS, self.y_at_v(0), self.height_canvas - TOL_CANVAS)
        print(f"{self.y_0=}")

        grads = list(rainbow_gradient(self.n * 2, rgb=False))[:self.n]
        # dummy, grads = sort_2_lists(list(self.original_array), grads)
        grads, dummy = sort_2_lists(grads, list(self.original_array))
        self.bars = [
            self.canvas.create_rectangle(
                *gc[0][i],
                # fill=self.fc_bars,
                fill=grads[i],
                outline=self.oc_bars
            )
            for i in range(self.n)
        ]
        self.texts = [
            self.canvas.create_text(
                gc[0][i][0] + (self.w_bar / 2),
                gc[0][i][1] + (self.h_bar / 2),
                text=f"{self.original_array[i]}",
                fill=self.fc_texts
            )
            for i in range(self.n)
        ]

        for i, el in enumerate(self.original_array):
            tb = self.bars[i]
            tt = self.texts[i]
            cdb = self.canvas.coords(tb)
            cdt = self.canvas.coords(tt)
            bbb = self.canvas.bbox(tb)
            bbt = self.canvas.bbox(tt)
            if self.zero_at_top:
                y_0, y_1 = minmax(0, abs(self.min_) + el)
            else:
                y_0, y_1 = minmax(0, el)
            y_0, y_1 = self.y_at_v(y_0), self.y_at_v(y_1)
            y_d = y_1 - y_0
            y_m = y_0 + (y_d / 2)
            y_d = abs(y_d)
            y_r = 0
            ht, wt = bbt[3] - bbt[1], bbt[2] - bbt[0]
            code = ""

            if ht > y_d:
                code += "A"
                if el < 0:
                    code += "B"
                    y_r = self.height_canvas - y_0
                    if y_r > ht:
                        code += "D"
                        y_m += clamp(18, y_d, 24)
                    else:
                        code += "E"
                        y_m -= clamp(18, y_d, 24)
                else:
                    code += "C"
                    y_r = y_1
                    if y_r > ht:
                        code += "F"
                        y_m -= clamp(18, y_d, 24)
                    else:
                        code += "G"
                        y_m += clamp(18, y_d, 24)
                code += "\n"

            self.canvas.tag_bind(tb, "<Button-1>", lambda event, idx=i: self.click_bar(event, i=idx))
            self.canvas.tag_bind(tt, "<Button-1>", lambda event, idx=i: self.click_bar(event, i=idx))

            # print(f"{i=}, {el=}, {y_0=:.3f}, {y_1=:.3f}, {y_d=:.3f}, {y_r=:.3f}, ypp={self.ypp:.3f}, {y_m=:.3f}\n{bbb=}\n{bbt=} {wt=:.3f} {ht=:.3f}\n{code}")
            self.canvas.coords(tb, (cdb[0], y_0, cdb[2], y_1))
            self.canvas.coords(tt, (cdt[0], y_m))

        self.canvas.create_line(0, self.y_0, self.width_canvas, self.y_0, fill=Colour(ORANGE).hex_code, width=3)

        self.canvas.pack(padx=5, pady=5)
        self.btn_go.pack()
        self.btn_reset.pack()

    def y_at_v(self, v_in):
        if self.zero_at_top:
            return (abs(self.min_) - v_in) * self.ypp
        else:
            return (self.max_ - v_in) * self.ypp

    def click_bar(self, event, i):
        if i not in self.state_list_of_flashing_bars:
            a_time = self.flash_bar(i)
            print(f"{a_time=}")
            self.state_list_of_flashing_bars.append(i)
            self.after(a_time, lambda: self.state_list_of_flashing_bars.remove(i))
        else:
            print(f"{self.state_list_of_flashing_bars=}")

    def bubble_sort(self):
        res = list(self.original_array)
        n = self.n
        code = ""
        print(f"START: {res=}")
        comparisons = 0
        swaps = 0
        operations = []
        for i in range(n - 1):
            for j in range(n - i - 1):
                comparisons += 1
                code += f"{i=}, {j=}\n"
                v1 = res[j]
                v2 = res[j + 1]
                # op = f"compare {i=}, {j=}, {j+1=}, {res[j]=} {res[j + 1]=}"
                op = {
                    "op": "compare",
                    "i": i,
                    "j": j,
                    "res[j]": res[j],
                    "res[j + 1]": res[j + 1],
                    "bb_0": self.canvas.bbox(self.bars[j]),
                    "bb_1": self.canvas.bbox(self.bars[j + 1])
                }
                if v2 < v1:
                    swaps += 1
                    res[j], res[j + 1] = res[j + 1], res[j]
                    # op = f"swap {i=}, {j=}, {j+1=}, {res[j]=} {res[j + 1]=}"
                    op["op"] = "swap"
                operations.append(op)
        print(f"FINAL: {res=}")
        print(f"{comparisons=}\n{swaps=}\n{len(operations)=}\n", end="")
        # print("\n".join(operations))
        # print(f"{code}")
        self.working_array = res
        return operations

    def anim_time(self, frames, ms_per_frame, i_0=0, half_offset=None):
        ho = half_offset if half_offset is not None else 1
        return sum([i_0 + (i * ms_per_frame) + (ho * (1 if half_offset is not None else 0) * (1 if ((i // 2) >= frames) else 0)) for i in range(frames)])

    def flash_bar(self, i, n_slices=10, half_offset=250, ms_per_frame=15, i_0=0):
        print(f"Flash {i}")
        tb = self.bars[i]
        tt = self.texts[i]
        fill1 = Colour(self.canvas.itemcget(tb, "fill"))
        fill2 = fill1.darkened(0.5)
        fill3 = Colour(self.canvas.itemcget(tt, "fill"))
        fill4 = fill3.brightened(0.5)
        grads_b = [gradient(i, n_slices, fill1, fill2, rgb=False) for i in range(n_slices)]
        grads_b = grads_b + grads_b[::-1]
        grads_t = [gradient(i, n_slices, fill3, fill4, rgb=False) for i in range(n_slices)]
        grads_t = grads_t + grads_t[::-1]
        tot_t = 0
        for j, grad in enumerate(grads_b):
            if j >= len(grads_b) // 2:
                o = half_offset
            else:
                o = 0
            t = i_0 + (ms_per_frame * j) + o
            self.after(t, lambda t=tb, jj=j: self.canvas.itemconfigure(tb, fill=grads_b[jj]))
            self.after(t, lambda t=tt, jj=j: self.canvas.itemconfigure(tt, fill=grads_t[jj]))
            tot_t = max(tot_t, t)
        # n_slices = 10
        # 100 + (0 * 15) + 0 -> 100 + (9 * 15) + 0 ==> 100, 115, 130, 145, 160, 175, 190, 205, 220, 235
        # 100 + (10 * 15) + 250 -> 100 + (19 * 15) + 250 ==> 500, 515, 530, 545, 560, 575, 590, 605, 620, 635
        # total time = 7350 ms
        # return self.anim_time(n_slices * 2, ms_per_frame, i_0, half_offset=half_offset)
        return tot_t

    def go(self):
        print(f"go")
        operations = self.bubble_sort()

        frames = 12
        nop = len(operations)
        tm = sum([op["bb_1"][0] - op["bb_0"][0] for op in operations])
        print(f"{tm=}")
        o = 0
        a_times = []
        t_a_time = 0
        a_off = 0
        for i, op in enumerate(operations):
            typ = op["op"]
            j = op["j"]
            j_1 = j + 1
            print(f"{t_a_time=}, {a_off=}, {t_a_time+a_off}")
            # self.after(100 + (i * 685) + o, lambda ij=j: self.flash_bar(i=ij, n_slices=10, half_offset=250, ms_per_frame=15, i_0=0))
            # self.after(100 + (i * 685) + o, lambda ij=j_1: self.flash_bar(i=ij, n_slices=10, half_offset=250, ms_per_frame=15, i_0=0))
            self.after(t_a_time + a_off, lambda ij=j: self.flash_bar(i=ij, n_slices=10, half_offset=250, ms_per_frame=15, i_0=0))
            self.after(t_a_time + a_off, lambda ij=j_1: self.flash_bar(i=ij, n_slices=10, half_offset=250, ms_per_frame=15, i_0=0))
            # self.after(t_a_time + a_off, lambda msg=f"Pass # {i + 1}": print(msg))
            a_times.append(self.anim_time(frames=10, ms_per_frame=15, i_0=0, half_offset=250))
            t_a_time += a_times[-1]
            if typ == "swap":
                bb_0 = op["bb_0"]
                bb_1 = op["bb_1"]
                xd = abs(bb_1[0] - bb_0[0])
                xpf = xd / frames
                d = -1 if bb_1[0] < bb_0[0] else 1
                tb1 = self.bars[j]
                tb2 = self.bars[j_1]
                mpf = 15
                sub_a_time = self.anim_time(frames, mpf)
                # a_times.append(sub_a_time)
                a_off += sub_a_time
                for j in range(frames):
                    c_time = t_a_time + (j * mpf)
                    self.after(
                        c_time,\
                        # t_a_time,\
                        # 100 + (i * 685) + (j * 120),\
                        # 10,\
                        lambda tb1_=tb1, bb_0_=bb_0, d_=d, j_=j, xpf_=xpf:\
                            self.canvas.coords(tb1_, (bb_0_[0] + (d_ * (j_ * xpf_)), bb_0_[1], bb_0_[1] + (d_ * (j_ * xpf_)), bb_0_[3])))
                    self.after(
                        c_time,
                        lambda tb1_=tb2, bb_0_=bb_1, d_=-d, j_=j, xpf_=xpf: \
                            self.canvas.coords(tb1_, (
                            bb_0_[0] + (d_ * (j_ * xpf_)), bb_0_[1], bb_0_[1] + (d_ * (j_ * xpf_)), bb_0_[3])))
                    # self.after(100 + (i * 685) + (j * 120), lambda tb1_=tb2, bb_0_=bb_1, d_=-d, j_=j, xpf_=xpf: self.canvas.coords(tb1_, (bb_0_[0] + (d_ * (j_ * xpf_)), bb_0_[1], bb_0_[1] + (d_ * (j_ * xpf_)), bb_0_[3])))
                    o += 100 + (i * 685) + (j * 120)
            print(f"{op}")
        # ops = nop / self.animation_time


    def reset(self):
        print(f"reset")


if __name__ == '__main__':
    zat = True
    zat = False
    arr = [8, 18, 9, -1, 0, 6, 1, 5, -7, 15, 16, 7]
    # arr = list(range(6))
    # arr = list(range(25))
    # arr = list(range(-12, 0, 1)) + list(range(60))
    # arr = list(range(-1, 0, 1)) + list(range(60))
    # arr = list(range(-20, 0, 1)) + list(range(60))
    # arr = [-199, 2000, 15, 16, 55, 999, 484, -55, -156, 1400]
    app = App(arr, zero_at_top=zat)

    # print(f"{app.y_at_v(max(arr))=}")
    # print(f"{app.y_at_v(min(arr))=}")
    # print(f"{app.y_at_v(max(arr)+1)=}")
    # print(f"{app.y_at_v(min(arr)-1)=}")

    app.mainloop()

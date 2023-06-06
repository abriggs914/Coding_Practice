import tkinter

from colour_utility import *
from tkinter_utility import *
from utility import minmax, maxmin


class App(tkinter.Tk):

    def __init__(self, array, zero_at_top=False):
        super().__init__()

        MAX_N = 25
        TOL_CANVAS = 3

        self.zero_at_top = zero_at_top
        self.original_array = list(array[:MAX_N])
        self.n = len(self.original_array)
        self.geometry(f"700x500")
        self.title("")
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

        self.bars = [
            self.canvas.create_rectangle(
                *gc[0][i],
                fill=self.fc_bars,
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

            # if int(y_d / self.ypp) <= abs(el):
            #     code += "A"
            #     if el < 0:
            #         code += "B"
            #         y_r = self.height_canvas - y_1
            #         if y_r > y_d:
            #             code += "D"
            #             y_m += clamp(18, y_d, 24)
            #         else:
            #             code += "E"
            #             y_m -= clamp(18, y_d, 24)
            #     else:
            #         code += "C"
            #         y_r = y_1
            #         if y_r > y_d:
            #             code += "F"
            #             y_m -= clamp(18, y_d, 24)
            #         else:
            #             code += "G"
            #             y_m += clamp(18, y_d, 24)
            #     code += "\n"
            print(f"{i=}, {el=}, {y_0=:.3f}, {y_1=:.3f}, {y_d=:.3f}, {y_r=:.3f}, ypp={self.ypp:.3f}, {y_m=:.3f}\n{bbb=}\n{bbt=} {wt=:.3f} {ht=:.3f}\n{code}")
            self.canvas.coords(tb, (cdb[0], y_0, cdb[2], y_1))
            self.canvas.coords(tt, (cdt[0], y_m))
            # self.canvas.coords(tt, (cdt[0] + (self.w_bar / 2), y_1 + (yh / 2)))

        self.canvas.create_line(0, self.y_0, self.width_canvas, self.y_0, fill=Colour(ORANGE).hex_code, width=3)

        self.canvas.pack(padx=5, pady=5)
        self.btn_go.pack()
        self.btn_reset.pack()

    def y_at_v(self, v_in):
        if self.zero_at_top:
            return (abs(self.min_) - v_in) * self.ypp
        else:
            return (self.max_ - v_in) * self.ypp
        # ypp = self.height_canvas / (self.spread if self.spread != 0 else 1)
        #
        # # if v_in < 0:
        # #     off = self.max_
        # # else:
        # #     off = 0
        # # print(f"{ypp=}, {off=}, {v_in=}, zat={self.zero_at_top}")
        # # print(f"{self.min_=}, {self.max_=}, {self.spread=}")
        #
        # res = (self.max_ - v_in) * ypp
        # # print(f"RES = <{self.height_canvas - ((v_in + off) * ypp)}>")
        # # return self.height_canvas - ((v_in + off) * ypp)
        # print(f"RES = <{res}>")
        # return res
        #
        # # if self.zero_at_top:
        # #     print(f"RES A= <{(v_in + off) * ypp}>")
        # #     return (v_in + off) * ypp
        # # else:
        # #     print(f"RES B= <{self.height_canvas - ((v_in + off) * ypp)}>")
        # #     return self.height_canvas - ((v_in + off) * ypp)
        # # # if self.has_negatives:
        # # # else:


    def go(self):
        print(f"go")

    def reset(self):
        print(f"reset")


if __name__ == '__main__':
    zat = True
    zat = False
    # arr = [8, 18, 9, -1, 0, 6, 1, 5, -7, 15, 16, 7]
    # arr = list(range(6))
    # arr = list(range(-12, 0, 1)) + list(range(60))
    # arr = list(range(-1, 0, 1)) + list(range(60))
    # arr = list(range(-20, 0, 1)) + list(range(60))
    arr = [-199, 2000, 15, 16, 55, 999, 484, -55, -156, 1400]
    app = App(arr, zero_at_top=zat)

    # print(f"{app.y_at_v(max(arr))=}")
    # print(f"{app.y_at_v(min(arr))=}")
    # print(f"{app.y_at_v(max(arr)+1)=}")
    # print(f"{app.y_at_v(min(arr)-1)=}")

    app.mainloop()

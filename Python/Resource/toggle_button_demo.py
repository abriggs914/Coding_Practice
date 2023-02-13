import tkinter

from colour_utility import *
from ctkinter import *
from tkinter_utility import *
from utility import Rect2


# class ToggleButton(tkinter.Frame):
#
#     def __init__(
#             self,
#             master,
#             label_text="Toggle",
#             state: bool = False,
#             width_label=25,
#             height_label=1,
#             width_canvas=100,
#             height_canvas=50,
#             colour_fg_true="#003000",
#             colour_bg_true="#29c164",
#             colour_fg_false="#300000",
#             colour_bg_false="#c12929",
#             *args, **kwargs):
#         super().__init__(master, width=width_canvas, height=height_canvas, *args, **kwargs)
#
#         self.tv_label = tkinter.StringVar(self, value=label_text)
#         self.label = tkinter.Label(self, textvariable=self.tv_label, width=width_label, height=height_label)
#         self.frame_canvas = tkinter.Frame(self, width=width_label + width_canvas)
#         self.canvas = tkinter.Canvas(self.frame_canvas, width=width_canvas, height=height_canvas)
#
#         self.colour_bg_true = colour_bg_true
#         self.colour_bg_false = colour_bg_false
#         self.colour_fg_true = colour_fg_true
#         self.colour_fg_false = colour_fg_false
#         self.width = width_canvas
#         self.height = height_canvas
#
#         self.state = tkinter.BooleanVar(self, value=state)
#         self.state.trace_variable("w", self.state_update)
#
#         self.sliding = tkinter.BooleanVar(self, value=False)
#
#         self.bind("<Button-1>", self.click)
#         self.label.bind("<Button-1>", self.click)
#         self.frame_canvas.bind("<Button-1>", self.click)
#         self.canvas.bind("<Button-1>", self.click)
#
#         x1, y1, x2, y2 = self.width * 0.15, self.height * 0.15, self.width * 0.85, self.height * 0.85
#         pts = [
#             (x1, y1),
#             (x2, y1),
#             (x2, y2),
#             (x1, y2)
#         ]
#         xs, ys = [[pt[i] for pt in pts] for i in range(2)]
#         self.round_rect = round_polygon(
#             self.canvas,
#             xs,
#             ys,
#             width=2,
#             sharpness=25,
#             outline=self.colour_fg_false,
#             fill=brighten(self.colour_bg_false, 0.25, rgb=False)
#         )
#         self.text_off = self.canvas.create_text(self.width * 0.25, self.height / 2, text="Off",
#                                                 fill=self.colour_fg_false)
#         self.text_on = self.canvas.create_text(self.width * 0.75, self.height / 2, text="On", fill=self.colour_fg_true)
#
#         self.state_update()
#
#     def state_update(self, *args):
#         slices = 10
#         state = self.state.get()
#         bg_start = self.colour_bg_true if not state else self.colour_bg_false
#         bg_end = self.colour_bg_false if not state else self.colour_bg_true
#         bg_gradient_colours = [gradient(i, slices, bg_start, bg_end) for i in range(slices)]
#         fg_start = self.colour_fg_true if not state else self.colour_fg_false
#         fg_end = self.colour_fg_false if not state else self.colour_fg_true
#         bg_gradient_colours = [gradient(i, slices, bg_start, bg_end, rgb=False) for i in range(slices)]
#         fg_gradient_colours = [gradient(i, slices, fg_start, fg_end, rgb=False) for i in range(slices)]
#
#         # print(f"Status Update: {state=}")
#
#         if state:
#             self.canvas.itemconfigure(self.text_on, state="normal")
#             self.canvas.itemconfigure(self.text_off, state="hidden")
#         else:
#             self.canvas.itemconfigure(self.text_on, state="hidden")
#             self.canvas.itemconfigure(self.text_off, state="normal")
#
#         def iter_update(i):
#             # print(f"\titer_{i=}")
#             if i == slices:
#                 self.sliding.set(False)
#                 return
#
#             bg_colour = bg_gradient_colours[i]
#             fg_colour = fg_gradient_colours[i]
#             fill_colour = brighten(bg_colour, 0.25, rgb=False) if not state else darken(bg_colour, 0.25, rgb=False)
#
#             # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
#             self.configure(background=bg_colour, highlightthickness=0)
#             self.canvas.itemconfigure(
#                 self.round_rect,
#                 outline=fg_colour,
#                 fill=fill_colour
#             )
#
#             self.canvas.itemconfigure(self.text_on, fill=fg_colour)
#             self.canvas.itemconfigure(self.text_off, fill=fg_colour)
#             self.canvas.configure(background=bg_colour, highlightthickness=0)
#             self.label.configure(background=bg_colour, foreground=fg_colour, highlightthickness=0)
#
#             self.after(50, iter_update, i + 1)
#
#         iter_update(0)
#
#     def click(self, *args):
#         if not self.sliding.get():
#             self.sliding.set(True)
#             self.state.set(not self.state.get())
#
#     def get_objects(self):
#         return (
#             self,
#             (self.tv_label, self.label),
#             self.frame_canvas,
#             (self.state, self.canvas)
#         )


def click_cbutton():
    print(f"click_cbutton")


def testt_b1():
    win = tkinter.Tk()
    win.geometry(f"600x600")

    tb = ToggleButton(win)

    tb.pack()

    tb2 = CButton(
        win,
        text="Click Me",
        fg="white",
        width=100,
        height=50,
        command=click_cbutton,
        rounded_corners="round"
    )

    # c = tkinter.Canvas(win, width_canvas=250, height_canvas=250, background="#666666")
    # c.pack(fill="both")
    #
    # c.create_text(50, 50, text="Hello")

    tb2.pack()

    win.mainloop()


def test_form():
    win = tkinter.Tk()
    win.geometry(f"600x600")

    q = "quantity"
    w = "wired(less)"

    frame_comp_choice = tkinter.Frame(name="fame_comp_choice")
    tv_label_comp_choice = tkinter.StringVar(win, value="Select Hardware:", name="tv_label_comp_choice")
    tv_comp_choice = tkinter.StringVar(win, name="tv_comp_choice")

    tv_label_comp_choice, \
    label_comp_choice, \
    tv_comp_choice, \
    combo_comp_choice = \
        combo_factory(
            frame_comp_choice,
            tv_label=tv_label_comp_choice,
            tv_combo=tv_comp_choice,
            kwargs_combo={
                "values": [
                    "Laptop",
                    "Desktop"
                ]
            }
        )

    questions = [
        ("Extra Charger(s)", None, tkinter.StringVar(win, name="extra_chargers")),
        ("Monitor(s)", q, tkinter.StringVar(win, name="monitors")),
        ("Peripheral Cable(s)", q, tkinter.StringVar(win, name="peripheral_cables")),
        ("Dock", None, tkinter.StringVar(win, name="dock")),
        ("Keyboard", w, tkinter.StringVar(win, name="keyboard")),
        ("Mouse", w, tkinter.StringVar(win, name="mouse")),
        ("Mouse pad", None, tkinter.StringVar(win, name="mouse_pad")),
        ("Camera", None, tkinter.StringVar(win, name="camera")),
        ("Microphone", None, tkinter.StringVar(win, name="microphone"))
    ]
    questions = {k.lower().replace("(", "").replace(")", ""): dict(zip(["text", "follow_up", "var"], [k, f, v])) for
                 k, f, v in questions}

    frame_toggle_buttons = tkinter.Frame(win, background=random_colour(rgb=False))
    for q_title, q_data in questions.items():
        q_text, q_follow_up, q_var = list(q_data.values())
        tb, label_data, \
        frame_canvas, btn_data = \
            ToggleButton(
                frame_toggle_buttons,
                label_text=q_text,
                labels=None
                # ,
                # t_animation_time=100,
                # n_slices=1000000
            ).get_objects()
        tv_label, label = label_data
        var, canvas = btn_data
        questions[q_title].update({
            "button": tb,
            "tv_label": tv_label,
            "label": label,
            "var": var,
            "frame_canvas": frame_canvas,
            "canvas": canvas
        })
        label.pack(side=tkinter.LEFT)
        canvas.pack(side=tkinter.LEFT)
        frame_canvas.pack(side=tkinter.LEFT)
        tb.pack()

    label_comp_choice.pack(side=tkinter.LEFT, ipadx=12, ipady=12)
    combo_comp_choice.pack(side=tkinter.LEFT, ipadx=12, ipady=12)
    frame_comp_choice.pack()
    frame_toggle_buttons.pack()

    win.mainloop()


if __name__ == '__main__':
    # test_tb1()
    test_form()

#
# class ToggleButton(tkinter.Frame):
#
#     def __init__(
#             self,
#             master,
#             label_text="Toggle",
#             state: bool = False,
#             width_label=25,
#             height_label=1,
#             width_canvas=100,
#             height_canvas=50,
#             colour_fg_true="#003000",
#             colour_bg_true="#29c164",
#             colour_fg_false="#300000",
#             colour_bg_false="#c12929",
#             *args, **kwargs):
#         super().__init__(master, width=width_canvas, height=height_canvas, *args, **kwargs)
#
#         self.tv_label = tkinter.StringVar(self, value=label_text)
#         self.label = tkinter.Label(self, textvariable=self.tv_label, width=width_label, height=height_label)
#         self.frame_canvas = tkinter.Frame(self, width=width_label + width_canvas)
#         self.canvas = tkinter.Canvas(self.frame_canvas, width=width_canvas, height=height_canvas)
#
#         self.colour_bg_true = colour_bg_true
#         self.colour_bg_false = colour_bg_false
#         self.colour_fg_true = colour_fg_true
#         self.colour_fg_false = colour_fg_false
#         self.width = width_canvas
#         self.height = height_canvas
#
#         self.state = tkinter.BooleanVar(self, value=state)
#         self.state.trace_variable("w", self.state_update)
#
#         self.sliding = tkinter.BooleanVar(self, value=False)
#
#         self.bind("<Button-1>", self.click)
#         self.label.bind("<Button-1>", self.click)
#         self.frame_canvas.bind("<Button-1>", self.click)
#         self.canvas.bind("<Button-1>", self.click)
#
#         self.text_off = self.canvas.create_text(self.width * 0.25, self.height / 2, text="Off", fill=self.colour_fg_false)
#         self.text_on = self.canvas.create_text(self.width * 0.75, self.height / 2, text="On", fill=self.colour_fg_true)
#         # self.round_rect = self.canvas.create_rectangle(self.width * 0.15, self.height * 0.15, self.width * 0.85, self.height * 0.85, outline=self.colour_fg_false, fill="")
#         self.round_rect = rounded_rect(self.canvas, self.width * 0.15, self.height * 0.15, self.width * 0.7, self.height * 0.7, 5)
#         for line in self.round_rect:
#             self.canvas.itemconfigure(line, fill=self.colour_fg_false)
#         # , width = 2, outline = self.colour_fg_false, fill = ""
#
#         self.state_update()
#
#     def state_update(self, *args):
#         slices = 10
#         state = self.state.get()
#         bg_start = self.colour_bg_true if not state else self.colour_bg_false
#         bg_end = self.colour_bg_false if not state else self.colour_bg_true
#         bg_gradient_colours = [gradient(i, slices, bg_start, bg_end) for i in range(slices)]
#         fg_start = self.colour_fg_true if not state else self.colour_fg_false
#         fg_end = self.colour_fg_false if not state else self.colour_fg_true
#         bg_gradient_colours = [gradient(i, slices, bg_start, bg_end, rgb=False) for i in range(slices)]
#         fg_gradient_colours = [gradient(i, slices, fg_start, fg_end, rgb=False) for i in range(slices)]
#
#         # print(f"Status Update: {state=}")
#
#         if state:
#             self.canvas.itemconfigure(self.text_on, state="normal")
#             self.canvas.itemconfigure(self.text_off, state="hidden")
#         else:
#             self.canvas.itemconfigure(self.text_on, state="hidden")
#             self.canvas.itemconfigure(self.text_off, state="normal")
#
#         def iter_update(i):
#             # print(f"\titer_{i=}")
#             if i == slices:
#                 self.sliding.set(False)
#                 return
#
#             bg_colour = bg_gradient_colours[i]
#             fg_colour = fg_gradient_colours[i]
#
#             # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
#             self.configure(background=bg_colour, highlightthickness=0)
#             for line in self.round_rect:
#                 tp = self.canvas.type(line)
#                 if tp == "line":
#                     self.canvas.itemconfigure(line, fill=fg_colour)
#                 elif tp == "arc":
#                     self.canvas.itemconfigure(line, outline=fg_colour)
#
#             self.canvas.itemconfigure(self.text_on, fill=fg_colour)
#             self.canvas.itemconfigure(self.text_off, fill=fg_colour)
#             self.canvas.configure(background=bg_colour, highlightthickness=0)
#             self.label.configure(background=bg_colour, foreground=fg_colour, highlightthickness=0)
#
#             self.after(50, iter_update, i + 1)
#
#         iter_update(0)
#
#     def click(self, *args):
#         if not self.sliding.get():
#             self.sliding.set(True)
#             self.state.set(not self.state.get())
#
#     def get_objects(self):
#         return (
#             self,
#             (self.tv_label, self.label),
#             self.frame_canvas,
#             (self.state, self.canvas)
#         )

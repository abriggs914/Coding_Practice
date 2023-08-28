import datetime
import enum
import json
import tkinter
from threading import Thread
from dataclasses import dataclass
from typing import Tuple

from datetime_utility import is_date
from json_utility import jsonify
from orbiting_date_picker import OrbitingDatePicker
from tkinter_utility import *
from tktimepicker import SpinTimePickerModern, constants as tktp_constants


def hours_until(d1: datetime.datetime, d2: datetime.datetime = None, rtype: str = "h"):
    if d2 is None:
        d2 = datetime.datetime.now()
    x = f"{d1=:%Y-%m-%d %H:%M}, {d2=:%Y-%m-%d %H:%M}"
    dd = (d2 - d1)
    d = dd.total_seconds()
    overdue = d < 0
    if rtype != "b":
        d = abs(d)
        f_days = int(abs(d // 86400))
        f_hrs = int(abs((d - (f_days * 86400)) // 3600))
        f_mins, f_secs = divmod(d - ((86400 * f_days) + (3600 * f_hrs)), 60)
        f_mins = int(abs(f_mins))
        f_secs = int(abs(round(f_secs, 0)))
        w = f"{d=}, {f_days=}, {f_hrs=}, {f_mins=}, {f_secs=}"
    match rtype:
        case "b":
            # overdue or not
            return overdue
        case "d":
            # Days as decimal
            r = f"{round(d / 86400, 4)} Days"
            # print(f"A: {w}, {x=}, {r=}")
            return r
        case "h":
            # Hours as decimal
            r = f"{round(d / 3600, 3)} Hrs"
            # print(f"B: {w}, {x=}, {r=}")
            return r
        case "m":
            # Minutes as decimal
            r = f"{int(round(d / 60, 0))} Mins"
            # print(f"C: {w}, {x=}, {r=}")
            return r
        case "s":
            # Seconds as decimal
            r = f"{int(round(d))} Secs"
            # print(f"D: {w}, {x=}, {r=}")
            return r
        case "tt":
            # Total time
            r = f"{f_days} Days, {f_hrs} Hrs, {f_mins} Mins, {f_secs} Secs"
            # print(f"E: {w}, {x=}, {r=}")
            return r
        case "t":
            # Max time unit and less.
            m = ""
            if f_days > 0:
                m = f"{f_days} Days, "

            if f_hrs > 0:
                m = m + f"{f_hrs} Hrs, "
                if f_mins > 0:
                    m = m + f"{f_mins} Mins, "
            else:
                if f_mins > 0:
                    m = m + f"{f_mins} Mins, "
            m = m + f"{f_secs} Secs, "
            r = m[:-2]
            # print(f"F: {w}, {x=}, {r=}")
            return r
        case _:
            raise ValueError(f"Error unrecognized return type value. Got '{rtype}'")


class TimeSlider(tkinter.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.value = tkinter.DoubleVar(self)
        # d_min_t = is_date(min_time)
        # d_max_t = is_date(max_time)
        # ds = (d_max_t - d_min_t).total_seconds()
        #
        # h_mi, m_mi, s_mi = d_min_t.hour, d_min_t.minute, d_min_t.second
        # h_ma, m_ma, s_ma = d_max_t.hour, d_max_t.minute, d_max_t.second

        # self.min_time, self.max_time = 1, 12
        # self.slider = tkinter.Scale(
        #     self,
        #     from_=self.min_time,
        #     to=self.max_time,
        #     variable=self.value,
        #     orient="horizontal"
        # )
        # self.slider.grid()

        self.time_picker = SpinTimePickerModern(self)
        self.time_picker.addAll(tktp_constants.HOURS12)  # adds hours clock, minutes and period
        self.time_picker.grid()


class State(enum.Enum):

    # State Name, StateID, State Acronym, State is Timed
    QUEUED: Tuple[str, int, str, bool] = "Queued", 0, "QUE", True
    INPROGRESS: Tuple[str, int, str, bool] = "In Progress", 1, "IPR", True
    EXPIRED: Tuple[str, int, str, bool] = "Expired", 2, "EXP", True
    WAITING: Tuple[str, int, str, bool] = "Waiting", 3, "WTG", True
    DEBUGGING: Tuple[str, int, str, bool] = "Debugging", 4, "BUG", True
    COMPLETE: Tuple[str, int, str, bool] = "Complete", 5, "CMP", False
    INCOMPLETE: Tuple[str, int, str, bool] = "Incomplete", 6, "INC", False
    DECLINED: Tuple[str, int, str, bool] = "Declined", 7, "DCL", False

    def is_timed_state(self):
        return self.value[3]

    def __hash__(self):
        return self.value[1]

    def __eq__(self, other):
        return isinstance(other, State) and self.value == other.value and self.name == other.name

    def __iter__(self):
        for v in [
            self.QUEUED,
            self.INPROGRESS,
            self.WAITING,
            self.DEBUGGING,
            self.COMPLETE,
            self.INCOMPLETE,
            self.DECLINED
        ]:
            yield v

    def __repr__(self):
        return str(self.value[0])

    def __str__(self):
        return str(self.value[0])


class Priority(enum.Enum):
    NEG_TWO: int = -2
    NEG_ONE: int = -1
    ZERO: int = 0
    ONE: int = 1
    TWO: int = 2
    THREE: int = 3
    FOUR: int = 4
    FIVE: int = 5
    SIX: int = 6
    SEVEN: int = 7
    EIGHT: int = 8
    NINE: int = 9
    TEN: int = 10

    def __eq__(self, other):
        return isinstance(other, Priority) and self.value == other.value and self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, Priority):
            raise TypeError(f"Error, cannot compare type '{type(other)}' with type 'Priority'.")
        return self.value < other.value

    def __le__(self, other):
        if not isinstance(other, Priority):
            raise TypeError(f"Error, cannot compare type '{type(other)}' with type 'Priority'.")
        return self.value <= other.value

    def __iter__(self):
        for v in [
            self.NEG_TWO,
            self.NEG_ONE,
            self.ONE,
            self.TWO,
            self.THREE,
            self.FOUR,
            self.FIVE,
            self.SIX,
            self.SEVEN,
            self.EIGHT,
            self.NINE,
            self.TEN,
        ]:
            yield v

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


@dataclass
class Attachment:
    id: int
    name: str
    file_path: str
    file_type: str


# @dataclass
class Task:
    idn: int  # id number
    name: str  # optional name
    due_date: datetime.datetime  # adjusted if due date is changed
    text: str
    priority: Priority
    comments: str = ""
    attachments: list = []
    state: State = State.QUEUED
    date_created: datetime.datetime = datetime.datetime.now()  # adjusted when requirement attributes are adjusted
    date_created_og: datetime.datetime = datetime.datetime.now()  # marks original request date
    due_date_og: datetime.datetime = None  # marks original due date

    def __init__(self, idn, name, due_date, text, priority, comments=None, attachments=None,
                 date_created=datetime.datetime.now(), date_created_og=datetime.datetime.now(), due_date_og=None):
        if attachments is None:
            attachments = []
        self.idn = idn
        self.name = name
        self.due_date = due_date
        self.text = text
        self.priority = priority
        self.comments = comments
        self.attachments = attachments
        self.date_created = date_created
        self.date_created_og = date_created_og
        self.due_date_og = due_date_og

        if self.due_date_og is None:
            self.due_date_og = self.due_date

    def __eq__(self, other):
        return isinstance(other, Task) and self.idn == other.idn

    @staticmethod
    def check_valid(input_, attr, allow_none=True):

        # is none and allowed to accept nones
        is_none = allow_none and not bool(input_)
        # must be a string, cannot be empty
        pop = bool(input_) and isinstance(input_, str)
        # is a date value
        is_date_ = is_date(input_)
        # can be empty, otherwise must be a populated string
        emp_or_pop = is_none or pop
        # can be empty, otherwise must be a date
        emp_or_date = is_none or is_date_
        # must be in the priorities string list
        is_priority = pop and (input_ in map(str, Priority))

        # print(f"{list(Priority)=}, {(input_ in list(Priority))=}")
        list_of_strings = isinstance(input_, (list, tuple)) and input_ and all(
            map(lambda x: isinstance(x, str) and x, input_))

        # print(f"{is_none=}, {pop=}, {is_date_=}, {emp_or_date=}, {emp_or_pop=}, {is_priority=}, {list_of_strings=}")

        match attr:
            case "name":
                return emp_or_pop
            case "date_created_og":
                return emp_or_date
            case "due_date":
                return is_date_
            case "text":
                return pop
            case "priority":
                return is_priority
            case "comments":
                return emp_or_pop
            case "date_created":
                return emp_or_date
            case "due_date_og":
                return emp_or_date
            case "attachments":
                return list_of_strings
            case _:
                raise ValueError(f"Error, attr '{attr}' not recognized.")

    def json_entry(self):
        # j = {1: datetime.datetime.now()}
        # print(f"{json.dumps(j)=}")
        return {
            "idn": self.idn,
            "name": self.name,
            "date_created_og": self.date_created_og,
            "date_created": self.date_created,
            "due_date_og": self.due_date_og,
            "due_date": self.due_date,
            "text": self.text,
            "comments": self.comments,
            "priority": self.priority,
            "attachments": self.attachments
        }

    def __repr__(self):
        return f"<Task due_date:{self.due_date}, text={self.text}>"


@dataclass
class TaskCell:
    task: Task
    tag: str = None
    bbox: tuple = None

    fill: Colour = Colour("#CCA0A0")
    active_fill: Colour = Colour("#CCA0A0").brighten(0.1)
    outline: Colour = Colour(BLACK)
    active_outline: Colour = Colour(BLACK).brighten(0.1)

    bg_check_expand: Colour = Colour("123456")
    active_bg_check_expand: Colour = Colour("123456").brighten(0.1)
    fg_check_expand: Colour = Colour("676555")
    active_fg_check_expand: Colour = Colour("676555").darken(0.1)

    is_expanded: bool = False

    fmt_task_due_date_long: str = "%Y-%m-%d %H:%M"
    fmt_task_due_date_short: str = lambda x: hours_until(x, rtype="h")

    tag_text_check: int = None
    tag_text_name: int = None
    tag_text_due: int = None
    tag_text_state: int = None

    # default_proportion, min_size, max_size
    # check, status, #, name, due, hrs
    p_width_check_expand = (0.05, 10, 35)
    p_width_status = (0.1, 15, 40)
    p_width_idn = (0.05, 10, 35)
    p_width_name = (0.40, 50, 300)
    p_width_due = (0.2, 50, 300)
    p_width_hrs = (0.2, 50, 300)


class TLSettings(tkinter.Toplevel):

    # sliders with int and value list ranges
    class OptionSlider(tkinter.Canvas):

        def __init__(self, master, options, default_value=None, width=300, height=80):
            super().__init__(master)
            self.configure(width=width, height=height, background=Colour("#AFCACF").hex_code)

            self.font_option_labels = tkinter.font.Font(self, font=("Arial", 10))

            self.continuous = False
            self.default_value = default_value
            self.value = tkinter.StringVar(self)

            self.width = width
            self.height = height
            self.margin_w = 5
            self.dims = [0, 0, width, height]

            self.options = options
            self.option_tags = []
            self.option_label_tags = []
            self.lngst_opt_label = sorted([opt for opt in self.options], key=lambda o: len(str(o)), reverse=True)
            self.width_option_label = (self.width - (2 * self.margin_w)) / len(self.options)
            self.rotate_option_labels = [
                self.font_option_labels.measure(opt) > (
                        self.width_option_label +
                        sum(map(lambda o: self.font_option_labels.measure(o) / 2, self.options[i-1:i] + self.options[i+1:i+2])))
                for i, opt in enumerate(self.options)]
            self.y_option_label = self.height * 0.45
            print(f"{self.rotate_option_labels=}")

            self.height_option_label = 12
            self.slider_width = 10
            self.slider_height = 15
            self.line_width = 6
            self.y_slider = self.height * 0.06

            self.dims_slider = {
                "x1": (self.width * 0.5) - (self.slider_width * 0.5),
                "y1": self.y_slider,
                "x2": (self.width * 0.5) + (self.slider_width * 0.5),
                "y2": self.y_slider + self.slider_height
            }

            pts = [
                (self.dims_slider["x1"], self.dims_slider["y1"]),
                (self.dims_slider["x2"], self.dims_slider["y1"]),
                (self.dims_slider["x2"], self.dims_slider["y2"] - (self.slider_height / 3)),
                (self.dims_slider["x1"] + (self.slider_width * 0.5), self.dims_slider["y2"]),
                (self.dims_slider["x1"], self.dims_slider["y2"] - (self.slider_height / 3)),
            ]
            self.slider = self.create_polygon(pts, fill="#456724")
            self.y_line = self.dims_slider["y2"] + (self.line_width * 0.5)
            self.line = self.create_line(
                self.margin_w,
                self.y_line,
                self.width - self.margin_w,
                self.y_line,
                fill="#ACEFAC",
                width=self.line_width
            )

            self.tag_bind(self.line, "<ButtonRelease-1>", self.click_line)
            self.tag_bind(self.slider, "<B1-Motion>", self.drag_slider)
            w_s = self.font_option_labels.measure(" ")
            tol = 6
            n_s = int((self.width_option_label - tol) // w_s)
            for i, opt in enumerate(self.options):
                # t = f"{'|'.center(n_s, chr(ord('.') + i))}\n"
                t = f"{'|'.center(n_s)}\n"
                l = ""
                dc = True
                ln = 2
                for j, c in enumerate(opt):
                    l += c
                    if self.font_option_labels.measure(l) > (self.width_option_label - tol):
                        l_space = lstindex(l, " ")
                        if l_space > -1:
                            l = l[:l_space] + f"\n{l[l_space:]}"
                        else:
                            l = l[:-2] + f"-\n{l[-2]}{c}"
                        # print(f"{opt=}, {n_s=}, {l=}, {c=} {l_space=}")
                        # t += l.center(n_s)
                        t += l
                        l = ""
                        dc = False
                        ln += 1
                    # else:
                    #     dc = True
                # t += l.center(n_s, "_") if dc else l
                t += l.center(n_s) if dc else l
                self.option_tags.append(self.create_rectangle(
                    self.margin_w + (i * self.width_option_label),
                    self.y_option_label - (self.height_option_label * 0.5),
                    self.margin_w + ((i + 1) * self.width_option_label),
                    self.y_option_label + (self.height_option_label * ln)
                    # ,
                    # fill=random_colour(rgb=False)
                ))
                self.option_label_tags.append(self.create_text(
                    self.margin_w + (self.width_option_label * 0.5) + (i * self.width_option_label),
                    self.y_option_label + (self.height_option_label * 0.5),
                    text=t,
                    font=self.font_option_labels,
                    justify=tkinter.CENTER
                ))
                self.tag_bind(self.option_tags[-1], "<ButtonRelease-1>", lambda event, x_=self.margin_w + (i * self.width_option_label): self.set_slider(x_))
                self.tag_bind(self.option_label_tags[-1], "<ButtonRelease-1>", lambda event, x_=self.margin_w + (i * self.width_option_label): self.set_slider(x_))

            if self.default_value is not None:
                self.set_slider(self.default_value)

        def drag_slider(self, event):
            # print(f"drag slider {event=}")
            self.set_slider(event.x)

        def click_line(self, event):
            # print(f"click line {event=}")
            self.set_slider(event.x)

        def set_slider(self, pos):
            if isinstance(pos, (int, float)):
                x, y = pos, self.y_slider
            elif isinstance(pos, (tuple, list)):
                x, y = pos
            elif isinstance(pos, str):
                if (idx := lstindex(self.options, pos)) >= 0:
                    x, y = self.margin_w + (idx * self.width_option_label), self.y_slider
                else:
                    raise ValueError(f"Error, cannot use value '{pos}' as param 'pos'.")
            else:
                raise ValueError(f"Error, cannot use value '{pos}' as param 'pos'.")

            if self.continuous:
                self.dims_slider.update({
                    "x1": clamp(self.margin_w, int(round(x - (self.slider_width * 0.5))), self.width - self.margin_w),
                    "y1": int(round(y)),
                    "x2": clamp(self.margin_w, int(round(x + (self.slider_width * 0.5))), self.width - self.margin_w),
                    "y2": int(round(y + self.slider_height))
                })
            else:
                bi = int(clamp(0, x // self.width_option_label, len(self.options) - 1))
                x = (self.width_option_label * bi) + (self.width_option_label * 0.5)
                self.dims_slider.update({
                    "x1": clamp(self.margin_w, int(round(x - (self.slider_width * 0.5))), self.width - self.margin_w),
                    "y1": int(round(y)),
                    "x2": clamp(self.margin_w, int(round(x + (self.slider_width * 0.5))), self.width - self.margin_w),
                    "y2": int(round(y + self.slider_height))
                })
                self.value.set(self.options[bi])
                # print(f"NV: {self.value.get()}")

            pts = [
                clamp(
                    self.margin_w,
                    int(round(self.dims_slider["x1"])),
                    self.width - self.margin_w - self.slider_width)
                , int(round(self.dims_slider["y1"])),
                clamp(
                    self.margin_w + self.slider_width,
                    int(round(self.dims_slider["x2"])),
                    self.width - self.margin_w)
                , int(round(self.dims_slider["y1"])),
                clamp(
                    self.margin_w + self.slider_width,
                    int(round(self.dims_slider["x2"])),
                    self.width - self.margin_w)
                , int(round(self.dims_slider["y2"] - (self.slider_height / 3))),
                clamp(
                    self.margin_w,
                    int(round(self.dims_slider["x1"] + (self.slider_width * 0.5))),
                    self.width - self.margin_w - (self.slider_width * 0.5))
                , int(round(self.dims_slider["y2"])),
                clamp(
                    self.margin_w,
                    int(round(self.dims_slider["x1"])),
                    self.width - self.margin_w - self.slider_width),
                int(round(self.dims_slider["y2"] - (self.slider_height / 3))),
            ]
            pts = pts + pts[0:2]
            # print(f"set slider {pts=}")
            self.coords(self.slider, *pts)

    def __init__(self, master, settings):
        super().__init__(master)

        self.title("Task Organizer Settings")
        self.geometry(calc_geometry_tl(width=0.72, height=0.48))

        # due time unit
        # days, hrs, mins, secs, total

        # number of digits for the due time unit

        # auto expand all tasks on load
        # self.columnconfigure(1, weight=100)
        self.columnconfigure(0, weight=50)
        self.columnconfigure(1, weight=50)

        self.settings = settings
        self.frames = []
        self.widgets = []
        for i, k_v in enumerate(settings.items()):
            k, v = k_v
            f = tkinter.Frame(self)
            self.frames.append(f)
            fl = tkinter.Frame(f)
            fw = tkinter.Frame(f)

            widget = v["widget"]
            kwargs = v["kwargs"]

            tv_lbl, lbl = label_factory(
                fl, tv_label=k
            )

            r, c, rs, cs, ix, iy, x, y, s = grid_keys()

            match widget:
                case "slider":
                    v = kwargs["default_value"]
                    if v == "d":
                        kwargs["default_value"] = "Days"
                    if v == "h":
                        kwargs["default_value"] = "Hours"
                    if v == "m":
                        kwargs["default_value"] = "Minutes"
                    if v == "s":
                        kwargs["default_value"] = "Seconds"
                    if v == "t":
                        kwargs["default_value"] = "Minimum"
                    if v == "tt":
                        kwargs["default_value"] = "Total"
                    widget = TLSettings.OptionSlider(fw, **kwargs)
                case _:
                    raise ValueError(f"Error, unsure what to do with widget entry '{widget}'.")

            self.widgets.append(widget)

            lbl.grid(**{r: 0, c: 0, s: "nsew"})
            widget.grid(**{r: 0, c: 0, s: "nsew"})
            fl.grid(**{r: 0, c: 0, s: "nsew"})
            fw.grid(**{r: 0, c: 1, s: "nsew"})
            f.grid(**{r: i, c: 0, s: "nsew"})
            fw.columnconfigure(0, weight=100)
            fl.columnconfigure(0, weight=100)
            f.columnconfigure(0, weight=50)
            f.columnconfigure(1, weight=50)

        # self.option_slider1 = TLSettings.OptionSlider(self, options=["yes", "no", "cancel"])
        # self.option_slider1.grid()
        # self.option_slider2 = TLSettings.OptionSlider(self, options=["Please take me back", "yes", "no", "cancel", "Cat in a hat", "Dog", "Mouse", "Parrot", "Squirrel"])
        # self.option_slider2.grid()

        self.grab_set()


class App(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.task_id_generator = None
        self.priorities_list = list(Priority)
        self.combo_priorities_list = self.priorities_list[2:]
        self.showing_input_form = tkinter.BooleanVar(self, value=False)
        self.editing_input_form = tkinter.BooleanVar(self, value=False)
        self.show_full_due_date = tkinter.BooleanVar(self, value=False)

        self.colours = {
            State.QUEUED: {
                "bg": Colour(GRAY_60),
                "active_bg": Colour(GRAY_60).brighten(0.1),
                "fg": Colour(BLACK),
                "outline": Colour(GRAY_45),
                "active_outline": Colour(GRAY_45)
            },
            State.EXPIRED: {
                "bg": Colour("#CCA0A0"),
                "active_bg": Colour("#CCA0A0").brighten(0.1),
                "fg": Colour(BLACK),
                "outline": Colour("#782111"),
                "active_outline": Colour("#782111").brighten(0.1)
            }
        }
        dims = calc_geometry_tl(0.81, 0.54, rtype=dict)
        self.geometry(dims["geometry"])
        self.p_width_canvas, self.p_height_canvas = 0.8, 0.9
        self.width_canvas, self.height_canvas = int(round(dims["width"] * self.p_width_canvas)), int(round(dims["height"] * self.p_height_canvas))
        self.canvas = tkinter.Canvas(
            self,
            width=self.width_canvas,
            height=self.height_canvas,
            bg=Colour("#664242").hex_code,
            # ,
            # scrollregion=(0, 0, self.width_canvas*2, self.height_canvas*10)
            scrollregion=(0, 0, self.width_canvas, self.height_canvas * 10)
        )
        self.v_scrollbar = tkinter.Scrollbar(
            self,
            command=self.canvas.yview,
            orient="vertical"
        )
        self.h_scrollbar = tkinter.Scrollbar(
            self,
            command=self.canvas.xview,
            orient="horizontal"
        )
        # self.canvas.configure(yscrollcommand=self.v_scrollbar_set, xscrollcommand=self.h_scrollbar_set)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.canvas.bind("<MouseWheel>",
                         lambda event: self.canvas.yview('scroll', int(-1 * (event.delta / 120)), 'units'))

        self.tv_btn_new_task, \
            self.btn_new_task \
            = button_factory(
            self,
            tv_btn="+",
            command=self.click_new_btn
        )

        self.tv_btn_settings, \
            self.btn_settings \
            = button_factory(
            self,
            tv_btn="settings",
            command=self.click_settings
        )

        self.tv_checkbox_submit_on_close, \
            self.checkbox_submit_on_close \
            = checkbox_factory(
            self,
            buttons=["submit on close"],
            default_values=[False]
        )
        self.tv_checkbox_submit_on_close = self.tv_checkbox_submit_on_close[0]
        self.checkbox_submit_on_close = self.checkbox_submit_on_close[0]

        self.frame_task_input = tkinter.Frame(self, name="f_task_input")

        # Name
        self.tv_lbl_tsk_inp_name, \
            self.lbl_tsk_inp_name, \
            self.tv_entry_tsk_inp_name, \
            self.entry_tsk_inp_name \
            = entry_tip_factory(
            self.frame_task_input,
            tip="Optional",
            tv_label="Name:",
            kwargs_entry={
                "width": 50
            }
        )
        # self.entry_tsk_inp_name.bind("<KeyDown>", )

        # Text
        self.tv_lbl_tsk_inp_text, \
            self.lbl_tsk_inp_text \
            = label_factory(
            self.frame_task_input,
            tv_label="Text:"
        )
        self.tsk_inp_text = TextWithVar(
            self.frame_task_input,
            width=50,
            height=6
        )

        # Comments
        self.tv_lbl_tsk_inp_comments, \
            self.lbl_tsk_inp_comments \
            = label_factory(
            self.frame_task_input,
            tv_label="Comments:"
        )
        self.tsk_inp_comments = TextWithVar(
            self.frame_task_input,
            width=50,
            height=6
        )

        # Priority
        self.tv_lbl_tsk_inp_priority, \
            self.lbl_tsk_inp_priority, \
            self.tv_combo_tsk_inp_priority, \
            self.combo_tsk_inp_priority, \
            = combo_factory(
            self.frame_task_input,
            tv_label="Priority:",
            values=self.combo_priorities_list
        )

        # Due Date
        self.tv_lbl_tsk_inp_due_date, \
            self.lbl_tsk_inp_due_date \
            = label_factory(
            self.frame_task_input,
            tv_label="Due Date:"
        )
        self.odp_due_date = OrbitingDatePicker(
            self.frame_task_input,
            start_date=datetime.datetime.now()
        )

        # Due Time
        self.due_time_slider = TimeSlider(
            self.frame_task_input
        )

        # clear button
        self.tv_btn_tsk_inp_clear, \
            self.btn_tsk_inp_clear \
            = button_factory(
            self.frame_task_input,
            tv_btn="clear",
            command=self.click_clear_input_form
        )

        # submit button
        self.tv_btn_tsk_inp_submit, \
            self.btn_tsk_inp_submit \
            = button_factory(
            self.frame_task_input,
            tv_btn="submit",
            command=self.click_submit_input_form
        )

        r, c, rs, cs, ix, iy, x, y, s = grid_keys()
        self.grid_args = {
            "btn_new_task": {r: 0, c: 0},
            "checkbox_submit_on_close": {r: 0, c: 2},
            "btn_settings": {r: 1, c: 2},
            "frame_task_input": {r: 2, c: 0},
            "canvas": {r: 3, c: 0},
            "v_scrollbar": {r: 3, c: 1, s: "ns"},
            "h_scrollbar": {r: 4, c: 0, s: "ew"},

            # frame_task_input
            "lbl_tsk_inp_name": {r: 0, c: 0},
            "entry_tsk_inp_name": {r: 1, c: 0},
            "lbl_tsk_inp_due_date": {r: 0, c: 1},
            "odp_due_date": {r: 1, c: 1},
            "due_time_slider": {r: 1, c: 2},
            "lbl_tsk_inp_text": {r: 2, c: 0},
            "tsk_inp_text": {r: 3, c: 0},
            "lbl_tsk_inp_comments": {r: 2, c: 1},
            "tsk_inp_comments": {r: 3, c: 1},
            "lbl_tsk_inp_priority": {r: 2, c: 2},
            "combo_tsk_inp_priority": {r: 3, c: 2},
            "btn_tsk_inp_clear": {r: 4, c: 0},
            "btn_tsk_inp_submit": {r: 4, c: 1}

            # ,
            #     "": {r: , c: },
            #     "": {r: , c: },
        }

        self.init_grid_args = {
            "btn_new_task",
            "btn_settings",
            "checkbox_submit_on_close",
            "canvas",
            "v_scrollbar",
            "h_scrollbar",
            "lbl_tsk_inp_due_date",
            "odp_due_date",
            "due_time_slider",
            "lbl_tsk_inp_name",
            "entry_tsk_inp_name",
            "lbl_tsk_inp_text",
            "tsk_inp_text",
            "tsk_inp_comments",
            "lbl_tsk_inp_comments",
            "lbl_tsk_inp_priority",
            "combo_tsk_inp_priority",
            "btn_tsk_inp_clear",
            "btn_tsk_inp_submit"
        }

        self.width_task_cell, self.height_task_cell = self.width_canvas, 60
        self.height_expanded_task_cell = 200
        self.margin_task_horizontal, self.margin_task_vertical = 2, 5

        self.tl_settings = None
        self.settings_s_width = 600
        self.settings = {
            "Auto-expand tasks on application open:": {
                "desc": "On start-up, all the tasks will be fully expanded",
                "widget": "slider",
                "kwargs": {
                    "options": ["Yes", "No"],
                    "default_value": "No",
                    "width": self.settings_s_width
                },
                "value": None,
                "func": None
            },
            "Due-date time units": {
                "desc": "Days, Hours, Minutes, Seconds, Total, Min",
                "widget": "slider",
                "kwargs": {
                    "options": ["Total", "Days", "Hours", "Minutes", "Seconds", "Minimum"],
                    "default_value": "Hours",
                    "width": self.settings_s_width
                },
                "value": None,
                "func": self.set_due_date_units
            }
        }

        self.file_tasks = r".\task_manager_records.json"
        self.tasks = []
        self.threads = {}
        self.found_settings = False
        self.load_tasks()

        for k, t in self.threads.items():
            t.join()

        if self.found_settings:
            print(f"Loaded settings!")
            self.apply_settings()

        self.init_tasks()
        self.grid_init()

        self.protocol_oc = self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(1000, self.task_timer)

    def task_timer(self):
        if self.tasks:
            now = datetime.datetime.now()
            for i, tc in enumerate(self.tasks):
                t = tc.task
                td = tc.tag_text_due

                if not t.state.is_timed_state():
                    continue

                fmt_due = tc.fmt_task_due_date_long
                if not self.show_full_due_date.get():
                    fmt_due = tc.fmt_task_due_date_short
                    if callable(fmt_due):
                        text_due = fmt_due(t.due_date)
                    else:
                        text_due = t.due_date.strftime(fmt_due)
                else:
                    text_due = t.due_date.strftime(fmt_due)

                # check_expiry
                if t.due_date < now and t.state != State.EXPIRED:
                    self.set_task_expired(tc)

                self.canvas.itemconfigure(td, text=text_due)
            self.after(1000, self.task_timer)

    def set_task_expired(self, tc: TaskCell):
        print(f"Set Expired {tc.task}")
        tc.task.state = State.EXPIRED
        tc.fill = self.colours[State.EXPIRED]["bg"]
        tc.active_fill = self.colours[State.EXPIRED]["active_bg"]
        tc.outline = self.colours[State.EXPIRED]["outline"]
        tc.active_outline = self.colours[State.EXPIRED]["active_outline"]
        self.canvas.itemconfigure(tc.tag_text_state, text=tc.task.state.value[2])
        self.redraw_tasks(tc)

    def v_scrollbar_set(self, *args):
        print(f"v scroll {args=}")
        self.v_scrollbar.set(*args)

    def h_scrollbar_set(self, *args):
        print(f"h scroll {args=}")
        self.h_scrollbar.set(*args)

    def on_close(self, event=None):
        print(f"closing")
        if self.tv_checkbox_submit_on_close.get():
            if self.tasks or self.found_settings:
                sett = self.settings
                sett = {"settings_data": {k: sett[k]["value"] for k in sett if sett[k]["value"]}}
                with open(self.file_tasks, "w") as f:
                    # res = {str(i): jsonify(t.task.json_entry()) for i, t in enumerate(self.tasks)}
                    # res = {str(i): t.task.json_entry() for i, t in enumerate(self.tasks)}
                    tsks = dict(sett)
                    tsks.update({str(i): t.task.json_entry() for i, t in enumerate(self.tasks)})
                    res = jsonify(tsks, in_line=0)
                    print("XX" + jsonify({str(i): t.task.json_entry() for i, t in enumerate(self.tasks)}, in_line=0))
                    # print(f"{res=}")
                    # res =
                    # json.dump(res, f)
                    f.write(res)
                    print(f"{res=}")
        self.destroy()

    def grid_init(self):
        for k in self.init_grid_args:
            args = self.grid_args[k]
            eval(f"self.{k}.grid(**{args})")

    def init_colours(self):
        if self.tasks:
            cols = self.colours
            for tc in self.tasks:
                s = tc.task.state
                bg = self.colours[s]["bg"]
                a_bg = self.colours[s]["active_bg"]
                out = self.colours[s]["outline"]
                a_out = self.colours[s]["active_outline"]

                tc.fill = bg
                tc.active_fill = a_bg
                tc.outline = out
                tc.active_outline = a_out

    def init_tasks(self):
        self.init_colours()
        the = self.height_expanded_task_cell
        x, y, tw, th = 0, 0, self.width_task_cell, self.height_task_cell
        mh, mv = self.margin_task_horizontal, self.margin_task_vertical
        for i, t in enumerate(self.tasks):
            th_ = the if t.is_expanded else th
            bbox = x + mh + mh, y + (mv if i == 0 else 0), x + tw - (1 * mh), y + th_ - (1 * mv)
            self.draw_task(t, bbox)
            y += th_

    def new_task(self, task_in: TaskCell):
        the = self.height_expanded_task_cell
        x, y, tw, th = 0, 0, self.width_task_cell, self.height_task_cell
        mh, mv = self.margin_task_horizontal, self.margin_task_vertical
        n_prev = len(self.tasks)
        n_reg = len([t for t in self.tasks if not t.is_expanded])
        n_exp = n_prev - n_reg
        # y += ((n_reg * th) + (max(0, n_reg - 2) * mv)) + (n_exp * the)
        y += ((n_reg * th) + (n_exp * the))
        bbox = x + mh + mh, y + (mv if n_prev == 0 else 0), x + tw - (1 * mh), y + th - (1 * mv)
        self.draw_task(task_in, bbox=bbox)
        self.tasks.append(task_in)

    def redraw_tasks(self, start: int | TaskCell = 0):

        if isinstance(start, TaskCell):
            start = self.tasks.index(start)

        the = self.height_expanded_task_cell
        x, y, tw, th = 0, 0, self.width_task_cell, self.height_task_cell
        mh, mv = self.margin_task_horizontal, self.margin_task_vertical
        n_prev = start
        # n_prev = len(self.tasks[:start])
        n_reg = len([t for t in self.tasks[:start] if not t.is_expanded])
        n_exp = n_prev - n_reg
        # y += ((n_reg * th) + (max(0, n_reg - 2) * mv)) + (n_exp * the)
        y += ((n_reg * th) + (n_exp * the))
        for i, t in enumerate(self.tasks[start:]):

            c_fill = t.fill.hex_code
            c_outl = t.outline.hex_code
            c_acfi = t.active_fill.hex_code
            c_acou = t.active_outline.hex_code

            th_ = the if t.is_expanded else th
            bbox = x + mh + mh, y + (mv if start + i == 0 else 0), x + tw - (1 * mh), y + th_ - (1 * mv)
            # self.canvas.moveto(t.tag, *bbox[:2])
            self.canvas.coords(t.tag, *bbox)
            # print(f"RD {start=}, {i=} BBOX: {bbox}, old={t.bbox}")
            t.bbox = bbox

            dims = self.calc_task_dims(t)
            self.canvas.coords(t.tag_text_check, dims["bbox_check"])
            self.canvas.itemconfigure(t.tag_text_check, height=dims["h"])
            self.canvas.coords(t.tag_text_name, dims["bbox_name"])
            self.canvas.coords(t.tag_text_due, dims["bbox_due"])
            self.canvas.coords(t.tag_text_state, dims["bbox_status"])
            self.canvas.itemconfigure(t.tag, fill=c_fill, outline=c_outl, activefill=c_acfi, activeoutline=c_acou)

            # self.draw_task(t, bbox)
            y += th_

    def draw_task(self, task_in: TaskCell, bbox=None):
        # assert isinstance(task_in, TaskCell)
        if bbox is None:
            bbox = task_in.bbox

        dims = self.calc_task_dims(task_in, bbox)
        fmt_due = task_in.fmt_task_due_date_long

        c_fill = task_in.fill.hex_code
        c_outl = task_in.outline.hex_code
        c_acfi = task_in.active_fill.hex_code
        c_acou = task_in.active_outline.hex_code

        c_cbbg = task_in.bg_check_expand.hex_code
        c_cbab = task_in.active_bg_check_expand.hex_code
        c_cbfg = task_in.fg_check_expand.hex_code
        c_cbaf = task_in.active_fg_check_expand.hex_code

        tag_rect = self.canvas.create_rectangle(
            *bbox,
            fill=c_fill,
            outline=c_outl,
            activefill=c_acfi,
            activeoutline=c_acou
        )

        if not self.show_full_due_date.get():
            fmt_due = task_in.fmt_task_due_date_short
            if callable(fmt_due):
                text_due = fmt_due(task_in.task.due_date)
            else:
                text_due = task_in.task.due_date.strftime(fmt_due)
        else:
            text_due = task_in.task.due_date.strftime(fmt_due)

        text_name = task_in.task.text[:25]
        text_status = task_in.task.state.value[2]

        check_box_f = checkbox_factory(self.canvas, buttons=[""], default_values=[False])
        # print(f"{check_box_f=}")
        tv_check_box, check_box = check_box_f
        tv_check_box, check_box = tv_check_box[0], check_box[0]
        check_box.configure(bg=c_cbbg, activebackground=c_cbab, fg=c_cbfg, activeforeground=c_cbaf)

        tag_check = self.canvas.create_window(
            dims["x_check"],
            dims["y_check"],
            width=dims["w_check"],
            height=dims["h_check"],
            window=check_box
        )

        tag_status = self.canvas.create_text(
            dims["x_status"],
            dims["y_status"],
            text=text_status
        )

        tag_name = self.canvas.create_text(
            dims["x_name"],
            dims["y_name"],
            text=text_name
        )

        tag_due = self.canvas.create_text(
            dims["x_due"],
            dims["y_due"],
            text=text_due
        )
        self.canvas.tag_bind(tag_rect, "<Double-Button-1>", lambda event, t_=task_in: self.dbl_click_task(event, t_))
        if bbox is not None:
            task_in.bbox = bbox
        task_in.tag = tag_rect
        task_in.tv_check_expanded = tv_check_box
        task_in.tag_text_check = tag_check
        task_in.tag_text_name = tag_name
        task_in.tag_text_due = tag_due
        task_in.tag_text_state = tag_status

    @staticmethod
    def calc_task_dims(task_in: TaskCell, bbox=None):

        if bbox is None:
            bbox = task_in.bbox

        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # check, status, #, name, due, hrs
        p_check = task_in.p_width_check_expand
        p_status = task_in.p_width_status
        p_idn = task_in.p_width_idn
        p_name = task_in.p_width_name
        p_due = task_in.p_width_due
        p_hrs = task_in.p_width_hrs

        w_check = p_check[0] * w
        w_status = p_status[0] * w
        w_idn = p_idn[0] * w
        w_name = p_name[0] * w
        w_due = p_due[0] * w
        w_hrs = p_hrs[0] * w

        h_check = h
        h_status = h
        h_idn = h
        h_name = h
        h_due = h
        h_hrs = h

        # print(f"{p_check=}")
        # print(f"{p_check[0]=}")

        x_check, y_check = bbox[0] + (w_check * 0.5), bbox[1] + (h * 0.5)
        x_status, y_status = x_check + w_check + (w_check * 0.5), bbox[1] + (h * 0.5)
        x_idn, y_idn = x_status + w_status, bbox[1]
        x_name, y_name = x_idn + w_idn + (w_name * 0.5), bbox[1] + (h * 0.5)
        x_due, y_due = x_name + w_name + (w_due * 0.5), bbox[1] + (h * 0.5)
        x_hrs, y_hrs = x_due + w_due, bbox[1]

        return {
            "w": w,
            "h": h,

            "x_check": x_check,
            "y_check": y_check,
            "w_check": w_check,
            "h_check": h_check,
            "bbox_check": (x_check, y_check),

            "x_status": x_status,
            "y_status": y_status,
            "w_status": w_status,
            "h_status": h_status,
            "bbox_status": (x_status, y_status),

            "x_idn": x_idn,
            "y_idn": y_idn,
            "w_idn": w_idn,
            "h_idn": h_idn,

            "x_name": x_name,
            "y_name": y_name,
            "w_name": w_name,
            "h_name": h_name,
            "bbox_name": (x_name, y_name),

            "x_due": x_due,
            "y_due": y_due,
            "w_due": w_due,
            "h_due": h_due,
            "bbox_due": (x_due, y_due),

            "x_hrs": x_hrs,
            "y_hrs": y_hrs,
            "w_hrs": w_hrs,
            "h_hrs": h_hrs
        }

    def dbl_click_task(self, event, task):
        # print(f"{task=}")
        task.is_expanded = not task.is_expanded
        idx = self.tasks.index(task)
        # print(f"double click: {idx=}")
        self.redraw_tasks(idx)

    def load_tasks(self):
        print(f"Loading tasks... ", end="")

        def sub_load_tasks():
            fn = self.file_tasks
            tasks = []
            self.found_settings = False
            try:
                with open(fn, "r") as f:
                    # print(f"{f.read()}")
                    lines = json.load(f)
                    for i, k_raw_task_data in enumerate(lines.items()):
                        key, raw_task_data = k_raw_task_data
                        print(f"{i=}, {raw_task_data=}")
                        if key == "settings_data":
                            for sk, sv in raw_task_data.items():
                                self.settings[sk]["value"] = sv
                                self.settings[sk]["kwargs"]["default_value"] = sv
                            self.found_settings = True
                        else:
                            # idn, name, due_date, text, priority, comments, attachments, date_created, date_created_og, due_date_og,
                            tasks.append(TaskCell(Task(
                                raw_task_data.get("idn", i),
                                raw_task_data.get("name"),
                                eval(raw_task_data.get("due_date")),
                                raw_task_data.get("text"),
                                raw_task_data.get("priority"),
                                raw_task_data.get("comments"),
                                raw_task_data.get("attachments"),
                                eval(raw_task_data.get("date_created")),
                                eval(raw_task_data.get("date_created_og")),
                                eval(raw_task_data.get("due_date_og"))
                            )))

            except FileNotFoundError:
                print(f"\nfile '{fn}' not found.")
                self.make_task_file()
            except PermissionError:
                print(f"\nfile '{fn}' could not be opened due to permission.")

            n = len(tasks)
            if n:
                # print(f"{n} task{'s' if n != 1 else ''} loaded!")
                print(f"{n} loaded!")
            else:
                print(f"None found.")

            self.tasks = tasks
            self.task_id_generator = (i for i in range(n, 10000))

        self.threads["load_tasks"] = Thread(target=sub_load_tasks)
        self.threads["load_tasks"].start()

    def make_task_file(self):
        with open(self.file_tasks, "w") as f:
            f.write("{}")
            f.close()
        print(f"Task file creation successful.")

    def apply_settings(self):
        for k, v in self.settings.items():
            if v["value"] is not None:
                v["func"]()

    def click_clear_input_form(self):
        print(f"click_clea_input_form")
        self.tv_entry_tsk_inp_name.set("")
        self.odp_due_date.date = datetime.datetime.now()
        self.tv_combo_tsk_inp_priority.set("")
        self.tsk_inp_text.text.set("")
        self.tsk_inp_comments.text.set("")

    def click_submit_input_form(self):
        print(f"click_clea_input_form")

        # name, due_date, text, priority, comments, attachments, date_created, date_created_og, due_date_og = [None for _
        #                                                                                                      in
        #                                                                                                      range(9)]

        hr, mn, pr = self.due_time_slider.time_picker.time()
        hr += 0 if pr == "AM" else 12

        vars = [
            self.tv_entry_tsk_inp_name.get().strip(),
            self.odp_due_date.date + datetime.timedelta(hours=hr, minutes=mn),
            self.tsk_inp_text.text.get().strip(),
            self.tv_combo_tsk_inp_priority.get().strip(),
            self.tsk_inp_comments.text.get().strip()
        ]
        ctls = [
            self.entry_tsk_inp_name,
            self.odp_due_date.dateentry_entry,
            self.tsk_inp_text,
            self.combo_tsk_inp_priority,
            self.tsk_inp_comments
        ]
        attrs = [
            "name",
            "due_date",
            "text",
            "priority",
            "comments"
        ]
        lvars = {a: None for a in attrs}
        # lvars = [
        #     name,
        #     due_date,
        #     priority,
        #     text,
        #     comments
        #     ,
        #     attachments := None,
        #     date_created := None,
        #     date_created_og := None,
        # due_date_og := None
        # ]

        # name = self.tv_entry_tsk_inp_name.get()
        # due_date = self.odp_due_date.date
        # priority = self.tv_combo_tsk_inp_priority.get()
        # text = self.tsk_inp_text.text.get()
        # comments = self.tsk_inp_comments.text.get()

        print(f"tip: {self.entry_tsk_inp_name.getvar('tip')}")
        replace_values = {
            "name": (self.entry_tsk_inp_name.getvar("tip"), "")
        }
        invalid_values = {}

        valid = True

        print(f"1> {lvars=}")

        for i, z_dat in enumerate(zip(vars, attrs, ctls, lvars)):
            input_, attr, ctl, var = z_dat
            input_ = input_ if (attr not in replace_values) else input_.replace(*replace_values[attr])
            valid = Task.check_valid(input_, attr) and (input_ not in invalid_values.get(attr, []))
            print(f"{attr=}, {input_=}, {valid=}\n")
            if not valid:
                print(f"Need input for attr='{attr}'")
                ctl.focus_set()
                break
            lvars[attr] = input_

        print(f"2> {lvars=}")

        if valid:
            idn = next(self.task_id_generator)

            # idn, name, due_date, text, priority, comments, attachments, date_created, date_created_og, due_date_og,
            t = Task(idn, *[lvars[k] for k in attrs])
            print(f"SUBMISSION!")
            print(f"{t=}")
            tc = TaskCell(t)
            self.new_task(tc)
            # t = Task(idn, name, due_date, text, priority, comments, attachments, date_created, date_created_og, due_date_og)

        # print(f"{name=}, {due_date=}, {priority=}, {text=}, {comments=}")

        # inputs = [name, due_date, priority, text, comments]

        # for input_, attr in zip(inputs, attrs):
        # print(f"{attr=}, {input_=}, {Task.check_valid(input_, attr)=}\n")

    def click_new_btn(self):
        print(f"click new task")
        self.show_task_input_form()

    def click_settings(self):
        print(f"click settings")
        self.show_settings_menu()

    def show_settings_menu(self):
        s_width = 600
        self.tl_settings = TLSettings(self, self.settings)
        self.tl_settings.protocol("WM_DELETE_WINDOW", self.tl_settings_on_close)
        self.wait_window(self.tl_settings)

    def tl_settings_on_close(self, event=None):
        print("settings_tl on_close")
        sett = self.settings
        for k, w in zip(self.tl_settings.settings, self.tl_settings.widgets):
            print(f"{k=}: {w.value.get()=}")
        self.apply_settings()
        self.found_settings = True
        self.tl_settings.destroy()

    def show_task_input_form(self):
        showing = self.showing_input_form.get()
        if showing:
            # now hide
            self.frame_task_input.grid_forget()
        else:
            # now show
            self.frame_task_input.grid(**self.grid_args["frame_task_input"])

        self.showing_input_form.set(not showing)

    def set_due_date_units(self):
        v = self.settings["Due-date time units"]["value"]

        if v == "Days":
            v = "d"
        if v == "Hours":
            v = "h"
        if v == "Minutes":
            v = "m"
        if v == "Seconds":
            v = "s"
        if v == "Minimum":
            v = "t"
        if v == "Total":
            v = "tt"

        for tc in self.tasks:
            tc.fmt_task_due_date_short = lambda x: hours_until(x, rtype=v)


if __name__ == '__main__':
    app = App()
    app.mainloop()

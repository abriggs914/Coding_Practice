import enum
import json
import tkinter
from threading import Thread
from dataclasses import dataclass

from datetime_utility import is_date
from json_utility import jsonify
from orbiting_date_picker import OrbitingDatePicker
from tkinter_utility import *


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
    date_created: datetime.datetime = datetime.datetime.now()  # adjusted when requirement attributes are adjusted
    date_created_og: datetime.datetime = datetime.datetime.now()  # marks original request date
    due_date_og: datetime.datetime = None  # marks original due date

    def __init__(self, idn, name, due_date, text, priority, comments=None, attachments=None, date_created=datetime.datetime.now(), date_created_og=datetime.datetime.now(), due_date_og=None):
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
    is_expanded: bool = False

    tag_text_name: int = None

    # default_proportion, min_size, max_size
    # check, status, #, name, due, hrs
    p_width_check_expand = (0.05, 10, 35)
    p_width_status = (0.1, 15, 40)
    p_width_idn = (0.05, 10, 35)
    p_width_name = (0.40, 50, 300)
    p_width_due = (0.2, 50, 300)
    p_width_hrs = (0.2, 50, 300)


class App(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.task_id_generator = None
        self.priorities_list = list(Priority)
        self.combo_priorities_list = self.priorities_list[2:]
        self.showing_input_form = tkinter.BooleanVar(self, value=False)
        self.editing_input_form = tkinter.BooleanVar(self, value=False)

        dims = calc_geometry_tl(0.54, 0.36, rtype=dict)
        self.geometry()
        self.width_canvas, self.height_canvas = dims["width"], dims["height"]
        self.canvas = tkinter.Canvas(
            self,
            width=self.width_canvas,
            height=self.height_canvas,
            bg=Colour("#664242").hex_code,
            # ,
            scrollregion=(0, 0, self.width_canvas*2, self.height_canvas*10)
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
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.tv_btn_new_task, \
            self.btn_new_task \
            = button_factory(
            self,
            tv_btn="+",
            command=self.click_new_btn
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
            "checkbox_submit_on_close": {r: 0, c: 1},
            "frame_task_input": {r: 1, c: 0},
            "canvas": {r: 2, c: 0},
            "v_scrollbar": {r: 2, c: 1, s: "ns"},
            "h_scrollbar": {r: 3, c: 0, s: "ew"},

            # frame_task_input
            "lbl_tsk_inp_name": {r: 0, c: 0},
            "entry_tsk_inp_name": {r: 1, c: 0},
            "lbl_tsk_inp_due_date": {r: 0, c: 1},
            "odp_due_date": {r: 1, c: 1},
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
            "checkbox_submit_on_close",
            "canvas",
            "v_scrollbar",
            "h_scrollbar",
            "lbl_tsk_inp_due_date",
            "odp_due_date",
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

        self.file_tasks = r".\task_manager_records.json"
        self.tasks = []
        self.threads = {}
        self.load_tasks()

        for k, t in self.threads.items():
            t.join()

        self.init_tasks()
        self.grid_init()

        self.protocol_oc = self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self, event=None):
        print(f"closing")
        if self.tv_checkbox_submit_on_close.get():
            if self.tasks:
                with open(self.file_tasks, "w") as f:
                    # res = {str(i): jsonify(t.task.json_entry()) for i, t in enumerate(self.tasks)}
                    # res = {str(i): t.task.json_entry() for i, t in enumerate(self.tasks)}
                    res = jsonify({str(i): t.task.json_entry() for i, t in enumerate(self.tasks)})
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

    def init_tasks(self):
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

    def redraw_tasks(self, start=0):
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
            th_ = the if t.is_expanded else th
            bbox = x + mh + mh, y + (mv if start + i == 0 else 0), x + tw - (1 * mh), y + th_ - (1 * mv)
            # self.canvas.moveto(t.tag, *bbox[:2])
            self.canvas.coords(t.tag, *bbox)
            # print(f"RD {start=}, {i=} BBOX: {bbox}, old={t.bbox}")
            t.bbox = bbox

            dims = self.calc_task_dims(t)
            self.canvas.coords(t.tag_text_name, dims["bbox_name"])

            # self.draw_task(t, bbox)
            y += th_

    def draw_task(self, task_in: TaskCell, bbox=None):
        # assert isinstance(task_in, TaskCell)
        if bbox is None:
            bbox = task_in.bbox

        dims = self.calc_task_dims(task_in, bbox)

        c_fill = task_in.fill.hex_code
        c_outl = task_in.outline.hex_code
        c_acfi = task_in.active_fill.hex_code
        c_acou = task_in.active_outline.hex_code
        tag_rect = self.canvas.create_rectangle(
            *bbox,
            fill=c_fill,
            outline=c_outl,
            activefill=c_acfi,
            activeoutline=c_acou,
        )
        tag_name = self.canvas.create_text(
            dims["x_name"],
            dims["y_name"],
            text=task_in.task.text[:25]
        )
        self.canvas.tag_bind(tag_rect, "<Double-Button-1>", lambda event, t_=task_in: self.dbl_click_task(event, t_))
        if bbox is not None:
            task_in.bbox = bbox
        task_in.tag = tag_rect
        task_in.tag_text_name = tag_name

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

        x_check, y_check = bbox[0], bbox[1]
        x_status, y_status = x_check + w_check, bbox[1]
        x_idn, y_idn = x_status + w_status, bbox[1]
        x_name, y_name = x_idn + w_idn + (w_name * 0.5), bbox[1] + (h * 0.5)
        x_due, y_due = x_name + w_name, bbox[1]
        x_hrs, y_hrs = x_due + w_due, bbox[1]

        return {
            "x_check": x_check,
            "y_check": y_check,
            "w_check": w_check,
            "h_check": h_check,

            "x_status": x_status,
            "y_status": y_status,
            "w_status": w_status,
            "h_status": h_status,

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
            try:
                with open(fn, "r") as f:
                    # print(f"{f.read()}")
                    lines = json.load(f)
                    for i, k_raw_task_data in enumerate(lines.items()):
                        key, raw_task_data = k_raw_task_data
                        print(f"{i=}, {raw_task_data=}")
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

        vars = [
            self.tv_entry_tsk_inp_name.get().strip(),
            self.odp_due_date.date,
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

    def show_task_input_form(self):
        showing = self.showing_input_form.get()
        if showing:
            # now hide
            self.frame_task_input.grid_forget()
        else:
            # now show
            self.frame_task_input.grid(**self.grid_args["frame_task_input"])

        self.showing_input_form.set(not showing)


if __name__ == '__main__':
    app = App()
    app.mainloop()

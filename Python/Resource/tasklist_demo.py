import enum
import json
from threading import Thread
from dataclasses import dataclass

from json_utility import jsonify
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


@dataclass
class Attachment:
    id: int
    name: str
    file_path: str
    file_type: str


@dataclass
class Task:
    idn: int  # id number
    name: str  # optional name
    date_created_og: datetime.datetime  # marks original request date
    date_created: datetime.datetime  # adjusted when requirement attributes are adjusted
    due_date_og: datetime.datetime  # marks original due date
    due_date: datetime.datetime  # adjusted if due date is changed
    text: str
    comments: str
    priority: Priority
    attachments: list

    def json_entry(self):
        j = {1: datetime.datetime.now()}
        print(f"{json.dumps(j)=}")
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


@dataclass
class TaskCell:
    task: Task
    tag: str = None
    bbox: tuple = None
    fill: Colour = Colour("#CCA0A0")
    active_fill: Colour = Colour("#CCA0A0").brighten(0.1)
    outline: Colour = Colour(BLACK)
    active_outline: Colour = Colour(BLACK).brighten(0.1)


class App(tkinter.Tk):

    def __init__(self):
        super().__init__()
        dims = calc_geometry_tl(0.54, 0.36, rtype=dict)
        self.geometry()
        self.width_canvas, self.height_canvas = dims["width"], dims["height"]
        self.canvas = tkinter.Canvas(
            self,
            width=self.width_canvas,
            height=self.height_canvas,
            bg=Colour("#664242").hex_code
            #,
            # scrollregion=(0, 0, self.width_canvas, self.height_canvas)
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
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        self.canvas.grid(row=0, column=0)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.width_task_cell, self.height_task_cell = self.width_canvas, 40

        self.file_tasks = r".\task_manager_records.json"
        self.tasks = []
        self.threads = {}
        self.load_tasks()

        for k, t in self.threads.items():
            t.join()

        self.init_tasks()

    def init_tasks(self):
        x, y, tw, th = 0, 0, self.width_task_cell, self.height_task_cell
        tsks = []
        # c_fill = self.colours["fill_task_cell"]
        # c_outl = self.colours["outline_task_cell"]
        # c_acfi = self.colours["active_fill_task_cell"]
        # c_acou = self.colours["active_outline_task_cell"]
        for t in self.tasks:
            # assert isinstance(t, TaskCell)
            c_fill = t.fill
            c_outl = t.outline
            c_acfi = t.active_fill
            c_acou = t.active_outline
            bbox = x, y, tw, th
            tsks.append(
                self.canvas.create_rectangle(
                    bbox,
                    Fill=c_fill,
                    outline=c_outl,
                    activefill=c_acfi,
                    activeoutline=c_acou
                )
            )
            t.bbox = bbox
            t.tag = tsks[-1]

    def load_tasks(self):
        print(f"Loading tasks... ", end="")

        def sub_load_tasks():
            fn = self.file_tasks
            tasks = []
            try:
                with open(fn, "r") as f:
                    lines = json.load(f)
                    for i, raw_task_data in enumerate(lines):
                        print(f"{i=}, {raw_task_data=}")
                        tasks.append(TaskCell(Task(
                            raw_task_data.get("idn", i),
                            raw_task_data.get("name"),
                            eval(raw_task_data.get("date_created_og")),
                            eval(raw_task_data.get("date_created")),
                            eval(raw_task_data.get("due_date_og")),
                            eval(raw_task_data.get("due_date")),
                            raw_task_data.get("text"),
                            raw_task_data.get("comments"),
                            raw_task_data.get("priority"),
                            eval(raw_task_data.get("attachments"))
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

        self.threads["load_tasks"] = Thread(target=sub_load_tasks)
        self.threads["load_tasks"].start()

    def make_task_file(self):
        with open(self.file_tasks, "w") as f:
            f.write("{}")
            f.close()
        print(f"Task file creation successful.")


if __name__ == '__main__':
    app = App()
    app.mainloop()

import enum
import json
from threading import Thread
from dataclasses import dataclass

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



class App(tkinter.Tk):

    def __init__(self):
        super().__init__()
        dims = calc_geometry_tl(0.54, 0.36, rtype=dict)
        self.geometry()
        self.width_canvas, self.height_canvas = dims["width"], dims["height"]
        self.canvas = tkinter.Canvas(self, width=self.width_canvas, height=self.height_canvas, bg=Colour("#664242").hex_code)
        self.canvas.grid()

        self.width_task_cell, self.height_task_cell = self.width_canvas, 40

        self.file_tasks = r".\task_manager_records.json"
        self.tasks = []
        self.threads = {}
        self.load_tasks()

        for k, t in self.threads:
            t.join()

    def load_tasks(self):

        def sub_load_tasks():
            fn = self.file_tasks
            tasks = []
            try:
                with open(fn, "r") as f:
                    lines = json.load(f)
                    for i, raw_task_data in enumerate(lines):



        self.threads["load_tasks"] = Thread(target=sub_load_tasks)
        self.threads["load_tasks"].start()


if __name__ == '__main__':
    app = App()
    app.mainloop()

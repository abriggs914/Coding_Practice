import webbrowser

from pdf_writer import PDF, MARGIN_LINES_MARGIN, MARGIN_LINES_WIDTH, MAX_X, MAX_Y, random_test_set
from colour_utility import *

# Python program to read a csv and create a PDF of it's data

import csv
import datetime
from tkinter import *
from tkinter import filedialog
import tkinterdnd2

# tk = Tk()


class CSVParser:

    def __init__(self, file_name):
        self.file_name = file_name
        self.field_names = None
        self.entries = None

    def get_file_name(self):
        return self.file_name

    def get_field_names(self):
        return self.field_names if self.field_names is not None else []

    def get_entries(self):
        return self.entries if self.entries is not None else []

    def read(self):
        self.entries = []
        self.field_names = []
        with open(self.file_name, 'r') as f:
            f_dicts = csv.DictReader(f)
            self.field_names = f_dicts.fieldnames
            for f_dict in f_dicts:
                self.entries.append(f_dict)


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(pady=35, padx=35)

        self.dnd_frame = Frame(self)
        self.listbox_frame = Frame(self.dnd_frame)
        self.btn_frame = Frame(self.dnd_frame)
        self.demo_frame = Frame(self)
        self.preview_frame = Frame(self.demo_frame)
        self.demo_btn_frame = Frame(self.demo_frame)
        self.dnd_frame.pack()
        self.listbox_frame.pack(side=TOP)
        self.btn_frame.pack(side=TOP)
        self.demo_frame.pack()
        self.preview_frame.pack(side=LEFT)
        self.demo_btn_frame.pack(side=RIGHT)

        # DND Listbox
        self.listbox = Listbox(self.listbox_frame, selectmode=EXTENDED, width=150, height=20)
        self.listbox.pack(fill=X, side=LEFT)
        self.listbox.drop_target_register(tkinterdnd2.DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.add_to_listbox)

        # DND Listbox control buttons
        self.clear_listbox_button = Button(self.btn_frame, text="Clear All", fg="red", bg="#c2c2c2", command=self.clear_listbox)
        self.clear_listbox_button.pack(side=LEFT)
        self.clear_selected_button = Button(self.btn_frame, text="Clear Selected", fg="red", bg="#c2c2c2", command=self.clear_selected)
        self.clear_selected_button.pack(side=LEFT)
        self.browse_files_button = Button(self.btn_frame, text="Browse Files", fg="red", bg="#c2c2c2", command=self.browse_files)
        self.browse_files_button.pack(side=LEFT)

        # Preview Demo
        DEMO_WIDTH = 250
        DEMO_HEIGHT = int(round(DEMO_WIDTH * (11 / 8.5)))
        self.demo_canvas = Canvas(self.preview_frame, bg="#ffffff", width=DEMO_WIDTH, height=DEMO_HEIGHT)
        self.demo_canvas.pack()

        sbv = Scrollbar(
            self.listbox_frame,
            orient=VERTICAL
        )
        sbv.pack(side=RIGHT, fill=Y)

        self.listbox.configure(yscrollcommand=sbv.set)
        sbv.config(command=self.listbox.yview)

    def add_to_listbox(self, event):
        if event is None or not event:
            return
        if isinstance(event, dict):
            file_strs = event["data"].split(" ")
        else:
            file_strs = event.data.split(" ")
        for file_str in file_strs:
            self.listbox.insert("end", file_str + "\n")

    def clear_listbox(self):
        self.listbox.delete(0, "end")

    def clear_selected(self):
        selected = list(self.listbox.curselection())
        remaining = self.listbox.get(0, "end")
        res = []
        for i, v in enumerate(remaining):
            if not selected or i != selected[0]:
                res.append(v)
            else:
                selected.pop(0)
        print("remaining ({})".format(len(remaining)), remaining)
        print("selected ({})".format(len(selected)), selected)
        print("res ({})".format(len(res)), res)

        self.clear_listbox()
        self.add_to_listbox({"data": " ".join(res)})

    # Function for opening the
    # file explorer window
    def browse_files(self):
        filename = list(filedialog.askopenfilenames(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*"))))

        # Change label contents
        # label_file_explorer.configure(text="File Opened: " + filename)
        self.add_to_listbox({"data": " ".join(filename)})

    def run(self):
        self.mainloop()


# class App(Frame):
#
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.pack(pady=35, padx=35)
#
#         self.cost = StringVar()
#         self.margin = StringVar()
#         self.increase = StringVar()
#         self.exchange = StringVar()
#         self.calculated_cost = StringVar()
#
#         self.current_cost_btn = Button(self, text="use calculated cost", command=self.use_calculated_cost)
#         self.label_cost = Label(self, text="Cost")
#         self.entry_cost = Entry(self, textvariable=self.cost)
#         self.label_margin = Label(self, text="% Margin")
#         self.entry_margin = Entry(self, textvariable=self.margin)
#         self.label_increase = Label(self, text="% Increase")
#         self.entry_increase = Entry(self, textvariable=self.increase)
#         self.label_exchange = Label(self, text="Exchange")
#         self.entry_exchange = Entry(self, textvariable=self.exchange)
#
#         self.text_display = Text(self, height=5, width=20)
#
#         self.btn_sub = Button(self, text="submit", command=self.submit)
#         self.btn_clear = Button(self, text="clear", command=self.clear_fields)
#
#         self.label_cost.grid(column=0, row=0, sticky=N)
#         self.entry_cost.grid(column=1, row=0, sticky=N)
#         self.label_margin.grid(column=0, row=1, sticky=N)
#         self.entry_margin.grid(column=1, row=1, sticky=N)
#         self.label_increase.grid(column=0, row=2, sticky=N)
#         self.entry_increase.grid(column=1, row=2, sticky=N)
#         self.label_exchange.grid(column=0, row=3, sticky=N)
#         self.entry_exchange.grid(column=1, row=3, sticky=N)
#
#         self.text_display.grid(column=0, row=4, columnspan=2, sticky=N)
#
#         self.current_cost_btn.grid(column=0, row=5, columnspan=2, stick=N, pady=5)
#         self.btn_sub.grid(column=0, row=6, columnspan=2, sticky=N, pady=5)
#         self.btn_clear.grid(column=0, row=7, columnspan=2, sticky=N, pady=5)
#
#     def use_calculated_cost(self):
#         if self.calculated_cost.get():
#             self.cost.set("%.2f" % float(self.calculated_cost.get()))
#         else:
#             self.text_display.delete('1.0', END)
#             self.text_display.insert('1.0', "Invalid")
#
#     def run(self):
#         self.mainloop()
#
#     def clear_fields(self):
#         self.cost.set("")
#         self.margin.set("")
#         self.increase.set("")
#         self.exchange.set("")
#         self.text_display.delete('1.0', END)
#
#     def submit(self):
#         self.text_display.delete('1.0', END)
#         c = self.cost.get()
#         m = self.margin.get()
#         i = self.increase.get()
#         e = self.exchange.get()
#
#         try:
#             if all([c, m, i, e]):
#                 c = float(c)
#                 m = float(m)
#                 i = float(i)
#                 e = float(e)
#
#                 # val, vals = updated_costing(c, m, e, i)
#                 val = "val"
#                 vals = {"vals": 1}
#                 result = "\n".join([k.ljust(6) + v for k, v in vals.items()])
#                 self.calculated_cost.set(val)
#                 self.text_display.insert('1.0', result)
#
#                 # print("cost    ", money(c))
#                 # print("margin  ", money(m))
#                 # print("increase", money(i))
#                 # print("exchange", money(e))
#                 # print("results:\n" + result)
#             else:
#                 raise ValueError
#         except ValueError:
#             self.text_display.insert('1.0', "Invalid")


if __name__ == "__main__":

    root = tkinterdnd2.Tk()
    root.title("CSV to PDF")
    WIDTH = 1100
    DIMS = "{}x{}".format(WIDTH, int(round(WIDTH * (6 / 9))))
    root.geometry(DIMS)
    root.config(bg='#fcb103')
    app = App(root)
    app.run()





    # print("GO")
    #
    # root = Tk(className="\CSV to PDF Converter")
    # app = App(root)
    # app.run()

########################################################################################################################

    # def show_text(event):
    #     textarea.delete("1.0", "end")
    #     if event.data.endswith(".txt") or 1:
    #         with open(event.data, "r") as file:
    #             for line in file:
    #                 line = line.strip()
    #                 textarea.insert("end", f"{line}\n")
    #
    #
    # ws = tkinterdnd2.Tk()
    # ws.title('PythonGuides')
    # ws.geometry('400x300')
    # ws.config(bg='#fcb103')
    #
    # frame = Frame(ws)
    # frame.pack()
    #
    # textarea = Text(frame, height=18, width=40)
    # textarea.pack(side=LEFT)
    # textarea.drop_target_register(tkinterdnd2.DND_FILES)
    # textarea.dnd_bind('<<Drop>>', show_text)
    #
    # sbv = Scrollbar(frame, orient=VERTICAL)
    # sbv.pack(side=RIGHT, fill=Y)
    #
    # textarea.configure(yscrollcommand=sbv.set)
    # sbv.config(command=textarea.yview)
    #
    # ws.mainloop()

########################################################################################################################







    # ws.mainloop()
########################################################################################################################

# class Line:
#     def __init__(self, quote_date, wo, quote, price, model_no, width, spread):
#         self.quote_date = datetime.datetime.strftime(datetime.datetime.strptime(quote_date[:10], "%Y-%m-%d"),
#                                                      "%Y-%m-%d")
#         self.wo = wo
#         self.quote = quote
#         self.price = price
#         self.model_no = model_no
#         self.width = width
#         self.spread = spread
#
#     def csv_entry(self):
#         return dict(zip(["WO#", "Q#", "$", "Name", "Width", "Spread"],
#                         [self.wo, self.quote, self.price, self.model_no, self.width, self.spread]))
#
#     def __repr__(self):
#         return "QD: {}, QO: {}, Q#: {}, P$: {}, MN: {}, W: {}, S: {}".format(self.quote_date, self.wo, self.quote,
#                                                                              self.price, self.model_no, self.width,
#                                                                              self.spread)
#
#
# if __name__ == "__main__":
#     data = {}
#     FILE_NAME = "last_100_quotes.PDF"
#     with open("random query data.csv", "r") as f:
#         lines = csv.DictReader(f)
#         for i, line in enumerate(lines):
#             # for key, val in line.items():
#             # print("key", key)
#             entry = Line(*line.values())
#             print(entry)
#             if entry.quote_date not in data:
#                 data[entry.quote_date] = []
#             data[entry.quote_date].append(entry.csv_entry())
#
#     print("data:", data)
#
#     TITLE_HEIGHT = 12
#     TITLE_MARGIN = 15
#     TABLE_MARGIN = 6
#     FOOTER_MARGIN = 10
#     TXT_MARGIN = 10
#     ori = "P"
#
#     if ori == "L":
#         MAX_X, MAX_Y = MAX_Y, MAX_X
#
#     pdf = PDF(FILE_NAME, orientation=ori, unit='mm', format='A4')
#     pdf.set_auto_page_break(True, margin=5)
#     pdf.set_title("Dealer Delivery Reports")
#     pdf.set_author('Avery Briggs')
#     pdf.add_page()
#
#     # pdf.margin_lines(MARGIN_LINES_MARGIN, MARGIN_LINES_MARGIN, MAX_X - (2 * MARGIN_LINES_MARGIN),
#     # 				 MAX_Y - (2 * MARGIN_LINES_MARGIN), BWS_RED, WHITE)
#     pdf.margin_border(BWS_RED, WHITE)
#     pdf.titles("Dealer Delivery Reports", MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN,
#                TITLE_MARGIN + MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN,
#                MAX_X - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN)), TITLE_HEIGHT, BWS_BLACK)
#
#     # TABLE_X = 5 + MARGIN_LINES_WIDTH + TABLE_MARGIN
#     # TABLE_Y = 10 + MARGIN_LINES_WIDTH + TABLE_MARGIN
#
#     TABLE_W = (MAX_X - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN)) - (2 * TABLE_MARGIN))
#
#     TABLE_X = TABLE_MARGIN + MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN
#     TABLE_Y = TABLE_MARGIN + MARGIN_LINES_WIDTH + TITLE_HEIGHT + TITLE_MARGIN
#
#     # TABLE_LEFT_MARGIN = 6
#     TITLE_V_MARGIN = 5
#
#     table1 = pdf.table(
#         title="Last 100 Quotes",
#         x=TABLE_X,
#         y=TABLE_Y,
#         w=TABLE_W,
#         contents=data,
#         desc_txt="Last 100 Quotes as of 2021-06-15",
#         # contents=random_test_set(453),
#         header_colours=[GRAY_30, BLACK],
#         colours=[[WHITE, GRAY_69],
#                  [BLACK]],
#         show_row_names=True,
#         include_top_doc_link=True,
#         new_page_for_table=False,
#         row_name_col_lbl="Date",
#         start_with_header=True,
#         cell_border_style=1,
#         col_align={"Date": "L", "$": "R", "Name": "L"}
#     )
#
#     # date = datetime.datetime.now()
#     # pdf.texts(
#     # 	MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN + TXT_MARGIN,
#     # 	TABLE_MARGIN + MARGIN_LINES_WIDTH + TITLE_HEIGHT + TITLE_MARGIN,
#     # 	0,
#     # 	10,
#     # 	"Prepared at {} on {}".format(
#     # 		datetime.datetime.strftime(date, "%I:%M:%S %p"),
#     # 		datetime.datetime.strftime(date, "%Y-%m-%d")
#     # 	),
#     # 	font=('Arial', '', 10)
#     # )
#
#     pdf.time_stamp()
#     pdf.output(FILE_NAME, 'F')
#     webbrowser.open(FILE_NAME)

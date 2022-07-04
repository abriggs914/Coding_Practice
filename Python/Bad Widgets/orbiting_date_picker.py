import datetime

from colour_utility import *
import tkinter
from tkinter import ttk
import tkcalendar


def toggle_show_date():
    # if gsm_showing_dae_picker[0][1]
    # datepicker.grid_forget()
    print("hey")


WIDTH, HEIGHT = 900, 600
WINDOW = tkinter.Tk()
WINDOW.title("Orbiting Date Selector")
WINDOW.geometry(f"{WIDTH}x{HEIGHT}")

ss = tkinter.Canvas(WINDOW)
ss.grid(row=1, column=1)
ss.create_rectangle(50, 50, 150, 150, fill=rgb_to_hex(GREEN))

frame_form = tkinter.Frame(WINDOW)
frame_form.grid(row=2, column=1)

frame_date_area = tkinter.Frame(frame_form)
frame_date_area.grid(row=1, column=1)

label_date_entry = tkinter.Label(frame_date_area, text="Select a date:")
label_date_entry.grid(row=1, column=1)
tv_date_entry = tkinter.StringVar()
entry_date_entry = tkinter.Entry(frame_date_area, textvariable=tv_date_entry)
entry_date_entry.grid(row=1, column=2)
btn_date_picker_btn = tkinter.Button(frame_date_area, text="select", command=toggle_show_date)
btn_date_picker_btn.grid(row=1, column=3)

today = datetime.datetime.now()
datepicker = tkcalendar.Calendar(frame_date_area, selectmode="day", cursor="hand1", year=today.year, month=today.month, day=today.day)
datepicker.pack()


def main():
    WINDOW.mainloop()


if __name__ == "__main__":

    main()

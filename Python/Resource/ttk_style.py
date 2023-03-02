import tkinter as tk
from tkinter import ttk
import tkcalendar
from datetime import datetime, timedelta

class DateEntryApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Date Entry App")
        self.create_widgets()

    def create_widgets(self):
        self.dateentry = tkcalendar.DateEntry(self.master)
        self.dateentry.grid(row=0, column=0, padx=20, pady=20)
        self.dateentry.bind("<<DateEntrySelected>>", self.update_label)

        self.button = ttk.Button(self.master, text="Update Label", command=self.update_label)
        self.button.grid(row=1, column=0, padx=20, pady=10)

        self.label = ttk.Label(self.master, text="Date selected: ")
        self.label.grid(row=2, column=0, padx=20, pady=10)

    def update_label(self, *args):
        selected_date = self.dateentry.get_date()
        invalid = False
        if selected_date is None or selected_date < datetime.now().date():
            print(f"A")
            invalid = True
        else:
            print(f"B")

        if invalid:
            self.dateentry.config(style="Red.TEntry")
            self.label.config(text="Invalid date")
            print(f"C")
        else:
            self.dateentry.config(style="TEntry")
            self.label.config(text=f"Date selected: {selected_date}")
            print(f"D")

def main():
    root = tk.Tk()
    app = DateEntryApp(master=root)
    app.style = ttk.Style()
    app.style.configure("Red.TEntry", fieldforeground="red", foreground="red")
    app.style.configure("TEntry", fieldforeground="black", foreground="black")
    app.mainloop()

if __name__ == '__main__':
    main()

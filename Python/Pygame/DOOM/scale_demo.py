import tkinter
from tkinter import *
from tkinter import ttk

t = tkinter.Tk()
t.geometry("500x500")


class OnOffToggle(tkinter.Frame):
    def __init__(self, is_on: bool = True, label_on_text="The Switch is On!", label_off_text="The Switch is Off!",
                 button_foreground_on="green", button_foreground_off="grey", show_label=True):
        super().__init__()

        # Keep track of the button state on/off
        # global is_on
        self.is_on = tkinter.BooleanVar(self, value=is_on)
        self.label_on_text = label_on_text
        self.label_off_text = label_off_text
        self.tv_label = tkinter.StringVar(self, value=label_on_text if is_on else label_off_text)
        self.button_foreground_on = button_foreground_on
        self.button_foreground_off = button_foreground_off
        self.show_label = show_label

        # Create Label
        self.my_label = Label(self,
                              textvariable=self.tv_label,
                              fg=self.button_foreground_on,
                              font=("Helvetica", 32))

        if self.show_label:
            self.my_label.pack(pady=20)

        # Define Our Images
        self.on = PhotoImage(file="resources/tkinter/on.png")
        self.off = PhotoImage(file="resources/tkinter/off.png")

        # Create A Button
        self.button = Button(self, image=self.on if self.is_on.get() else self.off, bd=0,
                             command=self.switch)
        self.button.pack(pady=50)

        # Define our switch function

    def switch(self):
        # Determine is on or off
        if self.is_on.get():
            self.button.config(image=self.off)
            self.tv_label.set(self.label_off_text)
            self.my_label.config(fg=self.button_foreground_off)
            self.is_on.set(False)
        else:
            self.button.config(image=self.on)
            self.tv_label.set(self.label_on_text)
            self.my_label.config(fg=self.button_foreground_on)
            self.is_on.set(True)


class BooleanToggle(tkinter.Frame):
    def __init__(self):
        super().__init__()
        


# def foo(*args):
#     print(f"foo, {args=}")
#
#
# var_1 = tkinter.IntVar(t, value=0)
#
# s = ttk.Scale(
#     t,
#     command=foo,
#     cursor="arrow",
#     length=100,
#     orient="horizontal",
#     state="normal",
#     from_=1,
#     to=3,
#     # class_="str",
#     # style="normal",
#     takefocus=True,
#     variable=var_1,
#     value=1
# )
#
# s.pack()

bt = OnOffToggle(show_label=False)
bt.pack()

if __name__ == "__main__":
    t.mainloop()

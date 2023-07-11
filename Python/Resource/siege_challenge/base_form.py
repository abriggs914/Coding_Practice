import tkinter
from abc import abstractmethod

from colour_utility import Colour, BLACK, RED, gradient
from tkinter_utility import button_factory


class Form(tkinter.Toplevel):

    def __init__(self, callback):
        super().__init__()

        self.tv_status = tkinter.StringVar(self, value="idle")
        self.callback = callback
        self.after_callbacks = {}
        self.after_pass_count = tkinter.IntVar(self, value=0)

        self.frame_ctl_btns = tkinter.Frame(self)
        self.tv_btn_cancel,\
            self.btn_cancel =\
            button_factory(
                self.frame_ctl_btns,
                tv_btn="cancel",
                command=self.click_cancel
            )

        self.tv_btn_submit,\
            self.btn_submit =\
            button_factory(
                self.frame_ctl_btns,
                tv_btn="submit",
                command=self.click_submit
            )

        self.btn_cancel.bind("<Return>", self.return_cancel)
        self.btn_submit.bind("<Return>", self.return_submit)

    @abstractmethod
    def valid_input(self):
        pass

    def flash_lbl(self, lbl):
        if isinstance(lbl, tkinter.Radiobutton):
            lbl.flash()
        else:
            c1 = lbl.cget("foreground")
            print(f"{c1=}")
            try:
                print(f"{Colour(c1)=}")
            except Colour.ColourCreationError:
                print(f"NOT A COLOUR")
            c1 = BLACK if not c1 else c1
            c2 = RED
            n = 24
            s = 300
            colours = [gradient(i, n // 2, c1, c2, rgb=False) for i in range(n // 2)]
            colours = colours + colours[::-1]
            spf = s / n
            self.after_pass_count.set(0)

            def sub_flash():
                for i in range(n):
                    self.after_callbacks[f"sub_flash_{('000' + str((n * self.after_pass_count.get()) + i))[-2:]}"] = self.after(
                        int(1 + (i * spf)),
                        lambda i_=i: lbl.configure(foreground=colours[i_], activebackground=colours[i_])
                    )
                self.after_pass_count.set(self.after_pass_count.get() + 1)

            self.after_callbacks[f"flash_001"] = self.after(1, sub_flash)
            self.after_callbacks[f"flash_002"] = self.after(s + 101, sub_flash)

    def click_cancel(self, event=None):
        self.tv_status.set("cancel")
        self.callback()

    def click_submit(self, event=None):
        if not self.valid_input():
            return
        self.tv_status.set("submit")
        self.callback()

    def return_cancel(self, event=None):
        if self.btn_cancel == self.btn_cancel.focus_get():
            self.click_cancel(event)

    def return_submit(self, event=None):
        if self.btn_submit == self.btn_submit.focus_get():
            self.click_submit(event)

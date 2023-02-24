
from collections import OrderedDict, deque
import tkinter


def clamp(s, v, l):
    """Clamp a number between small and large values."""
    return max(s, min(v, l))


def is_tk_var(var_in, str_var=True, int_var=True, dbl_var=True, bol_var=True, var_var=True):
    valid = [v for c, v in zip(
        [str_var, int_var, dbl_var, bol_var, var_var],
        [tkinter.StringVar, tkinter.IntVar, tkinter.DoubleVar, tkinter.BooleanVar, tkinter.Variable]
    ) if c]
    return type(var_in) in valid


def text_factory(master, tv_label=None, tv_text=None, kwargs_label=None, kwargs_text=None):
    """Return tkinter StringVar, Label, StringVar, and TextWithVar objects"""
    if tv_label is not None and tv_text is not None:
        res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
        res_tv_text = tv_text if is_tk_var(tv_text) else tkinter.StringVar(master, value=tv_text)
    elif tv_label is not None:
        res_tv_label = tv_label if is_tk_var(tv_label) else tkinter.StringVar(master, value=tv_label)
        res_tv_text = tkinter.StringVar(master)
    elif tv_text is not None:
        res_tv_label = tkinter.StringVar(master)
        res_tv_text = tv_text if is_tk_var(tv_text) else tkinter.StringVar(master, value=tv_text)
    else:
        res_tv_label = tkinter.StringVar(master)
        res_tv_text = tkinter.StringVar(master)

    print(f"{tv_label=}\n{tv_text=}\n{kwargs_label=}\n{kwargs_text=}")
    print(f"{res_tv_label=}\n{res_tv_text=}")

    if kwargs_label is not None and kwargs_text is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_text = TextWithVar(master, textvariable=res_tv_text, **kwargs_text)
    elif kwargs_label is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label, **kwargs_label)
        res_text = TextWithVar(master, textvariable=res_tv_text)
    elif kwargs_text is not None:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_text = TextWithVar(master, textvariable=res_tv_text, **kwargs_text)
    else:
        res_label = tkinter.Label(master, textvariable=res_tv_label)
        res_text = TextWithVar(master, textvariable=res_tv_text)
    return res_tv_label, res_label, res_text.text, res_text


class TextWithVar(tkinter.Text):
    def __init__(self, master, textvariable=None, max_undos=100, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if textvariable is None:
            print(f"TextWithVar A")
            textvariable = tkinter.StringVar(value=self.get("1.0", tkinter.END))
        else:
            if isinstance(textvariable, tkinter.StringVar):
                print(f"TextWithVar B")
                textvariable = textvariable
            elif isinstance(textvariable, tkinter.Variable):
                print(f"TextWithVar C")
                textvariable = tkinter.StringVar(self, value=str(textvariable.get()))
            else:
                print(f"TextWithVar D")
                textvariable = tkinter.StringVar(self, value=textvariable)

        print(f"HELLO TEXT: '{textvariable.get()}'")

        self.max_undos = clamp(0, max_undos, 1000)
        self.history = deque(maxlen=self.max_undos)
        self.text = textvariable
        self.text.trace_variable("w", self.update_set_text)
        self.bind("<<CustomTextChanged>>", self._on_text_changed)
        self.bind("<Control-Return>", self.submit)
        self.bind("<KeyRelease>", self.key_release)
        self.history.append(self.text.get())

        # Initialize the text widget if a initial value is passed with the StringVar.
        if txt := self.text.get():
            self.insert("1.0", txt, pass_thru=False)
            # self.text.set(txt)

    def submit(self, event):
        print(f"submit")
        print(f"{self.history=}")

    def key_release(self, *event):
        self.text.set(self.get("1.0", "end-1c"))
        # self._update_text_variable()
        # print(f"key_release TEXT='{self.text.get()}', T2='{}' {event=}")

    def undo(self):
        if len(self.history) > 1:
            hist = self.history.pop()
            hist = self.history.pop()
            # print(f"hist='{hist}'")
            self.text.set(hist)
            return True
        elif len(self.history):
            hist = self.history.pop()
            self.text.set(hist)
            return True
        else:
            print("Nothing to undo.")
            self.history.append('')
            return False

    # def update_set_text(self, *args):
    #     # print(f"update_set_text, {self.text.get()=}")
    #     self._on_text_changed(None, pass_thru=False)

    def update_set_text(self, *args, pass_thru=True):
        try:
            if self.focus_get() == self:
                self.text.set(self.get("1.0", tkinter.END).rstrip())
                if not pass_thru:
                    self.event_generate("<<CustomTextChanged>>")
            else:
                print(f"does not have focus")
        except KeyError as ke:
            self._on_text_changed(None, pass_thru=False)

    def _on_text_changed(self, event, pass_thru=True):
        self.trim_history()
        self.history.append(self.text.get())
        self.delete("1.0", tkinter.END, pass_thru=pass_thru)
        self.insert("1.0", self.text.get(), pass_thru=pass_thru)

    def trim_history(self):
        if len(self.history) >= self.max_undos:
            self.history.popleft()

    def insert(self, index, text, pass_thru=True):
        super().insert(index, text)
        if pass_thru:
            self._update_text_variable()

    def delete(self, index1, index2=None, pass_thru=True):
        print(f"Delete: {index1=}, {index2=}, {pass_thru=}")
        super().delete(index1, index2)
        if pass_thru:
            self._update_text_variable()

    def _update_text_variable(self):
        print(f"{self.text.get()=}")
        self.text.set(self.get("1.0", tkinter.END))
        self.event_generate("<<CustomTextChanged>>")


def tl_close():
	global tl
	print(f"Goodbye!")
	tl.destroy()
	tl = None
		
		
def open_tl():
	global tl
	tl = tkinter.Toplevel(win)
	a, b, c, d = text_factory(tl, tv_text=tv)
	b.pack()
	d.pack()
	e = tkinter.Button(tl, text="undo", command=d.undo)
	e.pack()
	tl.protocol("WM_DELETE_WINDOW", tl_close)
	tl.grab_set()
	

if __name__ == "__main__":
	win = tkinter.Tk()
	win.geometry(f"500x500")
	
	tv = tkinter.StringVar(win, value="hello there!")
	tl = None
	
	b = tkinter.Button(win, text="Open TL", command=open_tl)
	b.pack()
	
	win.mainloop()
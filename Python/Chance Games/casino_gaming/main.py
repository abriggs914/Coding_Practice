import casino

# Commented out the tkinter demo, should use easygui or something else

# from os import path
# from tkinter import *
# from tkinter import scrolledtext
# from tkinter import messagebox
# from tkinter import ttk
# from tkinter import filedialog
# from tkinter import Menu
# from tkinter.ttk import *
# from tkinter.ttk import Progressbar
#
# # DEMO
#
# demo_window = Tk()
#
# demo_window.title("Welcome to LikeGeeks app")
#
# # setting window size (WxH)
# demo_window.geometry('850x500')
#
# # creating a label and placing it in the window
# lbl = Label(demo_window, text="Hello")
#
# # formatting the label in a grid orientation
# lbl.grid(column=0, row=0)
#
# # creating a get text entry field with a default size, and placing it in the window
# txt = Entry(demo_window, width=10)
#
# # formatting the entry
# txt.grid(column=1, row=0)
#
# selected = IntVar()
#
# # function for handling the button click
# def clicked():
#     # get entry text
#     res = "Welcome to " + txt.get()
#
#     # edit label attributes and adjust the text
#     lbl.configure(text= res)
#     print(selected.get())
#     messagebox.showinfo('Message title', 'Message content')
#     messagebox.showerror('Message title', 'Message content')  # shows error message
#
#     # lbl.configure(text="Button was clicked !!")
#
# # creating a button, placing it in the window, setting it's text,
# # changing it's colours, and then assigning it a handler function.
# # btn = Button(demo_window, text="Click Me", background="orange", foreground="red", command="clicked")
# btn = Button(demo_window, text="Click Me", command=clicked)
# # btn.configure(background="orange")
#
# # formatting the button
# btn.grid(column=2, row=0)
#
# combo = Combobox(demo_window)
#
# combo['values'] = (1, 2, 3, 4, 5, "Text")
#
# combo.current(1)  # set the selected item
#
# combo.grid(column=3, row=0)
#
# chk_state = BooleanVar()
#
# chk_state.set(True)  # set check state
#
# chk = Checkbutton(demo_window, text='Choose', var=chk_state)
#
# chk.grid(column=4, row=0)
#
# rad1 = Radiobutton(demo_window, text='First', value=1, variable=selected)
#
# rad2 = Radiobutton(demo_window, text='Second', value=2, variable=selected)
#
# rad3 = Radiobutton(demo_window, text='Third', value=3, variable=selected)
#
# rad1.grid(column=0, row=1)
#
# rad2.grid(column=1, row=1)
#
# rad3.grid(column=2, row=1)
#
# scroll_txt = scrolledtext.ScrolledText(demo_window,width=40,height=10)
# scroll_txt.grid(column=3, row=1)
# scroll_txt.insert(INSERT,'This is scroll text')
# txt.delete(1,END)
#
# # messagebox.showinfo('Message title','Message content')
# messagebox.showwarning('Message title', 'Message content')  # shows warning message
#
# question = messagebox.askquestion('Asking a question', 'Is this a question?')
#
# y_n = messagebox.askyesno('Asking yes or no', 'Yes or no')
#
# y_n_c = messagebox.askyesnocancel('Asking yes or no or cancel', 'Yes, no or, cancel')
#
# o_c = messagebox.askokcancel('Asking ok or cancel', 'Ok or cancel')
#
# r_c = messagebox.askretrycancel('Asking retry or cancel', 'Retry or cancel')
#
# print("question\t-\t" + str(question))
# print("y_n\t-\t" + str(y_n))
# print("y_n_c\t-\t" + str(y_n_c))
# print("o_c\t-\t" + str(o_c))
# print("r_c\t-\t" + str(r_c))
#
# spin_1 = Spinbox(demo_window, from_=0, to=100, width=5)
#
# spin_1.grid(column=0, row=2)
#
# spin_2 = Spinbox(demo_window, values=(3, 8, 11), width=5)
#
# spin_2.grid(column=1, row=2)
#
# var = IntVar()
#
# var.set(36)
#
# spin_3 = Spinbox(demo_window, from_=0, to=100, width=5, textvariable=var)
#
# spin_3.grid(column=2, row=2)
#
# style = ttk.Style()
#
# style.theme_use('default')
#
# style.configure("black.Horizontal.TProgressbar", background='black')
#
# bar = Progressbar(demo_window, length=200, style='black.Horizontal.TProgressbar')
#
# bar['value'] = 70
#
# bar.grid(column=0, row=0)
#
# file = filedialog.askopenfilename()
# # files = filedialog.askopenfilenames()
# # Specify file types (filter file extensions)
# # You can specify the file types for a file dialog using filetypes parameter, just specify the extensions in tuples.
# # file = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*")))
#
# # You can ask for a directory using askdirectory method:
# dir = filedialog.askdirectory()
#
# # You can specify the initial directory for the file dialog by specifying the initialdir like this:
# file_path = filedialog.askopenfilename(initialdir=path.dirname(__file__))
#
# menu = Menu(demo_window)
#
# # new_item = Menu(menu)
# new_item = Menu(menu, tearoff=0)
#
# # new_item.add_command(label='New')
#
# new_item.add_separator()
#
# new_item.add_command(label='Edit')
#
# menu.add_cascade(label='File', menu=new_item)
#
# # menu.add_cascade(label='Edit', menu=new_item)
#
# demo_window.config(menu=menu)
#
# new_item.add_command(label='New', command=clicked)
#
# tab_control = ttk.Notebook(demo_window)
#
# tab1 = ttk.Frame(tab_control)
#
# tab_control.add(tab1, text='First')
#
# tab_control.pack(expand=1, fill='both')
#
# # show the window ALWAYS goes LAST
# demo_window.mainloop()


casino.welcome_to_casino()
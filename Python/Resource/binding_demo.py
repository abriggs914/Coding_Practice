import tkinter
WIN = tkinter.Tk()
WIN.geometry("600x500")
a = tkinter.StringVar(WIN, value="")
b = tkinter.Entry(WIN, textvariable=a)
b.pack()
a.set("testing...")
# b.configure(state="disabled")

def foo_a(event):
    print("foo_a")

binding_in_q = "<Control-Shift-KeyPress-Q>"

b_1 = b.bind(binding_in_q, foo_a)
print(f"{b_1=}")

bindings = b.bind()
print(f"{bindings=}, {type(bindings)=}")

for bind in bindings:
    print(f"{bind=}, {type(bind)=}, {b.bind(bind)=}, {type(b.bind(bind))=}")

c = tkinter.StringVar(WIN, value="")
d = tkinter.Entry(WIN, textvariable=c)
c.set("stop testing")

d.pack()

# using the return value of this binding, I can set another binding to the same callback
b_2 = d.bind("<Control-Shift-KeyPress-P>", b.bind(binding_in_q))
print(f"{b_2=}")

print(f"{d.bind('<Keypress-A>')=}")

WIN.mainloop()

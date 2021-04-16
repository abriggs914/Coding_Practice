import tkinter as tk
from utility import *

def updated_costing(cost, margin=30, FE=1.245, increase=0):
	cost *= (1 + (increase / 100))
	margin = (100 - margin) / 100
	return {
		"COST": money(cost),
		"CDN": money((cost / margin) if cost >= 0 else (cost * margin)),
		"US": money(((cost / margin) if cost >= 0 else (cost * margin)) / FE)
	}

class App(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack(pady=35, padx=35)

        self.cost = tk.StringVar()
        self.margin = tk.StringVar()
        self.increase = tk.StringVar()
        self.exchange = tk.StringVar()


        self.label_cost = tk.Label(self, text="Cost")
        self.entry_cost = tk.Entry(self, textvariable=self.cost)
        self.label_margin = tk.Label(self, text="% Margin")
        self.entry_margin = tk.Entry(self, textvariable=self.margin)
        self.label_increase = tk.Label(self, text="% Increase")
        self.entry_increase = tk.Entry(self, textvariable=self.increase)
        self.label_exchange = tk.Label(self, text="Exchange")
        self.entry_exchange = tk.Entry(self, textvariable=self.exchange)

        self.text_display = tk.Text(self, height = 5, width = 20)

        self.btn_sub = tk.Button(self, text="submit", command=self.submit)
        self.btn_clear = tk.Button(self, text="clear", command=self.clear_fields)


        self.label_cost.grid(column=0, row=0, sticky=tk.N)
        self.entry_cost.grid(column=1, row=0, sticky=tk.N)
        self.label_margin.grid(column=0, row=1, sticky=tk.N)
        self.entry_margin.grid(column=1, row=1, sticky=tk.N)
        self.label_increase.grid(column=0, row=2, sticky=tk.N)
        self.entry_increase.grid(column=1, row=2, sticky=tk.N)
        self.label_exchange.grid(column=0, row=3, sticky=tk.N)
        self.entry_exchange.grid(column=1, row=3, sticky=tk.N)
        
        self.text_display.grid(column=0, row = 4, columnspan=2, sticky=tk.N)

        self.btn_sub.grid(column=0, row=5, columnspan=2, sticky=tk.N, pady=5)
        self.btn_clear.grid(column=0, row=6, columnspan=2, sticky=tk.N, pady=5)

    def run(self):
        self.mainloop()

    def clear_fields(self):
        self.cost.set("")
        self.margin.set("")
        self.increase.set("")
        self.exchange.set("")
        self.text_display.delete('1.0', tk.END)

    def submit(self):
        self.text_display.delete('1.0', tk.END)
        c = self.cost.get()
        m = self.margin.get()
        i = self.increase.get()
        e = self.exchange.get()

        try:
            if all([c, m, i, e]):
                c = float(self.cost.get())
                m = float(self.margin.get())
                i = float(self.increase.get())
                e = float(self.exchange.get())
                print("cost    ", money(c))
                print("margin  ", money(m))
                print("increase", money(i))
                print("exchange", money(e))
                
                result = "\n".join([k.ljust(6) + v for k, v in updated_costing(c, m, e, i).items()])
                self.text_display.insert('1.0', result)
            else:
                raise ValueError
        except ValueError:
                self.text_display.insert('1.0', "Invalid")

if __name__ == "__main__":
    root = tk.Tk(className="Price Calculator")
    app = App(root)
    app.run()
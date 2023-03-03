import tkinter as tk
import tkinter.ttk as ttk

"""
class SeasonalColorsApp:
    def __init__(self, master):
        self.master = master
        master.title("Seasonal Colors")
        
        # create the ttk Style object and configure it with rules for each season
        self.style = ttk.Style(master)
        self.style.map('TCombobox', fieldbackground=[('winter', '#ADD8E6'), ('spring', '#90EE90'), ('summer', '#FFDAB9'), ('fall', '#FFA07A')])
        self.style.map('TCombobox', foreground=[('winter', 'black'), ('spring', 'black'), ('summer', 'black'), ('fall', 'black')])
        self.style.map('TCombobox', background=[('winter', '#B0C4DE'), ('spring', '#98FB98'), ('summer', '#FFE4C4'), ('fall', '#FF8C00')])
        self.style.map('TCombobox', fieldforeground=[('winter', 'white'), ('spring', 'black'), ('summer', 'black'), ('fall', 'white')])
        
        # create the Combobox widget and add it to the window
        self.season_var = tk.StringVar()
        self.season_combobox = ttk.Combobox(master, textvariable=self.season_var, values=['winter', 'spring', 'summer', 'fall'])
        self.season_combobox.pack()
        self.season_combobox.bind("<<ComboboxSelected>>", self.update_colors)
        
        # initialize the colors based on the initial value of the combobox
        self.update_colors()

    def update_colors(self, event=None):
        # update the colors based on the current value of the combobox
        season = self.season_var.get()
        self.style.configure('TCombobox', selectbackground=self.style.lookup('TCombobox', 'background.' + season))
        self.style.configure('TCombobox', selectforeground=self.style.lookup('TCombobox', 'foreground.' + season))
        self.style.configure('TCombobox', fieldbackground=self.style.lookup('TCombobox', 'fieldbackground.' + season))
        self.style.configure('TCombobox', fieldforeground=self.style.lookup('TCombobox', 'fieldforeground.' + season))

root = tk.Tk()
app = SeasonalColorsApp(root)
root.mainloop()
"""


class SeasonalColorsApp:
    def __init__(self, master):
        self.master = master
        master.title("Seasonal Colors")
        
        # create the ttk Style object and configure it with custom styles for each season
        self.style = ttk.Style(master)
        self.style.configure('Winter.TCombobox', fieldbackground='#ADD8E6', foreground='black', background='#B0C4DE', fieldforeground='white', selectbackground='#ADD8E6', selectforeground='black')
        self.style.configure('Spring.TCombobox', fieldbackground='#90EE90', foreground='black', background='#98FB98', fieldforeground='black', selectbackground='#90EE90', selectforeground='black')
        self.style.configure('Summer.TCombobox', fieldbackground='#FFDAB9', foreground='black', background='#FFE4C4', fieldforeground='black', selectbackground='#FFDAB9', selectforeground='black')
        self.style.configure('Fall.TCombobox', fieldbackground='#FFA07A', foreground='black', background='#FF8C00', fieldforeground='white', selectbackground='#FFA07A', selectforeground='white')
        
        # create the Combobox widget and add it to the window
        self.season_var = tk.StringVar(master, value="winter")
        self.season_combobox = ttk.Combobox(master, textvariable=self.season_var, values=['winter', 'spring', 'summer', 'fall'])
        self.season_combobox.pack()
        self.season_combobox.bind("<<ComboboxSelected>>", self.update_colors)
        
        # initialize the colors based on the initial value of the combobox
        self.update_colors()

    def update_colors(self, event=None):
        # update the style of the combobox based on the current value of the combobox
        season = self.season_var.get()
        print(f"season: {season}")
        self.style.configure('TCombobox', season.title() + '.TCombobox')

root = tk.Tk()
app = SeasonalColorsApp(root)
root.mainloop()
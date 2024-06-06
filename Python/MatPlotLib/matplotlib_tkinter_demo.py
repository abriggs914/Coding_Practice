import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Matplotlib in Tkinter")
        
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.button = ttk.Button(self.root, text="Generate Plot", command=self.create_plot)
        self.button.pack(side=tk.TOP)

    def create_plot(self):
        # Clear the previous plot
        self.ax.clear()
        
        # Generate random data
        x = np.random.rand(10)
        y = np.random.rand(10)
        
        # Create a new plot
        self.ax.plot(x, y, 'o-')
        
        # Redraw the canvas with the new plot
        self.canvas.draw()

# Create the main Tkinter window
window = tk.Tk()

# Create an instance of the App class
app = App(window)

# Start the Tkinter main loop
window.mainloop()
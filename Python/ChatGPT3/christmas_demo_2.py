# Import the necessary modules
import time
import tkinter as tk
import random

# Create a new Tkinter window
root = tk.Tk()

# Create a canvas to draw the tree on
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

# Create a list of colors to use for the lights
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

# Create a function to animate the lights
def animate():
    # Loop indefinitely
    while True:
        # Choose a random color from the list
        color = random.choice(colors)
        # Change the color of the lights
        canvas.itemconfigure(light1, fill=color)
        canvas.itemconfigure(light2, fill=color)
        canvas.itemconfigure(light3, fill=color)
        canvas.itemconfigure(light4, fill=color)
        canvas.itemconfigure(light5, fill=color)
        canvas.itemconfigure(light6, fill=color)
        canvas.itemconfigure(light7, fill=color)
        canvas.itemconfigure(light8, fill=color)
        # Update the canvas
        canvas.update()
        # Pause for 0.02 seconds
        time.sleep(0.02)

# Create the tree
tree = canvas.create_rectangle(100, 100, 200, 250, fill='green')

# Create the lights
light1 = canvas.create_oval(120, 120, 130, 130, fill='red')
light2 = canvas.create_oval(140, 120, 150, 130, fill='orange')
light3 = canvas.create_oval(160, 120, 170, 130, fill='yellow')
light4 = canvas.create_oval(180, 120, 190, 130, fill='green')
light5 = canvas.create_oval(120, 140, 130, 150, fill='blue')
light6 = canvas.create_oval(140, 140, 150, 150, fill='purple')
light7 = canvas.create_oval(160, 140, 170, 150, fill='red')
light8 = canvas.create_oval(180, 140, 190, 150, fill='orange')

# Animate the lights
animate()

# Run the Tkinter event loop
root.mainloop()

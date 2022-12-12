import tkinter as tk

# Create the window
window = tk.Tk()
window.title("Pong")

# Create the canvas
canvas = tk.Canvas(window, width=600, height=400)
canvas.pack()

# Create the paddles
left_paddle = canvas.create_rectangle(10, 150, 30, 250, fill="white")
right_paddle = canvas.create_rectangle(570, 150, 590, 250, fill="white")

# Move the left paddle up
def move_up(event):
    canvas.move(left_paddle, 0, -10)

# Move the left paddle down
def move_down(event):
    canvas.move(left_paddle, 0, 10)

# Bind the keys to the corresponding paddle movements
canvas.bind("<w>", move_up)
canvas.bind("<s>", move_down)

# Create the ball
ball = canvas.create_oval(290, 190, 310, 210, fill="black")

# Function to move the ball
def move_ball():
    canvas.move(ball, 5, 0)

# Call the move_ball function continuously
while True:
    move_ball()
    window.update()

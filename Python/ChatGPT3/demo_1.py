import tkinter as tk

class Circle:
    def __init__(self, x, y, radius, canvas):
        self.x = x
        self.y = y
        self.radius = radius
        self.canvas = canvas
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0.1
        self.gravity = 0.1

    def update(self):
        print(f"update")
        self.velocity_x += self.acceleration_x
        self.velocity_y += self.acceleration_y
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill="red"
        )

    def move_left(self, event):
        self.acceleration_x -= self.gravity
    
    def move_right(self, event):
        self.acceleration_x += self.gravity
    
    def move_up(self, event):
        print(f"move_up")
        self.acceleration_y -= self.gravity
    
    def move_down(self, event):
        self.acceleration_y += self.gravity

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()
        self.circle = Circle(100, 100, 20, self.canvas)
        self.root.bind("<Left>", self.circle.move_left)
        self.root.bind("<Right>", self.circle.move_right)
        self.root.bind("<Up>", self.circle.move_up)
        self.root.bind("<Down>", self.circle.move_down)
        self.root.after(0, self.update)
        self.root.mainloop()
    
    def update(self):
        self.circle.update()
        self.after(1, self.update)
		
		
if __name__ == "__main__":
	App()

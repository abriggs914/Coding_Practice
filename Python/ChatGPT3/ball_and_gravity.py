import tkinter as tk

class Ball:
    def __init__(self, canvas, x, y, r, vx=0, vy=0, color='red'):
        self.canvas = canvas
        self.id = canvas.create_oval(x-r, y-r, x+r, y+r, fill=color)
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0.5
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        
    def move(self):
        self.vy += self.ay
        self.y += self.vy
        if self.y + self.r > self.canvas_height:
            self.y = self.canvas_height - self.r
            self.vy *= -0.9
        self.vx += self.ax
        self.x += self.vx
        if self.x + self.r > self.canvas_width:
            self.x = self.canvas_width - self.r
            self.vx *= -0.9
        elif self.x - self.r < 0:
            self.x = self.r
            self.vx *= -0.9
        self.canvas.coords(self.id, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.ball = Ball(self.canvas, 200, 200, 20)
        self.bind_keys()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=400, bg='white')
        self.canvas.pack()

    def bind_keys(self):
        self.canvas.bind('<Left>', lambda event: self.move_ball(-5, 0))
        self.canvas.bind('<Right>', lambda event: self.move_ball(5, 0))
        self.canvas.bind('<Up>', lambda event: self.move_ball(0, -5))
        self.canvas.bind('<Down>', lambda event: self.move_ball(0, 5))
        
    def move_ball(self, x, y):
        self.ball.ax = x/20
        self.ball.ay = y/20
        self.ball.vx *= 0.99
        self.ball.vy *= 0.99
        self.ball.move()
		

if __name__ == "__main__":


	root = tk.Tk()
	app = Application(master=root)
	app.mainloop()
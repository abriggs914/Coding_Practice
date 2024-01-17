import tkinter
import random
	

A = (10, 270)
B = (310, 270)
C = (160, 10)
triangle_points = [A, B, C]


def add_point(pt, r=2):
	can.create_oval(pt[0]-(r//2), pt[1]-(r//2), pt[0]+(r//2), pt[1]+(r//2), fill="#000000")
	can.update()
		
		
def loop_serpenski(pt, n, t):
	if n <= 0:
		return
	
	tri_pt = triangle_points[random.randint(0, 2)]
	pt = pt[0] + ((tri_pt[0] - pt[0]) // 2), pt[1] + ((tri_pt[1] - pt[1]) // 2)
	add_point(pt)
	
	win.after(t, lambda pt_=pt, n_=n-1, t_=t: loop_serpenski(pt_, n_, t_))
		

def start_serpenski(n, t=10):
	min_x, max_y, max_x, min_y = *A, B[0], C[1]
	pt = (random.randint(min_x + 1, max_x - 1), random.randint(min_y + 1, max_y - 1))
	loop_serpenski(pt, n, t)
	

if __name__ == "__main__":
		
	win = tkinter.Tk()
	win.geometry(f"800x550")
	can = tkinter.Canvas(win, width=400, height=400, bg="#E10000")
	
	[add_point(p, r=8) for p in triangle_points]
	
	can.pack()
	tkinter.Button(win, text="start", command=lambda: start_serpenski(2500)).pack()
	
	win.mainloop()

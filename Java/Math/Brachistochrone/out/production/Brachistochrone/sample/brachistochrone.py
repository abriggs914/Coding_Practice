from math import *
from decimal import Decimal
from bisection import bisection, non_zero_bisection
import matplotlib.pyplot as plt
import numpy as np 
import sys

class Brachistochrone:

	def __init__(self, x1, y1, x2, y2, segments):
		print("IN (" + str(x1) + ", " + str(y1) + "), (" + str(x2) + ", " + str(y2) + ")")
		xt, yt = (x1, y1) if y1 >= y2 else (x2, y2)
		x2, y2 = (x2, y2) if y1 >= y2 else (x1, y1)
		x1, y1 = xt, yt# if y1 >= y2 else x1, y1
		print("OUT (" + str(x1) + ", " + str(y1) + "), (" + str(x2) + ", " + str(y2) + ")")
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.segments = segments
		self.points = self.calc_points()
		
	def calc_points(self):
		brachistochrone_x = lambda r, t, f_x: Decimal(f_x) + (Decimal(r) * (t - Decimal(sin(t))))
		brachistochrone_y = lambda r, t, f_y: Decimal(f_y) + (Decimal(r) * (Decimal(-1) + Decimal(cos(t))))
		t_equation = lambda x, y, t: (y * (t - Decimal(sin(t)))) - (x * (1 - Decimal(cos(t))))
		
		x1 = self.x1
		y1 = self.y1
		x2 = self.x2
		y2 = self.y2
		
		xs = []
		ys = []
		delta_x = Decimal(0 - x1)
		delta_y = Decimal(0 - y1)
		off_x = Decimal(-1) * delta_x
		off_y = Decimal(-1) * delta_y

		x_val = Decimal(x2)
		x_val *= Decimal(1) if x_val >= 0 else Decimal(-1)
		x_val += delta_x
		y_val = Decimal(y2)
		y_val *= Decimal(1) if y_val >= 0 else Decimal(-1)
		y_val += delta_y

		# off_x *= 2 if ((x2 < 0) ^ (x_val < 0)) else 1
		# off_y *= 2 if ((y2 < 0) ^ (y_val < 0)) else 1
		
		t = non_zero_bisection(t_equation, [-360, 360], times=25, args=[x_val, y_val])
		
		print("".join(["#" for i in range(50)]))
		print("x2: " + str(x2) + ", y2: " + str(y2))
		print("x_val: " + str(x_val) + ", y_val: " + str(y_val))
		print("delta_x: " + str(delta_x) + ", delta_y: " + str(delta_y))
		# print("off_x: " + str(off_x) + ", off_y: " + str(off_y))
		print("t: " + str(t))
		print("".join(["#" for i in range(50)]))
		
		i = 0
		j = 0
		
		d = t / Decimal(self.segments)
		r = abs(Decimal(y_val) / (Decimal(1) - Decimal(cos(t))))
		print("r: " + str(r))
		print("d: " + str(d))
		while i <= abs(t) :
			bx = brachistochrone_x(r, i, (x1))
			by = brachistochrone_y(r, i, (y1))
			xs.append((bx-x1))# + (off_x))
			ys.append((by-y1))# + (off_y))
			i += abs(d)
			j += 1
			
		print("xs before: " + str(xs))
		print("ys before: " + str(ys))
		if x2 != x_val:
			# xd = (abs(x2) - abs(x_val)) / segments
			xd = abs((x2 - x1) / x_val)
			print("xd: " + str(xd))
			xs = [(xd * x) + x1 for i, x in enumerate(xs)]
			# xns = [(x1 + x) * off_x for i, x in enumerate(xns)]
		if y2 != y_val:
			# yd = (abs(y2) - abs(y_val)) / segments
			yd = abs((y2 - y1) / y_val)
			print("yd: " + str(yd))
			ys = [(yd * y) + y1 for i, y in enumerate(ys)]
			# yns = [(y1 + y) * off_y for i, y in enumerate(yns)]
		print("xs after: " + str(xs))
		print("ys after: " + str(ys))
		for x, y in zip(xs, ys):
			print("(xn,yn): (" + str(x) + "," + str(y) + ")")
		
		return [(x, y) for x, y in zip(xs, ys)]
		
	def plot(self):
		xs = [p[0] for p in self.points]
		ys = [p[1] for p in self.points]
		xsys_plot = plt.plot(xs, ys, label="brachistochrone")

		h = 100
		k = 100
		r = 100
		
		solve_y = lambda x, h, k, r: sqrt(r**2 - (x - h)**2) + k
		top_f = lambda x, h, k, r: solve_y(x, h, k, r)
		bottom_f = lambda x, h, k, r: (-1 * solve_y(x, h, k, r)) + (2 * k)
		graph(top_f, range(0, 201), (h, k, r))
		graph(bottom_f, range(0, 201), (h, k, r))

		plt.legend(loc="upper left")
		plt.ylabel("y")
		plt.xlabel("x")
		plt.gca().set_aspect("equal")
		plt.plot(self.x1, self.y1, 'r+')
		plt.plot(self.x2, self.y2, 'r+')
		plt.show()

# Rotate a 2D point about the origin a given amount of degrees
def rotate_on_origin(px, py, theta):
	# x′ = x * cos(θ) - y * sin(θ)
    # y′ = x * sin(θ) + y * cos(θ)
	t = radians(theta)
	x = (px * cos(t)) - (py * sin(t))
	y = (px * sin(t)) + (py * cos(t))
	return x, y
	
def rotate_point(cx, cy, px, py, theta):
	xd = 0 - cx
	yd = 0 - cy
	rx, ry = rotate_on_origin(px + xd, py + yd, theta)
	# print("cx:", cx, "cy:", cy, "\npx:", px, "py:", py, "\npx - xd:", px - xd, "py - yd:", py - yd, "\nxd:", xd, "yd:", yd, "\nrx:", rx, "ry:", ry, "\nrx - xd:", rx - xd, "ry - yd", ry - yd, "\ntheta:", theta)
	return rx - xd, ry - yd
	
# compute the angle of the right_angled triangle formed from a 
# given center point and cordinates x and y.
# Quadrants are specified to the 2D coordinate system where right
# is positive x direction and down is positive y direction.
# Returns the angle in degrees.
def compute_angle(cx, cy, x, y):
	opp = abs(y - cy)
	adj = abs(x - cx)
	if adj == 0:
		adj = 1
	a = degrees(atan(opp / adj))
	delta_x = x - cx
	delta_y = y - cy
	# Quadrant 2 - Cartesian 3
	if delta_x < 0 and delta_y >= 0:
		a = 180 - a
	# Quadrant 3 - Cartesian 2
	if delta_y < 0 and delta_x < 0:
		a += 180
	# Quadrant 4 - Cartesian 1
	if delta_y < 0 and delta_x >= 0:
		a = 360 - a
	return (a)

def calc_segments(start, stop, segments):
	segs = []
	t = start
	start = min(t, stop)
	stop = max(t, stop)
	v = (stop - start) / segments
	for i in range(segments + 1):
		segs.append(start + (i * v))
	return segs

def graph(f, x_range, args, show=False):
	xs = np.array(x_range)  
	ys = [f(x, *args) for x in xs]
	plt.plot(xs, ys)
	if show:
		plt.show()

def sample():
	brachistochrone_x = lambda r, t, f_x: f_x + (r * (t - sin(t)))
	brachistochrone_y = lambda r, t, f_y: f_y + (r * (-1 + cos(t)))

	segments = 20

	x1 = 20
	y1 = 40
	x2 = 40
	y2 = 20
	# x1 = 1
	# y1 = 1
	# x2 = 5
	# y2 = -5
	# a = -1.04172

	xs = []
	ys = []
	xns = []
	yns = []
	t = abs(compute_angle(0, 0, x2, y2) - compute_angle(0, 0, x1, y1))

	solve_x = lambda y, h, k, r: sqrt(r**2 - (y - k)**2) + h
	solve_y = lambda x, h, k, r: sqrt(r**2 - (x - h)**2) + k
	top_f = lambda x, h, k, r: solve_y(x, h, k, r)
	bottom_f = lambda x, h, k, r: (-1 * solve_y(x, h, k, r)) + (2 * k)
	slope = lambda x1, y1, x2, y2: (y2 - y1) / (x2 - x1)
	# solve for the y of a given line. needs 2 points on the line and point x to calculate.
	linear = lambda x, x1, y1, x2, y2: (slope(x1, y1, x2, y2) * x) + (y1 - (slope(x1, y1, x2, y2) * x1))
	print("t: " + str(t))
	# for theta in thetas:
		# bx = brachistochrone_x(a, theta, x1)
		# by = brachistochrone_y(a, theta, y1)
		# # xs.append(rotate_point(x1, y1, bx, by, 180))
		# # ys.append(rotate_point(x1, y1, bx, by, 180))
		# xs.append(bx)
		# ys.append(by)
		# print("(" + str(bx) + ", " + str(by) + ")")
		
		
	# t_equation = lambda x, y, t : ((y * (t - sin(radians(t)))) - (x * (1 - cos(radians(t)))))

	def t_equation(x, y, t):
		# print("x: " + str(x) + ", y: " + str(y) + ", t: " + str(t))
		# return ((y * (t - sin(radians(t)))) - (x * (1 - cos(radians(t)))))
		return ((y * (t - sin(t))) - (x * (1 - cos(t))))

	delta_x = (0 - x1)
	delta_y = (0 - y1)
	off_x = -1 * delta_x
	off_y = -1 * delta_y

	x_val = x2
	x_val *= 1 if x_val >= 0 else -1
	x_val += delta_x
	y_val = y2
	y_val *= 1 if y_val >= 0 else -1
	y_val += delta_y

	off_x *= 2 if ((x2 < 0) ^ (x_val < 0)) else 1
	off_y *= 2 if ((y2 < 0) ^ (y_val < 0)) else 1

	print("x2: " + str(x2) + ", y2: " + str(y2))
	print("x_val: " + str(x_val) + ", y_val: " + str(y_val))
	print("delta_x: " + str(delta_x) + ", delta_y: " + str(delta_y))
	print("off_x: " + str(off_x) + ", off_y: " + str(off_y))
	t = bisection(t_equation, [0, 359], times=25, args=[x_val, y_val])
	print("t: " + str(t))
	# for i, x in enumerate(range(x1, x2+1, round((abs(x2 - x1) / segments)))):
		# # t = 15.4505#(180. / segments) * i
		# bx = brachistochrone_x(a, t, x)
		# by = brachistochrone_y(a, t, linear(x, x1, y1, x2, y2))
		# # xs.append(rotate_point(x1, y1, bx, by, 180))
		# # ys.append(rotate_point(x1, y1, bx, by, 180))
		# xs.append(bx)
		# ys.append(by)
		# print("(" + str(bx) + ", " + str(by) + ")")

	i = 0
	j = 0
	# off_x /= segments
	# off_y /= segments
	# rt = radians(t)
	d = t / segments
	r = y_val / (1 - cos(t))
	print("r: " + str(r))
	while i <= t :
		bx = brachistochrone_x(r, i, (x1))
		by = brachistochrone_y(r, i, (y1))
		xs.append(bx)
		ys.append(by)
		xns.append((bx-x1))# + (off_x))
		yns.append((by-y1))# + (off_y))
		i += d
		j += 1
		
	if x2 != x_val:
		# xd = (abs(x2) - abs(x_val)) / segments
		xd = abs((x2 - x1) / x_val)
		print("xd: " + str(xd))
		xns = [(xd * x) + x1 for i, x in enumerate(xns)]
		# xns = [(x1 + x) * off_x for i, x in enumerate(xns)]
	if y2 != y_val:
		# yd = (abs(y2) - abs(y_val)) / segments
		yd = abs((y2 - y1) / y_val)
		print("yd: " + str(yd))
		yns = [(yd * y) + y1 for i, y in enumerate(yns)]
		# yns = [(y1 + y) * off_y for i, y in enumerate(yns)]
	for x, y in zip(xs, ys):
		print("(x,y): (" + str(x) + "," + str(y) + ")")
	for x, y in zip(xns, yns):
		print("(xn,yn): (" + str(x) + "," + str(y) + ")")
	xsys_plot = plt.plot(xs, ys, label="xsys")
	xnsyns_plot = plt.plot(xns, yns, label="xnsyns")

	h = 100
	k = 100
	r = 100
	graph(top_f, range(0, 201), (h, k, r))
	graph(bottom_f, range(0, 201), (h, k, r))

	plt.legend(loc="upper left")
	plt.ylabel("y")
	plt.xlabel("x")
	plt.gca().set_aspect("equal")
	plt.plot(x1, y1, 'r+')
	plt.plot(x2, y2, 'r+')
	plt.show()

# def newton_root(func, )

if __name__ == "__main__":
	x1 = 20
	y1 = 40
	x2 = 40
	y2 = 20
	# sample()
	b1 = Brachistochrone(x1, y1, x2, y2, 20)
	b1.plot()
	
	x1 = 1
	y1 = 1
	x2 = 5
	y2 = -5
	b2 = Brachistochrone(x1, y1, x2, y2, 20)
	b2.plot()
	
	x1 = 40
	y1 = 20
	x2 = 20
	y2 = 160
	b3 = Brachistochrone(x1, y1, x2, y2, 20)
	b3.plot()
	
	# f = lambda x : (x+8)*(x - 1)
	# p = non_zero_bisection(f, [-100, 100], times=10)
	# print("non-zero: " + str(p))

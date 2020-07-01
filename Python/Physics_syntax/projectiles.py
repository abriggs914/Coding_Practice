import math

time_units = {
	"seconds": 1,
	"minutes": 60,
	"hours": 3600
}

# class representing a 2D vector
class Vector:

	def __init__(self, magnitude, angle, in_degrees=True):
		self.magnitude = abs(magnitude)
		if in_degrees:
			angle = math.radians(angle)
		self.angle = angle
		
	def get_components(self):
		"""return the x and y components of a 2D vector"""
		return self.magnitude * math.cos(self.angle), self.magnitude * math.sin(self.angle)

# simple acceleration

# compute final velocity in one dimension
final_velocity = lambda v0, a, t: v0 + (a * t)

# compute final positons in one dimension
final_position = lambda p0, v0, a, t: p0 + (v0 * t) + (0.5 * a * t**2)

def final_x_velocity(vx0, ax, t):
	return final_velocity(vx0, ax, t)

def final_y_velocity(vy0, ay, t):
	return final_velocity(vy0, ay, t)
	
def final_x(x0, vx0, ax, t):
	return final_position(x0, vx0, ax, t)
	
def final_y(y0, vy0, ay, t):
	return final_position(y0, vy0, ay, t)
	
def compute_acceleration(a, theta):
	return abs(a) * math.cos(theta), abs(a) * math.sin(theta)


initial_vector = Vector(0, 0)
gravity = Vector(-9.81, 90)

# initial x and y coordinates
x0, y0 = (0, 0)

# initial x and y velovities
vx0, vy0 = initial_vector.get_components()

# force of acceleration
acceleration = gravity
angle = math.radians(90)
t = 1

ax, ay = acceleration.get_components()

print("x acceleration   {0}".format(ax))
print("y acceleration   {0}".format(ay))
print("final x velocity {0}".format(final_x_velocity(vx0, ax, t)))
print("final y velocity {0}".format(final_y_velocity(vy0, ay, t)))
print("final x position {0}".format(final_x(x0, vx0, ax, t)))
print("final y position {0}".format(final_y(y0, vy0, ay, t)))

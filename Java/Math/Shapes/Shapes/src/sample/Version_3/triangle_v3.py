import math

SIDE_A = 0
SIDE_B = 1
SIDE_C = 2
ANGLE_A = 3
ANGLE_B = 4
ANGLE_C = 5

class Triangle:
	
	def __init__(self, name=None, a=None, b=None, c=None, A=None, B=None, C=None):
		self.name=name
		self.a=a
		self.b=b
		self.c=c
		self.A=A
		self.B=B
		self.C=C
	
	def __repr__(self):
		return "Triangle: " + self.name + "\na: " + str(self.a) + "\nb: " + str(self.b) + "\nc: " + str(self.c) + "\nA: " + str(self.A) + "\nB: " + str(self.B) + "\nC: " + str(self.C)
		
		
	def solve(self):
		attrs = [SIDE_A, SIDE_B, SIDE_C, ANGLE_A, ANGLE_B, ANGLE_C]
		c = sum([1 for i in attrs if self.getAttr(i) is not None])
		if c > 2 and [i for i in [self.a, self.b, self.c] if i is not None]:
			i = c
			while c < 6:
				print("c: " + str(c) + "\n" + str(self))
				if self.a is not None and self.b is not None and self.c is not None:
					self.loc(ANGLE_A)
					self.loc(ANGLE_B)
					self.loc(ANGLE_C)
				if self.a is not None and self.b is not None and self.C is not None:
					self.loc(SIDE_C)
				if self.a is not None and self.c is not None and self.B is not None:
					self.loc(SIDE_B)
				if self.b is not None and self.c is not None and self.A is not None:
					self.loc(SIDE_A)
				pair_a = self.a is not None and self.A is not None
				pair_b = self.b is not None and self.B is not None
				pair_c = self.c is not None and self.C is not None
				if pair_a or pair_b or pair_c:
					pair = (self.a, self.A) if pair_a else ((self.b, self.B) if pair_b else (self.c, self.C))
					if pair_a is not None and any([self.b, self.c, self.B, self.C]):
						self.los(pair)
					if pair_b is not None and any([self.a, self.c, self.A, self.C]):
						self.los(pair)
					if pair_c is not None and any([self.a, self.b, self.A, self.B]):
						self.los(pair)
				found_angles = sum([1 for i in [ANGLE_A, ANGLE_B, ANGLE_C] if self.getAttr(i) is not None])
				print("found_angles: " + str(found_angles))
				if found_angles == 2:
					if self.A is None:
						self.A = self.compute_angle(ANGLE_B, ANGLE_C)
					if self.B is None:
						self.B = self.compute_angle(ANGLE_A, ANGLE_C)
					if self.C is None:
						self.C = self.compute_angle(ANGLE_A, ANGLE_B)
				c = sum([1 for i in attrs if self.getAttr(i) is not None])
			if sum([self.a, self.b, self.c]) != 180:
				# raise ValueError("Interior angles do not sum to 180 degrees.")
				pass
		else:
			raise ValueError("Not enough known values to solve.")
				
	def compute_angle(self, code_a, code_b):
		print("COMPUTING")
		return 180 - self.getAttr(code_a) - self.getAttr(code_b)
	
	def getAttr(self, code):
		if code == SIDE_A:
			return self.a
		if code == SIDE_B:
			return self.b
		if code == SIDE_C:
			return self.c
		if code == ANGLE_A:
			return self.A
		if code == ANGLE_B:
			return self.B
		if code == ANGLE_C:
			return self.C
		
	def loc_side(self, a, b, C):
		return math.sqrt(a**2 + b**2 - (2 * a * b * math.cos(math.radians(C))))
		
	def loc_angle(self, a, b, c):
		return math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))
		
	def loc(self, code):
		a = self.a
		b = self.b
		c = self.c
		A = self.A
		B = self.B
		C = self.C
		if code == SIDE_A:
			if self.a is not None:
				return self.a
			self.a = self.loc_side(b, c, A)
		if code == SIDE_B:
			if self.b is not None:
				return self.b
			self.b = self.loc_side(a, c, B)
		if code == SIDE_C:
			if self.c is not None:
				return self.c
			self.c = self.loc_side(a, b, C)
		if code == ANGLE_A:
			if self.A is not None:
				return self.A
			self.A = self.loc_angle(a, b, c)
		if code == ANGLE_B:
			if self.B is not None:
				return self.B
			self.B = self.loc_angle(b, c, a)
		if code == ANGLE_C:
			if self.C is not None:
				return self.C
			self.C = self.loc_angle(c, a, b)
			
	def los(self, pair):
		#print("pair: " + str(pair))
		#l = [SIDE_A, SIDE_B, SIDE_C, ANGLE_A, ANGLE_B, ANGLE_C]
		#for i in l:
		#	print("attr: (" + str(i) + "): " + str(self.getAttr(i)))
		if self.a is None and self.A is not None:
			self.a = self.los_side(self.A, pair[0], pair[1])
		if self.b is None and self.B is not None:
			self.b = self.los_side(self.B, pair[0], pair[1])
		if self.c is None and self.C is not None:
			self.c = self.los_side(self.C, pair[0], pair[1])
		if self.A is None and self.a is not None:
			self.A = self.los_angle(self.a, pair[1], pair[0])
		if self.B is None and self.b is not None:
			self.B = self.los_angle(self.b, pair[1], pair[0])
		if self.C is None and self.c is not None:
			self.C = self.los_angle(self.c, pair[1], pair[0])
				
	def los_side(self, A, b, C):
		print("los side")
		return math.sin(math.radians(A)) * (b / math.sin(math.radians(C)))
		
	def los_angle(self, a, B, c):
		return math.degrees(math.asin(a * (math.sin(math.radians(B)) / c)))
			
t1 = Triangle("t1", 50, 40, 30, None, None, None)
t1.solve()
print(t1)
			
t2 = Triangle("t2", 110, None, None, 32, None, 18)
t2.solve()
print(t2)

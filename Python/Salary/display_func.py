from enum import Enum


f1  = "y = mx+b", "y = m * x + b"
f2  = "y = m x + b", "y = m * x + b"
f3  = "y=mx+b", "y = m * x + b"
f4  = "y = m*x+b", "y = m * x + b"
f5  = "y = m*x +b", "y = m * x + b"
f6  = "y = m*x + b", "y = m * x + b"
f7  = "y = m *x+b", "y = m * x + b"
f8  = "y = m * x+b", "y = m * x + b"
f9  = "y = m * x +b", "y = m * x + b"
f10 = "y = m * x + b", "y = m * x + b"
f11 = "y = m*x+ b", "y = m * x + b"


class Operators(Enum):
	def __new__(cls, *args, **kwds):
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value
		return obj
		
	def __init__(self, n, f):
		self.n = n
		self.f = f

	ADDITION = "+", lambda a, b : a + b
	SUBTRACTION = "-", lambda a, b : a - b
	MULTIPLICATION = "*", lambda a, b : a * b
	DIVISION = "/", lambda a, b : a / b
	POWER = "^", lambda a, b : a ** b

def display_func(f):
	operators = ["(", ")", "="] + [op.n for op in Operators]
	bracket_idxs = [i for i in f if i == "(" or i == ")"]
	lefts, rights = [], []
	for i in bracket_idxs:
		if f[i] == "(":
			lefts.append(i)
		if f[i] == ")":
			rights.append(i)
	if len(bracket_idxs) % 2 == 1 or len(lefts) != len(rights):
		# unmatched brackets
		raise ValueError("unmatched brackets: <<{0}>>".format(f))
	bracket_groups = []
	res = 
	return res
	
if __name__ == "__main__":
	to_test = [f1, f2, f3, f4, f4, f6, f7, f8, f9, f10, f11]
	border = "".join(["#" for i in range(45)])
	for t in to_test:
		print("tst: " + str(t) + " tst[0]: " + str(t[0]) + " tst[1]: " + str(t[1]))
		func, results = t
		res = display_func(func)
		print("{b}\nFUNC ARGS: <<{a}>>\nRES: <<{r}>>\nDESIRED: <<{d}>>\nCORRECT: <<{c}>>\n{b}".format(b=border, a=func, r=res, d=results, c=res==results))
	
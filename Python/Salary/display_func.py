from enum import Enum
from characters import Chars


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
f12 = "(y = ((m*(x)))+ b)", "y = m * x + b"
f13 = "((y) = (((m*(x)))+ (b)))", "y = m * x + b"


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
	
	
def text_wh(t):
	s = t.split("\n")
	return max([len(l) for l in s]), len(s)

		
def dict_print(n, d):
	m = "--  " + str(n) + "  --\n"
	for k, v in d.items():
		ml = str(k)
		ml += ("<<" + str(v) + ">>").rjust(18 - len(ml), ".") + "\n"
		m += ml
	return m
	
def indexOf(s, v, start=None, end=None, times=1):
	if not start:
		start = 0
	if not end:
		end = len(s)
		
	i = s.index(v, start, end)
	
	print("[\n\ts: {s}\n\tv: {v}\n\ti: {i}\n\tstart: {st}\n\tend: {e}\n\ttimes: {t}\n]".format(s=s, v=v, i=i, st=start, e=end, t=times))
	if times == 1:
		return i
	return indexOf(s, v, start=i+1, end=end, times=times-1)
	
def index_match_bracket(s):
	l, r = 0, 0
	for i, c in enumerate(s):
		if c == "(":
			l += 1
		if c == ")":
			r += 1
			if l != 0 and r != 0 and l == r:
				return i
	return -1

def collect_bracket_groups(f, lefts):
	groups = {} # key is char index in f, val is the substring forming a closed set of brackets
	# for i, c in enumerate(f):
	for n, i in enumerate(lefts):
		sub = f[i:]
		print("  f[i:]: {f}".format(f=sub))
		# cant use regular index function here because it defaults to first encounter, which typically is the most inner-nested set
		j = -1 if ")" not in sub else (index_match_bracket(sub) + (len(f) - len(sub))) 
		print("MATCHED:\n\tf[i:j]: <<{f}>>\n\ti: {i}\tj: {j}".format(f=sub[:j+1], i=i, j=j))
		if j < 0:
			return None
		brackets = f[i: j+1]
		groups[i] = brackets
	return groups
				

def display_func(f):
	operators = ["(", ")", "="] + [op.n for op in Operators]
	bracket_idxs = [i for i, c in enumerate(f) if c == "(" or c == ")"]
	lefts, rights = [], []
	print("f:               {f}\nbracket indexes: {b}\nlefts:           {l}\nright:           {r}".format(f=f, b=bracket_idxs, l=lefts, r=rights))
	for i in bracket_idxs:
		if f[i] == "(":
			lefts.append(i)
		if f[i] == ")":
			rights.append(i)
	if len(bracket_idxs) % 2 == 1 or len(lefts) != len(rights):
		# unmatched brackets
		raise ValueError("unmatched brackets: <<{0}>>".format(f))
	print("f:               {f}\nbracket indexes: {b}\nlefts:           {l}\nright:           {r}".format(f=f, b=bracket_idxs, l=lefts, r=rights))
	bracket_groups = collect_bracket_groups(f, lefts)
	print(dict_print("bracket groups", bracket_groups))
	if not bracket_groups and (lefts or rights):
		raise ValueError("mismatched brackets <<{0}>>".format(f))
	
	
	res = None
	return res
	
if __name__ == "__main__":
	to_test = {} 
	names = ["f1", "f2", "f3", "f4", "f4", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13"]
	tests = [f1, f2, f3, f4, f4, f6, f7, f8, f9, f10, f11, f12, f13]
	# to_test = dict(zip(names, tests))
	to_test["f1"] = f1
	to_test["f2"] = f2
	to_test["f3"] = f3
	to_test["f4"] = f4
	to_test["f5"] = f5
	to_test["f6"] = f6
	to_test["f7"] = f7
	to_test["f8"] = f8
	to_test["f9"] = f9
	to_test["f10"] = f10
	to_test["f11"] = f11
	to_test["f12"] = f12
	to_test["f13"] = f13
	border = "".join(["#" for i in range(45)])
	for n, t in to_test.items():
		# print("tst: " + str(t) + " tst[0]: " + str(t[0]) + " tst[1]: " + str(t[1]))
		func, results = t
		res = display_func(func)
		print("{b}\n\t--  {n}  --\nFUNC ARGS: <<{a}>>\nRES: <<{r}>>\nDESIRED: <<{d}>>\nCORRECT: <<{c}>>\n{b}".format(n=n, b=border, a=func, r=res, d=results, c=res==results))
	
	for c in Chars:
		print("\n" + c.j_s+"\n")
from enum import Enum

class Chars(Enum):
	def __new__(cls, *args, **kwds):
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value
		return obj
		
	def __init__(self, c, j):
		self.c = c
		self.j = j
		self.j_s = j.replace(c, "#")#"".join(["#" if s != " " else s for s in j])

	ONE = "1", "  1  \n  1  \n  1  \n  1  \n  1  "
	TWO = "2", "22222\n    2\n22222\n2    \n22222"
	THREE = "3", "33333\n    3\n  333\n    3\n33333"
	FOUR = "4", "    4\n4   4\n44444\n    4\n    4"
	FIVE = "5", "55555\n5     \n55555\n    5\n55555"
	SIX = "6", "66666\n6    \n66666\n6   6\n66666"
	SEVEN = "7", "77777\n    7\n    7\n    7\n    7"
	EIGHT = "8", "88888\n8   8\n88888\n8   8\n88888"
	NINE = "9", "99999\n9   9\n99999\n    9\n    9"
	ZERO = "0", "00000\n0   0\n0   0\n0   0\n00000"
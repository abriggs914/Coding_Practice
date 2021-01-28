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
		self.j_s = j.replace(c, "#")

	ONE = "1", "  1  \n  1  \n  1  \n  1  \n  1  "
	TWO = "2", "22222\n    2\n22222\n2    \n22222"
	THREE = "3", "33333\n    3\n  333\n    3\n33333"
	FOUR = "4", "    4\n4   4\n44444\n    4\n    4"
	FIVE = "5", "55555\n5     \n55555\n    5\n55555"
	SIX = "6", "66666\n6    \n66666\n6   6\n66666"
	SEVEN = "7", "77777\n    7\n    7\n    7\n    7"
	EIGHT = "8", "88888\n8   8\n88888\n8   8\n88888"
	NINE = "9", "99999\n9   9\n99999\n    9\n    9"
	ZERO = "0", "00000\n00  0\n0 0 0\n0  00\n00000"
	A = "A", "  A  \n A A \nAA AA\nAAAAA\nA   A"
	B = "B", "BBBB \nB  BB\nBBBB \nB   B\nBBBBB"
	C = "C", " CCCC\nC    \nC    \nC    \n CCCC"
	D = "D", "DDDD \nD   D\nD   D\nD   D\nDDDD "
	E = "E", "EEEEE\nE    \nEEE  \nE    \nEEEEE"
	F = "F", "FFFFF\nF    \nFFF  \nF    \nF    "
	G = "G", "GGGGG\nG    \nG  GG\nG   G\nGGGGG"
	H = "H", "H   H\nH   H\nHHHHH\nH   H\nH   H"
	I = "I", "IIIII\n  I  \n  I  \n  I  \nIIIII"
	J = "J", "JJJJJ\n  J  \n  J  \nJ J  \nJJJ  "
	K = "K", "K   K\nK  K \nKKK  \nK  K \nK   K"
	L = "L", "L    \nL    \nL    \nL    \nLLLLL"
	M = "M", " M M \nMMMMM\nM M M\nM M M\nM M M"
	N = "N", "N   N\nNN  N\nN N N\nN  NN\nN   N"
	O = "O", " OOO \nO   O\nO   O\nO   O\n OOO "
	P = "P", "PPPP \nP   P\nPPPP \nP    \nP    "
	Q = "Q", " QQQ \nQ   Q\nQ   Q\nQ  QQ\n QQQQ"
	R = "R", "RRRR \nR   R\nRRRR \nR  R \nR   R"
	S = "S", " SSS \nS    \n SSS \n    S\n SSS "
	T = "T", "TTTTT\n  T  \n  T  \n  T  \n  T  "
	U = "U", "U   U\nU   U\nU   U\nU   U\n UUU "
	V = "V", "V   V\nV   V\nV   V\n V V \n  V  "
	W = "W", "W W W\nW W W\nW W W\nWWWWW\n W W "
	X = "X", "X   X\n X X \n  X  \n X X \nX   X"
	Y = "Y", "Y   Y\n Y Y \n  Y  \n  Y  \n  Y  "
	Z = "Z", "ZZZZZ\n   Z \n  Z  \n Z   \nZZZZZ"
	ADDITION = "+", "     \n  +  \n +++ \n  +  \n     "
	SUBTRACTION = "-", "     \n     \n --- \n     \n     "
	MULTIPLICATION = "X", "     \n X X \n  X  \n X X \n     "
	DIVISON = "/", "     \n   / \n  /  \n /   \n     "
	PERCENTAGE = "%", "%   %\n   % \n  %  \n %   \n%   %"
	# POWERS / LOGS / LARGE DIVISIONS / FRACTIONS / BRACKETS
	# are done differently than a 5x5 preset text 
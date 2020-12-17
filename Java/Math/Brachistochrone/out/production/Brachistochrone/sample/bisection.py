from math import sin, cos, radians, degrees
import sys
from decimal import Decimal

def bisection(f, intervals, times=5, args=None, negative=False):
	if args is None:
		args = []
	args = [Decimal(a) for a in args]
	intervals = [Decimal(i) for i in intervals]
	c = (intervals[0] + intervals[1]) / Decimal(2.0)
	v = None
	args += [c]
	print("ARGS: " + str(args))
	f1 = f(*(args[:-1] + [intervals[0]]))
	f2 = f(*(args[:-1] + [intervals[1]]))
	# print("\tf1: " + str(f1) + ", f2: " + str(f2) + ", check: " + str(not ((f1 < 0) ^ (f2 < 0))))
	if not ((f1 < 0) ^ (f2 < 0)):
		print("DIVERGING")
	if times > 1:
		v = f(*args)
		print("\nintervals: " + str(intervals) + ", c: " + str(c) + ", v: " + str(v) + ", f1: " + str(f1) + ", f2: " + str(f2) + ", times left: " + str(times - 1))
		if v < 0 :
			if negative:
				intervals = [intervals[0], c]
			else:
				intervals = [c, intervals[1]]
		elif v == 0:
			return c
		else:
			if negative:
				intervals = [c, intervals[1]]
			else:
				intervals = [intervals[0], c]
		return bisection(f, intervals, times - 1, args[:-1], negative)
	print("intervals: " + str(intervals) + ", c: " + str(c) + ", v: " + str(v) + ", times left: " + str(times - 1))
	print("bisected value: " + str(c))
	return c
	
# Return the approximated root closest to the mid-point of the given interval.
# Ensures the result is non-zero, returns None if no root is found or approximated
# root is not accurate enough. If function has both positive and negative roots
# the smallest of the two is returned.
def non_zero_bisection(f, intervals, times=5, args=None) :
	if 0 in range(*[int(n) for n in intervals]):
		low = Decimal(intervals[0])
		high = Decimal(intervals[1])
		error = abs((high - low) / Decimal(2)**(Decimal(times) + Decimal(1)))
		negative = bisection(f, [low, Decimal(0-error)], times=times, args=args, negative=True)
		positive = bisection(f, [Decimal(0+error), high], times=times, args=args)
		include_n = False
		include_p = False
		# negative root falls within the error regions, root not calculated correctly
		if (low + error) < negative < (0 - error) :
			# if (0 - error) > negative and (low + error) < negative :   (low + error) < negative < (0 - error)
			include_n = True
		# positive root falls within the error regions, root not calculated correctly
		if (0 + error) < positive < (high - error) :
			include_p = True
			
		root = None
		if include_n:
			root = negative
		if include_p:
			if root is not None:
				root = negative if abs(negative) < abs(positive) else positive
			else:
				root = positive
		print("negative: " + str(negative) + ", positive: " + str(positive) + ", error: " + str(error) + ", root: " + str(root))
		return root
	else:
		return bisection(f, intervals, times, args)
	
def bisection2(f,a,b,N, args=None):
	'''Approximate solution of f(x)=0 on interval [a,b] by bisection method.

	Parameters
	----------
	f : function
		The function for which we are trying to approximate a solution f(x)=0.
	a,b : numbers
		The interval in which to search for a solution. The function returns
		None if f(a)*f(b) >= 0 since a solution is not guaranteed.
	N : (positive) integer
		The number of iterations to implement.

	Returns
	-------
	x_N : number
		The midpoint of the Nth interval computed by the bisection method. The
		initial interval [a_0,b_0] is given by [a,b]. If f(m_n) == 0 for some
		midpoint m_n = (a_n + b_n)/2, then the function returns this solution.
		If all signs of values f(a_n), f(b_n) and f(m_n) are the same at any
		iteration, the bisection method fails and return None.

	Examples
	--------
	>>> f = lambda x: x**2 - x - 1
	>>> bisection(f,1,2,25)
	1.618033990263939
	>>> f = lambda x: (2*x - 1)*(x - 3)
	>>> bisection(f,0,1,10)
	0.5
	'''
	if args == None:
		args = []
	if f(*(args + [a]))*f(*(args + [b])) >= 0:
		print("Bisection method fails.")
		return None
	a_n = a
	b_n = b
	for n in range(1,N+1):
		m_n = (a_n + b_n)/2
		f_m_n = f(*(args + [m_n]))
		if f(*(args + [a_n]))*f_m_n < 0:
			a_n = a_n
			b_n = m_n
		elif f(*(args + [b_n]))*f_m_n < 0:
			a_n = m_n
			b_n = b_n
		elif f_m_n == 0:
			print("Found exact solution.")
			return m_n
		else:
			print("Bisection method fails.")
			return None
	return (a_n + b_n)/2
	
if __name__ == "__main__" :
	f = lambda x : x**2 + 3*x - 4
	print("\nbisection of f: " + str(bisection(f, [0, 5])))
	print("\nbisection of f: " + str(bisection(f, [1, 5])))
	print("\nbisection of f: " + str(bisection(f, [-8, 8], 12)))
	g = lambda x : x**3 + x**2 - 3*x - 3
	print("\nbisection of g: " + str(bisection(g, [1, 2])))
	h = lambda x, y, t : degrees((y * (radians(t) - sin(radians(t)))) - (x * (1 - cos(radians(t))))) 
	print("\nbisection of h: " + str(bisection(h, [-1000, 1000], times=25, args=[20, 40])))
	i = lambda x: x**2 - 1
	print("bisection of i: " + str(bisection(i, [-1000, 1000], times=0)))
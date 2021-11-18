import math

"""
Calculate Accrued Amount (Principal + Interest)
A = P(1 + r/n)nt
Calculate Principal Amount, solve for P
P = A / (1 + r/n)nt
Calculate rate of interest in decimal, solve for r
r = n[(A/P)^(1/nt) - 1]
Calculate rate of interest in percent
R = r * 100
Calculate time, solve for t
t = ln(A/P) / n[ln(1 + r/n)] = [ ln(A) - ln(P) ] / n[ln(1 + r/n)]
"""

"""
A = the value of the accrued investment/loan
P = the principal amount
r = the annual interest rate (decimal)
n = the number of times that interest is compounded per unit t
t = the time the money is invested or borrowed for
"""

A = 10000
P = 4200
r = 0.065
n = 12
t = 13.38

time_years = lambda A, P, r, n: math.log(A / P) / (n * math.log(1 + (r / n)))
time_months = lambda A, P, r, n: math.log(A / P) / (n * math.log(1 + (r / n))) * 12
future_value = lambda P, r, n, t: P * math.pow((1 + (r / n)), (n * t))
present_value = lambda A, r, n, t: A / ((1 + (r / n)) ** (n * t))
interest = lambda A, P, n, t: 100 * n * (math.pow((A / P), (1 / ((n * t)))) - 1)
gain = lambda P, r, n, t: future_value(P, r, n, t) - P
# gain(5000, 0.005, 12, 1.5)
# 5000 down at 0.5% monthly compounding interest for 1.5 years = $37.63

question1 = """
Zack purchased a bond with a face value of ${FV} for ${PV} to build a new sports
stadium. If the bond pays {IR}% annual interest compounded monthly, how long must
he hold it until it reaches its face value?
"""

def solve_question(question, formats, A=None, P=None, n=None, r=None, t=None):
	print(question.format(**formats))
	print("time_months: (" + str(time_months(A, P, r, n)) + ") equals (" + str(t*12) + ") == " + str(time_months(A, P, r, n) == (t*12)))
	print("time_years: (" + str(time_years(A, P, r, n)) + ") equals (" + str(t) + ") == " + str(time_years(A, P, r, n) == t))
	print("future_value: (" + str(future_value(P, r, n, t)) + ") equals (" + str(A) + ") == " + str(future_value(P, r, n, t) == A))
	print("present_value: (" + str(present_value(A, r, n, t)) + ") equals (" + str(P) + ") == " + str(present_value(A, r, n, t) == P))
	print("interest: (" + str(interest(A, P, n, t)) + ") equals (" + str(r*100) + ") == " + str(interest(A, P, n, t) == (r*100)))


solve_question(question1, {"FV":A, "PV":P, "IR":r*100}, A, P, n, r, t)
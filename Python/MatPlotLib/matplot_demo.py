import matplotlib.pyplot as plt
import numpy as np


def f_pay(x):
    """Pay per month"""
    return (1518.16*26/12)*x


def f_gas(x, use_abs=True):
    """Gas bill per month"""
    return (60*50/12)*x * (-1 if not use_abs else 1)
	
	
def f_insurance(x, use_abs=True):
    """Insurance bill per month"""
    return 140*x * (-1 if not use_abs else 1)
	

def f_student_loan(x, use_abs=True):
    """Student Loan bill per month"""
    return 600*x * (-1 if not use_abs else 1)

	
def f_honda(x, use_abs=True):
    """Honda bill per month"""
    return (369.96*26/12)*x * (-1 if not use_abs else 1)
	
	
def f_starlink(x, use_abs=True):
    """Starlink bill per month"""
    return 161*x * (-1 if not use_abs else 1)
	

def f_disney(x, use_abs=True):
    """Disney bill per month"""
    return (150/12)*x * (-1 if not use_abs else 1)
	
	
def f_prime(x, use_abs=True):
    """Prime bill per month"""
    return (140/12)*x * (-1 if not use_abs else 1)
	
	
def f_cnb(x, use_abs=True):
    """CNB bill per month"""
    return 380*x * (-1 if not use_abs else 1)
	
	
def f_xbox(x, use_abs=True):
    """XBox bill per month"""
    return 90*x * (-1 if not use_abs else 1)

	
def f_lotteries(x, use_abs=True):
    """Lottery bill per month"""
    return (2*2*52/12)*x * (-1 if not use_abs else 1)
	
	
def f_oil_change(x, use_abs=True):
    """oil_change bill per month"""
    return (250*2/12)*x * (-1 if not use_abs else 1)


f_positive = {
	"f_pay": f_pay
}


f_negative = {
	"f_gas": f_gas,
	"f_insurance": f_insurance,
	"f_student_loan": f_student_loan,
	"f_honda": f_honda,
	"f_starlink": f_starlink,
	"f_disney": f_disney,
	"f_prime": f_prime,
	"f_cnb": f_cnb,
	"f_xbox": f_xbox,
	"f_lotteries": f_lotteries,
	"f_oil_change": f_oil_change
}


to_plot = {}
to_plot.update(f_positive)
to_plot.update(f_negative)


def total_earnings(x, use_abs=True):
	return sum(map(lambda f: f(x), f_positive.values()))

	
def total_payments(x, use_abs=True):
	return sum(map(lambda f: f(x, use_abs=False), f_negative.values()))
	# return sum([
	#	sum(map(lambda f, f(x), f_positive.values()))
	#	+ sum(map(lambda f, f(x, use_abs=False), f_negative.values()))
	#for name, func in to_plot.items()])
	

def total_leftover(x):
	return total_earnings(x) + total_payments(x)
	

def est_balance(x):
	return total_leftover(x) + 2000
	
	
def f(x):
	return x**2
	
	
if __name__ == "__main__":
	
	begin_x, end_x = 0, 60  # in months
	begin_y, end_y = 0, 200000  # in dollars
	
	# Create x and y Ranges
	x = np.linspace(begin_x, end_x, 1000)
	fig, ax = plt.subplots()
	
	for name, func in to_plot.items():
		y = func(x)
	
		# Plot the Data
		ax.plot(x, y, label=name)
		
	ax.plot(x, total_earnings(x), label="Total Earnings")
	ax.plot(x, total_payments(x), label="Total Payments")
	ax.plot(x, total_leftover(x), label="Total Leftover")
	ax.plot(x, est_balance(x), label="Estimated Balance")
		
	
	# Modify the Axes Limits
	ax.set_xlim(begin_x, end_x)
	ax.set_ylim(begin_y, end_y)
	
	# Set axes title
	ax.set_title('Plotting Money Functions in Matplotlib', size=14)
	
	# Show legend
	plt.legend()
	
	# Show the Data
	plt.show()
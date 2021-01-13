import math
from enum import Enum

# from aenum import Enum  # for the aenum version
# Animal = Enum('Animal', 'ant bee cat dog')
# Animal.ant  # returns <Animal.ant: 1>
# Animal['ant']  # returns <Animal.ant: 1> (string lookup)
# Animal.ant.name  # returns 'ant' (inverse lookup)

TimeFrame = Enum("TimeFrame", "SECOND MINUTE HOURLY DAILY WEEKLY MONTHLY QUARTERLY WORK_SECOND WORK_MINUTE WORK_HOURLY WORK_DAILY WORK_WEEKLY WORK_MONTHLY WORK_QUARTERLY ANNUALLY BI_ANNUALLY N5YEARS DECADE")

class Salary:

    # base is in the form $ / year.
	def __init__(self, base):
		self.base = base
		
	def create_line(self, m, v, l, is_money=False, is_percentage=False):
		# print("m: {m}, v: {v}, l: {l}, is_money: {is_money}, is_percentage: {is_percentage}".format(m=m, v=v, l=l, is_money=is_money, is_percentage=is_percentage))
		m += " " if m[-1] != " " else ""
		if is_money:
			return m + ("$ %.2f" % v).rjust(l - len(m), ".")
		if is_percentage:
			return m + (("%.2f " % v) + "%").rjust(l - len(m), ".")
		return m + ("%.2f %" % v).ljust(l - len(m), ".")
		
	def __repr__(self):
		l = 40
		message = self.create_line("Base salary", self.base, l, {"is_money":True}) + "\n"
		generic_to_view = [
			("Annual tax rate", self.annual_tax_rate, [], {"is_percentage":True}),
			("Annual taxes", self.tax_amount, [TimeFrame.ANNUALLY], {"is_money":True}),
			("Annual earnings", self.earn_amount, [TimeFrame.ANNUALLY], {"is_money":True}),
			("Bi-annual earnings", self.earn_amount, [TimeFrame.BI_ANNUALLY], {"is_money":True}),
			("5 year earnings", self.earn_amount, [TimeFrame.N5YEARS], {"is_money":True}),
			("Decade earnings", self.earn_amount, [TimeFrame.DECADE], {"is_money":True}),
			("Quarterly taxes", self.tax_amount, [TimeFrame.QUARTERLY], {"is_money":True}),
			("Quarterly work taxes", self.tax_amount, [TimeFrame.WORK_QUARTERLY], {"is_money":True}),
			("Quarterly earnings", self.earn_amount, [TimeFrame.QUARTERLY], {"is_money":True}),
			("Quarterly work earnings", self.earn_amount, [TimeFrame.WORK_QUARTERLY], {"is_money":True}),
			("Net decade earnings", self.net_earn_amount, [TimeFrame.DECADE], {"is_money":True}),
			("Net 5 year earnings", self.net_earn_amount, [TimeFrame.N5YEARS], {"is_money":True}),
			("Net bi-annual earnings", self.net_earn_amount, [TimeFrame.BI_ANNUALLY], {"is_money":True}),
			("Net annual earnings", self.net_earn_amount, [TimeFrame.ANNUALLY], {"is_money":True}),
			("Net quarterly earnings", self.net_earn_amount, [TimeFrame.QUARTERLY], {"is_money":True})
		]
		monthly_to_view = [
			("Monthly taxes", self.tax_amount, [TimeFrame.MONTHLY], {"is_money":True}),
			("Monthly work taxes", self.tax_amount, [TimeFrame.WORK_MONTHLY], {"is_money":True}),
			("Monthly earnings", self.earn_amount, [TimeFrame.MONTHLY], {"is_money":True}),
			("Monthly work earnings", self.earn_amount, [TimeFrame.WORK_MONTHLY], {"is_money":True}),
			("Net monthly earnings", self.net_earn_amount, [TimeFrame.MONTHLY], {"is_money":True}),
			("Net monthly work earnings", self.net_earn_amount, [TimeFrame.WORK_MONTHLY], {"is_money":True})
		]
		weekly_to_view = [
			("Weekly taxes", self.tax_amount, [TimeFrame.WEEKLY], {"is_money":True}),
			("Weekly work taxes", self.tax_amount, [TimeFrame.WORK_WEEKLY], {"is_money":True}),
			("Weekly earnings", self.earn_amount, [TimeFrame.WEEKLY], {"is_money":True}),
			("Weekly work earnings", self.earn_amount, [TimeFrame.WORK_WEEKLY], {"is_money":True}),
			("Net weekly earnings", self.net_earn_amount, [TimeFrame.WEEKLY], {"is_money":True}),
			("Net weekly work earnings", self.net_earn_amount, [TimeFrame.WORK_WEEKLY], {"is_money":True})
		]
		daily_to_view = [
			("Daily taxes", self.tax_amount, [TimeFrame.DAILY], {"is_money":True}),
			("Daily work taxes", self.tax_amount, [TimeFrame.WORK_DAILY], {"is_money":True}),
			("Dollars per day", self.earn_amount, [TimeFrame.DAILY], {"is_money":True}),
			("Dollars per work day", self.earn_amount, [TimeFrame.WORK_DAILY], {"is_money":True}),
			("Net daily earnings", self.net_earn_amount, [TimeFrame.DAILY], {"is_money":True}),
			("Net daily work earnings", self.net_earn_amount, [TimeFrame.WORK_DAILY], {"is_money":True})
		]
		hourly_to_view = [
			("Hourly taxes", self.tax_amount, [TimeFrame.HOURLY], {"is_money":True}),
			("Hourly work taxes", self.tax_amount, [TimeFrame.WORK_HOURLY], {"is_money":True}),
			("Hourly earnings", self.earn_amount, [TimeFrame.HOURLY], {"is_money":True}),
			("Hourly work earnings", self.earn_amount, [TimeFrame.WORK_HOURLY], {"is_money":True}),
			("Net hourly earnings", self.net_earn_amount, [TimeFrame.HOURLY], {"is_money":True}),
			("Net hourly work earnings", self.net_earn_amount, [TimeFrame.WORK_HOURLY], {"is_money":True})
		]
		minute_to_view = [
			("Taxes per minute", self.tax_amount, [TimeFrame.MINUTE], {"is_money":True}),
			("Taxes per work minute", self.tax_amount, [TimeFrame.WORK_MINUTE], {"is_money":True}),
			("Earnings per minute", self.earn_amount, [TimeFrame.MINUTE], {"is_money":True}),
			("Earnings per work minute", self.earn_amount, [TimeFrame.WORK_MINUTE], {"is_money":True}),
			("Net earnings per minute", self.net_earn_amount, [TimeFrame.MINUTE], {"is_money":True}),
			("Net earnings per work minute", self.net_earn_amount, [TimeFrame.WORK_MINUTE], {"is_money":True})
		]
		second_to_view = [
			("Taxes per seoond", self.tax_amount, [TimeFrame.SECOND], {"is_money":True}),
			("Taxes per work seoond", self.tax_amount, [TimeFrame.WORK_SECOND], {"is_money":True}),
			("Earnings per seoond", self.earn_amount, [TimeFrame.SECOND], {"is_money":True}),
			("Earnings per work seoond", self.earn_amount, [TimeFrame.WORK_SECOND], {"is_money":True}),
			("Net earnings per seoond", self.net_earn_amount, [TimeFrame.SECOND], {"is_money":True}),
			("Net earnings per work seoond", self.net_earn_amount, [TimeFrame.WORK_SECOND], {"is_money":True})
		]
		
		to_view = [
			("generic reporting", generic_to_view),
			("monthly reporting", monthly_to_view),
			("weekly reporting", weekly_to_view),
			("daily reporting", daily_to_view),
			("hourly reporting", hourly_to_view),
			("minute reporting", minute_to_view),
			("second reporting", second_to_view)
		]
		
		for description, category in to_view:
			message += "\n\t{d}\n".format(d=description)
			for m, func, fargs, args in category:
				message += self.create_line(m, func(*fargs), l, **args) + "\n"
				
		return message
		
	def tax_amount(self, time_frame):
		ta = self.base * (INCOME_TAX_RATE / 100)
		
		ypd = (1 / DAYS_PER_YEAR)
		dph = (1 / HOURS_PER_DAY)
		hpm = (1 / MINUTES_PER_HOUR)
		mps = (1 / SECONDS_PER_MINUTE)
		
		wypd = (1 / WORK_DAYS)
		wdph = (1 / WORK_HOURS_PER_DAY)
		whpm = (1 / MINUTES_PER_HOUR)
		wmps = (1 / SECONDS_PER_MINUTE)
		#WORK_QUARTERLY WORK_ANNUALLY WORK_BI_ANNUALLY WORK_5YEARS WORK_DECADE
		options = {
			0: lambda x : x * ypd * dph * hpm * mps, #SECOND
			1: lambda x : x * ypd * dph * hpm, #MINUTE
			2: lambda x : x * ypd * dph, #HOURLY
			3: lambda x : x * ypd, #DAILY
			4: lambda x : x * 1/ WEEKS_PER_YEAR, #WEEKLY
			5: lambda x : x * ypd * DAYS_PER_YEAR / MONTHS_PER_YEAR, #MONTHLY
			6: lambda x : x * ypd * DAYS_PER_YEAR / MONTHS_PER_YEAR * MONTHS_PER_QUARTER, #QUARTERLY
			7: lambda x : x * wypd * wdph * whpm * wmps, #WORK_SECOND
			8: lambda x : x * 1 / (WORK_DAYS * (WORK_HOURS_PER_DAY / 100) * MINUTES_PER_HOUR), #WORK_MINUTE
			9: lambda x : x * 1 / (WORK_DAYS * (WORK_HOURS_PER_DAY / 100)), #WORK_HOURLY
			10: lambda x : x * wypd, #WORK_DAILY
			11: lambda x : x * 1 / round(1 / (wypd * WORK_DAYS_PER_WEEK)), #WORK_WEEKLY
			12: lambda x : x * wypd * WORK_DAYS / MONTHS_PER_YEAR, #WORK_MONTHLY
			13: lambda x : x * wypd * WORK_DAYS / MONTHS_PER_YEAR * MONTHS_PER_QUARTER, #WORK_QUARTERLY
			14: lambda x : x, #ANNUALLY
			15: lambda x : x * YEARS_PER_BI_ANNUAL, #BI_ANNUALLY
			16: lambda x : x * 5, #5YEARS
			17: lambda x : x * YEARS_PER_DECADE #DECADE
		}
		
		return options[time_frame.value - 1](ta)
		
	
		
	def earn_amount(self, time_frame):
		ta = self.base
		
		ypd = (1 / DAYS_PER_YEAR)
		dph = (1 / HOURS_PER_DAY)
		hpm = (1 / MINUTES_PER_HOUR)
		mps = (1 / SECONDS_PER_MINUTE)
		
		wypd = (1 / WORK_DAYS)
		wdph = (1 / WORK_HOURS_PER_DAY)
		whpm = (1 / MINUTES_PER_HOUR)
		wmps = (1 / SECONDS_PER_MINUTE)
		#WORK_QUARTERLY WORK_ANNUALLY WORK_BI_ANNUALLY WORK_5YEARS WORK_DECADE
		options = {
			0: lambda x : x * ypd * dph * hpm * mps, #SECOND
			1: lambda x : x * ypd * dph * hpm, #MINUTE
			2: lambda x : x * ypd * dph, #HOURLY
			3: lambda x : x * ypd, #DAILY
			4: lambda x : x * 1/ WEEKS_PER_YEAR, #WEEKLY
			5: lambda x : x * ypd * DAYS_PER_YEAR / MONTHS_PER_YEAR, #MONTHLY
			6: lambda x : x * ypd * DAYS_PER_YEAR / MONTHS_PER_YEAR * MONTHS_PER_QUARTER, #QUARTERLY
			7: lambda x : x * wypd * wdph * whpm * wmps, #WORK_SECOND
			8: lambda x : x * 1 / (WORK_DAYS * (WORK_HOURS_PER_DAY / 100) * MINUTES_PER_HOUR), #WORK_MINUTE
			9: lambda x : x * 1 / (WORK_DAYS * (WORK_HOURS_PER_DAY / 100)), #WORK_HOURLY
			10: lambda x : x * wypd, #WORK_DAILY
			11: lambda x : x * 1 / round(1 / (wypd * WORK_DAYS_PER_WEEK)), #WORK_WEEKLY
			12: lambda x : x * wypd * WORK_DAYS / MONTHS_PER_YEAR, #WORK_MONTHLY
			13: lambda x : x * wypd * WORK_DAYS / MONTHS_PER_YEAR * MONTHS_PER_QUARTER, #WORK_QUARTERLY
			14: lambda x : x, #ANNUALLY
			15: lambda x : x * YEARS_PER_BI_ANNUAL, #BI_ANNUALLY
			16: lambda x : x * 5, #5YEARS
			17: lambda x : x * YEARS_PER_DECADE #DECADE
		}
		
		return options[time_frame.value - 1](ta)
		
	def net_earn_amount(self, time_frame):
		ta = self.base
		
		ypd = (1 / DAYS_PER_YEAR)
		dph = (1 / HOURS_PER_DAY)
		hpm = (1 / MINUTES_PER_HOUR)
		mps = (1 / SECONDS_PER_MINUTE)
		
		wypd = (1 / WORK_DAYS)
		wdph = (1 / WORK_HOURS_PER_DAY)
		whpm = (1 / MINUTES_PER_HOUR)
		wmps = (1 / SECONDS_PER_MINUTE)
		#WORK_QUARTERLY WORK_ANNUALLY WORK_BI_ANNUALLY WORK_5YEARS WORK_DECADE
		options = {
			0: lambda x : x * ypd * dph * hpm * mps, #SECOND
			1: lambda x : x * ypd * dph * hpm, #MINUTE
			2: lambda x : x * ypd * dph, #HOURLY
			3: lambda x : x * ypd, #DAILY
			4: lambda x : x * 1/ WEEKS_PER_YEAR, #WEEKLY
			5: lambda x : x * ypd * DAYS_PER_YEAR / MONTHS_PER_YEAR, #MONTHLY
			6: lambda x : x * ypd * DAYS_PER_YEAR / MONTHS_PER_YEAR * MONTHS_PER_QUARTER, #QUARTERLY
			7: lambda x : x * wypd * wdph * whpm * wmps, #WORK_SECOND
			8: lambda x : x * 1 / (WORK_DAYS * (WORK_HOURS_PER_DAY / 100) * MINUTES_PER_HOUR), #WORK_MINUTE
			9: lambda x : x * 1 / (WORK_DAYS * (WORK_HOURS_PER_DAY / 100)), #WORK_HOURLY
			10: lambda x : x * wypd, #WORK_DAILY
			11: lambda x : x * 1 / round(1 / (wypd * WORK_DAYS_PER_WEEK)), #WORK_WEEKLY
			12: lambda x : x * wypd * WORK_DAYS / MONTHS_PER_YEAR, #WORK_MONTHLY
			13: lambda x : x * wypd * WORK_DAYS / MONTHS_PER_YEAR * MONTHS_PER_QUARTER, #WORK_QUARTERLY
			14: lambda x : x, #ANNUALLY
			15: lambda x : x * YEARS_PER_BI_ANNUAL, #BI_ANNUALLY
			16: lambda x : x * 5, #5YEARS
			17: lambda x : x * YEARS_PER_DECADE #DECADE
		}
		
		return options[time_frame.value - 1](ta) - self.tax_amount(time_frame)
		
	def annual_tax_rate(self):
		return INCOME_TAX_RATE
		
def work_day_hours(start, end, lunch):
	return end - start - lunch
	
def twenty_four_toString(t):
	h, mh = divmod(t, 100)
	m = 60 * mh / 100
	return ("{h} hour" + ("s" if h > 1 else "") + " {m} minute" + ("s" if m > 1 else "")).format(h=h, m=m)
	
# convert a salary in a given TimeFrame to the value proportional to the change in TimeFrame.
# i.e. $50/H -> $438000/Y
def convert_to_annual(val, time_frame):
	print("CONVERTING: " + str(time_frame) + " -> ANNUALLY")
	options = {
		0: lambda x : x * SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY * DAYS_PER_YEAR, #SECOND
		1: lambda x : x * MINUTES_PER_HOUR * HOURS_PER_DAY * DAYS_PER_YEAR, #MINUTE
		2: lambda x : x * HOURS_PER_DAY * DAYS_PER_YEAR, #HOURLY
		3: lambda x : x * DAYS_PER_YEAR, #DAILY
		4: lambda x : x * WEEKS_PER_YEAR, #WEEKLY
		5: lambda x : x * MONTHS_PER_YEAR, #MONTHLY
		6: lambda x : x * MONTHS_PER_YEAR / MONTHS_PER_QUARTER, #QUARTERLY
		7: lambda x : x * WORK_SECONDS_PER_WORK_MINUTE * WORK_MINUTES_PER_HOUR * WORK_HOURS_PER_DAY * WORK_DAYS, #WORK_SECOND
		8: lambda x : x * WORK_MINUTES_PER_HOUR * WORK_HOURS_PER_DAY * WORK_DAYS, #WORK_MINUTE
		9: lambda x : x * WORK_HOURS_PER_DAY * WORK_DAYS_PER_WEEK * WORK_DAYS, #WORK_HOURLY
		10: lambda x : x * WORK_DAYS, #WORK_DAILY
		11: lambda x : x * WORK_DAYS / WORK_DAYS_PER_WEEK , #WORK_WEEKLY
		12: lambda x : x * MONTHS_PER_YEAR, #WORK_MONTHLY
		13: lambda x : x * MONTHS_PER_YEAR / MONTHS_PER_QUARTER, #WORK_QUARTERLY
		14: lambda x : x, #ANNUALLY
		15: lambda x : x / YEARS_PER_BI_ANNUAL, #BI_ANNUALLY
		16: lambda x : x / 5, #5YEARS
		17: lambda x : x / YEARS_PER_DECADE #DECADE
	}
	return options[time_frame.value - 1](val)
    
def get_numerical_input(prompt):
	inp = input(prompt + "\n")
	try:
		inp = float(inp)
	except ValueError:
		try:
			if "$" in inp:
				inp = inp[inp.index("$"):]
				inp = float(inp)
			else:
				inp = 0
		except ValueError: 
			inp = 0
	return inp
	
def get_timeframe_input(prompt):
	m = ""
	for tf in TimeFrame:
		x = len(str(tf.value))
		m += "\t" + str(tf.value).ljust(10, ".") + tf.name + "\n"
	print(m)
	inp = input(prompt + "\n")
	try:
		inp = int(inp)
		if not (0 < inp <= len(TimeFrame)):
			raise ValueError
	except ValueError:
		inp = TimeFrame.ANNUALLY.value # annual
	return inp
	
# True for yes False for no
def get_yes_no(prompt):
	valid = ["y","yes","n","no"]
	prompt += "\n\tEnter:\n\tY for yes\n\tN for no\n"
	inp = 0
	while inp not in valid:
		inp = input(prompt + "\n").lower()
	i = valid.index(inp)
	return i < 2
		
def run():
	loop = True
	while loop:
		money_input = get_numerical_input("Enter a monetary amount:")
		date_input = get_timeframe_input("Enter a value corresponding to a timeframe:")
		cap_input = False
		if date_input != TimeFrame.ANNUALLY.value:
			money_input = convert_to_annual(money_input, list(TimeFrame)[date_input - 1])
			# s = Salary(money_input)
		# print("s: " + str(money_input) + ", TF: " + str(date_input))
		salary = Salary(money_input)
		print(salary)
		cap_input = get_yes_no("Would you like to enter a cap for the amount of time worked?")
		if cap_input:
			cap_input = [get_numerical_input("Enter the number of time segments:\n(ex: '5' - for 5 minutes/days/weeks...etc)"), None]
			cap_input[1] = get_timeframe_input("Enter a timeframe corresponding to the number of time segments previously entered:")
			
		
		loop = get_yes_no("Run again?")
		
# Constants
MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60
WEEKS_PER_MONTH = 4
MONTHS_PER_YEAR = 12
MONTHS_PER_QUARTER = 3
DAYS_PER_WEEK = 7
HOURS_PER_DAY = 24
DAYS_PER_YEAR = 365
WEEKS_PER_YEAR = 52
YEARS_PER_BI_ANNUAL = 2
YEARS_PER_DECADE = 10

# Changeable vars
VACATION_DAYS = 14
WORK_DAYS_PER_WEEK = 5
WORK_DAY_START_TIME = 800
WORK_DAY_END_TIME = 1600
WORK_lUNCH_TIME = 50
INCOME_TAX_RATE = 15



WORK_HOURS_PER_DAY = work_day_hours(WORK_DAY_START_TIME, WORK_DAY_END_TIME, WORK_lUNCH_TIME)
WORK_DAYS = math.ceil(DAYS_PER_YEAR - VACATION_DAYS - ((DAYS_PER_WEEK - WORK_DAYS_PER_WEEK) * ((DAYS_PER_YEAR - VACATION_DAYS) / DAYS_PER_WEEK)))

if __name__ == "__main__":
	print("work hours per day: {0}".format(twenty_four_toString(WORK_HOURS_PER_DAY)))
	print("work days per year: {0}".format(WORK_DAYS))
	salary = Salary(40000)
	print(salary)
	run()
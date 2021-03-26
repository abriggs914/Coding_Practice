import datetime
import calendar

orders = {
	2016: [
		("2016-10-11", 8.95)
	],
	2017: [
		("2017-12-23", 86.72),
		("2017-12-06", 21.94),
		("2017-12-06", 148.40),
		("2017-12-06", 14.99),
		("2017-10-04", 91.99),
		("2017-09-24", 44.76),
		("2017-09-15", 22.99),
		("2017-09-15", 36.70)
	],
	2018: [
		("2018-12-08", 114.97),
		("2018-12-08", 5.79),
		("2018-12-08", 20.98),
		("2018-12-02", 31.03),
		("2018-12-02", 34.97),
		("2018-10-27", 25.99),
		("2018-10-27", 37.59),
		("2018-09-09", 39.54),
		("2018-09-08", 10),
		("2018-08-09", 35.35),
		("2018-06-26", 34.94),
		("2018-06-08", 12.99),
		("2018-06-02", 15.99),
		("2018-03-26", 38.59)
	],
	2019: [
		("2019-12-13", 24),
		("2019-11-29", 459.94),
		("2019-11-29", 102.67),
		("2019-11-18", 15.9),
		("2019-11-18", 15.99),
		("2019-03-09", 55.78),
		("2019-03-09", 19.96),
		("2019-01-31", 7.99),
		("2019-01-11", 25.54),
		("2019-01-08", 25.12)
	],
	2020: [
		("2020-12-21", 32.99),
		("2020-12-07", 35.14),
		("2020-12-07", 18.99),
		("2020-11-30", 12),
		("2020-11-30", 28.48),
		("2020-11-30", 15.18),
		("2020-11-30", 92.65),
		("2020-11-30", 15.38),
		("2020-11-27", 1053.14),
		("2020-11-27", 37.98),
		("2020-11-21", 21.6),
		("2020-11-21", 50.05),
		("2020-11-21", 32.5),
		("2020-11-21", 148.34),
		("2020-08-31", 32.55),
		("2020-06-18", 29.99),
		("2020-06-12", 21.24),
	],
	2021: [
		("2021-03-24", 28.97),
		("2021-03-24", 384.9),
		("2021-03-22", 59.99),
		("2021-03-19", 141.42),
		("2021-03-15", 26.99),
		("2021-02-26", 11.44),
		("2021-01-04", 16.84),
		("2021-01-04", 38.88),
	]
}

class YearHistory:

	def __init__(self, year):
		self.year = year
		self.balance = 0
		self.history = []
		self.months = dict(zip(calendar.month_name, [[] for i in range(len(calendar.month_name))]))
		
	def add(self, order):
		d, p = order
		m = datetime.date(*list(map(int, d.split("-")))).month
		self.balance += p
		self.history.append(order)
		self.months[calendar.month_name[m]].append(order)

	def get_monthly_spending(self, month):
		return sum(list(map(lambda x : x[1], self.months[calendar.month_name[month]])))

	def __repr__(self):
		return str(self.year)
		
history = {}
total_spent = 0
largest_order = None
smallest_order = None
highest_spending_month = None
least_spending_month = None
highest_spending_year = None
least_spending_year = None
average_order_price = 0
for year in orders:
	history[year] = YearHistory(year)
	for order in orders[year]:		
		history[year].add(order)

		d, p = order
		if largest_order == None or largest_order[1] < p:
			largest_order = order
		if smallest_order == None or smallest_order[1] > p:
			smallest_order = order

		m = datetime.date(*list(map(int, d.split("-")))).month
		if highest_spending_month == None or history[year].get_monthly_spending(m) > highest_spending_month[0].get_monthly_spending(highest_spending_month[1]):
			highest_spending_month = (history[year], m)
		if least_spending_month == None or history[year].get_monthly_spending(m) < least_spending_month[0].get_monthly_spending(least_spending_month[1]):
			least_spending_month = (history[year], m)

		if highest_spending_year == None or history[year].balance > highest_spending_year.balance:
			highest_spending_year = history[year]
		if least_spending_year == None or history[year].balance < least_spending_year.balance:
			least_spending_year = history[year]
		
if history:
	for hist, dat in history.items():
		print("hist: " + str(hist))
		b = dat.balance
		print("\tbalance: $ %.2f" % b)
		total_spent += b
	print("\n\nTotal spent: $ %.2f" % total_spent)
	print("Largest order:", largest_order)
	print("Smallest order:", smallest_order)
	print("Highest spending month:", highest_spending_month, "Spent:", highest_spending_month[0].get_monthly_spending(highest_spending_month[1]), "Orders:", highest_spending_month[0].months[calendar.month_name[highest_spending_month[1]]])
	print("least spending month:", least_spending_month, "Spent:", least_spending_month[0].get_monthly_spending(least_spending_month[1]), "Orders:", least_spending_month[0].months[calendar.month_name[least_spending_month[1]]])
	print("Highest spending year:", highest_spending_year, "Spent:", highest_spending_year.balance)
	print("least spending year:", least_spending_year, "Spent:", least_spending_year.balance)
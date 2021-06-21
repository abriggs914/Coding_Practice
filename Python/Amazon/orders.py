import datetime
import calendar
from utility import *

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
		("2021-06-01", 62.80),
		("2021-06-01", 34.50),
		("2021-06-01", 335.44),
		("2021-06-01", 100.12),
		("2021-03-24", 28.97),
		("2021-03-24", 384.9),
		("2021-03-22", 59.99),
		("2021-03-19", 141.42),
		("2021-03-15", 26.99),
		("2021-02-26", 11.44),
		("2021-01-04", 16.84),
		("2021-01-04", 38.88),
		("2021-06-18", 21.53),
		("2021-06-18", 52.89),
		("2021-06-18", 22.99),
		("2021-06-21", 39.99),
		("2021-06-21", 92.44)
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
	print("Highest spending month:", highest_spending_month, "Spent:", money(highest_spending_month[0].get_monthly_spending(highest_spending_month[1])), "Orders:", highest_spending_month[0].months[calendar.month_name[highest_spending_month[1]]])
	print("least spending month:", least_spending_month, "Spent:", money(least_spending_month[0].get_monthly_spending(least_spending_month[1])), "Orders:", least_spending_month[0].months[calendar.month_name[least_spending_month[1]]])
	print("Highest spending year:", highest_spending_year, "Spent:", money(highest_spending_year.balance))
	print("least spending year:", least_spending_year, "Spent:", money(least_spending_year.balance))
	
def amazon_recent():
	orders = {
		"2021-03-15": [
			(1, 6, 6, "NP", 26.99)
		],
		"2021-03-19": [
			(1, 8, 16, "S", 21.75),
			(1, 3, 3, "B", 22.03),
			(1, 6, 6, "P", 28.03),
			(1, 1, 1, "TS", 26.53),
			(1, 1, 1, "SH", 18.03),
			(1, 1, 1, "SH", 25.03)
		],
		"2021-03-22": [
			(1, 6, 42, "NP", 59.99)
		],
		"2021-03-24": [
			(1, 1, 2, "PY", 56.75),
			(1, 5, 10, "S", 20.22),
			(1, 8, 16, "S", 21.82),
			(1, 8, 16, "S", 21.90),
			(1, 1, 1, "B", 18.75),
			(1, 1, 1, "SH", 22.26),
			(1, 5, 5, "P", 29.75),
			(1, 3, 3, "B", 30.75),
			(1, 10, 10, "P", 35.75),
			(1, 1, 1, "B", 18.75),
			(1, 1, 1, "SH", 27.75),
			(1, 3, 3, "P", 20.74),
			(1, 1, 3, "PY", 29.90),
			(1, 5, 10, "S", 29.75),
			(1, 4, 4, "P", 28.97)
		],
		"2021-06-01": [
			(1, 2, 2, "D", 62.80),
			(1, 3, 3, "B", 36.99),
			(1, 1, 1, "B", 12.99),
			(1, 12, 24, "S", 19.99),
			(1, 6, 12, "S", 18.67),
			(1, 12, 12, "P", 29.69),
			(1, 12, 24, "S", 24.99),
			(1, 2, 2, "SH", 37.45),
			(1, 3, 3, "SH", 24.62),
		],
		"2021-06-18": [
			(1, 1, 2, "SE", 52.89),
			(1, 2, 2, "NP", 21.53),
			(1, 4, 4, "NP", 22.99),
			(1, 1, 6, "MU", 13.88),
			(1, 4, 4, "NP", 19.99)
		]
	}

	print("\n\n")
	total_cost = sum(sum([vals[-1] for vals in lst]) for lst in orders.values())
	quantites = {}
	for date, items in orders.items():
		for item in items:
			times, qty, pieces, typ, price = item
			if typ in quantites:
				quantites[typ]["Qty"] += qty
				quantites[typ]["Price"] += price
				quantites[typ]["Pieces"] += pieces
			else:
				quantites[typ] = {
					"Qty": qty,
					"Price": price,
					"Pieces": pieces
				}
				
	for item in quantites:
		quantites[item]["Cost / Item"] = money(quantites[item]["Price"] / max(1, quantites[item]["Qty"]))
		quantites[item]["Cost / Item"] = money(quantites[item]["Price"] / max(1, quantites[item]["Qty"]))
		quantites[item]["Cost / Piece"] = money(quantites[item]["Price"] / max(1, quantites[item]["Pieces"]))
		quantites[item]["Price"] = money(quantites[item]["Price"])
	
	
	print("total cost: $ ", total_cost)
	print(dict_print(quantites, "Qunatities"))
	
amazon_recent()

transactions = [
	(datetime.datetime(2021, 6, 1, 0, 0), -189.0),
	(datetime.datetime(2021, 6, 1, 0, 0), -123.45),
	(datetime.datetime(2021, 6, 1, 0, 0), -22.99),
	(datetime.datetime(2021, 6, 1, 0, 0), -37.45),
	(datetime.datetime(2021, 6, 1, 0, 0), -62.8),
	(datetime.datetime(2021, 6, 1, 0, 0), -34.5),
	(datetime.datetime(2021, 6, 2, 0, 0), -24.99),
	(datetime.datetime(2021, 6, 5, 0, 0), -24.99),
	(datetime.datetime(2021, 6, 5, 0, 0), 24.99),
	(datetime.datetime(2021, 6, 5, 0, 0), -15.99),
	(datetime.datetime(2021, 6, 5, 0, 0), 189.0),
	(datetime.datetime(2021, 6, 5, 0, 0), -69.52),
	(datetime.datetime(2021, 6, 7, 0, 0), -90.85),
	(datetime.datetime(2021, 6, 7, 0, 0), -36.99),
	(datetime.datetime(2021, 6, 7, 0, 0), -103.49),
	(datetime.datetime(2021, 6, 9, 0, 0), 69.52),
	(datetime.datetime(2021, 6, 9, 0, 0), -32.53)
]
sps = sum([t for d, t in transactions])
print("sps:", sps)
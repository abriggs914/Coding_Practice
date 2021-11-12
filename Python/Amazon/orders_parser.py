import csv
from utility import *


class Entry:
	def __init__(self, date, amount, tax, o_type, qty):
		self.date = date
		self.amount = float(amount)
		self.tax = float(tax)
		self.o_type = o_type
		self.qty = int(qty)
	
	def __repr__(self):
		return "d: {}, a: {}, t: {}, o: {}, q: {}".format(self.date, self.amount, self.tax, self.o_type, self.qty)
		

with open("orders.csv", "r") as f:
	dicts = csv.DictReader(f)
	
	entries = []
	for d in dicts:
		entries.append(Entry(*list(d.values())))
	
	total_spent = 0
	for e in entries:
		print(e)
		total_spent += e.amount
		
	print("Total spent: {}".format(money(total_spent)))
		
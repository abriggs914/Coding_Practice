import datetime
from utility import *

#pname	-	plural name "annual spending / weekly spending"

REOCCURRING = {
	"Once": {
				"pname": "Once",
				"ratio_to_annual": 1,
				"ratio_from_annual": 1,
				"occur_annual": 1,
				"occur_lifetime": 1
			},
	"Per second": {
				"pname": "Per second",
				"ratio_to_annual": 31536000,
				"ratio_from_annual": 1/31536000,
				"occur_annual": 31536000,
				"occur_lifetime": float("inf"),
			},
	"Per minute": {
				"pname": "Per minute",
				"ratio_to_annual": 525600,
				"ratio_from_annual": 1/525600,
				"occur_annual": 525600,
				"occur_lifetime": float("inf"),
			},
	"Hourly": {
				"pname": "Hourly",
				"ratio_to_annual": 8760,
				"ratio_from_annual": 1/8760,
				"occur_annual": 8760,
				"occur_lifetime": float("inf"),
			},
	"Daily": {
				"pname": "Daily",
				"ratio_to_annual": 365,
				"ratio_from_annual": 1/365,
				"occur_annual": 365,
				"occur_lifetime": float("inf"),
			},
	"Weekly": {
				"pname": "Weekly",
				"ratio_to_annual": 52,
				"ratio_from_annual": 1/52,
				"occur_annual": 52,
				"occur_lifetime": float("inf")
			},
	"Monthly": {
				"pname": "Monthly",
				"ratio_to_annual": 12,
				"ratio_from_annual": 1/12,
				"occur_annual": 12,
				"occur_lifetime": float("inf")
			},
	"Quarterly": {
				"pname": "Quarterly",
				"ratio_to_annual": 4,
				"ratio_from_annual": 1/4,
				"occur_annual": 4,
				"occur_lifetime": float("inf")
			},
	"Annually": {
				"pname": "Annual",
				"ratio_to_annual": 1,
				"ratio_from_annual": 1,
				"occur_annual": 1,
				"occur_lifetime": float("inf")
			}
}

TRANSACTION = {
	"Gas": 0,
	"Rent": 1,
	"Pay":2,
	"Entertainment": 3,
	"Learning": 4
}



class Entity:
	def __init__(self, name, balance=0):
		self.name = name
		self.balance = balance
		
	def __repr__(self):
		b = self.balance
		return self.name + " < $ " + ("%.2f" % b) + " >"
	

class Transaction:
	def __init__(self, amount, entity_from, entity_to, reoccurring_category, transaction_catgory, description, date_in):
		self.amount = amount
		self.entity_to = entities[entity_to]
		self.entity_from = entities[entity_from]
		self.description = description
		self.reoccurring_category = reoccurring_category
		self.transaction_catgory = transaction_catgory
		self.dates = []
		self.dates.append(date_in)
		
		self.entity_from.balance -= self.amount
		self.entity_to.balance += self.amount
		
	def __repr__(self):
		res = ""
		for date in self.dates:
			res += "{d} | $ {a} from: {ef} to {et}".format(d=date, a=self.amount, ef=self.entity_from, et=self.entity_to)
		return res
		
	def info_dict(self):
		d = {
			"Date": self.dates[0],
			"Amount": money(self.amount),
			"To": self.entity_to.name,
			"From": self.entity_from.name,
			"Reoccurring": self.reoccurring_category,
			"Category": self.transaction_catgory,
			"Description": self.description
		}
		# if 
		return d
		
		
def costing(transaction, period):
	toa = REOCCURRING[transaction.reoccurring_category]["occur_annual"]
	tra = REOCCURRING[transaction.reoccurring_category]["ratio_to_annual"]
	pra = REOCCURRING[period]["ratio_from_annual"]
	a = transaction.amount
	print("a: {a}, toa: {toa}, tra: {tra}, pra: {pra}".format(a=a, toa=toa, tra=tra, pra=pra))
	return a * toa * pra
	
def costing_report(entity, period, transaction=None, n=1):
	entity = entities[entity]
	res = "{p} costing report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity, n=n)
	if transaction != None:
		if entity not in [transaction.entity_to, transaction.entity_from]:
			return "Transaction <{t}>\ndoes not effect {e}".format(t=transaction, e=entity)
		x = min(REOCCURRING[transaction.reoccurring_category]["occur_lifetime"], n)
		cost = costing(transaction, period) * x
		if transaction.entity_from == entity:
			cost *= -1
		res += "$ %.2f" % cost
		return res
		
	total_cost = 0
	for transaction in transactions:
		if transaction.reoccurring_category != "Once":
			if entity in [transaction.entity_to, transaction.entity_from]:
				cost = costing(transaction, period) * n
				if transaction.entity_from == entity:
					cost *= -1
				total_cost += cost
	res += "total cost {tc}".format(tc=total_cost)
	return res
	
def earning_report(entity, period, transaction=None, n=1):
	entity = entities[entity]
	res = "{p} earning report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity, n=n)
	if transaction != None:
		if entity != transaction.entity_to:
			return "Transaction <{t}>\ndoes not effect {e}".format(t=transaction, e=entity)
		x = min(REOCCURRING[transaction.reoccurring_categoy]["occur_lifetime"], n)
		cost = costing(transaction, period) * x
		res += "$ %.2f" % cost
		return res
		
	total_cost = 0
	for transaction in transactions:
		if transaction.reoccurring_category != "Once":
			if entity == transaction.entity_to:
				x = min(REOCCURRING[transaction.reoccurring_category]["occur_lifetime"], n)
				cost = costing(transaction, period) * x
				total_cost += cost
	res += "total earnings {tc}".format(tc=total_cost)
	return res
	
def spending_report(entity, period, transaction=None, n=1):
	entity = entities[entity]
	res = "{p} spending report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity, n=n)
	if transaction != None:
		if entity != transaction.entity_from:
			return "Transaction <{t}>\ndoes not effect {e}".format(t=transaction, e=entity)
		x = min(REOCCURRING[transaction.reoccurring_categoy]["occur_lifetime"], n)
		cost = costing(transaction, period) * x
		res += "$ %.2f" % cost
		return res
		
	total_cost = 0
	for transaction in transactions:
		if transaction.reoccurring_category != "Once":
			if entity == transaction.entity_from:
				x = min(REOCCURRING[transaction.reoccurring_category]["occur_lifetime"], n)
				cost = costing(transaction, period) * x
				total_cost += cost
	res += "total spendings {tc}".format(tc=total_cost)
	return res
			
	# TODO something here
		
entities = {
	"Avery": Entity("Avery"),
	"BWS": Entity("BWS"),
	"Colpitts": Entity("Colpitts"),
	"Irving": Entity("Irving"),
	"Disney+": Entity("Disney+"),
	"Nintendo": Entity("Nintendo"),
	"Codecademy": Entity("Codecademy"),
	"Spotify": Entity("Spotify"),
	"Xbox Live": Entity("Xbox Live"),
	"Amazon Prime": Entity("Amazon Prime"),
	"Walmart": Entity("Walmart"),
	"SF": Entity("SF"),
	"ScotiaBank": Entity("ScotiaBank"),
	"BMO": Entity("BMO"),
	"GST": Entity("GST"),
	"Phone Bill": Entity("Phone Bill"),
	"NSLSC": Entity("NSLSC"),
	"Other": Entity("Other")
}


transactions = [
	Transaction(602.3, "BWS", "Avery", "Weekly", "Pay", "Pay", datetime.datetime.now()),
	Transaction(65, "Avery", "Irving", "Weekly", "Gas", "Gas", datetime.datetime.now()),
	Transaction(477.5, "Avery", "Colpitts", "Monthly", "Rent", "Gas", datetime.datetime.now()),
	
	Transaction(89.99, "Avery", "Disney+", "Annually", "Entertainment", "Disney+ subscription", datetime.datetime.now()),
	Transaction(25, "Avery", "Nintendo", "Annually", "Entertainment", "Nintendo subscription", datetime.datetime.now()),
	Transaction(69.99, "Avery", "Xbox Live", "Annually", "Entertainment", "Xbox Live subscription", datetime.datetime.now()),
	Transaction(69.99, "Avery", "Amazon Prime", "Annually", "Entertainment", "Amazon Prime subscription", datetime.datetime.now()),
	Transaction(251.75, "Avery", "Codecademy", "Annually", "Learning", "Codecademy subscription", datetime.datetime.now()),
	Transaction(45, "Avery", "Spotify", "Annually", "Entertainment", "Spotify subscription", datetime.datetime.now()),
	Transaction(175.93, "Avery", "Walmart", "Once", "Entertainment", "New TV", datetime.datetime.now()),
	Transaction(98.9, "Avery", "Walmart", "Once", "Clothing", "Some new work clothes", datetime.datetime.now()),
	Transaction(17.50, "Avery", "SF", "Monthly", "SF", "SF", datetime.datetime.now()),
	Transaction(15.95, "Avery", "ScotiaBank", "Monthly", "Bank fees", "Bank fees", datetime.datetime.now()),
	Transaction(10.50, "Avery", "BMO", "Monthly", "Bank fees", "Bank fees", datetime.datetime.now()),
	Transaction(25, "Avery", "BMO", "Monthly", "Bill", "Credit card", datetime.datetime.now()),
	Transaction(147.5, "GST", "Avery", "Quarterly", "GST", "GST pamyent", datetime.datetime.now()),
	Transaction(50, "Avery", "Phone Bill", "Monthly", "Bill", "Phone bill", datetime.datetime.now()),
	Transaction(634, "Avery", "NSLSC", "Monthly", "Bill", "Student Loan", datetime.datetime.now()),
	Transaction(100, "Avery", "Other", "Monthly", "Other", "Other", datetime.datetime.now())
]

ts = {}

for i, transaction in enumerate(transactions):
	print("\n" + str(transaction))
	# print("\t" + str(costing(transaction, "Annually")))
	print("\t" + str(costing(transaction, "Weekly")))
	print("\t" + str(costing_report("Avery", "Weekly", transaction)))
	ts[i+1] = transaction.info_dict()
	# print("\t" + str(costing(transaction, "Monthly")))
	
print("\n" + costing_report("BWS", "Annually", transactions[1]))
print("\n" + costing_report("Avery", "Annually"))

res = {}
for occurance in REOCCURRING:
	cr = costing_report("Avery", occurance)
	er = earning_report("Avery", occurance)
	sr = spending_report("Avery", occurance)
	print("\n" + cr)
	print("\n" + er)
	print("\n" + sr)
	res[occurance] = {
		"Costing": money(float(cr.split()[-1])),
		"Earning": money(float(er.split()[-1])),
		"Spending": money(float(sr.split()[-1]))
	}

print(dict_print(REOCCURRING, min_encapsulation=True))

print(dict_print(res, "Reports"))
print(dict_print(ts, "Transactions"))
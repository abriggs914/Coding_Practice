import datetime
from transactions_parser import *
from TransactionHandler import *
from utility import *
from Entity import Entity
from Transaction import Transaction


def test():
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

	TH = TransactionHandler()

	for t in transactions:
		TH.addTransaction(t)

	ts = {}

	for i, transaction in enumerate(transactions):
		print("\n" + str(transaction))
		# print("\t" + str(costing(transaction, "Annually")))
		print("\t" + str(TH.costing(transaction, "Weekly")))
		print("\t" + str(TH.costing_report("Avery", "Weekly", transaction)))
		ts[i+1] = transaction.info_dict()
		# print("\t" + str(costing(transaction, "Monthly")))

	print("\n" + TH.costing_report("BWS", "Annually", transactions[1]))
	print("\n" + TH.costing_report("Avery", "Annually"))

	res = {}
	for occurance in REOCCURRING:
		cr = TH.costing_report("Avery", occurance)
		er = TH.earning_report("Avery", occurance)
		sr = TH.spending_report("Avery", occurance)
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


if __name__ == "__main__":

	transactions_dict = populate_transactions_dict()
	TH = TransactionHandler()
	me = TH.get_entity("Me")
	print("transactions_dict {td}".format(td=transactions_dict))
	for num, transaction in transactions_dict.items():
		# amount, entity_from, entity_to, reoccurring_category, transaction_catgory, description, date_in
		# Transaction Date, Transaction Amount, Notes, Transaction Type, Entity
		amount = float(transaction["Transaction Amount"])
		entity = Entity(transaction["Entity"])
		transaction_type = transaction["Transaction Type"]
		date = transaction["Transaction Date"]
		transaction = {
			"amount": abs(amount),
			"entity_from": me if amount < 0 else entity,
			"entity_to": me if amount > 0 else entity,
			"reoccurring_category": REOCCURRING["Once"],
			"transaction_catgory": transaction_type,
			"description": entity,
			"date_in": date
		}
		print("transaction: {t}".format(t=list(transaction.values())))
		TH.create_transaction(*list(transaction.values()))

	print(TH.transaction_list)
	entities_dict = {}
	for entity in TH.entities_list:
		entities_dict[entity.name] = {"balance": money(entity.balance)}
	print(dict_print(entities_dict, "entities dict", number=True))

	a = "String one"
	b = "sTriNg TWo"
	print(computeMinEditDistance(a, b))

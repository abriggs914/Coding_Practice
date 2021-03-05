import datetime
from transactions_parser import *
from TransactionHandler import *
from utility import *
from Entity import Entity
from Transaction import Transaction
import re


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

		Transaction(89.99, "Avery", "Disney+", "Annually", "Entertainment", "Disney+ subscription",
					datetime.datetime.now()),
		Transaction(25, "Avery", "Nintendo", "Annually", "Entertainment", "Nintendo subscription",
					datetime.datetime.now()),
		Transaction(69.99, "Avery", "Xbox Live", "Annually", "Entertainment", "Xbox Live subscription",
					datetime.datetime.now()),
		Transaction(69.99, "Avery", "Amazon Prime", "Annually", "Entertainment", "Amazon Prime subscription",
					datetime.datetime.now()),
		Transaction(251.75, "Avery", "Codecademy", "Annually", "Learning", "Codecademy subscription",
					datetime.datetime.now()),
		Transaction(45, "Avery", "Spotify", "Annually", "Entertainment", "Spotify subscription",
					datetime.datetime.now()),
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
		ts[i + 1] = transaction.info_dict()
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

	# transactions_dict = populate_transactions_dict()
	# TH = TransactionHandler()
	# me = TH.get_entity("Me")
	# print("transactions_dict {td}".format(td=transactions_dict))
	# for num, transaction in transactions_dict.items():
	# 	# amount, entity_from, entity_to, reoccurring_category, transaction_catgory, description, date_in
	# 	# Transaction Date, Transaction Amount, Notes, Transaction Type, Entity
	# 	amount = float(transaction["Transaction Amount"])
	# 	entity = Entity(transaction["Entity"])
	# 	transaction_type = transaction["Transaction Type"]
	# 	date = transaction["Transaction Date"]
	# 	transaction = {
	# 		"amount": abs(amount),
	# 		"entity_from": me if amount < 0 else entity,
	# 		"entity_to": me if amount > 0 else entity,
	# 		"reoccurring_category": REOCCURRING["Once"],
	# 		"transaction_catgory": transaction_type,
	# 		"description": entity,
	# 		"date_in": date
	# 	}
	# 	print("transaction: {t}".format(t=list(transaction.values())))
	# 	TH.create_transaction(*list(transaction.values()))
	#
	# print(TH.transaction_list)
	# entities_dict = {}
	# for entity in TH.entities_list:
	# 	entities_dict[entity.name] = {"balance": money(entity.balance)}
	# print(dict_print(entities_dict, "entities dict", number=True))

	def unclutter(txt):
		m = "IN: <" + str(txt) + ">"
		ignore = ["FPOS", "OPOS", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "=", "+", "{", "}", "[", "]", "?", "/", "<", ">", ":", ";", "'", "`", "~", ",", "."] + [str(i) for i in range(10)]
		for val in ignore:
			txt = txt.replace(val, "")
		txt = txt.strip()
		m += "     OUT: <" + str(txt) + ">"
		# print(m)
		return txt


	def num_matching_words(txt_1, txt_2):
		spl_1 = txt_1.split()
		spl_2 = txt_2.split()
		spl_1.sort()
		spl_2.sort()
		i, j = 0, 0
		p, q = len(spl_1), len(spl_2)
		matching_words = [None for m in range(p*q)]
		edit_distances = [None for m in range(p*q)]
		word_lengths = [lenstr(word) for word in spl_1 + spl_2]
		avg_word_len = avg(word_lengths)

		print(dict_print({
			"txt_1": txt_1,
			"txt_2": txt_2,
			"spl_1": spl_1,
			"spl_2": spl_2,
			"p": p,
			"q": q,
		},
			"matching words"
		))

		while i < p:
			j = 0
			while j < q:
				word_1 = spl_1[i]
				word_2 = spl_2[j]
				m = compute_min_edit_distance(word_1, word_2)
				print("({i}, {j}) => (i*q)+j: {ij}".format(i=i, j=j, ij=(i*q)+j))
				edit_distances[(i*q)+j] = m
				matching_words[(i*q)+j] = word_1 if m == 0 else matching_words[(i*q)+j]
				j += 1
				# if m == 0:
				# 	break
			i += 1

		avg_word_len = avg(word_lengths)
		avg_edit_dist = avg(edit_distances)

		print("matching words: <{amw}>:\n{mw}\nedit distances: <{aed}>\n{ed}".format(mw=matching_words, ed=edit_distances, amw=avg_word_len, aed=avg_edit_dist))
		return matching_words


	# same len - could be a coincidence if the strings don't already match
	# matching word score - unreliable for few words
	# balance the edit distance (score-wise)
	# in the unmatched words, is the edit distance good?

	def same_entity(entity_1, entity_2, tol=2):
		entity_1 = unclutter(entity_1)
		entity_2 = unclutter(entity_2)
		if all([type(e) == Entity for e in [entity_1, entity_2]]):
			if entity_1 == entity_2:
				return True
		elif all([type(e) == str for e in [entity_1, entity_2]]):
			if entity_1.lower() == entity_2.lower():
				return True
			else:
				m = compute_min_edit_distance(entity_1, entity_2)
				# print("m: {m}".format(m=m))
				if m <= tol:
					return True
				mw = num_matching_words(entity_1, entity_2)
		return False


	a = "String one"
	b = "sTriNg Tne"
	print(same_entity(a, b))

	# All of the values in each list should be recognized as the same entity
	strings = {
		# "Amazon": [
		# 	"OPOS AMZN Mktp CA        WWW.A",
		# 	"OPOS Amazon.ca           AMAZO",
		# 	"OPOS Amazon.ca           Seatt",
		# 	"OPOS 0.26 Amazon.com     Amzn"
		# ],
		"Walmart": [
			"FPOS WALMART STORE #3032 FREDE",
			"WALMART STORE #3032      FREDE",
			"WAL-MART #1067           FREDE",
			"WAL-MART #3032           FREDE",
			"WAL-MART #3054           MISSI"

		],
		# "Spotify": [
		# 	"OPOS Spotify P1218E1D37  Stock",
		# 	"OPOS Spotify P11ADFDDFA  Stock",
		# 	"OPOS Spotify P1141E5D3C  Stock",
		# 	"OPOS Spotify P10DB0D4BE  Stock",
		# 	"OPOS Spotify P107B0FD46  Stock",
		# 	"OPOS Spotify P1016DF90E  Stock",
		# 	"OPOS Spotify P0FAEF62A7  Stock",
		# 	"OPOS Spotify P0F4ACEEDB  Stock",
		# 	"OPOS Spotify P0EE6E8930  Stock",
		# 	"OPOS Spotify P0E89649A6  Stock",
		# 	"OPOS Spotify P0E2BD45D7  Stock",
		# 	"OPOS Spotify P0DCCEAEA3  Stock",
		# 	"OPOS Spotify P0D70EFBFE  Stock",
		# 	"OPOS Spotify P0D1553710  Stock",
		# 	"OPOS Spotify P0CB386227  Stock",
		# 	"OPOS Spotify P0C3751BE6  Stock",
		# 	"OPOS Spotify P0BC0B1632  Stock",
		# 	"OPOS Spotify P0B480BBD8  Stock",
		# 	"OPOS Spotify P0ACCBD915  Stock",
		# 	"OPOS Spotify P0A56621F8  Stock"
		# ],
		"Irving": [
			"FPOS IRVING/FLORENCEVILLEFLORE",
			"FPOS IRVING/BOAT CLUB    FREDE",
			"FPOS IRVING STATION #1170CHIPM",
			"CIRCLE K / IRVING #201   FREDE",
			"FPOS IRVING #15886       WOODS"
		]
	}

	results = {}
	for entity, entries in strings.items():
		res = {}
		for i in range(len(entries)):
			for j in range(i + 1, len(entries)):
				e1, e2 = unclutter(entries[i]), unclutter(entries[j])
				res = {
					"entries[i]": entries[i],
					"entries[j]": entries[j],
					"e1": e1,
					"e2": e2,
					"m": compute_min_edit_distance(e1, e2),
					"same": same_entity(e1, e2)
				}
				if entity in results:
					results[entity].append(res)
				else:
					results[entity] = [res]
		# print(dict_print({entity: results[entity]}))
	# print("\tresults[entity]:\n{re}".format(re=results[entity]))

	print(dict_print(results, "Results", number=True, table_title="Entity name"))
	for res, strings in results.items():
		print("{r}, {s}".format(r=res, s=strings))

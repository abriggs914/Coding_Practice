import datetime
import numpy as np
from transactions_parser import *
from TransactionHandler import *
from pygame_utility import *
from Entity import Entity
from Transaction import Transaction
import re
from matplotlib import pyplot as plt


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
		Transaction(632.42, entities["BWS"], entities["Avery"], "Weekly", "Pay", "Pay", datetime.datetime.now()),
		Transaction(65, entities["Avery"], entities["Irving"], "Weekly", "Gas", "Gas", datetime.datetime.now()),
		Transaction(477.5, entities["Avery"], entities["Colpitts"], "Monthly", "Rent", "Gas", datetime.datetime.now()),

		Transaction(89.99, entities["Avery"], entities["Disney+"], "Annually", "Entertainment", "Disney+ subscription",
					datetime.datetime.now()),
		Transaction(25, entities["Avery"], entities["Nintendo"], "Annually", "Entertainment", "Nintendo subscription",
					datetime.datetime.now()),
		Transaction(69.99, entities["Avery"], entities["Xbox Live"], "Annually", "Entertainment", "Xbox Live subscription",
					datetime.datetime.now()),
		Transaction(69.99, entities["Avery"], entities["Amazon Prime"], "Annually", "Entertainment", "Amazon Prime subscription",
					datetime.datetime.now()),
		Transaction(251.75, entities["Avery"], entities["Codecademy"], "Annually", "Learning", "Codecademy subscription",
					datetime.datetime.now()),
		Transaction(45, entities["Avery"], entities["Spotify"], "Annually", "Entertainment", "Spotify subscription",
					datetime.datetime.now()),
		Transaction(175.93, entities["Avery"], entities["Walmart"], "Once", "Entertainment", "New TV", datetime.datetime.now()),
		Transaction(98.9, entities["Avery"], entities["Walmart"], "Once", "Clothing", "Some new work clothes", datetime.datetime.now()),
		Transaction(17.50, entities["Avery"], entities["SF"], "Monthly", "SF", "SF", datetime.datetime.now()),
		Transaction(15.95, entities["Avery"], entities["ScotiaBank"], "Monthly", "Bank fees", "Bank fees", datetime.datetime.now()),
		Transaction(10.50, entities["Avery"], entities["BMO"], "Monthly", "Bank fees", "Bank fees", datetime.datetime.now()),
		Transaction(25, entities["Avery"], entities["BMO"], "Monthly", "Bill", "Credit card", datetime.datetime.now()),
		Transaction(147.5, entities["GST"], entities["Avery"], "Quarterly", "GST", "GST pamyent", datetime.datetime.now()),
		Transaction(50, entities["Avery"], entities["Phone Bill"], "Monthly", "Bill", "Phone bill", datetime.datetime.now()),
		Transaction(634, entities["Avery"], entities["NSLSC"], "Monthly", "Bill", "Student Loan", datetime.datetime.now()),
		Transaction(100, entities["Avery"], entities["Other"], "Monthly", "Other", "Other", datetime.datetime.now())
	]

	TH = TransactionHandler()

	for t in transactions:
		TH.add_transaction(t)

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
		print("\ncr\t" + cr)
		print("\ner\t" + er)
		print("\nsr\t" + sr)
		res[occurance] = {
			"Costing": money(float(cr.split()[-1])),
			"Earning": money(float(er.split()[-1])),
			"Spending": money(float(sr.split()[-1]))
		}

	print(dict_print(REOCCURRING, min_encapsulation=True))

	print(dict_print(res, "Reports"))
	print(dict_print(ts, "Transactions"))



def scotia_transactions():
	transactions_dict = populate_transactions_dict()
	TH = TransactionHandler()
	me = TH.get_entity("Me")
	print("transactions_dict {td}".format(td=transactions_dict))

	tc, ti = float("inf"), 0
	# tc = 10

	for num, transaction in transactions_dict.items():
		# amount, entity_from, entity_to, reoccurring_category, transaction_catgory, description, date_in
		# Transaction Date, Transaction Amount, Notes, Transaction Type, Entity
		amount = float(transaction["Transaction Amount"])
		entity = Entity(unclutter(transaction["Entity"]))
		transaction_type = transaction["Transaction Type"]
		date = transaction["Transaction Date"]
		# TODO: if if there is no reason to use a dict here, then change to a list
		transaction = {
			"amount": abs(amount),
			"entity_from": me if amount < 0 else entity,
			"entity_to": me if amount > 0 else entity,
			"reoccurring_category": "Once",
			"transaction_category": transaction_type,
			"description": entity,
			"date_in": date
		}
		# print("transaction: {t}".format(t=list(transaction.values())))
		transaction = TH.create_transaction(*list(transaction.values()))
		TH.add_transaction(transaction)
		ti += 1
		if ti == tc:
			break

	print("TH.transaction_list:", TH.transaction_list)
	print(dict_print(dict(zip(range(1, 1 + len(TH.transaction_list)), [tl.info_dict() for tl in TH.transaction_list])), "Transactions"))
	ents = TH.entities_list.copy()
	# ents.sort(key=lambda x: x.name)
	ents.sort(key=lambda x: x.balance)
	entities_dict = {}
	for entity in ents:
		entities_dict[entity.name] = {"balance": money(entity.balance)}
	print(dict_print(entities_dict, "entities dict", number=True))

	print(TH.costing_report(TH.entities_list[0], "Monthly"))
	print(TH.spending_report(TH.entities_list[0], "Monthly"))
	print(TH.earning_report(TH.entities_list[0], "Monthly"))

	empty = dict(zip(["Costing", "Earning", "Spending"], ["-------" for i in range(3)]))
	lt = len(TH.transaction_list)
	sd = TH.first_date
	ed = TH.last_date
	sp = (ed - sd).days
	hd = TH.highest_debit(TH.get_entity("Me"))
	hd = money(hd[0]) + " on " + str(hd[1])
	ad = TH.average_debit(TH.get_entity("Me"))
	ld = TH.lowest_debit(TH.get_entity("Me"))
	ld = money(ld[0]) + " on " + str(ld[1])
	hc = TH.highest_credit(TH.get_entity("Me"))
	hc = money(hc[0]) + " on " + str(hc[1])
	ac = TH.average_credit(TH.get_entity("Me"))
	lc = TH.lowest_credit(TH.get_entity("Me"))
	lc = money(lc[0]) + " on " + str(lc[1])
	res = {
		"# Transactions": lt,
		"Starting": sd,
		"Ending": ed,
		"Span": str(sp) + " day" + ("s" if sp != 1 else ""),
		".": empty,
		"Highest Debit": hd,
		"Average Debit": ad,
		"Lowest Debit": ld,
		"Highest Credit": hc,
		"Average Credit": ac,
		"Lowest Credit": lc,
		"..": empty,
	}
	for occurrence in REOCCURRING:
		cr = TH.costing_report("Me", occurrence)
		er = TH.earning_report("Me", occurrence)
		sr = TH.spending_report("Me", occurrence)
		print("\ncr\t" + cr)
		print("\ner\t" + er)
		print("\nsr\t" + sr)
		res[occurrence] = {
			"Costing": money(float(cr.split()[-1])),
			"Earning": money(float(er.split()[-1])),
			"Spending": money(float(sr.split()[-1]))
		}

	# print(dict_print(REOCCURRING, min_encapsulation=True))

	print(dict_print(res, "Scotiabank Reporting"))
	# print(dict_print(ts, "Transactions"))


def temp_main():
	transactions_dict = populate_transactions_dict()
	TH = TransactionHandler()
	me = TH.get_entity("Me")
	tc, ti = float("inf"), 0
	# print("transactions_dict {td}".format(td=transactions_dict))
	print("\tReport\n", TH.costing_report(me, "Annually"))
	for num, transaction in transactions_dict.items():
		# amount, entity_from, entity_to, reoccurring_category, transaction_catgory, description, date_in
		# Transaction Date, Transaction Amount, Notes, Transaction Type, Entity
		amount = float(transaction["Transaction Amount"])
		entity = Entity(unclutter(transaction["Entity"]))
		transaction_type = transaction["Transaction Type"]
		date = transaction["Transaction Date"]
		# TODO: if if there is no reason to use a dict here, then change to a list
		transaction = {
			"amount": abs(amount),
			"entity_from": me if amount < 0 else entity,
			"entity_to": me if amount > 0 else entity,
			"reoccurring_category": "Once",
			"transaction_category": transaction_type,
			"description": entity,
			"date_in": date
		}
		# print("transaction: {t}".format(t=list(transaction.values())))
		transaction = TH.create_transaction(*list(transaction.values()))
		TH.add_transaction(transaction)
		ti += 1
		if ti == tc:
			break
	print("TH.transaction_list:", TH.transaction_list)
	print(dict_print(dict(zip(range(1, 1 + len(TH.transaction_list)), [tl.info_dict() for tl in TH.transaction_list])), "Transactions"))
	# ents = TH.entities_list.copy()
	# # ents.sort(key=lambda x: x.name)
	# ents.sort(key=lambda x: x.balance)
	# entities_dict = {}
	# for entity in ents:
	# 	entities_dict[entity.name] = {"balance": money(entity.balance)}
	# print(dict_print(entities_dict, "entities dict", number=True))
	#
	# print(TH.costing_report(TH.entities_list[0], "Monthly"))
	# print(TH.spending_report(TH.entities_list[0], "Monthly"))
	# print(TH.earning_report(TH.entities_list[0], "Monthly"))


def quick_view():
	app = PygameApplication("Transaction History", 750, 500)
	game = app.get_game()
	display = app.display

	current_data = []

	# show_graph_data("2021-01-01", "2021-10-11")

	label_start_date = Label(game, display, Rect2(25, 10, 160, 32), "Start Date:", fs=26)
	label_end_date = Label(game, display, Rect2(25, 42, 160, 32), "End Date:", fs=26)
	tbox_start_date = TextBox(game, display, Rect2(185, 10, 160, 32))
	tbox_end_date = TextBox(game, display, Rect2(185, 42, 160, 32))
	control_panel = ButtonBar(game, display, Rect2(25, 450, 160, 32), is_horizontal=False)
	results_window = TextBox(game, display, Rect2(400, 10, 200, 450), locked=True, draw_clear_btn=False, text="Run a report")

	def show_graph_data(current_data, start_date=None, end_date=None, entity_name=None, transaction_type=None):

		print(dict_print({"start_date": start_date, "end_date": end_date, "entity_name": entity_name,
						  "transaction_type": transaction_type}))

		transactions_dict = populate_transactions_dict()

		for k, v in transactions_dict.items():
			d = datetime.datetime.strptime(v["Transaction Date"], "%m/%d/%Y")
			v["Transaction Date"] = d.strftime("%Y-%m-%d")

		entities = {"Me": 0}
		values_spending = []
		labels_spending = []
		keys = list(transactions_dict.keys())
		keys.sort(reverse=True)

		print("keys1:", keys)

		if start_date is not None and end_date is not None:

			start_date = start_date.replace(" ", "")
			t_keys = []
			for k in keys:
				v = transactions_dict[k]
				# print("start_date:", start_date, "v[\"Transaction Date\"]", v["Transaction Date"], "end_date:", end_date, "start_date <= v[\"Transaction Date\"] <= end_date", start_date <= v["Transaction Date"] <= end_date)
				if start_date <= v["Transaction Date"] <= end_date:
					t_keys.append(k)
			keys = t_keys

		print("keys2", keys)

		for t_num in keys:
			t = transactions_dict[t_num]
			d = t["Transaction Date"]
			a = float(t["Transaction Amount"])
			y = t["Transaction Type"]
			n = t["Notes"]
			e = t["Entity"]
			if e not in entities:
				entities[e] = [-1 * a, [t]]
			else:
				entities[e] = [entities[e][0] + (-1 * a), entities[e][1] + [t]]
			entities["Me"] += a
			if d not in labels_spending:
				labels_spending.append(d)
				values_spending.append(0)
			values_spending[labels_spending.index(d)] += a

		if labels_spending:
			plt.plot(labels_spending, values_spending)
			step = ceil(len(labels_spending) / 20)
			plt.xticks(ticks=np.arange(0, (len(labels_spending) + step), step), rotation=65)
			plt.tight_layout()
			fig = plt.savefig("graph_image.png", transparent=True)
			plt.show()
		# print(dict_print({e: (v[0] if e != "Me" else v) for e, v in entities.items()}, "Entities"))

			current_data.append({k: transactions_dict[k] for k in keys})
			current_data = current_data[-5:]
		else:
			print("nothing to show")

	def update_results_window():
		if current_data:
			most_recent = current_data[-1]
			nt = len(most_recent)
			spent, earned = 0, 0
			for tn, t in transactions_dict.items():
				val = t["Transaction Amount"]
				if val < 0:
					spent += val
				else:
					earned += val
			results_window.set_text(
				"""{} -> {}
				
				N Transactions: {}
				Spent:          {}
				Earned:         {}
				Diff:           {}
				""".format(tbox_start_date.get_text(), tbox_end_date.get_text(), nt, spent, earned, (earned - spent)))

			f_name = "graph_image.png"
			img_surf = game.image.load(f_name)
			display.blit(img_surf, (20, 20))
		else:
			results_window.set_text("Run a report")


	tbox_start_date.set_text("2021-01-01")
	tbox_end_date.set_text("2021-10-10")


	while app.is_playing:
		display.fill(BLACK)
		control_panel.buttons.clear()

		label_start_date.draw()
		label_end_date.draw()
		tbox_start_date.draw()
		tbox_end_date.draw()
		control_panel.add_button("Refresh Window", YELLOW_3, YELLOW_2, update_results_window)
		control_panel.add_button("View Graph", GREEN_3, GREEN_2, show_graph_data, [current_data, tbox_start_date.get_text(), tbox_end_date.get_text()])
		control_panel.draw()
		results_window.draw()

		# draw widgets and objects here
		event_queue = app.run()
		for event in event_queue:
			# handle events
			tbox_start_date.handle_event(event)
			tbox_end_date.handle_event(event)

		app.clock.tick(30)



if __name__ == "__main__":
	quick_view()
	# temp_main()

	# test()
	# scotia_transactions()

	# PRINT = False
	# a = "String one"
	# b = "sTriNg Tne"
	# print(same_entity(a, b))
	#
	# # All of the values in each list should be recognized as the same entity
	# strings = {
	# 	"Amazon": [
	# 		"OPOS AMZN Mktp CA        WWW.A",
	# 		"OPOS Amazon.ca           AMAZO",
	# 		"OPOS Amazon.ca           Seatt",
	# 		"OPOS 0.26 Amazon.com     Amzn"
	# 	],
	# 	"Walmart": [
	# 		"FPOS WALMART Store #3032 FREDE",
	# 		"WALMART STORE #3032      FREDE",
	# 		"WAL-MART #1067           FREDE",
	# 		"WAL-MART #3032           FREDE",
	# 		"WAL-MART #3054           MISSI"
	#
	# 	],
	# 	"Spotify": [
	# 		"OPOS Spotify P1218E1D37  Stock",
	# 		"OPOS Spotify P11ADFDDFA  Stock",
	# 		"OPOS Spotify P1141E5D3C  Stock",
	# 		"OPOS Spotify P10DB0D4BE  Stock",
	# 		"OPOS Spotify P107B0FD46  Stock",
	# 		"OPOS Spotify P1016DF90E  Stock",
	# 		"OPOS Spotify P0FAEF62A7  Stock",
	# 		"OPOS Spotify P0F4ACEEDB  Stock",
	# 		"OPOS Spotify P0EE6E8930  Stock",
	# 		"OPOS Spotify P0E89649A6  Stock",
	# 		"OPOS Spotify P0E2BD45D7  Stock",
	# 		"OPOS Spotify P0DCCEAEA3  Stock",
	# 		"OPOS Spotify P0D70EFBFE  Stock",
	# 		"OPOS Spotify P0D1553710  Stock",
	# 		"OPOS Spotify P0CB386227  Stock",
	# 		"OPOS Spotify P0C3751BE6  Stock",
	# 		"OPOS Spotify P0BC0B1632  Stock",
	# 		"OPOS Spotify P0B480BBD8  Stock",
	# 		"OPOS Spotify P0ACCBD915  Stock",
	# 		"OPOS Spotify P0A56621F8  Stock"
	# 	],
	# 	"Irving": [
	# 		"FPOS IRVING/FLORENCEVILLEFLORE",
	# 		"FPOS IRVING/BOAT CLUB    FREDE",
	# 		"FPOS IRVING STATION #1170CHIPM",
	# 		"CIRCLE K / IRVING #201   FREDE",
	# 		"FPOS IRVING #15886       WOODS"
	# 	]
	# }
	#
	# results = {}
	# for entity, entries in strings.items():
	# 	res = {}
	# 	for i in range(len(entries)):
	# 		for j in range(i + 1, len(entries)):
	# 			e1, e2 = unclutter(entries[i]), unclutter(entries[j])
	# 			res = {
	# 				"entries[i]": entries[i],
	# 				"entries[j]": entries[j],
	# 				"e1": e1,
	# 				"e2": e2,
	# 				"m": compute_min_edit_distance(e1, e2),
	# 				"same": same_entity(e1, e2, tol=6)
	# 			}
	# 			if entity in results:
	# 				results[entity].append(res)
	# 			else:
	# 				results[entity] = [res]
	# 	# print(dict_print({entity: results[entity]}))
	# # print("\tresults[entity]:\n{re}".format(re=results[entity]))
	#
	# if PRINT or True:
	# 	print(dict_print(results, "Results", number=True, table_title="Entity name"))
	# 	for res, strings in results.items():
	# 		print("{r}, {s}".format(r=res, s=strings))

	# test()

'''
<<<<<<< HEAD
	print("Hello World!")
=======
	# test()
>>>>>>> 2f07108745b8da92448a5e2cdb3d70de7caf4fb8
'''
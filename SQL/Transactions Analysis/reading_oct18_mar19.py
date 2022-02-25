import csv

#  with open("oct 2018 - mar 2019.csv", "r") as f:
#  with open("2022-02-02.csv", "r") as f:
with open("2022-02-24.csv", "r") as f:
	d = csv.DictReader(f)
	for dtt in d:
		#  dd = dtt["Transaction Date"]
		#  da = dtt["Transaction Amount"]
		#  dn = dtt["Notes"]
		#  dt = dtt["Transaction Type"]
		#  de = dtt["Entity"]
		#  di = dtt["TransactionTypeID"]
		dd = dtt["Date"]
		da = dtt["Amount"]
		dn = dtt["Notes"]
		dt = dtt["Type"]
		de = dtt["Entity"]
		di = dtt["TransactionTypeID"]
		print("('{}', {}, '{}', '{}', '{}', {}),".format(dd, da, dn, dt, de, di))
	
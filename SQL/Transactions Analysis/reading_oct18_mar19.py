import csv

with open("oct 2018 - mar 2019.csv", "r") as f:
	d = csv.DictReader(f)
	for dtt in d:
		dd = dtt["Transaction Date"]
		da = dtt["Transaction Amount"]
		dn = dtt["Notes"]
		dt = dtt["Transaction Type"]
		de = dtt["Entity"]
		print("('{}', {}, '{}', '{}', '{}', NULL),".format(dd, da, dn, dt, de))
	
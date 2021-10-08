import csv
from utility import *

PRINT = False
transactions_dict = {}


def populate_transactions_dict():
	
	with open("pcbanking.csv", 'r') as f:
	# with open("pcbanking_test.csv", 'r') as f:
		d = csv.DictReader(f, delimiter=',')
		header = d.fieldnames
		print("header: {h}".format(h=header))
		lines = [{k.strip(): v.strip() for k, v in line.items()} for line in d]
		# for l in lines:
		# 	print(l)
		transaction_dict = dict(zip([i for i in range(len(lines))], lines))
		print(dict_print(transaction_dict, "lines", number=True))
		# print("transactions_dict {td}".format(td=transaction_dict))
		return transaction_dict


def unclutter(txt):
	global PRINT
	m = "IN: <" + str(txt) + ">"
	ignore = ["fpos", "opos", "store", "stock", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "=", "+",
			  "{", "}", "[", "]", "?", "/", "<", ">", ":", ";", "'", "`", "~", ",", "."] + [str(i) for i in range(10)]
	i, j = 0, 0
	res = ""
	while i < len(txt):
		if PRINT:
			print("\n\n")
		found = None
		for val in ignore:
			end = i + len(val)
			if PRINT:
				print("val.lower(): {vl}\ntxt[i: end].lower(): {tie}\nend: {e}".format(vl=val.lower(),
																					   tie=txt[i: end].lower(), e=end))
			if val.lower() == txt[i: end].lower():
				found = val
				# i += len(val)
				break

		if found is None:
			res += txt[i]
		else:
			i += len(found)
		i += 1

	# for val in ignore:
	# 	txt = txt.replace(val, "")
	# txt = txt.strip()
	# m += "     OUT: <" + str(txt) + ">"
	txt = res.strip()
	spl = txt.split()
	txt = " ".join([x.strip() for x in spl if len(x) > 1])
	m += "     OUT: <" + str(txt) + ">"
	if PRINT:
		print(m)
	return txt


if __name__ == "__main__":
	print(dict_print(populate_transactions_dict(), "lines", number=True))

import csv
from utility import *

transactions_dict = {}


def populate_transactions_dict():
	
	with open("pcbanking.csv", 'r') as f:
		d = csv.DictReader(f, delimiter=',')
		header = d.fieldnames
		print("header: {h}".format(h=header))
		lines = [{k.strip(): v.strip() for k, v in line.items()} for line in d]
		for l in lines:
			print(l)
		transactions_dict = dict(zip([i for i in range(len(lines))], lines))
		print(dict_print(transactions_dict, "lines", number=True))
		print("transactions_dict {td}".format(td=transactions_dict))
		return transactions_dict


if __name__ == "__main__":
	print(dict_print(populate_transactions_dict(), "lines", number=True))

import csv
import xlwt
from xlwt import Workbook

# Create an excel worksheet to store MTG card data dump.

if __name__ == "__main__":
	fn = "Collection.csv"
	lines = []
	with open(fn, "r") as f:
		lines = f.readlines()
	
	if lines:
		wb = Workbook()
		
		# add_sheet is used to create sheet.
		sheet1 = wb.add_sheet("Sheet 1")
		
		# writing in (r, c, Value) format
		for i, line in enumerate(lines):
			spl_line = line.split("\t")
			for j, val in enumerate(spl_line):
				sheet1.write(i, j, val)
		
	
		wb.save("cards.xls")
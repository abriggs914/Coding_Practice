import csv
import xlwt
from xlwt import Workbook

# Create an excel worksheet.

if __name__ == "__main__":	
	wb = Workbook()
		
	# add_sheet is used to create sheet.
	sheet1 = wb.add_sheet("Sheet 1")
		
	# writing in (r, c, Value) format
	hrs = [37.5 + (i * 1.25) for i in range(7)]
	mon = [40000 + (i * 250) for i in range(441)]
	vals = [[50] + hrs] + [[m] + [m / (50 * h) for h in hrs] for m in mon]
	for i, row in enumerate(vals):
		for j, val in enumerate(row):
			sheet1.write(i, j, val)
	
	wb.save("hours2.xls")
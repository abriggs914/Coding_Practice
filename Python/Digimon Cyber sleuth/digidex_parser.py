import csv

with open("digidex.csv", "r") as digidexCSV:
	digidex = csv.DictReader(digidexCSV)
	print(dir(digidex))
	print("Header: " + str(digidex.fieldnames))
	# for digimon in digidex:
		# print(digimon)
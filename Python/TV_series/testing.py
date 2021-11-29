
with open("input.txt", "r") as f:
	lines = f.readlines()
	for i, l in enumerate(lines):
		print("i: {}, l: {}".format(i, l))
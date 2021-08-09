class Colour:

	def __init__(self, name, hex, r, g, b, a):
		self.name = "_".join(name.split(" ")).upper().replace("(", "_").replace(")", "_").replace("*", "").replace("/", "")
		self.hex = hex
		self.r = int(r)
		self.g = int(g)
		self.b = int(b)
		self.a = int(a)
		
	def csv_entry(self):
		return ",".join(list(map(str, [self.name, self.hex, self.r, self.g, self.b, self.a])))
	
	def py_entry(self):
		return self.name + " = (" + ", ".join(list(map(str, [self.r, self.g, self.b]))) + ")"
		
	def __repr__(self):
		return "Name: {}, Hex: #{} RGB: ({}, {}, {}), Access: {}".format(self.name, self.hex, self.r, self.g, self.b, self.a)
		
with open("colours_file.txt", "r") as f1:
	lines = f1.readlines()
	colours = []
	for line in lines:
		spl = line.strip().split("#")
		names = spl[0]
		name = names.split("\t")[0]
		nums = spl[-1]
		#print("nums:", nums, "nums.split(\" \"):", nums.split("\t"))
		#nums_spl = nums.spl
		colours.append(Colour(name, *list(map(lambda x: x, nums.split("\t")))))
		# print("new_colour:", colours[-1])
		# print(colours[-1].name)
	
	colours.sort(key=lambda c: c.name)
	for colour in colours:
		print(colour.name)
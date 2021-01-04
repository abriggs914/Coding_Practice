from digimon import Digimon

types = ["vaccine", "virus", "data", "free"]
attributes = {
	"ring1": [
				("Water", "Blue"),
				("fire", "Red"),
				("Plant", "Green")
			],
	"ring2": [
				("Earth", "Brown"),
				("Electric", "Yellow"),
				("Wind", "Light Blue")
			],
	"ring3": [
				("Light", "White"),
				("Dark", "Purple")
			],
	"ring4": [
				("Neutral", "Grey")
			]
}

def digimon_strong_against_type(digimon):
	t = digimon.typeIn
	return type_strong_against(t)
	
def digimon_strong_against_attr(digimon):
	a = digimon.attrIn
	return attr_strong_against(a)
	
def digimon_weak_against_type(digimon):
	t = digimon.typeIn
	return type_weak_against(t)
	
def digimon_attack_mult(attack_digimon, defend_digimon):
	tm = type_attack_dmg_mult(attack_digimon.typeIn, defend_digimon.typeIn)
	am = attr_attack_dmg_mult(attack_digimon.attrIn, defend_digimon.attrIn)
	return tm * am

def attr_strong_against(typeIn):
	ring = [r for r, lst in attributes.items() if typeIn in lst][0]
	lst = attributes[ring]
	i = lst.index(typeIn)
	j = (i + 1) % len(lst)
	# ring 4 exception
	if i == j:
		return None
	return lst[j]
	
def type_strong_against(typeIn):
	i = types.index(typeIn)
	if i == 3:
		return None
	return types[(i + 1) % 3]
	
def type_weak_against(typeIn):
	i = types.index(typeIn)
	if i == 3:
		return None
	return types[(i - 1) % 3]
	
def type_attack_dmg_mult(attack_type, defend_type):
	if type_strong_against(attack_type) == defend_type:
		return 2
	elif type_weak_against(attack_type) == defend_type:
		return 0.5
	else:
		return 1
	
def attr_attack_dmg_mult(attack_attr, defend_attr):
	if attr_strong_against(attack_attr) == defend_attr:
		return 1.5
	else:
		return 1
		
# # Printing types strong and against
# t1 = types[0]
# t2 = types[1]
# t3 = types[2]
# t4 = types[3]
# for t in types:
	# print("\n\t" + str(t) + "\nstrong against: " + str(type_strong_against(t)))
	# print("weak against: " + str(type_weak_against(t)))
	# print("(" + str(t) + ") damage multiplier against (" + str(t1) + "): " + str(type_attack_dmg_mult(t, t1)))
	# print("(" + str(t) + ") damage multiplier against (" + str(t2) + "): " + str(type_attack_dmg_mult(t, t2)))
	# print("(" + str(t) + ") damage multiplier against (" + str(t3) + "): " + str(type_attack_dmg_mult(t, t3)))
	# print("(" + str(t) + ") damage multiplier against (" + str(t4) + "): " + str(type_attack_dmg_mult(t, t4)))
	
# Printing attributes strong and against
for ring, attribute_list in attributes.items():
	print("\n\t" + str(ring))
	for attr in attribute_list:
		print(str(attr) + " strong against " + str(attr_strong_against(attr)))
		
d1 = Digimon("1", 1, types[0], attributes["ring1"][0])
d2 = Digimon("2", 2, types[0], attributes["ring1"][0])
d3 = Digimon("1", 1, types[1], attributes["ring3"][0])
d4 = Digimon("2", 2, types[2], attributes["ring3"][1])
print(str(d1) + " VS. " + str(d2) + ": " + str(digimon_attack_mult(d1, d2)))
print(str(d3) + " VS. " + str(d4) + ": " + str(digimon_attack_mult(d3, d4)))
	

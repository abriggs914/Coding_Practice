from utility import *

fry = "Fry"
leela = "Leela"
zoid = "Zoidberg"
prof = "Professor"
amy = "Amy"
must = "Mustache"
afro = "Afro"
bucket = "Mop Bucket"
king = "King"
bender = "Bender"
hermes = "Hermes"

switches = []

switches.append((fry, must))	#	A
switches.append((zoid, afro))	#	B
switches.append((must, zoid))	#	C
switches.append((afro, fry))	#	D
switches.append((prof, must))	#	E
switches.append((bucket, afro))	#	F
switches.append((must, leela))	#	G
switches.append((afro, king))	#	H
switches.append((hermes, must))	#	I
switches.append((bender, afro))	#	J
switches.append((must, amy))	#	K
switches.append((afro, prof))	#	L
switches.append((bucket, must))	#	M

people = {fry: [], must: [], zoid: [], afro: [], prof: [], bucket: [], leela: [], king: [], hermes: [], bender: [], amy: []}

for switch in switches:
	a, b = switch
	people[a].append(b)
	
print(dict_print(people))
	
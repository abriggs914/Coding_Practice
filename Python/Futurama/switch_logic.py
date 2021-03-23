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

switches.append((fry, must))
switches.append((zoid, afro))
switches.append((must, zoid))
switches.append((afro, fry))
switches.append((prof, must))
switches.append((bucket, afro))
switches.append((must, leela))
switches.append((afro, king))
switches.append((hermes, must))
switches.append((bender, afro))
switches.append((must, amy))
switches.append((afro, prof))
switches.append((bucket, must))

people = {fry: [], must: [], zoid: [], afro: [], prof: [], bucket: [], leela: [], king: [], hermes: [], bender: [], amy: []}

for switch in switches:
	a, b = switch
	people[a].append(b)
	
print(dict_print(people))
	
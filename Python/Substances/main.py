# Python program to view letal doses of substances
# Saw a chart on the web
# 2021-06-04

from utility import *


substances = {
	"water": (90000, "mg/kg", ""),
	"sucrose": (29700, "mg/kg", "table sugar"),
	"monosodium glutamate": (16600, "mg/kg", "MSG"),
	"stevioside": (15000, "mg/kg", "from stevia"),
	"gasoline": (14063, "mg/kg", "petrol"),
	"viitamin c": (11900, "mg/kg", ""),
	"lactose": (10000, "mg/kg", "milk sugar"),
	"aspartame": (10000, "mg/kg", ""),
	"cyanuric acid": (7700, "mg/kg", "component of bleach"),
	"ethanol": (7060, "mg/kg", ""),
	"melamine": (6000, "mg/kg", "found in dishware and magic erasers"),
	"sodium chloride": (3000, "mg/kg", "salt"),
	"acetaminophen": (1944, "mg/kg", "paracetamol"),
	"THC": (1270, "mg/kg", ""),
	"cannabidiol": (980, "mg/kg", "CBD"),
	"methanol": (810, "mg/kg", ""),
	"ibuprofen": (636, "mg/kg", ""),
	"formaldehyde": (600, "mg/kg", ""),
	"solanine": (590, "mg/kg", "component of nightshade plants"),
	"psilocybin": (280, "mg/kg", ""),
	"hydrochloric acid": (238, "mg/kg", "used for cleaning, batteries, and fireworks"),
	"ketamine": (229, "mg/kg", "anesthesia medication"),
	"asprin": (200, "mg/kg", ""),
	"caffeine": (192, "mg/kg", ""),
	"sodium nitrate": (180, "mg/kg", "used in cured meats"),
	"MDMA/ecstasy": (160, "mg/kg", ""),
	"DDT": (135, "mg/kg", "insecticide"),
	"uranium": (114, "mg/kg", ""),
	"bisoprolol": (100, "mg/kg", "beta blocker medication"),
	"sodium thiopental": (64, "mg/kg", "used in lethal injections"),
	"methamphetamine": (57, "mg/kg", ""),
	"sodium fluoride": (52, "mg/kg", ""),
	"capsaicin": (47.2, "mg/kg", "active component of chili peppers"),
	"vitamin D3": (37, "mg/kg", "from exposure to sunlight"),
	"heroin": (21.8, "mg/kg", ""),
	"LSD": (16.5, "mg/kg", ""),
	"arsenic": (13, "mg/kg", ""),
	"sodium cyanide": (6.4, "mg/kg", ""),
	"chlorotoxin": (4.3, "mg/kg", "scorpion toxin"),
	"nicotine": (0.8, "mg/kg", ""),
	"fentanyl": (300, "ug/kg", ""),
	"sarin": (172, "ug/kg", "nerve agent"),
	"inland taipan venom": (25, "ug/kg", ""),
	"ricin": (22, "ug/kg", "from castor oil plants"),
	"TCDD": (20, "ug/kg", "in agent orange"),
	"CRTX-A": (5, "ug/kg", "from box jellyfish"),
	"latrotoxin": (4.3, "ug/kg", "from widow spider venom"),
	"batrachotoxin": (2, "ug/kg", "from poison dart frog"),
	"maitotoxin": (130, "ng/kg", "from algae eaten by ciguatera fish"),
	"polonium-210": (10, "ng/kg", "used for nuclear weapons production and to eliminate static"),
	"diphtheria toxin": (10, "ng/kg", ""),
	"shiga toxin": (2, "ng/kg", "from dysentery"),
	"tetranospasmin": (2, "ng/kg", "tetanus toxin"),
	"botulinum toxin": (1, "ng/kg", "causes botulism and used in botox")
}

# all substance ld50s are of format: (some_mass / kg)
def calc_g_kg(substance):
	ld50 = substance.ld50
	mass = substance.units.split("/")[0].strip()
	units = {
		"kg": lambda x: x * 1000,
		"g": lambda x: x,
		"mg": lambda x: x / 1000,
		"ug": lambda x: x / 1000000,
		"ng": lambda x: x / 1000000000,
	}
	return units[mass](ld50)


class Substance:
	def __init__(self, name, ld50, units, description):
		self.name = name
		self.ld50 = ld50
		self.units = units
		self.description = description
		self.ld50_gkg = calc_g_kg(self)
		
	def __iter__(self):
		d = self.description if self.description else "N/A"
		dct = {
			"LD50 (g / kg)": self.ld50_gkg,
			"Description": d
		}
		for key, val in dct.items():
			yield (key, val)
	
	def __repr__(self):
		d = " " + self.description if self.description else ""
		return "{}: {} g/kg{}".format(self.name, self.ld50_gkg, d)
		
		
print(dict_print({k: dict(Substance(k, *v)) for k, v in substances.items()}, "Substances"))

# mass in kg
def lethal_dose_mass(mass):
	res = {}
	for name, vals in substances.items():
		ld50, units, desc = vals
		s = Substance(name, ld50, units, desc)
		info = dict(s)
		info.update({"Lethal dose for {} kg (g)".format(mass): s.ld50_gkg * mass})
		res[name] = info
	return res
		
print(dict_print(lethal_dose_mass(lbs_kg(235)), "Lethal Doses"))

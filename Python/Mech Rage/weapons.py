primary_weapons = {
	"plasma gun mk.1" : {"DMG" : 4, "RPM": 212, "COST": 0},
	"plasma gun mk.2" : {"DMG" : 4, "RPM": 296, "COST": 500},
	"plasma gun mk.3" : {"DMG" : 4, "RPM": 416, "COST": 1750},
	"plasma gun mk.4" : {"DMG" : 10, "RPM": 212, "COST": 3500},
	"plasma gun mk.5" : {"DMG" : 10, "RPM": 296, "COST": 7250},
	"plasma gun mk.6" : {"DMG" : 10, "RPM": 416, "COST": 12000},
	"plasma gun mk.7" : {"DMG" : 28, "RPM": 212, "COST": 20000},
	"plasma gun mk.8" : {"DMG" : 28, "RPM": 296, "COST": 20000},
	"plasma gun mk.9" : {"DMG" : 28, "RPM": 416, "COST": 45000}
}

def dps(gun):
	return (primary_weapons[gun]["DMG"] * (primary_weapons[gun]["RPM"] / 60))
	
def dmg_per_cost(gun):
	if primary_weapons[gun]["COST"] == 0:
		return "NaN"
	return primary_weapons[gun]["DMG"] / primary_weapons[gun]["COST"]
	
def dps_per_cost(gun):
	if primary_weapons[gun]["COST"] == 0:
		return "NaN"
	return dps(gun) / primary_weapons[gun]["COST"]
	
for gun in primary_weapons:
	print("gun: " + gun + "\n\tDPS: " + str(dps(gun)) + "\n\tDMG per cost: " + str(dmg_per_cost(gun)) + "\n\tDPS per cost: " + str(dps_per_cost(gun)))


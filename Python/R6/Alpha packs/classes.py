class Reward:

    def __init__(self, rarity, name, description, duplicate, renown, availibility, code, operator, gun):
        self.rarity = rarity
        self.name = name
        self.description = description
        self.duplicate = duplicate
        self.renown = renown
        self.availibility = availibility
        self.code = code
        self.operator = operator
        self.gun = gun

    def __repr__(self):
        return "{" + self.rarity + "}, " + self.name + ", " + self.description

class Operator:

    def __init__(self, atk_def, name, unit, difficulty, speed, armour):
        self.atk_def = atk_def
        self.name = name
        self.unit = unit
        self.difficulty = difficulty
        self.speed = speed
        self.armour = armour

    def __repr__(self):
        atk_def = "Attacker" if self.atk_def else "Defender"
        return atk_def + " " + self.name + " {" + self.unit + "}"

class Weapon:

    def __init__(self, name, pri_sec, group):
        self.name = name
        self.pri_sec = pri_sec
        self.group = group

    def __repr__(self):
        return self.name + " {" + self.group + "}"

operators_dict = {
    "Pathfinders": {
        "Attack": [
            Operator(1, "Sledge", "SAS", 1, 2, 2),
            Operator(1, "Thatcher", "SAS", 1, 2, 2),
            Operator(1, "Ash", "FBI", 2, 3, 1),
            Operator(1, "Thermite", "FBI", 1, 2, 2),
            Operator(1, "Twitch", "GIGN", 2, 2, 2),
            Operator(1, "Montagne", "GIGN", 3, 1, 3),
            Operator(1, "Glaz", "Spetsnaz", 2, 2, 2),
            Operator(1, "Fuze", "Spetsnaz", 1, 1, 3),
            Operator(1, "Blitz", "GSG 9", 3, 2, 2),
            Operator(1, "IQ", "GSG 9", 3, 3, 1)
            ],
        "Defense": [
            Operator(0, "Smoke", "SAS", 2, 2, 2),
            Operator(0, "Mute", "SAS", 1, 2, 2),
            Operator(0, "Castle", "FBI", 2, 2, 2),
            Operator(0, "Pulse", "FBI", 3, 3, 1),
            Operator(0, "Doc", "GIGN", 1, 1, 3),
            Operator(0, "Rook", "GIGN", 1, 1, 3),
            Operator(0, "Kapkan", "Spetsnaz", 1, 2, 2),
            Operator(0, "Tachanka", "Spetsnaz", 1, 1, 3),
            Operator(0, "Jager", "GSG 9", 2, 2, 2),
            Operator(0, "Bandit", "GSG 9", 1, 3, 1)
        ]
    },
    "Y1S1 - Black Ice" : {
        "Attack": [
            Operator(1, "Buck", "JTF2", 1, 2, 2)
            ],
        "Defense": [
            Operator(0, "Frost", "JTF2", 1, 2, 2)
        ]
    },
    "Y1S2 - Dust Line" : {
        "Attack": [
            Operator(1, "Blackbeard", "NAVY SEAL", 1, 2, 2)
            ],
        "Defense": [
            Operator(0, "Valkyrie", "NAVY SEAL", 2, 2, 2)
        ]
    },
    "Y1S3 - Skull Rain" : {
        "Attack": [
            Operator(1, "Capitao", "BOPE", 2, 3, 1)
            ],
        "Defense": [
            Operator(0, "Caveira", "BOPE", 3, 3, 1)
        ]
    },
    "Y1S4 - Red Crow" : {
        "Attack": [
            Operator(1, "Hibana", "SAT", 1, 3, 1)
            ],
        "Defense": [
            Operator(0, "Echo", "SAT", 3, 1, 3)
        ]
    },
    "Y2S1 - Velvet Shell" : {
        "Attack": [
            Operator(1, "Jackal", "GEO", 3, 2, 2)
            ],
        "Defense": [
            Operator(0, "Mira", "GEO", 3, 2, 3)
        ]
    },
    "Y2S3 - Blood Orchid" : {
        "Attack": [
            Operator(1, "Ying", "SDU", 2, 2, 2)
            ],
        "Defense": [
            Operator(0, "Lesion", "SDU", 1, 2, 2),
            Operator(0, "Ela", "GROM", 1, 3, 1)
        ]
    },
    "Y2S4 - White Noise" : {
        "Attack": [
            Operator(1, "Dokkabei", "707th SMB", 2, 2, 2),
            Operator(1, "Zofia", "GROM", 1, 2, 2)
            ],
        "Defense": [
            Operator(0, "Vigil", "707th SMB", 3, 3, 1)
        ]
    },
    "Y3S1 - Chimera" : {
        "Attack": [
            Operator(1, "Lion", "CBRN THREAT UNIT", 1, 2, 2),
            Operator(1, "Finka", "CBRN THREAT UNTI", 1, 2, 2)
            ],
        "Defense": [
        ]
    },
    "Y3S2 - Para Bellum" : {
        "Attack": [
            ],
        "Defense": [
            Operator(0, "Maestro", "GIS", 2, 1, 3),
            Operator(0, "Alibi", "GIS", 3, 3, 1)
        ]
    },
    "Y3S3 - Grim Sky" : {
        "Attack": [
            Operator(1, "Maverick", "GSUTR", 2, 3, 1)
            ],
        "Defense": [
            Operator(0, "Clash", "GSUTR", 3, 1, 3)
        ]
    },
    "Y3S4 - Wind Bastion" : {
        "Attack": [
            Operator(1, "Nomad", "GIGR", 3, 2, 2)
            ],
        "Defense": [
            Operator(0, "Kaid", "GIGR", 2, 1, 3)
        ]
    },
    "Y4S1 - Burnt Horizon" : {
        "Attack": [
            Operator(1, "Gridlock", "SASR", 1, 1, 3)
            ],
        "Defense": [
            Operator(0, "Mozzie", "SASR", 2, 2, 2)
        ]
    },
    "Y4S2 - Phantom Sight" : {
        "Attack": [
            Operator(1, "Nokk", "JAEGER CORPS", 3, 2, 2)
            ],
        "Defense": [
            Operator(0, "Warden", "SECRET SERVICE", 2, 2, 2)
        ]
    },
    "Y4S3 - Ember Rise" : {
        "Attack": [
            Operator(1, "Amaru", "APCA", 2, 2, 2)
            ],
        "Defense": [
            Operator(0, "Goyo", "FUERZAS ESPECIALES", 2, 2, 2)
        ]
    },
    "Y4S4 - Shifting Tides" : {
        "Attack": [
            Operator(1, "Kali", "NIGHTHAVEN", 2, 2, 2)
            ],
        "Defense": [
            Operator(0, "Wamai", "NIGHTHAVEN", 2, 2, 2)
        ]
    },
    "Y5S1 - Void Edge" : {
        "Attack": [
            Operator(1, "Iana", "REU", 1, 2, 2)
            ],
        "Defense": [
            Operator(0, "Oryx", "UNAFFILIATED", 2, 2, 2)
        ]
    },
    "Y5S2 - Steel Wave" : {
        "Attack": [
            Operator(1, "Ace", "NIGHTHAVEN", 1, 2, 2)
            ],
        "Defense": [
            Operator(0, "Melusi", "INKABA TASK FORCE", 1, 3, 1)
        ]
    },
    "Y5S3 - Shadow Legacy" : {
        "Attack": [
            Operator(1, "Zero", "ROS", 1, 2, 2)
            ],
        "Defense": [
        ]
    },
    "Y5S4 - Neon Dawn" : {
        "Attack": [
            ],
        "Defense": [
            Operator(0, "ARUNI", "NIGHTHAVEN", 2, 2, 2)
        ]
    },
    "Y6S1 - Crimson Heist" : {
        "Attack": [
            Operator(1, "Flores", "UNAFFILIATED", 2, 2, 2)
            ],
        "Defense": [
        ]
    }
}
# pathfinders_attackers = [[ops for side, ops in operators_dict[season].items() if side == "Attack"] for season in operators_dict if season == "Pathfinders"]
pathfinders_attackers = []
pathfinders_defenders = []
attackers = []
defenders = []
units = {}
years = []
seasons = []

for season in operators_dict:
    spl = season.split("-")
    if len(spl) == 2:
        s_year = spl[0].strip()
        s_name = spl[1].strip()
    else:
        s_year = 0
        s_name = season
    years.append(s_year)
    seasons.append(s_name)
    atk = operators_dict[season]["Attack"]
    dfn = operators_dict[season]["Defense"]
    for op in atk:
        unit = op.unit
        attackers.append(op)
        if unit not in units:
            units[unit] = [op]
        else:
            units[unit].append(op)
        if season == "Pathfinders":
            pathfinders_attackers.append(op)
    for op in dfn:
        unit = op.unit
        defenders.append(op)
        if unit not in units:
            units[unit] = [op]
        else:
            units[unit].append(op)
        if season == "Pathfinders":
            pathfinders_defenders.append(op)

weapons = {
    "Primary": [],
    "Secondary": []
}

with open("weapons.csv", "r") as w:
    lines = w.readlines()
    for i, line in enumerate(lines):
        if i > 0:
            spl = line.split(",")
            pri_sec = spl[0].strip()
            name = spl[1].strip()
            group = spl[2].strip()
            k = "Primary" if pri_sec else "Secondary"
            weapons[k].append(Weapon(name, pri_sec, group))

def add_weapon(weapon, pri_sec, group):
    new_weapon = None
    with open("weapons.csv", "a") as w:
        pri_sec = "1" if pri_sec else "0"
        w.write("\n" + pri_sec + ", " + weapon + ", " + group)
        k = "Primary" if pri_sec else "Secondary"
        new_weapon = Weapon(weapon, pri_sec, group)
        weapons[k].append(new_weapon)
    return new_weapon

def lookup_weapon(name):
    print("looking up:", name)
    weapon = None
    if name.lower() == "universal":
        weapon = [] 
    for group in weapons:
        for w in weapons[group]:
            print("comparing:", w, "res", (str(w).lower() == name.lower()))
            if name.lower() == "universal":
                weapon.append(w)
            elif str(w).lower() == name.lower():
                return w
    return weapon





def tests():
    ops = attackers + defenders
    f = lambda x, a, b, c: x.difficulty == a and x.speed == b and x.armour == c 
    b = lambda x: "\n\t" + x[0] + "\n\t\t" + "\n\t\t".join(list(map(str, x[1])))
    vals = {
        "d1s1a1": [op for op in ops if f(op, 1, 1, 1)],
        "d1s1a2": [op for op in ops if f(op, 1, 1, 2)],
        "d1s1a3": [op for op in ops if f(op, 1, 1, 3)],

        "d1s2a1": [op for op in ops if f(op, 1, 2, 1)],
        "d1s2a2": [op for op in ops if f(op, 1, 2, 2)],
        "d1s2a3": [op for op in ops if f(op, 1, 2, 3)],

        "d1s3a1": [op for op in ops if f(op, 1, 3, 1)],
        "d1s3a2": [op for op in ops if f(op, 1, 3, 2)],
        "d1s3a3": [op for op in ops if f(op, 1, 3, 3)],

        "d2s1a1": [op for op in ops if f(op, 2, 1, 1)],
        "d2s1a2": [op for op in ops if f(op, 2, 1, 2)],
        "d2s1a3": [op for op in ops if f(op, 2, 1, 3)],

        "d2s2a1": [op for op in ops if f(op, 2, 2, 1)],
        "d2s2a2": [op for op in ops if f(op, 2, 2, 2)],
        "d2s2a3": [op for op in ops if f(op, 2, 2, 3)],

        "d2s3a1": [op for op in ops if f(op, 2, 3, 1)],
        "d2s3a2": [op for op in ops if f(op, 2, 3, 2)],
        "d2s3a3": [op for op in ops if f(op, 2, 3, 3)],

        "d3s1a1": [op for op in ops if f(op, 3, 1, 1)],
        "d3s1a2": [op for op in ops if f(op, 3, 1, 2)],
        "d3s1a3": [op for op in ops if f(op, 3, 1, 3)],

        "d3s2a1": [op for op in ops if f(op, 3, 2, 1)],
        "d3s2a2": [op for op in ops if f(op, 3, 2, 2)],
        "d3s2a3": [op for op in ops if f(op, 3, 2, 3)],

        "d3s3a1": [op for op in ops if f(op, 3, 3, 1)],
        "d3s3a2": [op for op in ops if f(op, 3, 3, 2)],
        "d3s3a3": [op for op in ops if f(op, 3, 3, 3)]
    }
    
    print("\n".join(list(map(b, list(vals.items())))))
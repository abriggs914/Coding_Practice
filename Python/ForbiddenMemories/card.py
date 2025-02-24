from typing import Optional, Generator


gen_unknown_ids: Generator[int, None, None] = (i for i in range(1000, 7001))

types_monster = ["A", "B", "BW", "Di", "Dr", "Fd", "Fh", "Fy", "I", "Mc", "Pl", "Py", "Re", "Ro", "SC", "SS", "Th", "W", "WB", "Z"]
types_equip = ["E"]
types_magic = ["Mg"]
types_trap = ["Tr"]
types_ritual = ["Ri"]

star_sign_ring_0 = ["Su", "Mo", "V", "Me"]
star_sign_ring_1 = ["Ma", "J", "Sa", "U", "P", "N"]

star_sign_ring_0_sym = ["☉", "☾", "♀", "☿"]
star_sign_ring_1_sym = ["♂", "♃", "♄", "Ꙩ", "♆", "♇"]

star_sign_ring_0_paths = [
    r"images/sun.png",
    r"images/moon.png",
    r"images/venus.png",
    r"images/mercury.png"
]
star_sign_ring_1_paths = [
    r"images/mars.png",
    r"images/jupiter.png",
    r"images/saturn.png",
    r"images/uranus.png",
    r"images/pluto.png",
    r"images/neptune.png"
]


class Card:
    def __init__(
            self,
            num: Optional[int] = None,
            name: str = "UNKNOWN",
            type_: str = "UNKNOWN",
            attribute: str = "UNKNOWN",
            cost: int = 0,
            atk_points: int = 0,
            def_points: int = 0,
            planet_0: str = "UNKNOWN",
            planet_1: str = "UNKNOWN"
    ):
        if num is None:
            num = -next(gen_unknown_ids)
        self.num = num
        self.name = name
        self.type_ = type_
        self.type_simple = "Ritual" if type_ in types_ritual else (
            "Trap" if type_ in types_trap else (
                "Magic" if type_ in types_magic else (
                    "Equip" if type_ in types_equip else "Monster"
                )))
        self.attribute = attribute
        self.cost = cost
        self.atk_points = atk_points
        self.def_points = def_points
        self.planet_0 = planet_0
        self.planet_1 = planet_1

        self.in_play = False
        self._planet = None
        self.face_down = None
        self.attack_mode = None

        self.ring = star_sign_ring_0 if self.planet in star_sign_ring_0 else star_sign_ring_1
        self.ring_sym = star_sign_ring_0_sym if self.ring == star_sign_ring_0 else star_sign_ring_1_sym
        self.ring_path = star_sign_ring_0_paths if self.ring == star_sign_ring_0 else star_sign_ring_1_paths

    def flip_card(self, face_down_in: Optional[bool] = None):
        if face_down_in is None:
            self.face_down = not self.face_down
        else:
            self.face_down = face_down_in

    def toggle_mode(self, mode_in: Optional[bool] = None):
        if mode_in is None:
            self.attack_mode = not self.attack_mode
        else:
            self.attack_mode = mode_in

    def data(self):
        return [
            self.num,
            self.name,
            self.type_,
            self.attribute,
            self.cost,
            self.atk_points,
            self.def_points,
            self.planet_0,
            self.planet_1
        ]

    def get_planet(self):
        return self._planet

    def set_planet(self, planet_in):
        self._planet = planet_in

        self.ring = star_sign_ring_0 if self.planet in star_sign_ring_0 else star_sign_ring_1
        self.ring_sym = star_sign_ring_0_sym if self.ring == star_sign_ring_0 else star_sign_ring_1_sym
        self.ring_path = star_sign_ring_0_paths if self.ring == star_sign_ring_0 else star_sign_ring_1_paths

    def del_planet(self):
        del self._planet

    def to_string(self):
        if self.type_simple == "Monster":
            return f"#{self.num} - {self.name} {self.atk_points}/{self.def_points}"
        else:
            return f"#{self.num} - {self.name} {self.type_simple[0].upper()}"

    def __eq__(self, other):
        return str(self.num) == str(other)
    #
    # def __cmp__(self, other):
    #     return -1 if self.num < other.num else (1 if other.num > self.num else 0)

    def __hash__(self):
        return self.num

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    planet = property(get_planet, set_planet, del_planet)

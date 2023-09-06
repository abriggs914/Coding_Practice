from typing import List

from utility import number_suffix


class Map:
    def __init__(self, name, country, num_floors, colours=None):
        self.name = name
        self.country = country
        self.num_floors = num_floors
        self.colours = colours

    def to_json(self):
        return {
            "name": self.name,
            "country": self.country,
            "num_floors": self.num_floors,
        }

    def __eq__(self, other):
        return isinstance(other, Map) and all([self.name == other.name, self.country == other.country, self.num_floors == other.num_floors])

    def __repr__(self):
        return f"<Map '{self.name}', {self.country}>"


class MapLocation:

    def __init__(self, name: str, base_map: Map, floors: List[int]):
        self.name = name
        self.base_map = base_map
        self.floors = floors  # use zero-index

    def __repr__(self):
        flrs = " and ".join(map(lambda x: f"{x+1}{number_suffix(x+1)}", self.floors))
        # flrs += " Floor"
        # flrs += ("s" if len(self.floors) != 1 else "")
        return f"<MapLocation '{self.name}', FLR(s): {flrs}, Base-Map: '{self.base_map.name}'>"

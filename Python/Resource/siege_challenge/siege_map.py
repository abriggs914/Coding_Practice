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

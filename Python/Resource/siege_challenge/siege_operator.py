
class Operator:
    def __init__(self, name, ctu, atk_def, sex, colours=None, country=None):
        self.name = name
        self.ctu = ctu
        self.atk_def = atk_def
        self.sex = sex
        self.colours = colours
        self.country = country

    def to_json(self):
        return {
            "name": self.name,
            "ctu": self.ctu,
            "sex": self.sex,
            "atk_def": self.atk_def
        }

    def __eq__(self, other):
        return isinstance(other, Operator) and all([self.name == other.name, self.ctu == other.ctu, self.atk_def == other.atk_def])

    def __repr__(self):
        return f"<{('ATK' if self.atk_def == 'attacker' else 'DEF')} Op '{self.name}', {self.ctu}>"

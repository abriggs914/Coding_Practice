class Entity:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def __repr__(self):
        b = self.balance
        return self.name + " < $ " + ("%.2f" % b) + " >"

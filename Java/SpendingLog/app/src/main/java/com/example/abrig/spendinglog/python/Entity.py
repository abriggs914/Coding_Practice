class Entity:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
        self.transactions_list = []

    def add_transaction(self, transaction):
        self.transactions_list.append(transaction)

    def __repr__(self):
        b = self.balance
        return self.name + " < $ " + ("%.2f" % b) + " >"

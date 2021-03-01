from utility import *


class Transaction:
    def __init__(self, amount, entity_from, entity_to, reoccurring_category, transaction_catgory, description, date_in):
        self.amount = amount
        # self.entity_to = entities[entity_to]
        # self.entity_from = entities[entity_from]
        self.entity_to = entity_to
        self.entity_from = entity_from
        self.description = description
        self.reoccurring_category = reoccurring_category
        self.transaction_catgory = transaction_catgory
        self.dates = []
        self.dates.append(date_in)

        self.entity_from.balance -= self.amount
        self.entity_to.balance += self.amount

    def __repr__(self):
        res = ""
        for date in self.dates:
            res += "{d} | $ {a} from: {ef} to {et}".format(d=date, a=self.amount, ef=self.entity_from,
                                                           et=self.entity_to)
        return res

    def info_dict(self):
        d = {
            "Date": self.dates[0],
            "Amount": money(self.amount),
            "To": self.entity_to.name,
            "From": self.entity_from.name,
            "Reoccurring": self.reoccurring_category,
            "Category": self.transaction_catgory,
            "Description": self.description
        }
        # if
        return d
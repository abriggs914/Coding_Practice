from utility import *


TRANSACTION_ID_COUNTER = 0
ENTITY_ID_COUNTER = 0


class Transaction:

    def __init__(self, amount, entity_from, entity_to=None, date=None):
        global TRANSACTION_ID_COUNTER
        TRANSACTION_ID_COUNTER += 1
        self.id = str(TRANSACTION_ID_COUNTER).rjust(2, "0")
        self.amount = amount
        self.entity_from = entity_from
        self.entity_to = entity_to

        if date is None:
            date = dt.datetime.now()
        self.date = date

    def __eq__(self, other):
        return isinstance(other, Entity) and self.id == other.id

    def __repr__(self):
        return "<Transaction #{}: Date: {}, amount: {}, from: \"{}\" to: \"{}\">".format(self.id, self.date, money(self.amount), self.entity_from.name, self.entity_to.name)


class Entity:

    def __init__(self, name, start_balance=0):
        global ENTITY_ID_COUNTER
        ENTITY_ID_COUNTER += 1
        if name == "**POT**":
            name = name.replace("*", "")
            ENTITY_ID_COUNTER = 0
        self.id = str(ENTITY_ID_COUNTER).rjust(2, "0")
        self.name = name
        self.balance = start_balance
        self.transactions_list = []

    def add_transaction(self, transaction):
        self.transactions_list.append(transaction)
        amount = transaction.amount
        if self == transaction.entity_from:
            amount *= -1
        self.balance += amount

    def __eq__(self, other):
        return isinstance(other, Entity) and self.id == other.id

    def __repr__(self):
        return "<Entity #{}: \"{}\", BAL: {}>".format(self.id, self.name, money(self.balance))


class LogBook:

    def __init__(self):
        self.entities_list = []
        self.transactions_list = []

    def add_transaction(self, transaction):
        self.transactions_list.append(transaction)
        entity_from = transaction.entity_from
        entity_to = transaction.entity_to
        if entity_from not in self.entities_list:
            self.entities_list.append(entity_from)
        if entity_to not in self.entities_list:
            self.entities_list.append(entity_to)

        entity_from.add_transaction(transaction)
        entity_to.add_transaction(transaction)

    def create_transaction(self, amount, entity_from, entity_to, date=None):
        self.add_transaction(Transaction(amount, entity_from, entity_to, date))

    def who_pays_who(self):
        # people_to_check = who(name_str)
        people_to_check = self.entities_list
        people_who_pay = [person for person in people_to_check if person["OWES"] > 0]
        people_who_get = [person for person in people_to_check if person["OWES"] < 0]
        print("people_who_pay:", people_who_pay)
        print("people_who_get:", people_who_get)
        first_pass = True
        quitt = 0
        quittt = 8
        pay_pairs = []
        while (people_who_pay and people_who_get) and (first_pass or people_to_check):
            # print("fp:", first_pass, ", people_who_check:", "\n\t" + "\n\t".join(list(map(str, people_to_check))))
            beg_a = len(people_who_pay)
            beg_b = len(people_who_get)
            i, j = 0, 0
            while i < len(people_who_pay):
                person_a = people_who_pay[i]
                j = 0
                while j < len(people_who_get):
                    person_b = people_who_get[j]
                    owe_a = 0 if "OWES" not in person_a else person_a["OWES"]
                    owe_b = 0 if "OWES" not in person_b else person_b["OWES"]
                    # print("1 OWES_a: {}, OWES_b: {}, owe_a + owe_b: {}".format(owe_a, owe_b, owe_a + owe_b), "COND:", (not first_pass and (owe_a >= owe_b and ((owe_a + owe_b) > 0)) and (owe_a < 0 or owe_b < 0)))
                    if owe_a == 0:
                        people_who_pay.remove(person_a)
                        people_to_check.remove(person_a)
                        break
                    if owe_b == 0:
                        people_who_get.remove(person_b)
                        people_to_check.remove(person_b)
                        break
                    if owe_a + owe_b == 0:
                        # A owes what B needs. pay each other, exit pool.
                        pay_pairs.append((owe_a, person_a, person_b))
                        people_who_pay.remove(person_a)
                        people_who_get.remove(person_b)
                        people_to_check.remove(person_a)
                        people_to_check.remove(person_b)
                        # print("\tA removing:", person_a)
                        # print("\tB removing:", person_b)
                        break
                    elif not first_pass and (owe_a >= owe_b and ((owe_a + owe_b) > 0)) and (owe_a < 0 or owe_b < 0):
                        # A has more to pay than B needs
                        pay_pairs.append((abs(owe_b), person_a, person_b))
                        person_a.update({"BAL": person_a["BAL"] + owe_b, "OWES": person_a["OWES"] + owe_b})
                        person_b.update(
                            {"BAL": person_b["BAL"] - owe_a, "OWES": person_b["OWES"] + min(abs(owe_a), abs(owe_b))})
                        # print("2 OWES_a: {}, OWES_b: {}, owe_a + owe_b: {}".format(person_a["OWES"], person_b["OWES"], person_a["OWES"] + person_b["OWES"]))
                        # print("\npeople_who_pay: {}\nperson_a: {}\n".format(people_who_pay, person_a), dict_print(person_b, "REMOVING {}".format(person_b["LET"])))
                        if person_b["OWES"] >= 0:
                            people_who_get.remove(person_b)
                            people_to_check.remove(person_b)
                            # print("\tC removing:", person_b)
                            break
                        elif person_a["OWES"] <= 0:
                            people_who_pay.remove(person_a)
                            people_to_check.remove(person_a)
                            # print("\tD removing:", person_a)
                            break

                    elif len(people_who_get) == 1:
                        pay_pairs.append((owe_a, person_a, person_b))
                        person_b.update({"BAL": person_b["BAL"] - owe_a, "OWES": person_b["OWES"] + owe_a})
                        people_to_check.remove(person_a)
                        people_who_pay.remove(person_a)

                    # else

                    # print("bal_a: {}, bal_b: {}".format(bal_a, bal_b))
                    j += 1
                i += 1
            aft_a = len(people_who_pay)
            aft_b = len(people_who_get)
            sam_a = beg_a == aft_a
            sam_b = beg_b == aft_b
            # print(dict_print({
            #     "beg_a": beg_a,
            #     "aft_a": aft_a,
            #     "beg_b": beg_b,
            #     "aft_b": aft_b,
            #     "sam_a": sam_a,
            #     "sam_b": sam_b,
            #     "first_pass": first_pass,
            #     "quitt": quitt,
            #     "pay_pairs": pay_pairs,
            #     "people_who_pay": people_who_pay,
            #     "people_who_get": people_who_get,
            #     "not sam_a or not sam_b": (not sam_a or not sam_b)
            # }))
            if sam_a and sam_b:
                first_pass = False
            elif first_pass and (not sam_a or not sam_b):
                # print("people_to_check:", people_to_check)
                quitt += 1
                if quitt == quittt:
                    raise ValueError("quitt is {}".format(quittt))
            else:
                first_pass = True

        print("Who pays who:\n{}".format("\n".join([
            dict_print(
                {
                    "Amount": money(pr[0]),
                    "Payer": pr[1]["LET"],
                    "Payee": pr[2]["LET"]
                },
                "{} -> {}".format(pr[1]["LET"], pr[2]["LET"])
            ) for pr in pay_pairs
        ])))

    def __repr__(self):
        return "<LogBook>"


if __name__ == "__main__":
    POT = Entity("**POT**", 0)
    entity_01 = Entity("01", 0)
    transaction_01 = Transaction(10, entity_01, POT)
    logbook = LogBook()
    logbook.add_transaction(transaction_01)

    print(dict_print({
        "Entity_POT": POT,
        "Entity_01": entity_01,
        "Transaction_01": transaction_01,
        "LogBook": logbook
    }, "VALUES"))

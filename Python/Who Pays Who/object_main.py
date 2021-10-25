from utility import *


TRANSACTION_ID_COUNTER = 0
ENTITY_ID_COUNTER = 0


class Transaction:

    def __init__(self, amount, entity_from, entity_to=None, date=None):
        global TRANSACTION_ID_COUNTER
        TRANSACTION_ID_COUNTER += 1
        self.id_num = str(TRANSACTION_ID_COUNTER).rjust(2, "0")
        self.amount = amount
        self.entity_from = entity_from
        self.entity_to = entity_to

        if date is None:
            date = dt.datetime.now()
        self.date = date

    def __eq__(self, other):
        return isinstance(other, Entity) and self.id_num == other.id_num

    def __repr__(self):
        return "<Transaction #{}: Date: {}, amount: {}, from: \"{}\" to: \"{}\">".format(self.id_num, self.date, money(self.amount), self.entity_from.name, self.entity_to.name)


class Entity:

    def __init__(self, name, start_balance=0):
        global ENTITY_ID_COUNTER
        ENTITY_ID_COUNTER += 1
        if name == "**POT**":
            name = name.replace("*", "")
            ENTITY_ID_COUNTER = 0
        self.id_num = str(ENTITY_ID_COUNTER).rjust(2, "0")
        self.name = name
        self.balance = start_balance
        self.spending_balance = 0
        self.earning_balance = 0
        self.transactions_list = []

    def add_transaction(self, transaction):
        self.transactions_list.append(transaction)
        amount = transaction.amount
        if self == transaction.entity_from:
            amount *= -1
            self.spending_balance += amount
        else:
            self.earning_balance += amount
        self.balance += amount

    def info_dict(self):
        return {
            "ID": self.id_num,
            "NAME": self.name,
            "BAL": self.balance,
            "N_T": len(self.transactions_list)
        }

    def __eq__(self, other):
        return isinstance(other, Entity) and self.id_num == other.id_num

    def __repr__(self):
        return "<Entity #{}: \"{}\", BAL: {}>".format(self.id_num, self.name, money(self.balance))


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

    def entity_look_up(self, id_num):
        id_num = str(id_num).rjust(2, "0")
        for ent in self.entities_list:
            if ent.id_num == id_num:
                return ent

    def get_pot_entity(self):
        return self.entity_look_up(0)

    def who_pays_who(self, pot_pays_out=False):
        pot = self.get_pot_entity()
        if pot is None:
            print("No generic \"POT\" entity found.")
            return
        pn = pot.balance / max(1, (len(self.entities_list) - 1))
        people_to_check = [{"ID": p.id_num, "LET": p.name, "BAL": p.balance, "OWES": -1 * (-p.balance - pn)} for p in self.entities_list]

        print(dict_print({i: v for i, v in enumerate(people_to_check)}))

        people_who_pay = [person for person in people_to_check if person["OWES"] > 0]
        people_who_get = [person for person in people_to_check if person["OWES"] < 0]

        print("POT:", pot)

        if not pot_pays_out:
            keeping = []
            for p in people_who_pay:
                if p["ID"] == pot.id_num:
                    continue
                keeping.append(p)
            people_who_pay = keeping


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

        return pay_pairs

    def __repr__(self):
        return "<LogBook>"


if __name__ == "__main__":
    # POT = Entity("**POT**", 0)
    # entity_01 = Entity("01", 0)
    # entity_02 = Entity("02", 0)
    # transaction_01 = Transaction(10, entity_01, POT)
    # transaction_02 = Transaction(100, entity_02, POT)
    # transaction_03 = Transaction(30, entity_01, POT)
    # logbook_1 = LogBook()
    # logbook_1.add_transaction(transaction_01)
    # logbook_1.add_transaction(transaction_02)
    # logbook_1.add_transaction(transaction_03)
    #
    # print(dict_print({
    #     "Entity_POT": POT,
    #     "Entity_01": entity_01,
    #     "Entity_02": entity_02,
    #     "Transaction_01": transaction_01,
    #     "Transaction_02": transaction_02,
    #     "LogBook": logbook_1
    # }, "VALUES"))
    #
    # logbook_1.who_pays_who()

#######################################################################################################################

    # e_pot = Entity("**POT**", 0)
    # e_avery = Entity("Avery", 0)
    # e_kristen = Entity("Kristen", 0)
    # e_emily = Entity("Emily", 0)
    # e_hayley = Entity("Hayley", 0)
    # logbook_2 = LogBook()
    # logbook_2.create_transaction(15, e_avery, e_pot)
    # logbook_2.create_transaction(15, e_kristen, e_pot)
    # logbook_2.create_transaction(40, e_emily, e_pot)
    # logbook_2.create_transaction(20, e_avery, e_pot)
    # logbook_2.create_transaction(50, e_hayley, e_pot)
    # logbook_2.create_transaction(100, e_kristen, e_hayley)
    #
    # print(dict_print({
    #     "e_pot": e_pot,
    #     "e_avery": e_avery,
    #     "e_kristen": e_kristen,
    #     "e_emily": e_emily,
    #     "e_hayley": e_hayley
    # }, "VALUES"))
    #
    # pay_pairs = logbook_2.who_pays_who()
    # for pair in pay_pairs:
    #     amount, p_0, p_1 = pair
    #     entity_from = logbook_2.entity_look_up(p_0["ID"])
    #     entity_to = logbook_2.entity_look_up(p_1["ID"])
    #     print("pair:", pair)
    #     transaction = Transaction(amount, entity_from, entity_to)
    #     print("\tT:", transaction)
    #     logbook_2.add_transaction(transaction)
    #
    # print("Entities:", logbook_2.entities_list)
    # for ent in logbook_2.entities_list:
    #     print(dict_print(ent.info_dict()))

#######################################################################################################################

    e_pot = Entity("**POT**", 0)
    e_avery = Entity("Avery", 0)
    e_kristen = Entity("Kristen", 0)
    e_emily = Entity("Emily", 0)
    e_hayley = Entity("Hayley", 0)
    logbook_3 = LogBook()
    logbook_3.create_transaction(100, e_avery, e_pot)#     Payment("Mother's Day Supper (Wingo's)", "A", "P", 100, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(17.58, e_kristen, e_pot)#     Payment("Mother's Day Supper (Wingo's)", "K", "P", 17.58, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(115.74, e_emily, e_pot)#     Payment("Mother's Day Present ()", "E", "P", 115.74, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(55, e_hayley, e_emily)#     Payment("Hayley paid Emily", "H", "E", 55, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(170.7, e_kristen, e_pot)#     Payment("Father's Day Present (Air Fryer)", "K", "P", 170.7, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(40, e_avery, e_emily)#     Payment("Father's Day Boating", "A", "E", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(50, e_emily, e_pot)#     Payment("Father's Day Boating", "E", "P", 50, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(40, e_hayley, e_pot)#     Payment("Father's Day Boating", "H", "P", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(10, e_emily, e_avery)#     Payment("Father's Day Boating", "E", "A", 10, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(180, e_kristen, e_pot)#     Payment("Spotify", "K", "P", 180, datetime.datetime.strptime("2021-08-04", "%Y-%m-%d")),
    logbook_3.create_transaction(89.99, e_avery, e_pot)#     Payment("Disney+", "A", "P", 89.99, datetime.datetime.strptime("2021-08-04", "%Y-%m-%d"))

    print(dict_print({
        "e_pot": e_pot,
        "e_avery": e_avery,
        "e_kristen": e_kristen,
        "e_emily": e_emily,
        "e_hayley": e_hayley
    }, "VALUES"))

    pay_pairs = logbook_3.who_pays_who()
    for pair in pay_pairs:
        amount, p_0, p_1 = pair
        entity_from = logbook_3.entity_look_up(p_0["ID"])
        entity_to = logbook_3.entity_look_up(p_1["ID"])
        print("pair:", pair)
        transaction = Transaction(amount, entity_from, entity_to)
        print("\tT:", transaction)
        logbook_3.add_transaction(transaction)

    print("Entities:", logbook_3.entities_list)
    for ent in logbook_3.entities_list:
        print(dict_print(ent.info_dict()))


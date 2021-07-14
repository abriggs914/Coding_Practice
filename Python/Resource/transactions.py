from utility import *
import datetime

AVERY = {"LET": "A", "BAL": 0.0}
KRISTEN = {"LET": "K", "BAL": 0.0}
EMILY = {"LET": "E", "BAL": 0.0}
HAYLEY = {"LET": "H", "BAL": 0.0}
MOM = {"LET": "M", "BAL": 0.0}
DAD = {"LET": "D", "BAL": 0.0}
POT = {"LET": "P", "BAL": 0.0}

def who(name_str):
    global AVERY, KRISTEN, EMILY, HAYLEY, MOM, DAD, POT
    payers = []
    for let in name_str:
        if let == AVERY["LET"]:
            payers.append(AVERY)
        elif let == KRISTEN["LET"]:
            payers.append(KRISTEN)
        elif let == EMILY["LET"]:
            payers.append(EMILY)
        elif let == HAYLEY["LET"]:
            payers.append(HAYLEY)
        elif let == MOM["LET"]:
            payers.append(MOM)
        elif let == DAD["LET"]:
            payers.append(DAD)
        elif let == POT["LET"]:
            payers.append(POT)
    return payers

def adjust_owed(name_str):
    res = []
    for let in name_str:
        person = who(let)[0]
        if let != POT["LET"]:
            person.update({"OWED": -person["BAL"]})
        else:
            person.update({"OWED": person["BAL"]})
        res.append(person)
    return res



class Payment:

    def __init__(self, desc, payer, payee, amount, date):
        self.desc = desc
        self.payer = payer
        self.payee = payee
        self.amount = amount
        self.date = date

        payers = who(payer)
        payees = who(payee)
        pay_amount = amount / len(payers)
        get_amount = amount / len(payees)

        for payer in payers:
            payer["BAL"] -= pay_amount
        for payee in payees:
            payee["BAL"] += get_amount

        adjust_owed(self.payer)
        adjust_owed(self.payee)

    def __repr__(self):
        return "{} from {} to {} on {}".format(self.amount, self.payer, self.payee, self.date)


# payments = [
#     Payment("A->H", "A", "H", 15, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
#     Payment("H->K", "H", "K", 20, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
#     Payment("K->A", "K", "A", 20, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d"))
# ]
#
payments = [
    Payment("Mother's Day Supper (Wingo's)", "A", "P", 100, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Mother's Day Supper (Wingo's)", "K", "P", 17.58, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Mother's Day Present ()", "E", "P", 115.74, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Hayley paid Emily", "H", "E", 55, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Father's Day Present", "K", "P", 170.7, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Father's Day Boating", "A", "E", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Father's Day Boating", "E", "P", 50, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Father's Day Boating", "H", "P", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Father's Day Boating", "E", "A", 10, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
]
# payments = [
#     Payment("Mother's Day Supper (Wingo's)", "AK", "P", 100, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d"))
# ]

for payer in "AKEHMDP":
    person = who(payer)[0]
    print("Payer: {}\n{}".format(payer, dict_print(person, "Person")))

def who_pays_who(name_str):
    people_to_check = who(name_str)
    people_who_pay = [person for person in people_to_check if person["BAL"] > 0]
    people_who_get = [person for person in people_to_check if person["BAL"] < 0]
    print("people_who_pay:", people_who_pay)
    print("people_who_get:", people_who_get)
    first_pass = True
    quitt = 0
    quittt = 8
    pay_pairs = []
    while (people_who_pay and people_who_get) and (first_pass or people_to_check):
        beg_a = len(people_who_pay)
        beg_b = len(people_who_get)
        i, j = 0, 0
        while i < len(people_who_pay):
            person_a = people_who_pay[i]
            while j < len(people_who_get):
                person_b = people_who_get[j]
                bal_a = person_a["BAL"]
                bal_b = person_b["BAL"]
                owe_a = person_a["OWED"]
                owe_b = person_b["OWED"]
                if bal_a == owe_b:
                    pay_pairs.append((bal_a, person_a, person_b))
                    people_who_pay.remove(person_a)
                    people_who_get.remove(person_b)
                    people_to_check.remove(person_a)
                    people_to_check.remove(person_b)
                elif not first_pass and bal_a > owe_b:
                    pay_pairs.append((owe_b, person_a, person_b))
                    people_who_get.remove(person_b)
                    people_to_check.remove(person_b)
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

    print("Who pays who:\n{}".format("\n".join([str(pr) for pr in pay_pairs])))

who_pays_who("AKEHP")

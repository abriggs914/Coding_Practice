from utility import *
import datetime

AVERY = {"LET": "A", "BAL": 0.0, "OWES": 0.0, "PMTS": []}
KRISTEN = {"LET": "K", "BAL": 0.0, "OWES": 0.0, "PMTS": []}
EMILY = {"LET": "E", "BAL": 0.0, "OWES": 0.0, "PMTS": []}
HAYLEY = {"LET": "H", "BAL": 0.0, "OWES": 0.0, "PMTS": []}
MOM = {"LET": "M", "BAL": 0.0, "OWES": 0.0, "PMTS": []}
DAD = {"LET": "D", "BAL": 0.0, "OWES": 0.0, "PMTS": []}
POT = {"LET": "P", "BAL": 0.0, "OWES": 0.0, "PMTS": []}

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

def adjust_OWES(name_str):
    res = []
    for let in name_str:
        person = who(let)[0]
        if let != POT["LET"]:
            # person.update({"OWES": -person["BAL"]})
            person.update({"OWES": person["BAL"]})
        else:
            person.update({"OWES": person["BAL"]})
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
            payer["PMTS"].append(self)
        for payee in payees:
            payee["BAL"] += get_amount
            payee["PMTS"].append(self)

    def __repr__(self):
        return "{} from {} to {} on {}".format(self.amount, self.payer, self.payee, self.date)


# payments = [
#     Payment("A->P", "A", "P", 100, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
#     Payment("H->P", "H", "P", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
#     Payment("K->P", "K", "P", 10, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d"))
# ]

# payments = [
#     Payment("A->P", "A", "P", 100, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
#     Payment("H->P", "H", "P", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
#     Payment("K->P", "K", "P", 10, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
#     Payment("K->A", "K", "A", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d"))
# ]
#
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
    Payment("Father's Day Present (Air Fryer)", "K", "P", 170.7, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Father's Day Boating", "A", "E", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Father's Day Boating", "E", "P", 50, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Father's Day Boating", "H", "P", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Father's Day Boating", "E", "A", 10, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    Payment("Spotify", "K", "P", 180, datetime.datetime.strptime("2021-08-04", "%Y-%m-%d")),
    Payment("Disney+", "A", "P", 89.99, datetime.datetime.strptime("2021-08-04", "%Y-%m-%d"))
]
#
# payments = [
#     Payment("Mother's Day Supper (Wingo's)", "AK", "P", 100, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d"))
# ]
#
# payments = [
#     Payment("T", "A", "P", 10, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
#     Payment("T", "K", "P", 100, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
#     Payment("T", "A", "P", 30, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d"))
# ]
#
owe_val = 0
payments_to_pot = []
transactors = []
for payment in payments:
    people = who(payment.payer) + who(payment.payee)
    transactors += [p for p in people if p not in transactors and p != POT]
    if payment.payee == POT["LET"]:
        payments_to_pot.append(payment)
        owe_val += payment.amount / len(payment.payer)
owe_val /= max(1, len(payments_to_pot))
share = (owe_val * max(1, len(payments_to_pot))) / max(1, len(transactors))
print("owe_val:{}, over {} transactions to the pot.".format(owe_val, len(payments_to_pot)))
print("Share: {}, over {} transactors.".format(share, len(transactors)))

for payer in "AKEHMD":
    person = who(payer)[0]
    if person["PMTS"]:
        person["OWES"] = share + person["BAL"]
    else:
        person["OWES"] = 0
    print("Payer: {}\n{}".format(payer, dict_print(person, "Person")))

# POT["OWES"] = -POT["BAL"]
POT["OWES"] = POT["BAL"]
print("Payer: {}\n{}".format(POT["LET"], dict_print(POT, "Person")))


def who_pays_who(name_str):
    people_to_check = who(name_str)
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
                    person_b.update({"BAL": person_b["BAL"] - owe_a, "OWES": person_b["OWES"] + min(abs(owe_a), abs(owe_b))})
                    # print("2 OWES_a: {}, OWES_b: {}, owe_a + owe_b: {}".format(person_a["OWES"], person_b["OWES"], person_a["OWES"] + person_b["OWES"]))
                    #print("\npeople_who_pay: {}\nperson_a: {}\n".format(people_who_pay, person_a), dict_print(person_b, "REMOVING {}".format(person_b["LET"])))
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

#
# def who_pays_who(name_str):
#     people_to_check = who(name_str)
#     people_who_pay = [person for person in people_to_check if person["BAL"] > 0]
#     people_who_get = [person for person in people_to_check if person["BAL"] < 0]
#     print("people_who_pay:", people_who_pay)
#     print("people_who_get:", people_who_get)
#     first_pass = True
#     quitt = 0
#     quittt = 8
#     pay_pairs = []
#     while (people_who_pay and people_who_get) and (first_pass or people_to_check):
#         beg_a = len(people_who_pay)
#         beg_b = len(people_who_get)
#         i, j = 0, 0
#         while i < len(people_who_pay):
#             person_a = people_who_pay[i]
#             while j < len(people_who_get):
#                 person_b = people_who_get[j]
#                 bal_a = person_a["BAL"]
#                 bal_b = person_b["BAL"]
#                 owe_a = 0 if "OWES" not in person_a else person_a["OWES"]
#                 owe_b = 0 if "OWES" not in person_b else person_b["OWES"]
#                 if bal_a == owe_b:
#                     pay_pairs.append((bal_a, person_a, person_b))
#                     people_who_pay.remove(person_a)
#                     people_who_get.remove(person_b)
#                     people_to_check.remove(person_a)
#                     people_to_check.remove(person_b)
#                 elif not first_pass and bal_a > owe_b:
#                     pay_pairs.append((owe_b, person_a, person_b))
#                     person_a["BAL"] -= owe_b
#                     people_who_get.remove(person_b)
#                     people_to_check.remove(person_b)
#                 # else
#
#                 # print("bal_a: {}, bal_b: {}".format(bal_a, bal_b))
#                 j += 1
#             i += 1
#         aft_a = len(people_who_pay)
#         aft_b = len(people_who_get)
#         sam_a = beg_a == aft_a
#         sam_b = beg_b == aft_b
#         # print(dict_print({
#         #     "beg_a": beg_a,
#         #     "aft_a": aft_a,
#         #     "beg_b": beg_b,
#         #     "aft_b": aft_b,
#         #     "sam_a": sam_a,
#         #     "sam_b": sam_b,
#         #     "first_pass": first_pass,
#         #     "quitt": quitt,
#         #     "pay_pairs": pay_pairs,
#         #     "people_who_pay": people_who_pay,
#         #     "people_who_get": people_who_get,
#         #     "not sam_a or not sam_b": (not sam_a or not sam_b)
#         # }))
#         if sam_a and sam_b:
#             first_pass = False
#         elif first_pass and (not sam_a or not sam_b):
#             # print("people_to_check:", people_to_check)
#             quitt += 1
#             if quitt == quittt:
#                 raise ValueError("quitt is {}".format(quittt))
#         else:
#             first_pass = True
#
#     print("Who pays who:\n{}".format("\n".join([str(pr) for pr in pay_pairs])))

# who_pays_who("AKEHP")
who_pays_who("AKEH")

from Transaction import Transaction
from Entity import Entity
from utility import *

# pname	-	plural name "annual spending / weekly spending"
PRINT = False

REOCCURRING = {
    "Once": {
        "pname": "Once",
        "ratio_to_annual": 1,
        "ratio_from_annual": 1,
        "occur_annual": 1,
        "occur_lifetime": 1
    },
    "Per second": {
        "pname": "Per second",
        "ratio_to_annual": 31536000,
        "ratio_from_annual": 1 / 31536000,
        "occur_annual": 31536000,
        "occur_lifetime": float("inf"),
    },
    "Per minute": {
        "pname": "Per minute",
        "ratio_to_annual": 525600,
        "ratio_from_annual": 1 / 525600,
        "occur_annual": 525600,
        "occur_lifetime": float("inf"),
    },
    "Hourly": {
        "pname": "Hourly",
        "ratio_to_annual": 8760,
        "ratio_from_annual": 1 / 8760,
        "occur_annual": 8760,
        "occur_lifetime": float("inf"),
    },
    "Daily": {
        "pname": "Daily",
        "ratio_to_annual": 365,
        "ratio_from_annual": 1 / 365,
        "occur_annual": 365,
        "occur_lifetime": float("inf"),
    },
    "Weekly": {
        "pname": "Weekly",
        "ratio_to_annual": 52,
        "ratio_from_annual": 1 / 52,
        "occur_annual": 52,
        "occur_lifetime": float("inf")
    },
    "Monthly": {
        "pname": "Monthly",
        "ratio_to_annual": 12,
        "ratio_from_annual": 1 / 12,
        "occur_annual": 12,
        "occur_lifetime": float("inf")
    },
    "Quarterly": {
        "pname": "Quarterly",
        "ratio_to_annual": 4,
        "ratio_from_annual": 1 / 4,
        "occur_annual": 4,
        "occur_lifetime": float("inf")
    },
    "Annually": {
        "pname": "Annual",
        "ratio_to_annual": 1,
        "ratio_from_annual": 1,
        "occur_annual": 1,
        "occur_lifetime": float("inf")
    }
}

TRANSACTION = {
    "Gas": 0,
    "Rent": 1,
    "Pay": 2,
    "Entertainment": 3,
    "Learning": 4
}


class TransactionHandler:

    def __init__(self):
        self.transaction_list = []
        self.entities_list = [Entity("Me")]
        self.first_date = None
        self.last_date = None

    def create_transaction(self, amount, entity_from, entity_to, reoccurring_category, transaction_catgory, description,
                           date_in):

        # TODO fix this
        et, ef = -1, -1
        for i, entity in enumerate(self.entities_list):
            # print("entity in: te: <{te}> <{e}, ten: {ten}> ".format(te=type(entity), e=entity.name, ten=type(entity.name)))
            # print("entity_to: te: <{te}> <{e}> ".format(te=type(entity_to), e=entity_to.name))
            if same_entity(entity.name.lower(), entity_to.name.lower()):
                entity_to = entity
                et = i
            if same_entity(entity.name.lower(), entity_from.name.lower()):
                entity_from = entity
                ef = i
        if et < 0:
            self.entities_list.append(entity_to)
        if ef < 0:
            self.entities_list.append(entity_from)
        transaction = Transaction(amount, entity_from, entity_to, reoccurring_category, transaction_catgory,
                                  description, date_in)
        entity_to.add_transaction(transaction)
        entity_from.add_transaction(transaction)
        # self.add_transaction(transaction)
        return transaction

    def costing(self, transaction, period):
        toa = REOCCURRING[transaction.reoccurring_category]["occur_annual"]
        tra = REOCCURRING[transaction.reoccurring_category]["ratio_to_annual"]
        pra = REOCCURRING[period]["ratio_from_annual"]
        a = transaction.amount
        # print("a: {a}, toa: {toa}, tra: {tra}, pra: {pra}".format(a=a, toa=toa, tra=tra, pra=pra))
        return a * toa * pra

        # Using a starting entity, produce a report on transactions
        # for a given period, and / or over a predetermined list of
        # transactions.
        # Usage: TH.costing_report(Entity("Me"), "Daily", None, )
    def costing_report(self, entity, period, transaction=None, n=1):
        res = "{p} costing report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity, n=n)
        er = self.earning_report(entity, period, transaction, n)
        sr = self.spending_report(entity, period, transaction, n)
        er = float(er.split()[-1].strip())
        sr = float(sr.split()[-1].strip())
        total_cost = er - sr
        res += "total cost {tc}".format(tc=total_cost)
        return res

        # # entity = entities[entity]
        # if type(entity) != Entity:
        #     entity = self.get_entity(entity)
        # res = "{p} costing report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity, n=n)
        # if transaction is not None:
        #     if entity not in [transaction.entity_to, transaction.entity_from]:
        #         return "Transaction <{t}>\ndoes not effect {e}".format(t=transaction, e=entity)
        #     x = min(REOCCURRING[transaction.reoccurring_category]["occur_lifetime"], n)
        #     cost = self.costing(transaction, period) * x
        #     if transaction.entity_from == entity:
        #         cost *= -1
        #     res += "$ %.2f" % cost
        #     return res
        # total_cost = 0
        # for transaction in self.transaction_list:
        #     # print("transaction:", transaction)
        #     if entity in [transaction.entity_to, transaction.entity_from]:
        #         if transaction.reoccurring_category != "Once":
        #             print("\ttransaction.reoccurring_category != \"Once\"",
        #                   (transaction.reoccurring_category != "Once"))
        #             print("\t-entity", entity)
        #             print("\t-entity_to", transaction.entity_to)
        #             print("\t-entity_from", transaction.entity_from)
        #             cost = self.costing(transaction, period) * n
        #             if transaction.entity_from == entity:
        #                 cost *= -1
        #             total_cost += cost
        #         else:
        #             cost = transaction.amount
        #             cost = self.costing(transaction, period) * n
        #             if transaction.entity_from == entity:
        #                 cost *= -1
        #             total_cost += cost
        # res += "total cost {tc}".format(tc=total_cost)
        # return res

    def earning_report(self, entity, period, transaction=None, n=1):
        # entity = entities[entity]
        if type(entity) != Entity:
            entity = self.get_entity(entity)
        res = "{p} earning report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity, n=n)
        if transaction is not None:
            if entity != transaction.entity_to:
                return "Transaction <{t}>\ndoes not effect {e}".format(t=transaction, e=entity)
            x = min(REOCCURRING[transaction.reoccurring_categoy]["occur_lifetime"], n)
            cost = self.costing(transaction, period) * x
            res += "$ %.2f" % cost
            return res
        total_cost = 0
        for transaction in self.transaction_list:
            if entity == transaction.entity_to:
                if transaction.reoccurring_category != "Once":
                        x = min(REOCCURRING[transaction.reoccurring_category]["occur_lifetime"], n)
                        cost = self.costing(transaction, period) * x
                        total_cost += cost
                else:
                    # total_cost += transaction.amount
                    total_cost += self.costing(transaction, period) * n
        res += "total earnings {tc}".format(tc=total_cost)
        return res

    def spending_report(self, entity, period, transaction=None, n=1):
        # entity = entities[entity]
        if type(entity) != Entity:
            entity = self.get_entity(entity)
        res = "{p} spending report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity,
                                                                       n=n)
        if transaction is not None:
            if entity != transaction.entity_from:
                return "Transaction <{t}>\ndoes not effect {e}".format(t=transaction, e=entity)
            x = min(REOCCURRING[transaction.reoccurring_categoy]["occur_lifetime"], n)
            cost = self.costing(transaction, period) * x
            res += "$ %.2f" % cost
            return res
        total_cost = 0
        for transaction in self.transaction_list:
            # print("spending total cost:", total_cost)
            if entity == transaction.entity_from:
                if transaction.reoccurring_category != "Once":
                    x = min(REOCCURRING[transaction.reoccurring_category]["occur_lifetime"], n)
                    cost = self.costing(transaction, period) * x
                    total_cost += cost
                else:
                    # total_cost += transaction.amount
                    total_cost += self.costing(transaction, period) * n
            res += "total spendings {tc}".format(tc=total_cost)
        return res
    # # Using a starting entity, produce a report on transactions
    # # for a given period, and / or over a predetermined list of
    # # transactions.
    # # Usage: TH.costing_report(Entity("Me"), "Daily", None, )
    # def costing_report(self, entity, period, transaction=None, n=1):
    #     # entity = entities[entity]
    #     if type(entity) != Entity:
    #         entity = self.get_entity(entity)
    #     res = "{p} costing report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity, n=n)
    #     if transaction is not None:
    #         if entity not in [transaction.entity_to, transaction.entity_from]:
    #             return "Transaction <{t}>\ndoes not effect {e}".format(t=transaction, e=entity)
    #         x = min(REOCCURRING[transaction.reoccurring_category]["occur_lifetime"], n)
    #         cost = self.costing(transaction, period) * x
    #         if transaction.entity_from == entity:
    #             cost *= -1
    #         res += "$ %.2f" % cost
    #         return res
    #
    #     total_cost = 0
    #     for transaction in self.transaction_list:
    #         # print("transaction:", transaction)
    #         if transaction.reoccurring_category != "Once" or 1:
    #             print("\ttransaction.reoccurring_category != \"Once\"", (transaction.reoccurring_category != "Once"))
    #             print("\t-entity", entity)
    #             print("\t-entity_to", transaction.entity_to)
    #             print("\t-entity_from", transaction.entity_from)
    #             if entity in [transaction.entity_to, transaction.entity_from]:
    #                 print("\t\tentity in [transaction.entity_to, transaction.entity_from]",
    #                       (entity in [transaction.entity_to, transaction.entity_from]))
    #                 cost = self.costing(transaction, period) * n
    #                 if transaction.entity_from == entity:
    #                     cost *= -1
    #                 total_cost += cost
    #     res += "total cost {tc}".format(tc=total_cost)
    #     return res
    #
    # def earning_report(self, entity, period, transaction=None, n=1):
    #     # entity = entities[entity]
    #     if type(entity) != Entity:
    #         entity = self.get_entity(entity)
    #     res = "{p} earning report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity, n=n)
    #     if transaction is not None:
    #         if entity != transaction.entity_to:
    #             return "Transaction <{t}>\ndoes not effect {e}".format(t=transaction, e=entity)
    #         x = min(REOCCURRING[transaction.reoccurring_categoy]["occur_lifetime"], n)
    #         cost = self.costing(transaction, period) * x
    #         res += "$ %.2f" % cost
    #         return res
    #
    #     total_cost = 0
    #     for transaction in self.transaction_list:
    #         if transaction.reoccurring_category != "Once" or 1:
    #             if entity == transaction.entity_to:
    #                 x = min(REOCCURRING[transaction.reoccurring_category]["occur_lifetime"], n)
    #                 cost = self.costing(transaction, period) * x
    #                 total_cost += cost
    #     res += "total earnings {tc}".format(tc=total_cost)
    #     return res
    #
    # def spending_report(self, entity, period, transaction=None, n=1):
    #     # entity = entities[entity]
    #     if type(entity) != Entity:
    #         entity = self.get_entity(entity)
    #     res = "{p} spending report for {e}\nNum periods: {n}\n".format(p=REOCCURRING[period]["pname"], e=entity, n=n)
    #     if transaction is not None:
    #         if entity != transaction.entity_from:
    #             return "Transaction <{t}>\ndoes not effect {e}".format(t=transaction, e=entity)
    #         x = min(REOCCURRING[transaction.reoccurring_categoy]["occur_lifetime"], n)
    #         cost = self.costing(transaction, period) * x
    #         res += "$ %.2f" % cost
    #         return res
    #
    #     total_cost = 0
    #     for transaction in self.transaction_list:
    #         print("spending total cost:", total_cost)
    #         if transaction.reoccurring_category != "Once" or 1:
    #             if entity == transaction.entity_from:
    #                 x = min(REOCCURRING[transaction.reoccurring_category]["occur_lifetime"], n)
    #                 cost = self.costing(transaction, period) * x
    #                 total_cost += cost
    #     res += "total spendings {tc}".format(tc=total_cost)
    #     return res

    def average_debit(self, entity):
        m = [0, 0]
        for t in self.transaction_list:
            if t.entity_from == entity:
                m[0] += t.amount
                m[1] += 1
        return m[0] / m[1]

    def average_credit(self, entity):
        m = [0, 0]
        for t in self.transaction_list:
            if t.entity_to == entity:
                m[0] += t.amount
                m[1] += 1
        return m[0] / m[1]

    def highest_debit(self, entity):
        m = 0, None
        for t in self.transaction_list:
            if t.entity_from == entity:
                if t.amount > m[0]:
                    m = t.amount, t.dates[0]
        return m

    def highest_credit(self, entity):
        m = 0, None
        for t in self.transaction_list:
            if t.entity_to == entity:
                if t.amount > m[0]:
                    m = t.amount, t.dates[0]
        return m

    def lowest_debit(self, entity):
        m = float("inf"), None
        for t in self.transaction_list:
            if t.entity_from == entity:
                if t.amount < m[0]:
                    m = t.amount, t.dates[0]
        return m

    def lowest_credit(self, entity):
        m = float("inf"), None
        for t in self.transaction_list:
            if t.entity_to == entity:
                if t.amount < m[0]:
                    m = t.amount, t.dates[0]
        return m

    def add_transaction(self, transaction):
        self.transaction_list.append(transaction)

        # print("DATES", transaction.dates)
        if self.first_date is None or transaction.dates[0] < self.first_date:
            self.first_date = transaction.dates[0]
        if self.last_date is None or transaction.dates[0] > self.last_date:
            self.last_date = transaction.dates[0]

        if transaction.entity_to not in self.entities_list:
            self.entities_list.append(transaction.entity_to)
        if transaction.entity_from not in self.entities_list:
            self.entities_list.append(transaction.entity_from)

    def get_entity(self, name):
        for entity in self.entities_list:
            if entity.name.lower() == name.lower():
                return entity

    # def


def unclutter(txt):
    global PRINT
    m = "IN: <" + str(txt) + ">"
    ignore = ["fpos", "opos", "store", "stock", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "=", "+",
              "{", "}", "[", "]", "?", "/", "<", ">", ":", ";", "'", "`", "~", ",", "."] + [str(i) for i in range(10)]
    i, j = 0, 0
    res = ""
    while i < len(txt):
        if PRINT:
            print("\n\n")
        found = None
        for val in ignore:
            end = i + len(val)
            if PRINT:
                print("val.lower(): {vl}\ntxt[i: end].lower(): {tie}\nend: {e}".format(vl=val.lower(),
                                                                                       tie=txt[i: end].lower(), e=end))
            if val.lower() == txt[i: end].lower():
                found = val
                # i += len(val)
                break

        if found is None:
            res += txt[i]
        else:
            i += len(found)
        i += 1

    # for val in ignore:
    # 	txt = txt.replace(val, "")
    # txt = txt.strip()
    # m += "     OUT: <" + str(txt) + ">"
    txt = res.strip()
    spl = txt.split()
    txt = " ".join([x.strip() for x in spl if len(x) > 1])
    m += "     OUT: <" + str(txt) + ">"
    if PRINT:
        print(m)
    return txt


def num_matching_words(txt_1, txt_2):
    global PRINT
    spl_1 = txt_1.split()
    spl_2 = txt_2.split()
    spl_1.sort()
    spl_2.sort()
    i, j = 0, 0
    p, q = len(spl_1), len(spl_2)
    matching_words = [None for m in range(p * q)]
    edit_distances = [None for m in range(p * q)]
    word_lengths = [lenstr(word) for word in spl_1 + spl_2]
    avg_word_len = avg(word_lengths)

    if PRINT:
        print(dict_print({
            "txt_1": txt_1,
            "txt_2": txt_2,
            "spl_1": spl_1,
            "spl_2": spl_2,
            "p": p,
            "q": q,
        },
            "matching words"
        ))

    while i < p:
        j = 0
        while j < q:
            word_1 = spl_1[i]
            word_2 = spl_2[j]
            m = compute_min_edit_distance(word_1, word_2)
            if PRINT:
                print("({i}, {j}) => (i*q)+j: {ij}".format(i=i, j=j, ij=(i * q) + j))
            edit_distances[(i * q) + j] = m
            matching_words[(i * q) + j] = word_1 if m == 0 else matching_words[(i * q) + j]
            j += 1
        # if m == 0:
        # 	break
        i += 1

    avg_word_len = avg(word_lengths)
    avg_edit_dist = avg(edit_distances)

    if PRINT:
        print(
            "matching words: <{amw}>:\n{mw}\nedit distances: <{aed}>\n{ed}".format(mw=matching_words, ed=edit_distances,
                                                                                   amw=avg_word_len, aed=avg_edit_dist))
    return matching_words


# same len - could be a coincidence if the strings don't already match
# matching word score - unreliable for few words
# balance the edit distance (score-wise)
# in the unmatched words, is the edit distance good?

def same_entity(entity_1, entity_2, tol=2):
    entity_1 = unclutter(entity_1)
    entity_2 = unclutter(entity_2)
    if all([type(e) == Entity for e in [entity_1, entity_2]]):
        if entity_1 == entity_2:
            return True
    elif all([type(e) == str for e in [entity_1, entity_2]]):
        if entity_1.lower() == entity_2.lower():
            return True
        else:
            m = compute_min_edit_distance(entity_1, entity_2)
            # print("m: {m}".format(m=m))
            if m <= tol:
                return True
            mw = num_matching_words(entity_1, entity_2)
    return False

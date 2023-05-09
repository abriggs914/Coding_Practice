import datetime
import tkinter

from tkinter_utility import button_factory


class Transaction:
    def __init__(self, amount, e_from, e_to=None, description="N/A", date_in=None):
        self.amount = amount
        self.e_from = e_from
        self.e_to = e_to
        self.description = description
        self.date_in = date_in
        self.square = False

    def __repr__(self):
        return f"<Transaction $ {self.amount:.2f} from {len(self.e_from)} to {len(self.e_to)}>"


class Entity:
    def __init__(self, name, start_balance=0):
        self.name = name
        self.start_balance = start_balance
        self.balance = start_balance
        self.transactions = list()

    def copy(self):
        ent = Entity(self.name)
        ent.start_balance = self.start_balance
        ent.balance = self.balance
        ent.transactions = [trans for trans in self.transactions]
        return ent

    def __repr__(self):
        return f"<Entity '{self.name}': $ {self.balance:.2f}>"


class TransactionSplit:
    def __init__(self):
        self.entities = set()
        self.transactions = set()

    def entity_lookup(self, entity):
        if entity is None or entity == POT or entity.lower() == "pot":
            entity = POT
        else:
            for ent in self.entities:
                if entity == ent.name:
                    entity = ent
                    break
            if isinstance(entity, str):
                entity = Entity(entity)
        self.entities.add(entity)
        return entity

    def add_transaction(self, amount, e_from, e_to=None, description="N/A", date_in=None):
        if not isinstance(e_from, list) and not isinstance(e_from, tuple):
            e_from = [e_from]
        if not isinstance(e_to, list) and not isinstance(e_to, tuple):
            e_to = [e_to]

        e_from = [self.entity_lookup(e) for e in e_from]
        e_to = [self.entity_lookup(e) for e in e_to]

        pay_amount = -1 * amount / len(e_from)
        rec_amount = amount / len(e_to)

        transaction = Transaction(amount, e_from, e_to, description, date_in)

        for ent in e_from:
            ent.balance += pay_amount
            ent.transactions.append(transaction)

        for ent in e_to:
            ent.balance += rec_amount
            ent.transactions.append(transaction)

        self.transactions.add(transaction)

    def split(self, entites=None):
        # pot = self.entity_lookup("pot")
        if entites is None:
            entites = [ent.copy() for ent in self.entities]
        else:
            temp = []
            for ent in entites:
                temp.append(ent.copy())
            entites = temp

        results = []
        # open_transactions = [trans for trans in self.transactions if not trans.square and (POT in trans.e_to)]
        open_transactions = [trans for trans in self.transactions if not trans.square]
        outstanding = sum([trans.amount for trans in open_transactions if POT in trans.e_to])
        equal_share = outstanding / (len(entites) - (0 if POT in entites else 1))
        owed = {}
        owes = {}
        for trans in open_transactions:
            amount = trans.amount
            pay = trans.e_from
            rec = trans.e_to
            eq_share = -1 * amount / len(pay)
            eq_pay = amount / len(rec)
            # print(f"\n\t{amount=}\n\t{pay=}\n\t{rec=}\n\t{eq_share=}\n\t{eq_pay=}")
            for ent in pay:
                if ent == POT:
                    continue
                if ent not in owed:
                    owed.update({ent: 0})
                owed[ent] += eq_share
            # print(f"{owed=}")
            for ent in rec:
                if ent == POT:
                    continue
                if ent not in owes:
                    owes.update({ent: 0})
                if POT not in pay:
                    for e2 in pay:
                        t = owed[e2]
                        # print(f"\t\t{t=}, {ent=}, {e2=}, {owes[ent]=}, {owed[e2]=}")
                        if ent not in owed:
                            owed[ent] = 0
                        owed[ent] -= t
                        del owes[ent]

                else:
                    owes[ent] += eq_pay

        owed_to_remove = []
        for ent, amount in owed.items():
            if -1 * amount >= equal_share:
                owed[ent] = amount + equal_share
            else:
                owed_to_remove.append(ent)
        # print(f"{owed_to_remove=}")
        for ent in owed_to_remove:
            # print(f"{owed[ent]=}")
            if (-1 * owed[ent]) > equal_share:
                owed[ent] -= equal_share
            else:
                if ent not in owes:
                    owes[ent] = 0
                owes[ent] += owed[ent] + equal_share
                del owed[ent]

        # transactions = "\n".join(str(t) for t in open_transactions)
        owes = {k: abs(v) for k, v in owes.items()}
        owed = {k: abs(v) for k, v in owed.items()}
        # print(f"\n\n\tBefore\n{equal_share=}\n{owed=}\n{owes=}\n{outstanding=}")

        block = "#" * 120

        for p1, amount_owed in owed.items():
            for p2, amount_owes in owes.items():
                # print(f"{block}\n{p1=}, {p2=}, {amount_owed=}, {amount_owes=}")
                if amount_owes != 0 and amount_owed != 0:
                    if amount_owes <= amount_owed:
                        # print(f"\tT {p2} pays {p1} {amount_owes}")
                        # results.append((p2, p1, amount_owes))
                        # print(f"\tT {p2} pays {p1} {amount_owes}")
                        results.append((p2, p1, amount_owes))
                        owed[p1] -= amount_owes
                        owes[p2] = 0
                    else:
                        # print(f"\tB {p2} pays {p1} {amount_owed}")
                        results.append((p2, p1, amount_owed))
                        owes[p2] -= amount_owed
                        owed[p1] = 0

                # print(f"\n\tIN\n{owed=}\n{owes=}\n")
                if owed[p1] == 0:
                    break

        # print(transactions)
        # print(f"\n\n\n\n\n")

        # iig = 0
        # while (len(owed) + len(owes)) > 0:
        #
        #     print(f"\n\tA {iig}\n{equal_share=}\n{owed=}\n{owes=}")
        #     owed_to_remove = []
        #     for p_ent, p_amount in owed.items():
        #         # diff = -1 * (equal_share + p_amount)
        #         diff = None
        #         owes_to_remove = []
        #         for r_ent, r_amount in owes.items():
        #
        #             # print(f"\n\tC\n{equal_share=}\n{owed=}\n{owes=}")
        #             # print(f"{r_amount=}, {p_amount=}, {diff=}")
        #             if (p_amount * -1) == r_amount:
        #                 # print(f"XXA")
        #                 results.append((r_ent, p_ent, p_amount))
        #                 owed[p_ent] = 0
        #                 owes[r_ent] = 0
        #             elif r_amount >= p_amount:
        #                 # print(f"XXB")
        #                 x = min(r_amount, (0 - p_amount))
        #                 p_amount = p_amount + x
        #                 results.append((r_ent, p_ent, abs(x)))
        #                 owed[p_ent] = p_amount
        #                 owes[r_ent] -= x
        #
        #             if (0 - TOL) <= owes[r_ent] <= (0 + TOL):
        #                 owes_to_remove.append(r_ent)
        #             # print(f"\n\tD\n{equal_share=}\n{owed=}\n{owes=}")
        #
        #         if (0 - TOL) <= owed[p_ent] <= (0 + TOL):
        #             owed_to_remove.append(p_ent)
        #
        #         for ent in owes_to_remove:
        #             del owes[ent]
        #
        #     for ent in owed_to_remove:
        #         del owed[ent]
        #
        #     print(f"\n\tB {iig}\n{equal_share=}\n{owed=}\n{owes=}")
        #
        #     iig += 1
        #     if iig == 5:
        #         quit()

        # print(f"\n\n\tAfter\n{equal_share=}\n{owed=}\n{owes=}\n{outstanding=}")

        print(f"\n\nPAYMENTS")
        for p_ent, r_ent, amount in results:
            print(f"{p_ent} pays {amount=} to {r_ent}")

        # outstanding = sum([trans.amount for trans in self.transactions])
        # equal_share = outstanding / len(entites)
        # while outstanding != 0:
        #     print(f"{outstanding=}")
        #     for trans in open_transactions:
        #         amount = trans.amount
        #         pay = trans.e_from
        #         rec = trans.e_to
        #         eq_share = amount / len(pay)
        #         for ent in pay:
        #             if amount !=
        #         print(f"\t{amount=}\n\t{pay=}\n\t{rec=}")
        #     outstanding *= 0


POT = Entity("POT")
TOL = 1e-7


class TkSplitMenu(tkinter.Tk):

    ent_gener = (i for i in range(10000))

    class Entity:

        def __init__(self, tag, name=None, start_balance=0):
            id_number = next(TkSplitMenu.ent_gener)
            idn = f"00000{id_number}"[-5:]
            if name is None:
                name = f"entity_{idn}"
            self.name = name
            self.id_number = id_number
            self.id_number_s = idn
            self.tag = tag
            self.start_balance = start_balance
            self.balance = self.start_balance

        def __repr__(self):
            return f"<Ent {self.name}>"

    def __init__(self):
        super().__init__()
        self.entities = []
        self.transactions = []

        self.data = dict()
        self.data["canvas_width"] = 500
        self.data["canvas_height"] = 500
        self.data["canvas_background"] = "#505050"

        self.data["width_entity"] = 80
        self.data["fill_entity"] = "#DCDCDC"
        self.data["outline_entity"] = "#000000"
        self.data["outline_width_entity"] = 1

        r, c, rs, cs, ix, iy, px, py, s = self.grid_keys()
        self.grid_args = {
            "top_frame": {r: 0, c: 0, cs: 1, rs: 1},
            "canvas": {r: 1, c: 0, cs: 1, rs: 1},

            "btn_new_entity": {r: 0, c: 0}
        }

        self.top_frame = tkinter.Frame(self)
        self.tv_btn_new_entity, \
        self.btn_new_entity = \
            button_factory(
                self.top_frame,
                tv_btn="New Entity",
                command=self.click_new_entity
            )
        self.canvas = tkinter.Canvas(
            self,
            width=self.data["canvas_width"],
            height=self.data["canvas_height"],
            background=self.data["canvas_background"]
        )

        self.grid_widgets()

    def grid_widgets(self):
        for k, args in self.grid_args.items():
            eval(f"self.{k}.grid(**{args})")

    def grid_keys(self):
        return "row", "column", "rowspan", "columnspan", "ipadx", "ipady", "padx", "pady", "sticky"

    def pick_spawn_pos(self):
        cw = self.data["canvas_width"]
        ew = self.data["width_entity"]
        ch = self.data["canvas_height"]
        eh = self.data["width_entity"]
        ow = self.data["outline_width_entity"]
        hh = eh // 2
        hw = ew // 2
        found = False
        res = hw + ow, hh + ow, hw + ew + (2 * ow), hh + eh + (2 * ow)
        for i in range(ew // 2, cw, ew):
            for j in range(eh // 2, ch, eh):
                a, b, c, d = j - ow, i - ow, j + ew + ow, i + eh + ow
                for ent in self.entities:
                    pos = self.canvas.bbox(ent.tag)
                    print(f"{ent} {pos=}, c_pos={(a, b, c, d)}")
                    x1, y1, x2, y2 = pos
                    if not (x1 <= a <= x2) and not (y1 <= b <= y2) and not (x1 <= c <= x2) and not (y1 <= d <= y2):
                        res = j, i, j + ew, i + eh
                        found = True
                        break
                if found:
                    break
            if found:
                break
        print(f"{res=}")
        return res



            # x1, y1, ww, hh = pos
            # x2, y2 = x1 + ww, y1 + hh
        # i, j = ew // 2, eh // 2
        # for i in range(ew // 2, w, ew):
        #     for j in range(eh // 2, h, eh):
        #         pt = (i, j)
        #         for ent in self.entities:
        #             pos = self.canvas.bbox(ent.tag)
        #             print(f"{ent} {pos=}")
        #             x1, y1, ww, hh = pos
        #             x2, y2 = x1 + ww, y1 + hh
        #             if not (x1 <= j <= x2) and not (y1 <= i <= y2):
        #                 found = True
        #                 break
        #         if found:
        #             break
        #     if found:
        #         break
        #
        # return 180, 180, 100, 65

    def click_new_entity(self, *args):
        print()
        x1, y1, x2, y2 = self.pick_spawn_pos()
        fill = self.data["fill_entity"]
        outline = self.data["outline_entity"]
        outline_width = self.data["outline_width_entity"]
        print(f"P {x1=}, {y1=}, {x2=}, {y2=}")
        tag = self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=fill,
            outline=outline,
            width=outline_width
        )
        print(f"{self.canvas.bbox(tag)=}")
        ent = TkSplitMenu.Entity(tag=tag)
        self.entities.append(ent)


if __name__ == '__main__':
    ts = TransactionSplit()


    def test_1():
        ts.add_transaction(30, "Avery", description="TEST")
        ts.add_transaction(30, ["Avery", "Kristen"], description="TEST")
        ts.add_transaction(30, ["Avery"], description="TEST")
        ts.add_transaction(31, ["Emily"], description="TEST")
        ts.add_transaction(10, ["Emily"], e_to="Avery", description="TEST")
        ts.add_transaction(20, ["Kristen"], e_to="Avery", description="TEST")


    def test_2():
        ts.add_transaction(20, "Avery", description="TEST")
        ts.add_transaction(20, "Kristen", description="TEST")
        ts.add_transaction(20, ["Emily"], description="TEST")
        ts.add_transaction(40, ["Hayley"], description="TEST")


    def test_4():
        ts.add_transaction(75, "Avery", description="TEST")
        ts.add_transaction(25, "Kristen", description="TEST")
        ts.add_transaction(40, ["Emily"], description="TEST")
        ts.add_transaction(40, ["Hayley"], description="TEST")


    def test_5():
        ts.add_transaction(100, "Avery", description="TEST")
        ts.add_transaction(0, "Kristen", description="TEST")
        ts.add_transaction(15, ["Emily"], description="TEST")
        ts.add_transaction(85, ["Hayley"], description="TEST")


    def test_6():
        ts.add_transaction(50, "Avery", description="TEST")
        ts.add_transaction(25, "Kristen", description="TEST")
        ts.add_transaction(25, ["Emily"], description="TEST")
        ts.add_transaction(21, ["Hayley"], e_to="Avery", description="TEST")


    def test_3():
        ts.add_transaction(20, ["Avery"], description="TEST")
        ts.add_transaction(200, ["Avery"], description="TEST")
        ts.add_transaction(1, [POT], e_to=["Avery"], description="TEST")


    def historic():
        ts.add_transaction(100, "Avery", description="Mother's Day Supper (Wingo's)")
        ts.add_transaction(17.58, "Kristen", description="Mother's Day Supper (Wingo's)")
        ts.add_transaction(115.74, "Emily", description="Mother's Day Present")
        ts.add_transaction(55, "Hayley", e_to="Emily", description="Mother's Day Present")
        ts.add_transaction(170.7, "Kristen", description="Father's Day Present")
        ts.add_transaction(40, "Avery", e_to="Emily", description="Father's Day Boating")
        ts.add_transaction(50, "Emily", description="Father's Day Boating")
        ts.add_transaction(40, "Hayley", description="Father's Day Boating")
        ts.add_transaction(10, "Emily", e_to="Avery", description="Father's Day Boating")
        ts.add_transaction(180, "Kristen", description="Spotify 2021")
        ts.add_transaction(180, "Kristen", description="Spotify 2022")
        ts.add_transaction(180, "Kristen", description="Spotify 2023")
        ts.add_transaction(120, "Avery", description="Spotify 2021")
        ts.add_transaction(120, "Avery", description="Spotify 2022")
        ts.add_transaction(120, "Avery", description="Spotify 2023")


    # payments = [
    #     Payment("Mother's Day Supper (Wingo's)", "A", "P", 100, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    #     Payment("Mother's Day Supper (Wingo's)", "K", "P", 17.58, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    #     Payment("Mother's Day Present ()", "E", "P", 115.74, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    #     Payment("Hayley paid Emily", "H", "E", 55, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    #     Payment("Father's Day Present (Air Fryer)", "K", "P", 170.7,
    #             datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    #     Payment("Father's Day Boating", "A", "E", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    #     Payment("Father's Day Boating", "E", "P", 50, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    #     Payment("Father's Day Boating", "H", "P", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    #     Payment("Father's Day Boating", "E", "A", 10, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    #     Payment("Spotify", "K", "P", 180, datetime.datetime.strptime("2021-08-04", "%Y-%m-%d")),
    #     Payment("Disney+", "A", "P", 89.99, datetime.datetime.strptime("2021-08-04", "%Y-%m-%d"))
    # ]

    # test_3()
    # test_4()
    # test_5()
    # test_6()
    historic()

    print(f"Entities")
    for ent in ts.entities:
        print(f"{ent}")

    print(f"Transactions")
    for trans in ts.transactions:
        print(f"{trans}")

    ts.split()

    app = TkSplitMenu()
    app.mainloop()

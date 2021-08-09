import re
import os
import easygui as gui
import webbrowser
import datetime
from test_suite import *
from pdf_writer import PDF
from colour_utility import *

# file_name = "C:/Users/ABriggs/Documents/BWS/Dealer reports/Dealer Status Review.txt"
# file_name = "C:/Users/ABriggs/Documents/BWS/Dealer reports/demo_1.txt"
ORDERS_TO_CHANGE_OUTPUT = "Orders to change.txt"
PDF_HEADER = ["Q#", "Wo#", "Model", "Serial #", "Prod.", "Mrp", "P", "Avail.", "Est. Del.", "F", "New Del"]
FILE_NAME = "Dealer Delivery Report.pdf"

HOLIDAYS_2021 = list(map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d"), [
    "2021-02-15",
    "2021-01-01",
    "2021-04-02",
    "2021-05-24",
    "2021-07-01",
    "2021-07-02",
    "2021-08-02",
    "2021-08-03",
    "2021-08-04",
    "2021-08-05",
    "2021-08-06",
    "2021-09-06",
    "2021-10-11",
    "2021-11-11",
    "2021-12-24",
    "2021-12-27",
    "2021-12-28",
    "2021-12-29",
    "2021-12-30",
    "2021-12-31"
]))


class Order:
    def __init__(self, data, line):
        # spl = line.split()
        # print("(" + str(len(line)) + ")" + str(line))
        self.line = line

        char_table = []
        for page in data:
            for dat in page:
                char_table.append(list(dat))

        vertical_dividers = []
        for row in char_table:
            for i, let in enumerate(row):
                if let == " ":
                    keep = True
                    for j in range(len(char_table)):
                        if i < len(char_table[j]) and char_table[j][i] != " ":
                            keep = False
                            break
                    if keep and i not in vertical_dividers:
                        vertical_dividers.append(i)

        vertical_dividers = list(vertical_dividers)
        vertical_dividers.sort()
        i = 0
        grouped_dividers = []
        lvd = len(vertical_dividers)
        while i < lvd:
            j = i + 1
            while j < (lvd - 1) and vertical_dividers[i] == vertical_dividers[j] - 1:
                j += 1
            if j < lvd:
                grouped_dividers.append(vertical_dividers[j])
            i = j
            i += 1
        grouped_dividers.append(len(line))

        items = []
        start = 0
        stop = 0
        i = 0
        while i < len(grouped_dividers):
            stop = grouped_dividers[i]
            s = "".join(line[start: stop]).strip()
            if s:
                items.append(s)
            start = grouped_dividers[i]
            if i + 1 < len(grouped_dividers):
                stop = grouped_dividers[i + 1]
            else:
                stop = len(line)
            i += 1
        self.manual_review = False
        self.grouped_dividers = grouped_dividers
        if len(items) == 10:
            self.quote, self.WO, self.model_no, self.serial_number, self.order, self.production, self.MRP_finish, self.req_delivery_date, self.P, self.est_delivery = items
            self.available_date = None
            self.F = None
        elif len(items) == 12:
            self.quote, self.WO, self.model_no, self.serial_number, self.order, self.production, self.MRP_finish, self.req_delivery_date, self.P, self.available_date, self.est_delivery, self.F = items
        else:
            self.manual_review = True
        # raise ValueError("items:\n\t" + str(items))

    def table_entry(self):
        # PDF_HEADER = ["Q#", "Wo#", "Model", "Serial #", "Prod.", "Mrp", "P", "Avail.", "Est. Del.", "F", "New Del"]
        # print(dict_print(dict(zip(PDF_HEADER, [self.quote, self.WO, self.model_no, self.serial_number, self.order, self.production, self.MRP_finish, self.req_delivery_date, self.P, self.available_date, self.est_delivery, self.F])), "Entry"))
        return dict(zip(PDF_HEADER, [self.quote, self.WO, self.model_no[:10], self.serial_number[-8:], self.production,
                                     self.MRP_finish, self.P, self.available_date, self.est_delivery, self.F,
                                     self.new_delivery_date]))

    def report_format(self, dividers, new_date, spacer_len):
        line = self.line

        nd = dt.datetime.strftime(new_date, "%d-%b-%y")
        # data = [self.quote, self.WO[-5:], self.model_no, self.serial_number[-8:], self.order, self.production, self.MRP_finish, self.req_delivery_date, self.P, self.available_date, self.est_delivery, self.F, nd]
        data = [self.quote, self.WO[-5:], self.model_no[:21], self.serial_number[-8:], self.production, self.MRP_finish,
                self.P, self.available_date, self.est_delivery, self.F, nd]
        stop = 0
        i = 0
        res = ""
        # print("len(gd):", len(dividers), "gd", dividers, "\nlen(data):", len(data))
        while i < len(data):
            stop = dividers[i]
            # print("i", i, "len(res)", len(res), "(", start, ",", stop, ")", "s-s", (stop - start))
            d = data[i] if data[i] != None else "-"
            x = 0
            if i > 0:
                x = spacer_len
            res += pad_centre(str(d), (x + stop - len(res)))
            start = dividers[i]
            if i + 1 < len(dividers):
                stop = dividers[i + 1]
            else:
                stop = len(line)
            i += 1
        return res

    def __repr__(self):
        return "{quote}, {WO}, {model_no}, {serial_number}, {order}, {production}, {MRP_finish}, {req_delivery_date}, {P}, {available_date}, {est_delivery}, {F}".format(
            quote=self.quote,
            WO=self.WO,
            model_no=self.model_no,
            serial_number=self.serial_number,
            order=self.order,
            production=self.production,
            MRP_finish=self.MRP_finish,
            req_delivery_date=self.req_delivery_date,
            P=self.P,
            available_date=self.available_date,
            est_delivery=self.est_delivery,
            F=self.F)


def need_est_delivery_update(orders, lead_days=5, forward_review_threshold=5, backward_review_threshold=3,
                             forward_adjust_threshold=10, backward_adjust_threshold=float("-inf")):
    need_adjusting = []
    forward_review = []
    backward_review = []
    manual_review = []
    for order in orders:
        try:
            est = dt.datetime.strptime(order.est_delivery, "%d-%b-%y")
            mrp = dt.datetime.strptime(order.MRP_finish, "%d-%b-%y")
            avail = dt.datetime.strptime(order.available_date, "%d-%b-%y") if order.available_date is not None else None
            # print("\nest: {est}, mrp: {mrp}, avail: {avail}".format(est=est, mrp=mrp, avail=avail))
            if avail:
                new_date = add_business_days(avail, lead_days, HOLIDAYS_2021)
            else:
                new_date = add_business_days(mrp, lead_days, HOLIDAYS_2021)
            date_diff = business_days_between(est, new_date, HOLIDAYS_2021)
            # print("date_diff:", date_diff)
            if new_date < est:
                # moving forward
                if date_diff >= forward_review_threshold:  # comparing business days
                    forward_review.append((new_date, order))
                if date_diff >= forward_adjust_threshold:
                    need_adjusting.append((new_date, order))  # only update very far pushed forward orders

            elif new_date > est:
                # moving backward
                if date_diff >= backward_review_threshold:  # comparing business days
                    backward_review.append((new_date, order))
                if date_diff >= backward_adjust_threshold:
                    need_adjusting.append((new_date, order))  # only update very far pushed backward orders
            else:
                # no change
                pass
        except ValueError:
            print("ValueError Exception caught in need_est_delivery_update")
        except TypeError:
            print("TypeError Exception caught in need_est_delivery_update")
            manual_review.append(order)

    return need_adjusting, forward_review, backward_review, manual_review


# def need_est_delivery_update(orders, lead_days=5, forward_review_threshold=5, backward_review_threshold=3, forward_adjust_threshold=10, backward_adjust_threshold=float("-inf")):
# 	need_adjusting = []
# 	forward_review = []
# 	backward_review = []
# 	manual_review = []
# 	for order in orders:
# 		try :
# 			est = dt.datetime.strptime(order.est_delivery, "%d-%b-%y")
# 			mrp = dt.datetime.strptime(order.MRP_finish, "%d-%b-%y")
# 			avail = dt.datetime.strptime(order.available_date, "%d-%b-%y") if order.available_date != None else None
# 			# print("\nest: {est}, mrp: {mrp}, avail: {avail}".format(est=est, mrp=mrp, avail=avail))
# 			if avail:
# 				new_date = add_business_days(avail, lead_days, HOLIDAYS_2021)
# 				date_diff = business_days_between(est, new_date, HOLIDAYS_2021)
# 				print("date_diff:", date_diff)
# 				if new_date < est:
# 					# moving forward
# 					if date_diff >= forward_review_threshold: # comparing business days
# 						forward_review.append((new_date, order))
# 					if date_diff >= forward_adjust_threshold:
# 						need_adjusting.append((new_date, order))  # only update very far pushed forward orders

# 				elif new_date > est:
# 					# moving backward
# 					if date_diff >= backward_review_threshold: # comparing business days
# 						backward_review.append((new_date, order))
# 					if date_diff >= backward_adjust_threshold:
# 						need_adjusting.append((new_date, order))  # only update very far pushed backward orders
# 				else:
# 					# no change
# 					pass
# 			else:					
# 				new_date = add_business_days(mrp, lead_days, HOLIDAYS_2021)
# 				date_diff = business_days_between(est, new_date, HOLIDAYS_2021)
# 				print("date_diff:", date_diff)
# 				if new_date < est:
# 					# moving forward
# 					if date_diff >= forward_review_threshold: # comparing business days
# 						forward_review.append((new_date, order))
# 					if date_diff >= forward_adjust_threshold:
# 						need_adjusting.append((new_date, order))  # only update very far pushed forward orders

# 				elif new_date > est:
# 					# moving backward
# 					if date_diff >= backward_review_threshold: # comparing business days
# 						backward_review.append((new_date, order))
# 					if date_diff >= backward_adjust_threshold:
# 						need_adjusting.append((new_date, order))  # only update very far pushed backward orders
# 				else:
# 					# no change
# 					pass
# 		except:
# 			print("Exception caught in need_est_delivery_update")
# 			manual_review.append(order)

# 	return need_adjusting, forward_review, backward_review, manual_review

def create_orders(data):
    orders = []
    manual_review_orders = []
    for page in data:
        for dat in page:
            order = Order(data, dat)
            # print(dir(order))
            if not order.manual_review:
                orders.append(order)
            else:
                manual_review_orders.append(order)
    # print(orders[-1])
    return orders, manual_review_orders


def write_est_delivery_update_report(dealer, col_names, orders):
    spacer_len = 3
    header = "\n\n\tDealer Delivery Report for << " + " ".join(dealer) + " >>"
    header += "\n\tThe following orders need their estimated delivery dates updated.\n\n"
    dividers = [0 for i in range(11)]
    x = 0
    manual_review = []
    for order_line in orders:
        try:
            new_date, order = order_line
            nd = dt.datetime.strftime(new_date, "%d-%b-%y")
            spl = list(map(str.strip, (str(order) + "," + nd).split(",")))
            # print("spl", spl)
            for i in range(len(spl)):
                col_name = col_names[i]
                ls = len(spl[i])
                if "serial" in col_name.lower():
                    ls = 8
                if "model" in col_name.lower():
                    ls = min(20, ls)
                if "wo#" in col_name.lower():
                    ls = 5
                if "p" == col_name.lower():
                    ls = len(spl[8])
                    if spl[8] == None or spl[8] == "_":
                        ls = 1
                if "f" == col_name.lower():
                    ls = len(spl[11])
                    if spl[11] == None or spl[11] == "_" or spl[11].lower() == "none":
                        ls = 1
                # print("col_name", col_name)
                off = 0 if i == 0 else dividers[i - 1] + spacer_len
                dividers[i] = max(dividers[i], ls + off, len(col_name) + off)
        except:
            manual_review.append(order)

    col_line = ""
    for i, div in enumerate(dividers):
        x = 0
        if i > 0:
            x = spacer_len
        col_line += pad_centre(col_names[i], x + (max(len(col_names[i]) + 1, div - len(col_line))))
    header += col_line + "\n"
    orders = [order.report_format(dividers, new_date, spacer_len) for new_date, order in orders]
    write_results(ORDERS_TO_CHANGE_OUTPUT, header, orders)
    return manual_review


def write_results(file, header, data):
    with open(file, 'a') as wf:
        wf.write("\n" + header)
        for dat in data:
            wf.write(dat + "\n")
        wf.write("\nEOF")


def do_test():
    bd_test_set = {
        "test_1, 03-Jul-21 -> 21-Jun-21 - no holidays": [
            [
                dt.datetime.strptime("21-Jun-21", "%d-%b-%y"),
                dt.datetime.strptime("03-Jul-21", "%d-%b-%y")
            ],
            10
        ],
        "test_2, 21-Jun-21 -> 03-Jul-21 - no holidays": [
            [
                dt.datetime.strptime("03-Jul-21", "%d-%b-%y"),
                dt.datetime.strptime("21-Jun-21", "%d-%b-%y")
            ],
            10
        ],
        "test_3, 02-Aug-21 -> 28-Jul-21 - no holidays": [
            [
                dt.datetime.strptime("02-Aug-21", "%d-%b-%y"),
                dt.datetime.strptime("28-Jul-21", "%d-%b-%y")
            ],
            3
        ],
        "test_4, 02-Aug-21 -> 28-Jul-21": [
            [
                dt.datetime.strptime("02-Aug-21", "%d-%b-%y"),
                dt.datetime.strptime("28-Jul-21", "%d-%b-%y"),
                HOLIDAYS_2021
            ],
            3
        ],
        "test_5, 07-Jul-21 -> 25-Jun-21": [
            [
                dt.datetime.strptime("07-Jul-21", "%d-%b-%y"),
                dt.datetime.strptime("25-Jun-21", "%d-%b-%y"),
                HOLIDAYS_2021
            ],
            6
        ],
        "test_6, 07-Jul-21 -> 25-Jun-21 - no holidays": [
            [
                dt.datetime.strptime("07-Jul-21", "%d-%b-%y"),
                dt.datetime.strptime("25-Jun-21", "%d-%b-%y")
            ],
            8
        ]
    }

    add_business_days_test_set = {
        "test_1, 07-Jul-21 + 7 business days - no holidays": [
            [
                dt.datetime.strptime("07-Jul-21", "%d-%b-%y"),
                7
            ],
            dt.datetime(2021, 7, 16)
        ],
        "test_2, 27-Jun-21 + 7 business days - no holidays": [
            [
                dt.datetime.strptime("27-Jun-21", "%d-%b-%y"),
                7
            ],
            dt.datetime(2021, 7, 6)
        ],
        "test_3, 27-Jun-21 + 7 business days": [
            [
                dt.datetime.strptime("27-Jun-21", "%d-%b-%y"),
                7,
                HOLIDAYS_2021
            ],
            dt.datetime(2021, 7, 8)
        ]
    }
    tests_to_run = [
        (business_days_between, bd_test_set),
        (add_business_days, add_business_days_test_set)
    ]
    run_multiple_tests(tests_to_run)


def dealer_delivery_report_updates(dealer, file_name, lead_days=5, forward_review_threshold=5,
                                   backward_review_threshold=3, forward_adjust_threshold=10,
                                   backward_adjust_threshold=float("-inf")):
    print("file_name", file_name)
    all_for_adjusting = []

    with open(file_name, 'r') as f:
        lines = f.readlines()

        i = 0
        pages = 0
        data = []
        header_line = None
        while i < len(lines):
            line = lines[i]
            spl = line.split()
            # print("i:", i, "spl", spl)
            if spl == ["Date", "Date", "Date"]:
                if header_line is None:
                    header_line = [l.strip() for l in lines[i - 1].split("   ") if l] + ["New Delivery"]
                # print("header_line BEFORE:", header_line)
                i += 1
                page_data = []
                while i < len(lines) and "Criteria: Dealer, PO Date, Date Completed, Shipped Date and Date" not in \
                        lines[i]:
                    s = lines[i].strip()
                    if s:
                        page_data.append(s)
                    i += 1
                pages += 1
                data.append(page_data)
            i += 1

        # print("header_line", header_line)
        refined_header = []
        for col_name in header_line:
            temp = col_name.lower()
            if "quote" in temp:
                temp = temp.replace("quote", "Q")
            if "date" in temp:
                temp = temp.replace("date", "")
            if "production" in temp:
                temp = temp.replace("production", "prod.")
            if "delivery" in temp:
                temp = temp.replace("delivery", "del.")
            if "number" in temp:
                temp = temp.replace("number", "#")
            if "available" in temp:
                temp = temp.replace("available", "avail.")
            if "finish" in temp:
                temp = temp.replace("finish", "")
            if "model no" in temp:
                temp = temp.replace("no", "")
            if "order" == temp:
                continue
            if "req." in temp:
                continue
            temp = temp.strip().title()
            refined_header.append(temp)
        header_line = refined_header
        # print("header_line AFTER:", header_line)

        print("pages: " + str(pages))
        # print("\n\n-----------\n\n")

        orders, manual_review_orders = create_orders(data)
        # print("manual review after creation:", [q.quote if q.manual_review is False else q.line for q in orders])
        need_adjusted, forward_review, backward_review, manual_review = need_est_delivery_update(orders,
                                                                                                 lead_days=lead_days,
                                                                                                 forward_review_threshold=forward_review_threshold,
                                                                                                 backward_review_threshold=backward_review_threshold,
                                                                                                 forward_adjust_threshold=forward_adjust_threshold,
                                                                                                 backward_adjust_threshold=backward_adjust_threshold)
        print("need_Adjusted({}): {}: {}".format(len(need_adjusted), type(need_adjusted), need_adjusted))
        print("forward_review({}): {}: {}".format(len(forward_review), type(forward_review), forward_review))
        print("backward_review({}): {}: {}".format(len(backward_review), type(backward_review), backward_review))
        print("manual_review({}): {}: {}".format(len(manual_review), type(manual_review), manual_review))

        manual_review_orders += manual_review

        print("\n\tNeeds estimated delivery date updated:\n")
        for order in need_adjusted:
            all_for_adjusting.append(order)
            print(order)
        manual_review_orders.append(write_est_delivery_update_report(dealer, header_line, need_adjusted))

        print("\n\tReview forward moving units:\n")
        for order in forward_review:
            print(order)

        print("\n\tReview backward moving units:\n")
        for order in backward_review:
            print(order)

        print("\n\tNeeds manual review due to missing data:\n")
        for order in manual_review_orders:
            try:
                print(order.line)
            except:
                print("CHECK: ", order)

    # do_test()

    return all_for_adjusting


def run_reports(n=None):
    ld = 5
    frt = 5
    brt = 3
    fat = 7
    bat = 5
    with open(ORDERS_TO_CHANGE_OUTPUT, 'w') as out:
        d = dt.datetime.strftime(dt.datetime.now(), "%d-%b-%y")
        out.write("Dealer Delivery Reports as of " + d)
        out.write("\n\nUsing lead time of {0} days".format(ld))
        out.write("\nAdjusting deliveries moved back by at least {0} days ".format(bat))
        out.write("\nAdjusting deliveries moved forward by at least {0} days ".format(fat))

    path = "C:/Users/ABriggs/Documents/BWS/Dealer reports/Reports"
    try:
        # File directory at work
        files = os.listdir(path)
        files = [path + "/" + f for f in files if "Dealer Status" in f and f.endswith(".txt")]
    except FileNotFoundError:
        # File directory at home
        path = "C:/Users/abrig/Documents/BWS/BWS/Dealer reports/Reports"
        files = os.listdir(path)
        files = [path + "/" + f for f in files if "Dealer Status" in f and f.endswith(".txt")]
    # s = "C:\Users\ABriggs\Documents\BWS\Dealer reports\Reports\Atlantic Powertrain Dealer Status Review.txt"

    # files = ["Reports/Remorques Lewis Inc Dealer Status Review.txt", "Reports/Hale Trailer Brake & Wheel Dealer Status Review.txt"]
    need_adjusted = []
    pdf_table_data = {}
    max_n = n if n is not None else len(files)
    for i, f in enumerate(files[:max_n]):
        dealer = f[f.index("/") + 1:].split()[:-3]
        need_adj = dealer_delivery_report_updates(dealer, f, lead_days=ld, forward_review_threshold=frt,
                                                  backward_review_threshold=brt, forward_adjust_threshold=fat,
                                                  backward_adjust_threshold=bat)
        print("type A:", type(need_adj))
        f_short = f[len(path) + 1: len(path) + 1 + 230]
        pdf_table_data[f_short] = dict(zip(PDF_HEADER, [None for header in PDF_HEADER]))
        if need_adj is not None:
            print("need_adj:", need_adj, "type:", type(need_adj))
            if need_adj:
                for j, d_point in enumerate(need_adj):
                    new_date = d_point[0]
                    order = d_point[1]
                    order.new_delivery_date = datetime.datetime.strftime(new_date, "%d-%b-%y")
                    print("type:", type(order), "isinstance(order, Order):", isinstance(order, Order), "entry:",
                          order.table_entry())
                    pdf_table_data[f_short + "".join([" " for k in range(j)])] = order.table_entry()
                print("type D:", type(need_adj[0][1]))
            need_adjusted += need_adj

    print(dict_print(pdf_table_data), "PDF_table_data")

    print("\n\tFinal tally of orders that require estimated delivery update:\n")
    for order in need_adjusted:
        print(order)

    testing = '''
	# desired = [25433, 25703, 24847, 24848, 25647, 25243, 25342, 25376, 25379, 25378, 25519, 25760, 25761, 25762, 25763, 25764, 25765, 25766, 25767, 25768, 25091]
	desired = [25433, 25703, 25647, 25243, 25342, 25376, 25379, 25378, 25519, 25760, 25761, 25762, 25763, 25764, 25765, 25766, 25767, 25768, 25091]
	# desired = [25433, 25703, 25647, 25243, 25342, 25376, 25379, 25378, 25765, 25766, 25767, 25768, 25091]
	desired.sort()
	print("desired\n", desired)
	adjs = [int(q[1].quote) for q in need_adjusted]
	adjs.sort()
	print("adjs:\n", adjs)
	print("equal?", adjs == (desired))
	right = intersection(adjs, desired)
	right.sort()
	print("right:", right)
	print("Got all required:", right==desired)
	diff = disjoint(adjs, desired)
	diff.sort()
	print("diff:", diff)
	'''
    return pdf_table_data


def write_pdf_report(data):
    MAX_Y = 297
    MAX_X = 210
    MARGIN_LINES_WIDTH = 2
    MARGIN_LINES_MARGIN = 4
    TITLE_HEIGHT = 6
    TITLE_MARGIN = 4
    TXT_MARGIN = 5
    TABLE_MARGIN = 2
    FOOTER_MARGIN = 10
    ori = "P"

    if ori == "L":
        MAX_X, MAX_Y = MAX_Y, MAX_X

    pdf = PDF(FILE_NAME, orientation=ori, unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=5)
    pdf.set_title("Dealer Delivery Reports")
    pdf.set_author('Avery Briggs')
    pdf.add_page()

    # pdf.margin_lines(MARGIN_LINES_MARGIN, MARGIN_LINES_MARGIN, MAX_X - (2 * MARGIN_LINES_MARGIN),
    # 				 MAX_Y - (2 * MARGIN_LINES_MARGIN), BWS_RED, WHITE)
    pdf.margin_border(BWS_RED, WHITE)
    pdf.titles("Dealer Delivery Reports", MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN,
               TITLE_MARGIN + MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN,
               MAX_X - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN)), TITLE_HEIGHT, BWS_BLACK)

    # TABLE_X = 5 + MARGIN_LINES_WIDTH + TABLE_MARGIN
    # TABLE_Y = 10 + MARGIN_LINES_WIDTH + TABLE_MARGIN

    TABLE_W = (MAX_X - (2 * (MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN)) - (2 * TABLE_MARGIN))

    TABLE_X = TABLE_MARGIN + MARGIN_LINES_WIDTH + MARGIN_LINES_MARGIN
    TABLE_Y = TABLE_MARGIN + MARGIN_LINES_WIDTH + TITLE_HEIGHT + TITLE_MARGIN

    # TABLE_LEFT_MARGIN = 6
    TITLE_V_MARGIN = 5

    table1 = pdf.table(
        title="Need Adjusted",
        x=TABLE_X,
        y=TABLE_Y,
        w=TABLE_W,
        contents=data,
        desc_txt="The following quotes should have their estimated delivery dates edited in Access:",
        # contents=random_test_set(453),
        header_colours=[GRAY_30, BLACK],
        colours=[[WHITE, GRAY_69],
                 [BLACK]],
        show_row_names=True,
        include_top_doc_link=True,
        new_page_for_table=False,
        row_name_col_lbl="Dealer",
        start_with_header=True,
        cell_border_style=1,
        col_align={"Dealer": "L"},
        top_margin=2,
        col_widths={"Dealer": 3/24, "P": 1/24, "F": 1/24}
    )

    pdf.time_stamp()
    pdf.output(FILE_NAME, 'F')
    webbrowser.open(FILE_NAME)


pdf_table_data = run_reports()
print(dict_print(pdf_table_data, "pdf_table_data before writing"))
write_pdf_report(pdf_table_data)

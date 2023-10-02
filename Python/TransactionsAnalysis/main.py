import os
from PyPDF2 import PdfReader

if __name__ == '__main__':
    print('PyCharm')

    file_root = r"D:\Important documents\Spending\Amex"
    list_files = [f.path for f in os.scandir(file_root) if f.is_file() and f.path.endswith(".pdf")]

    for file_path in list_files:
        print(f"{file_path=}")
        with open(file_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                # extract text from the page
                # page_text = page.extractText()
                page_text = page.extract_text()
                # p_split = page_text.lower().replace("\n", "_").split("transaction")
                p_split = page_text.lower().replace("\n", "_").split("amount($)")
                p_split_ = "\t" + "\n".join(p_split) + "\t"
                print(f"P {page_num}, len={len(p_split)}, {p_split_}")

    # try:
    #
    #     # open the PDF file in binary mode
    #     with open(fn, 'rb') as f:
    #         # create a PDF reader object
    #         # pdf_reader = PyPDF2.PdfFileReader(f)
    #         pdf_reader = PdfReader(f)
    #         # read each page of the PDF file
    #         # for page_num in range(pdf_reader.numPages):
    #         # print(f"{pdf_reader=}")
    #         # assert pdf_reader is not None, "Else IS NONE"
    #         for page_num in range(len(pdf_reader.pages)):
    #             # page = pdf_reader.getPage(page_num)
    #             page = pdf_reader.pages[page_num]
    #             # extract text from the page
    #             # page_text = page.extractText()
    #             page_text = page.extract_text()
    #             # append the text from this page to the overall text
    #             text += page_text
    #
    #     # t1 = "Expédié via / Ship Via No commande / Order number Incoterms Termes / Terms Date No client Customer No. Page"
    #     # print(f"{text.count(t1)=}")
    #
    #     invoice_number = None
    #     order_number = None
    #     splitter = 0, "Page"
    #     in_spl_invoice = "No.:"
    #     # in_spl_order_1 = "TermsIncoterms"
    #     in_spl_order_1 = "Incoterms"
    #     # in_spl_order_2 = "/qty"
    #     in_spl_order_2 = "FCAGRANBY"
    #     in_spl_order_3 = "PICK-UP "
    #     num_pages = text.count(splitter[1])
    #     # if print_test:
    #     #     print(f"{text=}")
    #     #     print(f"{num_pages=}")
    #     #     print(f"{splitter=}")
    #     pages_real_pages = [page.replace("\x03", "") for page in text.split(splitter[1])]  # [1:]
    #     invoice_match, order_match = None, None
    #
    #     # print(f"{len(pages_real_pages)=}")
    #
    #     for i, page in enumerate(pages_real_pages):
    #
    #         try:
    #             # q_id = 0
    #             # # print(f"{i}-{page=}")
    #             # la_idx = lstindex(page, "laseramp")
    #             # assert la_idx >= 0 or ((i + 1) == len(pages_real_pages)), f"Error 'laseramp' not found on page {i + 1}."
    #             #
    #             # if print_test:
    #             #     print(f"\nNewPage {i}")
    #             #
    #             # # if invoice_number == None and order_number == None:
    #             # re_check_order_1 = False
    #             # re_check_order_2 = False
    #             # re_check_order_3 = False
    #             # iv_idx = lstindex(page, in_spl_invoice)
    #             # if print_test:
    #             #     print(f"{iv_idx=}, {page=}")
    #             # if iv_idx >= 0:
    #             #     left = (page[:iv_idx]).strip().split(" ")[-1] + in_spl_invoice
    #             #     right1 = page[iv_idx:].split(" ")[0].strip()
    #             #     right2 = f"{in_spl_invoice} " + (page[iv_idx:].split(" ")[1]).strip()
    #             #     # check right first:
    #             #     l_match = re.search(r'(\d+)' + in_spl_invoice, left)
    #             #     r_match1 = re.search(in_spl_invoice + r'(\d+)', right1)
    #             #     r_match2 = re.search(in_spl_invoice + r' (\d+)', right2)
    #             #     if print_test:
    #             #         print(f"A> {iv_idx=} {l_match=}, {left=}\n{r_match1=}, {right1=}\n{r_match2=}, {right2=}")
    #             #     if r_match1:
    #             #         invoice_match = r_match1.group(1)
    #             #     elif r_match2:
    #             #         invoice_match = r_match2.group(1)
    #             #     else:
    #             #         invoice_match = l_match.group(1)
    #             #
    #             #     p_a = l_match.group(0)
    #             #     p_b = len(p_a)
    #             #     p_c = len(in_spl_invoice)
    #             #     # if print_test:
    #             #     #     print(f"\t\t{p_a=}, {p_b=}, {p_c}, {(p_b - p_c)=}")
    #             #     if l_match and ((len(p_a)) - len(in_spl_invoice) == LEN_ORDER_NUMBER) and any(
    #             #             [r_match1, r_match2]):
    #             #         order_match = p_a.replace(in_spl_invoice, "")
    #             #         re_check_order_1 = False
    #             #     else:
    #             #         re_check_order_1 = True
    #             #
    #             # if order_match is None and iv_idx < 0:
    #             #     re_check_order_1 = True
    #             #
    #             # if re_check_order_1:
    #             #     # order number not found
    #             #     iv_idx = lstindex(page, in_spl_order_1)
    #             #     left = (page[:iv_idx].split(" ")[-1] + in_spl_order_1).replace("\n", "")
    #             #     right = (page[iv_idx:].split(" ")[0]).replace("\n", "")
    #             #     l_match = re.search(r'(\d+)' + in_spl_order_1, left)
    #             #     r_match = re.search(in_spl_order_1 + r'(\d+)', right)
    #             #     if print_test:
    #             #         print(f"B> {iv_idx=} {l_match=}, {left=}\n{r_match=}, {right=}")
    #             #     if r_match:
    #             #         order_match = r_match.group(1)
    #             #         re_check_order_2 = False
    #             #         if print_test:
    #             #             print(f"\n\t0-0 {order_match=}")
    #             #     elif l_match:
    #             #         order_match = l_match.group(1)
    #             #         re_check_order_2 = False
    #             #         if print_test:
    #             #             print(f"\n\t0-1 {order_match=}")
    #             #     else:
    #             #         re_check_order_2 = True
    #             #
    #             # if re_check_order_2:
    #             #     # order number not found
    #             #     iv_idx = lstindex(page, in_spl_order_2)
    #             #     left = (" ".join(page[:iv_idx].split(" ")[-2:]) + in_spl_order_2).replace("\n", "").replace(" ", "")
    #             #     right = (page[iv_idx:].split(" ")[0]).replace("\n", "").replace(" ", "")
    #             #     l_match = re.search(r'(\d+)' + in_spl_order_2, left)
    #             #     r_match = re.search(in_spl_order_2 + r'(\d+)', right)
    #             #     if print_test:
    #             #         print(f"C> {iv_idx=} {l_match=}, {left=}\n{r_match=}, {right=}")
    #             #     if r_match:
    #             #         order_match = r_match.group(1)
    #             #         re_check_order_3 = False
    #             #         if print_test:
    #             #             print(f"\n\t1-0 {order_match=}")
    #             #     elif l_match:
    #             #         order_match = l_match.group(1)
    #             #         re_check_order_3 = False
    #             #         if print_test:
    #             #             print(f"\n\t1-1 {order_match=}")
    #             #     else:
    #             #         re_check_order_3 = True
    #             #
    #             # if re_check_order_3:
    #             #     # order number not found
    #             #     iv_idx = lstindex(page, in_spl_order_3)
    #             #     left = (page[:iv_idx].split(" ")[-1] + in_spl_order_3).replace(" ", "")
    #             #     right = in_spl_order_3 + (page[iv_idx:].replace(in_spl_order_3, "").split(" ")[0]).replace(" ",
    #             #                                                                                                "")
    #             #     l_match = re.search(r'(\d+)' + in_spl_order_3, left)
    #             #     r_match = re.search(in_spl_order_3 + r'(\d+)', right)
    #             #     if print_test:
    #             #         print(f"D> {iv_idx=} {l_match=}, {left=}\n{r_match=}, {right=}")
    #             #     if r_match:
    #             #         order_match = r_match.group(1)
    #             #         # if print_test:
    #             #         #     print(f"\n\t2-0 {order_match=}")
    #             #     elif l_match:
    #             #         order_match = l_match.group(1)
    #             #         # if print_test:
    #             #         #     print(f"\n\t2-1 {order_match=}")
    #             #     else:
    #             #         order_match = None
    #             #         # if print_test:
    #             #         #     print(f"\n\t2-2 {order_match=}")
    #             #
    #             # if invoice_match:
    #             #     invoice_number = invoice_match.replace(in_spl_invoice, "")
    #             #     invoices_l.append(invoice_number)
    #             # if order_match:
    #             #     order_number = order_match
    #             #     orders_l.append(order_number)
    #             #
    #             # page_lines = [pl for pl in page.split("\n") if (pl.count("$") == 2) or (in_spl_invoice in pl)]
    #             # # page_lines = [pl.replace(in_spl_invoice, f"{in_spl_invoice} ") for pl in page.split("\n") if (pl.count("$") == 2) or (in_spl_invoice in pl)]
    #             # values = [pl.split(" ")[:5] for pl in page_lines if len(pl.split(" ")) >= 4]
    #             # if print_test:
    #             #     print(f"{page_lines=}\n{values=}")
    #             # for j, vals in enumerate(values):
    #             #
    #             #     qty = None,
    #             #     part_number = None
    #             #     amount = None
    #             #     rev = None
    #             #     price = None
    #             #     amount = None
    #             #
    #             #     if len(vals) == 4:
    #             #         q_id = 1
    #             #         a, b, c, d = vals
    #             #         if is_money(a) and "$" in a:
    #             #             # money value first
    #             #             a, b, c, d = d, c, b, a
    #             #             q_id = 2
    #             #         l_vals = [a, b, c, d]
    #             #     else:
    #             #         # if print_test:
    #             #         #     print("! 5 !")
    #             #         q_id = 3
    #             #         a, b, c, d, e = vals
    #             #         if is_money(a) and "$" in a:
    #             #             q_id = 4
    #             #             # money value first
    #             #             a, b, c, d, e = e, d, c, b, a
    #             #         l_vals = [a, b, c, d, e]
    #             #
    #             #     # print(f"\nv1:{vals}\nv2:{l_vals}")
    #             #     # p_is_money = is_money(vals[-2])
    #             #     # a_is_money = is_money(vals[-1])
    #             #
    #             #     if len(vals) == 4:
    #             #         q_id = 5
    #             #         a, b, c, d = vals
    #             #         im_c, im_d = is_money(c), is_money(d)
    #             #         if im_c and im_d:
    #             #             # if "$" not in d:
    #             #                 # d is rev, qty is at end of partnumber, price=c, amount=b
    #             #
    #             #             q_id = 6
    #             #             m_c, m_d = money_value(c), money_value(d)
    #             #             m_c, m_d = min(m_c, m_d), max(m_c, m_d)
    #             #             price, amount = money(m_c), money(m_d)
    #             #             # price, amount = money(min(m_c, m_d)), money(max(m_c, m_d))
    #             #             if print_test:
    #             #                 print(f"-- {m_c=}, {m_d=}, {price=}, {amount=}")
    #             #             c_q = round(m_d / m_c)
    #             #             part_func_type = [key for key in known_prefixes.keys() if key in a][0]
    #             #             part_type_func = known_prefixes[part_func_type]
    #             #             qty, part_number = part_type_func(a)
    #             #             # print(f"{qty=}, {type(qty)=}, {str(c_q)=}, {type(str(c_q))=}")
    #             #             if print_test:
    #             #                 print(f"{qty=}, {c_q=}, {part_number=}, {amount=}, {price=}, {a=}, {b=}, {c=}, {d=}")
    #             #
    #             #             if qty == "":
    #             #                 if part_number.endswith(str(c_q)):
    #             #                     q_id = 7
    #             #                     part_number = part_number[:part_number.index(str(c_q))]
    #             #                     qty = c_q
    #             #             else:
    #             #                 if str(c_q) != qty:
    #             #                     # print(f"{m_c=}, {m_d=}, {price=}, {amount=}")
    #             #                     q_id = 8
    #             #                     qty, rev = int(b), qty
    #             #                 else:
    #             #                     rev = b
    #             #         if print_test:
    #             #             print(f"AA {qty=}, {part_number=}, {amount=}, {rev=}, {price=}, {invoice_number=}, {order_number=}")
    #             #     else:
    #             #         a, b, c, d, e = vals
    #             #         im_c, im_d, im_e = is_money(c), is_money(d), is_money(e)
    #             #         if print_test:
    #             #             print(f"{a=}, {b=}, {c=}, {d=}, {e=}, {im_c=}, {im_d=}, {im_e=}")
    #             #         handled = False
    #             #         if all([im_c, im_d, im_e]):
    #             #             if "$" in d and "$" in e:
    #             #                 q_id = 9
    #             #
    #             #                 part_func_type = [key for key in known_prefixes.keys() if key in a]
    #             #                 if part_func_type:
    #             #                     part_type_func = known_prefixes[part_func_type[0]]
    #             #                     qty, part_number = part_type_func(a)
    #             #
    #             #                     rev, price, amount = c, d, e
    #             #                     handled = True
    #             #
    #             #         if not handled and im_c and im_d:
    #             #             q_id = 10
    #             #             part_number = a
    #             #             qty = b
    #             #             m_c, m_d = money_value(c), money_value(d)
    #             #             if m_d == 0 and m_c != m_d:
    #             #                 m_c, m_d = m_d, m_c
    #             #             if m_d == 0 == m_c == 0:
    #             #                 price, amount = money(0), money(0)
    #             #                 c_q = b
    #             #             else:
    #             #                 price, amount = money(min(m_c, m_d)), money(max(m_c, m_d))
    #             #                 c_q = round(m_c / m_d)
    #             #             if str(c_q) != qty:
    #             #                 q_id = 11
    #             #                 qty, rev = int(a), qty
    #             #             else:
    #             #                 rev = e
    #             #         # else:
    #             #
    #             #         # print(f"{a=}, {b=}, {c=}, {d=}, {e=}, {im_c=}, {im_d=}, {im_e=}")
    #             #
    #             #     if all([
    #             #         qty is not None,
    #             #         part_number is not None,
    #             #         amount is not None,
    #             #         rev is not None,
    #             #         price is not None,
    #             #         invoice_number is not None,
    #             #         order_number is not None
    #             #     ]):
    #             #         page_idxs.append(i - 1)
    #             #         qtys.append(qty)
    #             #         p_nums.append(part_number)
    #             #         revs.append(rev)
    #             #         prices.append(price)
    #             #         amounts.append(amount)
    #             #         invoices.append(invoice_number)
    #             #         orders.append(order_number)
    #             #         q_ids.append(q_id)
    #             #         passes.append(fn)
    #             #     else:
    #             #         if print_test:
    #             #             print(f"{i=} {j=}, PASS ON {vals=}")
    #             #             print(f"BB {qty=}, {part_number=}, {amount=}, {rev=}, {price=}, {invoice_number=}, {order_number=}")
    #             #
    #             #     # if p_is_money and a_is_money and i > 0:
    #             #     #     q_id = 5
    #             #     #     # if print_test:
    #             #     #     #     print(f"\t{a=}, {b=}, {c=}, {d=}")
    #             #     #     if len(vals) == 4:
    #             #     #         q_id = 6
    #             #     #         part_func_type = [key for key in known_prefixes.keys() if key in a][0]
    #             #     #         part_type_func = known_prefixes[part_func_type]
    #             #     #         qty, part_number = part_type_func(a)
    #             #     #         rev, price, amount = b, c, d
    #             #     #     else:
    #             #     #         q_id = 7
    #             #     #         part_number = a
    #             #     #         qty = b
    #             #     #         rev, price, amount = c, d, e
    #             #     #         # rev, price, amount = e, d, c
    #             #     #
    #             #     #     m_price = money_value(l_vals[-2])
    #             #     #     m_amount = money_value(l_vals[-1])
    #             #     #
    #             #     #     try:
    #             #     #         i_qty = int(qty)
    #             #     #     except ValueError:
    #             #     #         try:
    #             #     #             i_part_number = int(part_number)
    #             #     #             q_id = 8
    #             #     #             qty, part_number = part_number, qty
    #             #     #         except ValueError:
    #             #     #             q_id = 9
    #             #     #
    #             #     #     try:
    #             #     #         tol = 0.01
    #             #     #         price_check = (m_amount - tol) <= m_price * qty <= (m_amount + tol)
    #             #     #         if not price_check:
    #             #     #             q_id = -3
    #             #     #     except ValueError:
    #             #     #         q_id = -4
    #             #     #
    #             #     #     if print_test:
    #             #     #         print(f"{qty=}, {part_number=}, {rev=}, {price=}, {amount=}")
    #             #     #     # print(f"ELSE")
    #             #     #     page_idxs.append(i - 1)
    #             #     #     qtys.append(qty)
    #             #     #     p_nums.append(part_number)
    #             #     #     revs.append(rev)
    #             #     #     prices.append(price)
    #             #     #     amounts.append(amount)
    #             #     #     invoices.append(invoice_number)
    #             #     #     orders.append(order_number)
    #             #     #     q_ids.append(q_id)
    #             #     #     passes.append(fn)
    #             #     # else:
    #             #     #     if q_id == 0:
    #             #     #         q_id = -2
    #             #     #     if print_test:
    #             #     #         print(f"{i=} {j=}, PASS ON {vals=}")
    #         except (ValueError, AttributeError, KeyError, NameError, TypeError, IndexError, AssertionError, ZeroDivisionError) as e2:
    #             q_id = -1
    #             if print_test:
    #                 print(f"FAILURE, {fn=}, {e2=}")
    #             # raise e2
    #             fails.append((fn, i + 1, f"{e2} || {traceback.format_exc()}"))
    #
    #     if print_test:
    #         print(f"{str(len(invoices_l)).ljust(5)}||{invoices_l=}")
    #         print(f"{str(len(orders_l)).ljust(5)}||{orders_l=}")
    #     for j, idx in enumerate(page_idxs):
    #         invoices[j] = invoices_l[idx]
    #         orders[j] = orders_l[idx]
    #
    # except (ValueError, AttributeError, KeyError, NameError, TypeError, IndexError, AssertionError, ZeroDivisionError) as e1:
    #     # print(f"FAILURE")
    #     # raise e
    #     fails.append((fn, i + 1,  f"{e1} || {traceback.format_exc()}"))
    #
    # if print_test:
    #     print(f"\n\n\tFINAL\n")
    #     s_lists = "\n".join([f"{l_name.ljust(12)} len={len(lst)}, lst={lst}" for l_name, lst in
    #                          [
    #                              ("page_idxs", page_idxs),
    #                              ("fails", fails),
    #                              ("qtys", qtys),
    #                              ("passes", passes),
    #                              ("p_nums", p_nums),
    #                              ("revs", revs),
    #                              ("prices", prices),
    #                              ("amounts", amounts),
    #                              ("invoices", invoices),
    #                              ("orders", orders),
    #                              ("invoices_l", invoices),
    #                              ("orders_l", orders),
    #                              ("q_ids", q_ids)
    #                          ]])
    #     print(f"{s_lists}")




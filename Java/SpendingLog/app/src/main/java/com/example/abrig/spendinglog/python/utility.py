import locale

TAB = "    "
SEPARATOR = "  -  "
TABLE_DIVIDER = "|"


# Utility functions

def pad_centre(text, l, pad_str=" "):
    if l > 0:
        h = (l - len(text)) // 2
        odd = (((2 * h) + len(text)) == l)
        text = text.rjust(h + len(text), pad_str)
        h += 1 if not odd else 0
        text = text.ljust(h + len(text), pad_str)
        return text
    else:
        return ""


def text_size(txt):
    spl = txt.split("\n")
    return len(spl), max([len(line) for line in spl])


# Function returns a formatted string containing the contents of a dict object.
# Special lines and line count for values that are lists.
# Supports dictionaries with special value types.
# Lists are printed line by line, but the counting index is constant for all elements. - Useful for ties.
# Dicts are represented by a table which will dynamically generate a header and appropriately format cell values.
# Strings, floats, ints, bools are simply converted to their string representations.
# d					-	dict object.
# n					-	Name of the dict, printed above the contents.
# number			-	Decide whether to number the content lines.
# l					-	Minimum number of chars in the content line.
# 						Spaces between keys and values are populated by marker.
# sep				-	Additional separation between keys and values.
# marker			-	Char that separates the key and value of a content line.
# sort_header		-	Will alphabetically sort the header line if any value is a
#						dictionary. Only one level of nesting supported.
# min_encapsulation	-	If a table is necessary because of a value that is a
#						dictionary, then opt to keep all column widths as small as
#						possible. This will most likely produce varying widths.
# table_title		-	If a table is created, then display the title in the first
#						column directly above the row names.
def dict_print(d, n="Untitled", number=False, l=15, sep=5, marker=".", sort_header=False, min_encapsulation=True,
               table_title=""):
    if not d or not n or type(d) != dict:
        return "None"
    m = "\n--  " + str(n).title() + "  --\n\n"
    fill = 0
    lenstr = lambda x: len(str(x))

    # max_key = max([len(str(k)) + ((2 * len(k) + 2 + len(k) - 1) if type(k) == (list or tuple) else 0) for k in d.keys()])
    # max_val = max([max([len(str(v_elem)) for v_elem in v]) if type(v) == (list or tuple) else len(str(v)) if type(v) != dict else 0 for v in d.values()])
    # fill += sum([len(v) for v in d.values() if type(v) == (list or tuple)])
    # l = max(l, (max_key + max_val)) + sep
    # has_dict = [(k, v) for k, v in d.items() if type(v) == dict]
    # has_list = any([1 if type(v) in [list, tuple] else 0 for v in d.values()])

    max_key = float("-inf")
    max_val = float("-inf")
    fill = float("-inf")
    l = float("-inf")
    has_dict = False
    has_list = False

    for k, v in d.items():
        max_key = max((len(str(k)) + ((2 * len(k) + 2 + len(k) - 1) if type(k) == (list or tuple) else 0)), max_key)
        max_val = max((max([len(str(v_elem)) for v_elem in v] if v else [0]) if type(v) == (list or tuple) else len(
            str(v)) if type(v) != dict else 0), max_val)

    l = max(len(table_title), max(l, (max_key + max_val))) + sep
    has_dict = [(k, v) for k, v in d.items() if type(v) == dict or (type(v) == list and v and type(v[0]) == dict)]
    has_list = any([1 if type(v) in [list, tuple] else 0 for v in d.values()])

    header = []
    max_cell = 0
    max_cell_widths = []

    print("has_dict: {hd}".format(hd=has_dict))
    if has_list:
        number = True
    for k1, v in has_dict:
        for k2 in v:
            key = str(k2)
            print("key: {k}".format(k=key))
            if key not in header:
                if type(v) == dict:
                    print("\t\tNew key: {k}".format(k=key))
                    header.append(key)
                    max_cell = max(max_cell, max(len(key), max([lenstr(value) for value in v.values()])))
                # print("max_cell: {mc}".format(mc=max_cell))
                elif type(k2) == dict:
                    strkeys = list(map(str, list(k2.keys())))
                    strvals = list(map(str, list(k2.values())))
                    header += [strkey for strkey in strkeys if strkey not in header]
                    max_cell = max(max_cell, max(list(map(len, strkeys))), max(list(map(len, strvals))))
                else:
                    for lst in v:
                        a = max(list(map(lenstr, list(map(str, lst.keys())))))
                        b = max(list(map(lenstr, list(map(str, lst.values())))))
                        # print("a: {a}, b: {b}, values: {v}".format(a=a, b=b, v=lst.values()))
                        max_cell = max(max_cell, max(a, b))

    max_cell += 2

    # print("max_cell: {mc}".format(mc=max_cell))
    if sort_header:
        header.sort(key=lambda x: x.rjust(max_cell))

    if min_encapsulation:
        for h in header:
            max_col_width = len(h) + 2
            # print("h: {h}, type(h): {th}".format(h=h, th=type(h)))
            for k, d_val in has_dict:
                d_val = {str(d_val_k): str(d_val_v) for d_val_k, d_val_v in d_val.items()} if type(
                    d_val) == dict else d_val
                # print("d_val: {dv},\thidv: {hidv},\tetdvlist: {etdvl}".format(dv=d_val, hidv=(h in d_val), etdvl=(type(d_val) == list)))
                # print("k: {k}\nt(k): {tk}\nd: {d}\nt(d): {td}".format(k=k, tk=type(k), d=d_val, td=type(d_val)))
                if h in d_val:
                    max_col_width = max(max_col_width, lenstr(d_val[h]) + 2)
                elif type(d_val) == list:
                    max_col_width = max(max_col_width, max([max(
                        max(list(map(lenstr, [ek for ek in elem.keys() if ek == h]))),
                        max(list(map(lenstr, [ev for ek, ev in elem.items() if ek == h]))) + 2) for elem in d_val]))
            max_cell_widths.append(max_col_width)

    # print("max_cell_widths: {mcw}".format(mcw=max_cell_widths))
    table_header = TABLE_DIVIDER + TABLE_DIVIDER.join(
        map(lambda x: pad_centre(str(x), max_cell), header)) + TABLE_DIVIDER
    empty_line = TABLE_DIVIDER + TABLE_DIVIDER.join(
        [pad_centre(" ", max_cell) for i in range(len(header))]) + TABLE_DIVIDER

    if min_encapsulation:
        table_header = TABLE_DIVIDER + TABLE_DIVIDER.join(
            [pad_centre(str(h), max_cell_widths[i]) for i, h in enumerate(header)]) + TABLE_DIVIDER
        empty_line = TABLE_DIVIDER + TABLE_DIVIDER.join(
            [pad_centre(" ", max_cell_widths[i]) for i in range(len(header))]) + TABLE_DIVIDER
    else:
        max_cell_widths = [max_cell for i in range(len(header))]

    print("Header: {h}\nTable Header: {th}".format(h=header, th=table_header))
    fill = "".join([" " for i in range(len(str(fill + len(d))))])
    table_width = l + len(fill) + len(SEPARATOR) + len(TAB) + len(table_header) - (4 * len(TABLE_DIVIDER))
    table_tab = "".join([marker for i in range(len(TAB))])
    if has_dict:
        table_header_title = pad_centre(table_title, l + len(SEPARATOR) - 1)
        m += TAB
        m += "" if not number else fill + SEPARATOR
        m += table_header_title + table_header.rjust(
            table_width - len(table_header_title) - len(fill) - len(SEPARATOR)) + "\n"
    i = 0
    # print("FINAL L: {l}\nFill: {n}<{f}>".format(l=l, n=len(fill), f=fill))
    for k, v in d.items():
        if type(v) not in [list, tuple]:
            v = [v]
        for j, v_elem in enumerate(v):
            ml = str(k).strip()
            orig_ml = ml
            num = str(i + 1)
            if number:
                ml = fill + SEPARATOR + ml
                if j == 0:
                    ml = num.ljust(len(fill)) + ml[len(fill):]
            v_val = v_elem
            if has_dict and type(v_elem) == dict:
                v_val = ""
            ml += str(v_val).rjust(l - len(orig_ml), marker)
            if has_dict:
                ml += table_tab
                if type(v_elem) == dict:
                    keys = {str(k).strip(): v for k, v in v_elem.items()}
                    vals = [keys[key] if key in keys else "" for key in header]
                    ml += TABLE_DIVIDER + TABLE_DIVIDER.join(
                        pad_centre(str(cell), max_cell_widths[i]) for i, cell in enumerate(vals)) + TABLE_DIVIDER
                else:
                    ml += empty_line
            ml += "\n"
            m += TAB + ml
            i += 1
    return m


def money(v):
    # return "$ %.2f" % v
    locale.setlocale(locale.LC_ALL, "")
    m = locale.currency(v, grouping=True)
    i = m.index("$") + 1
    return m[:i] + " " + m[i:]


def money_value(m):
    return float("".join(m[1:].split(",")))


def compute_min_edit_distance(a, b):
    len_a = len(a);
    len_b = len(b)
    x = max(len_a, len_b)
    s = b if x == len_a else a
    m, instructions = min_edit_distance(a, b)
    print(instructions)
    return m


def min_edit_distance(a, b, show_table=False):
    a = a.upper()
    b = b.upper()
    print("Minimum edit Distance to convert \"" + a + "\" to \"" + b + "\"")
    n = len(a) + 2
    m = len(b) + 2
    table = [[0 for j in range(n)] for i in range(m)]
    for i in range(2, max(n, m)):
        if i < n:
            table[0][i] = a[i - 2]
            table[1][i] = i - 1
        if i < m:
            table[i][0] = b[i - 2]
            table[i][1] = i - 1

    for i in range(2, m):
        for j in range(2, n):
            x = table[i][j - 1]
            y = table[i - 1][j - 1]
            z = table[i - 1][j]
            mini = min(x, min(y, z))
            u = table[0][j]
            v = table[i][0]
            if u == v:
                table[i][j] = table[i - 1][j - 1]
            else:
                # System.out.println("x: " + x + ", y: " + y + ", z: " + z + ", min(x, min(y, z): " + mini);
                table[i][j] = mini + 1

    if show_table:
        show(table)
    return table[m - 1][n - 1], table


def show(arr):
    res = "{"
    for i in range(len(arr)):
        res += "{"
        if i > 0:
            res += " "
        for j in range(len(arr[i])):
            if j < len(arr[i]) - 1:
                if i == 0 or j == 0:
                    res += str(arr[i][j]) + ", "
                else:
                    res += str(arr[i][j]) + ", "
            else:
                if i == 0 or j == 0:
                    res += str(arr[i][j])
                else:
                    res += str(arr[i][j])
        if i < len(arr) - 1:
            res += "},\n"
        else:
            res += "}"
    res += "}\n"
    print(res)
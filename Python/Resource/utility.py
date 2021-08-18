from locale import currency, setlocale, LC_ALL
from math import e, ceil, sin, cos, radians
from random import random, choice
import datetime as dt
import shutil
import sys

"""
	General Utility Functions
	Version..............1.10
	Date...........2021-08-17
	Author.......Avery Briggs
"""


def lenstr(x):
    return len(str(x))


def minmax(a, b):
    if a <= b:
        return a, b
    return b, a


def avg(lst):
    try:
        return sum(lst) / max(1, len(lst))
    except TypeError:
        return 0


def median(lst):
    if not isinstance(lst, list) and not isinstance(lst, str):
        raise TypeError("Cannot find median of \"{}\" of type: \"{}\".".format(lst, type(lst)))
    if not lst:
        return None

    lt = lst.copy()
    lt.sort()
    l = len(lt)
    if l == 1:
        return lt
    else:
        h = l // 2
        o = (l % 2) == 1
        f = [] if o else lt[h - 1: h]
        return f + lt[h: h + 1]


def mode(lst):
    if not isinstance(lst, list) and not isinstance(lst, str):
        raise TypeError("Cannot find mode of \"{}\" of type: \"{}\".".format(lst, type(lst)))
    d = {}
    mv = float("-inf")
    for el in lst:
        if el in d:
            v = d[el] + 1
        else:
            v = 1

        d[el] = v
        if v > mv:
            mv = v

    print("mv", mv, "d", d)
    return [k for k, v in d.items() if v == mv]


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
               table_title="", TAB="    ", SEPARATOR="  -  ", TABLE_DIVIDER="|"):
    if not d or not n or type(d) != dict:
        return "None"
    m = "\n{}--  ".format(TAB[:len(TAB) // 2]) + str(n).title() + "  --\n\n"
    fill = 0

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
        max_val = max((max([len(str(v_elem)) for v_elem in v] if v else [0]) if (
                (type(v) == list) or (type(v) == tuple)) else len(
            str(v)) if type(v) != dict else 0), max_val)

    l = max(len(table_title), max(l, (max_key + max_val))) + sep
    has_dict = [(k, v) for k, v in d.items() if type(v) == dict or (type(v) == list and v and type(v[0]) == dict)]
    has_list = any([1 if type(v) in [list, tuple] else 0 for v in d.values()])

    header = []
    max_cell = 0
    max_cell_widths = []

    # print("has_dict: {hd}".format(hd=has_dict))
    if has_list:
        number = True
    for k1, v in has_dict:
        for k2 in v:
            key = str(k2)
            # print("key: {k}".format(k=key))
            if key not in header:
                if type(v) == dict:
                    # print("\t\tNew key: {k}".format(k=key))
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

    # print("Header: {h}\nTable Header: {th}".format(h=header, th=table_header))
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
    setlocale(LC_ALL, "")
    m = currency(v, grouping=True)
    i = m.index("$") + 1
    return m[:i] + " " + m[i:]


def money_value(m):
    return float("".join(m[1:].split(",")))


def percent(v):
    return ("%.2f" % (v * 100)) + " %"


def compute_min_edit_distance(a, b, show=False):
    len_a = len(a)
    len_b = len(b)
    x = max(len_a, len_b)
    s = b if x == len_a else a
    m, instructions = min_edit_distance(a, b, show_table=show)
    # print(instructions)
    return m


def min_edit_distance(a, b, show_table=False):
    a = a.upper()
    b = b.upper()
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
        print("Minimum edit Distance to convert \"" + a + "\" to \"" + b + "\": " + str(table[m - 1][n - 1]))
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


def add_business_days(d, bd, holidays=None):
    if holidays == None:
        holidays = []
    i = 0
    t = dt.datetime(d.year, d.month, d.day)
    # print("holidays: " + str(holidays))
    while i < bd:
        t = t + dt.timedelta(days=1)
        # print("t: " + str(t) + ", (t not in holidays): " + str(t not in holidays))
        if t.weekday() < 5 and t not in holidays:
            i += 1
    return t


def business_days_between(d1, d2, holidays=None):
    business_days = 0
    if holidays == None:
        holidays = []
    date_1 = d1 if type(d1) == dt.datetime else dt.datetime.strptime(d1, "%d-%b-%y")
    date_2 = d2 if type(d2) == dt.datetime else dt.datetime.strptime(d2, "%d-%b-%y")

    date_1, date_2 = minmax(date_1, date_2)

    diff = (date_2 - date_1).days
    temp = date_1
    for i in range(diff):
        temp = date_1 + dt.timedelta(days=i + 1)
        if temp.weekday() < 5 and temp not in holidays:  # Monday == 0, Sunday == 6
            business_days += 1
    i = 0
    while temp.weekday() >= 5 or temp in holidays:
        temp = temp + dt.timedelta(days=1)
        if temp not in holidays:
            business_days += 1
            break
    # print("temp: {temp}\ndate_2: {date_2}\ntemp < date_2: {td2}".format(temp=temp, date_2=date_2, td2=(temp < date_2)))
    # print("business_days: " + str(business_days))
    return business_days


def intersection(a, b):
    res = []
    l = a if len(a) >= len(b) else b
    m = b if len(a) >= len(b) else a
    for i in l:
        if i in m:
            res.append(i)
    return res


def disjoint(a, b):
    overlap = intersection(a, b)
    res = []
    for el in a + b:
        if el not in overlap:
            res.append(el)
    return res


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def same_calendar_day(d1, d2):
    if type(d1) != type(d2) and type(d1) != dt.datetime:
        raise ValueError(
            "Check types of d1: <{d1}> and d2: <{d2}>.\nBoth values must be datetime.datetime objects.".format(d1=d1,
                                                                                                               d2=d2))
    return all([
        d1.year == d2.year,
        d1.month == d2.month,
        d1.day == d2.day
    ])


def pyth(a=None, b=None, c=None):
    if all([a is None, b is None, c is None]):
        return None
    if c is None:
        if a is not None and b is not None:
            return {"a": a, "b": b, "c": (a ** 2 + b ** 2) ** 0.5}
    elif a is None:
        if b is not None and c is not None:
            return {"a": (c ** 2 - b ** 2) ** 0.5, "b": b, "c": c}
    elif b is None:
        if a is not None and c is not None:
            return {"a": a, "b": (c ** 2 - a ** 2) ** 0.5, "c": c}
    return {"a": a, "b": b, "c": c}


def sigmoid(x):
    return 1 / (1 + (e ** -x))


def random_in_range(a, b):
    return ((max(a, b) - min(a, b)) * random()) + min(a, b)


def max_idx(lst):
    max_val = None, float("-inf")
    for i, el in enumerate(lst):
        if el > max_val[1]:
            max_val = i, el
    return max_val


def min_idx(lst):
    min_val = None, float("inf")
    for i, el in enumerate(lst):
        if el < min_val:
            min_val = i, el
    return min_val


# Usage:
# (val, weight) where weight is a float or integer.
# float weights must sum to 1 or less, indicatiing a percentage of 100.
# A whole integer will be considered as a ratio value.
# l1 = [(1, 0.7), (2, 0.3)]  # '1' 70% of the time, '2' 30% of the time
# l2 = [(0, 0.05), (1, 0.05), (2, 0.05), (3, 0.1), (4, 0.2), (5, 0.05), (6, 10), (7, 2), (8, 3)]
# 5% of the time: '0', '1', '2', '5', '3' 10% of the time, '4' 20% of the time, and 10 individual counts of 6, 2 and 7 and 3 counts of 8.
# l3 = [("Avery", 5), ("Jordan", 15), ("Briggs", 2)]
# List of 5 counts of 'Avery', 15 counts of 'Jordan', and 2 counts of 'Briggs'
# weighted_choice(l1)
# Returns a radnom choice from a generated weighted list.
def weighted_choice(weighted_lst):
    item_scalar = 10
    lst_len = 1000
    res = []
    whole = []
    fract = []
    fract_sum = 0
    sum_count = 0
    for el in weighted_lst:
        if isinstance(el, list) or isinstance(el, tuple):
            if len(el) == 2:
                val, weight = el
                if str(weight).startswith("0."):
                    fract.append(el)
                    fract_sum += weight
                    sum_count += weight * lst_len
                else:
                    whole.append(el)
    # print("Whole:", whole)
    # print("Fract:", fract)
    if fract_sum > 1:
        print("Fract:", fract)
        raise ValueError("Fractional weights sum to 1 or less.")

    remaining = lst_len - sum_count
    remaining = remaining if remaining != 0 else 1
    sum_whole = sum([weight for val, weight in whole])
    sum_whole = sum_whole if sum_whole != 0 else 1
    p = sum_whole / remaining

    for val, weight in fract:
        print("item_scalar:", item_scalar, "p:", p, "weight:", weight, "lst_len:", lst_len)
        s = ceil(item_scalar * p * weight * lst_len)
        print("\ts:", s)
        res += [val for i in range(s)]

    for val, weight in whole:
        print("{} x {}".format(weight, val))
        res += [val for i in range(ceil(weight))]

    # print("\tres", res)
    if res:
        print("Choice from:\n\t{}".format(res))
        return choice(res)
    if isinstance(weighted_lst, list) or isinstance(weighted_lst, tuple):
        print("Choice from:\n\t{}".format(weighted_lst))
        return choice(weighted_lst)
    return None


# TODO - Broken test:
#	weighted_choice([(1, 9), 2])


def lbs_kg(lbs):
    """
    lbs_kg(args) -> int() or float()
    Convert N pounds to Kilograms.
    1 Lbs = 0.453592 Kg
    :param lbs: int or float value in pounds.
    :return: float value in kilograms.
    """
    if not isinstance(lbs, int) or isinstance(lbs, float):
        raise ValueError("Cannot convert \"{}\" of type: \"{}\" to kilograms.".format(lbs, type(lbs)))
    return 0.453592 * lbs


def kg_lbs(kg):
    """
    kg_lbs(args) -> int() or float()
    Convert N Kilograms to pounds.
    1 Lbs = 0.453592 Kg
    :param kg: int or float value in kilograms.
    :return: float value in pounds.
    """
    if not isinstance(kg, int) or isinstance(kg, float):
        raise ValueError("Cannot convert \"{}\" of type: \"{}\" to pounds.".format(kg, type(kg)))
    if kg == 0:
        return 0.0
    return 1 / lbs_kg(kg)


def miles_km(miles):
    """
    miles_km(args) -> int() or float()
    Convert N Miles to Kilometers.
    1 Mi = 1.60934 Km
    :param miles: int or float value in miles.
    :return: float value in kilometers.
    """
    if not isinstance(miles, int) or isinstance(miles, float):
        raise ValueError("Cannot convert \"{}\" of type: \"{}\" to miles.".format(miles, type(miles)))
    return 1.60934 * miles


def km_miles(km):
    """
    km_miles(args) -> int() or float()
    Convert N Kilometers to Miles.
    1 Mi = 1.60934 Km.
    :param km: int or float value in kilometers.
    :return: float value in miles.
    """
    if not isinstance(km, int) or isinstance(km, float):
        raise ValueError("Cannot convert \"{}\" of type: \"{}\" to kilometers.".format(km, type(km)))
    if km == 0:
        return 0.0
    return 1 / miles_km(km)


def flatten(lst):
    """
    flatten(args) -> list()
    Flatten a multi-dimensional list into a single dimension.
    Non-list objects are returned in a list.
    :param lst: list object with one or more dimensions.
    :return: list object with one dimension.
    """
    if not isinstance(lst, list):
        return [lst]
    if not lst:
        return lst
    return [*flatten(lst[0]), *flatten(lst[1:])]


# Clamp an number between small and large values.
# Inclusive start, exclusive end.
def clamp(s, v, l):
    return max(s, min(v, l))


# Darken an RGB color using a proportion p (0-1)
def darken(c, p):
    r, g, b = c
    r = clamp(0, round(r - (255 * p)), 255)
    g = clamp(0, round(g - (255 * p)), 255)
    b = clamp(0, round(b - (255 * p)), 255)
    return r, g, b


# Brighten an RGB color using a proportion p (0-1)
def brighten(c, p):
    r, g, b = c
    r = clamp(0, round(r + (255 * p)), 255)
    g = clamp(0, round(g + (255 * p)), 255)
    b = clamp(0, round(b + (255 * p)), 255)
    return r, g, b


# return random RGB color
def random_color():
    return (
        random.randint(10, 245),
        random.randint(10, 245),
        random.randint(10, 245)
    )


# Rotate a 2D point about the origin, a given amount of degrees. Counterclockwise
def rotate_on_origin(px, py, theta):
    t = radians(theta)
    x = (px * cos(t)) - (py * sin(t))
    y = (px * sin(t)) + (py * cos(t))
    return x, y


# Rotate a 2D point around any central point, a given amount of degrees. Counterclockwise
def rotate_point(cx, cy, px, py, theta):
    xd = 0 - cx
    yd = 0 - cy
    rx, ry = rotate_on_origin(px + xd, py + yd, theta)
    return rx - xd, ry - yd


def bar(a, b, c=10):
    if not isinstance(c, int) or c < 1:
        c = 10
    return "{} |".format(percent(a / b)) + "".join(["#" if i < int((c * a) / b) else " " for i in range(c)]) + "|"


def lstindex(lst, target):
    for i, val in enumerate(lst):
        if val == target:
            return i
    return -1


def cos_x(degrees, amplitude=1, period=1, phase_shift=0, vertical_shift=0):
    return (amplitude * (cos(period * (degrees + phase_shift)))) + vertical_shift


def sin_x(degrees, amplitude=1, period=1, phase_shift=0, vertical_shift=0):
    return (amplitude * (sin(period * (degrees + phase_shift)))) + vertical_shift


def get_terminal_columns():
    return shutil.get_terminal_size().columns


def is_imported(module_name):
    return module_name in sys.modules


def distance(start, end):
    return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5


def dot_product(a, b):
    return (a[0] * b[0]) + (b[0] * b[1])


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.tupl = ((x1, y1), (x2, y2))
        self.p1 = x1, y1
        self.p2 = x2, y2
        div = x2 - x1
        if div != 0:
            self.m = (y2 - y1) / div
        else:
            self.m = "undefined"
        if self.m != "undefined":
            self.b = y1 - (x1 * self.m)
        else:
            self.b = "undefined"
        self.abc = (y2 - y1, x1 - x2, ((y2 - y1) * x1) + ((x1 - x2) * y1))

    def collide_point(self, x, y, is_segment=True):
        if self.m == "undefined" or self.b == "undefined":
            return self.x1 == x and self.x2 == x
        if not is_segment:
            return y == (self.m * x) + self.b
        return y == (self.m * x) + self.b and (self.x1 <= x <= self.x2 or self.x2 <= x <= self.x1) and (
                    self.y1 <= y <= self.y2 or self.y2 <= y <= self.y1)

    def collide_line(self, line):
        assert isinstance(line, Line)
        a1, b1, c1 = self.abc
        a2, b2, c2 = line.abc
        det = a1 * b2 - a2 * b1
        if det == 0:
            # Lines are parallel
            return None
        else:
            x = (b2 * c1 - b1 * c2) / det
            y = (a1 * c2 - a2 * c1) / det
            if self.collide_point(x, y) and line.collide_point(x, y):
                return x, y
            else:
                return None

    def __repr__(self):
        if self.m == "undefined":
            return "x = {}".format(self.x1)
        return "y = {}x + {}".format("%.2f" % str(self.m), self.b)


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.tupl = (x, y, w, h)
        self.top = y
        self.left = x
        self.bottom = y + h
        self.right = x + w
        self.center = x + (w / 2), y + (h / 2)
        self.top_left = x, y
        self.top_right = x + w, y
        self.bottom_left = x, y + h
        self.bottom_right = x + w, y + h

    def collide_line(self, line):
        assert isinstance(line, Line)
        if self.collide_point(*line.p1) or self.collide_point(*line.p1):
            return True
        else:
            top = Line(self.left, self.top, self.right, self.top)
            bottom = Line(self.left, self.bottom, self.right, self.bottom)
            left = Line(self.left, self.top, self.left, self.bottom)
            right = Line(self.right, self.top, self.right, self.bottom)
            return any([
                line.collide_line(top),
                line.collide_line(bottom),
                line.collide_line(left),
                line.collide_line(right)
            ])

    def collide_point(self, x, y):
        return all([
            self.x <= x <= self.right,
            self.y <= y <= self.bottom
        ])

    def __repr__(self):
        return "<rect(" + ", ".join(list(map(str, [self.x, self.y, self.width, self.height]))) + ")>"
from locale import currency, setlocale, LC_ALL
from math import e, ceil, sin, cos, radians
from random import random, choice, randint
from plyer import notification
import datetime as dt
import shutil
import sys
import os

"""
	General Utility Functions
	Version..............1.38
	Date...........2022-01-24
	Author.......Avery Briggs
"""


def func_def():
    pass


class Foo:
    def __init__(self):
        pass

    def f1(self):
        pass

    def f2(self, f):
        pass


FOO_OBJ = Foo()


def isfunc(f):
    return isinstance(f, type(func_def))


def isclassmethod(m):
    return isinstance(m, type(FOO_OBJ.f1))


def lenstr(x):
    return len(str(x))


def minmax(a, b):
    if a <= b:
        return a, b
    return b, a


def maxmin(a, b):
    if a < b:
        return b, a
    return a, b


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


def money(v, int_only=False):
    # return "$ %.2f" % v
    setlocale(LC_ALL, "")
    m = currency(v, grouping=True)
    i = m.index("$") + 1
    if int_only:
        return (m[:i] + " " + m[i:]).split(".")[0]
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
    if holidays is None:
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
    if holidays is None:
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
        if j in m:
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


def isnumber(value):
    if isinstance(value, int) or isinstance(value, float):
        return True
    if isinstance(value, str):
        if value.count("-") < 2:
            if value.replace("-", "").isnumeric():
                return True
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
        # print("item_scalar:", item_scalar, "p:", p, "weight:", weight, "lst_len:", lst_len)
        s = ceil(item_scalar * p * weight * lst_len)
        # print("\ts:", s)
        res += [val for i in range(s)]

    for val, weight in whole:
        # print("{} x {}".format(weight, val))
        res += [val for i in range(ceil(weight))]

    # print("\tres", res)
    if res:
        # print("Choice from:\n\t{}".format(res))
        return choice(res)
    if isinstance(weighted_lst, list) or isinstance(weighted_lst, tuple):
        # print("Choice from:\n\t{}".format(weighted_lst))
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
        randint(10, 245),
        randint(10, 245),
        randint(10, 245)
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


def reduce(lst, p, how="left"):
    if not isinstance(how, str):
        how = str(how)
    how = how.lower()
    if how not in ["left", "center", "right", "distributed"]:
        how = "distributed"

    l = len(lst)
    n_items = round(l * p)
    if n_items <= 0:
        return []

    if how == "left":
        return lst[:n_items]
    elif how == "center":
        a = (l - n_items) // 2
        b = (l + n_items) // 2
        if l % 2 == 1:
            b += 1
        return lst[a:b]
    elif how == "right":
        return lst[l - n_items:]
    else:
        return lst[0: l: l // n_items]


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.is_init = False
        self.tupl = None
        self.p1 = None
        self.p2 = None
        self.m = None
        self.b = None
        self.abc = None
        self.init(x1, y1, x2, y2)

    def init(self, x1, y1, x2, y2):
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
        self.is_init = True

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
            sx1, sy1 = self.p1
            sx2, sy2 = self.p2
            sx1, sx2 = minmax(sx1, sx2)
            sy1, sy2 = minmax(sy1, sy2)
            lx1, ly1 = line.p1
            lx2, ly2 = line.p2
            lx1, lx2 = minmax(lx1, lx2)
            ly1, ly2 = minmax(ly1, ly2)
        #         if self.collide_point(x, y) and line.collide_point(x,
        #                                                            y) and self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2 and line.x1 <= x <= line.x2 and line.y1 <= y <= line.y2:

        if self.collide_point(x, y) and line.collide_point(x,
                                                           y) and sx1 <= x <= sx2 and sy1 <= y <= sy2 and lx1 <= x <= lx2 and ly1 <= y <= ly2:
            return x, y
        else:
            return None

    def __eq__(self, other):
        return isinstance(other, Line) and (all([
            self.x1 == other.x1,
            self.y1 == other.y1,
            self.x2 == other.x2,
            self.y2 == other.y2
        ]) or all([
            self.x1 == other.x2,
            self.y1 == other.y2,
            self.x2 == other.x1,
            self.y2 == other.y1
        ]))

    # comparison object "other" must be a tuple of:
    #   (x, y, none_result) -> None comparisons return none_result
    #   (x, y) -> None comparisons throw TypeErrors
    def __lt__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            if len(other) == 2:
                if all([isinstance(x, int) or isinstance(x, float) for x in other]):
                    ox, oy = other
                    return oy < self.y_at_x(ox)
            elif len(other) == 3:
                if all([isinstance(x, int) or isinstance(x, float) for x in other[:2]]):
                    if isinstance(other[2], bool) or (isinstance(other[2], int) and other[2] in [0, 1]):
                        ox, oy, none_result = other
                        v = self.y_at_x(ox)
                        # return (oy < v) if v is not None else bool(none_result)
                        return (oy < v) if v is not None else (ox < self.x_at_y(oy))
        raise TypeError(
            "Cannot compare \"{}\" of type with Line.\nRequires tuple / list: (x, y)".format(other, type(other)))

    # comparison object "other" must be a tuple of:
    #   (x, y, none_result) -> None comparisons return none_result
    #   (x, y) -> None comparisons throw TypeErrors
    def __le__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            if len(other) == 2:
                if all([isinstance(x, int) or isinstance(x, float) for x in other]):
                    ox, oy = other
                    return oy <= self.y_at_x(ox)
            elif len(other) == 3:
                if all([isinstance(x, int) or isinstance(x, float) for x in other[:2]]):
                    if isinstance(other[2], bool) or (isinstance(other[2], int) and other[2] in [0, 1]):
                        ox, oy, none_result = other
                        v = self.y_at_x(ox)
                        # return (oy <= v) if v is not None else bool(none_result)
                        return (oy <= v) if v is not None else (ox <= self.x_at_y(oy))
        raise TypeError(
            "Cannot compare \"{}\" of type with Line.\nRequires tuple / list: (x, y)".format(other, type(other)))

    # comparison object "other" must be a tuple of:
    #   (x, y, none_result) -> None comparisons return none_result
    #   (x, y) -> None comparisons throw TypeErrors
    def __gt__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            if len(other) == 2:
                if all([isinstance(x, int) or isinstance(x, float) for x in other]):
                    ox, oy = other
                    return oy > self.y_at_x(ox)
            elif len(other) == 3:
                if all([isinstance(x, int) or isinstance(x, float) for x in other[:2]]):
                    if isinstance(other[2], bool) or (isinstance(other[2], int) and other[2] in [0, 1]):
                        ox, oy, none_result = other
                        v = self.y_at_x(ox)
                        # return (oy > v) if v is not None else bool(none_result)
                        return (oy > v) if v is not None else (ox > self.x_at_y(oy))
        raise TypeError(
            "Cannot compare \"{}\" of type with Line.\nRequires tuple / list: (x, y)".format(other, type(other)))

    # comparison object "other" must be a tuple of:
    #   (x, y, none_result) -> None comparisons return none_result
    #   (x, y) -> None comparisons throw TypeErrors
    def __ge__(self, other):
        if isinstance(other, tuple) or isinstance(other, list):
            if len(other) == 2:
                if all([isinstance(x, int) or isinstance(x, float) for x in other]):
                    ox, oy = other
                    return oy >= self.y_at_x(ox)
            elif len(other) == 3:
                if all([isinstance(x, int) or isinstance(x, float) for x in other[:2]]):
                    if isinstance(other[2], bool) or (isinstance(other[2], int) and other[2] in [0, 1]):
                        ox, oy, none_result = other
                        v = self.y_at_x(ox)
                        # return (oy >= v) if v is not None else bool(none_result)
                        return (oy >= v) if v is not None else (ox >= self.x_at_y(oy))
        raise TypeError(
            "Cannot compare \"{}\" of type with Line.\nRequires tuple / list: (x, y)".format(other, type(other)))

    def y_at_x(self, x):
        if self.m == "undefined":
            # return None
            return None
        if self.m == 0:
            return self.y1
        return (self.m * x) + self.b

    def x_at_y(self, y):
        if self.m == "undefined":
            return self.x1
        if self.m == 0:
            return None
        return (y - self.b) / self.m

    def translate(self, x, y):
        self.x1 += x
        self.x2 += x
        self.y1 += y
        self.y2 += y
        self.init(self.x1, self.y1, self.x2, self.y2)

    def translated(self, x, y):
        r = Line(self.x1, self.y1, self.x2, self.y2)
        r.translate(x, y)
        return r

    def __iter__(self):
        lst = [self.p1, self.p2]
        for val in lst:
            yield val

    def __repr__(self):
        if self.m == "undefined":
            return "x = {}".format(self.x1)
        if self.m == 0:
            return "y = {}".format(self.b)
        return "y = {}x + {}".format("%.2f" % self.m, self.b)


# class Rect:
#     def __init__(self, x, y=None, w=None, h=None):
#         self.x = x
#         self.y = y
#         self.width = w
#         self.height = h
#         if any([y is None, w is None, h is None]):
#             if is_imported("pygame"):
#                 if isinstance(x, pygame.Rect):
#                     x = x.left
#                     y = x.y
#                     w = x.width
#                     y = x.height
#                 else:
#                     raise ValueError("Cannot create a Rect object with <{}>.\nExpected a pygame.Rect object.".format(x))
#             else:
#                 ValueError("Cannot create a rect object with <{}>.\npygame module is not imported.".format(x))
#         self.is_init = False
#         self.tupl = None
#         self.top = None
#         self.left = None
#         self.bottom = None
#         self.right = None
#         self.center = None
#         self.top_left = None
#         self.top_right = None
#         self.bottom_left = None
#         self.bottom_right = None
#         self.top_line = None
#         self.left_line = None
#         self.right_line = None
#         self.bottom_line = None
#         self.center_top = None
#         self.center_left = None
#         self.center_right = None
#         self.center_bottom = None
#         self.area = None
#         self.perimetre = None
#         self.init(x, y, w, h)
#
#     def init(self, x, y, w, h):
#         self.x = x
#         self.y = y
#         self.width = w
#         self.height = h
#         self.tupl = (x, y, w, h)
#         self.top = y
#         self.left = x
#         self.bottom = y + h
#         self.right = x + w
#         self.center = x + (w / 2), y + (h / 2)
#         self.top_left = x, y
#         self.top_right = x + w, y
#         self.bottom_left = x, y + h
#         self.bottom_right = x + w, y + h
#         self.center_top = self.center[0], y
#         self.center_left = x, self.center[1]
#         self.center_right = x + w, self.center[1]
#         self.center_bottom = self.center[0], y + h
#         self.area = w * h
#         self.perimetre = 2 * (w + h)
#         self.top_line = Line(*self.top_left, *self.top_right)
#         self.left_line = Line(*self.top_left, *self.bottom_left)
#         self.right_line = Line(*self.top_right, *self.bottom_right)
#         self.bottom_line = Line(*self.bottom_left, *self.bottom_right)
#         self.is_init = True
#
#     def __iter__(self):
#         lst = [self.x, self. y, self.width, self.height]
#         for val in lst:
#             yield val
#
#     def collide_rect(self, rect, strictly_inside=True):
#         if strictly_inside:
#             return all([
#                 self.left < rect.left,
#                 self.right > rect.right,
#                 self.top < rect.top,
#                 self.bottom > rect.bottom
#             ])
#         else:
#             return any([
#                 self.collide_point(*rect.top_left),
#                 self.collide_point(*rect.top_right),
#                 self.collide_point(*rect.bottom_left),
#                 self.collide_point(*rect.bottom_right)
#             ])
#
#     def collide_line(self, line):
#         assert isinstance(line, Line)
#         if self.collide_point(*line.p1) or self.collide_point(*line.p1):
#             return True
#         else:
#             top = Line(self.left, self.top, self.right, self.top)
#             bottom = Line(self.left, self.bottom, self.right, self.bottom)
#             left = Line(self.left, self.top, self.left, self.bottom)
#             right = Line(self.right, self.top, self.right, self.bottom)
#             return any([
#                 line.collide_line(top),
#                 line.collide_line(bottom),
#                 line.collide_line(left),
#                 line.collide_line(right)
#             ])
#
#     def collide_point(self, x, y):
#         return all([
#             self.x <= x <= self.right,
#             self.y <= y <= self.bottom
#         ])
#
#     def translate(self, x, y):
#         if not self.is_init:
#             self.init(self.x, self.y, self.width, self.height)
#         self.x += x
#         self.y += y
#         self.init(self.x, self.y, self.width, self.height)
#
#     def translated(self, x, y):
#         r = Rect(self.x, self.y, self.width, self.height)
#         r.translate(x, y)
#         return r
#
#     def scale(self, w_factor, h_factor):
#         self.init(self.x, self.y, self.width * w_factor, self.height * h_factor)
#
#     def scaled(self, w_factor, h_factor):
#         r = Rect(self.x, self.y, self.width, self.height)
#         r.scale(w_factor, h_factor)
#         return r
#
#     def move(self, rect):
#         self.init(rect.x, rect.y, rect.width, rect.height)
#
#     def resize(self, rect):
#         self.init(rect.x, rect.y, rect.width, rect.height)
#
#     def __repr__(self):
#         return "<rect(" + ", ".join(list(map(str, [self.x, self.y, self.width, self.height]))) + ")>"


#            x2,y2              x1,y1 ---- x2,y2
#  x1,y1  /    |                  |          |
#    |       x3,y3              x4,y4 ---- x3,y3
#  x4,y4  /

class Rect2:
    def __init__(self, x, y=None, w=None, h=None, a=0):
        self.x = None
        self.y = None
        self.w = None
        self.h = None
        self.width = None
        self.height = None
        self.angle = None

        self.x1, self.y1 = None, None
        self.x2, self.y2 = None, None
        self.x3, self.y3 = None, None
        self.x4, self.y4 = None, None
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.l4 = None
        self.a = a % 360
        self.angle = a % 360
        self.tupl = None
        self.max_encapsulating_rect = None
        self.min_encapsulating_rect = None
        self.top = None
        self.left = None
        self.bottom = None
        self.right = None
        self.center = None
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None
        self.center_top = None
        self.center_left = None
        self.center_right = None
        self.center_bottom = None
        self.area = None
        self.perimeter = None
        self.top_line = None
        self.right_line = None
        self.bottom_line = None
        self.left_line = None

        self.diagonal_p1_p3 = None
        self.diagonal_p3_p1 = None
        self.diagonal_p2_p4 = None
        self.diagonal_p4_p2 = None

        self.init(x, y, w, h, a)

    def init(self, x, y, w, h, a):
        if w < 0:
            raise ValueError("width value: \"{}\" must not be less than 0.".format(w))
        if h < 0:
            raise ValueError("height value: \"{}\" must not be less than 0.".format(h))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.width = w
        self.height = h
        self.angle = a

        self.x1, self.y1 = x, y
        self.x2, self.y2 = rotate_point(x, y, x + w, y, a)
        self.x3, self.y3 = rotate_point(x, y, x + w, y + h, a)
        self.x4, self.y4 = rotate_point(x, y, x, y + h, a)
        self.p1 = self.x1, self.y1
        self.p2 = self.x2, self.y2
        self.p3 = self.x3, self.y3
        self.p4 = self.x4, self.y4
        self.l1 = Line(self.x1, self.y1, self.x2, self.y2)
        self.l2 = Line(self.x2, self.y2, self.x3, self.y3)
        self.l3 = Line(self.x3, self.y3, self.x4, self.y4)
        self.l4 = Line(self.x4, self.y4, self.x1, self.y1)
        self.top_line = self.l1
        self.right_line = self.l2
        self.bottom_line = self.l3
        self.left_line = self.l4

        # self.tupl = (self.p1, self.p2, self.p3, self.p4)
        self.tupl = (self.x, self.y, self.w, self.h)
        if a == 0:
            self.max_encapsulating_rect = self
            self.min_encapsulating_rect = self
        else:
            xs = [self.x1, self.x2, self.x3, self.x4]
            ys = [self.y1, self.y2, self.y3, self.y4]
            xs.sort()
            ys.sort()
            self.max_encapsulating_rect = Rect2(xs[0], ys[0], xs[3] - xs[0], ys[3] - ys[0], 0)
            self.min_encapsulating_rect = Rect2(xs[1], ys[1], xs[2] - xs[1], ys[2] - ys[1], 0)

        # Using max_encapsulating_rect for calculations
        self.top = self.max_encapsulating_rect.y
        self.left = self.max_encapsulating_rect.x
        self.bottom = self.max_encapsulating_rect.y + self.max_encapsulating_rect.height
        self.right = self.max_encapsulating_rect.x + self.max_encapsulating_rect.width
        self.center = self.left + (self.max_encapsulating_rect.width / 2), self.top + (
                self.max_encapsulating_rect.height / 2)
        self.top_left = self.left, self.top
        self.top_right = self.right, self.top
        self.bottom_left = self.left, self.bottom
        self.bottom_right = self.bottom, self.right
        self.center_top = self.center[0], self.top
        self.center_left = self.left, self.center[1]
        self.center_right = self.right, self.center[1]
        self.center_bottom = self.center[0], self.bottom

        self.diagonal_p1_p3 = Line(*self.p1, *self.p3)
        self.diagonal_p3_p1 = Line(*self.p3, *self.p2)
        self.diagonal_p2_p4 = Line(*self.p2, *self.p4)
        self.diagonal_p4_p2 = Line(*self.p4, *self.p2)

        # Calculations done on the main rect object
        self.area = w * h
        self.perimeter = 2 * (w + h)

    def __iter__(self):
        lst = [self.x, self.y, self.width, self.height, self.angle]
        for val in lst:
            yield val

    def collide_point(self, x, y, strictly_inside=False):
        if not all([
            any([
                isinstance(x, int),
                isinstance(x, float)
            ]),
            any([
                isinstance(y, int),
                isinstance(y, float)
            ])
        ]):
            raise TypeError(
                "Cannot determine if x=\"{}\" of type: \"{}\" y=\"{}\" of type: \"{}\" collides with Rect object. Requires int and / or float objects.".format(
                    x, type(x), y, type(y)))
        if strictly_inside:
            return all([
                (x, y, 1) < self.l1,
                (x, y, 1) > self.l2,
                (x, y, 1) > self.l3,
                (x, y, 1) < self.l4
            ])
        else:
            return all([
                (x, y, 1) <= self.l1,
                (x, y, 1) >= self.l2,
                (x, y, 1) >= self.l3,
                (x, y, 1) <= self.l4
            ])

    def collide_line(self, line, strictly_inside=False):
        if not isinstance(line, Line):
            raise TypeError(
                "Cannot determine if line=\"{}\" of type: \"{}\" collides with Rect object. Requires Line object.".format(
                    line, type(line)))
        if strictly_inside:
            return all([
                self.collide_point(*line.p1),
                self.collide_point(*line.p2)
            ])
        else:
            return any([
                self.collide_point(*line.p1),
                self.collide_point(*line.p2)
            ])

    def collide_rect(self, rect, strictly_inside=False):
        if not isinstance(rect, Rect2):
            raise TypeError(
                "Cannot determine if rect=\"{}\" of type: \"{}\" collides with Rect object. Requires Rect object.".format(
                    rect, type(rect)))
        if strictly_inside:
            return all([
                self.collide_point(*rect.p1),
                self.collide_point(*rect.p2),
                self.collide_point(*rect.p3),
                self.collide_point(*rect.p4)
            ])
        else:
            return any([
                self.collide_point(*rect.p1),
                self.collide_point(*rect.p2),
                self.collide_point(*rect.p3),
                self.collide_point(*rect.p4)
            ])

    def translate(self, x, y):
        self.init(self.x + x, self.y + y, self.width, self.height, self.angle)

    def translated(self, x, y):
        return Rect2(self.x + x, self.y + y, self.width, self.height, self.angle)

    def scale(self, w, h):
        w = abs(w)
        h = abs(h)
        self.init(self.x, self.y, self.width * w, self.height * h, self.angle)

    def scaled(self, x, y):
        r = Rect2(*self)
        r.scale(x, y)
        return r

    def rotate(self, a):
        self.init(self.x, self.y, self.width, self.height, self.angle + a)

    def rotated(self, a):
        r = Rect2(*self)
        r.rotate(a)
        return r

    #     if any([y is None, w is None, h is None]):
    #         if is_imported("pygame"):
    #             if isinstance(x, pygame.Rect):
    #                 x = x.left
    #                 y = x.y
    #                 w = x.width
    #                 y = x.height
    #             else:
    #                 raise ValueError("Cannot create a Rect object with <{}>.\nExpected a pygame.Rect object.".format(x))
    #         else:
    #             ValueError("Cannot create a rect object with <{}>.\npygame module is not imported.".format(x))
    #     self.is_init = False
    #     self.tupl = None
    #     self.top = None
    #     self.left = None
    #     self.bottom = None
    #     self.right = None
    #     self.center = None
    #     self.top_left = None
    #     self.top_right = None
    #     self.bottom_left = None
    #     self.bottom_right = None
    #     self.top_line = None
    #     self.left_line = None
    #     self.right_line = None
    #     self.bottom_line = None
    #     self.center_top = None
    #     self.center_left = None
    #     self.center_right = None
    #     self.center_bottom = None
    #     self.area = None
    #     self.perimetre = None
    #     self.init(x, y, w, h)
    #
    # def init(self, x, y, w, h):
    #     self.x = x
    #     self.y = y
    #     self.width = w
    #     self.height = h
    #     self.tupl = (x, y, w, h)
    #     self.top = y
    #     self.left = x
    #     self.bottom = y + h
    #     self.right = x + w
    #     self.center = x + (w / 2), y + (h / 2)
    #     self.top_left = x, y
    #     self.top_right = x + w, y
    #     self.bottom_left = x, y + h
    #     self.bottom_right = x + w, y + h
    #     self.center_top = self.center[0], y
    #     self.center_left = x, self.center[1]
    #     self.center_right = x + w, self.center[1]
    #     self.center_bottom = self.center[0], y + h
    #     self.area = w * h
    #     self.perimetre = 2 * (w + h)
    #     self.top_line = Line(*self.top_left, *self.top_right)
    #     self.left_line = Line(*self.top_left, *self.bottom_left)
    #     self.right_line = Line(*self.top_right, *self.bottom_right)
    #     self.bottom_line = Line(*self.bottom_left, *self.bottom_right)
    #     self.is_init = True
    #
    # def __iter__(self):
    #     lst = [self.x, self. y, self.width, self.height]
    #     for val in lst:
    #         yield val
    #
    # def collide_rect(self, rect, strictly_inside=True):
    #     if strictly_inside:
    #         return all([
    #             self.left < rect.left,
    #             self.right > rect.right,
    #             self.top < rect.top,
    #             self.bottom > rect.bottom
    #         ])
    #     else:
    #         return any([
    #             self.collide_point(*rect.top_left),
    #             self.collide_point(*rect.top_right),
    #             self.collide_point(*rect.bottom_left),
    #             self.collide_point(*rect.bottom_right)
    #         ])
    #
    # def collide_line(self, line):
    #     assert isinstance(line, Line)
    #     if self.collide_point(*line.p1) or self.collide_point(*line.p1):
    #         return True
    #     else:
    #         top = Line(self.left, self.top, self.right, self.top)
    #         bottom = Line(self.left, self.bottom, self.right, self.bottom)
    #         left = Line(self.left, self.top, self.left, self.bottom)
    #         right = Line(self.right, self.top, self.right, self.bottom)
    #         return any([
    #             line.collide_line(top),
    #             line.collide_line(bottom),
    #             line.collide_line(left),
    #             line.collide_line(right)
    #         ])
    #
    # def collide_point(self, x, y):
    #     return all([
    #         self.x <= x <= self.right,
    #         self.y <= y <= self.bottom
    #     ])
    #
    # def translate(self, x, y):
    #     if not self.is_init:
    #         self.init(self.x, self.y, self.width, self.height)
    #     self.x += x
    #     self.y += y
    #     self.init(self.x, self.y, self.width, self.height)
    #
    # def translated(self, x, y):
    #     r = Rect(self.x, self.y, self.width, self.height)
    #     r.translate(x, y)
    #     return r
    #
    # def scale(self, w_factor, h_factor):
    #     self.init(self.x, self.y, self.width * w_factor, self.height * h_factor)
    #
    # def scaled(self, w_factor, h_factor):
    #     r = Rect(self.x, self.y, self.width, self.height)
    #     r.scale(w_factor, h_factor)
    #     return r
    #
    # def move(self, rect):
    #     self.init(rect.x, rect.y, rect.width, rect.height)
    #
    # def resize(self, rect):
    #     self.init(rect.x, rect.y, rect.width, rect.height)

    def __repr__(self):
        return "<rect(p1:({}), p2:({}), p3:({}), p4:({}))>".format(self.p1, self.p2, self.p3, self.p4)


def date_suffix(day):
    s_day = str(day)
    if s_day[-1] == "1":
        res = "st"
        if len(s_day) > 1:
            if s_day[-2] == "1":
                res = "th"
    elif s_day[-1] == "2":
        res = "nd"
        if len(s_day) > 1:
            if s_day[-2] == "1":
                res = "th"
    elif s_day[-1] == "3":
        res = "rd"
        if len(s_day) > 1:
            if s_day[-2] == "1":
                res = "th"
    else:
        res = "th"
    return res


# Takes "2021-08-03" -> August 3rd, 2021
def date_str_format(date_str):
    date_obj = dt.datetime.fromisoformat(date_str)
    suffix = date_suffix(date_obj.day)
    res = dt.datetime.strftime(date_obj, "%B %d###, %Y").replace("###", suffix)
    s_res = res.split(" ")
    x = s_res[1] if s_res[1][0] != "0" else s_res[1][1:]
    res = " ".join([s_res[0], x, s_res[2]])
    return res


# Appends a counter '(1)' to a given file path to avoid overwriting.
def next_available_file_name(path):
    counter = 0
    path.replace("\\", "/")
    og_path = path
    while os.path.exists(path):
        counter += 1
        spl = og_path.split(".")
        path = ".".join(spl[:-1]) + " ({}).".format(counter) + spl[-1]
    path.replace("/", "\\")
    return path


# leap year calculation: https://www.timeanddate.com/date/leapyear.html
def random_date(start_year=1, end_year=10000, start_m=None, start_d=None):
    start_year, end_year = minmax(start_year, end_year)
    start_year = clamp(1, start_year, end_year)
    end_year = clamp(start_year + 1, end_year + 1, 10000)

    r_y = list(range(start_year, end_year))
    r_m = list(range(1, 13))
    r_d = list(range(1, 32))
    r_dsm = list(range(1, 31))
    r_df = list(range(1, 29))
    r_dfl = list(range(1, 30))
    r_sm = [2, 4, 6, 9, 11]
    y = choice(r_y)
    m = choice(r_m)
    if start_m in r_m:
        m = start_m
    if m in r_sm:
        d = choice(r_dsm)
        if start_d in r_dsm:
            d = start_d
    else:
        d = choice(r_d)
        if start_d in r_d:
            d = start_d

    if m == 2:
        d = choice(r_df)
        if start_d in r_df:
            d = start_d
        if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0):
            d = choice(r_dfl)
            if start_d in r_dfl:
                d = start_d

    return "{}-{}-{}".format(("0000" + str(y))[-4:], ("00" + str(m))[-2:], ("00" + str(d))[-2:])


def is_date(date_in, fmt="%Y-%m-%d"):
    if isinstance(date_in, dt.datetime) or isinstance(date_in, dt.date):
        return True
    try:
        d = dt.datetime.strptime(date_in, fmt)
        return True
    except TypeError:
        print("Cannot determine if date param \"{}\" is a valid date using datetime format: {}".format(date_in, fmt))
    except ValueError:
        print("Cannot determine if date param \"{}\" is a valid date using datetime format: {}".format(date_in, fmt))
    return False


def first_of_day(date_in):
    assert isinstance(date_in, dt.datetime)
    return dt.datetime(date_in.year, date_in.month, date_in.day)


def first_of_week(date_in):
    assert isinstance(date_in, dt.datetime)
    print("date_in:", date_in)
    # return dt.datetime.fromisoformat("2022-02-02")
    wd = 0 if date_in.isocalendar()[2] == 7 else date_in.isocalendar()[2]
    return date_in + dt.timedelta(days=-wd)
    # return dt.datetime.fromisocalendar(date_in.isocalendar()[0], date_in.isocalendar()[1], 1) + dt.timedelta(hours=date_in.hour, minutes=date_in.minute, seconds=date_in.second)
    # return dt.datetime(date_in.year, date_in.month, 1, date_in.hour, date_in.minute, date_in.second)


def first_of_month(date_in):
    assert isinstance(date_in, dt.datetime)
    return dt.datetime(date_in.year, date_in.month, 1, date_in.hour, date_in.minute, date_in.second)


def alert_colour(x, n):
    assert isnumber(x), "Parameter \"x\": ({}) needs to be a number".format(x)
    assert isnumber(n), "Parameter \"n\": ({}) needs to be a number".format(n)
    assert x <= n, "Parameter \"x\": ({}) needs to be less than or equal to parameter \"n\": ({})".format(x, n)
    assert 0 < n, "Parameter \"n\": ({}) must be non-zero and positive".format(n)
    t_diff = 255
    x = abs(x / n) * t_diff
    return x, 255 - x, 0


def notify(message, title="", app_icon=None, timeout=5):
    if app_icon is not None:
        notification.notify(
            title=title,
            message=message,
            app_icon=(app_icon),
            timeout=timeout  # seconds
        )
    else:
        notification.notify(
            title=title,
            message=message,
            timeout=timeout  # seconds
        )


BLK_ONE = "1", "  1  \n  1  \n  1  \n  1  \n  1  "
BLK_TWO = "2", "22222\n    2\n22222\n2    \n22222"
BLK_THREE = "3", "33333\n    3\n  333\n    3\n33333"
BLK_FOUR = "4", "    4\n4   4\n44444\n    4\n    4"
BLK_FIVE = "5", "55555\n5     \n55555\n    5\n55555"
BLK_SIX = "6", "66666\n6    \n66666\n6   6\n66666"
BLK_SEVEN = "7", "77777\n    7\n    7\n    7\n    7"
BLK_EIGHT = "8", "88888\n8   8\n88888\n8   8\n88888"
BLK_NINE = "9", "99999\n9   9\n99999\n    9\n    9"
BLK_ZERO = "0", "00000\n00  0\n0 0 0\n0  00\n00000"
BLK_A = "A", "  A  \n A A \nAA AA\nAAAAA\nA   A"
BLK_B = "B", "BBBB \nB  BB\nBBBB \nB   B\nBBBBB"
BLK_C = "C", " CCCC\nC    \nC    \nC    \n CCCC"
BLK_D = "D", "DDDD \nD   D\nD   D\nD   D\nDDDD "
BLK_E = "E", "EEEEE\nE    \nEEE  \nE    \nEEEEE"
BLK_F = "F", "FFFFF\nF    \nFFF  \nF    \nF    "
BLK_G = "G", "GGGGG\nG    \nG  GG\nG   G\nGGGGG"
BLK_H = "H", "H   H\nH   H\nHHHHH\nH   H\nH   H"
BLK_I = "I", "IIIII\n  I  \n  I  \n  I  \nIIIII"
BLK_J = "J", "JJJJJ\n  J  \n  J  \nJ J  \nJJJ  "
BLK_K = "K", "K   K\nK  K \nKKK  \nK  K \nK   K"
BLK_L = "L", "L    \nL    \nL    \nL    \nLLLLL"
BLK_M = "M", " M M \nMMMMM\nM M M\nM M M\nM M M"
BLK_N = "N", "N   N\nNN  N\nN N N\nN  NN\nN   N"
BLK_O = "O", " OOO \nO   O\nO   O\nO   O\n OOO "
BLK_P = "P", "PPPP \nP   P\nPPPP \nP    \nP    "
BLK_Q = "Q", " QQQ \nQ   Q\nQ   Q\nQ  QQ\n QQQQ"
BLK_R = "R", "RRRR \nR   R\nRRRR \nR  R \nR   R"
BLK_S = "S", " SSS \nS    \n SSS \n    S\n SSS "
BLK_T = "T", "TTTTT\n  T  \n  T  \n  T  \n  T  "
BLK_U = "U", "U   U\nU   U\nU   U\nU   U\n UUU "
BLK_V = "V", "V   V\nV   V\nV   V\n V V \n  V  "
BLK_W = "W", "W W W\nW W W\nW W W\nWWWWW\n W W "
BLK_X = "X", "X   X\n X X \n  X  \n X X \nX   X"
BLK_Y = "Y", "Y   Y\n Y Y \n  Y  \n  Y  \n  Y  "
BLK_Z = "Z", "ZZZZZ\n   Z \n  Z  \n Z   \nZZZZZ"
BLK_ADDITION = "+", "     \n  +  \n +++ \n  +  \n     "
BLK_SUBTRACTION = "-", "     \n     \n --- \n     \n     "
BLK_MULTIPLICATION = "X", "     \n X X \n  X  \n X X \n     "
BLK_DIVISON = "/", "     \n   / \n  /  \n /   \n     "
BLK_PERCENTAGE = "%", "%   %\n   % \n  %  \n %   \n%   %"

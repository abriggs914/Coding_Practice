
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
			
			
## TODO
## When a dict value is a list, the content lines are too long.
## When a dict value is a list, opt to print the key only once per list (similarily to the numbering system)
## Add functionality for the numbering system to only count the keys, instead of sum of keys and all lengths of values that are lists
			
# Function returns a formatted string containing the contents of a dict object.
# Special lines and line count for values that are lists.
# Supports dictionaries with special value types.
# Lists are printed line by line, but the counting index is constant for all elements. - Useful for ties.
# Dicts are represented by a table which will dynamically generate a header and appropriately format cell values.
# Strings, floats, ints, bools are simply converted to their string representations.
# n					-	Name of the dict, printed above the contents.
# d					-	dict object.
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
def dict_print(d, n="Untitled", number=False, l=15, sep=5, marker=".", sort_header=False, min_encapsulation=True):
	if not d or not n:
		return "None"
	m = "\n--  " + str(n).title() + "  --\n\n"
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
		max_val = max((max([len(str(v_elem)) for v_elem in v] if v else [0]) if type(v) == (list or tuple) else len(str(v)) if type(v) != dict else 0), max_val)
			
	
	l = max(l, (max_key + max_val)) + sep
	has_dict = [(k, v) for k, v in d.items() if type(v) == dict]
	has_list = any([1 if type(v) in [list, tuple] else 0 for v in d.values()])
	
	
	
	header = []
	max_cell = 0
	max_cell_widths = []
	
	if has_list:
		number = True
	
	for k, v in has_dict:
		for k in v:
			key = str(k)
			if key not in header:
				header.append(key)
				max_cell = max(max_cell, max(len(key), max([len(str(value)) for value in v.values()])))
				
	max_cell += 2
	
	if sort_header:
		header.sort(key=lambda x: x.rjust(max_cell))
	
	if min_encapsulation:
		for h in header:
			max_col_width = len(" " + h + " ")
			for k, d_val in has_dict:
				if h in d_val:
					max_col_width = max(max_col_width, len(" " + str(d_val[h]) + " "))
			max_cell_widths.append(max_col_width) 
						
	table_header = TABLE_DIVIDER + TABLE_DIVIDER.join(map(lambda x: pad_centre(str(x), max_cell), header)) + TABLE_DIVIDER
	empty_line = TABLE_DIVIDER + TABLE_DIVIDER.join([pad_centre(" ", max_cell) for i in range(len(header))]) + TABLE_DIVIDER
	
	if min_encapsulation:
		table_header = TABLE_DIVIDER + TABLE_DIVIDER.join([pad_centre(str(h), max_cell_widths[i]) for i, h in enumerate(header)]) + TABLE_DIVIDER
		empty_line = TABLE_DIVIDER + TABLE_DIVIDER.join([pad_centre(" ", max_cell_widths[i]) for i in range(len(header))]) + TABLE_DIVIDER
	else:
		max_cell_widths = [max_cell for i in range(len(header))]
		
	fill = "".join([" " for i in range(len(str(fill + len(d))))])
	table_width = l + len(fill) + len(SEPARATOR) + len(TAB) + len(table_header) - (4 * len(TABLE_DIVIDER))
	table_tab = "".join([marker for i in range(len(TAB))])
	if has_dict:
		table_header_title = pad_centre("Table Header", l + len(SEPARATOR) - 1)
		m += TAB
		m += "" if not number else fill + SEPARATOR
		m += table_header_title + table_header.rjust(table_width - len(table_header_title) - len(fill) - len(SEPARATOR)) + "\n"
	i = 0
	# print("FINAL L: {l}\nFill: {n}<{f}>".format(l=l, n=len(fill), f=fill))
	for k, v in d.items():
		if type(v) not in [list, tuple]:
			v = [v]
		for j, v_elem in enumerate(v):
			ml = str(k).strip()
			orig_ml = ml
			num = str(i+1)
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
					ml += TABLE_DIVIDER + TABLE_DIVIDER.join(pad_centre(str(cell), max_cell_widths[i]) for i, cell in enumerate(vals)) + TABLE_DIVIDER
				else:
					ml += empty_line
			ml += "\n"
			m += TAB + ml
			i += 1
	return m
	
		
def money(v):
	# return "$ %.2f" % v
	return locale.currency(v, grouping=True)
	
	
def money_value(m):
	return float("".join(m[1:].split(",")))
	
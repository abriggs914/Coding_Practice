from operators import Operators
from Term import Term
from characters import Chars


# return the calculated width and height of a text => (w, h)
def text_wh(txt):
	splt = txt.split("\n")
	return max([len(letter) for letter in splt]), len(splt)


# Function returns a formatted string containing the contents of a dict object.
# Special lines and line count for values that are lists.
# n			-	Name of the dict, printed above the contents.
# d			-	dict object.
# number	-	Decide whether to number the content lines.
# l			-	Minimum number of chars in the content line.
# 				Spaces between keys and values are populated by marker.
# sep		-	Additional separation between keys and values.
# marker	-	Char that separates the key and value of a content line.
def dict_print(n, d, number=False, l=15, sep=5, marker="."):
	if not d or not n:
		return "None"
	m = "\n--  " + str(n).title() + "  --\n\n"
	fill = 0
	for k, v in d.items():
		lk = len(str(k))
		lv = len(str(v))
		# print("lk: {lk}, lv: {lv}".format(lk=lk, lv=lv))
		if type(k) == list:
			lk += (2 * len(k) + 2 + len(k) - 1)
		if type(v) == list:
			lv = max([len(str(v_elem)) for v_elem in v])
			# print("v: {v}".format(v=v))
			# for v_elem in v:
			# print("\tv_elem: {n}<{ve}>".format(n=len(v_elem), ve=v_elem))
			fill += len(v)
		l = max(l, (lk + lv))
	# print("calculated L : {l}\tLK: {lk}\tLV: {lv}".format(l=l, lk=lk, lv=lv))
	l += sep
	fill = "".join([" " for i in range(len(str(fill + len(d))))])
	i = 0
	# print("FINAL L: {l}\nFill: {n}<{f}>".format(l=l, n=len(fill), f=fill))
	for k, v in d.items():
		if type(v) != list:
			v = [v]
		for j, v_elem in enumerate(v):
			ml = str(k)
			orig_ml = ml
			num = str(i + 1)
			if number:
				ml = fill + "  -  " + ml
				if j == 0:
					ml = num.ljust(len(fill)) + ml[len(fill):]
			ml += str(v_elem).rjust(l - len(orig_ml), marker) + "\n"
			m += "\t" + ml
			i += 1
	return m


def indexOf(s, v, start=None, end=None, times=1):
	if not start:
		start = 0
	if not end:
		end = len(s)
		
	i = s.index(v, start, end)
	
	print("[\n\ts: {s}\n\tv: {v}\n\ti: {i}\n\tstart: {st}\n\tend: {e}\n\ttimes: {t}\n]".format(s=s, v=v, i=i, st=start, e=end, t=times))
	if times == 1:
		return i
	return indexOf(s, v, start=i+1, end=end, times=times-1)
	
# # return the index of the matching close parenthesis.
# def index_match_bracket(s):
	# l, r = 0, 0
	# for i, c in enumerate(s):
		# if c == "(":
			# l += 1
		# if c == ")":
			# r += 1
			# if l != 0 and r != 0 and l == r:
				# return i
	# return -1

# def collect_bracket_groups(f, lefts):
	# groups = {} # key is char index in f, val is the substring forming a closed set of brackets
	# # for i, c in enumerate(f):
	# for n, i in enumerate(lefts):
		# sub = f[i:]
		# print("  f[i:]: {f}".format(f=sub))
		# # cant use regular index function here because it defaults to first encounter, which typically is the most inner-nested set
		# j = -1 if ")" not in sub else (index_match_bracket(sub) + (len(f) - len(sub))) 
		# print("MATCHED:\n\tf[i:j]: <<{f}>>\n\ti: {i}\tj: {j}".format(f=sub[:j+1], i=i, j=j))
		# if j < 0:
			# return None
		# brackets = f[i: j+1]
		# groups[i] = brackets
	# return groups
				

# return the index of the matching close parenthesis.
# TODO calculate the depth of the nested brackets.
def index_match_bracket(s):
	l, r = 0, 0
	for i, c in enumerate(s):
		if c == "(":
			l += 1
		if c == ")":
			r += 1
			# print("l: " + str(l) + ", r: " + str(r))
			if l != 0 and r != 0 and l == r:
				return i
	return -1


def collect_bracket_groups(f, lefts, rights):
	groups = {} # key is char index in f, val is the substring forming a closed set of brackets
	# for i, c in enumerate(f):
	for n, i in enumerate(lefts):
		sub = f[i:]
		# print("  f[i:]: {f}".format(f=sub))
		# cant use regular index function here because it defaults to first encounter, which typically is the most inner-nested set
		m = index_match_bracket(sub)
		j = -1 if ")" not in sub else (m + (len(f) - len(sub)))
		d = sum([1 if v == "(" else -1 if v == ")" else 0 for v in f[:j+1]])
		# d = len(lefts) - (-1 if j < 0 else m[1]) 
		# print("MATCHED:\n\tf[i:j]: <<{f}>>\n\ti: {i}\tj: {j}".format(f=sub[:j+1], i=i, j=j))
		if j < 0:
			return None
		brackets = i, f[i: j+1]
		if d in groups:
			groups[d].append(brackets)
		else:
			groups[d] = [brackets]
			
	# for bracket in brackets:
		# idx = lefts.index(bracket)
		
	# for l in lefts:
		# for r in rights:
	return groups


def reduce_brackets(f, bracket_groups):
	redundant = []
	og = f
	for depth in range(len(bracket_groups)):
		d1 = depth + 1
		if d1 == len(bracket_groups):
			break

		for g0 in bracket_groups[depth]:
			for g1 in bracket_groups[d1]:
				g0_start, g0_end = g0[0], g0[0] + len(g0[1])
				g1_start, g1_end = g1[0], g1[0] + len(g1[1])
				print("\t({0}, {1}), ({2}, {3}), g0s==g1s-1 => {4}, g0e==g1e+1 => {5}, g1s-g1e => {6}".format(g0_start, g0_end, g1_start, g1_end, g0_start==g1_start-1, g0_end==g1_end+1, g1_end-g1_start))
				if (g1_end - g1_start) == 2 or ((g0_start == (g1_start - 1)) and (g0_end == (g1_end + 1))):
					redundant.append((g1_start - 1, g1_end))

		# if redundant:
	print("redundant: {r}".format(r=redundant))

	i = 0
	while i < len(redundant):
		left, right = redundant[i]
		updated = redundant[:i]
		f = f[:left] + f[left+1: right] + f[right+1:]
		for l1, r1 in redundant[i+1:]:
			if left < l1:
				l1 -= 1
			if left < r1:
				r1 -= 1
			if right < l1:
				l1 -= 1
			if right < r1:
				r1 -= 1
			updated.append((l1, r1))
		redundant = updated
		i += 1

	print("non redundant f: " + str(f) + "\noriginal f:      " + str(og))
	return f


def brackets_only(val, reverse=False):
	if reverse:
		rev = [l for l in val]
		rev.reverse()
		val = "".join(rev)

	past_equals = False
	res = ""
	for let in val:
		if let == "=":
			past_equals = True
			continue
		if not past_equals:
			if let == "(" or let == ")":
				res += let
		else:
			res += let

	if reverse:
		print("reverse res <{res}>".format(res=res))
		rev = [l for l in res]
		rev.reverse()
		res = "".join(rev)
		print("reverse res <{res}>".format(res=res))

	return res.strip()


def parse_eval(val):
	equals = val.index("=")
	og = val
	past_equals = False
	right = brackets_only(val)
	left = brackets_only(val, reverse=True)

	res = ""
	non_terms = ["(", ")", "+", "-", "*", "/", " "]
	i = 0
	lv = len(right)
	terms = []
	while i < lv:
		let = right[i]
		if let not in non_terms:
			j = i + 1 if i < lv - 1 else -1
			next_let = right[j] if j >= 0 else None
			t = let
			print("let: {let}, next_let: {nl}".format(let=let, nl=next_let))
			if next_let is not None and next_let not in non_terms:
				k = j
				while k < lv - 1:
					letter = right[k]
					if letter in non_terms:
						break
					t += letter
					k += 1
					i += 1
					print("Loop\nk: {k}\nlv: {lv}\nletter: {letter}".format(k=k, lv=lv, letter=letter))
			terms.append((i - len(t) + 1, Term(t, None)))
		i += 1


	print("ORIGINAL VAL:\n\t<{0}>\nRIGHT:\n\t<{1}>\nLEFT:\n\t<{2}>\nCALCULATED TERMS\n\t{3}".format(og, right, left, terms))
	e = left + str(eval(right))
	print("EVALUATED TO: <{0}>".format(e))
	return e


def display_func(f):
	f = "(" + f + ")"
	operators = ["(", ")", "="] + [op.n for op in Operators]
	bracket_idxs = [i for i, c in enumerate(f) if c == "(" or c == ")"]
	lefts, rights = [], []
	print("f:               {f}\nbracket indexes: {b}\nlefts:           {l}\nright:           {r}".format(f=f, b=bracket_idxs, l=lefts, r=rights))
	for i in bracket_idxs:
		if f[i] == "(":
			lefts.append(i)
		if f[i] == ")":
			rights.append(i)
	if len(bracket_idxs) % 2 == 1 or len(lefts) != len(rights):
		pass
		# unmatched brackets
		# raise ValueError("unmatched brackets: <<{0}>>".format(f))
	print("f:               {f}\nbracket indexes: {b}\nlefts:           {l}\nright:           {r}".format(f=f, b=bracket_idxs, l=lefts, r=rights))
	bracket_groups = collect_bracket_groups(f, lefts, rights)
	print(dict_print("bracket groups", bracket_groups))
	if not bracket_groups and (lefts or rights):
		raise ValueError("mismatched brackets <<{0}>>".format(f))

	f = reduce_brackets(f, bracket_groups)
	e = parse_eval(f)

	# At this stage the equation should be divided into it's nested bracket groups


	# Need to split each group to determine if any multi-vertical line terms need to be added.
	# i.e. if there is a division, then the height of the result function will be increased to include
	# the height of stacked terms. (Character height varies due to jumbo feature)
	# Operations which add new height lines are: DIVISION / LOG / POWER / FRACTIONS
	
	res = None
	return res

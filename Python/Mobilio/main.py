import datetime as dt


entries = [
	('2021-05-07 08:30:00', 0.357786),
	("2021-05-21 08:30:00", 0.351614),
	("2021-05-26 08:30:00", 0.348944),
	("2021-05-26 08:31:00", 0.348939),
	("2021-05-27 08:30:00", 0.348185),
	("2021-05-31 08:30:00", 0.344921),
	("2021-06-01 08:30:00", 0.344017),
	("2021-06-02 08:30:00", 0.343418),
	("2021-06-03 08:30:00", 0.343039),
	("2021-06-04 08:30:00", 0.342799),
	("2021-06-07 08:30:00", 0.341943),
	("2021-06-08 08:30:00", 0.341695),
	("2021-06-09 08:30:00", 0.341486),
	("2021-06-10 08:30:00", 0.341286),
	("2021-06-11 08:30:00", 0.341135),
	("2021-06-14 08:30:00", 0.340505),
	("2021-06-15 08:30:00", 0.340314),
	("2021-06-16 08:30:00", 0.340152),
	("2021-06-17 08:30:00", 0.340008),
	("2021-06-18 08:30:00", 0.339882),
	("2021-06-21 08:30:00", 0.339336),
	("2021-06-22 08:30:00", 0.339133),
	("2021-06-23 08:30:00", 0.338951),
	("2021-06-24 08:30:00", 0.338815),
	("2021-06-25 08:30:00", 0.338118),
	("2021-06-30 08:30:00", 0.337746),
	("2021-07-05 08:30:00", 0.336870),
	("2021-07-06 08:30:00", 0.336684),
	("2021-07-09 08:30:00", 0.336191),
	("2021-07-12 08:30:00", 0.335692),
	("2021-07-14 08:30:00", 0.335290)
]

es = lambda vs: (dt.datetime.strptime(vs[0], "%Y-%m-%d %H:%M:%S"), vs[1])
lst = list(map(es, entries))
print("entries:", entries)
print("lst:", lst)

td = 0
mid = dt.datetime.today()
mad = dt.datetime(1, 1, 1)
wd = -float("inf"), dt.datetime.today()
bd = float("inf"), dt.datetime.today()
for i, entry in enumerate(entries):
	d = entries[0][1]
	date, value = es(entry)
	if 0 < i < len(entries):
		d = entries[i - 1][1]
	d = value - d
	td += d
	if date < mid:
		mid = date
	if mad < date:
		mad = date
	if wd[0] < value:
		wd = value, date
	if value < bd[0]:
		bd = value, date
	print("\nEntry: {}\t\texchange: {}\nDiff from last entry: {}".format(i, value, d))

if td == 0:
	td = float("inf")

print("\nTotal diff: {}".format(td))
print("first day:  {}\nlast day:   {}".format(mid, mad))
print("best day:   {}\nworst day:  {}".format(bd, wd))
if entries:
	gain = (1 / entries[-1][1]) - (1 / entries[0][1])
	# gain *= 1 if gain >= 1 else -1
	# gain = 1 / gain
else:
	gain = 1 / abs(td)
dd = mad - mid
print("By waiting {} days, I have the potential to gain {} Mobilio per point.".format(dd.days, gain))
balance = float(input("enter a point balance:\n"))
old = balance / entries[0][1]
new = balance / entries[-1][1]
dif = new - old
print("With a balance of {} points\nI could have made: {} Mobilio on {}\nNow I will make: {} Mobilio on {}\nDifference of {} Mobilio".format(balance, old, mid, new, mad, dif))
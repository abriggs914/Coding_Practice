import datetime as dt


entries = [
	('2021-05-07 00:30:00', 0.357786),
	("2021-05-21 00:30:00", 0.351614),
	("2021-05-26 00:30:00", 0.348944),
	("2021-05-26 00:31:00", 0.348939),
	("2021-05-27 00:30:00", 0.348185),
	("2021-05-31 00:30:00", 0.344921),
	("2021-06-01 00:30:00", 0.344017),
	("2021-06-02 00:30:00", 0.343418),
	("2021-06-03 00:30:00", 0.343039),
	("2021-06-04 00:30:00", 0.342799),
	("2021-06-07 00:30:00", 0.341943),
	("2021-06-08 00:30:00", 0.341695),
	("2021-06-09 00:30:00", 0.341486),
	("2021-06-10 00:30:00", 0.341286),
	("2021-06-11 00:30:00", 0.341135),
	("2021-06-14 00:30:00", 0.340505),
	("2021-06-15 00:30:00", 0.340314),
	("2021-06-16 00:30:00", 0.340152),
	("2021-06-17 00:30:00", 0.340008),
	("2021-06-18 00:30:00", 0.339882),
	("2021-06-21 00:30:00", 0.339336)
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
print("With a balance of {} points\nI could have made: {} Mobilio\nNow I will make: {} Mobilio\nDifference of {} Mobilio".format(balance, old, new, dif))
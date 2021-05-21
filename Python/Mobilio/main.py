
entries = [('2021-05-07 00:30:00', 0.357786), "2021-05-21 00:30:00", 0.351614]
es = lambda vs: (dt.datetime.strptime(vs[0], "%Y-%m-%d %H:%M:%S"), vs[1])
list(map(es, er))
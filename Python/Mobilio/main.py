
entries = [('2021-05-07 00:30:00', 0.357786)]
es = lambda vs: (dt.datetime.strptime(vs[0], "%Y-%m-%d %H:%M:%S"), vs[1])
list(map(es, er))


teams = [
    ("A", 0, 0),
    ("B", 0, 0),
    ("C", 0, 0),
    ("D", 0, 1),
    ("E", 0, 1),
    ("F", 0, 1),
    ("G", 1, 2),
    ("H", 1, 2),
    ("I", 1, 2),
    ("J", 1, 3),
    ("K", 1, 3),
    ("L", 1, 3)
]

t_list = [t[0] for t in teams]

div0 = [t for t in teams if t[2] == 0]
div1 = [t for t in teams if t[2] == 1]
div2 = [t for t in teams if t[2] == 2]
div3 = [t for t in teams if t[2] == 3]
conf0 = [t for t in teams if t[1] == 0]
conf1 = [t for t in teams if t[1] == 1]

print(f"{div0=}\n{div1=}\n{div2=}\n{div3=}\n{conf0=}\n{conf1=}")

games = []

if __name__ == '__main__':

    # 1 Home and Away game between each team
    # conf
    for t0 in conf0:
        for t1 in conf1:
            games.append((t0[0], t1[0]))
    # conf
    for t0 in conf1:
        for t1 in conf0:
            games.append((t0[0], t1[0]))
    # other div same conf
    for t0 in div0:
        for t1 in div1:
            games.append((t0[0], t1[0]))
    # other div same conf
    for t0 in div1:
        for t1 in div0:
            games.append((t0[0], t1[0]))
    # other div same conf
    for t0 in div2:
        for t1 in div3:
            games.append((t0[0], t1[0]))
    # other div same conf
    for t0 in div3:
        for t1 in div2:
            games.append((t0[0], t1[0]))


    # same div other team
    for t0 in div0:
        for t1 in div0:
            if t0 != t1:
                games.append((t0[0], t1[0]))
    # same div other team
    for t0 in div1:
        for t1 in div1:
            if t0 != t1:
                games.append((t0[0], t1[0]))
    # same div other team
    for t0 in div2:
        for t1 in div2:
            if t0 != t1:
                games.append((t0[0], t1[0]))
    # same div other team
    for t0 in div3:
        for t1 in div3:
            if t0 != t1:
                games.append((t0[0], t1[0]))

    # 1 Home and Away game between each team same conf
    for i, t0 in enumerate(conf0):
        for t1 in conf0[i:]:
            print(f"0\t{t0=}, {t1=}")
            if t0[2] != t1[2]:
                games.append((t0[0], t1[0]))
                # games.append((-1, -2))
    for i, t0 in enumerate(conf1):
        for t1 in conf1[i:]:
            print(f"1\t{t0=}, {t1=}")
            if t0[2] != t1[2]:
                games.append((t0[0], t1[0]))
                # games.append((-1, -2))

    # Bottom 4
    # same div other team
    for t0 in div0:
        for t1 in div0:
            if t0 != t1:
                games.append((t0[0], t1[0]))
    # same div other team
    for t0 in div1:
        for t1 in div1:
            if t0 != t1:
                games.append((t0[0], t1[0]))
    # same div other team
    for t0 in div2:
        for t1 in div2:
            if t0 != t1:
                games.append((t0[0], t1[0]))
    # same div other team
    for t0 in div3:
        for t1 in div3:
            if t0 != t1:
                games.append((t0[0], t1[0]))

    for g in games:
        print(f"{g=}")
    print(f"{len(games)=}")

    a_games = 0
    for t_ in t_list:
        opponents = []
        for t0, t1 in games:
            if t0 == t_ or t1 == t_:
                a_games += 1
                opponents.append(t1 if t0 == t_ else t0)
                # print(f"{t0=}, {t1=}")

        opponents.sort()
        print(f"{t_=}, len={len(opponents)}, {opponents=}")

        # print(f"{a_games=}")

    standings = {}
    s_template = {"w": 0, "l": 0, "otl": 0}

    # a wins all, then b, then c ...
    # for i, t in enumerate(t_list):
    #     idx = t_list.index(t)
    for i, game in enumerate(games):
        t0, t1 = game
        i0, i1 = t_list.index(t0), t_list.index(t1)
        if t0 not in standings:
            standings.update({t0: {k: v for k, v in s_template.items()}})
        if t1 not in standings:
            standings.update({t1: {k: v for k, v in s_template.items()}})

        print(f"{t0=} VS. {t1=} ", end="")
        if i0 < i1:
            print(f"A")
            standings[t0]["w"] += 1
            standings[t1]["l"] += 1
        else:
            print(f"B")
            standings[t0]["l"] += 1
            standings[t1]["w"] += 1

    for k, v in standings.items():
        print(f"{k=}, {v=}")
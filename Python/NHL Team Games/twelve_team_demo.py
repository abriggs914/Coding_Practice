import random

NHL_MODE = False

n_seeds_per_div = 2
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

# teams = [
#     ("A", 0, 0),
#     ("B", 0, 0),
#     ("C", 0, 0),
#     ("D", 0, 0),
#     ("E", 0, 1),
#     ("F", 0, 1),
#     ("G", 0, 1),
#     ("H", 0, 1),
#     ("I", 1, 2),
#     ("J", 1, 2),
#     ("K", 1, 2),
#     ("L", 1, 2),
#     ("M", 1, 3),
#     ("N", 1, 3),
#     ("O", 1, 3),
#     ("P", 1, 3)
# ]


if NHL_MODE:
    n_seeds_per_div = 3
    teams = [
        ("00", 0, 0),
        ("01", 0, 0),
        ("02", 0, 0),
        ("03", 0, 0),
        ("04", 0, 0),
        ("05", 0, 0),
        ("06", 0, 0),
        ("07", 0, 0),

        ("08", 0, 1),
        ("09", 0, 1),
        ("10", 0, 1),
        ("11", 0, 1),
        ("12", 0, 1),
        ("13", 0, 1),
        ("14", 0, 1),
        ("15", 0, 1),

        ("16", 1, 2),
        ("17", 1, 2),
        ("18", 1, 2),
        ("19", 1, 2),
        ("20", 1, 2),
        ("21", 1, 2),
        ("22", 1, 2),
        ("23", 1, 2),

        ("24", 1, 3),
        ("25", 1, 3),
        ("26", 1, 3),
        ("27", 1, 3),
        ("28", 1, 3),
        ("29", 1, 3),
        ("30", 1, 3),
        ("31", 1, 3)
    ]

t_list = [t[0] for t in teams]

div0 = [t for t in teams if t[2] == 0]
div1 = [t for t in teams if t[2] == 1]
div2 = [t for t in teams if t[2] == 2]
div3 = [t for t in teams if t[2] == 3]
conf0 = [t for t in teams if t[1] == 0]
conf1 = [t for t in teams if t[1] == 1]

div0_teams = [t[0] for t in div0]
div1_teams = [t[0] for t in div1]
div2_teams = [t[0] for t in div2]
div3_teams = [t[0] for t in div3]
conf0_teams = [t[0] for t in conf0]
conf1_teams = [t[0] for t in conf1]

teams_to_confs = {
    t: conf0_teams if t in conf0_teams else conf1_teams
    for t in t_list
}

teams_to_divs = {
    t: div0_teams if t in div0_teams else (div1_teams if t in div1_teams else (div2_teams if t in div2_teams else div3_teams))
    for t in t_list
}

print(f"{div0=}\n{div1=}\n{div2=}\n{div3=}\n{conf0=}\n{conf1=}\n{teams_to_confs=}\n{teams_to_divs=}")

games = []


def get_pts(scores_games_left: dict | int) -> int:
    if isinstance(scores_games_left, int):
        games_left_ = scores_games_left
        return 2 * games_left_
        # return 3 * games_left_
    else:
        scores = scores_games_left
        return((scores.get("w", 0) + scores.get("otw", 0) + scores.get("sow", 0)) * 2) + (scores.get("otl", 0) + scores.get("sol", 0))
        # return((scores.get("w", 0) * 3) + (scores.get("otw", 0) + scores.get("sow", 0)) * 2) + (scores.get("otl", 0) + scores.get("sol", 0))


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
    n_inner_div_games = 0
    for t0 in div0:
        for t1 in div0:
            if t0 != t1:
                n_inner_div_games += 1
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

    if NHL_MODE:
        n_games_rem = 4
        to_rem_div0 = random.sample(games[-4*n_inner_div_games:-3*n_inner_div_games], n_games_rem)
        to_rem_div1 = random.sample(games[-3*n_inner_div_games:-2*n_inner_div_games], n_games_rem)
        to_rem_div2 = random.sample(games[-2*n_inner_div_games:-n_inner_div_games], n_games_rem)
        to_rem_div3 = random.sample(games[-n_inner_div_games:], n_games_rem)

        for to_rem in [to_rem_div0, to_rem_div1, to_rem_div2, to_rem_div3]:
            for g_ in to_rem:
                games.remove(g_)

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
    s_template = {"w": 0, "l": 0, "otw": 0, "otl": 0, "sow": 0, "sol": 0}
    TTL_GAMES_PER_TEAM = int(len(games) / (len(t_list) / 2))
    INC_OT = True
    INC_SO = False
    OT_CHANCE = 0.25
    SO_CHANCE = 0.08
    games_left = games.copy()
    if not INC_OT:
        del s_template["otl"]
        del s_template["otw"]
    if not INC_SO:
        del s_template["sol"]
        del s_template["sow"]

    for i, t in enumerate(t_list):
        if t not in standings:
            standings.update({t: {k: v for k, v in s_template.items()}})

    # a wins all, then b, then c ...
    # for i, t in enumerate(t_list):
    #     idx = t_list.index(t)
    print(f"{t_list=}")
    print(f"{TTL_GAMES_PER_TEAM=}")
    eliminated_teams = {}
    for i, game in enumerate(games):
        t0, t1 = game
        i0, i1 = t_list.index(t0), t_list.index(t1)
        # conf_t0 = conf0_teams if t0 in conf0_teams else conf1_teams
        # conf_t1 = conf0_teams if t1 in conf0_teams else conf1_teams
        # if conf_t0 == conf0_teams:
        #     div_t0 = div0_teams if t0 in div0_teams else div1_teams
        # else:
        #     div_t0 = div2_teams if t0 in div2_teams else div3_teams
        # if conf_t1 == conf0_teams:
        #     div_t1 = div0_teams if t1 in div0_teams else div1_teams
        # else:
        #     div_t1 = div2_teams if t1 in div2_teams else div3_teams

        in_ot = INC_OT and (random.random() <= OT_CHANCE)
        in_so = INC_OT and INC_SO and (random.random() <= SO_CHANCE)
        lk, wk = "l", "w"
        lk = ("so" if in_so else ("ot" if in_ot else "")) + lk
        wk = ("so" if in_so else ("ot" if in_ot else "")) + wk

        print(f"{t0=} VS. {t1=}, OT={'T' if in_ot else 'F'}, SO={'T' if in_so else 'F'} ", end="")
        if i0 < i1:
            print(f">A")
            standings[t0][wk] += 1
            standings[t1][lk] += 1
        else:
            print(f">B")
            standings[t0][lk] += 1
            standings[t1][wk] += 1

        games_left.remove(game)

        elim_data = {}

        for t_ in t_list:
            games_left_t_ = []
            for g in games_left:
                if t_ in g:
                    games_left_t_.append(g)

            conf_t_ = teams_to_confs[t_]
            div_t_ = teams_to_divs[t_]

            games_left_t_conf = [g for g in games_left_t_ if t_ in conf_t_]
            games_left_t_div = [g for g in games_left_t_conf if t_ in div_t_]

            s_ = standings[t_]
            gp_t = int(sum(s_.values()))
            gl_t = TTL_GAMES_PER_TEAM - gp_t
            gl_c = len(games_left_t_conf)
            gl_d = len(games_left_t_div)
            pts_ = get_pts(s_)
            pts_avail_t = get_pts(gl_t)
            pts_avail_c = get_pts(gl_c)
            pts_avail_d = get_pts(gl_d)

            elim_data[t_] = {
                "gp_t": gp_t,
                "gl_t": gl_t,
                "gl_c": gl_c,
                "gl_d": gl_d,
                "pts": pts_,
                "pts_p_t": pts_ + pts_avail_t,
                "pts_p_c": pts_ + pts_avail_c,
                "pts_p_d": pts_ + pts_avail_d,
                "pts_a_t": pts_avail_t,
                "pts_a_c": pts_avail_c,
                "pts_a_d": pts_avail_d
            }

            # print(f"{ta=}, C0={conf_ta}, D0={div_ta}, pts={pts_a}, glC={len(games_left_ta_conf)}, glD={len(games_left_ta_div)}, ", end="")
            # print(f"{tb=}, C0={conf_tb}, D0={div_tb}, pts={pts_b}, glC={len(games_left_tb_conf)}, glD={len(games_left_tb_div)}")

            print(f"{t_=}, pts={pts_}, glC={gl_c}, glD={gl_d}")

        # check

        max_pts_conf0 = [(t_, v["pts_p_t"]) for t_, v in elim_data.items() if t_ in conf0_teams]
        max_pts_conf1 = [(t_, v["pts_p_t"]) for t_, v in elim_data.items() if t_ in conf1_teams]
        max_pts_div0 = [(t_, v["pts_p_t"]) for t_, v in elim_data.items() if t_ in div0_teams]
        max_pts_div1 = [(t_, v["pts_p_t"]) for t_, v in elim_data.items() if t_ in div1_teams]
        max_pts_div2 = [(t_, v["pts_p_t"]) for t_, v in elim_data.items() if t_ in div2_teams]
        max_pts_div3 = [(t_, v["pts_p_t"]) for t_, v in elim_data.items() if t_ in div3_teams]

        max_pts_conf0.sort(key=lambda tup: tup[1], reverse=True)
        max_pts_conf1.sort(key=lambda tup: tup[1], reverse=True)
        max_pts_div0.sort(key=lambda tup: tup[1], reverse=True)
        max_pts_div1.sort(key=lambda tup: tup[1], reverse=True)
        max_pts_div2.sort(key=lambda tup: tup[1], reverse=True)
        max_pts_div3.sort(key=lambda tup: tup[1], reverse=True)

        div0_possible_cutoff = max_pts_div0[n_seeds_per_div - 1]
        div1_possible_cutoff = max_pts_div1[n_seeds_per_div - 1]
        div2_possible_cutoff = max_pts_div2[n_seeds_per_div - 1]
        div3_possible_cutoff = max_pts_div3[n_seeds_per_div - 1]

        po_t3_div0 = max_pts_div0[:n_seeds_per_div]
        po_t3_div1 = max_pts_div1[:n_seeds_per_div]
        po_t3_div2 = max_pts_div2[:n_seeds_per_div]
        po_t3_div3 = max_pts_div3[:n_seeds_per_div]
        max_pts_conf0_copy = max_pts_conf0.copy()
        max_pts_conf1_copy = max_pts_conf1.copy()
        for t_pts_ in [*po_t3_div0, *po_t3_div1]:
            max_pts_conf0_copy.remove(t_pts_)
        for t_pts_ in [*po_t3_div2, *po_t3_div3]:
            max_pts_conf1_copy.remove(t_pts_)
        conf0_possible_cutoff = max_pts_conf0_copy[1]
        conf1_possible_cutoff = max_pts_conf1_copy[1]
        # conf0_possible_cutoff = max_pts_conf0[2]
        # conf1_possible_cutoff = max_pts_conf1[2]

        print(f" div0_cutoff={div0_possible_cutoff}")
        print(f"conf0_cutoff={conf0_possible_cutoff}")
        print(f"{elim_data[t_list[0]]=}")
        print(f"{elim_data[t_list[1]]=}")
        print(f"{elim_data[t_list[2]]=}")
        print(f"{elim_data[t_list[3]]=}")
        print(f"{elim_data[t_list[4]]=}")
        print(f"{elim_data[t_list[5]]=}")
        for t_ in div0_teams:
            t_pts_d = elim_data[t_]["pts_p_d"]
            t_pts_c = elim_data[t_]["pts_p_c"]
            c_pts_d = div0_possible_cutoff[1]
            c_pts_c = conf0_possible_cutoff[1]
            print(f"d0: {t_=}, {t_pts_d=}, {t_pts_c=}, {c_pts_d=}, {c_pts_c=}")
            if t_pts_d < c_pts_d:
                # eliminated from division seed.
                if t_ not in eliminated_teams:
                    eliminated_teams[t_] = {"d": (standings[t_].get("gp", 0),)}
                    # if "d" not in eliminated_teams[t_]:
                    print(f"{t_} has been eliminated from division seed.")
                else:
                    if "d" not in eliminated_teams[t_]:
                        print(f"{t_} has been eliminated from division seed.")
                        eliminated_teams[t_] = {"d": (standings[t_].get("gp", 0),)}
            if t_pts_c < c_pts_c:
                # eliminated from conference wildcard
                if t_ not in eliminated_teams:
                    eliminated_teams[t_] = {"wc": (standings[t_].get("gp", 0),)}
                    # if "wc" not in eliminated_teams[t_]:
                    #     eliminated_teams[t_]["wc"] = (standings[t_]["gp"],)
                    print(f"{t_} has been eliminated from playoff contention.")
                else:
                    if "wc" not in eliminated_teams[t_]:
                        eliminated_teams[t_] = {"wc": (standings[t_].get("gp", 0),)}
                        print(f"{t_} has been eliminated from playoff contention.")
        # for t_ in div1_teams:
        #     if elim_data[t_]["pts_p_d"] < div1_possible_cutoff[1]:
        #         # eliminated from division seed.
        #         if t_ not in eliminated_teams:
        #             print(f"{t_} has been eliminated from division seed.")
        #     if elim_data[t_]["pts_p_c"] < conf0_possible_cutoff[1]:
        #         # eliminated from conference wildcard
        #         if t_ not in eliminated_teams:
        #             eliminated_teams[t_] = (standings[t_]["gp"],)
        #             print(f"{t_} has been eliminated from playoff contention.")
        #
        # for t_ in div2_teams:
        #     if elim_data[t_]["pts_p_d"] < div2_possible_cutoff[1]:
        #         # eliminated from division seed.
        #         if t_ not in eliminated_teams:
        #             print(f"{t_} has been eliminated from division seed.")
        #     if elim_data[t_]["pts_p_c"] < conf1_possible_cutoff[1]:
        #         # eliminated from conference wildcard
        #         if t_ not in eliminated_teams:
        #             eliminated_teams[t_] = (standings[t_]["gp"],)
        #             print(f"{t_} has been eliminated from playoff contention.")
        #
        # for t_ in div3_teams:
        #     if elim_data[t_]["pts_p_d"] < div3_possible_cutoff[1]:
        #         # eliminated from division seed.
        #         if t_ not in eliminated_teams:
        #             print(f"{t_} has been eliminated from division seed.")
        #     if elim_data[t_]["pts_p_c"] < conf1_possible_cutoff[1]:
        #         # eliminated from conference wildcard
        #         if t_ not in eliminated_teams:
        #             eliminated_teams[t_] = (standings[t_]["gp"],)
        #             print(f"{t_} has been eliminated from playoff contention.")

        print(f"{eliminated_teams=}")

        # for ta, tb in games_left:
        #     games_left_ta = []
        #     games_left_tb = []
        #     for g in games_left:
        #         if t0 in g:
        #             games_left_ta.append(g)
        #         if t1 in g:
        #             games_left_tb.append(g)
        #
        #     conf_ta = teams_to_confs[ta]
        #     conf_tb = teams_to_confs[tb]
        #     div_ta = teams_to_divs[ta]
        #     div_tb = teams_to_divs[tb]
        #
        #     games_left_ta_conf = [g for g in games_left_ta if ta in conf_ta or tb in conf_ta]
        #     games_left_tb_conf = [g for g in games_left_tb if ta in conf_tb or tb in conf_tb]
        #     games_left_ta_div = [g for g in games_left_ta_conf if ta in div_ta or tb in div_ta]
        #     games_left_tb_div = [g for g in games_left_tb_conf if ta in div_tb or tb in div_tb]
        #
        #     sa = standings[ta]
        #     sb = standings[tb]
        #     gp_a_t = sum(sa.values())
        #     gp_b_t = sum(sb.values())
        #     gl_a = TTL_GAMES_PER_TEAM - gp_a_t
        #     gl_b = TTL_GAMES_PER_TEAM - gp_b_t
        #     pts_a = get_pts(sa)
        #     pts_b = get_pts(sb)
        #
        #     # print(f"{ta=}, C0={conf_ta}, D0={div_ta}, pts={pts_a}, glC={len(games_left_ta_conf)}, glD={len(games_left_ta_div)}, ", end="")
        #     # print(f"{tb=}, C0={conf_tb}, D0={div_tb}, pts={pts_b}, glC={len(games_left_tb_conf)}, glD={len(games_left_tb_div)}")
        #
        #     print(f"{ta=}, pts={pts_a}, glC={len(games_left_ta_conf)}, glD={len(games_left_ta_div)}, ", end="")
        #     print(f"{tb=}, pts={pts_b}, glC={len(games_left_tb_conf)}, glD={len(games_left_tb_div)}")

    print(f"{t_list=}\n{TTL_GAMES_PER_TEAM=}")
    print(f"{len(games) / (len(t_list) / 2)=}")
    for k in t_list:
        v = standings[k]
        pts = get_pts(standings[k])
        print(f"{k=}, {pts=}, {v=}")

import random

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

div0_teams = [t[0] for t in div0]
div1_teams = [t[0] for t in div1]
div2_teams = [t[0] for t in div2]
div3_teams = [t[0] for t in div3]
conf0_teams = [t[0] for t in conf0]
conf1_teams = [t[0] for t in conf1]

teams_to_confs = {
    t: conf0 if t in conf0_teams else conf1_teams
    for t in t_list
}

teams_to_divs = {
    t: div0 if t in div0_teams else (div1 if t in div1_teams else (div2 if t in div2_teams else div3))
    for t in t_list
}

print(f"{div0=}\n{div1=}\n{div2=}\n{div3=}\n{conf0=}\n{conf1=}")

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
    s_template = {"w": 0, "l": 0, "otw": 0, "otl": 0, "sow": 0, "sol": 0}
    TTL_GAMES_PER_TEAM = len(games) / (len(t_list) / 2)
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

    # a wins all, then b, then c ...
    # for i, t in enumerate(t_list):
    #     idx = t_list.index(t)
    print(f"{t_list=}")
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
        if t0 not in standings:
            standings.update({t0: {k: v for k, v in s_template.items()}})
        if t1 not in standings:
            standings.update({t1: {k: v for k, v in s_template.items()}})

        in_ot = INC_OT and (random.random() <= OT_CHANCE)
        in_so = INC_OT and INC_SO and (random.random() <= SO_CHANCE)
        lk, wk = "l", "w"
        lk = ("so" if in_so else ("ot" if in_ot else "")) + lk
        wk = ("so" if in_so else ("ot" if in_ot else "")) + wk

        print(f"{t0=} VS. {t1=}, OT={'T' if in_ot else 'F'}, SO={'T' if in_so else 'F'} ", end="")
        if i0 < i1:
            print(f">A ", end="")
            standings[t0][wk] += 1
            standings[t1][lk] += 1
        else:
            print(f">B ", end="")
            standings[t0][lk] += 1
            standings[t1][wk] += 1

        games_left.remove(game)

        for ta, tb in games_left:
            games_left_ta = []
            games_left_tb = []
            for g in games_left:
                if t0 in g:
                    games_left_ta.append(g)
                if t1 in g:
                    games_left_tb.append(g)

            conf_ta = teams_to_confs[ta][0]
            conf_tb = teams_to_confs[tb][0]
            div_ta = teams_to_divs[ta][0]
            div_tb = teams_to_divs[tb][0]

            games_left_ta_conf = [g for g in games_left_ta if ta in conf_ta or tb in conf_ta]
            games_left_tb_conf = [g for g in games_left_tb if ta in conf_tb or tb in conf_tb]
            games_left_ta_div = [g for g in games_left_ta_conf if ta in div_ta or tb in div_ta]
            games_left_tb_div = [g for g in games_left_tb_conf if ta in div_tb or tb in div_tb]

        s0 = standings[t0]
        s1 = standings[t1]
        gp_0_t = sum(s0.values())
        gp_1_t = sum(s1.values())
        gl_0 = TTL_GAMES_PER_TEAM - gp_0_t
        gl_1 = TTL_GAMES_PER_TEAM - gp_1_t
        pts_0 = get_pts(s0)
        pts_1 = get_pts(s1)

        print(f"{t0=}, C0={conf_t0}, D0={div_t0}, pts={pts_0}, glC={len(games_left_t0_conf)}, glD={len(games_left_t0_div)}, ", end="")
        print(f"{t1=}, C0={conf_t1}, D0={div_t1}, pts={pts_1}, glC={len(games_left_t1_conf)}, glD={len(games_left_t1_div)}")

    for k in t_list:
        v = standings[k]
        pts = get_pts(standings[k])
        print(f"{k=}, {pts=}, {v=}")

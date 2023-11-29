import itertools
import random

import pandas as pd


og_league = [
    [
        ["00", "01", "02", "03", "04", "05", "06", "07"],
        ["08", "09", "10", "11", "12", "13", "14", "15"]
    ],
    [
        ["16", "17", "18", "19", "20", "21", "22", "23"],
        ["24", "25", "26", "27", "28", "29", "30", "31"]
    ]
]


if __name__ == '__main__':

    league_games = list(itertools.combinations(range(32), 2))
    league_games += list(itertools.combinations(range(32), 2))
    league_games += list(itertools.combinations(range(16), 2))
    league_games += list(itertools.combinations(range(16, 32), 2))

    print(f"{len(league_games)=}")
    rem_div_teams = {i: 5 for i in range(32)}
    div_games = {i: {i} for i in range(32)}
    for i in range(4):
        div_teams = [t for t in rem_div_teams if ((i * 8) <= t < ((i + 1) * 8))]
        print(f"{div_teams=}")
        # for t1 in div_teams:
        div_count = 0
        for j in range(20):
            t1 = random.choice(div_teams)
            t2 = random.choice(div_teams)
            while t2 in div_games[t1]:
                t2 = random.choice(div_teams)
            print(f"{i=}, #{div_count+1}, {t1=}, {t2=}")
            league_games.append((t1, t2))
            div_games[t1].add(t2)
            div_games[t2].add(t1)
            div_count += 1
            rem_div_teams[t1] -= 1
            rem_div_teams[t2] -= 1
            if rem_div_teams[t1] == 0:
                print(f"\t{t1=}")
                del rem_div_teams[t1]
                div_teams.remove(t1)
            if rem_div_teams[t2] == 0:
                print(f"\t{t2=}")
                del rem_div_teams[t2]
                div_teams.remove(t2)
            print(f"{div_teams=}")
            for tm in div_games:
                print(f"div_games[{tm}]={div_games[tm]}")

    print(f"{len(league_games)=}")

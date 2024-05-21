import json

import pandas as pd
import os

from utility import percent

excel_picks = r"C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Python\Hockey pool\2024\Pool Picks.xlsx"
player_data_by_box_json = r"C:\Users\Abriggs\Documents\Coding Practice\Coding_Practice\Python\Hockey pool\2024\player_data_pool_2024.json"
if not os.path.exists(excel_picks):
    excel_picks = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\2024\Pool Picks.xlsx"
if not os.path.exists(player_data_by_box_json):
    player_data_by_box_json = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\2024\player_data_pool_2024.json"


out_round_1 = [
    "TB",
    "NYI",
    "WAS",
    "TOR",
    "LA",
    "WPG",
    "VGK",
    "NSH"
]

out_round_2 = [
    "BOS",
    "CAR",
    "VAN",
    "COL"
]

out_round_3 = [
    "NYR",
    "EDM"
]


if __name__ == '__main__':

    with open(player_data_by_box_json, "r") as f:
        player_data_by_box = json.load(f)

    df_picks = pd.read_excel(excel_picks)
    # print(f"{df_picks=}")

    player_2_team = {}
    player_ppg = {}
    team_2_player = {}
    team_name_2_acr = {}
    for box_num, box_data in player_data_by_box.items():
        for player_data, ppg in box_data.items():
            spl = player_data.split("(")
            name = spl[0].strip()
            team = spl[1]
            team = team[:team.index(")")]
            player_2_team[name] = team
            player_ppg[name] = float(ppg)
            if team not in team_2_player:
                team_2_player[team] = []
            team_2_player[team].append(name)
            if box_num in ["10", "11", "22", "23"]:
                team_name_2_acr[name] = team

    list_pool_people = sorted(list(df_picks.columns))
    print(f"Number pool people: {len(list_pool_people)}")
    percentage_alike_r1 = {}
    percentage_alike_r2 = {}
    percentage_alike_r3 = {}
    percentage_alike_r4 = {}
    player_data = {}
    team_data = {}
    box_choices = {}

    print(f"{player_2_team=}")

    for person_a in list_pool_people:
        df_picks_a = df_picks[person_a]
        percentage_alike_r1[person_a] = {}
        percentage_alike_r2[person_a] = {}
        percentage_alike_r3[person_a] = {}
        percentage_alike_r4[person_a] = {}

        print(f"{person_a=}")
        for person_b in list_pool_people:
            if person_a != person_b:
                print(f"{person_b=}")
                df_picks_b = df_picks[person_b]
                cnt_alike = 0
                n_picks = df_picks_a.shape[0]
                n_picks_r2 = 0
                cnt_alike_r2 = 0
                n_picks_r3 = 0
                cnt_alike_r3 = 0
                n_picks_r4 = 0
                cnt_alike_r4 = 0
                for i in range(n_picks):
                    pick_a = df_picks_a.iloc[i].replace("è", "e").replace("Van Ri", "van Ri").replace(" Rangers", "(NYR)").replace(" Islanders", "(NYI)")
                    pick_b = df_picks_b.iloc[i].replace("è", "e").replace("Van Ri", "van Ri").replace(" Rangers", "(NYR)").replace(" Islanders", "(NYI)")
                    splt_a = pick_a.split("(")
                    splt_b = pick_b.split("(")
                    box_type_a = splt_a[-1].split(")")[0].lower()
                    box_type_b = splt_b[-1].split(")")[0].lower()

                    idx_a = pick_a.find(",")
                    idx_b = pick_b.find(",")
                    pas = pick_a.split(",")
                    pbs = pick_b.split(",")
                    # pa = f"{pas[0]},{pas[1][:2]}" if (idx_a >= 0) else f"{splt_a[0].strip()} ({team_name_2_acr[splt_a[0].strip()]})"
                    # pb = f"{pbs[0]},{pbs[1][:2]}" if (idx_b >= 0) else f"{splt_b[0].strip()} ({team_name_2_acr[splt_b[0].strip()]})"
                    pa = f"{pas[0]},{pas[1][:2]}" if (idx_a >= 0) else splt_a[0].strip()
                    pb = f"{pbs[0]},{pbs[1][:2]}" if (idx_b >= 0) else splt_b[0].strip()
                    pick_a_in_r2 = player_2_team[pa] not in out_round_1
                    pick_b_in_r2 = player_2_team[pb] not in out_round_1
                    picks_in_r2 = pick_a_in_r2 and pick_b_in_r2
                    pick_a_in_r3 = (player_2_team[pa] not in out_round_1) and (player_2_team[pa] not in out_round_2)
                    pick_b_in_r3 = (player_2_team[pb] not in out_round_1) and (player_2_team[pb] not in out_round_2)
                    picks_in_r3 = pick_a_in_r3 and pick_b_in_r3
                    pick_a_in_r4 = (player_2_team[pa] not in out_round_1) and (player_2_team[pa] not in out_round_2) and (player_2_team[pa] not in out_round_3)
                    pick_b_in_r4 = (player_2_team[pb] not in out_round_1) and (player_2_team[pb] not in out_round_2) and (player_2_team[pb] not in out_round_3)
                    picks_in_r4 = pick_a_in_r4 and pick_b_in_r4
                    same = pick_a == pick_b

                    # if "(team)" in pick_a.lower():
                    #     box_type = "team"
                    # else:
                    #     if "(d)" in pick_a.lower():
                    #         box_type = "defence"
                    print(f"A:{pick_a.rjust(25)}, B:{pick_b.rjust(25)}, {same=}, {box_type_a=}, {box_type_b=}, {picks_in_r2=}, {pa=}, {pb=}, {player_2_team[pa]=}, {player_2_team[pb]=}")

                    if picks_in_r2:
                        n_picks_r2 += 1
                        if picks_in_r3:
                            n_picks_r3 += 1
                            if picks_in_r4:
                                n_picks_r4 += 1

                    if same:
                        cnt_alike += 1
                        if picks_in_r2:
                            cnt_alike_r2 += 1
                            if picks_in_r3:
                                cnt_alike_r3 += 1
                                if picks_in_r4:
                                    cnt_alike_r4 += 1

                    if box_type_a != "team":
                        if pick_a not in player_data:
                            player_data[pick_a] = {"people": set()}
                        player_data[pick_a]["people"].add(person_a)
                    else:
                        if pick_a not in team_data:
                            team_data[pick_a] = {"people": set()}
                        team_data[pick_a]["people"].add(person_a)

                    if box_type_b != "team":
                        if pick_b not in player_data:
                            player_data[pick_b] = {"people": set()}
                        player_data[pick_b]["people"].add(person_b)
                    else:
                        if pick_b not in team_data:
                            team_data[pick_b] = {"people": set()}
                        team_data[pick_b]["people"].add(person_b)

                    if i not in box_choices:
                        box_choices[i] = {"choices": dict()}

                    if pick_a not in box_choices[i]["choices"]:
                        box_choices[i]["choices"][pick_a] = 1
                    else:
                        box_choices[i]["choices"][pick_a] += 1

                    # if pick_b not in box_choices[i]["choices"]:
                    #     box_choices[i]["choices"][pick_b] = 1
                    # else:
                    #     box_choices[i]["choices"][pick_b] += 1

                pct_alike = cnt_alike / n_picks
                # percentage_alike_r1[person_a][person_b] = pct_alike
                percentage_alike_r1[person_a][person_b] = (cnt_alike, n_picks)

                pct_alike_r2 = (cnt_alike_r2 / n_picks_r2) if (n_picks_r2 != 0) else 0
                # percentage_alike_r2[person_a][person_b] = pct_alike_r2
                percentage_alike_r2[person_a][person_b] = (cnt_alike_r2, n_picks_r2) if (n_picks_r2 != 0) else (0, 0)

                pct_alike_r3 = (cnt_alike_r3 / n_picks_r3) if (n_picks_r3 != 0) else 0
                # percentage_alike_r2[person_a][person_b] = pct_alike_r2
                percentage_alike_r3[person_a][person_b] = (cnt_alike_r3, n_picks_r3) if (n_picks_r3 != 0) else (0, 0)

                pct_alike_r4 = (cnt_alike_r4 / n_picks_r4) if (n_picks_r4 != 0) else 0
                # percentage_alike_r2[person_a][person_b] = pct_alike_r2
                percentage_alike_r4[person_a][person_b] = (cnt_alike_r4, n_picks_r4) if (n_picks_r4 != 0) else (0, 0)
                print(f"\t{person_a=}, {person_b=}, {percentage_alike_r1[person_a][person_b]=}")
                print(f"\t{person_a=}, {person_b=}, {percentage_alike_r2[person_a][person_b]=}")
                print(f"\t{person_a=}, {person_b=}, {percentage_alike_r3[person_a][person_b]=}")
                print(f"\t{person_a=}, {person_b=}, {percentage_alike_r4[person_a][person_b]=}")

    for box_n, box_data in box_choices.items():
        for pick in box_data["choices"]:
            box_choices[box_n]["choices"][pick] //= (len(list_pool_people) - 1)

    print(f"{percentage_alike_r1=}")
    print(f"{percentage_alike_r2=}")
    print(f"{percentage_alike_r3=}")
    print(f"{percentage_alike_r4=}")
    print(f"{player_data=}")
    print(f"{team_data=}")

    # print(f"{[(player, player_data[player]) for player in player_data]}")
    most_picked_players_r1 = sorted(
        [(player, len(player_data[player]["people"])) for player in player_data],
        key=lambda tup: tup[1],
        reverse=True
    )
    most_picked_teams_r1 = sorted(
        [(team, len(team_data[team]["people"])) for team in team_data],
        key=lambda tup: tup[1],
        reverse=True
    )

    print(f"\n\n\n\tRESULTS\n\n\n")

    top_n_picks = 15
    print(f"\nTop {min(top_n_picks, len(most_picked_players_r1))} picked player(s)")
    for i in range(min(top_n_picks, len(most_picked_players_r1))):
        name, count = most_picked_players_r1[i]
        print(f"\t{count} x {name}")
    print(f"\nBottom {min(top_n_picks, len(most_picked_players_r1))} picked player(s)")
    for i in range(-1, -(min(top_n_picks, len(most_picked_players_r1)) + 1), -1):
        name, count = most_picked_players_r1[i]
        print(f"\t{count} x {name}")

    print(f"\nTop {min(top_n_picks, len(most_picked_teams_r1))} picked team(s)")
    for i in range(min(top_n_picks, len(most_picked_teams_r1))):
        name, count = most_picked_teams_r1[i]
        print(f"\t{count} x {name}")
    print(f"\nBottom {min(top_n_picks, len(most_picked_teams_r1))} picked team(s)")
    for i in range(-1, -(min(top_n_picks, len(most_picked_teams_r1)) + 1), -1):
        name, count = most_picked_teams_r1[i]
        print(f"\t{count} x {name}")

    print(f"{box_choices=}")
    for box_n, box_data in box_choices.items():
        print(f"{box_n+1}")
        sort_box_choices = [tup[0] for tup in sorted(
            # [(name, box_data["choices"][name] if (name in player_data) else team_data["choices"][name]) for name in box_data["choices"]]
            [(name, box_data["choices"][name]) for name in box_data["choices"]],
            key=lambda tup: (-tup[1], tup[0])
        )]
        # print(f"{sort_box_choices=}")
        for choice in sort_box_choices:
            # pool_pickers = box_choices[box_n]["choices"][choice]
            pool_pickers = player_data.get(choice, None)
            if pool_pickers is None:
                pool_pickers = team_data.get(choice)
            n_picks = box_data['choices'][choice]
            pct_pick = 100 * n_picks / len(list_pool_people)
            print(f"\t{percent(pct_pick).ljust(8)} | {str(n_picks).rjust(3)} x {choice.ljust(28)}, {pool_pickers=}")

    print(f"\n\n")
    pct_alike_matrix_r1 = set()
    pct_alike_matrix_r2 = set()
    pct_alike_matrix_r3 = set()
    pct_alike_matrix_r4 = set()
    for person_a, data_a in percentage_alike_r1.items():
        print(f"{person_a=}")
        sort_pct_choices = sorted(
            [(name, p_alike) for name, p_alike in data_a.items()],
            key=lambda tup: (-(tup[1][0] / tup[1][1]), tup[0])
        )
        for person_b, p_alike in sort_pct_choices:
            p_a = (p_alike[0] / p_alike[1]) if p_alike[1] != 0 else 0
            print(f"\t{percent(p_a).ljust(8)} | {person_b}")
            pct_alike_matrix_r1.add((min(person_a, person_b), max(person_a, person_b), p_alike))

    for person_a, data_a in percentage_alike_r2.items():
        print(f"{person_a=}")
        sort_pct_choices = sorted(
            [(name, p_alike) for name, p_alike in data_a.items()],
            key=lambda tup: (-(tup[1][0] / tup[1][1]), tup[0])
        )
        for person_b, p_alike in sort_pct_choices:
            p_a = (p_alike[0] / p_alike[1]) if p_alike[1] != 0 else 0
            print(f"\t{percent(p_a).ljust(8)} | {person_b}")
            pct_alike_matrix_r2.add((min(person_a, person_b), max(person_a, person_b), p_alike))

    for person_a, data_a in percentage_alike_r3.items():
        print(f"{person_a=}")
        sort_pct_choices = sorted(
            [(name, p_alike) for name, p_alike in data_a.items()],
            key=lambda tup: (-((tup[1][0] / tup[1][1]) if tup[1][1] != 0 else 0), tup[0])
        )
        for person_b, p_alike in sort_pct_choices:
            p_a = (p_alike[0] / p_alike[1]) if p_alike[1] != 0 else 0
            print(f"\t{percent(p_a).ljust(8)} | {person_b}")
            pct_alike_matrix_r3.add((min(person_a, person_b), max(person_a, person_b), p_alike))

    for person_a, data_a in percentage_alike_r4.items():
        print(f"{person_a=}")
        sort_pct_choices = sorted(
            [(name, p_alike) for name, p_alike in data_a.items()],
            key=lambda tup: (-((tup[1][0] / tup[1][1]) if tup[1][1] != 0 else 0), tup[0])
        )
        for person_b, p_alike in sort_pct_choices:
            p_a = (p_alike[0] / p_alike[1]) if p_alike[1] != 0 else 0
            print(f"\t{percent(p_a).ljust(8)} | {person_b}")
            pct_alike_matrix_r4.add((min(person_a, person_b), max(person_a, person_b), p_alike))

    print(f"\n\n")
    for person_a, person_b, p_alike in sorted(
        [(a, b, p) for a, b, p in pct_alike_matrix_r1],
        key=lambda tup: (tup[2][0] / tup[2][1]) if tup[2][1] != 0 else 0,
        reverse=True
    ):
        p_a = (p_alike[0] / p_alike[1]) if p_alike[1] != 0 else 0
        print(f"{percent(p_a).ljust(8)} | {person_a.rjust(12)} | {person_b.ljust(12)} | {p_alike=}")

    ################################################################################
    #  End Round 1
    ################################################################################

    players_left_r2 = [name for name, team in player_2_team.items() if team not in out_round_1]
    print(f"{players_left_r2=}")

    print(f"\n\n")
    for person_a, person_b, p_alike in sorted(
        [(a, b, p) for a, b, p in pct_alike_matrix_r2],
        key=lambda tup: (tup[2][0] / tup[2][1]) if tup[2][1] != 0 else 0,
        reverse=True
    ):
        p_a = (p_alike[0] / p_alike[1]) if p_alike[1] != 0 else 0
        print(f"{percent(p_a).ljust(8)} | {person_a.rjust(12)} | {person_b.ljust(12)} | {p_alike=}")

    ################################################################################
    #  End Round 2
    ################################################################################

    players_left_r3 = [name for name, team in player_2_team.items() if ((team not in out_round_1) and (team not in out_round_2))]
    print(f"{players_left_r3=}")

    print(f"\n\n")
    for person_a, person_b, p_alike in sorted(
        [(a, b, p) for a, b, p in pct_alike_matrix_r3],
        key=lambda tup: (tup[2][0] / tup[2][1]) if tup[2][1] != 0 else 0,
        reverse=True
    ):
        p_a = (p_alike[0] / p_alike[1]) if p_alike[1] != 0 else 0
        print(f"{percent(p_a).ljust(8)} | {person_a.rjust(12)} | {person_b.ljust(12)} | {p_alike=}")

    ################################################################################
    #  End Round 3
    ################################################################################

    players_left_r4 = [name for name, team in player_2_team.items() if ((team not in out_round_1) and (team not in out_round_2) and (team not in out_round_3))]
    print(f"{players_left_r4=}")

    print(f"\n\n")
    for person_a, person_b, p_alike in sorted(
        [(a, b, p) for a, b, p in pct_alike_matrix_r4],
        key=lambda tup: (tup[2][0] / tup[2][1], tup[2][0]) if tup[2][1] != 0 else (0, 0),
        reverse=True
    ):
        p_a = (p_alike[0] / p_alike[1]) if p_alike[1] != 0 else 0
        print(f"{percent(p_a).ljust(8)} | {person_a.rjust(12)} | {person_b.ljust(12)} | {p_alike=}")

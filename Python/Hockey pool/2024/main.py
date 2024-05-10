import pandas as pd


excel_picks = r"C:\Users\ABriggs\Documents\Coding Practice\Coding_Practice\Python\Hockey pool\2024\Pool Picks.xlsx"


if __name__ == '__main__':
    print(f"main")

    df_picks = pd.read_excel(excel_picks)
    # print(f"{df_picks=}")

    list_pool_people = sorted(list(df_picks.columns))
    print(f"Number pool people: {len(list_pool_people)}")
    percentage_alike = {}
    player_data = {}
    team_data = {}
    box_choices = {}

    for person_a in list_pool_people:
        df_picks_a = df_picks[person_a]
        percentage_alike[person_a] = {}

        print(f"{person_a=}")
        for person_b in list_pool_people:
            if person_a != person_b:
                print(f"{person_b=}")
                df_picks_b = df_picks[person_b]
                cnt_alike = 0
                n_picks = df_picks_a.shape[0]
                for i in range(n_picks):
                    pick_a = df_picks_a.iloc[i]
                    pick_b = df_picks_b.iloc[i]
                    box_type_a = pick_a.split("(")[-1].split(")")[0].lower()
                    box_type_b = pick_b.split("(")[-1].split(")")[0].lower()
                    # if "(team)" in pick_a.lower():
                    #     box_type = "team"
                    # else:
                    #     if "(d)" in pick_a.lower():
                    #         box_type = "defence"
                    print(f"{pick_a=}, {pick_b=}, {box_type_a=}, {box_type_b=}")
                    if pick_a == pick_b:
                        cnt_alike += 1

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
                percentage_alike[person_a][person_b] = pct_alike

    for box_n, box_data in box_choices.items():
        for pick in box_data["choices"]:
            box_choices[box_n]["choices"][pick] //= 20

    print(f"{percentage_alike=}")
    print(f"{player_data=}")

    print(f"{[(player, player_data[player]) for player in player_data]}")
    most_picked_players = sorted(
        [(player, len(player_data[player]["people"])) for player in player_data],
        key=lambda tup: tup[1],
        reverse=True
    )
    most_picked_teams = sorted(
        [(team, len(team_data[team]["people"])) for team in team_data],
        key=lambda tup: tup[1],
        reverse=True
    )

    print(f"\n\n\n\tRESULTS\n\n\n")

    top_n_picks = 15
    print(f"\nTop {min(top_n_picks, len(most_picked_players))} picked player(s)")
    for i in range(min(top_n_picks, len(most_picked_players))):
        name, count = most_picked_players[i]
        print(f"\t{count} x {name}")
    print(f"\nBottom {min(top_n_picks, len(most_picked_players))} picked player(s)")
    for i in range(-1, -(min(top_n_picks, len(most_picked_players)) + 1), -1):
        name, count = most_picked_players[i]
        print(f"\t{count} x {name}")

    print(f"\nTop {min(top_n_picks, len(most_picked_teams))} picked team(s)")
    for i in range(min(top_n_picks, len(most_picked_teams))):
        name, count = most_picked_teams[i]
        print(f"\t{count} x {name}")
    print(f"\nBottom {min(top_n_picks, len(most_picked_teams))} picked team(s)")
    for i in range(-1, -(min(top_n_picks, len(most_picked_teams)) + 1), -1):
        name, count = most_picked_teams[i]
        print(f"\t{count} x {name}")

    print(f"{box_choices=}")
    for box_n, box_data in box_choices.items():
        print(f"{box_n}")
        for choice in box_data["choices"]:
            # pool_pickers = box_choices[box_n]["choices"][choice]
            if choice in player_data:
                pool_pickers = player_data[choice]
            else:
                pool_pickers = team_data[choice]
            print(f"\t{choice=}, {box_data['choices'][choice]=}, {pool_pickers=}")

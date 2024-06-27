import pandas as pd
import json
import os

from utility import percent

excel_picks = r"C:\Users\ABriggs\Documents\Coding_Practice\Python\Hockey pool\2024\Pool Picks.xlsx"
player_data_by_box_json = r"C:\Users\Abriggs\Documents\Coding_Practice\Python\Hockey pool\2024\player_data_pool_2024.json"
if not os.path.exists(excel_picks):
    excel_picks = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\2024\Pool Picks.xlsx"
if not os.path.exists(player_data_by_box_json):
    player_data_by_box_json = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\2024\player_data_pool_2024.json"


if __name__ == "__main__":
    
    with open(player_data_by_box_json, "r") as f:
        player_data_by_box = json.load(f)

    df_picks = pd.read_excel(excel_picks, sheet_name=None)
    
    # print(f"{df_picks=}")
    
    real_and_best_picks = df_picks["Sheet1"]
    worst_picks = df_picks["Sheet2"]
    best_picks = real_and_best_picks["BEST_PICKS"]
    real_picks = real_and_best_picks
    del real_picks["BEST_PICKS"]
    
    print(f"{worst_picks=}\n{best_picks=}\n{real_picks=}")
    template = {"count_best": 0, "count_worst": 0, "players_best": list, "players_worst": list}
    players = dict(zip(real_picks.columns, [{k: (v() if callable(v) else v) for k, v in template.items()} for _ in range(real_picks.shape[1])]))
    print(f"{players=}")
    
    for i, row in real_picks.iterrows():
        best_pick = best_picks.iloc[i].strip().lower()
        # print(f"{i=}, {row=}")
        worst_pick = worst_picks.iloc[i]
        for player in players:
            b_pick = row[player].strip().lower()
            print(f"{b_pick=}, {best_pick=}, {player=}")
            if b_pick == best_pick:
                players[player]["count_best"] += 1
                players[player]["players_best"].append(row[player])

            print(f"{i=}, {worst_pick=}")
            for val in worst_pick:
                # w_pick = val.iloc[i]["WORST_PICKS"]
                print(f"{val=}")
                if not pd.isna(val):
                    # w_pick = val.strip().lower()
                    # print(f"{w_pick=}")
                    if b_pick == val.strip().lower():
                        players[player]["count_worst"] += 1
                        players[player]["players_worst"].append(row[player])
                        break

    print(f"{players=}")

    result_cols = ["Team", "Count Best", "Count Worst"]
    data = {
        'Team': [],
        'Count Best': [],
        'Count Worst': []
    }
    for player, stats in players.items():
        data['Team'].append(player.replace("ALFIE_C", "Sneaker Beach Leafs").replace("PATRICK_R", "This Cars Could Be Lauder").replace("_", " ").title())
        data['Count Best'].append(stats['count_best'])
        data['Count Worst'].append(stats['count_worst'])

    df_results = pd.DataFrame(data, columns=result_cols)
    df_results = df_results.sort_values(by=['Count Best', 'Count Worst'], ascending=[False, True])

    # df_results["% Best"] = df_results.apply(lambda row: percent(row["Count Best"] / 24))
    # df_results["% Best"] = df_results.apply(lambda row: percent(row["Count Best"] / 24))
    df_results["% Best"] = df_results.apply(lambda row: "{:.2%}".format(row["Count Best"] / 24), axis=1)
    df_results["% Worst"] = df_results.apply(lambda row: "{:.2%}".format(row["Count Worst"] / 24), axis=1)

    df_results.to_excel("Best Worst Analysis.xlsx", index=False)

    print(f"{df_results=}")
    
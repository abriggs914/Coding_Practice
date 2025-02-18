import json
import pandas as pd

file = "4_nations_2025_20250215.json"

with open(file, "r") as f:
    data = json.load(f)
    
    
# df_teams = pd.DataFrame(columns=["name"], data=[d["name"] for d in data["teams"]])
# df_players = pd.DataFrame(columns=["TeamIdx", "Num", "Player", "Position", "Team"])

player_row_dfs = []
team_dfs = []
for i, team_data in enumerate(data["teams"]):
    team = team_data["name"]
    roster = team_data["players"]
    team_dfs.append(pd.DataFrame([{"Name": team}]))
    for j, row in enumerate(roster[1:]):
        spl = row.split(",")
        num, player, position, team_name = spl
        row = pd.DataFrame([{
            "TeamIdx": i,
            "Num": num,
            "Player": player,
            "Position": position,
            "NHLTeam": team_name
        }])
        player_row_dfs.append(row)
df_players = pd.concat(player_row_dfs).reset_index()
df_teams = pd.concat(team_dfs).reset_index()

print(df_players)

for i, row in df_teams.iterrows():
    name = row["Name"]
    print(f"\n\t{name}")
    df_team_players = df_players.loc[df_players["TeamIdx"] == i]
    df_player_team_freq = df_team_players.groupby(
        by="NHLTeam"
    ).agg({
        "NHLTeam": "count"
    }).rename(
        columns={"NHLTeam": "TeamName"}
    ).sort_values(
        ascending=False,
        by="TeamName"
    )
    print(df_player_team_freq)


df_oal_player_team_freq = df_players.groupby(
    by="NHLTeam"
).agg({
    "NHLTeam": "count"
}).rename(
    columns={"NHLTeam": "TeamName"}
).sort_values(
    ascending=False,
    by="TeamName"
)
print("\n\tOverall")
print(df_oal_player_team_freq)
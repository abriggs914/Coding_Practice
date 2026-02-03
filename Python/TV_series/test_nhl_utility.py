import os
import datetime
import pandas as pd
from dateutil.utils import today

from nhl_utility import NHLAPIHandler, NHLSchedule, NHLGameDate, NHLBoxScore, NHLStandings
# from json_utility import jsonify
import json


DB_FILE: str = "testing_save_file_2026_02_02.json"
key_selected_team: str = "k_selected_team"
key_save_date: str = "k_save_date"


def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)


def set_selected_team():

    df_team_name_ids = df_teams[["id", "fullName"]]
    teams_text = ""
    for i, row in df_team_name_ids.iterrows():
        teams_text += f"{str(row['id']).rjust(4)} - {row['fullName'].rjust(25)}\n"
    team = input(f"Enter the id of your favourite team:\n{teams_text}\n\t")
    try:
        team = int(team)
    except ValueError:
        team = 0
    return team


def save_session():
    db[key_save_date] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DB_FILE, "w") as f:
        json.dump(db, f)


if __name__ == "__main__":
    api = NHLAPIHandler(init=True)
    db: dict = load_db()

    df_teams: pd.DataFrame = api.get_team_data()

    if key_selected_team not in db:
        db[key_selected_team] = set_selected_team()

    today: datetime.date = datetime.datetime.now().date()
    if datetime.datetime.now().hour < 3:
        today -= datetime.timedelta(days=1)
    sel_team_id = db.get(key_selected_team, 0)
    ser_sel_team: pd.Series = df_teams.loc[df_teams["id"] == sel_team_id].reset_index().iloc[0]

    print(f"Selected Team: {ser_sel_team['fullName']}")

    print("="*120)
    print("Teams")
    print(df_teams)

    standings: NHLStandings = api.get_standings(date_in=today)
    schedule: NHLSchedule = api.get_schedule(date_in=today)
    schedule_game_week: list[NHLGameDate] = schedule.game_week
    print("="*120)
    print("standings")
    print(standings.df_standings)
    print("="*120)
    print("schedule")
    print(schedule)
    print("="*120)

    for i, game_date in enumerate(schedule_game_week):
        if game_date.date == today:
            print(f"Game {i}: {game_date.date}")
            games: list[NHLBoxScore] = game_date.games
            team_plays_today = False
            for j, game in enumerate(games):
                # print(game)
                if sel_team_id in (game.away_team_id, game.home_team_id):
                    print(f"Selected Team Game: {game}")
                    team_plays_today = True
                    g_id = game.g_id
                    print(game.to_df_row())
                    landing = api.load_game_landing(g_id)
                    print("landing")
                    print(landing)
                    box_score = api.load_game_boxscore(g_id)
                    print("box_score")
                    print(box_score)
            if not team_plays_today:
                print(f"sel team does not play today {game_date.date}")

    print(api.check_game_status(sel_team_id, today))
    print("="*120)

    save_session()
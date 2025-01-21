import datetime
import os.path
from typing import Any

import pandas as pd
import requests
import streamlit as st

# from pandas_profiling import ProfileReport
# import pandas_profiling
from ydata_profiling import ProfileReport


st.set_page_config(layout="wide")


@st.cache_data(ttl=None, show_spinner=True)
def load_game_predictions() -> pd.DataFrame:
	return pd.read_excel(
		path_excel,
		skiprows=1
	)


@st.cache_data(show_spinner=True, ttl=None)
def load_game_landing(game_id: int) -> dict[str: Any]:
	print(f"New Game Landing {game_id=}, {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
	return requests.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/landing").json()


def report_name(team: str) -> str:
	return f"report_{team}.html"


# C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions.xlsx
path_excel = r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions.xlsx"

if not os.path.exists(path_excel):
	path_excel = path_excel.replace(r"abrig", r"abriggs")

	if not os.path.exists(path_excel):
		raise FileNotFoundError(f"Could not find Game Predictions Excel file '{path_excel}'.")

df_game_predictions: pd.DataFrame = load_game_predictions()
df_game_predictions = df_game_predictions[[col for col in df_game_predictions.columns if "unnamed" not in col.lower()]]
df_game_predictions = df_game_predictions.loc[df_game_predictions["GameIsOver"] == 1].reset_index(drop=True)

list_teams = sorted(df_game_predictions["HomeTeam"].dropna().unique().tolist())
team_dfs = {t: {} for t in list_teams}

for i, team in enumerate(list_teams):
	df_t_occ: pd.DataFrame = df_game_predictions.loc[
		(df_game_predictions["HomeTeam"] == team)
		| (df_game_predictions["AwayTeam"] == team)
	]
	list_columns = [
			"parent_idx",
			"date",
			"id",
			"is_home",
			"opponent",
			"my_score",
			"opp_score",
			"result",
			"won",
			"watched",
			"inter_conf",
			"inter_div",
			"watch_order",
			"watch_date"
	]
	# df_t: pd.DataFrame = pd.DataFrame()
	row_dfs = []
	for j, row in df_t_occ.iterrows():
		nhl_game_id = row["GameID"]
		game_date = row["GameDate"]
		team_away = row["AwayTeam"]
		team_home = row["HomeTeam"]
		act_score_away = row["ActualAwayScore"]
		act_score_home = row["ActualHomeScore"]
		act_winner = row["ActualWinner"]
		act_result = row["ActualResult"]
		watched = bool(row["WatchedGame"])
		inter_conf = bool(row["InterConf"])
		inter_div = bool(row["InterDiv"])
		watch_order = row["WatchOrder"]
		watch_date = row["WatchDate"]

		is_home = team_home == team
		my_score = act_score_home if is_home else act_score_away
		opp_score = act_score_away if is_home else act_score_home

		row_dfs.append(
			pd.DataFrame(
				data=[{
					"parent_idx": j,
					"date": game_date,
					"id": nhl_game_id,
					"is_home": is_home,
					"opponent": team_away if is_home else team_home,
					"my_score": my_score,
					"opp_score": opp_score,
					"result": act_result,
					"won": my_score > opp_score,
					"watched": watched,
					"inter_conf": inter_conf,
					"inter_div": inter_div,
					"watch_order": watch_order,
					"watch_date": watch_date
				}],
				columns=list_columns
			)
		)

	df_t: pd.DataFrame = pd.concat(row_dfs).reset_index(drop=True)

	df_t["game_points"] = df_t.apply(lambda row:
		2 if row["won"] else (1 if row ["result"] in ("OT", "SO") else 0)
		, axis=1
	)

	df_t["ttl_points"] = df_t["game_points"].cumsum()
	df_t["avg_points_last_5_games"] = df_t["game_points"].rolling(
		window=5
	).mean()

	df_t["ttl_gf"] = df_t["my_score"].cumsum()
	df_t["ttl_ga"] = df_t["opp_score"].cumsum()
	df_t["avg_gf_last_5_games"] = df_t["my_score"].rolling(
		window=5
	).mean()
	df_t["avg_ga_last_5_games"] = df_t["opp_score"].rolling(
		window=5
	).mean()

	df_t_ttl: pd.DataFrame = df_t[[
		"my_score",
		"opp_score",
		"game_points",
		"ttl_points",
		"avg_points_last_5_games",
		"ttl_gf",
		"ttl_ga",
		"avg_gf_last_5_games",
		"avg_ga_last_5_games"
	]].agg(["sum", "mean", "min", "max", "std"]).T

	team_dfs[team]["raw"] = df_t
	team_dfs[team]["describe"] = df_t_ttl
	rn = report_name(team)
	if not os.path.exists(os.path.join(os.getcwd(), rn)):
		profile = ProfileReport(df_t, title="Cumulative Performance Report")
		team_dfs[team]["profile"] = profile.to_file(rn)
	else:
		team_dfs[team]["profile"] = rn

st.write(df_game_predictions.head())

if st.button(
	label="check my records",
	key="btn_check_records"
):
	incorrect_games = []
	n = df_game_predictions.shape[0]
	progress_bar = st.progress(0, text="checking records...")

	for i, row in df_game_predictions.iterrows():
		print(f"{i + 1} / {n}")
		progress_bar.progress((i + 1) / n, text="checking records...")
		nhl_game_id = row["GameID"]
		game_date = row["GameDate"]
		team_away = row["AwayTeam"]
		team_home = row["HomeTeam"]
		act_score_away = row["ActualAwayScore"]
		act_score_home = row["ActualHomeScore"]
		act_winner = row["ActualWinner"]
		act_result = row["ActualResult"]

		game_data = load_game_landing(nhl_game_id)
		real_team_away = game_data.get("awayTeam", {}).get("abbrev", 0)
		real_team_home = game_data.get("homeTeam", {}).get("abbrev")
		real_score_away = game_data.get("awayTeam", {}).get("score", 0)
		real_score_home = game_data.get("homeTeam", {}).get("score", 0)
		period_num = game_data.get("periodDescriptor", {}).get("number", 1)
		game_result = game_data.get("periodDescriptor", {}).get("periodType", "").upper()

		m = ""
		if (team_away != real_team_away) or (team_home != real_team_home):
			m = (m + f"\nPossible Incorrect GameID MyRecords: ({team_away} @ {team_home}) -> ({real_team_away} @ {real_team_home})").strip()
			m = (m + f"\nPossible Incorrect GameID MyRecords: ({team_away} @ {team_home}) -> ({real_team_away} @ {real_team_home})").strip()
		if act_score_away != real_score_away:
			m = (m + f"\nIncorrect Away Score ({act_score_away}) -> ({real_score_away})").strip()
		if act_score_home != real_score_home:
			m = (m + f"\nIncorrect Home Score ({act_score_home}) -> ({real_score_home})").strip()
		if act_result != game_result:
			m = (m + f"\nIncorrect Result ({act_result}) -> ({game_result})").strip()

		if m:
			m = f"\nGameID ({nhl_game_id}) {team_away} @ {team_home} on {game_date}\n\t-" + "\n\t-".join(m.split("\n"))
			incorrect_games.append(m)

	if incorrect_games:
		print("\n".join(incorrect_games))
		st.write(incorrect_games)
	else:
		st.write("completed without errors")


selectbox_team = st.selectbox(
	label="Choose a team to view game stats",
	key="selectbox_team",
	options=list_teams
)

if selectbox_team:
	select_team = st.session_state.get("selectbox_team")
	st.dataframe(
		team_dfs[select_team]["raw"]
	)
	st.dataframe(
		team_dfs[select_team]["describe"]
	)
	# with open(report_name(select_team), "r") as f:
	# 	st.html(f.read())
	# 	# st.markdown(f.read(), unsafe_allow_html=True)
	path_html_file = os.path.join(os.getcwd(), report_name(select_team))
	st.link_button(label=f"{select_team} Report", url=path_html_file)
	st.code(path_html_file)
	import pathlib
	p1 = pathlib.Path(path_html_file).as_uri()
	st.code(p1)
	st.link_button(label="P1", url=p1)

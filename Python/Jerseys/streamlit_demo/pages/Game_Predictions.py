import datetime
import os.path
from typing import Any

import matplotlib.colors
import pandas as pd
import requests
import streamlit as st

# from pandas_profiling import ProfileReport
# import pandas_profiling
import streamlit.components.v1 as components
from ydata_profiling import ProfileReport
import plotly.express as px

from colour_utility import gradient, gradient_merge, GREEN, RED, WHITE, YELLOW, Colour
from streamlit_utility import aligned_text, display_df
from nhl_utility import reverse_lookup


cache_hold_time = 2*60*60

st.set_page_config(layout="wide")


@st.cache_data(ttl=cache_hold_time, show_spinner=True)
def load_game_predictions() -> pd.DataFrame:
	return pd.read_excel(
		path_excel,
		skiprows=1,
		sheet_name="DataRegularSeason20242025"
	)


@st.cache_data(ttl=cache_hold_time, show_spinner=True)
def load_rest_sheets_game_predictions() -> dict:
	return pd.read_excel(
		path_excel,
		sheet_name=None
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

rest_sheets: dict[str: pd.DataFrame] = load_rest_sheets_game_predictions()
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


def score_to_points(record: str) -> int:
    try:
        w, l, otl = map(int, record.split("-"))
        pts = (2 * w) + otl
        gms = sum([w, l, otl])
        if toggle_normalize:
            return pts / (gms if gms != 0 else 1)
        else:
            return pts
    except (ValueError, AttributeError) as e:
        return 0


def pts_colour(record: str) -> str:
	try:
		w, l, otl = map(int, record.split("-"))

		return rg_grads[(2 * w) + otl].hex_code
	except (ValueError, AttributeError) as e:
		return WHITE
        

def records_to_points_df(df: pd.DataFrame) -> pd.DataFrame:
    df_numeric = df.copy()
    for i in range(df.shape[0]):
        for j in range(0, df.shape[1]):  # skip label column
            if i == j:
                # same team
                df_numeric.iloc[i, j] = -1
            else:
                val = df.iloc[i, j]
                if pd.isna(val):
                    df_numeric.iloc[i, j] = 0
                else:
                    df_numeric.iloc[i, j] = score_to_points(val)
    
    # Convert to numeric dtype (in case it's still object)
    df_numeric.iloc[:, :] = df_numeric.iloc[:, :].apply(pd.to_numeric)

    # Sort rows by total points across columns
    df_numeric["RowSum"] = df_numeric.iloc[:, :].sum(axis=1)
    df_numeric = df_numeric.sort_values(by="RowSum", ascending=False)
    df_numeric = df_numeric.drop(columns=["RowSum"])

    # Sort columns (excluding label col) by total points across rows
    col_sums = df_numeric.iloc[:, :].sum(axis=0).sort_values(ascending=False)
    # sorted_cols = [df_numeric.columns[0]] + col_sums.index.tolist()
    sorted_cols = col_sums.index.tolist()

    df_numeric = df_numeric[sorted_cols]
    
    print(f"df_numeric")
    print(df_numeric)
                
    return df_numeric



# rg_grads: list[str] = [gradient(i, 8, RED, GREEN, rgb=False) for i in range(8 + 1)]
# rg_grads: list[str] = [gradient(i, 4, RED, YELLOW, rgb=False) for i in range(4)]
# rg_grads += [gradient(i, 4, YELLOW, GREEN, rgb=False) for i in range(5)]
rg_grads = gradient_merge([GREEN, YELLOW, RED], 14, as_hex=True)
ordered_teams = [
	"ANA", "CGY", "EDM", "LAK", "SEA", "SJS", "VAN", "VGK",
	"CHI", "COL", "DAL", "MIN", "NSH", "STL", "UTA", "WPG",
	"CAR", "CBJ", "NJD", "NYI", "NYR", "PHI", "PIT", "WSH",
	"BOS", "BUF", "DET", "FLA", "MTL", "OTT", "TBL", "TOR"
]
grid = [st.columns(33) for _ in range(33)]
st.write(ordered_teams)
df_team_records: pd.DataFrame = rest_sheets["Sheet5"].iloc[:32, :33]
df_team_stats: pd.DataFrame = rest_sheets["StatsRegularSeason20242025"].iloc[:32, :90]


cont_heatmap = st.container(border=True)

with cont_heatmap:
    toggle_normalize = st.toggle(
        label="Normalize by PPG?",
        value=False
    )


records = [v for v in pd.unique(df_team_records.iloc[1:, 1:].values.ravel()) if not pd.isna(v)]
records.sort(key=lambda r: (-score_to_points(r), -int(r[0]), sum(map(int, r.split("-")))))
record_colours = dict(zip(records, rg_grads))
record_colours["0-0-0"] = Colour("#CFAFAF").hex_code
record_colours["1-1-0"] = Colour("#4F4F4F").hex_code
record_colours["2-2-0"] = Colour("#7F7F7F").hex_code

df_team_records.rename(
    columns={
        df_team_records.columns[0]: "Team"
    },
    inplace=True
)

st.write("rest_sheets['Sheet5']")
st.write(rest_sheets['Sheet5'])
st.write("df_team_records")
st.write(df_team_records)
st.write("rg_grads")
st.write(rg_grads)
st.write("records")
st.write(records)
st.write("record_colours")
st.write(record_colours)

for i, row in df_team_records.iterrows():
	if i == 0:
		for j, col in enumerate(df_team_records.columns):
			grid[i + 1][j].markdown(
				aligned_text(
					col,
					colour=pts_colour(col),
					tag_style="h6"
				),
				unsafe_allow_html=True
			)
	for j, val in enumerate(row):
		if not pd.isna(val):
			if j == 0:
				colour = None
			else:
				colour = record_colours[val]
			grid[i + 1][j].markdown(
				aligned_text(
					val,
					colour=colour,
					tag_style="h6"
				),
				unsafe_allow_html=True
			)

	if i == (df_team_records.shape[0] - 1):
		for j, col in enumerate(df_team_records.columns):
			if j == (len(df_team_records.columns) - 1):
				grid[i + 1][j].empty()
			grid[i + 1][j].markdown(
				aligned_text(
					col,
					colour=pts_colour(col),
					tag_style="h6"
				),
				unsafe_allow_html=True
			)


df_numeric = records_to_points_df(df_team_records.iloc[0:, 1:])
st.write("df_numeric")
st.write(df_numeric)
ys = [df_team_records.loc[i, "Team"] for i in df_numeric.index.tolist()]  # team names
st.write(f"ys: {ys}")
with cont_heatmap:
    fig = px.imshow(
        df_numeric,
        labels=dict(y="Team", x="Opponent", color="Points"),
        x=df_numeric.columns.tolist(),
        y=ys,
        color_continuous_scale=px.colors.sequential.Turbo,  # or custom
        width=800,
        height=800
    )



    st.plotly_chart(fig, use_container_width=True)


# df_team_points: pd.DataFrame = rest_sheets["Sheet2"].iloc[:32, :-70]
#
# st.write("df_team_points1")
# st.dataframe(df_team_points)
# st.write("df_c")
#
# date_cols = df_team_points.columns.tolist()[3:]
# df_c = df_team_points.copy()[["Team"] + date_cols]
# df_c = df_c.transpose().reset_index().rename(columns={"index": "Date"})
# team_col_names = df_c.iloc[0][1:].values.tolist()
# df_c = df_c.drop(0)
# df_c.rename(columns=dict(zip(range(32), team_col_names)), inplace=True)
# df_c.reset_index(inplace=True, drop=True)
# df_c["Points"] = df_c.apply(lambda row: min(row[1:].values), axis=1)
# st.dataframe(df_c)
#
# df_team_points = df_team_points.melt(
# 	id_vars="Team",
# 	value_vars=df_team_points.columns.tolist()[3:],
# 	value_name="Points"
# ).rename(columns={"variable": "Date"})
# st.write("df_team_points2")
# st.dataframe(df_team_points)
#
# chart = px.line(
# 	df_c,
# 	x="Date",
# 	# y="Points",
# 	y=df_c.columns.tolist()[1:],
# 	# color="Team",
# 	width=1500,
# 	height=865,
# 	animation_group="Points",
# 	animation_frame="Date",
# 	range_x=[df_team_points["Date"].min(), df_team_points["Date"].max()],
# 	range_y=[df_team_points["Points"].min(), df_team_points["Points"].max()]
# )
#
# st.plotly_chart(
# 	chart,
# 	use_container_width=True
# )


def get_playoff_matchups():
	playoff_teams = get_playoff_teams()
	top_west = playoff_teams["pacific"][:1] + playoff_teams["central"][:1]
	top_east = playoff_teams["metropolitan"][:1] + playoff_teams["atlantic"][:1]
	wc_west = playoff_teams["wc_west"]
	wc_east = playoff_teams["wc_east"]
	if not tie_break_swap(*top_west):
		top_west = top_west[::-1]
	if not tie_break_swap(*top_east):
		top_east = top_east[::-1]

	playoffs = {
		"p1_wc" : playoff_teams["pacific"][:1] + [wc_west[top_west.index(playoff_teams["pacific"][0])]],
		"c1_wc" : playoff_teams["central"][:1] + [wc_west[top_west.index(playoff_teams["central"][0])]],
		"p2_p3": playoff_teams["pacific"][1:],
		"c2_c3": playoff_teams["central"][1:],
		"m2_m3": playoff_teams["metropolitan"][1:],
		"a2_a3": playoff_teams["atlantic"][1:],
		"m1_wc" : playoff_teams["metropolitan"][:1] + [wc_east[top_east.index(playoff_teams["metropolitan"][0])]],
		"a1_wc" : playoff_teams["atlantic"][:1] + [wc_east[top_east.index(playoff_teams["atlantic"][0])]]
	}

	return playoffs

def get_playoff_teams():
	playoffs = {
		"pacific": [],
		"central": [],
		"metropolitan": [],
		"atlantic": []
	}

	for t in list_teams:
		playoffs[reverse_lookup(t, "div")].append(t)

	for k, lst in playoffs.items():
		# lst.sort(key=lambda x: df_team_stats.loc[df_team_stats["Teams"] == t].iloc[0]["PTS"], reverse=True)
		need_swaps = True
		while need_swaps:
			need_swaps = False
			for i in range(len(lst) - 1):
				a = lst[i]
				b = lst[i + 1]
				tb = tie_break_swap(a, b)
				if tb:
					playoffs[k][i], playoffs[k][i + 1] = b, a
					need_swaps = True

	wc_west = playoffs["pacific"][3:6] + playoffs["central"][3:6]
	wc_east = playoffs["metropolitan"][3:6] + playoffs["atlantic"][3:6]

	for lst in [wc_west, wc_east]:
		need_swaps = True
		while need_swaps:
			need_swaps = False
			for i in range(len(lst) - 1):
				a = lst[i]
				b = lst[i + 1]
				tb = tie_break_swap(a, b)
				if tb:
					lst[i], lst[i + 1] = b, a
					need_swaps = True
	#
	# need_swaps = True
	# while need_swaps:
	# 	need_swaps = False
	# 	for i in range(len(wc_east) - 1):
	# 		a = wc_east[i]
	# 		b = wc_east[i + 1]
	# 		tb = tie_break_swap(a, b)
	# 		if tb:
	# 			wc_east[i], wc_east[i + 1] = b, a
	# 			need_swaps = True

	for k in playoffs:
		playoffs[k] = playoffs[k][:3]
	playoffs["wc_west"] = wc_west[:2]
	playoffs["wc_east"] = wc_east[:2]

	return playoffs

def tie_break_swap(team_a, team_b) -> bool:
	# Tie-Breaking Procedure
	# If two or more clubs are tied in points during the regular season, the standing of the clubs is determined in the following order:
	# The fewer number of games played (i.e., superior points percentage).
	# The greater number of games won, excluding games won in Overtime or by Shootout (i.e., 'Regulation Wins'). This figure is reflected in the RW column.
	# The greater number of games won, excluding games won by Shootout. This figure is reflected in the ROW column.
	# The greater number of games won by the Club in any manner (i.e., 'Total Wins'). This figure is reflected in the W column.
	# The greater number of points earned in games against each other among two or more tied clubs. For the purpose of determining standing for two or more Clubs that have not played an even number of games with one or more of the other tied Clubs, the first game played in the city that has the extra game (the 'odd game') shall not be included. When more than two Clubs are tied, the percentage of available points earned in games among each other (and not including any 'odd games') shall be used to determine standing.
	# The greater differential between goals for and against (including goals scored in Overtime or awarded for prevailing in Shootouts) for the entire regular season. This figure is reflected in the DIFF column.
	# The greater number of goals scored (including goals scored in Overtime or awarded for prevailing in Shootouts) for the entire regular season. This figure is reflected in the GF column.
	# NOTE: In standings a victory in a shootout counts as one goal for, while a shootout loss counts as one goal against.
	df_team_a = df_team_stats.loc[df_team_stats["Teams"] == team_a].iloc[0]
	df_team_b = df_team_stats.loc[df_team_stats["Teams"] == team_b].iloc[0]
	pts_a = df_team_a["PTS"]
	pts_b = df_team_b["PTS"]
	print(f"{team_a} ({pts_a}) vs {team_b} ({pts_b})")
	if pts_b > pts_a:
		# B has more points than A
		return True
	elif pts_a > pts_b:
		return False

	pts_p_a = df_team_a["PTS%"]
	pts_p_b = df_team_b["PTS%"]
	if pts_p_b > pts_p_a:
		# B has better points % than A
		return True
	elif pts_p_a > pts_p_b:
		return False

	rw_a = df_team_a["RW"]
	rw_b = df_team_b["RW"]
	if rw_b > rw_a:
		# B has more RW than A
		return True
	elif rw_a > rw_b:
		return False

	row_a = df_team_a["ROW"]
	row_b = df_team_b["ROW"]
	if row_b > row_a:
		# B has more ROW than A
		return True
	elif row_a > row_b:
		return False

	w_a = df_team_a["W"]
	w_b = df_team_b["W"]
	if w_b > w_a:
		# B has more W than A
		return True
	elif w_a > w_b:
		return False

	raise ValueError("Branches not written yet to compare season head-to-head")

def mirror_chart(title: str, left: tuple, right: tuple, width: int = 600, height: int = 300):
	# title = "GF"
	# left_value = 8
	# right_value = 4
	left_label = "A"
	right_label = "B"
	left_colour = Colour("#008FFB")
	right_colour = Colour("#FF4560")

	if isinstance(left, tuple):
		left_label, left_value = left
	elif isinstance(left, dict):
		left_label = left.get("label", left_label)
		left_value = left.get("value")
		left_colour = Colour(left.get("colour", left_colour))

	if isinstance(right, tuple):
		right_label, right_value = right
	elif isinstance(right, dict):
		right_label = right.get("label", right_label)
		right_value = right.get("value")
		right_colour = Colour(right.get("colour", right_colour))

	# Determine max value for symmetric axis
	max_value = max(left_value, right_value) * 1.2  # extra padding

	components.html(f"""
	<!DOCTYPE html>
	<html>
	  <head>
		<script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
	  </head>
	  <body>
		<div id="chart"></div>
		<script>
		  var options = {{
			chart: {{
			  type: 'bar',
			  height: {height * 2/3},
			  width: {width},
			  stacked: true,
			  toolbar: {{ show: false }}
			}},
			plotOptions: {{
			  bar: {{
				horizontal: true,
				barHeight: '60%',
			  }}
			}},
			stroke: {{
			  width: 1,
			  colors: ['#fff']
			}},
			series: [
			  {{
				name: '{left_label}',
				data: [-{left_value}]
			  }},
			  {{
				name: '{right_label}',
				data: [{right_value}]
			  }}
			],
			xaxis: {{
			  min: -{max_value},
			  max: {max_value},
			  categories: ['{title}'],
			  labels: {{
				formatter: function(val) {{
				  return Math.abs(val);
				}}
			  }}
			}},
			tooltip: {{
			  shared: false,
			  x: {{
				formatter: function(val) {{
				  return Math.abs(val);
				}}
			  }}
			}},
			colors: ['{left_colour.hex_code}', '{right_colour.hex_code}'],
			dataLabels: {{
			  enabled: true,
			  formatter: function (val) {{
				return Math.abs(val);
			  }}
			}}
		  }};

		  var chart = new ApexCharts(document.querySelector("#chart"), options);
		  chart.render();
		</script>
	  </body>
	</html>
	""", height=height)

display_df(
	df_team_stats,
	"Stats"
)

playoff_matchups = get_playoff_matchups()
# st.write(get_playoff_teams())
st.write(playoff_matchups)

df_playoff_matchups = {}

cols_round_1 = {
	"west": st.columns(4),
	"east": st.columns(4)
}
for i, matchup_key in enumerate(playoff_matchups):
	with cols_round_1["east" if i >= 4 else "west"][i % 4]:
		st.write(matchup_key)
		home, away = playoff_matchups[matchup_key]
		st.write(away)
		st.write("@")
		st.write(home)
		df_matchups = df_game_predictions.loc[
			(
					(df_game_predictions["HomeTeam"] == home)
					& (df_game_predictions["AwayTeam"] == away)
			)
			| (
					(df_game_predictions["HomeTeam"] == away)
					& (df_game_predictions["AwayTeam"] == home)
			)
		]
		df_playoff_matchups[matchup_key] = df_matchups

		for i, row in df_matchups.iterrows():
			t_h = row["HomeTeam"]
			t_a = row["AwayTeam"]
			s_h = int(row["ActualHomeScore"])
			s_a = int(row["ActualAwayScore"])
			g_d = row["GameDate"]

			st.write(f"{g_d:%Y-%m-%d}")
			st.write(f"({s_a}) {t_a} @ {t_h} ({s_h})")

		t_a, t_h = df_matchups.iloc[0][["AwayTeam", "HomeTeam"]]
		df_a_a = df_matchups.loc[df_matchups["AwayTeam"] == t_a]
		df_a_h = df_matchups.loc[df_matchups["HomeTeam"] == t_a]

		df_h_a = df_matchups.loc[df_matchups["AwayTeam"] == t_h]
		df_h_h = df_matchups.loc[df_matchups["HomeTeam"] == t_h]

		gf_a = df_a_a["ActualAwayScore"].sum() + df_a_h["ActualHomeScore"].sum()
		gf_h = df_h_a["ActualAwayScore"].sum() + df_h_h["ActualHomeScore"].sum()
		ga_a, ga_h = gf_h, gf_a

		mirror_chart(
			title="GF",
			left={
				"label": t_a,
				"value": gf_a
			},
			right={
				"label": t_h,
				"value": gf_h
			},
			width=400,
			height=200
		)

		mirror_chart(
			title="GA",
			left={
				"label": t_a,
				"value": ga_a
			},
			right={
				"label": t_h,
				"value": ga_h
			},
			width=400,
			height=200
		)


		# st.write(away)
		# pg_pct_correct_prediction = st.progress(
		# 	value=df_matchups["CorrectWinnerPrediction"].value_counts(normalize=True)[0]
		# )
		#
		# st.write(home)
		# pg_pct_correct_prediction = st.progress(
		# 	value=df_matchups["CorrectWinnerPrediction"].value_counts(normalize=True)[0]
		# )

		st.write("% Correct")
		pg_pct_correct_prediction = st.progress(
			value=df_matchups["CorrectWinnerPrediction"].value_counts(normalize=True)[0]
		)

		btn_sel_matchup = st.button(
			label="view",
			key=f"btn_sel_matchup_{i}",
			on_click=lambda mu=matchup_key: st.session_state.update({"selected_matchup": mu})
		)


if st.session_state.get("selected_matchup"):
	sel_matchup = st.session_state.get("selected_matchup")
	df_sel_matchup = df_playoff_matchups[sel_matchup]
	st.dataframe(df_sel_matchup)

	t_a, t_h = df_sel_matchup.iloc[0][["AwayTeam", "HomeTeam"]]
	df_a_a = df_sel_matchup.loc[df_sel_matchup["AwayTeam"] == t_a]
	df_a_h = df_sel_matchup.loc[df_sel_matchup["HomeTeam"] == t_a]

	df_h_a = df_sel_matchup.loc[df_sel_matchup["AwayTeam"] == t_h]
	df_h_h = df_sel_matchup.loc[df_sel_matchup["HomeTeam"] == t_h]

	gf_a = df_a_a["ActualAwayScore"].sum() + df_a_h["ActualHomeScore"].sum()
	gf_h = df_h_a["ActualAwayScore"].sum() + df_h_h["ActualHomeScore"].sum()
	ga_a, ga_h = gf_h, gf_a

	st.write(f"({gf_a}) {t_a} VS {t_h} ({gf_h})")
	mirror_chart(
		title="GF",
		left={
			"label": t_a,
			"value": gf_a
		},
		right={
			"label": t_h,
			"value": gf_h
		}
	)
	mirror_chart(
		title="GA",
		left={
			"label": t_a,
			"value": ga_a
		},
		right={
			"label": t_h,
			"value": ga_h
		}
	)


# from streamlit_apex_charts import st_apexcharts
#
# st_apexcharts(
#     options={
#         "chart": {"type": "bar"},
#         "plotOptions": {
#             "bar": {
#                 "horizontal": True,
#                 "barHeight": "80%",
#             }
#         },
#         "xaxis": {"categories": ["Comparison"]},
#         "colors": ["#FF4560", "#008FFB"]
#     },
#     series=[
#         {"name": "Left Team", "data": [-65]},  # Negative values flip left
#         {"name": "Right Team", "data": [70]}
#     ],
#     type="bar",
#     height=150,
#     width="100%"
# )


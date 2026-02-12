import pandas as pd
import plotly.express as px
from streamlit_utility import st, display_df_paginated
from utility import percent

from typing import Optional

import os


@st.cache_data(show_spinner=True, show_time=True)
def read_excel(pth: str) -> pd.DataFrame:
    if not os.path.exists(pth):
        if r"\abrig\documents" in pth.lower():
            pth_o = pth
            pth = pth.lower().replace(r"\abrig\documents", r"\abriggs\documents")
            if not os.path.exists(pth):
                raise FileNotFoundError(f"Could not open '{pth_o}'")
    return pd.read_excel(pth)


def describe_score_cols(df_games: pd.DataFrame, team: Optional[str] = None):
    df_home_games: pd.DataFrame = df_games[df_games["HomeTeam"] == team] if team is not None else df_games
    df_away_games: pd.DataFrame = df_games[df_games["AwayTeam"] == team] if team is not None else df_games

    df_p_away_score: pd.DataFrame = df_away_games["PredictedAwayScore"].describe()
    df_p_away_score["mode"] = df_away_games["PredictedAwayScore"].mode().iloc[0]
    st.write(df_p_away_score)

    df_p_home_score: pd.DataFrame = df_home_games["PredictedHomeScore"].describe()
    df_p_home_score["mode"] = df_home_games["PredictedHomeScore"].mode().iloc[0]
    st.write(df_p_home_score)

    df_a_away_score: pd.DataFrame = df_away_games["ActualAwayScore"].describe()
    df_a_away_score["mode"] = df_away_games["ActualAwayScore"].mode().iloc[0]
    st.write(df_a_away_score)

    df_a_home_score: pd.DataFrame = df_home_games["ActualHomeScore"].describe()
    df_a_home_score["mode"] = df_home_games["ActualHomeScore"].mode().iloc[0]
    st.write(df_a_home_score)


@st.cache_data(show_spinner=True, show_time=True)
def line_season_points_cache(df_games: pd.DataFrame, team: Optional[str] = None):
    fig = px.line(
        df_games,
        x="GameDate",
        y="RunningPoints",
        title=f"Season Points Totals for {team}"
    )
    fd = df_games["GameDate"].min().date()
    ld = df_games["GameDate"].max().date()
    dd = (ld - fd).days
    post_msg = f"Pts / Day = {df_games['RunningPoints'].max() / dd:.3f}"
    return fig, post_msg


def line_season_points(df_games: pd.DataFrame, team: Optional[str] = None):
    fig, post_msg = line_season_points_cache(
        df_games=df_games,
        team=team
    )
    st.plotly_chart(
        fig,
        key=f"k_line_points_{team}"
    )
    st.write(post_msg)


@st.cache_data(show_spinner=True, show_time=True)
def pie_scores_cache(df_games: pd.DataFrame, actual: bool = True, home: bool = True):
    col_a = "Actual" if actual else "Predicted"
    col_b = "Home" if home else "Away"
    col_c = "Score"
    col = col_a + col_b + col_c

    counts = df_games[col].value_counts()
    proportions = df_games[col].value_counts(normalize=True)
    top_values = counts.index

    df_score_counts: pd.DataFrame = pd.DataFrame({
        "Value": top_values,
        "Count": counts.loc[top_values].values,
        "Proportion": proportions.loc[top_values].values
    }).sort_values(by="Value", ascending=False)

    # st.write("df_score_counts")
    # st.write(df_score_counts)

    fig = px.pie(
        df_score_counts,
        names="Value",       # labels
        values="Proportion", # values
        title=f"{col_a} {col_b} {col_c} Distribution",
        hole=0.15
    )

    # Optional: Customize chart appearance
    fig.update_traces(textinfo="percent+label", pull=[0.05, 0, 0, 0])

    # Display in Streamlit
    post_msg: str = f"Average: {df_games[col].mean():.3f}, StD.: {df_games[col].std():.3f}"
    return fig, post_msg


def pie_scores(df_games: pd.DataFrame, actual: bool = True, home: bool = True):
    fig, post_msg = pie_scores_cache(df_games=df_games, actual=actual, home=home)
    st.plotly_chart(fig, key=f"k_pie_scores_{df_games.shape=}_{actual=}_{home=}")
    st.write(post_msg)


def running_score(df_games: pd.DataFrame) -> pd.DataFrame:
    df_games["NewPointsAway"] = df_games.apply(lambda row: 
        2 if row["AwayTeam"] == row["ActualWinner"] else (1 if row["ActualResult"] in ["OT", "SO"] else 0)
        , axis=1
    )
    df_games["NewPointsHome"] = df_games.apply(lambda row: 
        2 if row["HomeTeam"] == row["ActualWinner"] else (1 if row["ActualResult"] in ["OT", "SO"] else 0)
        , axis=1
    )

    df_games[["RunningPointsAway", "RunningPointsHome"]] = (0, 0)

    team_pts = dict(zip(lst_teams, [0 for _ in lst_teams]))
    for i, row in df_games.iterrows():
        a_team: str = row["AwayTeam"]
        h_team: str = row["HomeTeam"]
        a_pts: int = row["NewPointsAway"]
        h_pts: int = row["NewPointsHome"]
        team_pts[a_team] += a_pts
        team_pts[h_team] += h_pts
        df_games.loc[i, "RunningPointsAway"] = team_pts[a_team]
        df_games.loc[i, "RunningPointsHome"] = team_pts[h_team]
    
    return df_games


st.set_page_config(
    layout="wide"
)


excel_paths = {
    "20242025": r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions_2425_copy.xlsx",
    "20252026": r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions_2526_copy.xlsx"
}


excel_dfs = {
    k: read_excel(pth)
    for k, pth in excel_paths.items()
}

games_show_cols: list = [
    "GameID",
    "GameDate",
    "PredictedAwayScore",
    "AwayTeam",
    "HomeTeam",
    "PredictedHomeScore",
    "PredictedResult",
    "GameIsOver",
    "ActualAwayScore",
    "ActualHomeScore",
    "ActualResult",
    "CorrectWinnerPrediction",
    "GamePredictionScore",
    "GamePredictionScore2"
]


k_selectbox_season: str = "k_selectbox_season"
st.session_state.setdefault(k_selectbox_season, None)
selectbox_season = st.selectbox(
    label=f"Select a Season",
    options=list(excel_dfs.keys()) + [None],
    key=k_selectbox_season
)


if selectbox_season:
    st.header(f"Data from the {selectbox_season[:4]} - {selectbox_season[4:]} Season")
    df_season: pd.DataFrame = excel_dfs[selectbox_season]

    lst_teams: list = sorted(df_season["AwayTeam"].dropna().unique().tolist())
    lst_game_dates: list = sorted(df_season["GameDate"].dropna().unique().tolist())

    df_season = running_score(df_season)

    k_checkbox_complete_games_only: str = "key_checkbox_complete_games_only"
    st.session_state.setdefault(k_checkbox_complete_games_only, True)
    checkbox_complete_games_only = st.checkbox(
        label="Complete Games Only?",
        key=k_checkbox_complete_games_only
    )

    if checkbox_complete_games_only:
        df_season = df_season[df_season["GameIsOver"].isin([1, "Y"])]

    t_games: int = df_season.shape[0]
    df_season_games_completed: pd.DataFrame = df_season[df_season["GameIsOver"] == 1]
    t_games_complete: int = df_season_games_completed.shape[0]
    t_games_left: int = t_games - t_games_complete
    p_games_complete: float = t_games_complete / t_games
    season_complete: bool = t_games_complete == t_games

    if season_complete:
        st.subheader(f"All {t_games} Games Complete")
    else:
        st.subheader(f"{t_games_left} Games Left to Play")

    st.divider()

    cols_control = st.columns(2)

    with cols_control[0]:

        k_selectbox_team: str = "k_selectbox_team"
        st.session_state.setdefault(k_selectbox_team, None)
        selectbox_team = st.selectbox(
            label=f"Select a Team",
            options=lst_teams + [None],
            key=k_selectbox_team
        )

        if selectbox_team:
            df_team_games = df_season[
                (df_season["AwayTeam"] == selectbox_team)
                | (df_season["HomeTeam"] == selectbox_team)
            ]

            t_team_games: int = df_team_games.shape[0]

            df_predicted_winners: pd.DataFrame = df_team_games[
                (
                    (df_team_games["AwayTeam"] == selectbox_team)
                    & (df_team_games["PredictedAwayScore"] > df_team_games["PredictedHomeScore"])
                )
                | (
                    (df_team_games["HomeTeam"] == selectbox_team)
                    & (df_team_games["PredictedHomeScore"] > df_team_games["PredictedAwayScore"])
                )
            ]
            df_predicted_losers: pd.DataFrame = df_team_games[~df_team_games["GameID"].isin(df_predicted_winners["GameID"])]

            k_stdf_predicted_winners: str = "key_stdf_predicted_winners"
            display_df_paginated(
                df_predicted_winners[games_show_cols],
                "Times Predicted Winner:",
                key=k_stdf_predicted_winners,
                batch_size_options=(100, 250, 1000)
            )

            k_stdf_predicted_losers: str = "key_stdf_predicted_losers"
            display_df_paginated(
                df_predicted_losers[games_show_cols],
                "Times Predicted Loser:",
                key=k_stdf_predicted_losers,
                batch_size_options=(100, 250, 1000)
            )

            df_pw_s: pd.DataFrame = df_predicted_winners[df_predicted_winners["CorrectWinnerPrediction"].isin([1, "Y"])]
            df_pl_s: pd.DataFrame = df_predicted_losers[df_predicted_losers["CorrectWinnerPrediction"].isin([1, "Y"])]
            df_pw_s["PredictedToWin"] = 1
            df_pl_s["PredictedToWin"] = 0
            df_correct_predictions = pd.concat(
                [
                    df_pw_s,
                    df_pl_s
                ],
                ignore_index=True
            ).sort_values("GameDate")

            t_predicted_winner: int = df_predicted_winners.shape[0]
            p_predicted_winner: float = t_predicted_winner / t_team_games
            t_predicted_correct: int = df_correct_predictions.shape[0]
            p_predicted_correct: float = t_predicted_correct / t_team_games

            # describe_score_cols(df_team_games, selectbox_team)

            pb_season_progress: st.progress = st.progress(
                value=p_games_complete,
                text="Season Completion: " + percent(p_games_complete)
            )

            pb_predicted_winner: st.progress = st.progress(
                value=p_predicted_winner,
                text="Predicted Winner: " + percent(p_predicted_winner)
            )

            k_stdf_correct_predictions: str = "key_stdf_correct_predictions"
            display_df_paginated(
                df_correct_predictions[games_show_cols],
                "Times Predicted Correcly:",
                key=k_stdf_correct_predictions,
                batch_size_options=(100, 250, 1000)
            )

            p_predicted_correctly: float = t_predicted_correct / t_team_games
            pb_predicted_correctly: st.progress = st.progress(
                value=p_predicted_correctly,
                text="Predicted Correctly: " + percent(p_predicted_correctly)
            )

            cols_pie = st.columns(2)
            with cols_pie[0]:
                pie_scores(df_team_games, actual=False, home=False)
                pie_scores(df_team_games, actual=True, home=False)
            with cols_pie[1]:
                pie_scores(df_team_games, actual=False, home=True)
                pie_scores(df_team_games, actual=True, home=True)

            line_season_points(df_team_games, selectbox_team)

    with cols_control[1]:
        st.write("All Game Data:")
        describe_score_cols(df_season)

        cols_pie = st.columns(2)
        with cols_pie[0]:
            pie_scores(df_season, actual=False, home=False)
            pie_scores(df_season, actual=True, home=False)
        with cols_pie[1]:
            pie_scores(df_season, actual=False, home=True)
            pie_scores(df_season, actual=True, home=True)

        line_season_points(df_season, selectbox_team=None)

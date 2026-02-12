import pandas as pd
from streamlit_utility import st, display_df_paginated

import os


@st.cache_data(show_spinner=True, show_time=True)
def read_excel(pth: str) -> pd.DataFrame:
    return pd.read_excel(pth)


excel_paths = {
    "20242025": r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions_2425_copy.xlsx"
}


excel_dfs = {
    k: read_excel(pth)
    for k, pth in excel_paths.items()
}


k_selectbox_season: str = "k_selectbox_season"
st.session_state.setdefault(k_selectbox_season, None)
selectbox_season = st.selectbox(
    label=f"Select a Season",
    options=list(excel_dfs.keys()) + [None],
    key=k_selectbox_season
)


def describe_score_cols(df_games: pd.DataFrame):
    df_p_away_score: pd.DataFrame = df_games["PredictedAwayScore"].describe()
    df_p_away_score["mode"] = df_games["PredictedAwayScore"].mode().iloc[0]
    st.write(df_p_away_score)

    df_p_home_score: pd.DataFrame = df_games["PredictedHomeScore"].describe()
    df_p_home_score["mode"] = df_games["PredictedHomeScore"].mode().iloc[0]
    st.write(df_p_home_score)

    df_a_away_score: pd.DataFrame = df_games["ActualAwayScore"].describe()
    df_a_away_score["mode"] = df_games["ActualAwayScore"].mode().iloc[0]
    st.write(df_a_away_score)

    df_a_home_score: pd.DataFrame = df_games["ActualHomeScore"].describe()
    df_a_home_score["mode"] = df_games["ActualHomeScore"].mode().iloc[0]
    st.write(df_a_home_score)


if selectbox_season:
    st.header(f"Data from the {selectbox_season[:4]} - {selectbox_season[4:]} Season")
    df_season: pd.DataFrame = excel_dfs[selectbox_season]
    t_games: int = df_season.shape[0]
    df_season_games_completed: pd.DataFrame = df_season[df_season["GameIsOver"] == 1]
    t_games_complete: int = df_season_games_completed.shape[0]
    t_games_left: int = t_games - t_games_complete
    season_complete: bool = t_games_complete == t_games
    lst_teams: list = sorted(df_season["AwayTeam"].dropna().unique().tolist())
    lst_game_dates: list = sorted(df_season["GameDate"].dropna().unique().tolist())

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
                df_predicted_winners,
                "Times Predicted Winner:",
                key=k_stdf_predicted_winners,
                batch_size_options=(100, 250, 1000)
            )

            k_stdf_predicted_losers: str = "key_stdf_predicted_losers"
            display_df_paginated(
                df_predicted_losers,
                "Times Predicted Loser:",
                key=k_stdf_predicted_losers,
                batch_size_options=(100, 250, 1000)
            )

            describe_score_cols(df_team_games)

    with cols_control[1]:
        st.write("All Game Data:")
        describe_score_cols(df_season)

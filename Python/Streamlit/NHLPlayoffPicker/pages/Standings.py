import datetime
import requests
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards


# from NHLPlayoffPicker import NHL_API_Handler as nhl_api


class NHLAPIHandler:
    # 2023-12-18 0336

    def __init__(self):
        self.history = {}

    HOST_NAME = f"https://api-web.nhle.com"

    def query_url(self, url, do_print=False, check_history=True) -> dict | None:
        if do_print:
            print(f"{url=}")

        if check_history:
            if url in self.history:
                return self.history[url]

        response = requests.get(url)
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204:
            ct = response.headers["Content-Type"].lower()
            if ct.startswith("application/json"):
                self.history[url] = response.json()
            elif ct.startswith("text/javascript"):
                self.history[url] = eval(response.text.replace("jsonFeed(", "")[:-2])

        return self.history.get(url, None)

    def get_calendar_schedule(self, date: datetime.date, do_print=False) -> dict | None:
        url = f"{NHLAPIHandler.HOST_NAME}/v1/schedule-calendar/{date:%Y-%m-%d}"
        if do_print:
            print(f"{url=}")
        # schedule keys
        # ['endDate', 'nextStartDate', 'previousStartDate', 'startDate', 'teams']
        # teams list keys
        # ['id', 'seasonId', 'commonName', 'abbrev', 'name', 'placeName', 'logo', 'darkLogo', 'isNhl', 'french']
        return self.query_url(url)

    def get_schedule(self, date: datetime.date, do_print=False) -> dict | None:
        """Get 1 week's schedule of games"""
        url = f"{NHLAPIHandler.HOST_NAME}/v1/schedule/{date:%Y-%m-%d}"
        if do_print:
            print(f"{url=}")
        # schedule keys
        # ['nextStartDate', 'previousStartDate', 'gameWeek', 'oddsPartners', 'preSeasonStartDate', 'regularSeasonStartDate', 'regularSeasonEndDate', 'playoffEndDate', 'numberOfGames']
        return self.query_url(url)

    def get_geolocation(self, do_print=False) -> dict | None:
        url = "https://geolocation.onetrust.com/cookieconsentpub/v1/geo/location"
        if do_print:
            print(f"{url=}")
        return self.query_url(url)

    def get_country(self, do_print=False) -> dict | None:
        url = f"{NHLAPIHandler.HOST_NAME}/v1/location"
        if do_print:
            print(f"{url=}")
        return self.query_url(url)

    def get_score(self, date: datetime.date, do_print=False) -> dict | None:
        """Get scores for a particular date"""
        # score keys:
        # ['prevDate', 'currentDate', 'nextDate', 'gameWeek', 'oddsPartners', 'games']
        url = f"{NHLAPIHandler.HOST_NAME}/v1/score/{date:%Y-%m-%d}"
        if do_print:
            print(f"{url=}")
        return self.query_url(url)

    def get_standings(self, date: datetime.date, do_print=False) -> dict | None:
        """Get standings up to a particular date"""
        # standings keys:
        # ['wildCardIndicator', 'standings']
        url = f"{NHLAPIHandler.HOST_NAME}/v1/standings/{date:%Y-%m-%d}"
        if do_print:
            print(f"{url=}")
        return self.query_url(url)


if __name__ == '__main__':

    st.set_page_config(page_title="Standings", layout="wide")

    for k, v in {
        "choice_standings_chart_view": None,
        "choice_standings_profile": None
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

    today = datetime.datetime.today()

    st.title("NHL Standings")
    st.markdown(f"###### as of {today:%Y-%m-%d}")

    nhl_api = NHLAPIHandler()

    standings_dict = nhl_api.get_standings(today)
    standings_dict = standings_dict["standings"]
    keys_to_update = [
        ("placeName", "default"),
        ("teamName", "default"),
        ("teamCommonName", "default"),
        ("teamAbbrev", "default"),
        ("Record", lambda row: f"{row['wins']}-{row['losses']}-{row['otLosses']}"),
        ("SO", lambda row: f"{row['shootoutWins']}-{row['shootoutLosses']}"),
        ("Streak", lambda row: f"{row['streakCode']}{row['streakCount']}")
    ]
    for i, dat in enumerate(standings_dict):
        for k, ik in keys_to_update:
            if k in standings_dict[i]:
                standings_dict[i][k] = standings_dict[i][k][ik]
            else:
                standings_dict[i][k] = ik(row=dat)

    df_standings = pd.DataFrame(standings_dict)
    calc_keys = {
        "Pts Out Top Div": -99,
        "Pts Out Top Conf": -99,
        "Pts Out Div Seed": -99,
        "Pts Out Wildcard": -99
    }
    for k, v in calc_keys.items():
        df_standings[k] = int(v)

    selectable_cols_df_standings = {
        "leagueSequence": "Place League",
        "conferenceSequence": "Conf Place",
        "divisionSequence": "Div Place",
        "wildcardSequence": "WC Place",
        "conferenceName": "Conf",
        "divisionName": "Div",
        "placeName": "Team Place",
        "teamLogo": "Logo",
        "teamName": "Team",
        "teamCommonName": "Mascot",
        "teamAbbrev": "T",
        "gamesPlayed": "GP",
        "points": "PTS",
        "pointPctg": "PTS %",
        "regulationPlusOtWinPctg": "ROW PTS %",
        "regulationWinPctg": "RW PTS %",
        "wins": "W",
        "losses": "L",
        "winPctg": "W %",
        "otLosses": "OTL",
        "shootoutLosses": "SOL",
        "shootoutWins": "SOW",
        "streakCode": "streakCode",
        "streakCount": "streakCount",
        "regulationPlusOtWins": "ROW",
        "regulationWins": "RW",
        "goalFor": "GF",
        "goalAgainst": "GA",
        "goalDifferential": "DIFF",
        "goalDifferentialPctg": "GDIFF %",
        "goalsForPctg": "GF %",

        "homeGamesPlayed": "GP_H",
        "homeGoalDifferential": "GDIFF_H",
        "homeGoalsAgainst": "GA_H",
        "homeGoalsFor": "GF_H",
        "homeWins": "W_H",
        "homeLosses": "L_H",
        "homeOtLosses": "OTL_H",
        "homePoints": "PTS_H",
        "homeRegulationPlusOtWins": "ROW_H",
        "homeRegulationWins": "RW_H",

        "roadGamesPlayed": "GP_A",
        "roadGoalDifferential": "GDIFF_A",
        "roadGoalsAgainst": "GA_A",
        "roadGoalsFor": "GF_A",
        "roadWins": "W_A",
        "roadLosses": "L_A",
        "roadOtLosses": "OTL_A",
        "roadPoints": "PTS_A",
        "roadRegulationPlusOtWins": "ROW_A",
        "roadRegulationWins": "RW_A",

        "l10GoalDifferential": "GDIFF_L10",
        "l10GoalsAgainst": "GA_L10",
        "l10GoalsFor": "GF_L10",
        "l10Losses": "L_L10",
        "l10OtLosses": "OTL_L10",
        "l10Points": "P_L10",
        "l10RegulationPlusOtWins": "ROW_L10",
        "l10RegulationWins": "RW_L10",
        "l10Wins": "W_L10",
        "leagueHomeSequence": "Home League Place",
        "leagueRoadSequence": "Away League Place",
        "leagueL10Sequence": "L10 League Place",

        "Record": "Record"
    }

    selectable_cols_df_standings_2 = {
        "leagueSequence": "Place League",
        "conferenceAbbrev": "Conf",
        "divisionAbbrev": "Div",
        "teamLogo": "Logo",
        "teamAbbrev": "T",
        "teamCommonName": "Team",
        "points": "PTS",
        "pointPctg": "PTS %",
        "Record": "Record",
        "gamesPlayed": "GP",
        "wins": "W",
        "losses": "L",
        "otLosses": "OTL",
        "SO": "SO",
        "regulationWins": "RW",
        "regulationPlusOtWins": "ROW",
        "winPctg": "W %",
        "regulationPlusOtWinPctg": "ROW PTS %",
        "regulationWinPctg": "RW PTS %",

        "goalFor": "GF",
        "goalAgainst": "GA",
        "goalDifferential": "DIFF",

        "Streak": "Streak",
        "goalDifferentialPctg": "GDIFF %",
        "goalsForPctg": "GF %",

        "homeGamesPlayed": "GP_H",
        "homeGoalDifferential": "GDIFF_H",
        "homeGoalsAgainst": "GA_H",
        "homeGoalsFor": "GF_H",
        "homeWins": "W_H",
        "homeLosses": "L_H",
        "homeOtLosses": "OTL_H",
        "homePoints": "PTS_H",
        "homeRegulationPlusOtWins": "ROW_H",
        "homeRegulationWins": "RW_H",

        "roadGamesPlayed": "GP_A",
        "roadGoalDifferential": "GDIFF_A",
        "roadGoalsAgainst": "GA_A",
        "roadGoalsFor": "GF_A",
        "roadWins": "W_A",
        "roadLosses": "L_A",
        "roadOtLosses": "OTL_A",
        "roadPoints": "PTS_A",
        "roadRegulationPlusOtWins": "ROW_A",
        "roadRegulationWins": "RW_A",

        "l10GoalDifferential": "GDIFF_L10",
        "l10GoalsAgainst": "GA_L10",
        "l10GoalsFor": "GF_L10",
        "l10Losses": "L_L10",
        "l10OtLosses": "OTL_L10",
        "l10Points": "P_L10",
        "l10RegulationPlusOtWins": "ROW_L10",
        "l10RegulationWins": "RW_L10",
        "l10Wins": "W_L10",
        "leagueHomeSequence": "Home League Place",
        "leagueRoadSequence": "Away League Place",
        "leagueL10Sequence": "L10 League Place"
        ,

        "conferenceSequence": "Conf Place",
        "divisionSequence": "Div Place",
        "wildcardSequence": "WC Place",

        "Pts Out Div Seed": "Pts Out Div Seed",
        "Pts Out Wildcard": "Pts Out Wildcard"
    }

    st.dataframe(
        df_standings,
        hide_index=True
    )

    place_dict = dict(zip(range(32), range(1, 33)))

    # df_c2 = df_standings[selectable_cols_df_standings.keys()].rename(index=place_dict, columns=selectable_cols_df_standings)
    # df_c2.index.names = ["League Place"]

    df_c2 = df_standings[selectable_cols_df_standings.keys()].rename(columns=selectable_cols_df_standings)
    st.data_editor(
        df_c2,
        column_config={
            selectable_cols_df_standings["teamLogo"]: st.column_config.ImageColumn(
                "Logo", help="team logo"
            )
        },
        hide_index=True,
        disabled=True
    )

    st.divider()

    df_sel_2 = df_standings[selectable_cols_df_standings_2.keys()].rename(columns=selectable_cols_df_standings_2)
    df_league_1 = df_sel_2
    df_conf_w_1 = df_sel_2.loc[df_sel_2["Conf"] == "W"]
    df_conf_e_1 = df_sel_2.loc[df_sel_2["Conf"] == "E"]

    for df in [df_conf_w_1, df_conf_e_1]:
        df["Place League"] = df["Conf Place"]
        df.rename(columns={"Place League": "Conf #"}, inplace=True)
        # del df["Conf"]
        # del df["Div"]

    df_div_a_1 = df_sel_2.loc[df_sel_2["Div"] == "A"]
    df_div_m_1 = df_sel_2.loc[df_sel_2["Div"] == "M"]
    df_div_c_1 = df_sel_2.loc[df_sel_2["Div"] == "C"]
    df_div_p_1 = df_sel_2.loc[df_sel_2["Div"] == "P"]

    lst_div_codes = ["p", "c", "m", "a"]
    lst_conf_codes = ["w", "e"]
    top_conf_pts = dict(zip(lst_conf_codes, [df_conf_e_1, df_conf_w_1]))
    top_conf_pts = {k: df[selectable_cols_df_standings_2["points"]].max() for k, df in top_conf_pts.items()}

    top_div_pts = dict(zip(lst_div_codes, [df_div_p_1, df_div_c_1, df_div_m_1, df_div_a_1]))
    top_div_pts = {k: df[selectable_cols_df_standings_2["points"]].max() for k, df in top_div_pts.items()}

    for c_code, d_code, df in [
        ("e", "a", df_div_a_1),
        ("e", "m", df_div_m_1),
        ("w", "c", df_div_c_1),
        ("w", "p", df_div_p_1)
    ]:
        df["Place League"] = df["Div Place"]
        df["Pts Out Top Conf"] = (df[selectable_cols_df_standings_2["points"]] - top_conf_pts[c_code]).astype("int32")
        df["Pts Out Top Div"] = (df[selectable_cols_df_standings_2["points"]] - top_div_pts[d_code]).astype("int32")
        df.rename(columns={"Place League": "Div #"}, inplace=True)
        # del df["Conf"]
        # del df["Div"]

    # assert isinstance(df_conf_w_1, pd.DataFrame)
    # df_conf_w_sort_pts = df_conf_w_1.sort_values(selectable_cols_df_standings_2["points"], ascending=False)
    # df_conf_e_sort_pts = df_conf_e_1.sort_values(selectable_cols_df_standings_2["points"], ascending=False)
    #
    # df_top3_conf_w = df_conf_w_sort_pts.head(3)
    # df_top3_conf_e = df_conf_e_sort_pts.head(3)

    # sort by pts
    df_div_a_sort_pts = df_div_a_1.sort_values(selectable_cols_df_standings_2["points"], ascending=False)
    df_div_m_sort_pts = df_div_m_1.sort_values(selectable_cols_df_standings_2["points"], ascending=False)
    df_div_c_sort_pts = df_div_c_1.sort_values(selectable_cols_df_standings_2["points"], ascending=False)
    df_div_p_sort_pts = df_div_p_1.sort_values(selectable_cols_df_standings_2["points"], ascending=False)

    # top 3
    df_top3_div_a = df_div_a_sort_pts.head(3)
    df_top3_div_m = df_div_m_sort_pts.head(3)
    df_top3_div_c = df_div_c_sort_pts.head(3)
    df_top3_div_p = df_div_p_sort_pts.head(3)

    # bottom 5
    df_bottom5_div_a = df_div_a_sort_pts.tail(5)
    df_bottom5_div_m = df_div_m_sort_pts.tail(5)
    df_bottom5_div_c = df_div_c_sort_pts.tail(5)
    df_bottom5_div_p = df_div_p_sort_pts.tail(5)

    df_conf_e_bottom10_sort_pts = pd.concat([df_bottom5_div_a, df_bottom5_div_m]).sort_values(
        selectable_cols_df_standings_2["points"], ascending=False)
    df_conf_w_bottom10_sort_pts = pd.concat([df_bottom5_div_c, df_bottom5_div_p]).sort_values(
        selectable_cols_df_standings_2["points"], ascending=False)

    df_conf_e_wc = df_conf_e_bottom10_sort_pts.head(2)
    df_conf_w_wc = df_conf_w_bottom10_sort_pts.head(2)

    df_conf_e_out_wc = df_conf_e_bottom10_sort_pts.tail(8)
    df_conf_w_out_wc = df_conf_w_bottom10_sort_pts.tail(8)

    min_div_seed_pts = dict(zip(lst_div_codes, [df_top3_div_p, df_top3_div_c, df_top3_div_m, df_top3_div_a]))
    min_div_seed_pts = {k: df[selectable_cols_df_standings_2["points"]].min() + 1 for k, df in min_div_seed_pts.items()}

    min_conf_wc_pts = dict(zip(lst_conf_codes, [df_conf_w_wc, df_conf_e_wc]))
    min_conf_wc_pts = {k: df[selectable_cols_df_standings_2["points"]].min() + 1 for k, df in min_conf_wc_pts.items()}

    print(f"{min_div_seed_pts=}")
    print(f"{min_conf_wc_pts=}")

    # # update dfs with "Pts out of Playoff spot, and wildcard spot"
    # for c_code, d_code, df in [
    #     ("e", "a", df_div_a_1),
    #     ("e", "m", df_div_m_1),
    #     ("w", "c", df_div_c_1),
    #     ("w", "p", df_div_p_1),
    # ]:
    #     # df["Pts Out Div Seed"] = 0 if (df[selectable_cols_df_standings_2["points"]] == (min_div_seed_pts[d_code] - 1)) else (df[selectable_cols_df_standings_2["points"]] - min_div_seed_pts[d_code])
    #     # df["Pts Out Wildcard"] = df[selectable_cols_df_standings_2["points"]] - min_conf_wc_pts[c_code]
    #     df["Pts Out Div Seed"] = np.where(df[selectable_cols_df_standings_2["points"]] == (min_div_seed_pts[d_code] - 1), 0, (df[selectable_cols_df_standings_2["points"]] - min_div_seed_pts[d_code]))
    #     df["Pts Out Wildcard"] = np.where(df[selectable_cols_df_standings_2["points"]] == (min_conf_wc_pts[c_code] - 1), 0, (df[selectable_cols_df_standings_2["points"]] - min_conf_wc_pts[c_code]))

    # update the top and bottom dfs
    for df in [
        df_conf_w_1,
        df_conf_e_1,
        df_div_a_1,
        df_div_m_1,
        df_div_c_1,
        df_div_p_1,
        df_conf_e_wc,
        df_conf_w_wc,
        df_conf_w_out_wc,
        df_conf_e_out_wc,
        df_top3_div_p,
        df_top3_div_c,
        df_top3_div_m,
        df_top3_div_a,
        df_bottom5_div_p,
        df_bottom5_div_c,
        df_bottom5_div_m,
        df_bottom5_div_a
    ]:
        for i, row in df.iterrows():
            pts = row[selectable_cols_df_standings_2["points"]]
            div = row["Div"].lower()
            conf = row["Conf"].lower()
            df.loc[i, 'Pts Out Div Seed'] = 0 if pts == min_div_seed_pts[div] else int(pts - min_div_seed_pts[div])
            df.loc[i, 'Pts Out Wildcard'] = 0 if pts == min_conf_wc_pts[conf] else int(pts - min_conf_wc_pts[conf])
            df.loc[i, "Pts Out Top Conf"] = 0 if pts == top_conf_pts[conf] else int(pts - top_conf_pts[conf])
        # # df['Pts Out Div Seed'] = np.where(df[selectable_cols_df_standings_2["points"]] == (min_div_seed_pts[d_code] - 1), 0, (df[selectable_cols_df_standings_2["points"]] - min_div_seed_pts[d_code]))
        # df['Pts Out Div Seed'] = np.where(df[selectable_cols_df_standings_2["points"]] == (min_div_seed_pts[d_code if d_code != "GET_DIV" else df["Div"].str.lower()] - 1), 0, (df[selectable_cols_df_standings_2["points"]] - min_div_seed_pts[d_code if d_code != "GET_DIV" else df["Div"].str.lower()]))
        # df["Pts Out Wildcard"] = np.where(df[selectable_cols_df_standings_2["points"]] == (min_conf_wc_pts[c_code] - 1), 0, (df[selectable_cols_df_standings_2["points"]] - min_conf_wc_pts[c_code]))



    # # update the top and bottom dfs
    # for c_code, d_code, df in [
    #     ("e", "GET_DIV", df_conf_e_wc),
    #     ("e", "GET_DIV", df_conf_w_wc),
    #     ("w", "GET_DIV", df_conf_w_out_wc),
    #     ("e", "GET_DIV", df_conf_e_out_wc),
    #     ("w", "p", df_top3_div_p),
    #     ("w", "c", df_top3_div_c),
    #     ("e", "m", df_top3_div_m),
    #     ("e", "a", df_top3_div_a),
    #     ("w", "p", df_bottom5_div_p),
    #     ("w", "c", df_bottom5_div_c),
    #     ("e", "m", df_bottom5_div_m),
    #     ("e", "a", df_bottom5_div_a)
    # ]:
    #     # df['Pts Out Div Seed'] = np.where(df[selectable_cols_df_standings_2["points"]] == (min_div_seed_pts[d_code] - 1), 0, (df[selectable_cols_df_standings_2["points"]] - min_div_seed_pts[d_code]))
    #     df['Pts Out Div Seed'] = np.where(df[selectable_cols_df_standings_2["points"]] == (min_div_seed_pts[d_code if d_code != "GET_DIV" else df["Div"].str.lower()] - 1), 0, (df[selectable_cols_df_standings_2["points"]] - min_div_seed_pts[d_code if d_code != "GET_DIV" else df["Div"].str.lower()]))
    #     df["Pts Out Wildcard"] = np.where(df[selectable_cols_df_standings_2["points"]] == (min_conf_wc_pts[c_code] - 1), 0, (df[selectable_cols_df_standings_2["points"]] - min_conf_wc_pts[c_code]))

    print(f"{df_div_a_1=}")

    stss_chart_view = st.session_state["choice_standings_chart_view"]
    stss_profile = st.session_state["choice_standings_profile"]

    graph_items_options = {
        "League": {
            "graph_options": {
                "Entire League": df_league_1
            },
            "height": 1175
        },
        "Conference": {
            "graph_options": {
                "Eastern": df_conf_e_1,
                "Westerm": df_conf_w_1
            },
            "height": 600
        },
        "Division": {
            "graph_options": {
                "Atlantic": df_div_a_1,
                "Metroploitan": df_div_m_1,
                "Central": df_div_c_1,
                "Pacific": df_div_p_1
            }
        },
        "Wildcard": {
            "graph_options": {
                "Eastern Conference": st.divider,
                "Atlantic": df_top3_div_a,
                "Metropolitan": df_top3_div_m,
                "East Wildcard": df_conf_e_wc,
                "East Remainder": df_conf_e_out_wc,
                "Western Conference": st.divider,
                "Central": df_top3_div_c,
                "Pacific": df_top3_div_p,
                "West Wildcard": df_conf_w_wc,
                "West Remainder": df_conf_w_out_wc
            }
        }
    }

    radio_standings_view = st.radio(
        "Choose Order 👇",
        graph_items_options.keys(),
        key="choice_standings_chart_view",
        horizontal=True,
    )

    radio_profile_view = st.radio(
        "Profile",
        ["Chart", "Low", "Graph"],
        key="choice_standings_profile",
        horizontal=True,
    )

    if stss_chart_view is not None:
        if stss_profile == "Chart":
            graphs = graph_items_options[stss_chart_view]["graph_options"]
            height = graph_items_options[stss_chart_view].get("height", None)
            for t, df in graphs.items():
                st.subheader(t)
                if callable(df):
                    df()
                else:
                    params = {
                        "hide_index": True,
                        "disabled": True
                    }
                    if height:
                        params["height"] = height

                    st.data_editor(
                        df,
                        column_config={
                            selectable_cols_df_standings["teamLogo"]: st.column_config.ImageColumn(
                                "Logo", help="team logo"
                            )
                        },
                        **params
                    )
        elif stss_profile == "Low":
            if stss_chart_view == "Conference":
                west_col, east_col = st.columns(2)
                west_rows, east_rows = [], []

                for df, col, lst, met_diff_key in (
                        (df_conf_w_1, west_col, west_rows, "Pts Out Top Conf"),
                        (df_conf_e_1, east_col, east_rows, "Pts Out Top Conf")
                ):
                    for i, row in df.iterrows():
                        team = row[selectable_cols_df_standings_2["teamCommonName"]]
                        logo = row[selectable_cols_df_standings_2["teamLogo"]]
                        pts = row[selectable_cols_df_standings_2["points"]]
                        met_diff = int(row[met_diff_key])
                        lst.append(col.columns([0.4, 0.6]))
                        c1, c2 = lst[-1]
                        # c1.image(logo, caption=f"{team}")
                        # c2.markdown(pts)
                        c1.image(logo, caption=f"{team}")
                        # c2.markdown(pts)
                        c2.metric(":gray[PTS]", pts, met_diff)

                # pac_col, cen_col = west_col.columns(2)
                # met_col, atl_col = east_col.columns(2)
            elif stss_chart_view == "Division":
                west_rows, east_rows = [], []

                pac_col, cen_col, met_col, atl_col = st.columns(4)

                for df, col, lst, met_diff_key in (
                        (df_div_p_1, pac_col, west_rows, "Pts Out Top Div"),
                        (df_div_c_1, cen_col, west_rows, "Pts Out Top Div"),
                        (df_div_m_1, met_col, east_rows, "Pts Out Top Div"),
                        (df_div_a_1, atl_col, east_rows, "Pts Out Top Div")
                ):
                    for i, row in df.iterrows():
                        team = row[selectable_cols_df_standings_2["teamCommonName"]]
                        logo = row[selectable_cols_df_standings_2["teamLogo"]]
                        pts = row[selectable_cols_df_standings_2["points"]]
                        met_diff = int(row[met_diff_key])
                        lst.append(col.columns([0.4, 0.6]))
                        c1, c2 = lst[-1]
                        # c1.image(logo, caption=f"{team} logo")
                        # c2.markdown(pts)
                        c1.image(logo, caption=f"{team}")
                        # c2.markdown(pts)
                        c2.metric(":gray[PTS]", pts, met_diff)
            elif stss_chart_view == "Wildcard":
                west_rows, east_rows = [], []

                pac_col, cen_col, met_col, atl_col = st.columns(4)
                add_vertical_space(1)
                west_wc_col, east_wc_col = st.columns(2)
                add_vertical_space(1)
                # rest_p_col, rest_c_col, space_col, rest_m_col, rest_a_col = st.columns(5)
                rest_w_col, space_col, rest_e_col = st.columns(3)

                for df, col, lst, met_diff_key in (
                        ("Pacific", pac_col, west_rows, ""),
                        ("Central", cen_col, west_rows, ""),
                        ("Metropolitan", met_col, east_rows, ""),
                        ("Atlantic", atl_col, east_rows, ""),
                        (df_top3_div_p, pac_col, west_rows, "Pts Out Top Div"),
                        (df_top3_div_c, cen_col, west_rows, "Pts Out Top Div"),
                        (df_top3_div_m, met_col, east_rows, "Pts Out Top Div"),
                        (df_top3_div_a, atl_col, east_rows, "Pts Out Top Div"),
                        ("West Wildcard", west_wc_col, west_rows, ""),
                        ("East Wildcard", east_wc_col, east_rows, ""),
                        (df_conf_w_wc, west_wc_col, west_rows, "Pts Out Div Seed"),
                        (df_conf_e_wc, east_wc_col, east_rows, "Pts Out Div Seed"),

                        ("West Remainder", rest_w_col, west_rows, ""),
                        ("East Remainder", rest_e_col, east_rows, ""),
                        (df_conf_w_out_wc, rest_w_col, west_rows, "Pts Out Wildcard"),
                        (df_conf_e_out_wc, rest_e_col, west_rows, "Pts Out Wildcard"),

                        # (df_bottom5_div_p, rest_p_col, west_rows, "Pts Out Wildcard"),
                        # (df_bottom5_div_c, rest_c_col, west_rows, "Pts Out Wildcard"),
                        # (df_bottom5_div_m, rest_m_col, east_rows, "Pts Out Wildcard"),
                        # (df_bottom5_div_a, rest_a_col, east_rows, "Pts Out Wildcard")
                ):
                    if isinstance(df, pd.DataFrame):
                        for i, row in df.iterrows():
                            team = row[selectable_cols_df_standings_2["teamCommonName"]]
                            logo = row[selectable_cols_df_standings_2["teamLogo"]]
                            pts = row[selectable_cols_df_standings_2["points"]]
                            met_diff = row[met_diff_key]
                            lst.append(col.columns([0.4, 0.6]))
                            c1, c2 = lst[-1]
                            c1.image(logo, caption=f"{team}")
                            # c2.markdown(pts)
                            c2.metric(":gray[PTS]", pts, met_diff)
                    else:
                        lst.append(col.columns([0.25, 0.75]))
                        c1, c2 = lst[-1]
                        c2.subheader(df)

        elif stss_profile == "Graph":
            pass
        else:
            st.markdown("Select a profile to view standings.")

    style_metric_cards(background_color="#112336", border_left_color="#1551CC", border_color="#FFCF88", border_radius_px=9)

    st.divider()

    # st.dataframe(
    #     df_c2,
    #     hide_index=True
    # )

    df_exp_standings = dataframe_explorer(df_standings)
    st.dataframe(
        df_exp_standings,
        hide_index=True
    )

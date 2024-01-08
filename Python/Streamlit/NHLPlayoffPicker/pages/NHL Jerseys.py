from typing import Literal

from PIL import Image
from streamlit_extras.add_vertical_space import add_vertical_space

import streamlit as st
import pandas as pd
import platform
import datetime
import requests
from pandas import NaT

from streamlit_timeline import timeline

jerseys_excel_path = r"D:\NHL Jerseys.xlsm"

labels_choice_toggle_unique_teams = [f"All Jersey Data", f"Unique Teams Only"]


def exclusive_mean(lst, invalid=None):
    ttl = 0
    count = 0
    if invalid is None:
        invalid = set()
    for v in lst:
        if v not in invalid:
            ttl += v
            count += 1
    return ttl / count


class NHLAPIHandler:
    # 2023-12-21 0036

    HOST_NAME = f"https://api-web.nhle.com"

    def __init__(self):
        self.history = {}

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

    def is_game_ongoing_now(self, include_pregames: bool = True, r_type: Literal["bool", "dict", "next_games"] = "bool") -> bool | dict:
        """Return True if a game is in the 'LIVE' state or optionally 'PRE' state NOW!"""
        valid = ["LIVE"] + ([] if not include_pregames else ["PRE"])
        now = datetime.datetime.now()

        # check yesterday first since east coast means late night games
        gy = self.get_score((now + datetime.timedelta(days=-1)).date())
        gsy = [g["gameState"] in valid for g in gy["games"]]
        print(f"{gy=}\n{gsy=}")
        if any(gsy):
            return True if r_type == "bool" else gy

        # check today's games
        gt = self.get_score(now.date())
        gst = [g["gameState"] in valid for g in gt["games"]]
        print(f"{gt=}\n{gst=}")
        if any(gst):
            return True if r_type == "bool" else gt
        return False if r_type == "bool" else (gt if r_type == "next_games" else {})

    def are_games_going_on_today(self, include_finals: bool = True, r_type: Literal["bool", "dict", "next_games"] = "bool") -> bool | dict:
        """Return True if a game is on the 'LIVE' state or optionally 'PRE' state NOW!"""
        valid = ["FUT", "PRE", "LIVE"]
        now = datetime.datetime.now()

        # check yesterday first since east coast means late night games
        gy = self.get_score((now + datetime.timedelta(days=-1)).date())
        if any([g["gameState"] in valid for g in gy["games"]]):
            return True if r_type == "bool" else gy

        valid += ([] if not include_finals else ["FINAL", "OFF"])

        # check today's games
        gt = self.get_score(now.date())
        if any([g["gameState"] in valid for g in gt["games"]]):
            return True if r_type == "bool" else gt
        return False if r_type == "bool" else (gt if r_type == "next_games" else {})


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


# def click_choice_toggle_unique_teams():
#     # choice_toggle_unique_teams["label"] = labels_choice_toggle_unique_teams[0 if st.session_state["choice_toggle_unique_teams"] else 1]
#     st.session_state["choice_toggle_unique_teams"] = not st.session_state["choice_toggle_unique_teams"]


if __name__ == '__main__':

    print(f"\n\n\trerun\n\n")

    st.set_page_config(layout="wide")

    if platform.uname().node == "DESKTOP-47DUBI9":

        if "choice_toggle_unique_teams" not in st.session_state:
            st.session_state["choice_toggle_unique_teams"] = False

        # home computer
        # read_excel = pd.read_excel(jerseys_excel_path, "JerseyData")
        read_excel = pd.ExcelFile(jerseys_excel_path)
        sheet_jersey_data = pd.read_excel(read_excel, "JerseyData")
        sheet_nhl_teams = pd.read_excel(read_excel, "NHLTeams")
        sheet_conferences = pd.read_excel(read_excel, "Conferences")
        sheet_divisions = pd.read_excel(read_excel, "Divisions")
        print(f"{type(read_excel)=}\n{read_excel=}")

        sheet_nhl_teams = sheet_nhl_teams.merge(sheet_conferences, on="Conference", how="inner")
        sheet_nhl_teams = sheet_nhl_teams.merge(sheet_divisions, on="Division", how="inner")

        valid_home = ["home", "alternate", "reverse retro"]
        valid_away = ["away", "hockey fights cancer"]

        home_labels = [lbl for lbl in sheet_jersey_data["Colours"].dropna().unique().tolist() if ("home" in lbl.lower()) or ("alternate" in lbl.lower()) or ("reverse retro" in lbl.lower())]
        away_labels = [lbl for lbl in sheet_jersey_data["Colours"].dropna().unique().tolist() if ("away" in lbl.lower()) or ("fights cancer" in lbl.lower())]

        print(f"{home_labels=}, {away_labels=}")

        # choice_toggle_unique_teams = st.button(
        #     label=labels_choice_toggle_unique_teams[0 if st.session_state["choice_toggle_unique_teams"] else 1],
        #     # key="choice_toggle_unique_teams",
        #     on_click=click_choice_toggle_unique_teams,
        #     type="primary"
        # )

        choice_toggle_unique_teams = st.toggle(
            label=f"Unique Teams",
            key="choice_toggle_unique_teams"
            # on_click=click_choice_toggle_unique_teams,
            # type="primary"
        )

        if st.session_state["choice_toggle_unique_teams"]:
            jersey_stat_sheet_jersey_data = sheet_jersey_data.drop_duplicates(subset=["Team"], keep="first")
        else:
            jersey_stat_sheet_jersey_data = sheet_jersey_data.copy()

        jerseys_home = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Colours"].isin(home_labels)]
        jerseys_away = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Colours"].isin(away_labels)]

        jerseys_forward = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Position"] == "Forward"]
        jerseys_defence = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Position"] == "Defence"]
        jerseys_goalie = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Position"] == "Goalie"]

        distinct_owned_teams = jersey_stat_sheet_jersey_data["Team"].dropna().unique()
        distinct_owned_teams_homes = jerseys_home["Team"].dropna().unique()
        distinct_owned_teams_aways = jerseys_away["Team"].dropna().unique()

        jerseys_eastern = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Conference"] == "Eastern"]
        jerseys_western = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Conference"] == "Western"]

        jerseys_atlantic = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Division"] == "Atlantic"]
        jerseys_metropolitan = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Division"] == "Metropolitan"]
        jerseys_central = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Division"] == "Central"]
        jerseys_pacific = jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Division"] == "Pacific"]

        unique_player_countries = jersey_stat_sheet_jersey_data["Nationality"].dropna().unique().tolist()
        player_countries = []
        for country in unique_player_countries:
            player_countries.append({
                "country": country,
                "df": jersey_stat_sheet_jersey_data.loc[jersey_stat_sheet_jersey_data["Nationality"] == country]
            })
            player_countries[-1].update({"count": player_countries[-1]["df"].shape[0]})

        player_countries.sort(key=lambda d: d["count"], reverse=True)

        count_home = jerseys_home.shape[0]
        count_away = jerseys_away.shape[0]

        count_forward = jerseys_forward.shape[0]
        count_defence = jerseys_defence.shape[0]
        count_goalie = jerseys_goalie.shape[0]

        count_east = jerseys_eastern.shape[0]
        count_west = jerseys_western.shape[0]

        count_atl = jerseys_atlantic.shape[0]
        count_met = jerseys_metropolitan.shape[0]
        count_cen = jerseys_central.shape[0]
        count_pac = jerseys_pacific.shape[0]

        st.subheader("Home & Away Counts")
        home_count_0, away_count_1 = st.columns(2)
        home_count_0.metric("Home + Alternate + Reverse Retro", value=count_home)
        away_count_1.metric("Away", value=count_away)

        st.subheader("Position Counts")
        pos_count_0, pos_count_1, pos_count_2 = st.columns(3)
        pos_count_0.metric("Forward", value=count_forward)
        pos_count_1.metric("Defence", value=count_defence)
        pos_count_2.metric("Goalie", value=count_goalie)

        st.subheader("Conference Counts")
        conf_count_0, conf_count_1 = st.columns(2)
        conf_count_0.metric("Western", value=count_west)
        conf_count_1.metric("Eastern", value=count_east)

        st.subheader("Division Counts")
        div_count_0, div_count_1, div_count_2, div_count_3 = st.columns(4)
        div_count_0.metric("Pacific", value=count_pac)
        div_count_1.metric("Central", value=count_cen)
        div_count_2.metric("Metropolitan", value=count_met)
        div_count_3.metric("Atlantic", value=count_atl)

        st.subheader("Country Counts")
        country_cols = st.columns(len(player_countries))
        for c_data, col, in zip(player_countries, country_cols):
            # c_data = player_countries[country]
            count = c_data["count"]
            country = c_data["country"]
            col.metric(label=country, value=count)

        # -------------------------------------------------------------------
        # -------------------------------------------------------------------

        average_wait_days = exclusive_mean(sheet_jersey_data["WaitDays"].dropna().values.tolist(), invalid=[0])
        average_owned_days = exclusive_mean(sheet_jersey_data["OwnedDays"].dropna().values.tolist(), invalid=[45298.77416736111])

        st.subheader("Wait & Owned Days")
        wait_cols = st.columns(2)
        wait_cols[0].metric(
            label="Average Wait Days",
            value=average_wait_days
        )
        wait_cols[1].metric(
            label="Average Owned Days",
            value=average_owned_days
        )

        # -------------------------------------------------------------------
        # -------------------------------------------------------------------

        print(f"{distinct_owned_teams_homes=}")
        print(f"{distinct_owned_teams_aways=}")

        # using full datatset, not unique teams version
        sheet_jersey_data.fillna("", inplace=True)

        st.subheader("Jersey Data")
        st.dataframe(sheet_jersey_data)
        st.subheader("NHL Teams")
        st.dataframe(sheet_nhl_teams)

        # teams checklist
        exp_teams_checklist = st.expander("Jersey Team Checklist")
        sheet_nhl_teams.sort_values(by=["Conference", "Division", "FullTeamName"], inplace=True)
        shown_confs = set()
        shown_divs = set()
        for i, data in sheet_nhl_teams.iterrows():
            team_name = data["FullTeamName"]
            conf_name = data["ConferenceName"]
            div_name = data["DivisionName"]
            if conf_name not in shown_confs:
                shown_confs.add(conf_name)
                exp_teams_checklist.divider()
                exp_teams_checklist.markdown(f'{conf_name}')
                # col0.markdown(f'{conf_name}')
                exp_teams_checklist.divider()
                # col1.add_vertical_space(1)
            if div_name not in shown_divs:
                shown_divs.add(div_name)
                exp_teams_checklist.divider()
                exp_teams_checklist.markdown(f'{div_name}')
                # col0.markdown(f'{div_name}')
                exp_teams_checklist.divider()
                # col1.add_vertical_space(1)
                # col1.add_vertical_space(1)

            key_owned = f"owned_{team_name}"
            key_owned_home = f"owned_home_{team_name}"
            key_owned_away = f"owned_away_{team_name}"
            st.session_state[key_owned] = team_name in distinct_owned_teams
            st.session_state[key_owned_home] = team_name in distinct_owned_teams_homes
            st.session_state[key_owned_away] = team_name in distinct_owned_teams_aways

            jersey_data_by_team = sheet_jersey_data.loc[sheet_jersey_data["Team"] == team_name]
            if jersey_data_by_team.empty:
                owned_count = 0
            else:
                owned_count = jersey_data_by_team.shape[0]

            col0, col1, col2, col3, col4 = exp_teams_checklist.columns(5)
            col0.markdown(f"{team_name}")
            col1.markdown(f"x{owned_count}")
            col2.checkbox(
                label="Owned",
                key=key_owned,
                disabled=True
                # ,
                # label_visibility="hidden"
            )
            col3.checkbox(
                label="Home",
                key=key_owned_home,
                disabled=True
                # ,
                # label_visibility="hidden"
            )
            col4.checkbox(
                label="Away",
                key=key_owned_away,
                disabled=True
                # ,
                # label_visibility="hidden"
            )

        # timeline
        # graphable_dates = [
        #     ("Order Date", order_date),
        #     ("Receive Date", receive_date)
        # ]
        graphable_dates = [
            "Made Date",
            "Order Date",
            "Receive Date",
            "Open Date",
            "DOB"
        ]
        btn_gdate_cols = st.columns(len(graphable_dates))
        g_date_btns = []
        for lbl, col in zip(graphable_dates, btn_gdate_cols):
            g_date_btns.append(col.toggle(
                label=lbl,
                key=f"choice_g_date_{lbl.lower().replace(' ', '')}"
            ))
        n_graphable_dates = []
        for lbl, btn in zip(graphable_dates, g_date_btns):
            if st.session_state[f"choice_g_date_{lbl.lower().replace(' ', '')}"]:
                n_graphable_dates.append(lbl)
        graphable_dates.clear()
        graphable_dates = n_graphable_dates

        movements_data = []
        ii = 0
        for i, data in sheet_jersey_data.iterrows():
            team = data["Team"]
            player_last = data["PlayerLast"]
            player_first = data["PlayerFirst"]
            player = f"{player_first} {player_last}"
            if all([team, player]):
                order_date = pd.to_datetime(data["OrderDate"]).date()
                receive_date = pd.to_datetime(data["ReceiveDate"]).date()
                open_date = pd.to_datetime(data["OpenDate"]).date()
                made_date = data["MadeDate"]
                made_m, made_y = made_date.split("/") if made_date else (None, None)
                if made_m and made_y:
                    made_date = datetime.datetime.strptime(f"20{made_y}-{made_m}-01", "%Y-%m-%d")
                else:
                    made_date = None
                birth_date = pd.to_datetime(data["DOB"]).date()

                g_dates_dict = {
                    "Order Date": order_date,
                    "Receive Date": receive_date,
                    "Open Date": open_date,
                    "Made Date": made_date,
                    "DOB": birth_date
                }
                graphable_dates_d = [(k, g_dates_dict[k]) for k in graphable_dates]
                for t_typ, dat in graphable_dates_d:
                    if not pd.isnull(dat):
                        print(f"{team=}, {player=}, {t_typ=}, {dat=}, {order_date=}, {receive_date=}")
                        movements_data.append({
                            "id": ii,
                            # "content": f"{t_typ}",
                            # "text": f"{team}  -  {player}",
                            # "content": f"{team}  -  {player}",
                            "content": f"{player}  -  {team}",
                            "text": f"{t_typ}",
                            "start": dat
                        })
                        ii += 1

        print(f"{movements_data=}")

        movements_dict = {
            "title": {
                "text": {
                    "headline": "Jersey Movement Dates",
                    "text": ""
                }
            },
            "events": []
        }
        for event in movements_data:
            movements_dict["events"].append({
                "start_date": {
                    "day": event["start"].day,
                    "month": event["start"].month,
                    "year": event["start"].year
                },
                "text": {
                    "headline": event["content"],
                    "text": event["text"]
                }
            })
        # df_all_dates = sheet_jersey_data[]
        if movements_dict["events"]:
            timeline_all_data = timeline(
                movements_dict,
                height=500
            )
        else:
            st.write(f"Please choose a date to graph on the timeline first.")

        st.subheader("Jersey Inventory")
        cont_jersey_inventory = st.container()
        base_width, base_height = 300, 300
        for i, row in sheet_jersey_data.iterrows():
            player_name_first = row["PlayerFirst"]
            player_name_last = row["PlayerLast"]
            if player_name_first and player_name_last:
                player_number = row.get("Number", 0)
                player_number = int(player_number) if not isinstance(player_number, str) else 0
                player_name = f"#{player_number} {player_name_first} {player_name_last}"
                image_front = row["ImageFront"]
                image_back = row["ImageBack"]
                cont_jersey_inventory.divider()
                cont_jersey_inventory.markdown(f"{player_name}")
                if image_front and image_back:

                    image_front = Image.open(image_front).resize((base_width, base_height)).transpose(Image.ROTATE_270)
                    image_back = Image.open(image_back).resize((base_width, base_height)).transpose(Image.ROTATE_270)

                    image_cols = cont_jersey_inventory.columns(2)
                    image_cols[0].image(image_front, "front")
                    image_cols[1].image(image_back, "back")

    else:
        st.markdown(f"Must be on home computer to access the base excel file.")
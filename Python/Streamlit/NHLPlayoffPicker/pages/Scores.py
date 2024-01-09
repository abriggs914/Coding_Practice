from fractions import Fraction
from typing import Literal

import streamlit as st
import pandas as pd
import datetime
import requests
from decimal import Decimal
from fractions import Fraction


def isnumber(value):
    # if isinstance(value, int) or isinstance(value, float):
    #     return True
    # if isinstance(value, str):
    #     if value.count("-") < 2 and value.count(".") < 2:
    #         if value.replace("-", "").replace(".", "").isnumeric():
    #             return True
    # return False
    if isinstance(value, (int, float, complex, Decimal, Fraction)) or pd.api.types.is_numeric_dtype(value):
        return True
    xs = str(value)
    if xs.count(".") < 2 and xs.count("-") < 2:
        return xs.replace(".", "").removeprefix("-").isnumeric()
    return False


def number_suffix(n):
    if not isnumber(n):
        raise ValueError(f"Error cannot determine suffix for non-number input '{n}'")
    if isinstance(n, str) and n.count(".") != 0:
        raise ValueError(f"Error cannot determine suffix for non-integer input '{n}'")
    if not isinstance(n, str):
        n = str(n)
    # if len(n) < 2:
    #     n = f"0{n}"
    if n[-1] == "1":
        res = "st"
        if len(n) > 1:
            if n[-2] == "1":
                res = "th"
    elif n[-1] == "2":
        res = "nd"
        if len(n) > 1:
            if n[-2] == "1":
                res = "th"
    elif n[-1] == "3":
        res = "rd"
        if len(n) > 1:
            if n[-2] == "1":
                res = "th"
    else:
        res = "th"
    return res


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


game_state_full = {
    "REG": "Regulation",
    "OT": "Overtime",
    "SO": "Shootout",
    "FINAL": "Final",
    "OFF": "Final"
}


if __name__ == '__main__':

    print(f"\n\n\tRERUN\n\n")

    nhl_api = NHLAPIHandler()

    today = datetime.datetime.today()
    # scores_today = nhl_api.get_score(today + datetime.timedelta(days=-1))
    scores_today = nhl_api.is_game_ongoing_now(r_type="next_games")  # fetches the newest data

    # scores_today = nhl_api.get_score(today)

    print(f"{type(scores_today)=} {scores_today=}")

    df_scores_today_gameWeek = pd.DataFrame(scores_today.get("gameWeek", {}))
    df_scores_today_oddsPartners = pd.DataFrame(scores_today.get("oddsPartners", {}))
    scores_today_dict = scores_today.get("games", [])
    df_scores_today_games = pd.DataFrame(scores_today_dict)

    # keys_to_update = [
    #     ("venue", "default")
    #     # ,
    #     # ("teamName", "default"),
    #     # ("teamCommonName", "default"),
    #     # ("teamAbbrev", "default"),
    #     # ("Record", lambda row: f"{row['wins']}-{row['losses']}-{row['otLosses']}"),
    #     # ("SO", lambda row: f"{row['shootoutWins']}-{row['shootoutLosses']}"),
    #     # ("Streak", lambda row: f"{row['streakCode']}{row['streakCount']}")
    # ]
    # for i, dat in enumerate(scores_today_dict):
    #     for k, ik in keys_to_update:
    #         if k in scores_today_dict[i]:
    #             scores_today_dict[i][k] = scores_today_dict[i][k][ik]
    #         else:
    #             scores_today_dict[i][k] = ik(row=dat)
    # df_scores_today_games = pd.DataFrame(scores_today_dict)
    #
    # # df_scores_today_games["venue"] =
    #
    # st.write(df_scores_today_gameWeek)
    # st.write(df_scores_today_oddsPartners)
    st.write(df_scores_today_games)

    # game_expanders = []
    game_containers = []

    for i, game_data in enumerate(scores_today_dict):
        # keys:
        # ['id', 'season', 'gameType', 'gameDate', 'venue', 'startTimeUTC', 'easternUTCOffset', 'venueUTCOffset',
        # 'tvBroadcasts', 'gameState', 'gameScheduleState', 'awayTeam', 'homeTeam', 'gameCenterLink', 'neutralSite',
        # 'venueTimezone', 'ticketsLink', 'teamLeaders']
        # print(f"{list(game_data.keys())=}")
        # print(f"{list(game_data.values())=}")
        away_team, home_team = None, None
        venue_english = game_data["venue"]["default"]
        venue_french = game_data["venue"].get("fr", None)
        if venue_french is None:
            venue_french = venue_english
        start_time_utc = game_data["startTimeUTC"]
        start_time_east_offset = game_data["easternUTCOffset"]
        start_time_venue_offset = game_data["venueUTCOffset"]
        game_state = game_data["gameState"]
        game_schedule_state = game_data["gameScheduleState"]

        clock_team_data = game_data.get("clock", {})
        away_team_data = game_data["awayTeam"]
        home_team_data = game_data["homeTeam"]

        away_team = away_team_data.get("name", {}).get("default", "")
        home_team = home_team_data.get("name", {}).get("default", "")

        time_running = clock_team_data.get("running", False)
        in_intermission = clock_team_data.get("inIntermission", False)
        time_remaining = clock_team_data.get("timeRemaining", "20:00")
        seconds_remaining = clock_team_data.get("secondsRemaining", 0)
        away_score = away_team_data.get("score", 0)
        home_score = home_team_data.get("score", 0)
        away_sog = away_team_data.get("sog", 0)
        home_sog = home_team_data.get("sog", 0)

        time_period = game_data.get("period", 1)
        period_descriptor = game_data.get("periodDescriptor", {})  # dict
        period_number = period_descriptor.get("number", 1)  # period as number
        period_type = period_descriptor.get("periodType", "REG")  # REG / OT / SO
        game_centre_link = game_data["gameCenterLink"]  # str of link
        neutral_site = game_data["neutralSite"]  # bool if neutral site
        venue_time_zone = game_data["venueTimezone"]
        tickets_link = game_data.get("ticketsLink", "")

        game_goals = game_data.get("goals", [])
        team_leader_data = game_data.get("teamLeaders", {})
        # print(f"{venue_english=}")

        elements = {}

        # start time and location
        east_off_splt = start_time_east_offset.split(":")
        h_off, m_off = int(east_off_splt[0].strip()) + 1, int(east_off_splt[1].strip())
        start_time_utc = datetime.datetime.fromisoformat(start_time_utc) + datetime.timedelta(hours=h_off,
                                                                                              minutes=m_off)

        fmt = "%Y-%m-%d %H:%M"
        message_future = f"{start_time_utc:{fmt}}  -  {venue_english}"
        message_live_action = f"{time_remaining} {period_number}{number_suffix(period_number)}  -  {venue_english}"
        message_live_intermission = f"{period_number} INT  -  {venue_english}"
        message_pregame = f"PRE-GAME  -  {start_time_utc:{fmt}}  -  {venue_english}"

        status_away, status_home = "", ""
        game_message = ""
        if game_state in ("FINAL", "OFF"):
            status_away, status_home = ("W ", " L") if away_score > home_score else ("L ", " W")
            game_message = f"{game_state_full[game_state]}"
        elif game_state == "FUT":
            game_message = message_future
        elif game_state == "LIVE":
            if seconds_remaining > 0:
                game_message = message_live_action
            else:
                if in_intermission:
                    game_message = message_live_intermission
        elif game_state == "PRE":
            game_message = message_pregame

        st.divider()
        exp_game = st.container()
        game_containers.append(exp_game)
        # f"{status_away}{away_team} {away_score} @ {home_score} {home_team} {status_home}  |  {game_message}"

        container_top = exp_game.container()

        # teams data
        teams = {"away": {}, "home": {}}
        for k, dat in teams.items():
            dat["logo_cols"] = tuple()
        for k, td in zip(teams.keys(), [away_team_data, home_team_data]):
            if k == "away":
                away_team = td["abbrev"]
            elif k == "home":
                home_team = td["abbrev"]
            teams[k]["id"] = td.get("id")
            teams[k]["name_english"] = td["name"].get("default")
            teams[k]["name_french"] = td["name"].get("fr", None)
            if teams[k]["name_french"] is None:
                teams[k]["name_french"] = teams[k]["name_english"]
            teams[k]["name_abbrev"] = td["abbrev"]
            teams[k]["record"] = td.get("record", "-")
            teams[k]["logo"] = td["logo"]

        print(f"{away_team=}")
        print(f"{home_team=}")

        # team_img_cols = st.columns([0.38, 0.24, 0.38])
        team_img_cols = exp_game.columns([0.3, 0.1, 0.2, 0.1, 0.3])
        team_expander_cols = exp_game.columns(2)
        # team_expanders = [col.expander("Details") for col in team_expander_cols]
        team_expanders = [col.container() for col in team_expander_cols]
        # for te in team_expanders:
        #     te.markdown(f"#### Details")
        # elements[f"{i}_team_img_cols"] = (
        col_away_logo = team_img_cols[0]
        col_away_score = team_img_cols[1]
        col_home_score = team_img_cols[-2]
        col_home_logo = team_img_cols[-1]
        col_away_logo.image(teams["away"]["logo"], teams["away"]["name_abbrev"])  # ,
        team_img_cols[len(team_img_cols) // 2].write(f"@")  # ,
        col_home_logo.image(teams["home"]["logo"], teams["home"]["name_abbrev"])
        # )
        # elements[f"{i}_team_img_cols"][0].write(f"{teams['away']['record']}")
        # elements[f"{i}_team_img_cols"][2].write(f"{teams['home']['record']}")
        if game_state != "LIVE":
            col_away_logo.write(f"{teams['away']['record']}")
            col_home_logo.write(f"{teams['home']['record']}")

        if game_state not in ("FUT", "PRE"):
            col_away_score.markdown(f"### {away_score}")
            col_home_score.markdown(f"### {home_score}")

        # players data
        # elements[f"{i}_exp_cols_columns"] = st.columns(2)
        # elements[f"{i}_exp_cols_expanders"] = (
        #     elements[f"{i}_exp_cols_columns"][0].expander(teams["away"]["name_abbrev"]),
        #     elements[f"{i}_exp_cols_columns"][1].expander(teams["home"]["name_abbrev"])
        # )

        cols_team_details = exp_game.columns(2)

        print(f"{game_state=}, {in_intermission=}, {time_remaining=}, {period_number=}, {seconds_remaining=}")

        if game_state == "LIVE":

            if seconds_remaining > 0:
                container_top.markdown(message_live_action)
            else:
                if in_intermission:
                    container_top.markdown(message_live_intermission)
                # else:

            det_col_0, det_col_1 = cols_team_details
            # det_col_0.markdown(f"#### {scores_today}")

        if game_state == "PRE":
            container_top.markdown(message_pregame)
            # else:

            det_col_0, det_col_1 = cols_team_details
            # det_col_0.markdown(f"#### {scores_today}")

        if game_state in ("FINAL", "OFF"):

            # if seconds_remaining > 0:
            #     container_top.markdown(f"{time_remaining} {period_number} - {venue_english}")
            # else:
            #     if in_intermission:
            container_top.markdown(f"FINAL  -  {venue_english}")
            # else:

            det_col_0, det_col_1 = cols_team_details
            # det_col_0.markdown(f"#### {scores_today}")

        elif game_state == "FUT":

            container_top.markdown(message_future)

            # elements[f"{i}_exp_cols_expanders"] = (
            #     cols_team_details[0].expander(f"{teams['away']['name_abbrev']} Leaders"),
            #     cols_team_details[1].expander(f"{teams['home']['name_abbrev']} Leaders")
            # )

            # elements[f"{i}_exp_cols_expanders"] = (
            #     cols_team_details[0].container(),
            #     cols_team_details[1].container()
            # )
            elements[f"{i}_exp_cols_expanders"] = [
                cols_team_details[0].expander(f"### {teams['away']['name_abbrev']} Leaders"),
                cols_team_details[1].expander(f"### {teams['home']['name_abbrev']} Leaders")
            ]

            # away_leaders = [l for l in team_leader_data if l["teamAbbrev"] in away_team]
            # home_leaders = [l for l in team_leader_data if l["teamAbbrev"] in home_team]

            # # ensure that the team_leader_data is sorted away then home
            # l_t1 = team_leader_data[0]
            # l_t2 = team_leader_data[1]
            # print(f"{team_leader_data=}\n{l_t1}\n{l_t2}")
            # if l_t1[0]["playerTeam"] != teams["away"]["name_abbrev"]:
            #     team_leader_data = (l_t2, l_t1)

            players = {"away": {}, "home": {}}
            # for j, k_pd in enumerate(zip(players, team_leader_data)):
            for j, pd in enumerate(team_leader_data):
                # k, pd = k_pd
                # k = ""
                k = "away" if pd["teamAbbrev"] == away_team else "home"
                print(f"{i=}, {j=}, {k=}, {pd=}")
                if j not in players[k]:
                    players[k][j] = {}
                players[k][j]["id"] = pd["id"]
                players[k][j]["name_english"] = pd["name"].get("default")
                players[k][j]["name_french"] = pd["name"].get("fr", None)
                if players[k][j]["name_french"] is None:
                    players[k][j]["name_french"] = players[k][j]["name_english"]
                players[k][j]["headshot"] = pd["headshot"]
                players[k][j]["playerTeam"] = pd["teamAbbrev"]
                players[k][j]["category"] = pd["category"]
                players[k][j]["value"] = pd["value"]

                print(
                    f"{i=}, {j=}, {k=}, t={teams[k]['name_abbrev']}, pt={players[k][j]['playerTeam']}, c={players[k][j]['category']}, p={players[k][j]['name_english']}")

            print(f"{list(players)=}, {players=}")

            # exp1, exp2 = elements[f"{}_exp_cols_expanders"]
            # exp1.image(teams["away"]["logo"], teams["away"]["name_abbrev"])
            # exp2.image(teams["home"]["logo"], teams["home"]["name_abbrev"])
            for j, k_pd in enumerate(players.items()):
                key, pd = k_pd
                exp = elements[f"{i}_exp_cols_expanders"][j]
                print(f"{i=}\n{j=}\n{key=}\n{pd=}")
                # for k, pdd in enumerate(pd):
                for k, pdd in pd.items():
                    name = pdd["name_english"]
                    team = pdd["playerTeam"]
                    headshot = pdd["headshot"]
                    category = pdd["category"]
                    value = pdd["value"]

                    exp.write(
                        f"{value} {category}{'s' if ((int(value) != 0) and (not category.endswith('s'))) else ''}")
                    exp.image(headshot, name)
                    exp.write(f"{name}")

        # if game_state in ("LIVE", "FINAL", "OFF"):
        #     exp_away_dets, exp_home_dets = team_expanders
        #     if not game_goals:
        #         exp_away_dets.markdown(f"### No goals yet")
        #         exp_home_dets.markdown(f"### No goals yet")
        #     else:
        #         away_goals = [g for g in game_goals if g["teamAbbrev"] == away_team]
        #         home_goals = [g for g in game_goals if g["teamAbbrev"] == home_team]
        #         # away_p1 = [g for g in away_goals if g.get("periodDescriptor", {}).get("number", -1) == 1 and g.get("periodDescriptor", {}).get("periodType", "") == "REG"]
        #         # away_p2 = [g for g in away_goals if g.get("periodDescriptor", {}).get("number", -1) == 2 and g.get("periodDescriptor", {}).get("periodType", "") == "REG"]
        #         # away_p3 = [g for g in away_goals if g.get("periodDescriptor", {}).get("number", -1) == 3 and g.get("periodDescriptor", {}).get("periodType", "") == "REG"]
        #         #
        #         # home_p1 = [g for g in home_goals if g.get("periodDescriptor", {}).get("number", -1) == 1 and g.get("periodDescriptor", {}).get("periodType", "") == "REG"]
        #         # home_p2 = [g for g in home_goals if g.get("periodDescriptor", {}).get("number", -1) == 2 and g.get("periodDescriptor", {}).get("periodType", "") == "REG"]
        #         # home_p3 = [g for g in home_goals if g.get("periodDescriptor", {}).get("number", -1) == 3 and g.get("periodDescriptor", {}).get("periodType", "") == "REG"]
        #
        #         print(f"LEN=={len(away_goals)}, {away_goals=}\nLEN=={len(home_goals)}, {home_goals=}")
        #         s_a, s_h = 0, 0
        #         for exp, goals_data, key in zip(team_expanders, (away_goals, home_goals), ("away", "home")):
        #             b_type, b_pn = False, False
        #             print(f"{i=}, {key=}, {home_team}_{away_team}, {s_a=}, {s_h=}, {b_pn=}, {b_type=}, len={len(goals_data)}, {goals_data=}")
        #             if not b_type:
        #                 for pt in ["REG", "OT", "SO"]:
        #                     if (pt != "REG") and (s_a != s_h):
        #                         break
        #                     shown_ptl = False
        #                     ptl = game_state_full[pt]
        #                     # if not shown_ptl:
        #                     exp.divider()
        #                     exp.markdown(f"# {ptl}")
        #                     # shown_ptl = True
        #                     for pn in range(1, (3 if pt == "REG" else 12) + 1):
        #                         shown_period = False
        #                         for goal_data in goals_data:
        #                             if not b_pn:
        #                                 pd = goal_data.get("periodDescriptor", {})
        #                                 if pd.get("number", -1) == pn and pd.get("periodType", "") == pt:
        #                                     s_a += 1 if key == "away" else 0
        #                                     s_h += 1 if key == "home" else 0
        #                                     if not shown_period:
        #                                         exp.divider()
        #                                         exp.markdown(f"### {pn}{number_suffix(pn)} Period")
        #                                         shown_period = True
        #                                     exp.markdown(f"#### GOAL! A={s_a} {s_h}=H")
        #
        #                             if s_a != s_h:
        #                                 # score is not tied
        #                                 if pn > 3:
        #                                     # regulation ended
        #                                     b_pn = True
        #                                     b_type = True
        #
        #                             if not shown_period:
        #                                 exp.divider()
        #                                 exp.markdown(f"### {pn}{number_suffix(pn)} Period")
        #                                 shown_period = True
        #
        #                             if b_pn:
        #                                 break
        #
        #                     # exp.divider()
        #
        #                     # if not shown_ptl:
        #                     #     exp.divider()
        #                     #     exp.markdown(f"# {ptl}")
        #                     #     shown_ptl = True
        #
        #                     if b_type:
        #                         break


    # for k,

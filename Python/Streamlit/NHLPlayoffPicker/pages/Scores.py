import streamlit as st
import pandas as pd
import datetime
import requests


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

    print(f"\n\n\tRERUN\n\n")

    nhl_api = NHLAPIHandler()

    today = datetime.datetime.today()
    scores_today = nhl_api.get_score(today)

    # print(f"{type(scores_today)=} {scores_today=}")

    df_scores_today_gameWeek = pd.DataFrame(scores_today["gameWeek"])
    df_scores_today_oddsPartners = pd.DataFrame(scores_today["oddsPartners"])
    scores_today_dict = scores_today["games"]
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

    for i, game_data in enumerate(scores_today_dict):
        # keys:
        # ['id', 'season', 'gameType', 'gameDate', 'venue', 'startTimeUTC', 'easternUTCOffset', 'venueUTCOffset',
        # 'tvBroadcasts', 'gameState', 'gameScheduleState', 'awayTeam', 'homeTeam', 'gameCenterLink', 'neutralSite',
        # 'venueTimezone', 'ticketsLink', 'teamLeaders']
        # print(f"{list(game_data.keys())=}")
        # print(f"{list(game_data.values())=}")
        venue_english = game_data["venue"]["default"]
        venue_french = game_data["venue"].get("fr", None)
        if venue_french is None:
            venue_french = venue_english
        start_time_utc = game_data["startTimeUTC"]
        start_time_east_offset = game_data["easternUTCOffset"]
        start_time_venue_offset = game_data["venueUTCOffset"]
        game_state = game_data["gameState"]
        game_schedule_state = game_data["gameScheduleState"]
        away_team_data = game_data["awayTeam"]
        home_team_data = game_data["homeTeam"]
        game_centre_link = game_data["gameCenterLink"]
        neutral_site = game_data["neutralSite"]
        venue_time_zone = game_data["venueTimezone"]
        tickets_link = game_data["ticketsLink"]
        team_leader_data = game_data["teamLeaders"]
        # print(f"{venue_english=}")

        elements = {}

        # start time and location
        east_off_splt = start_time_east_offset.split(":")
        h_off, m_off = int(east_off_splt[0].strip()) + 1, int(east_off_splt[1].strip())
        start_time_utc = datetime.datetime.fromisoformat(start_time_utc) + datetime.timedelta(hours=h_off, minutes=m_off)
        fmt = "%Y-%m-%d %H:%M"
        st.markdown(f"{start_time_utc:{fmt}} - {venue_english}")

        # teams data
        teams = {"away": {}, "home": {}}
        away_team, home_team = None, None
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
            teams[k]["record"] = td["record"]
            teams[k]["logo"] = td["logo"]

        print(f"{away_team=}")
        print(f"{home_team=}")

        team_img_cols = st.columns([0.38, 0.24, 0.38])
        # elements[f"{i}_team_img_cols"] = (
        team_img_cols[0].image(teams["away"]["logo"], teams["away"]["name_abbrev"]) #,
        team_img_cols[1].write(f"@") #,
        team_img_cols[2].image(teams["home"]["logo"], teams["home"]["name_abbrev"])
        # )
        # elements[f"{i}_team_img_cols"][0].write(f"{teams['away']['record']}")
        # elements[f"{i}_team_img_cols"][2].write(f"{teams['home']['record']}")
        team_img_cols[0].write(f"{teams['away']['record']}")
        team_img_cols[2].write(f"{teams['home']['record']}")

        # players data
        # elements[f"{i}_exp_cols_columns"] = st.columns(2)
        # elements[f"{i}_exp_cols_expanders"] = (
        #     elements[f"{i}_exp_cols_columns"][0].expander(teams["away"]["name_abbrev"]),
        #     elements[f"{i}_exp_cols_columns"][1].expander(teams["home"]["name_abbrev"])
        # )

        cols_player = st.columns(2)
        elements[f"{i}_exp_cols_expanders"] = (
            cols_player[0].expander(f"{teams['away']['name_abbrev']} Leaders"),
            cols_player[1].expander(f"{teams['home']['name_abbrev']} Leaders")
        )

        away_leaders = [l for l in team_leader_data if l["teamAbbrev"] in away_team]
        home_leaders = [l for l in team_leader_data if l["teamAbbrev"] in home_team]

        # # ensure that the team_leader_data is sorted away then home
        # l_t1 = team_leader_data[0]
        # l_t2 = team_leader_data[1]
        # print(f"{team_leader_data=}\n{l_t1}\n{l_t2}")
        # if l_t1[0]["playerTeam"] != teams["away"]["name_abbrev"]:
        #     team_leader_data = (l_t2, l_t1)

        players = {"away": {}, "home": {}}
        for j, k_pd in enumerate(zip(players.keys(), team_leader_data)):
            k, pd = k_pd
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

            print(f"{i=}, {j=}, {k=}, t={teams[k]['name_abbrev']}, pt={players[k][j]['playerTeam']}, c={players[k][j]['category']}, p={players[k][j]['name_english']}")

        print(f"{list(players)=}, {players=}")

        # exp1, exp2 = elements[f"{}_exp_cols_expanders"]
        # exp1.image(teams["away"]["logo"], teams["away"]["name_abbrev"])
        # exp2.image(teams["home"]["logo"], teams["home"]["name_abbrev"])
        for j, k_pd in enumerate(players.items()):
            key, pd = k_pd
            exp = elements[f"{i}_exp_cols_expanders"][j]
            print(f"{i=}, {j=}, {key=}, {pd=}")
            for k, pdd in enumerate(pd):
                name = pdd[j]["name_english"]
                team = pdd[j]["playerTeam"]
                headshot = pdd[j]["headshot"]
                category = pdd[j]["category"]
                value = pdd[j]["value"]

                exp.write(f"{value} {category}{'s' if ((int(value) != 0) and (not category.endswith('s'))) else ''}")
                exp.image(headshot, name)
                exp.write(f"{name}")

    # for k,

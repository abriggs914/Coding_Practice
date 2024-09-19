import copy
import datetime
import json
import os

import requests
import streamlit as st
from json_utility import jsonify

TEST_GAMES = [
    # 2024010001
]


# https://github.com/Zmalski/NHL-API-Reference?tab=readme-ov-file
# https://api-web.nhle.com/v1/gamecenter/2023020121/landing

if TEST_GAMES:
    print(f"\n\nJerseys Start!")
    sst = sorted(((k, v) for k, v in st.session_state.items()), key=lambda tup: str(tup[1]))
    for i, k_v in enumerate(sst):
        k, v = k_v
        if (k.removeprefix("v_") in map(str, TEST_GAMES)) or (k.removeprefix("v_").split("_")[0] in map(str, TEST_GAMES)):
            print(f"\tS {i=}, {k=}, {v=}")


columns = {
    "top row": st.columns(1),
    "top arrows": st.columns(3, gap="large"),
    "top_sub_row": st.columns(2, gap="large"),
    "games_data": st.columns(1)
}


for k, v in (
        ("gm_date_prev", datetime.datetime.now() + datetime.timedelta(days=-1)),
        ("gm_date_today", datetime.datetime.now()),
        ("gm_date_next", datetime.datetime.now() + datetime.timedelta(days=1)),
        ("gm_lbl_date_prev", datetime.datetime.now() + datetime.timedelta(days=-1)),
        ("gm_lbl_date_today", datetime.datetime.now()),
        ("gm_lbl_date_next", datetime.datetime.now() + datetime.timedelta(days=1))
):
    if k not in st.session_state:
        st.session_state.setdefault(k, v)


dict_team_abbrev_to_id = dict()
dict_id_to_team_abbrev = dict()


def load_games_history():
    in_f = r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\streamlit_demo\game_results.json"
    if not os.path.exists(in_f):
        in_f = r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\streamlit_demo\game_results.json"
    with open(in_f, "r") as f:
        data = json.load(f)
    return data


@st.cache_data
def load_games_history_start_up():
    return load_games_history()


def click_reload_games_history():
    print(f"click_reload_games_history")
    global data_games_history
    data_games_history = load_games_history()


def click_save_games_history():
    n = datetime.datetime.now()
    # out_f = r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\streamlit_demo\game_results_{date}.json"
    # out_f = out_f.format(date=f"{n:%Y%d%m_%H%M}")
    out_f = r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\streamlit_demo\game_results.json"
    data_games_history.update({"lastUpdated": n})
    print(f"SAVE {jsonify(data_games_history, in_line=False)}")
    dgh = {k: v for k, v in data_games_history["games"].items() if v.get("myChoice", True) is not None}
    print(f"SAVE {dgh=}")
    with open(out_f, "w") as f:
        f.write(jsonify(data_games_history, in_line=False))


@st.cache_data(show_spinner=False)
def get_game_data(date: datetime.datetime):
    url = f"https://api-web.nhle.com/v1/schedule/{date:%Y-%m-%d}"
    try:
        json_data = requests.get(url).json()
    except requests.exceptions.CompatJSONDecodeError as reCJSONDE:
        json_data = {}
        print(f"{reCJSONDE=}")
    return json_data


def set_gm_dates(y, n, t):
    st.session_state["gm_date_prev"] = y
    st.session_state["gm_date_today"] = n
    st.session_state["gm_date_next"] = t
    st.session_state["gm_lbl_date_prev"] = y
    st.session_state["gm_lbl_date_today"] = n
    st.session_state["gm_lbl_date_next"] = t


def click_prev_date():
    print(f"click_prev_date {st.session_state.gm_date_today:%Y-%m-%d}")
    n = st.session_state.gm_date_prev
    y = n + datetime.timedelta(days=-1)
    t = st.session_state.gm_date_today
    set_gm_dates(y, n, t)


def click_next_date():
    print(f"click_next_date {st.session_state.gm_date_today:%Y-%m-%d}")
    n = st.session_state.gm_date_next
    y = st.session_state.gm_date_today
    t = n + datetime.timedelta(days=1)
    set_gm_dates(y, n, t)


def click_goto_today():
    n = datetime.datetime.now()
    print(f"click_goto_today {n:%Y-%m-%d}")
    y = n + datetime.timedelta(days=-1)
    t = n + datetime.timedelta(days=1)
    set_gm_dates(y, n, t)


def click_choice_locked(game: int, key: str):
    locked = st.session_state[key]
    v = datetime.datetime.now() if locked else None
    print(f"CHXLCK {v=}, {locked=}, {game=}, {key=}")
    st.session_state[f"v_{key}"] = locked
    st.session_state[f"v_{key}_date"] = datetime.datetime.now() if locked else None
    data_games_history["games"][str(game)].update({
        "myChoiceLocked": locked,
        "myChoiceLockDate": datetime.datetime.now() if locked else None
    })


def click_choice(game: int, key: str):
    v = st.session_state[key]
    print(f"CHX {v=}, {game=}, {key=}")
    t_id = dict_team_abbrev_to_id[v]
    st.session_state[f"v_{key}"] = t_id
    st.session_state[f"v_{key}_date"] = datetime.datetime.now()
    data_games_history["games"][str(game)].update({
        "myChoice": t_id,
        "myChoiceDate": datetime.datetime.now()
    })
    for gk, gkv in data_games_history["games"].items():
        if gk.strip("_")[0] in map(str, TEST_GAMES):
            print(f"{gk=}, {gkv=}")

data_games_history = load_games_history_start_up()
data_games_history_og = copy.deepcopy(data_games_history)
print(f"{data_games_history=}")


with columns["top arrows"][0]:
    btn_prev_date = st.button(
        label=f"{st.session_state.gm_lbl_date_prev:%Y-%m-%d}",
        on_click=click_prev_date,
        key="btn_prev_date"
    )


with columns["top arrows"][1]:
    st.write(
        f"{st.session_state.gm_date_today:%Y-%m-%d}"
    )


with columns["top arrows"][2]:
    btn_next_date = st.button(
        label=f"{st.session_state.gm_lbl_date_next:%Y-%m-%d}",
        on_click=click_next_date,
        key="btn_next_date"
    )


with columns["top_sub_row"][1]:
    btn_goto_today = st.button(
        label=f"Today {datetime.datetime.now():%Y-%m-%d}",
        on_click=click_goto_today,
        key="btn_goto_today"
    )

now = datetime.datetime.now()


with columns["games_data"][0]:
    y = st.session_state.gm_date_prev.date()
    n = st.session_state.gm_date_today.date()
    t = st.session_state.gm_date_next.date()
    data_today = get_game_data(n)

    print(f"{n=}")

    if data_today:
        next_start_date = data_today.get("nextStartDate")
        prev_start_date = data_today.get("previousStartDate")
        game_week = data_today.get("gameWeek", list())
        odds_partners = data_today.get("oddsPartners", list())
        pre_season_start_date = data_today.get("preSeasonStartDate")
        reg_season_start_date = data_today.get("regularSeasonStartDate")
        reg_season_end_date = data_today.get("regularSeasonEndDate")
        playoff_end_date = data_today.get("playoffEndDate")
        number_of_games = data_today.get("numberOfGames", 0)

        for i, game_week_data in enumerate(game_week):
            do_show = True
            game_date = datetime.datetime.strptime(game_week_data.get("date"), "%Y-%m-%d").date()
            if game_date != n:
                # print(f"skip {game_date=}")
                do_show = False
                # continue
            # else:
            #     print(f"show {game_date=}")

            game_day_abbrev = game_week_data.get("dayAbbrev")
            game_day_number_of_games = game_week_data.get("numberOfGames")
            game_day_games = game_week_data.get("games", list())

            if do_show and not game_day_games:
                st.write(f"No games scheduled on {game_date:%Y-%m-%d}")
                continue

            for j, game_data in enumerate(game_day_games):
                if do_show:
                    st.divider()
                    cols_team_vs = st.columns(4)
                    exp = st.expander("Game Data")
                game_id = game_data.get("id")
                game_season = game_data.get("season")
                game_type = game_data.get("gameType")
                game_venue_default = game_data.get("venue", dict()).get("default")
                game_venue_cs = game_data.get("venue", dict()).get("cs")
                game_venue_es = game_data.get("venue", dict()).get("es")
                game_venue_fi = game_data.get("venue", dict()).get("fi")
                game_venue_sk = game_data.get("venue", dict()).get("sk")

                game_neutral_site = game_data.get("neutralSite", False)
                game_start_time_utc = game_data.get("startTimeUTC")
                game_eastern_utc_offset = game_data.get("easternUTCOffset")
                game_venue_utc_offset = game_data.get("venueUTCOffset")
                game_start_time = datetime.datetime.strptime(game_start_time_utc, "%Y-%m-%dT%H:%M:%SZ")
                game_venue_timezone = game_data.get("venueTimezone")
                game_state = game_data.get("gameState")
                game_schedule_state = game_data.get("gameScheduleState")

                game_tv_broadcasts = game_data.get("tvBroadcasts", list())

                away_team_data = game_data.get("awayTeam", dict())
                away_team_id = away_team_data.get("id")
                away_team_place_name = away_team_data.get("placeName", dict()).get("default", "")
                away_team_place_name_fr = away_team_data.get("placeName", dict()).get("fr", "")
                away_team_place_name_w_prep = away_team_data.get("placeNameWithPreposition", dict()).get("default", "")
                away_team_place_name_w_prep_fr = away_team_data.get("placeNameWithPreposition", dict()).get("fr", "")
                away_team_abbrev = away_team_data.get("abbrev", "")
                away_team_logo = away_team_data.get("logo", "")
                away_team_dark_logo = away_team_data.get("darkLogo", "")
                away_team_split_squad = away_team_data.get("awaySplitSquad", False)
                away_team_radio_link = away_team_data.get("radioLink", "")
                away_team_odds = away_team_data.get("odds", list())

                home_team_data = game_data.get("homeTeam", dict())
                home_team_id = home_team_data.get("id")
                home_team_place_name = home_team_data.get("placeName", dict()).get("default", "")
                home_team_place_name_fr = home_team_data.get("placeName", dict()).get("fr", "")
                home_team_place_name_w_prep = home_team_data.get("placeNameWithPreposition", dict()).get("default", "")
                home_team_place_name_w_prep_fr = home_team_data.get("placeNameWithPreposition", dict()).get("fr", "")
                home_team_abbrev = home_team_data.get("abbrev", "")
                home_team_logo = home_team_data.get("logo", "")
                home_team_dark_logo = home_team_data.get("darkLogo", "")
                home_team_split_squad = home_team_data.get("homeSplitSquad", False)
                home_team_radio_link = home_team_data.get("radioLink", "")
                home_team_odds = home_team_data.get("odds", list())

                game_period_descriptor_data = game_data.get("periodDescriptor", dict())
                game_period_number = game_period_descriptor_data.get("number", 1)
                game_period_type = game_period_descriptor_data.get("periodType", "REG")
                game_max_reg_periods = game_period_descriptor_data.get("maxRegulationPeriods", 3)

                game_outcome_data = game_data.get("gameOutcome", dict())
                game_outcome_last_period = game_outcome_data.get("lastPeriodType", "")

                game_special_data = game_data.get("specialEvent", dict())
                game_special_name = game_special_data.get("default")
                game_special_name_fr = game_special_data.get("fr")
                game_special_event_logo = game_data.get("specialEventLogo")
                game_tickets_link = game_data.get("ticketsLink")
                game_tickets_link_fr = game_data.get("ticketsLinkFr")
                game_center_link = game_data.get("gameCenterLink")

                if home_team_abbrev not in dict_team_abbrev_to_id:
                    dict_team_abbrev_to_id[home_team_abbrev] = home_team_id
                if away_team_abbrev not in dict_team_abbrev_to_id:
                    dict_team_abbrev_to_id[away_team_abbrev] = away_team_id
                if home_team_id not in dict_id_to_team_abbrev:
                    dict_id_to_team_abbrev[home_team_id] = home_team_abbrev
                if away_team_id not in dict_id_to_team_abbrev:
                    dict_id_to_team_abbrev[away_team_id] = away_team_abbrev

                sgid = str(game_id)
                # my_choice_locked = game_start_time <= now
                k_chx_correct = f"{sgid}_choice_correct"
                k_chx_lock_d = f"{sgid}_choice_locked_date"
                k_chx_lock = f"{sgid}_choice_locked"
                k_chx_d = f"{sgid}_choice_date"
                k_chx = f"{sgid}_choice"
                vals = dict()
                ss_dgh = {
                    k_chx: "myChoice",
                    k_chx_d: "myChoiceDate",
                    k_chx_lock: "myChoiceLocked",
                    k_chx_lock_d: "myChoiceLockDate",
                    k_chx_correct: "myChoiceCorrect"
                }
                funcs = {
                    k_chx: lambda team_id: dict_id_to_team_abbrev[team_id]
                }
                if sgid not in data_games_history["games"]:
                    data_games_history["games"][sgid] = {
                        "homeTeam": home_team_id,
                        "awayTeam": away_team_id,
                        "date": f"{game_date:%Y-%m-%d}",
                        "gameState": game_state,
                        "gameType": game_type,
                        "myChoice": None,
                        "myChoiceDate": None,
                        "myChoiceLocked": False,
                        "myChoiceLockDate": None,
                        "myChoiceCorrect": False
                    }
                    vals[k_chx] = None
                    vals[k_chx_d] = None
                    vals[k_chx_lock] = False
                    vals[k_chx_lock_d] = game_start_time <= now
                    vals[k_chx_correct] = False
                else:
                    vals[k_chx] = data_games_history["games"][sgid].get("myChoice")
                    vals[k_chx_d] = data_games_history["games"][sgid].get("myChoiceDate")
                    vals[k_chx_lock] = data_games_history["games"][sgid].get("myChoiceLocked", game_start_time <= now)
                    vals[k_chx_lock_d] = data_games_history["games"][sgid].get("myChoiceLockDate")
                    vals[k_chx_correct] = data_games_history["games"][sgid].get("myChoiceCorrect")

                my_choice_lock_disabled = game_start_time <= now
                if my_choice_lock_disabled:
                    vals[k_chx_lock] = True

                if vals[k_chx] is None:
                    my_choice_date = None
                else:
                    if vals[k_chx_d] is None:
                        my_choice_date = datetime.datetime.now()
                        vals[k_chx_d] = my_choice_date
                    else:
                        my_choice_date = vals[k_chx_d]

                # print(f"{sgid} {home_team_abbrev}, {away_team_abbrev}, {my_choice}, {my_choice_date}")

                for ss_key, dgh_key in ss_dgh.items():
                    func = funcs.get(ss_key)
                    # if ss_key not in st.session_state:
                    if st.session_state.get(ss_key) is None:
                        st.session_state[ss_key] = vals[ss_key]
                        print(f"NEW {ss_key=}, {vals[ss_key]=}")
                    else:
                        if f"v_{ss_key}" in st.session_state:
                            if func is not None and callable(func):
                                print(f"CALLABLE: {ss_key=}")
                                vals[ss_key] = func(st.session_state[f"v_{ss_key}"])
                            else:
                                print(f"NOT CALL: {ss_key=}")
                                vals[ss_key] = st.session_state[f"v_{ss_key}"]
                            print(f"RECOVER {ss_key=}, {dgh_key=}, {vals[ss_key]=}")
                            # st.session_state["myChoiceDate"] = my_choice_locked
                            data_games_history["games"][sgid][dgh_key] = vals[ss_key]
                        else:
                            print(f"FTR\t{ss_key=}, {dgh_key=}")

                print(f"{ss_dgh=}")

                my_choice = vals[k_chx]
                my_choice_d = vals[k_chx_d]
                my_choice_locked = vals[k_chx_lock]
                my_choice_locked_d = vals[k_chx_lock_d]

                game_is_over = bool(game_outcome_data)

                for key in vals:
                    st.session_state[key] = vals[key]

                print(f"{sgid=}, {vals=}, {home_team_abbrev=}, {away_team_abbrev=}, {my_choice=}, {my_choice_date=}")

                if do_show:
                    with cols_team_vs[0]:
                        if away_team_logo:
                            st.image(
                                away_team_logo,
                                caption=away_team_abbrev,
                                width=80
                            )
                        else:
                            st.write(f"could not load image for {away_team_abbrev}")
                    with cols_team_vs[1]:
                        st.write(f"@")
                    with cols_team_vs[2]:
                        if home_team_logo:
                            st.image(
                                home_team_logo,
                                caption=home_team_abbrev,
                                width=80
                            )
                        else:
                            st.write(f"could not load image for {home_team_abbrev}")
                    with cols_team_vs[3]:
                        print(f"{k_chx_lock=}, {k_chx=}, {my_choice_lock_disabled=}")
                        print(f"{st.session_state.get(k_chx_lock)=}, {st.session_state.get(k_chx)=}, {my_choice_lock_disabled=}")
                        st.toggle(
                            label="Choice Locked",
                            key=k_chx_lock,
                            disabled=my_choice_lock_disabled,
                            on_change=lambda g_=game_id, kcl=k_chx_lock: click_choice_locked(g_, kcl)
                        )
                        st.radio(
                            label="Choice",
                            options=[
                                away_team_abbrev,
                                home_team_abbrev
                            ],
                            key=k_chx,
                            disabled=my_choice_lock_disabled or my_choice_locked,
                            on_change=lambda g_=game_id, kc=k_chx: click_choice(g_, kc)
                        )
                        # # st.write(f"")
                        # if game_is_over:

                    if game_neutral_site:
                        cols_site_info = st.columns(2)
                        with cols_site_info[1]:
                            st.write(f"Neutral site: {game_venue_default}")


st.divider()


with st.columns(4)[-1]:
    st.button(
        label="Reload Games History",
        on_click=click_reload_games_history
    )


with st.columns(4)[-1]:
    st.button(
        label="Save Games History",
        on_click=click_save_games_history
    )


with columns["top row"][0]:
    st.checkbox(
        label="Unsaved Work:",
        value=data_games_history != data_games_history_og,
        disabled=True,
        key="checkbox_unsaved_work"
    )


if TEST_GAMES:
    print(f"JERSEYS END!")
    sst = sorted(((k, v) for k, v in st.session_state.items()), key=lambda tup: str(tup[1]))
    for i, k_v in enumerate(sst):
        k, v = k_v
        # if k.removeprefix("v_") in map(str, TEST_GAMES):
        if (k.removeprefix("v_") in map(str, TEST_GAMES)) or (k.removeprefix("v_").split("_")[0] in map(str, TEST_GAMES)):
            print(f"\tE {i=}, {k=}, {v=}")
    print(f"\n\n")
import asyncio
import datetime
import random

import requests
from PIL import Image
from streamlit_extras.card import card
import streamlit as st
import pandas as pd

from utility import number_suffix


# @st.cache_data
def query_player(pid: int) -> str:
    if not len(str(pid)) == 7:
        raise ValueError(f"param 'pid' must be an integer of length 7, got '{pid}'.")
    try:
        result = requests.get(f"https://api-web.nhle.com/v1/player/{pid}/landing")
        # print(f"{result=}")
        # print(f"{result.text=}")
        # print(f"{result.content=}")
        # print(f"{result.json()=}")
        result = result.json()
    except requests.RequestException as req_e:
        result = {"None": "none"}
        print(f"{req_e=}")
    return result


# Caching the fetched data
# @st.cache_data(show_spinner=False)
async def fetch_data(url):
    response = requests.get(url)
    return response.json()


async def load_all_data():
    tasks = []
    for i, pid in enumerate(df_nhl_jerseys["NHL_API_PlayerID"].dropna().unique()):
        url = f"https://api-web.nhle.com/v1/player/{int(pid)}/landing"
        print(f"url_{i}: {url}")
        tasks.append(fetch_data(url))
    results = await asyncio.gather(*tasks)
    return dict(zip(df_nhl_jerseys['NHL_API_PlayerID'].dropna().unique(), results))


@st.cache_data(show_spinner=False)
def load_all_nhl_player_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(load_all_data())
    loop.close()
    return data


def new_jersey_preview():
    # opened_only = st.session_state.njp_tog_image_only
    # images_only = st.session_state.njp_tog_image_only
    opened_only = tog_njp_opened_only
    images_only = tog_njp_images_only
    # print(f"{opened_only=}\n{images_only=}")
    # print(f"{st.session_state.njp_tog_image_only=}")
    # print(f"{st.session_state.njp_tog_open_only=}")
    # print(f"{tog_njp_opened_only=}")
    # print(f"{tog_njp_images_only=}")

    if images_only:
        df = df_nhl_jerseys_images
    elif opened_only:
        df = df_nhl_jerseys_opened
    else:
        df = df_nhl_jerseys_owned

    n = df.shape[0]

    rnd_id = st.session_state.njp_last_id
    if rnd_id is None:
        st.session_state.njp_last_id = rnd_n = rnd_id = 0

    # df_nhl_jerseys.loc[df_nhl_jerseys["JerseyID"] == ]
    while rnd_id == st.session_state.njp_last_id:
        rnd_n = random.randint(0, n)
        rnd_id = df.iloc[rnd_n]["JerseyID"]

    print(f"{n=}, {rnd_id=}")

    df_njp = df.loc[df["JerseyID"] == rnd_id].iloc[0]
    # j_id = df_njp["JerseyID"]
    brand = df_njp["BrandName"]
    make = df_njp["Colours"]
    team = df_njp["Team"]
    pl_num = f"{int(df_njp['Number'])}"
    pl_first = df_njp["PlayerFirst"]
    pl_last = df_njp["PlayerLast"]
    nhl_api_pid = df_njp["NHL_API_PlayerID"]

    print(f"{brand=}, {make=}, {team=}, {pl_num=}, {pl_first=}, {pl_last=}")

    st.session_state.njp_last_id = rnd_id
    st.session_state.njp_brand = brand
    st.session_state.njp_make = make
    st.session_state.njp_team = team
    st.session_state.njp_pl_first = pl_first
    st.session_state.njp_pl_last = pl_last
    st.session_state.njp_pl_num = pl_num

    if not pd.isna(nhl_api_pid):
        # json_result = query_player(int(nhl_api_pid))
        if nhl_api_pid not in loaded_nhl_player_data:
            print(f"SLOW RETRIEVAL")
            json_result = query_player(int(nhl_api_pid))
        else:
            print(f"FAST RETRIEVAL")
            json_result = loaded_nhl_player_data[nhl_api_pid]
        # print(f"{json_result=}")

        path_team_logo = json_result.get("teamLogo")
        path_headshot_logo = json_result.get("headshot")
        path_hero_shot_logo = json_result.get("heroImage")

        pl_name_first = json_result.get("firstName", dict()).get("default", pl_first)
        pl_name_last = json_result.get("lastName", dict()).get("default", pl_last)
        pl_number = json_result.get("sweaterNumber", pl_num)
        pl_position = json_result.get("position")
        pl_shoots_catches = json_result.get("shootsCatches")
        pl_height_inch = json_result.get("heightInInches")
        pl_height_cent = json_result.get("heightInCentimeters")
        pl_weight_lb = json_result.get("weightInPounds")
        pl_weight_kg = json_result.get("weightInKilograms")
        pl_is_active = json_result.get("isActive")
        pl_dob = json_result.get("birthDate")
        pl_birth_city = json_result.get("birthCity", dict()).get("default")
        pl_birth_province = json_result.get("birthStateProvince", dict()).get("default")
        pl_birth_country = json_result.get("birthCountry")
        pl_in_HHOF = json_result.get("inHHOF")

        draft_year = json_result.get("draftDetails", dict()).get("year")
        draft_team_abbrev = json_result.get("draftDetails", dict()).get("teamAbbrev")
        draft_round = json_result.get("draftDetails", dict()).get("round")
        draft_pick_in_round = json_result.get("draftDetails", dict()).get("pickInRound")
        draft_overall_pick = json_result.get("draftDetails", dict()).get("overallPick")

        team_id = json_result.get("currentTeamId")
        team_abbrev = json_result.get("currentTeamAbbrev")
        team_name = json_result.get("fullTeamName", dict()).get("default")
        team_name_fr = json_result.get("fullTeamName", dict()).get("fr", team_name)
        team_common_name = json_result.get("teamCommonName", dict()).get("default")
        team_place_name = json_result.get("teamPlaceNameWithPreposition", dict()).get("default")
        team_place_name_fr = json_result.get("teamPlaceNameWithPreposition", dict()).get("fr", team_place_name)

        with njp_gc[7]:
            njp_gc_cols = st.columns(2)
            with njp_gc_cols[0]:
                if path_headshot_logo:
                    st.image(
                        path_headshot_logo,
                        caption=f"{pl_first} {pl_last}"
                    )
                njp_gc_cols_0 = st.columns(2)
                with njp_gc_cols_0[0]:
                    st.write(f"#{pl_number}")
                with njp_gc_cols_0[1]:
                    st.write(f"Active: {pl_is_active}")
                st.write(f"{pl_name_first} {pl_name_last}")

            with njp_gc_cols[1]:
                njp_gc_cols_1 = st.columns(3)
                if path_team_logo:
                    with njp_gc_cols_1[0]:
                        st.image(
                            path_team_logo,
                            caption=team_name
                        )
                    with njp_gc_cols_1[1]:
                        st.write(f"Position: {pl_position}")
                    with njp_gc_cols_1[2]:
                        if pl_position == "G":
                            st.write(f"catches: {pl_shoots_catches}")
                        else:
                            st.write(f"shoots: {pl_shoots_catches}")

                njp_gc_cols_2 = st.columns(2)
                with njp_gc_cols_2[0]:
                    # st.write(f"{pl_height_inch}\"")
                    st.write(f"{pl_height_inch // 12}' {pl_height_inch - (12 * (pl_height_inch // 12))}\"")
                with njp_gc_cols_2[1]:
                    st.write(f"{pl_weight_lb} lbs")
                st.write(f"{pl_dob}")
                st.write(f"{pl_birth_city}, {pl_birth_province}, {pl_birth_country}")
                st.write(f"In Hockey HOF: {bool(pl_in_HHOF)}")
                st.write(f"Drafted in {draft_year}")
                st.write(f"{draft_overall_pick}{number_suffix(draft_overall_pick)} Overall ({draft_pick_in_round}{number_suffix(draft_pick_in_round)} pick {draft_round}{number_suffix(draft_round)} Round)")

            if path_hero_shot_logo:
                st.image(path_hero_shot_logo, caption=f"{pl_first} {pl_last}")
            st.json(json_result)

    update_njp_image()


def update_njp_image():
    j_id = st.session_state.njp_last_id
    # df_njp = df_nhl_jerseys_owned.loc[df_nhl_jerseys_owned["JerseyID"] == j_id]
    # j_id = df_njp["JerseyID"]
    # print(f"{j_id=}")
    df_njp_img = df_jersey_images.loc[df_jersey_images["JerseyID"] == j_id]

    if not df_njp_img.empty:
        img_idx = st.session_state.njp_img_idx
        path = df_njp_img.iloc[img_idx]["Path"]
        cap = df_njp_img.iloc[img_idx]["NoImageText"]
        st.session_state.njp_img_path = path
        st.session_state.njp_img_cap = cap
        st.session_state.njp_img_max_idx = df_njp_img.shape[0] - 1
    else:
        st.session_state.njp_img_path = None
        st.session_state.njp_img_cap = None


def njp_image_click_left():
    n = st.session_state.njp_img_idx
    st.session_state.njp_img_idx = max(n - 1, 0)
    update_njp_image()


def njp_image_click_right():
    n = st.session_state.njp_img_idx
    m = st.session_state.njp_img_max_idx
    st.session_state.njp_img_idx = min(m, n + 1)
    update_njp_image()


def toggle_njp_image_only():
    new_jersey_preview()


def toggle_njp_opened_only():
    new_jersey_preview()


def random_jersey():
    rj = random.randint(0, df_nhl_jerseys_opened.shape[0])
    rj = df_nhl_jerseys_opened.iloc[rj]
    print(f"{rj}")


@st.cache_data
def load_excel_dfs():
    return pd.read_excel(
        r"D:\NHL Jerseys.xlsm",
        sheet_name=list(range(8))
    )


if __name__ == '__main__':

    st.set_page_config(
        page_title="Avery's Jerseys",
        layout="wide"
    )

    for k, v in (
            ("njp_last_id", None),

            ("njp_brand", None),
            ("njp_make", None),
            ("njp_team", None),
            ("njp_pl_num", None),
            ("njp_pl_first", None),
            ("njp_pl_last", None),

            ("njp_img_idx", 0),
            ("njp_img_max_idx", 0),
            ("njp_img_path", None),
            ("njp_tog_open_only", False),
            ("njp_tog_image_only", False),
            ("njp_img_cap", "Select a jersey to check if images exist")
    ):
        if k not in st.session_state:
            st.session_state.setdefault(k, v)

    excel_dfs = load_excel_dfs()

    excel_dfs_keys = list(excel_dfs.keys())

    df_nhl_jerseys = excel_dfs[excel_dfs_keys[0]]
    df_jersey_images = excel_dfs[excel_dfs_keys[1]]
    df_nike_jerseys = excel_dfs[excel_dfs_keys[2]]
    df_jersey_wishlist = excel_dfs[excel_dfs_keys[3]]
    df_jersey_reporting = excel_dfs[excel_dfs_keys[4]]
    df_nhl_teams = excel_dfs[excel_dfs_keys[5]]
    df_nhl_divisions = excel_dfs[excel_dfs_keys[6]]
    df_nhl_conferences = excel_dfs[excel_dfs_keys[7]]

    df_nhl_jerseys_owned = df_nhl_jerseys.loc[
        (df_nhl_jerseys["OpenDate"] is not None)
        & (df_nhl_jerseys["CancelledOrder"] == 0)
        & (df_nhl_jerseys["Team"] != "")
        & (df_nhl_jerseys["Team"] is not None)
        ]
    df_nhl_jerseys_opened = df_nhl_jerseys_owned.loc[
        (df_nhl_jerseys_owned["OpenDate"] is not None)
        & (df_nhl_jerseys["Team"] != "")
        & (df_nhl_jerseys["Team"] is not None)
        ]
    df_nhl_jerseys_images = df_nhl_jerseys_opened.merge(
        df_jersey_images,
        how="left",
        on="JerseyID"
    )

    loaded_nhl_player_data = load_all_nhl_player_data()

    # Begin Widgets
    st.dataframe(df_nhl_jerseys_owned)
    st.dataframe(df_nhl_jerseys_images)

    # print(f"{df_nhl_jerseys}")
    # print(f"{df_nike_jerseys}")
    # print(f"{df_jersey_wishlist}")
    # print(f"{df_jersey_reporting}")
    # print(f"{df_nhl_teams}")
    # print(f"{df_nhl_divisions}")
    # print(f"{df_nhl_conferences}")

    # btn_njp_opened_only = stoggle(
    #     label=f"Opened Jerseys Only",
    #     help=f"Show a only jerseys that I have already opened",
    #     on_click=new_jersey_preview
    # )

    btn_random = st.button(
        label="random",
        on_click=random_jersey
    )

    njp_gc = [
        st.columns(3),
        st.divider(),
        st.columns(3),
        st.columns(3),
        st.columns(2),
        st.columns(1),
        st.divider(),
        st.expander(label="NHL Data", expanded=False)
    ]

    with njp_gc[0][0]:
        btn_njp = st.button(
            label=f"Change Jersey Preview",
            help=f"Show a new jersey in the preview area",
            on_click=new_jersey_preview
        )
    with njp_gc[0][1]:
        tog_njp_opened_only = st.toggle(
            label=f"Opened Jerseys Only",
            help=f"Show a only jerseys that I have already opened",
            value=st.session_state.njp_tog_open_only,
            on_change=toggle_njp_opened_only
        )
    with njp_gc[0][2]:
        tog_njp_images_only = st.toggle(
            label=f"Jerseys With Images Only",
            help=f"Show a only jerseys that I have images for",
            value=st.session_state.njp_tog_image_only,
            on_change=toggle_njp_image_only
        )

    with njp_gc[2][0]:
        txt_njp_brand = card(
            title=f"Brand Name:",
            text=st.session_state.njp_brand
        )
    with njp_gc[2][1]:
        txt_njp_make = card(
            title=f"Make Name:",
            text=st.session_state.njp_make
        )
    with njp_gc[2][2]:
        txt_njp_team = card(
            title=f"Team Name:",
            text=st.session_state.njp_team
        )
    with njp_gc[3][0]:
        txt_njp_pl_num = card(
            title=f"Player Number:",
            text=st.session_state.njp_pl_num
        )
    with njp_gc[3][1]:
        txt_njp_pl_first = card(
            title=f"First Name:",
            text=st.session_state.njp_pl_first
        )
    with njp_gc[3][2]:
        txt_njp_pl_last = card(
            title=f"Last Name:",
            text=st.session_state.njp_pl_last
        )

    if st.session_state.njp_img_path is not None:
        with njp_gc[4][0]:
            btn_njp_img_l = st.button(
                label=f"prev",
                help=f"previous image",
                on_click=njp_image_click_left
            )
        with njp_gc[4][1]:
            btn_njp_img_r = st.button(
                label=f"next",
                help=f"next image",
                on_click=njp_image_click_right
            )

        img = Image.open(st.session_state.njp_img_path).rotate(-90)
        n = st.session_state.njp_img_idx + 1
        m = st.session_state.njp_img_max_idx + 1
        with njp_gc[5][0]:
            njp_img = st.image(
                image=img,
                caption=st.session_state.njp_img_cap
            )

            st.markdown(f"{n} / {m} image" + ("" if m == 1 else "s"))

    else:
        if st.session_state.njp_last_id is None:
            with njp_gc[7]:
                # st.json({"VALUE": f"Nothing Yet {datetime.datetime.now():%x %X}"})
                st.json({"VALUE": f"Nothing Yet"})

    expander = st.expander(
        label=f"General Stats"
    )

    # most popular number
    list_player_numbers = df_nhl_jerseys["Number"].values.tolist()
    count_occurrences = [(k, list_player_numbers.count(k)) for k in list_player_numbers if not pd.isna(k)]
    count_occurrences.sort(key=lambda tup: tup[1], reverse=True)
    with expander:
        card(
            "Most popular number:",
            f"# {int(count_occurrences[0][0])}"
        )

    # most popular first name
    list_player_first_name = df_nhl_jerseys["PlayerFirst"].values.tolist()
    count_occurrences_first_name = [(k, list_player_first_name.count(k)) for k in list_player_first_name if
                                    not pd.isna(k)]
    count_occurrences_first_name.sort(key=lambda tup: tup[1], reverse=True)
    with expander:
        card(
            "Most popular first name:",
            f"{count_occurrences_first_name[0][0]}"
        )

    # most popular last name
    list_player_last_name = df_nhl_jerseys["PlayerLast"].values.tolist()
    count_occurrences_last_name = [(k, list_player_last_name.count(k)) for k in list_player_last_name if not pd.isna(k)]
    count_occurrences_last_name.sort(key=lambda tup: tup[1], reverse=True)
    with expander:
        card(
            "Most popular last name:",
            f"{count_occurrences_last_name[0][0]}"
        )

    # most popular country
    list_player_country = df_nhl_jerseys["Nationality"].values.tolist()
    count_occurrences_country = [(k, list_player_country.count(k)) for k in list_player_country if not pd.isna(k)]
    count_occurrences_country.sort(key=lambda tup: tup[1], reverse=True)
    with expander:
        card(
            "Most popular country:",
            f"{count_occurrences_country[0][0]}"
        )

    # most popular position
    list_player_position = df_nhl_jerseys["Position"].values.tolist()
    count_occurrences_position = [(k, list_player_position.count(k)) for k in list_player_position if not pd.isna(k)]
    count_occurrences_position.sort(key=lambda tup: tup[1], reverse=True)
    with expander:
        card(
            "Most popular position:",
            f"{count_occurrences_position[0][0]}"
        )

    # most popular team
    list_player_team = df_nhl_jerseys["Team"].values.tolist()
    count_occurrences_team = [(k, list_player_team.count(k)) for k in list_player_team if not pd.isna(k)]
    count_occurrences_team.sort(key=lambda tup: tup[1], reverse=True)
    with expander:
        card(
            "Most popular team:",
            f"{count_occurrences_team[0][0]}"
        )

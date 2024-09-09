import asyncio
import datetime
import os.path
import random

import requests
from PIL import Image
from matplotlib import pyplot as plt
import plotly.express as px
from streamlit_extras.card import card
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd

from colour_utility import Colour
from location_utility import address_to_coords
from utility import number_suffix


ROOT_IMAGE_RESOURCES = r"C:\Users\abrig\Documents\Coding_Practice\Resources\Flags"
if not os.path.exists(ROOT_IMAGE_RESOURCES):
    ROOT_IMAGE_RESOURCES = r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags"
def_colour_text = Colour("#FFFFFF")


def decode_position(position_code: str) -> str:
    match position_code.lower():
        case "g":
            return "Goalie"
        case "c":
            return "Center"
        case "l":
            return "Left Wing"
        case "r":
            return "Right Wing"
        case "d":
            return "Defence"
        case _:
            return position_code


@st.cache_data(show_spinner=False)
def query_lat_long(address):
    return address_to_coords(pl_address)


@st.cache_data(show_spinner=False)
def search_image_resources(term: str):
    sterm = term.lower().removesuffix(".png").replace(" ", "-")
    if sterm == "russia":
        sterm = "russian-federation"
    if os.path.exists(ROOT_IMAGE_RESOURCES) and sterm:
        for path in os.listdir(ROOT_IMAGE_RESOURCES):
            st_path = "".join(path.removeprefix("icons8-").split("-")[:2]).removesuffix("flag").removesuffix(".png").replace(" ", "-")
            # print(f"{sterm=}, {st_path=}")
            if sterm == st_path.lower():
                return os.path.join(ROOT_IMAGE_RESOURCES, path)
    print(f"\t\tNO PATH FOUND for '{term}'")


def get_state_flag(province):
    return search_image_resources(province)


def get_country_flag(country):
    return search_image_resources(country)


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
    # print(f"df_njp\t{df_njp}")
    # st.write("HERE V")
    st.dataframe(df_njp)
    # j_id = df_njp["JerseyID"]
    brand = df_njp["BrandName"]
    make = df_njp["Colours"]
    team = df_njp["Team"]
    pl_num = f"{int(df_njp['Number'])}"
    pl_first = df_njp["PlayerFirst"]
    pl_last = df_njp["PlayerLast"]
    nhl_api_pid = df_njp["NHL_API_PlayerID"]
    pl_address = df_njp["address"]
    df_team = df_nhl_teams.loc[df_nhl_teams["FullTeamName"] == team]
    team_colours = list()
    if not df_team.empty:
        columns = ["Colour_1", "Colour_2", "Colour_3", "Colour_4", "Colour_5", "Colour_6"]
        df_cols = df_team[columns]
        print(f"df_cols:\n{df_cols}")
        for col in columns:
            lst = df_cols[col].dropna().values.tolist()
            print(f"{col=}, {lst=}")
            if lst:
                team_colours.append(lst[0])
    else:
        print(f"df_teams is empty")

    print(f"{brand=}, {make=}, {team=}, {pl_num=}, {pl_first=}, {pl_last=}")

    st.session_state.njp_last_id = rnd_id
    st.session_state.njp_brand = brand
    st.session_state.njp_make = make
    st.session_state.njp_team = team
    st.session_state.njp_pl_first = pl_first
    st.session_state.njp_pl_last = pl_last
    st.session_state.njp_pl_num = pl_num

    st.toast(f"#{pl_num} {pl_first} {pl_last}")

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

        featured_stats = json_result.get("featuredStats", dict())
        career_totals = json_result.get("careerTotals", dict())
        last_5_games = json_result.get("last5Games", list())
        season_totals = json_result.get("seasonTotals", list())
        current_team_roster = json_result.get("currentTeamRoster", list())

        cols_season_totals = [
            "season",
            "leagueAbbrev",
            "teamName"
            "gamesTypeId",
            "goals",
            "assists",
            "points",
            "gamesPlayed",
            "plusMinus",
            "powerPlayGoals",
            "shortHandedGoals",
            "pim"
        ]
        data_season_totals = list()
        data_playoff_totals = list()
        data_unknown_totals = list()
        for i, data in enumerate(season_totals):
            print(f"{data=}")
            if data["gameTypeId"] == 2:
                # season
                data_totals = data_season_totals
            elif data["gameTypeId"] == 3:
                # playoffs
                data_totals = data_playoff_totals
            else:
                # figure these ones out
                data_totals = data_unknown_totals
            table_data = {
                "Season": str(data["season"])[:4] + "-" + str(data["season"])[4:],
                "League": data["leagueAbbrev"],
                "Team": data["teamName"]["default"],
                "G": data.get("goals", 0),
                "A": data.get("assists", 0),
                "GA": data.get("goalsAgainst"),
                "GAAVG": data.get("goalsAgainstAvg"),
                "L": data.get("losses", 0),
                "OTL": data.get("otLosses", 0),
                "SV%": data.get("savePctg", 0),
                "SA": data.get("shotsAgainst", 0),
                "SO": data.get("shutouts", 0),
                "PTS": data.get("points", 0),
                "GP": data.get("gamesPlayed", 0),
                "+/-": data.get("plusMinus", "-"),
                "PPG": data.get("powerPlayGoals", "-"),
                "SHG": data.get("shortHandedGoals", "-"),
                "PIM": data.get("pim", "-")
            }
            if pl_position != "G":
                table_data.pop("GA")
                table_data.pop("GAAVG")
                table_data.pop("L")
                table_data.pop("OTL")
                table_data.pop("SV%")
                table_data.pop("SA")
                table_data.pop("SO")

            data_totals.append(table_data)

        data_season_totals.sort(key=lambda d: d["Season"])
        data_playoff_totals.sort(key=lambda d: d["Season"])
        data_unknown_totals.sort(key=lambda d: d["Season"])

        df_season_totals = pd.DataFrame(data_season_totals)
        df_playoff_totals = pd.DataFrame(data_playoff_totals)
        df_unknown_totals = pd.DataFrame(data_unknown_totals)

        df_totals = df_season_totals.merge(
            df_playoff_totals,
            how="left",
            on=["Season", "League", "Team"]
        )

        birthStateProvinceImage = df_njp["birthStateProvinceImage"]
        birthCountryImage = df_njp["birthCountryImage"]

        with njp_gc[7]:

            # st.dataframe(df_season_totals)
            # st.dataframe(df_playoff_totals)
            st.dataframe(df_totals)
            if not df_unknown_totals.empty:
                st.dataframe(df_unknown_totals)
            if not df_team.empty:
                st.dataframe(df_team)

            if team_colours:
                cols_team_colours = st.columns(len(team_colours))
                for i, colour in enumerate(team_colours):
                    fg = Colour(colour).font_foreground(rgb=False)
                    with cols_team_colours[i]:
                        st.markdown(
                            f"""
                            <div style='background-color: {colour}; padding: 10px; border-radius: 5px;'>
                                <h3 style='color: {fg}'>{colour}</h3>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.write(f"Could not fetch team colours.")

            njp_gc_cols = st.columns(2)
            with njp_gc_cols[0]:
                njp_gc_cols_a = st.columns(2)
                with njp_gc_cols_a[0]:
                    if path_headshot_logo:
                        st.image(
                            path_headshot_logo,
                            caption=f"{pl_first} {pl_last}"
                        )
                with njp_gc_cols_a[1]:
                    if path_hero_shot_logo:
                        st.image(
                            path_hero_shot_logo
                            # ,
                            # caption=f"{pl_first} {pl_last}"
                        )

                cols_birth_state_country = st.columns(2)
                if birthStateProvinceImage:
                    with cols_birth_state_country[0]:
                        st.image(
                            Image.open(birthStateProvinceImage)
                        )
                if birthCountryImage:
                    with cols_birth_state_country[1]:
                        st.image(
                            Image.open(birthCountryImage)
                        )

                njp_gc_cols_0 = st.columns(4)
                with njp_gc_cols_0[0]:
                    st.write(f"#{pl_number}")
                with njp_gc_cols_0[1]:
                    st.write(f"{decode_position(pl_position)}")
                with njp_gc_cols_0[2]:
                    if pl_position == "G":
                        st.write(f"catches: {pl_shoots_catches}")
                    else:
                        st.write(f"shoots: {pl_shoots_catches}")
                with njp_gc_cols_0[3]:
                    st.write(f"Active: {pl_is_active}")
                st.write(f"{pl_name_first} {pl_name_last}")

            with njp_gc_cols[1]:
                # njp_gc_cols_1 = st.columns(3)
                if path_team_logo:
                    # with njp_gc_cols_1[0]:
                    st.image(
                        path_team_logo,
                        caption=team_name
                    )
                    # with njp_gc_cols_1[1]:

                njp_gc_cols_2 = st.columns(2)
                with njp_gc_cols_2[0]:
                    # st.write(f"{pl_height_inch}\"")
                    st.write(f"{pl_height_inch // 12}' {pl_height_inch - (12 * (pl_height_inch // 12))}\"")
                with njp_gc_cols_2[1]:
                    st.write(f"{pl_weight_lb} lbs")
                st.write(f"{pl_dob}")
                # st.write(f"{pl_birth_city}, {pl_birth_province}, {pl_birth_country}")
                st.write(f"{pl_address}")
                st.write(f"In Hockey HOF: {bool(pl_in_HHOF)}")
                st.write(f"Drafted in {draft_year}")
                if draft_overall_pick:
                    st.write(
                        f"{draft_overall_pick}{number_suffix(draft_overall_pick)} Overall ({draft_pick_in_round}{number_suffix(draft_pick_in_round)} pick {draft_round}{number_suffix(draft_round)} Round)")
                else:
                    st.write("Undrafted")

            # if path_hero_shot_logo:
            #     st.image(path_hero_shot_logo, caption=f"{pl_first} {pl_last}")
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
        if not os.path.exists(path):
            path = None
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
    if os.path.exists(r"D:\NHL Jerseys.xlsm"):
        return pd.read_excel(
            r"D:\NHL Jerseys.xlsm",
            sheet_name=list(range(8))
        )
    else:
        if os.path.exists(
                r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHL Jerseys as of 202408280337.xlsm"):
            return pd.read_excel(
                r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHL Jerseys as of 202408280337.xlsm",
                sheet_name=list(range(8))
            )
        else:
            return pd.read_excel(
                r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\NHL Jerseys as of 202408280337.xlsm",
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

    df_nhl_jerseys = df_nhl_jerseys.rename(
        columns={
            "Conference": "ConferenceName",
            "Division": "DivisionName"
        }
    )

    df_nhl_jerseys = df_nhl_jerseys.merge(
        df_nhl_teams,
        how="inner",
        left_on="Team",
        right_on="FullTeamName",
        suffixes=("NHLJerseyData", "NHLDivisions")
    )
    st.write(f"A")
    st.dataframe(df_nhl_jerseys)

    df_nhl_jerseys = df_nhl_jerseys.merge(
        df_nhl_divisions,
        how="inner",
        on="Division",
        suffixes=("NHLJerseyData__x__NHLDivision", "NHLConferences")
    )
    st.write(f"B")
    st.dataframe(df_nhl_jerseys)

    df_nhl_jerseys = df_nhl_jerseys.merge(
        df_nhl_conferences,
        how="inner",
        on="Conference"
    )
    st.write(f"C")
    st.dataframe(df_nhl_jerseys)

    loaded_nhl_player_data = load_all_nhl_player_data()
    for nhl_api_key, json_data in loaded_nhl_player_data.items():

        pl_name_first = json_data.get("firstName", dict()).get("default")
        pl_name_last = json_data.get("lastName", dict()).get("default")

        if pl_name_first and pl_name_last:
            path_team_logo = json_data.get("teamLogo")
            path_headshot_logo = json_data.get("headshot")
            path_hero_shot_logo = json_data.get("heroImage")

            pl_number = json_data.get("sweaterNumber")
            pl_position = json_data.get("position")
            pl_shoots_catches = json_data.get("shootsCatches")
            pl_height_inch = json_data.get("heightInInches")
            pl_height_cent = json_data.get("heightInCentimeters")
            pl_weight_lb = json_data.get("weightInPounds")
            pl_weight_kg = json_data.get("weightInKilograms")
            pl_is_active = json_data.get("isActive")
            pl_dob = json_data.get("birthDate")
            pl_birth_city = json_data.get("birthCity", dict()).get("default", "")
            pl_birth_province = json_data.get("birthStateProvince", dict()).get("default", "")
            pl_birth_country = json_data.get("birthCountry", "")

            pl_in_HHOF = json_data.get("inHHOF")

            draft_year = json_data.get("draftDetails", dict()).get("year")
            draft_team_abbrev = json_data.get("draftDetails", dict()).get("teamAbbrev")
            draft_round = json_data.get("draftDetails", dict()).get("round")
            draft_pick_in_round = json_data.get("draftDetails", dict()).get("pickInRound")
            draft_overall_pick = json_data.get("draftDetails", dict()).get("overallPick")

            team_id = json_data.get("currentTeamId")
            team_abbrev = json_data.get("currentTeamAbbrev")
            team_name = json_data.get("fullTeamName", dict()).get("default")
            team_name_fr = json_data.get("fullTeamName", dict()).get("fr", team_name)
            team_common_name = json_data.get("teamCommonName", dict()).get("default")
            team_place_name = json_data.get("teamPlaceNameWithPreposition", dict()).get("default")
            team_place_name_fr = json_data.get("teamPlaceNameWithPreposition", dict()).get("fr", team_place_name)

            featured_stats = json_data.get("featuredStats", dict())
            career_totals = json_data.get("careerTotals", dict())
            last_5_games = json_data.get("last5Games", list())
            season_totals = json_data.get("seasonTotals", list())
            current_team_roster = json_data.get("currentTeamRoster", list())

            for sn, ln in (
                    ("CAN", "Canada"),
                    ("SLO", "Slovakia"),
                    ("SWE", "Sweden"),
                    ("FIN", "Finland"),
                    ("SUI", "Switzerland"),
                    ("GER", "Germany"),
                    ("RUS", "Russia")
            ):
                pl_birth_country = pl_birth_country.replace(sn, ln)
            pl_address = f"{pl_birth_city}, {pl_birth_province}, {pl_birth_country}"
            pl_address = pl_address.replace(", , ", ", ")
            pl_birth_province_image = get_state_flag(pl_birth_province)
            pl_birth_country_image = get_country_flag(pl_birth_country)
            # pl_birth_province_image = pl_birth_province_image if not pl_birth_province_image else Image.open(pl_birth_province_image)
            # pl_birth_country_image = pl_birth_country_image if not pl_birth_country_image else Image.open(pl_birth_country_image)

            if pl_address.strip().removeprefix(",").removesuffix(",").strip():
                pl_coords = query_lat_long(pl_address)
                # set all rows that match 'PlayerFirst' and 'PlayerLast' in 'df_nhl_jerseys' with the new address
                df_nhl_jerseys.loc[
                    (df_nhl_jerseys["PlayerFirst"] == pl_name_first)
                    & (df_nhl_jerseys["PlayerLast"] == pl_name_last),
                    [
                        "latitude",
                        "longitude",
                        "birthCity",
                        "birthStateProvince",
                        "birthStateProvinceImage",
                        "birthCountry",
                        "birthCountryImage",
                        "address",
                        "activePlayer"
                    ]
                ] = (
                    *pl_coords,
                    pl_birth_city,
                    pl_birth_province,
                    pl_birth_province_image,
                    pl_birth_country,
                    pl_birth_country_image,
                    pl_address,
                    pl_is_active
                )

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

    df_active_players: pd.DataFrame = df_nhl_jerseys.loc[
        (df_nhl_jerseys["activePlayer"] == 1)
    ]
    p_df_active_players = df_active_players[
        ['PlayerFirst', 'PlayerLast', 'birthCountry', 'address', 'activePlayer']
    ].drop_duplicates(
        subset=['PlayerFirst', 'PlayerLast']
    ).sort_values(by=['PlayerLast', 'PlayerFirst'])
    print(f"{p_df_active_players=}")

    df_inactive_players: pd.DataFrame = df_nhl_jerseys.loc[
        df_nhl_jerseys["activePlayer"] == 0
        ]
    p_df_inactive_players = df_inactive_players[
        ['PlayerFirst', 'PlayerLast', 'birthCountry', 'address', 'activePlayer']
    ].drop_duplicates(
        subset=['PlayerFirst', 'PlayerLast']
    ).sort_values(by=['PlayerLast', 'PlayerFirst'])
    print(f"{p_df_inactive_players=}")

    total_active_players = df_active_players.drop_duplicates(subset=["PlayerFirst", "PlayerLast"]).shape[0]
    total_inactive_players = df_inactive_players.drop_duplicates(subset=["PlayerFirst", "PlayerLast"]).shape[0]
    print(f"{total_active_players=}")
    print(f"{total_inactive_players=}")

    df_numbers_plt = df_nhl_jerseys["Number"].value_counts().sort_index().dropna()
    fig_plt, ax_plt = plt.subplots()
    ax_plt.bar(df_numbers_plt.index, df_numbers_plt.values)
    ax_plt.set_title("Player Number Frequency")
    ax_plt.set_xlabel("Number")
    ax_plt.set_ylabel("Frequency")
    # ax_plt.set_xticks(range(int(min(df_numbers_plt.index)), int(max(df_numbers_plt.index) + 1)))
    ax_plt.set_xticks(df_numbers_plt.index)
    # Display the plot in Streamlit
    with st.expander("Jersey Numbers MatPlotLib"):
        st.pyplot(fig_plt)

    df_numbers_ply = df_nhl_jerseys["Number"].value_counts().sort_index().reset_index()
    df_numbers_ply.columns = ["Number", "Frequency"]
    fig_ply_numbers = px.bar(df_numbers_ply, x="Number", y="Frequency", title="Player Number Frequency")
    with st.expander("Jersey Numbers Plotly"):
        st.plotly_chart(fig_ply_numbers)

    df_u_players_countries_ply = df_nhl_jerseys[["PlayerFirst", "PlayerLast", "Nationality"]].drop_duplicates()
    df_countries_ply = df_u_players_countries_ply["Nationality"].value_counts().sort_values(
        ascending=False).reset_index()
    # df_countries_ply = df_nhl_jerseys["Nationality"].value_counts().sort_values(ascending=False).reset_index()
    df_countries_ply.columns = ["Country", "Frequency"]
    # df_countries_ply["Country"] = df_countries_ply["Country"] + f"{100*df_countries_ply['Frequency']/df_countries_ply.shape[0]:.2f} %"
    df_countries_ply["Country"] = df_countries_ply.apply(
        lambda row: f"{row['Country']}: {100 * row['Frequency'] / df_countries_ply['Frequency'].sum():.2f} %", axis=1)
    fig_ply_countries = px.bar(df_countries_ply, x="Country", y="Frequency", title="Player Number Frequency")
    with st.expander("Player Nationalities"):
        st.plotly_chart(fig_ply_countries)
        st.write(
            f"{df_u_players_countries_ply.shape[0]} unique players from {df_countries_ply.shape[0]} unique countries")

    df_u_players_sizes_ply = df_nhl_jerseys[["Size"]]
    df_sizes_ply = df_u_players_sizes_ply["Size"].value_counts().sort_values(ascending=False).reset_index()
    # df_countries_ply = df_nhl_jerseys["Nationality"].value_counts().sort_values(ascending=False).reset_index()
    df_sizes_ply.columns = ["Size", "Frequency"]
    # df_countries_ply["Country"] = df_countries_ply["Country"] + f"{100*df_countries_ply['Frequency']/df_countries_ply.shape[0]:.2f} %"
    df_sizes_ply["Size"] = df_sizes_ply.apply(
        lambda row: f"{row['Size']}: {100 * row['Frequency'] / df_sizes_ply['Frequency'].sum():.2f} %", axis=1)
    fig_ply_sizes = px.bar(df_sizes_ply, x="Size", y="Frequency", title="Jersey Size Frequency")
    with st.expander("Jersey Sizes"):
        st.plotly_chart(fig_ply_sizes)

    df_u_players_brand_ply = df_nhl_jerseys[["BrandName"]]
    df_brand_ply = df_u_players_brand_ply["BrandName"].value_counts().sort_values(ascending=False).reset_index()
    # df_countries_ply = df_nhl_jerseys["Nationality"].value_counts().sort_values(ascending=False).reset_index()
    df_brand_ply.columns = ["Brand Name", "Frequency"]
    # df_countries_ply["Country"] = df_countries_ply["Country"] + f"{100*df_countries_ply['Frequency']/df_countries_ply.shape[0]:.2f} %"
    df_brand_ply["Brand Name"] = df_brand_ply.apply(
        lambda row: f"{row['Brand Name']}: {100 * row['Frequency'] / df_brand_ply['Frequency'].sum():.2f} %", axis=1)
    fig_ply_brand = px.bar(df_brand_ply, x="Brand Name", y="Frequency", title="Jersey Brand Name Frequency")
    with st.expander("Jersey Brand"):
        st.plotly_chart(fig_ply_brand)

    df_u_players_make_ply = df_nhl_jerseys[["JerseyMake"]]
    df_make_ply = df_u_players_make_ply["JerseyMake"].value_counts().sort_values(ascending=False).reset_index()
    # df_countries_ply = df_nhl_jerseys["Nationality"].value_counts().sort_values(ascending=False).reset_index()
    df_make_ply.columns = ["Make", "Frequency"]
    # df_countries_ply["Country"] = df_countries_ply["Country"] + f"{100*df_countries_ply['Frequency']/df_countries_ply.shape[0]:.2f} %"
    df_make_ply["Make"] = df_make_ply.apply(
        lambda row: f"{row['Make']}: {100 * row['Frequency'] / df_make_ply['Frequency'].sum():.2f} %", axis=1)
    fig_ply_make = px.bar(df_make_ply, x="Make", y="Frequency", title="Jersey Brand Name Frequency")
    with st.expander("Jersey Make"):
        st.plotly_chart(fig_ply_make)

    df_u_players_teams_ply = df_nhl_jerseys[["Team"]]
    df_teams_ply = df_u_players_teams_ply["Team"].value_counts().sort_values(ascending=False).reset_index()
    # df_countries_ply = df_nhl_jerseys["Nationality"].value_counts().sort_values(ascending=False).reset_index()
    df_teams_ply.columns = ["Team", "Frequency"]
    # df_countries_ply["Country"] = df_countries_ply["Country"] + f"{100*df_countries_ply['Frequency']/df_countries_ply.shape[0]:.2f} %"
    df_teams_ply["Team"] = df_teams_ply.apply(
        lambda row: f"{row['Team']}: {100 * row['Frequency'] / df_teams_ply['Frequency'].sum():.2f} %", axis=1)
    fig_ply_teams = px.bar(df_teams_ply, x="Team", y="Frequency", title="Jersey Team Frequency")
    with st.expander("Jersey Teams"):
        st.plotly_chart(fig_ply_teams)

    df_u_players_divisions_ply = df_nhl_jerseys[["DivisionNameNHLConferences"]]
    df_divisions_ply = df_u_players_divisions_ply["DivisionNameNHLConferences"].value_counts().sort_values(
        ascending=False).reset_index()
    # df_divisions_ply = df_u_players_divisions_ply["DivisionNameNHLConferences"].value_counts().sort_index(ascending=False).reset_index()
    # df_countries_ply = df_nhl_jerseys["Nationality"].value_counts().sort_values(ascending=False).reset_index()
    df_divisions_ply.columns = ["Division", "Frequency"]
    # df_countries_ply["Country"] = df_countries_ply["Country"] + f"{100*df_countries_ply['Frequency']/df_countries_ply.shape[0]:.2f} %"
    df_divisions_ply["Division"] = df_divisions_ply.apply(
        lambda row: f"{row['Division']}: {100 * row['Frequency'] / df_divisions_ply['Frequency'].sum():.2f} %", axis=1)
    fig_ply_divisions = px.bar(df_divisions_ply, x="Division", y="Frequency", title="Jersey Team Frequency")
    with st.expander("Team Divisions"):
        st.plotly_chart(fig_ply_divisions)

    # df_u_players_conferences_ply = df_nhl_jerseys[["ConferenceName_x"]]
    # df_conferences_ply = df_u_players_conferences_ply["ConferenceName_x"].value_counts().sort_values(ascending=False).reset_index()
    # # df_divisions_ply = df_u_players_divisions_ply["DivisionNameNHLConferences"].value_counts().sort_index(ascending=False).reset_index()
    # # df_countries_ply = df_nhl_jerseys["Nationality"].value_counts().sort_values(ascending=False).reset_index()
    # df_conferences_ply.columns = ["Conference", "Frequency"]
    # # df_countries_ply["Country"] = df_countries_ply["Country"] + f"{100*df_countries_ply['Frequency']/df_countries_ply.shape[0]:.2f} %"
    # df_conferences_ply["Conference"] = df_conferences_ply.apply(lambda row: f"{row['Conference']}: {100*row['Frequency']/df_conferences_ply['Frequency'].sum():.2f} %", axis=1)
    # fig_ply_conferences = px.bar(df_conferences_ply, x="Conference", y="Frequency", title="Jersey Team Conference Frequency")
    # with st.gs_expander("Team Conferences"):
    #     st.plotly_chart(fig_ply_conferences)

    lst_data = [{
        "expLbl": "Team Conferences",
        "title": "Jersey Team Conference Frequency",
        "NHLJerseyKey": ["ConferenceName_x"],
        "newCols": {
            "x": "Conference",
            "y": "Frequency"
        },
        "df_u_vals": None,
        "df_vals": None,
        "fig": None,
        "exp": None,
        "s_asc": False
    }]
    for data in lst_data:
        data.update({
            "df_u_vals": df_nhl_jerseys[data["NHLJerseyKey"]]
        })
        data.update({
            "df_vals": data["df_u_vals"][data["NHLJerseyKey"][0]].value_counts().sort_values(
                ascending=data["s_asc"]).reset_index()
        })
        data["df_vals"].columns = list(data["newCols"].values())
        data["df_vals"][data["newCols"]["x"]] = data["df_vals"].apply(
            lambda row:
                f"{row[data['newCols']['x']]}: {100 * row[data['newCols']['y']] / data['df_vals'][data['newCols']['y']].sum():.2f} %",
            axis=1
        )
        data.update({
            "fig": px.bar(
                data["df_vals"],
                x=data["newCols"]["x"],
                y=data["newCols"]["y"],
                title=data["title"]
            )
        })
        data.update({
            "exp": st.expander(data["expLbl"])
        })

        with data["exp"]:
            st.plotly_chart(data["fig"])

    # TODO loop through some graphical stats
    # dict_

    # dict_dfs_team_stats = {
    #     "Divi"
    # }

    # Begin Widgets
    st.write("HERE")
    st.dataframe(df_nhl_jerseys)
    st.data_editor(
        df_nhl_jerseys,
        column_config={
            "birthCountryImage": st.column_config.ImageColumn(
                "Country Flag",
                width="large"
            ),
            "birthStateProvinceImage": st.column_config.ImageColumn(
                "State or Province Flag",
                width="large"
            )
        }
    )
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

    njp_gc = {

        # 0
        0: st.columns(3),
        1: st.divider(),
        2: st.columns(3),
        3: st.columns(3),
        4: st.columns(2),

        # 5
        5: st.columns(1),
        6: st.divider(),
        7: st.expander(label="NHL Data", expanded=False),
        8: st.divider(),
        9: st.columns(1)
    }

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

    with njp_gc[9][0]:
        lat_long_cols = ["latitude", "longitude"]
        df_lat_long: pd.DataFrame = df_nhl_jerseys[lat_long_cols].dropna(subset=lat_long_cols)
        df_lat_long.drop_duplicates(subset=lat_long_cols)
        st.map(df_lat_long)

    gs_expander = st.expander(
        label=f"General Stats"
    )

    # most popular number
    list_player_numbers = df_nhl_jerseys["Number"].values.tolist()
    count_occurrences = [(k, list_player_numbers.count(k)) for k in list_player_numbers if not pd.isna(k)]
    count_occurrences.sort(key=lambda tup: tup[1], reverse=True)

    # most popular first name
    list_player_first_name = df_nhl_jerseys["PlayerFirst"].values.tolist()
    count_occurrences_first_name = [(k, list_player_first_name.count(k)) for k in list_player_first_name if
                                    not pd.isna(k)]
    count_occurrences_first_name.sort(key=lambda tup: tup[1], reverse=True)

    # most popular last name
    list_player_last_name = df_nhl_jerseys["PlayerLast"].values.tolist()
    count_occurrences_last_name = [(k, list_player_last_name.count(k)) for k in list_player_last_name if not pd.isna(k)]
    count_occurrences_last_name.sort(key=lambda tup: tup[1], reverse=True)

    # most popular country
    list_player_country = df_nhl_jerseys["Nationality"].values.tolist()
    count_occurrences_country = [(k, list_player_country.count(k)) for k in list_player_country if not pd.isna(k)]
    count_occurrences_country.sort(key=lambda tup: tup[1], reverse=True)

    # most popular position
    list_player_position = df_nhl_jerseys["Position"].values.tolist()
    count_occurrences_position = [(k, list_player_position.count(k)) for k in list_player_position if not pd.isna(k)]
    count_occurrences_position.sort(key=lambda tup: tup[1], reverse=True)

    # most popular team
    list_player_team = df_nhl_jerseys["Team"].values.tolist()
    count_occurrences_team = [(k, list_player_team.count(k)) for k in list_player_team if not pd.isna(k)]
    count_occurrences_team.sort(key=lambda tup: tup[1], reverse=True)
    with gs_expander:
        stat_cols_0 = st.columns(3)
        stat_cols_1 = st.columns(3)
        with stat_cols_0[0]:
            card(
                "Most popular number:",
                f"# {int(count_occurrences[0][0])}"
            )
        with stat_cols_0[1]:
            card(
                "Most popular first name:",
                f"{count_occurrences_first_name[0][0]}"
            )
        with stat_cols_0[2]:
            card(
                "Most popular last name:",
                f"{count_occurrences_last_name[0][0]}"
            )
        with stat_cols_1[0]:
            card(
                "Most popular country:",
                f"{count_occurrences_country[0][0]}"
            )
        with stat_cols_1[1]:
            card(
                "Most popular position:",
                f"{count_occurrences_position[0][0]}"
            )
        with stat_cols_1[2]:
            card(
                "Most popular team:",
                f"{count_occurrences_team[0][0]}"
            )
    stat_cols_2 = st.columns(2)
    with stat_cols_2[0]:
        # gs_active_players_expander = st.expander("Active Players")
        with st.expander("Active Players"):
            card(
                "Total Active Players:",
                f"{total_active_players}"
            )
            st.dataframe(
                p_df_active_players[p_df_active_players.columns[:-1]],
                hide_index=True
            )
            # st.data_editor(
            #     p_df_active_players,
            #     column_config={
            #         "PlayerLast": st.column_config.ListColumn(
            #             "Player Last",
            #             width="medium"
            #         )
            #     }
            # )
    with stat_cols_2[1]:
        with st.expander("InActive Players"):
            card(
                "Total In-Active Players:",
                f"{total_inactive_players}"
            )
            st.dataframe(
                p_df_inactive_players[p_df_inactive_players.columns[:-1]],
                hide_index=True
            )

# Define nodes (events in the timeline)
nodes = [
    Node(id="Start", label="2024-01-01", size=15),
    Node(id="Milestone 1", label="2024-02-01", size=15),
    Node(id="Milestone 2", label="2024-03-01", size=15),
    Node(id="End", label="2024-04-01", size=15)
]

# Define edges (connections between events)
edges = [
    Edge(source="Start", target="Milestone 1", type="CURVE_SMOOTH"),
    Edge(source="Milestone 1", target="Milestone 2", type="CURVE_SMOOTH"),
    Edge(source="Milestone 2", target="End", type="CURVE_SMOOTH")
]

# Configure the timeline visualization
config = Config(width=700, height=400, directed=True)

# Display the timeline
agraph(nodes=nodes, edges=edges, config=config)

# data = {
#
# }
#
#
# # Sample DataFrame with timelines
# data = {
#     'Event': ['Event A', 'Event B', 'Event C', 'Event D'],
#     'Start Date': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01'],
#     'End Date': ['2024-01-10', '2024-02-10', '2024-03-10', '2024-04-10']
# }


# df_timeline_order_receive = pd.DataFrame(data)
cols_timeline_order_receive = ["OrderDate", "ReceiveDate", "JerseyID"]
df_timeline_order_receive = df_nhl_jerseys.loc[df_nhl_jerseys["CancelledOrder"] != 1][cols_timeline_order_receive]
st.dataframe(df_timeline_order_receive)
# df_timeline_order_receive["Event"] = df_timeline_order_receive.apply(lambda row: print(f"{row=}"))
# df_timeline_order_receive["Event"] = df_timeline_order_receive.apply(lambda row: print(f"{row=}"))
df_timeline_order_receive["Event"] = df_timeline_order_receive.apply(
    lambda row:
        ", ".join(map(str, df_nhl_jerseys.loc[
                df_nhl_jerseys["JerseyID"] == row["JerseyID"]][
                    ["Number", "PlayerFirst", "PlayerLast", "Team", "BrandName", "JerseyMake"]
        ].values)),
    axis=1
)
del df_timeline_order_receive["JerseyID"]
df_timeline_order_receive = df_timeline_order_receive.rename(
    columns={"OrderDate": "Start Date", "ReceiveDate": "End Date"})

df_timeline_order_receive['Start Date'] = pd.to_datetime(df_timeline_order_receive['Start Date'])
df_timeline_order_receive['End Date'] = pd.to_datetime(df_timeline_order_receive['End Date'])

# Create a Gantt-like timeline using Plotly
fig_timeline_order_receive = px.timeline(
    df_timeline_order_receive,
    x_start='Start Date',
    x_end='End Date',
    y='Event',
    title='Time Between Order to Receive date'
)

# Update layout to make it more readable
fig_timeline_order_receive.update_layout(xaxis_title="Date", yaxis_title="Order Date to Receive Date")

# Display in Streamlit
st.plotly_chart(fig_timeline_order_receive)


cols_timeline_order_open = ["OrderDate", "OpenDate", "JerseyID"]
df_timeline_order_open = df_nhl_jerseys.loc[df_nhl_jerseys["CancelledOrder"] != 1][cols_timeline_order_open]
st.dataframe(df_timeline_order_open)
# df_timeline_order_receive["Event"] = df_timeline_order_receive.apply(lambda row: print(f"{row=}"))
# df_timeline_order_receive["Event"] = df_timeline_order_receive.apply(lambda row: print(f"{row=}"))
df_timeline_order_open = df_timeline_order_open.rename(
    columns={"OrderDate": "Start Date", "OpenDate": "End Date"})

df_timeline_order_open['Start Date'] = pd.to_datetime(df_timeline_order_open['Start Date'])
df_timeline_order_open["Category"] = df_timeline_order_open.apply(lambda row: "Yet To Open" if pd.isna(row["End Date"]) else "Opened", axis=1)
df_timeline_order_open['End Date'] = pd.to_datetime(df_timeline_order_open['End Date']).fillna(pd.Timestamp.now())
df_timeline_order_open["DDiff"] = df_timeline_order_open.apply(lambda row: (row["End Date"] - row["Start Date"]).days, axis=1)
df_timeline_order_open["Event"] = df_timeline_order_open.apply(
    lambda row:
        ", ".join(map(str, df_nhl_jerseys.loc[
                df_nhl_jerseys["JerseyID"] == row["JerseyID"],
            ["Number", "PlayerFirst", "PlayerLast", "Team", "BrandName", "JerseyMake", "Colours"]
            ].iloc[0].values)) + " Dates between: " + str(row["DDiff"]),
    axis=1
)
del df_timeline_order_open["JerseyID"]
df_timeline_order_open.sort_values(
    by=["End Date", "DDiff"],
    inplace=True
)

# Create a Gantt-like timeline using Plotly
fig_timeline_order_open = px.timeline(
    df_timeline_order_open,
    x_start='Start Date',
    x_end='End Date',
    y='Event',
    title='Time Between Order to Open date',
    color='Category',
    color_discrete_map={
        'Yet To Open': 'red',
        'Medium': 'orange',
        'Opened': 'green'
    }
)

# Update layout to make it more readable
fig_timeline_order_open.update_layout(xaxis_title="Date", yaxis_title="Order Date to Open Date", height=1500)

# Display in Streamlit
st.plotly_chart(fig_timeline_order_open)


image_refs_htmls = [
    """<a target="_blank" href="https://icons8.com/icon/nz6Zx2vJbzRG/switzerland">Switzerland</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/WpPbz1F98VUy/denmark">Denmark</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/Dum84gAXfBP6/canada">Canada</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/OyqucOGoByl9/germany">Germany</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/NDrD4CYtRBwQ/georgia-flag">Georgia Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/XTantlC-UA3q/texas-flag">Texas Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/Vos-tGVy-9iR/california-flag">California Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/vnYmQQ4X0JsA/colorado-flag">Colorado Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/kbSQX7XfBI5h/hawaii-flag">Hawaii Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/s1-q7JfG-sh7/florida-flag">Florida Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/s1-q7JfG-sh7/florida-flag">Florida Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/FXgk2XOgWT7M/alabama-flag">Alabama Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/FXgk2XOgWT7M/alabama-flag">Alabama Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/GAE6WZTPKYO1/virginia-flag">Virginia Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/J5GxnkQaXFtb/washington-flag">Washington Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/U-ALwM5OpR7S/massachusetts-flag">Massachusetts Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/TKorkvgkXnqa/nevada-flag">Nevada Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/44fY7vWjhjiH/ohio-flag">Ohio Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/X-lScXq7uV90/oregon-flag">Oregon Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/Aib05gDheyNf/alaska-flag">Alaska Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/jQPaxKFfArNp/arkansas-flag">Arkansas Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/Y23SDXCP-XCb/wisconsin-flag">Wisconsin Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/IyhPFm2AXnFh/kentucky-flag">Kentucky Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/AGO0jdY-bkmt/indiana-flag">Indiana Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/jZHsrwgZA1OV/minnesota-flag">Minnesota Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/VoWoTmq3C4SB/pennsylvania-flag">Pennsylvania Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/zpkl1Hbgzf7W/idaho-flag">Idaho Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/rw08FzGx83AK/mississippi-flag">Mississippi Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/l39NAYp3jpyq/michigan-flag">Michigan Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/hMYv_tfME4iE/missouri-flag">Missouri Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/5I0q-mn8NKdv/oklahoma-flag">Oklahoma Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/PiDPd3RIB-aI/montana-flag">Montana Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/fcpZguwMtVSs/delaware-flag">Delaware Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/HtXyBhiNrojW/iowa-flag">Iowa Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/drFlVZjrpy3u/maine-flag">Maine Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/hYXb8jExIHVj/connecticut-flag">Connecticut Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/0u4UrZ-kAH9O/kansas-flag">Kansas Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/INQZPwNNw3L8/sweden">Sweden</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/VLKK6MVJuoXO/slovenia">Slovenia</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/Halaubi1vvya/united-states-minor-outlying-islands">United States Minor Outlying Islands</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15532/usa">USA</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/c_e0JWgTsNNx/illinois-flag">Illinois Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/mxUcnMuNAOSp/lousiana-flag">Lousiana Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/9FKO1QSdmhdH/maryland-flag">Maryland Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/fVBKgBFYEsAS/nebraska-flag">Nebraska Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/ViZFYL8OnHoI/new-hampshire-flag">New Hampshire Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/6wBSXgD-30f4/new-jersey-flag">New Jersey Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/uKYT_MT6Af1M/new-mexico-flag">New Mexico Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/PHJN-9UdTYcq/new-york-flag">New York Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/h4spXYDZr-ez/north-carolina-flag">North Carolina Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/HG94AoyH021p/north-dakota-flag">North Dakota Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/bEdKRwxEQ3bR/rhode-island-flag">Rhode Island Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/lvMLadGC2uIq/south-carolina-flag">South Carolina Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/LGWMf_LvV35D/south-dakota-flag">South Dakota Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/DoreHlNCT-va/utah-flag">Utah Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/y1Sr8HgfqBOL/vermont-flag">Vermont Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/TKwBVwV4ffLU/west-virginia-flag">West Virginia Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/kZS0xbjHYerT/wyoming-flag">Wyoming Flag</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15526/switzerland">Switzerland</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15527/sweden">Sweden</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/17966/slovenia">Slovenia</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/17965/slovakia">Slovakia</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15544/norway">Norway</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15536/netherlands">Netherlands</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15524/latvia">Latvia</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15534/great-britain">Great Britain</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/22435/japan">Japan</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15511/finland">Finland</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15497/france">France</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15502/germany">Germany</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15513/czech-republic">Czech Republic</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15520/denmark">Denmark</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15512/canada">Canada</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15506/austria">Austria</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>""",
    """<a target="_blank" href="https://icons8.com/icon/15528/russian-federation">Russian Federation</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>"""
]

with st.expander("References:"):
    for link in image_refs_htmls:
        st.write(link, unsafe_allow_html=True)

shown_opened_group_change = False
for i, row in df_nhl_jerseys.sort_values(by="OpenDate", ascending=False).iterrows():
    if all([
        i > 0,
        pd.isna(row["OpenDate"]),
        not shown_opened_group_change,
        i < (df_nhl_jerseys.shape[0] - 1)
    ]):
        shown_opened_group_change = True
        st.divider()
    st.write(f"{row['PlayerLast']}, {row['PlayerFirst']}, {row['Team']}, {row['BrandName']}, {row['JerseyMake']}, {row['Colours']}")

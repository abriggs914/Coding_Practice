import os
import time
import geocoder
from geopy.geocoders import Nominatim


import pandas as pd
import streamlit as st
import pydeck as pdk


app_title: str = "League"

path_excel_team_arenas = r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHLTeamArenas2425.xlsx"
path_excel_game_predictions = r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions.xlsx"
user_agent_name = "Get Loc"
k_geo_loc = "geo_loc"

if not os.path.exists(path_excel_team_arenas):
    path_excel_team_arenas = path_excel_team_arenas.replace(r"\abriggs\Documents", r"\abrig\Documents")
if not os.path.exists(path_excel_game_predictions):
    path_excel_game_predictions = path_excel_game_predictions.replace(r"\abriggs\Documents", r"\abrig\Documents")


@st.cache_data(ttl=None, show_spinner=True)
def load_excel_team_arenas():
    return pd.read_excel(path_excel_team_arenas)


@st.cache_data(ttl=None, show_spinner=True)
def load_excel_game_predicitons():
    df = pd.read_excel(path_excel_game_predictions, skiprows=1)
    cols = [c for c in df.columns if not c.lower().startswith("unnamed:")]
    return df[cols]


@st.cache_data(ttl=None, show_spinner=True)
def coords_to_address(coords_str: str):
    try:
        geo_loc = st.session_state.setdefault(k_geo_loc, Nominatim(user_agent=user_agent_name))
        return geo_loc.reverse(coords_str)
    except Exception:
        return None
    

def coords_to_lat_lon(coords_str: str):
    try:
        # print(f"{coords_str=}")
        location = coords_to_address(coords_str)
        # print(f"{location=}")
        lat, lon = location.raw["lat"], location.raw["lon"]
        # print(f"{lat=}, {lon=}")
        return float(lat), float(lon)
    except Exception:
        return None, None


st.set_page_config(page_title=app_title, layout="wide")


df_team_arenas = load_excel_team_arenas()
df_game_predictions = load_excel_game_predicitons()

df_team_arenas[["Lat", "Lon"]] = df_team_arenas.apply(
    lambda row: coords_to_lat_lon(row["Coordinates"]),
    result_type="expand",
    axis=1
)

df_combined = df_game_predictions.merge(
    df_team_arenas,
    how="inner",
    left_on="AwayTeam",
    right_on="TeamAcronym"
).merge(
    df_team_arenas,
    how="inner",
    left_on="HomeTeam",
    right_on="TeamAcronym",
    suffixes=["_away", "_home"]
)

lst_teams = sorted(df_combined["HomeTeam"].dropna().unique().tolist())

st.write("Combined:")
stdf_combined = st.dataframe(
    data=df_combined,
    hide_index=True
)

st.write("Team Arenas:")
stdf_team_arenas = st.dataframe(
    data=df_team_arenas,
    hide_index=True
)

st.write("Game Predictions:")
stdf_game_predictions = st.dataframe(
    data=df_game_predictions,
    hide_index=True
)

st.map(
    data=df_team_arenas[["Lat", "Lon"]].rename(columns={"Lat": "LAT", "Lon": "LON"})
)

k_selectbox_team_choice = "selectbox_team_choice"
selectbox_team_choice = st.selectbox(
    label="Select a Team",
    key=f"k_{k_selectbox_team_choice}",
    options=lst_teams
)

if selectbox_team_choice:
    df_team_choice = df_combined.loc[
        (df_combined["HomeTeam"] == selectbox_team_choice)
        | (df_combined["AwayTeam"] == selectbox_team_choice)
    ]
    stdf_team_choice = st.dataframe(
        data=df_team_choice,
        hide_index=True
    )

    data = df_team_choice.rename(columns={"Lat_home": "latitude", "Lon_home": "longitude"})
    map_container = st.empty()

    initial_path_pos = pd.DataFrame(data.iloc[:1][["latitude", "longitude"]])

    st.write("initial_path_pos")
    st.write(initial_path_pos)

    # Animate object moving along the path
    # for i in range(len(data)):
    for i in range(10):

        # view_state = pdk.ViewState(
        #     latitude=data.iloc[i]["Lat_home"],
        #     longitude=data.iloc[i]["Lon_home"],
        #     zoom=8,
        #     pitch=0
        # )
        # Extract the current location
        current_location = data.iloc[i][["latitude", "longitude"]]

        # Define ScatterplotLayer for current location
        layer_point = pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame([current_location]),  # Single point at current location
            get_position=["longitude", "latitude"],
            get_color=[255, 0, 0, 200],  # Red color
            get_radius=10000,  # Adjust size of the moving point
        )
        # print(f"ILOC")
        # print(data.iloc[:i])
        # print(data.iloc[:i].columns)
        # print(f"END ILOC")
        df_path = pd.concat([
            initial_path_pos,
            pd.DataFrame(data.iloc[:i][["latitude", "longitude"]])
        ]).reset_index(drop=True)
        df_path["path"] = df_path.apply(
            lambda row: (row['latitude'], row["longitude"]),
            axis=1
        )

        df_path = pd.DataFrame({"path": [data.iloc[:i][["latitude", "longitude"]].values.tolist()]})

        st.write(data.iloc[:i][["latitude", "longitude"]].values.tolist())
        print(data.iloc[:i][["latitude", "longitude"]].values.tolist())

        print(f"df_path")
        print(df_path)
        layer_line = pdk.Layer(
            "PathLayer",
            data=data.iloc[:i][["latitude", "longitude"]].values.tolist(),
            # data=df_path,
            # # get_position=["longitude", "latitude"],
            get_path="-",
            get_color=[0, 0, 255, 160],  # Blue path
            width_scale=2000
        )

        # Define Pydeck map with updated position
        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            # initial_view_state=view_state,
            layers=[layer_point, layer_line]
        )

        # Update the map in Streamlit
        map_container.pydeck_chart(deck)

        # Wait before updating next position
        time.sleep(1)  # Adjust for animation speed
        print(f"{current_location=}")
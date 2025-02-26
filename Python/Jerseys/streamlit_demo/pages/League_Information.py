import os
import time
import geocoder
from geopy.geocoders import Nominatim
from typing import Literal

import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk


app_title: str = "League"

path_excel_team_arenas = r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHLTeamArenas2425.xlsx"
path_excel_game_predictions = r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions.xlsx"
user_agent_name = "Get Loc"
k_geo_loc = "geo_loc"

s_p_frame = 0.95
radius_0_location = 10000
radius_1_location = 18000
width_scale_travel_path = 6
width_travel_path = 800
height_deck_map = 800

# basically St. Louis, Missouri
na_view_state = pdk.ViewState(
    latitude=38.6268005,
    longitude=-90.20261996009455,
    zoom=3,
    pitch=0
)

k_state_anim_started: str = "anim_started"
k_animation_run = "animation_run"   # session_state key storing state_anim_____ values
state_anim_idle: str = "idle"       # before running animation
state_anim_run: str = "run"         # running animation
state_anim_pause: str = "pause"     # a phase suring animation
state_anim_end: str = "end"         # the end of the animation


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
    

def calc_path(location_0: list[float], location_1: list[float], step: int = 0, order: Literal["latlon", "lonlat"] = "latlon"):
    """
    Generates intermediate points between two geographic coordinates.

    Args:
        location_0 (list[float]): Coordinates of the starting point.
        location_1 (list[float]): Coordinates of the ending point.
        step (int): Number of steps (including start and end).
        order (str): "latlon" (default) for [latitude, longitude], 
                     "lonlat" for [longitude, latitude] (GeoJSON format).

    Returns:
        list: A list of tuples representing the path, following the specified order.
    """
    if (not isinstance(location_0, (list, tuple))) or (len(location_0) != 2):
        raise ValueError(f"param 'location_0' must be a list of coordinates representing latitude and longitude, got: ({location_0=})")
    if (not isinstance(location_1, (list, tuple))) or (len(location_1) != 2):
        raise ValueError(f"param 'location_1' must be a list of coordinates representing latitude and longitude, got: ({location_1=})")
    if step < 3:
        return [location_0, location_1]
    
    # Extract latitudes and longitudes
    if order == "latlon":
        lat_0, lon_0 = location_0
        lat_1, lon_1 = location_1
    elif order == "lonlat":  # GeoJSON format
        lon_0, lat_0 = location_0
        lon_1, lat_1 = location_1
    else:
        raise ValueError(f"Invalid 'order' argument: {order}. Use 'latlon' or 'lonlat'.")

    # Generate linearly spaced values for latitudes and longitudes
    lats = np.linspace(lat_0, lat_1, num=step)
    lons = np.linspace(lon_0, lon_1, num=step)
    
    # Return list of tuples in the specified order
    return list(zip(lons, lats)) if order == "lonlat" else list(zip(lats, lons))
    

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

control_container = st.container(border=1, height=450)
content_container = st.container()

k_selectbox_team_choice = "selectbox_team_choice"
selectbox_team_choice = control_container.selectbox(
    label="Select a Team",
    key=f"k_{k_selectbox_team_choice}",
    options=lst_teams
)

animation_started = st.session_state.setdefault(k_state_anim_started, -1) >= 0
default_state_anim = state_anim_pause if animation_started else state_anim_idle

st.write(f"{selectbox_team_choice=}")
st.write(f"{st.session_state.get(k_animation_run)=}")
st.write(f"{st.session_state.get(k_state_anim_started)=}")
st.write(f"{animation_started=}")
st.write(f"{default_state_anim=}")

if selectbox_team_choice:
    df_team_choice = df_combined.loc[
        (df_combined["HomeTeam"] == selectbox_team_choice)
        | (df_combined["AwayTeam"] == selectbox_team_choice)
    ]
    stdf_team_choice = control_container.dataframe(
        data=df_team_choice,
        hide_index=True
        ,
        height=225
    )
    starts_at_home = df_team_choice.iloc[0]["HomeTeam"] == selectbox_team_choice

    data = df_team_choice.rename(columns={"Lat_home": "latitude", "Lon_home": "longitude"})

    # st.write("initial_path_pos")
    # st.write(initial_path_pos)

    # CRITICAL TO USE [LONGITUDE, LATITUDE] in this order, see geoJSON for more details.
    lat_long = ["longitude", "latitude"]
    if starts_at_home:
        initial_path_pos = pd.DataFrame(data.iloc[:1][lat_long])
    else:
        initial_path_pos = pd.DataFrame(data.loc[data["HomeTeam"] == selectbox_team_choice].iloc[:1][lat_long])

    view_state = pdk.ViewState(
        latitude=initial_path_pos.iloc[0]["latitude"],  # Center near Downtown SF
        longitude=initial_path_pos.iloc[0]["longitude"],
        zoom=4,  # Adjust for a closer view
        pitch=0
    )    

    if st.session_state.setdefault(k_animation_run, state_anim_idle) == state_anim_run:
        if content_container.button(
            label="pause"
        ):
            st.session_state.update({k_animation_run: state_anim_pause})
            st.rerun()

    if control_container.button(
        label="Start Travel Animation"
    ):
        st.session_state.update({
            k_animation_run: state_anim_run,
            k_state_anim_started: 0
        })
        st.rerun()
    if animation_started:
        if control_container.button(
            label="Resume Travel Animation"
        ):
            st.session_state.update({
                k_animation_run: state_anim_run
            })
            st.rerun()
    
    if st.session_state.setdefault(k_animation_run, default_state_anim) == state_anim_run:
        st.write("-A")
        data_container = content_container.container(height=100)
        data_text = data_container.empty()
        map_container = content_container.empty()

        progress_travel = data_container.progress(value=0)
        last_location = None
        l_data = len(data)
        distance_traveled = 0
        i = st.session_state.get(k_state_anim_started, 0)
        j = 0
        while i in range(l_data):
            p_travel = (i+1)/l_data
            progress_travel.progress(value=p_travel, text=f"{100*p_travel:.2f} % - {(l_data - (i + 1)) * s_p_frame:.2f}s left")

            df_i = data.iloc[i]
            game_day = df_i["GameDate"]
            current_location = df_i[lat_long]

            layer_point = pdk.Layer(
                "ScatterplotLayer",
                data=pd.DataFrame([current_location]),
                get_position=lat_long,
                get_color=[255, 0, 0, 200],
                get_radius=radius_0_location
            )

            df_path = pd.concat([
                initial_path_pos,
                pd.DataFrame(data.iloc[:i][lat_long])
            ]).reset_index(drop=True)
            df_path["path"] = df_path.apply(
                lambda row: (row['longitude'], row["latitude"]),
                axis=1
            )

            df_path = pd.DataFrame({"path": [data.iloc[:i+1][lat_long].values.tolist()]})
            df_path[lat_long] = current_location[lat_long]

            if (not starts_at_home) and ((i * j) == 0):
                dt = geocoder.distance(
                    [initial_path_pos.iloc[0]["latitude"], initial_path_pos.iloc[0]["longitude"]],
                    [df_path.iloc[0]["latitude"], df_path.iloc[0]["longitude"]]
                )
                distance_traveled += dt
                # st.write(f"{i=}, {dt=}, {distance_traveled=}")
            else:
                if (i * j) > 0:    
                    dt = geocoder.distance(
                        [df_path.iloc[0]["latitude"], df_path.iloc[0]["longitude"]],
                        [last_location["latitude"], last_location["longitude"]]
                    )
                    # st.write(f"{i=}, {dt=}, {distance_traveled=}")
                    distance_traveled += dt

            layer_line = pdk.Layer(
                "PathLayer",
                data = df_path,
                get_path="path",
                get_color=[0, 0, 255, 160],
                width_scale=width_scale_travel_path,
                get_width=width_travel_path
            )

            df_path_direct = pd.DataFrame([{
                "path": calc_path(
                    location_0=initial_path_pos.iloc[0][lat_long].values.tolist(),
                    location_1=current_location[lat_long].values.tolist(),
                    order="lonlat"
                )
            }])
            layer_line_direct = pdk.Layer(
                "PathLayer",
                data = df_path_direct,
                get_path="path",
                get_color=[0, 255, 0, 160],
                width_scale=width_scale_travel_path,
                get_width=width_travel_path
            )

            deck = pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=na_view_state,
                layers=[layer_point, layer_line, layer_line_direct],
                height=height_deck_map
            )

            data_text.write(f"{game_day:%x %X} -- Total Distance Traveled: {distance_traveled} KM")
            map_container.pydeck_chart(deck)

            # if st.session_state.setdefault(k_animation_run, default_state_anim) in (state_anim_pause, state_anim_end, state_anim_idle):
                # i = l_data + 1

            time.sleep(s_p_frame)
            i += 1
            j += 1
            st.session_state.update({k_state_anim_started: i})
            last_location = current_location

        st.session_state.update({
            k_animation_run: state_anim_end
        })
    elif animation_started and (st.session_state.get(k_animation_run) == state_anim_pause):
        st.write("-B")
        i = st.session_state.get(k_state_anim_started, 0)
        df_i = data.iloc[i]
        game_day = df_i["GameDate"]
        current_location: pd.Series = df_i[lat_long]
        layer_point = pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame([current_location]),
            get_position=lat_long,
            get_color=[255, 0, 0, 200],
            get_radius=radius_0_location
        )

        df_path = pd.concat([
            initial_path_pos,
            pd.DataFrame(data.iloc[:i][lat_long])
        ]).reset_index(drop=True)
        df_path["path"] = df_path.apply(
            lambda row: (row['longitude'], row["latitude"]),
            axis=1
        )

        df_path = pd.DataFrame({"path": [data.iloc[:i+1][lat_long].values.tolist()]})
        df_path[lat_long] = current_location[lat_long]
        layer_line = pdk.Layer(
            "PathLayer",
            data = df_path,
            get_path="path",
            get_color=[0, 0, 255, 160],
            width_scale=width_scale_travel_path,
            get_width=width_travel_path
        )

        df_path_direct = pd.DataFrame([{
            "path": calc_path(
                location_0=initial_path_pos.iloc[0][lat_long].values.tolist(),
                location_1=current_location[lat_long].values.tolist(),
                order="lonlat"
            )
        }])
        layer_line_direct = pdk.Layer(
            "PathLayer",
            data = df_path_direct,
            get_path="path",
            get_color=[0, 255, 0, 160],
            width_scale=width_scale_travel_path,
            get_width=width_travel_path
        )

        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=na_view_state,
            layers=[layer_point, layer_line, layer_line_direct],
            height=height_deck_map
        )
        content_container.pydeck_chart(deck)
    else:
        # Just show the home location of the selected team
        st.write("-C")
        layer_point = pdk.Layer(
            "ScatterplotLayer",
            data=initial_path_pos,
            get_position=lat_long,
            get_color=[255, 0, 0, 200],
            get_radius=radius_1_location,
        )
        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=[layer_point],
            height=height_deck_map
        )
        content_container.pydeck_chart(deck)




# import os
# import time
# import geocoder
# from geopy.geocoders import Nominatim


# import pandas as pd
# import streamlit as st
# import pydeck as pdk


# app_title: str = "League"

# path_excel_team_arenas = r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHLTeamArenas2425.xlsx"
# path_excel_game_predictions = r"C:\Users\abriggs\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions.xlsx"
# user_agent_name = "Get Loc"
# k_geo_loc = "geo_loc"

# s_p_frame = 0.95
# radius_0_location = 10000
# radius_1_location = 18000
# width_scale_travel_path = 6
# width_travel_path = 800
# height_deck_map = 800

# # basically St. Louis, Missouri
# na_view_state = pdk.ViewState(
#     latitude=38.6268005,
#     longitude=-90.20261996009455,
#     zoom=3,
#     pitch=0
# )


# if not os.path.exists(path_excel_team_arenas):
#     path_excel_team_arenas = path_excel_team_arenas.replace(r"\abriggs\Documents", r"\abrig\Documents")
# if not os.path.exists(path_excel_game_predictions):
#     path_excel_game_predictions = path_excel_game_predictions.replace(r"\abriggs\Documents", r"\abrig\Documents")


# @st.cache_data(ttl=None, show_spinner=True)
# def load_excel_team_arenas():
#     return pd.read_excel(path_excel_team_arenas)


# @st.cache_data(ttl=None, show_spinner=True)
# def load_excel_game_predicitons():
#     df = pd.read_excel(path_excel_game_predictions, skiprows=1)
#     cols = [c for c in df.columns if not c.lower().startswith("unnamed:")]
#     return df[cols]


# @st.cache_data(ttl=None, show_spinner=True)
# def coords_to_address(coords_str: str):
#     try:
#         geo_loc = st.session_state.setdefault(k_geo_loc, Nominatim(user_agent=user_agent_name))
#         return geo_loc.reverse(coords_str)
#     except Exception:
#         return None
    

# def coords_to_lat_lon(coords_str: str):
#     try:
#         # print(f"{coords_str=}")
#         location = coords_to_address(coords_str)
#         # print(f"{location=}")
#         lat, lon = location.raw["lat"], location.raw["lon"]
#         # print(f"{lat=}, {lon=}")
#         return float(lat), float(lon)
#     except Exception:
#         return None, None


# st.set_page_config(page_title=app_title, layout="wide")


# df_team_arenas = load_excel_team_arenas()
# df_game_predictions = load_excel_game_predicitons()

# df_team_arenas[["Lat", "Lon"]] = df_team_arenas.apply(
#     lambda row: coords_to_lat_lon(row["Coordinates"]),
#     result_type="expand",
#     axis=1
# )

# df_combined = df_game_predictions.merge(
#     df_team_arenas,
#     how="inner",
#     left_on="AwayTeam",
#     right_on="TeamAcronym"
# ).merge(
#     df_team_arenas,
#     how="inner",
#     left_on="HomeTeam",
#     right_on="TeamAcronym",
#     suffixes=["_away", "_home"]
# )

# lst_teams = sorted(df_combined["HomeTeam"].dropna().unique().tolist())

# st.write("Combined:")
# stdf_combined = st.dataframe(
#     data=df_combined,
#     hide_index=True
# )

# st.write("Team Arenas:")
# stdf_team_arenas = st.dataframe(
#     data=df_team_arenas,
#     hide_index=True
# )

# st.write("Game Predictions:")
# stdf_game_predictions = st.dataframe(
#     data=df_game_predictions,
#     hide_index=True
# )

# st.map(
#     data=df_team_arenas[["Lat", "Lon"]].rename(columns={"Lat": "LAT", "Lon": "LON"})
# )

# control_container = st.container(border=1, height=400)
# content_container = st.container()

# k_selectbox_team_choice = "selectbox_team_choice"
# selectbox_team_choice = control_container.selectbox(
#     label="Select a Team",
#     key=f"k_{k_selectbox_team_choice}",
#     options=lst_teams
# )

# if selectbox_team_choice:
#     df_team_choice = df_combined.loc[
#         (df_combined["HomeTeam"] == selectbox_team_choice)
#         | (df_combined["AwayTeam"] == selectbox_team_choice)
#     ]
#     stdf_team_choice = control_container.dataframe(
#         data=df_team_choice,
#         hide_index=True
#     )
#     starts_at_home = df_team_choice.iloc[0]["HomeTeam"] == selectbox_team_choice

#     data = df_team_choice.rename(columns={"Lat_home": "latitude", "Lon_home": "longitude"})

#     # st.write("initial_path_pos")
#     # st.write(initial_path_pos)

#     # CRITICAL TO USE [LONGITUDE, LATITUDE] in this order, see geoJSON for more details.
#     lat_long = ["longitude", "latitude"]
#     if starts_at_home:
#         initial_path_pos = pd.DataFrame(data.iloc[:1][lat_long])
#     else:
#         initial_path_pos = pd.DataFrame(data.loc[data["HomeTeam"] == selectbox_team_choice].iloc[:1][lat_long])

#     view_state = pdk.ViewState(
#         latitude=initial_path_pos.iloc[0]["latitude"],  # Center near Downtown SF
#         longitude=initial_path_pos.iloc[0]["longitude"],
#         zoom=4,  # Adjust for a closer view
#         pitch=0
#     )

#     if control_container.button(
#         label="Animate Travel"
#     ):
    
#         data_container = content_container.container(height=100)
#         map_container = content_container.empty()

#         # Animate object moving along the path
#         progress_travel = data_container.progress(value=0)
#         last_location = None
#         l_data = len(data)
#         distance_traveled = 0
#         i = 0
#         while i in range(l_data):
#             if i >= 7:
#                 break
#             p_travel = (i+1)/l_data
#             progress_travel.progress(value=p_travel, text=f"{100*p_travel:.2f} % - {(l_data - (i + 1)) * s_p_frame:.2f}s left")
#             # for i in range(10):

#             # view_state = pdk.ViewState(
#             #     latitude=data.iloc[i]["Lat_home"],
#             #     longitude=data.iloc[i]["Lon_home"],
#             #     zoom=8,
#             #     pitch=0
#             # )
#             # Extract the current location
#             df_i = data.iloc[i]
#             game_day = df_i["GameDate"]
#             current_location = df_i[lat_long]

#             # Define ScatterplotLayer for current location
#             layer_point = pdk.Layer(
#                 "ScatterplotLayer",
#                 data=pd.DataFrame([current_location]),  # Single point at current location
#                 get_position=lat_long,
#                 get_color=[255, 0, 0, 200],  # Red color
#                 get_radius=radius_0_location,  # Adjust size of the moving point
#             )
#             # print(f"ILOC")
#             # print(data.iloc[:i])
#             # print(data.iloc[:i].columns)
#             # print(f"END ILOC")
#             df_path = pd.concat([
#                 initial_path_pos,
#                 pd.DataFrame(data.iloc[:i][lat_long])
#             ]).reset_index(drop=True)
#             df_path["path"] = df_path.apply(
#                 lambda row: (row['longitude'], row["latitude"]),
#                 axis=1
#             )

#             # df_path = pd.DataFrame({"path": [data.iloc[:i+1][lat_long].values.tolist()]})
#             df_path = pd.DataFrame({"path": [data.iloc[:i+1][lat_long].values.tolist()]})
#             df_path[lat_long] = current_location[lat_long]
#             # st.write(f"{i=}")
#             # st.write(df_path)
#             # st.write(last_location)
#             if (not starts_at_home) and (i == 0):
#                 dt = geocoder.distance(
#                     [initial_path_pos.iloc[0]["latitude"], initial_path_pos.iloc[0]["longitude"]],
#                     [df_path.iloc[0]["latitude"], df_path.iloc[0]["longitude"]]
#                 )
#                 distance_traveled += dt
#                 st.write(f"{i=}, {dt=}, {distance_traveled=}")
#             else:
#                 if i > 0:    
#                     dt = geocoder.distance(
#                         [df_path.iloc[0]["latitude"], df_path.iloc[0]["longitude"]],
#                         [last_location["latitude"], last_location["longitude"]]
#                     )
#                     st.write(f"{i=}, {dt=}, {distance_traveled=}")
#                     distance_traveled += dt

#             # st.write(data.iloc[:i][lat_long].values.tolist())
#             # # print(data.iloc[:i][lat_long].values.tolist())

#             # # print(f"df_path")
#             # # print(df_path)
#             # # st.write(df_path)
#             layer_line = pdk.Layer(
#                 "PathLayer",
#                 data = df_path,
#                 get_path="path",
#                 get_color=[0, 0, 255, 160],  # Blue path
#                 width_scale=width_scale_travel_path,
#                 get_width=width_travel_path  # Ensure the path is visible
#             )

#             # Define Pydeck map with updated position
#             deck = pdk.Deck(
#                 map_style="mapbox://styles/mapbox/light-v9",
#                 # initial_view_state=view_state,
#                 initial_view_state=na_view_state,
#                 layers=[layer_point, layer_line],
#                 height=height_deck_map
#             )

#             # Update the map in Streamlit
#             data_container.write(f"{game_day:%x %X} -- Total Distance Traveled: {distance_traveled} KM")
#             map_container.pydeck_chart(deck)

#             if data_container.button(
#                 label="stop",
#                 key=f"k_btn_stop_animation_{i}"
#             ):
#                 i = l_data + 1 

#             # Wait before updating next position
#             time.sleep(s_p_frame)  # Adjust for animation speed
#             i += 1
#             last_location = current_location
#             # print(f"{current_location=}")

#         # p_data = [
#         #     {"name": "Path 1", "path": [[-122.42, 37.77], [-122.41, 37.78], [-122.40, 37.79]]},
#         #     {"name": "Path 2", "path": [[-122.39, 37.80], [-122.38, 37.81], [-122.37, 37.82]]}
#         # ]
#         # p1_data = pd.DataFrame(p_data)
#         # # p_data = [
#         # #     {"name": "Path 1", "path": [[37.77, -122.42], [37.78, -122.41], [37.79, -122.40]]},
#         # #     {"name": "Path 2", "path": [[37.80, -122.39], [37.81, -122.38], [37.82, -122.37]]}
#         # # ]
#         # # p_data = pd.DataFrame({
#         # #     "name": ["Path 1", "Path 2"],
#         # #     "path": [
#         # #         [[37.77, -122.42], [37.78, -122.41], [37.79, -122.40]],  # Path 1
#         # #         [[37.80, -122.39], [37.81, -122.38], [37.82, -122.37]]   # Path 2
#         # #     ]
#         # # })
#         # st.write("p_data")
#         # st.write(p_data)
#         # st.write("data.iloc[:1]")
#         # st.write(data.iloc[:1])
#         # t0_view_state = pdk.ViewState(
#         #     latitude=37.78,  # Center near Downtown SF
#         #     longitude=-122.41,
#         #     zoom=12,  # Adjust for a closer view
#         #     pitch=0
#         # )
#         # t0_layer_point = pdk.Layer(
#         #     "ScatterplotLayer",
#         #     data=data.iloc[:1],  # Single point at current location
#         #     get_position=["longitude", "latitude"],
#         #     get_color=[255, 0, 0, 200],  # Red color
#         #     get_radius=10000,  # Adjust size of the moving point
#         # )
#         # t0_layer_line = pdk.Layer(
#         #     "PathLayer",
#         #     # data=data.iloc[:i][["latitude", "longitude"]].values.tolist(),
#         #     data=p_data,
#         #     # data=p_data,
#         #     # data=df_path,
#         #     # # get_position=["longitude", "latitude"],
#         #     get_path="path",
#         #     get_color=[0, 0, 255, 160],  # Blue path
#         #     width_scale=20,
#         #     get_width=2000,  # Ensure the path is visible
#         #     pickable=True
#         # )
#         # st.write(t0_layer_line)
#         # t1_layer_line = pdk.Layer(
#         #     "PathLayer",
#         #     # data=data.iloc[:i][["latitude", "longitude"]].values.tolist(),
#         #     data=p_data,
#         #     # data=p_data,
#         #     # data=df_path,
#         #     # # get_position=["longitude", "latitude"],
#         #     get_path="path",
#         #     get_color=[0, 255, 0, 160],  # Blue path
#         #     width_scale=8,
#         #     get_width=1200,  # Ensure the path is visible
#         #     pickable=True
#         # )
#         # st.write(t1_layer_line)

#         # # Define Pydeck map with updated position
#         # t0_deck = pdk.Deck(
#         #     map_style="mapbox://styles/mapbox/light-v9",
#         #     # initial_view_state=view_state,
#         #     initial_view_state=t0_view_state,
#         #     layers=[t0_layer_point, t0_layer_line, t1_layer_line],
#         #     tooltip={"text": "{name}"},
#         # )

#         # st.pydeck_chart(t0_deck)
#     else:
#         layer_point = pdk.Layer(
#             "ScatterplotLayer",
#             data=initial_path_pos,  # Single point at current location
#             get_position=lat_long,
#             get_color=[255, 0, 0, 200],  # Red color
#             get_radius=radius_1_location,  # Adjust size of the moving point
#         )
#         deck = pdk.Deck(
#             map_style="mapbox://styles/mapbox/light-v9",
#             initial_view_state=view_state,
#             layers=[layer_point],
#             height=height_deck_map
#         )

#         # Update the map in Streamlit
#         content_container.pydeck_chart(deck)
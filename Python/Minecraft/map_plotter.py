import math
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


places = {
    "Bed": (146, 58, 0, "<"),
    "Chicken": (107, 65, -11, "C"),
    "Train Departure": (106, 96, -19, "D"),
    "Train Arrival": (113, 96, -20, "H"),
    "Nether Portal": (128, 89, 11, "S"),
    "Resource Hut": (-138, 64, 146, "R"),
    "Natural Cave": (-184, 89, 393, "."),
    "Centre of Town 1": (556, 71, 28, "1"),
    "Birch Forest": (750, 64, -30, "B"),
    "Rest Stop": (920, 64, -93, "R"),
    "Centre of Town 2": (1065, 64, -304, "2"),
    "Amphitheatre": (960, 79, -310, "A"),
    "Centre of Town 3": (640, 66, -280, "3"),
    "Glacier": (720, 62, -560, "G"),
    "Coral Reef": (400, 62, -455, "O"),
    "Tower": (100, 96, 160, "T"),
    "Zombie Spawner 1": (165, 16, 38, "Z"),
    
    "Ocelot": (562, 61, 7, "L"),
    "Tunnel Network": (600, 61, 60, "K"),
    "Pit of Doom": (541, 63, 89, "J"),
    "Train Tunnel": (483, 64, 40, "G"),
    "Spider Spawner 1": (611, 18, 76, "F"),
    "Zombie Spawner 2": (536, 31, 186, "M"),
    "Spider Spawner 2": (592, 24, 215, "N"),
    
    "Tunnel Entrance": (520, 63, 140, "4"),
    "Zombie Spawner 3": (653, 44, 74, "5"),
    "Minecart Chest 1": (662, 36, 112, "6"),
    "Minecart Chest 2": (662, 41, 118, "7"),
    "POI 1": (400, 65, 1600, "8"),
    "Town 3": (-1500, 72, 2900, "9"),
    "Town 4": (-2100, 74, 2315, "0"),
    "Huge Cavern": (-1741, 72, 2467, "Q"),
    "Jungle": (-1040, 64, 2535, "W"),
    "Bees": (-265, 64, 1968,  "E"),
}
lst_places = list(places.keys())


def distance_comps(x1: int, z1: int, y1: int, x2: int, z2: int, y2: int) -> tuple[int, int, int]:
    return x2 - x1, z2 - z1, y2 - y1


def distance(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> float:
    return math.sqrt(sum(map(lambda v: v ** 2, distance_comps(*p1, *p2))))


def build_places_df(places: dict) -> pd.DataFrame:
    rows = []
    
    center = places[st.session_state.get(k_centered_on)]
    c_x, c_z, c_y, lbl = center

    for name, (east_west, up_down, south_north, marker_text) in places.items():
        rows.append({
            "name": name,
            "east_west": east_west,
            "up_down": up_down,
            "south_north": south_north,
            "marker_text": marker_text,
            "description": (
                f"{name}<br>"
                f"E/W: {east_west}<br>"
                f"U/D: {up_down}<br>"
                f"S/N: {south_north}"
            ),
            "elevation_group": "Below Y=64" if up_down < 64 else "Y=64 or above",
            "distance": distance((c_x, c_z, c_y), (east_west, up_down, south_north))
        })

    return pd.DataFrame(rows)


st.set_page_config(page_title="3D Map", layout="wide")

c_mapping = st.selectbox("Color Mapping", ["Elevation", "Distance"], 0)
c_maps = {
    "Elevation": "elevation_group",
    "Distance": "distance"
}
c_mapping = c_maps[c_mapping]

k_centered_on = "key_centered_on"
st.session_state.setdefault(k_centered_on, "Bed")
if c_mapping == "distance":
    c_loc = st.selectbox("Centered on", lst_places, 0, key=k_centered_on)

st.title("3D Coordinate Map")
cols_layout = st.columns([0.67, 0.33])
df = build_places_df(places)
    
with cols_layout[1]:
    st.write("Distance Between Points")
    k_point_start = "key_point_start"
    k_point_end = "key_point_end"
    st.session_state.setdefault(k_point_start, lst_places[0])
    st.session_state.setdefault(k_point_end, lst_places[1])
    cols_distance_between = st.columns(2)
    with cols_distance_between[0]:
        c_loc_start = st.selectbox("Start", lst_places.copy(), key=k_point_start)
    with cols_distance_between[1]:
        c_loc_end = st.selectbox("End", lst_places.copy(), key=k_point_end)

    data_start = places[c_loc_start]
    data_end = places[c_loc_end]
    pts_start = data_start[:3]
    pts_end = data_end[:3]
    d_comps = distance_comps(*pts_start, *pts_end)
    dist = distance(pts_start, pts_end)
    st.subheader(f"Distance from {c_loc_start} to {c_loc_end}: {dist:,.2f} blocks")

    cols_comps = st.columns(3)
    for i, v in enumerate(["X", "Z", "Y"]):
        with cols_comps[i]:
            st.metric(v, pts_end[i], d_comps[i])

with cols_layout[0]:
    fig = px.scatter_3d(
        df,
        x="south_north",
        y="east_west",
        z="up_down",
        text="marker_text",
        color=c_mapping,
        hover_name="name",
        hover_data={
            "south_north": True,
            "east_west": True,
            "up_down": True,
            "marker_text": False,
            "elevation_group": False,
        },
    )
    
    df_line = pd.DataFrame({"x": list(range(500)), "y": list(range(500))})
    fig.add_trace(go.Line(df_line, x="x", y="y"))

    fig.update_traces(
        marker=dict(size=7),
        textposition="top center",
    )

    fig.update_layout(
        height=800,
        scene=dict(
            xaxis_title="South / North (Z coordinate)",
            yaxis_title="East / West (X coordinate)",
            zaxis_title="Up / Down (Y coordinate)",
        ),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)


with st.expander("Show coordinate table"):
    st.dataframe(df, use_container_width=True)


# '''
# ==============
# 3D scatterplot
# ==============

# Demonstration of a basic scatterplot in 3D.
# '''

# import random as rand
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np


# def randrange(n, vmin, vmax):
#     '''
#     Helper function to make an array of random numbers having shape (n, )
#     with each number distributed Uniform(vmin, vmax).
#     '''
#     return (vmax - vmin)*np.random.rand(n) + vmin

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# n = 100

# # For each set of style and range settings, plot n random points in the box
# # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
# # for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
# #     xs = randrange(n, 23, 32)
# #     ys = randrange(n, 0, 100)
# #     zs = randrange(n, zlow, zhigh)
# #     ax.scatter(xs, ys, zs, c=c, marker=m)

# # ax.scatter(10, 10, 10)

# '''
# Coordinates of the form (XXX/YYY/ZZZ)
# X - Determines your position East/West in the map. A positive value increases your position to the East. A negative value increases your position to the West.
# Y - Determines your position up/down in the map. A positive value increases your position upward. A negative value increases your position downward.
# Z - Determines your position South/North in the map. A positive value increases your position to the South. A negative value increases your position to the North.
# '''

# places = {
#     "Bed": (146, 58, 0, '<'),  # marker points true North
#     "Chicken": (107, 65, -11, '$C$'),
#     "Train Departure": (106, 96, -19, 'd'),
#     "Train Arrival": (113, 96, -20, 'H'),
#     "Nether Portal": (128, 89, 11, 's'),
#     "Resource Hut": (-138, 64, 146, '$R$'),
#     "Natural Cave": (-184, 89, 393, '.'),
#     "Centre of Town 1": (556, 71, 28, '$1$'),
#     "Birch Forest": (750, 64, -30, '.'),
#     "Rest Stop": (920, 64, -93, '.'),
#     "Centre of Town 2": (1065, 64, -304, '$2$'),
#     "Amphitheatre": (960, 79, -310, '$A$'),
#     "Centre of Town 3": (640, 66, -280, '$3$'),
#     "Glacier": (720, 62, -560, '$G$'),
#     "Coral Reef": (400, 62, -455, '.'),
#     "Tower": (100, 96, 160, '$T$'),
#     "Zombie Spawner": (165, 16, 38, '$Z$')
# }

# for n, coords in places.items():
#     x = coords[2]  # replace x with North/South
#     y = coords[0]  # replace y with East/West
#     z = coords[1]  # Up/Down
#     m = coords[3]
#     c_r = rand.random()
#     c_g = rand.random()
#     c_b = rand.random()
#     c = [[c_r, c_b, c_g]]
#     # color all places below 64 black
#     if z < 64:
#         c = [[0, 0, 0]]
#     ax.scatter(x, y, z, marker=m, c=c,)

# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# plt.show()

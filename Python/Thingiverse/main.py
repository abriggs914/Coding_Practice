from streamlit_utility import display_df, get_selected_rows
from datetime_utility import date_str_format
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from stl import mesh
import pandas as pd
import numpy as np
import glob
import os


path_to_stats = r"C:\Users\abrig\Documents\Coding_Practice\Python\Thingiverse\model_stats.xlsx"


st.set_page_config(layout="wide")


@st.cache_data
def load_stats() -> dict[str, pd.DataFrame]:
    dfs = pd.read_excel(path_to_stats, sheet_name=None)
    for k, df in dfs.items():
        if "Date" in df.columns:
            df["Date"] = df["Date"].apply(lambda d: d.date())
    return dfs


def load_image_paths(directory: str) -> list[str]:
    g = glob.glob("*.png", root_dir=directory) 
    g += glob.glob("*.jpg", root_dir=directory)
    g += glob.glob("*.svg", root_dir=directory)
    g.sort()
    g = list(map(lambda p: os.path.join(directory, p), g))
    return g


@st.cache_data
def get_stl_file_name(directory: str, model_name: str) -> str:
    c_name = model_name.lower().replace("_", " ").removesuffix(".stl") + ".stl"
    p = os.path.join(directory, c_name)
    if not os.path.exists(p):
        c_name = model_name.lower().removesuffix(".stl") + ".stl"
        p = os.path.join(directory, c_name)
        return p if os.path.exists(p) else ""
    else:
        return p
    
    
def generate_stl_render(
    path: str,
    color: str = "#6CA4FF",
    bg_color: str = "#16191e",
    opacity: float = 1.0,
    
    # params for lighting
    ambient: float = 0.4,
    diffuse: float = 0.8,
    roughness: float = 0.3,
    specular: float = 0.4,
    light_x: float = 0,
    light_y: float = 1,
    light_z: float = 1.5,
    
    # params for camera
    camera_x: float = 1.5,
    camera_y: float = -1.5,
    camera_z: float = 1.5
):
    
    lighting = dict(ambient=ambient, diffuse=diffuse, roughness=roughness, specular=specular)
    light_position = dict(x=light_x, y=light_y, z=light_z)
    camera = dict(x=camera_x, y=camera_y, z=camera_z)
    
    m = mesh.Mesh.from_file(path)
    
    # Extract vertex coordinates
    # Each facet has 3 vertices: shape = (num_facets, 3, 3)
    x = m.vectors[:, :, 0].flatten()
    y = m.vectors[:, :, 1].flatten()
    z = m.vectors[:, :, 2].flatten()

    # Build face indices (0,1,2), (3,4,5), etc.
    faces = np.arange(len(x)).reshape(-1, 3)
    i, j, k = faces[:, 0], faces[:, 1], faces[:, 2]

    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=x,
                y=y,
                z=z,
                i=i,
                j=j,
                k=k,
                color=color,
                opacity=opacity,
                flatshading=True,
                lighting=lighting,
                lightposition=light_position
            )
        ]
    )

    fig.update_layout(
        scene=dict(
            aspectmode="data",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(eye=camera)
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor=bg_color,
    )
    
    return fig
        

dfs: dict[str, pd.DataFrame] = load_stats()
df_stats = dfs["Overall"]
df_models = dfs["Inventory"]
df_file_stats = dfs["SubModels"]


display_df(
    df_stats,
    "Stats"
)

display_df(
    df_models,
    "df_models"
)

display_df(
    df_file_stats,
    "df_file_stats"
)

stat_cols: list[str] = [c for c in df_stats.columns if c not in ["Date", "Model", "Published"]]

first_date = df_stats["Date"].min()
last_date = df_stats["Date"].max()
k_slider_dates = "key_slider_dates"
st.session_state.setdefault(k_slider_dates, (first_date, last_date))

display_df(
    df_stats,
    "Stats"
)

cols_top = st.columns([0.25, 0.75])
with cols_top[0]:
    k_selectbox_all = "key_selectbox_all"
    st.selectbox(
        "All",
        stat_cols,
        len(stat_cols) - 1,
        key=k_selectbox_all
    )

    filt_dates = st.slider("Dates", first_date, last_date, key=k_slider_dates)
    
with cols_top[1]:
    fig = px.line(
        df_stats[(filt_dates[0] <= df_stats["Date"]) & (df_stats["Date"] <= filt_dates[1])],
        x="Date",
        y=st.session_state.get(k_selectbox_all),
        color="Model"
    )
    st.plotly_chart(fig)
    
    fig = px.line(
        df_file_stats[(filt_dates[0] <= df_file_stats["Date"]) & (df_file_stats["Date"] <= filt_dates[1])],
        x="Date",
        y="Downloads",
        color="Parent"
    )
    st.plotly_chart(fig)

with st.container(horizontal=True):
    for i, m_n in enumerate(df_stats["Model"].unique()):
        with st.container():
            df_model = df_stats[
                (df_stats["Model"] == m_n)
                & (filt_dates[0] <= df_stats["Date"])
                & (df_stats["Date"] <= filt_dates[1])
            ]
            
            df_m = df_model.copy().reset_index()
            pub = df_m.iloc[0]["Published"]
            age = df_m.iloc[-1]["Age"]
            df_model = df_model.groupby(["Date"]).agg({c: "min" for c in stat_cols}).reset_index()
            
            st.subheader(m_n)
            st.caption(pub)
            st.caption(f"{age} day(s) old")
            
            key = f"selectbox_{i}"
            if st.session_state.get(k_selectbox_all) is not None:
                st.session_state.update({key: st.session_state.get(k_selectbox_all)})
            fig = px.line(
                df_model,
                x="Date",
                y=st.selectbox(
                    "Y-Axis",
                    stat_cols,
                    # len(stat_cols) - 1,
                    key=key,
                    on_change=lambda: st.session_state.update({k_selectbox_all: None})
                )
            )
            st.plotly_chart(fig)
            
            with st.expander("Data"):    
                display_df(
                    df_model,
                    show_shape=False
                )
        

st.divider()
        
        
sel_model = st.selectbox("Investigate", [""] + df_stats["Model"].unique().tolist(), 0)
if not sel_model:
    st.info(f"Select a model to investigate")
else:
    st.write(sel_model)
    df_sel_model_og = df_models[df_models["Parent"] == sel_model]
    df_sel_subs_og = df_file_stats[df_file_stats["Parent"] == sel_model]
    df_sel_stats_og = df_stats[df_stats["Model"] == sel_model]
    df_sel_model = df_sel_model_og.copy().reset_index()
    df_sel_subs = df_sel_subs_og.copy().reset_index()
    df_sel_stats = df_sel_stats_og.copy().reset_index()
    
    if len(df_sel_model) * len(df_sel_subs) * len(df_sel_stats) == 0:
        st.error(f"Could not load all stats")
        st.stop()
    
    thingiverse_id = df_sel_model.loc[0, "ThingiverseID"]
    thingiverse_link = df_sel_model.loc[0, "Thingiverse"]
    directories = df_sel_model["Dir"].unique().tolist()
    publish_date = df_sel_model["Published"].min()
    publish_date_last = df_sel_model["Published"].max()
    edited = publish_date != publish_date_last
    
    # Most popular file in the Thing
    most_popular_file_idx = df_sel_subs["Downloads"].idxmax()
    ser_most_popular_file = df_sel_subs.loc[most_popular_file_idx]
    mpf_name = ser_most_popular_file["ModelName"]
    mpf_n_downloads = ser_most_popular_file["Downloads"]
    df_mpf_model = df_sel_model[df_sel_model["ModelName"] == mpf_name]
    if df_mpf_model.empty:
        st.warning(f"df_mpf_model.empty")
        st.stop()
    ser_mpf_model = df_mpf_model.reset_index().loc[0]
    path_most_popular_model = get_stl_file_name(ser_mpf_model["Dir"], mpf_name)
    
    st.write(ser_most_popular_file)
    st.code(path_most_popular_model)
    
    cols_sel_model = st.columns([0.33, 0.67])
    
    with cols_sel_model[0]:    
        # st.caption(f"Published: {publish_date:%a %b} {str(publish_date.day).removeprefix('0')}{date_suffix(publish_date.day)} {publish_date:%Y}")
        if edited:
            st.caption(f"Published: {date_str_format(publish_date, include_weekday=True, short_weekday=True, short_month=True)}")
            st.caption(f"Last Edited: {date_str_format(publish_date_last, include_weekday=True, short_weekday=True, short_month=True)}")
        else:
            st.caption(f"Published: {date_str_format(publish_date, include_weekday=True)}")
        st.write(thingiverse_link)
        
        
        df_sel_subs_: pd.DataFrame = df_sel_subs.copy()
        df_sel_subs_ = df_sel_subs_.merge(df_sel_model, "inner", ["Parent", "ModelName"])
        df_sel_subs_.sort_values("Downloads", ascending=False, inplace=True)
        k_stde_model_files = "key_stde_model_files"
        # st.session_state.setdefault(k_stde_model_files, {"selection": {"rows": [0]}})
        stde_model_files = st.dataframe(
            df_sel_subs_[["ModelName", "Downloads"]],
            selection_mode="single-row",
            on_select="rerun",
            hide_index=True,
            key=k_stde_model_files,
            selection_default={"selection": {"rows": [0]}}
        )
        w = get_selected_rows(df_sel_subs_, stde_model_files, ["Dir", "ModelName"], 1)
        path_model = get_stl_file_name(*w.values)
        
    with st.container(horizontal=True):
        ## Lighting sliders
        with st.container(border=True):
            slider_vals = [
                ("Ambient", 0, 100, 40),  # 0.4
                ("Diffuse", 0, 100, 80),  # 0.8
                ("Roughness", 0, 100, 30),  # 0.3
                ("Specular", 0, 100, 40),  # 0.4
                
                ("X", -50000, 50000, 0),  # 0.0
                ("Y", -50000, 50000, 100),  # 1.0
                ("Z", -50000, 50000, 150),  # 1.5
            ]
            sliders = []
            slider_keys = [[f"key_slider_lighting_{name}", val / 100] for name, low, high, val in slider_vals]
            with st.container(horizontal=True):
                st.subheader("Lighting")
                if st.button("reset", key="key_reset_lighting"):
                    st.session_state.update({k: v for k, v in slider_keys})
                    
            for i, (name, low, high, val) in enumerate(slider_vals):
                key = slider_keys[i][0]
                sliders.append(st.slider(name, low / 100, high / 100, val / 100, format="%.2f", step=0.01, key=key))
            ambient, diffuse, roughness, specular, light_x, light_y, light_z = sliders
        
        ## Camera sliders
        with st.container(border=True):
            slider_vals = [
                ("X", 150),  # 1.5
                ("Y", -150),  # -1.5
                ("Z", 150),  # 1.5
            ]
            sliders = []
            slider_keys = [[f"key_slider_camera_{name}", val / 100] for name, val in slider_vals]
            with st.container(horizontal=True):
                st.subheader("Camera")
                if st.button("reset", key="key_reset_camera"):
                    st.session_state.update({k: v for k, v in slider_keys})
                    
            for i, (name, val) in enumerate(slider_vals):
                key = slider_keys[i][0]
                sliders.append(st.slider(name, -25.0, 20.0, val / 100, format="%.2f", step=0.01, key=key))
            camera_x, camera_y, camera_z = sliders
    
    with cols_sel_model[1]:
        with st.container(border=True):
            # st.subheader(f"Most popular file: {mpf_name}")           
            # st.caption(f"{mpf_n_downloads} downloads")
            fig = generate_stl_render(
                path_model,
                ambient=ambient, diffuse=diffuse,
                roughness=roughness, specular=specular,
                light_x=light_x, light_y=light_y, light_z=light_z,
                camera_x=camera_x, camera_y=camera_y, camera_z=camera_z,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.code(path_model)
            fs_b = os.path.getsize(path_model)
            fs_kb = fs_b / 1024
            fs_mb = fs_kb / 1024
            use_mb = fs_mb >= 1
            st.caption(f"{fs_mb if use_mb else fs_kb:,.2f} {'M' if use_mb else 'K'}B")
    
    with st.expander("Data"):
        with st.container(horizontal=True):
            display_df(df_sel_model, "Model", show_shape="separate")
            display_df(df_sel_subs, "Files", show_shape="separate")
            display_df(df_sel_stats, "Stats", show_shape="separate")
    
    ## Images
    lst_images = []
    lst_svgs = []
    for dir_ in directories:
        paths = load_image_paths(dir_)
        svgs = [p for p in paths if p.lower().endswith(".svg")]
        lst_images += [p for p in paths if p not in svgs]
        lst_svgs += svgs
    lst_images.sort()
    lst_images.sort()
    cols_images = st.columns(2)
    with cols_images[0]:
        with st.expander("SVGs"):
            with st.container(horizontal=True):
                for i, path in enumerate(lst_svgs):
                    try:
                        st.image(path, caption=os.path.basename(path), width=150)
                    except:
                        st.caption(path)
                
    with cols_images[1]:
        with st.expander("Images"):
            with st.container(horizontal=True):
                for i, path in enumerate(lst_images):
                    try:
                        st.image(path, caption=os.path.basename(path), width=150)
                    except:
                        st.caption(path)
from main import series_list
from streamlit_utility import *
import plotly.express as px


st.set_page_config(layout="wide")


st.write(series_list)

ts_0 = series_list[0]
st.write(ts_0)
st.write(ts_0.__dict__)

data_df = []
for i, series in enumerate(series_list):
    d_series = {k:v for k, v in series.__dict__.items()}
    d_series["total_seasons"] = len(d_series["episodes_list"])
    d_series["total_episodes"] = series.count_episodes()
    d_series["episodes_per_season"] = series.calc_episode_per_season()
    d_series["total_runtime_years"] = series.calc_series_run()
    rt_m, rt_y = series.how_long_is_series()
    d_series["total_runtime_minutes"] = rt_m
    d_series["total_runtime_hours"] = rt_y
    del d_series["episodes_list"]
    data_df.append(d_series)

df_series = pd.DataFrame(data_df)

df_series["Event"] = df_series.apply(
    lambda row: str(series_list[row.name]),
    # lambda row: print(row.index),
    axis=1
)

df_series["start_year"] = df_series.apply(
    lambda row: datetime.datetime(row["start_year"], 1, 1),
    axis=1
)

df_series["end_year"] = df_series.apply(
    lambda row: datetime.datetime(row["end_year"], 12, 31),
    axis=1
)

df_series.sort_values(["start_year", "end_year"], ascending=[True, False], inplace=True)

st.write(df_series)

# st.write(px.timeline.__doc__)

data = px.timeline(
    data_frame=df_series[["name", "start_year", "end_year", "Event"]],
    x_start="start_year",
    x_end="end_year",
    y="name",
    color="name",
    height=1000
)
st.plotly_chart(data)

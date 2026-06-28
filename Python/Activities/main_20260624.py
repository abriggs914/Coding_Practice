import streamlit as st
import pandas as pd
import datetime
import os

from streamlit_utility import display_df


st.set_page_config(layout="wide", page_title="Activities", page_icon=":biking_man:")

path_excel_data = r"data.xlsx"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_excel(path_excel_data)
    df["date"] = df["date"].dt.date
    return df


df = load_data()
display_df(df, "Master data:")

num_cols = [c for c in df.columns if df[c].dtypes in [int, float]]
st.write("num_cols")
st.write(num_cols)

# time per activity
df_tpa = df.copy()
df_tpa["times2"] = df_tpa["times"]
df_tpa["times3"] = df_tpa["times"]
df_tpa["date2"] = df_tpa["date"]
df_tpa = df_tpa.groupby([
    "activity", "unit"
]).agg({
    "times": "sum",
    "times2": "count",
    "times3": "mean",
    "cardioload": "mean",
    "date": "min",
    "date2": "max"
}).reset_index().rename(columns={
    "times": "sum_times",
    "times2": "num_times",
    "times3": "avg_times",
    "cardioload": "avg_cardioload",
    "date": "firstdate",
    "date2": "lastdate"
})
df_tpa["datediff"] = df_tpa["lastdate"] - df_tpa["firstdate"]

df_tpa2 = df.copy()

af = [
    "sum",
    "mean",
    "median",
    "min",
    "max",
    "count",
    "size",
    "std",
    "var",
    "sem",
    "prod",
    "first",
    "last",
    "nunique",
    "any",
    "all",
    "skew",
]

ac = {}
rn = {}
for i, col in enumerate(num_cols):
    for j, agg in enumerate(af):
        nc1 = f"{agg}_{col}"
        nc2 = f"{col}{j}"
        rn[nc2] = nc1
        df_tpa2[nc2] = df_tpa2[col]
        ac[nc2] = agg
        
with st.container(horizontal=True):
    st.write(ac)
    st.write(rn)
        
df_tpa2 = df_tpa2.groupby(["activity", "unit"]).agg(ac).reset_index().rename(columns=rn)

with st.container(horizontal=True):
    display_df(df_tpa, "Time per Activity")
    display_df(df_tpa2, "Time per Activity2")
with st.container(horizontal=True):
    display_df(df_tpa.describe(), "Time per Activity")
    display_df(df_tpa2.describe(), "Time per Activity2")
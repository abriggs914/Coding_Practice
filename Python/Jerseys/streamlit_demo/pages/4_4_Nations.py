import streamlit as st
import json

from html_utility import list_to_html
from nhl_utility import *


data_file = "./4_nations_2025.json"
with open(data_file, "r") as f:
	data = json.load(f)


st.set_page_config(layout="wide")

st.json(data, expanded=False)

st.write(data["info"])

team_cols = st.columns(4)

for i, keys in enumerate([
	("Canada", "CANADA"),
	("Sweden", "SWEDEN"),
	("Finland", "FINLAND"),
	("USA", "UNITED STATES")
]):
	k0, k1 = keys
	with team_cols[i]:
		st.subheader(k0)
		roster_cols = st.columns(2)
		roster_c = data["teams"][k1]["roster"]
		with roster_cols[0]:
			st.write("###### Forwards")
			fwds = roster_c["forwards"]
			fwd_fmt = [f"{t[0]} - {t[1]}" + (f"{t[2]}" if len(t) == 3 else "") for t in fwds]
			fwd_style, fwd_fmt = list_to_html(
				fwd_fmt,
				is_raw=True
			)
			st.markdown(fwd_style, unsafe_allow_html=True)
			st.markdown(fwd_fmt, unsafe_allow_html=True)
		with roster_cols[1]:
			defn = roster_c["defensemen"]
			defn_fmt = [f"{t[0]} - {t[1]}" + (f"{t[2]}" if len(t) == 3 else "") for t in defn]
			defn_style, defn_fmt = list_to_html(
				defn_fmt,
				is_raw=True
			)
			goal = roster_c["goalies"]
			goal_fmt = [f"{t[0]} - {t[1]}" + (f"{t[2]}" if len(t) == 3 else "") for t in goal]
			goal_style, goal_fmt = list_to_html(
				goal_fmt,
				is_raw=True
			)

			st.markdown(defn_style, unsafe_allow_html=True)
			st.markdown(goal_style, unsafe_allow_html=True)

			st.write("###### Defence")
			st.markdown(defn_fmt, unsafe_allow_html=True)
			st.write("###### Goalies")
			st.markdown(goal_fmt, unsafe_allow_html=True)

st.write(league)

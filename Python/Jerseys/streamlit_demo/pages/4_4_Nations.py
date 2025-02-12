import os

import streamlit as st
import json

from html_utility import list_to_html
from nhl_utility import *


@st.cache_data()
def load_flags():
	image_root = r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags"
	to_find_og = [t[0] for t in teams_lu]
	to_find = to_find_og.copy()
	found = []
	for image in os.listdir(image_root):
		if image.endswith(".png"):
			t = None
			lf = len(found)
			print(f"{to_find=}, {image=}")
			for t in to_find:
				if t.lower() in image.lower():
					found.append([t, image])
					break
				else:
					print(f"{t=} not like {image=}")

			if (lf != len(found)) and (t is not None):
				to_find.remove(t)

	found.sort(key=lambda t: to_find_og.index(t[0]))
	for i, t in enumerate(to_find_og):
		if i >= len(found):
			found.append([t, None])
		else:
			if found[i][0] != t:
				found.insert(i, [t, None])
			else:
				found[i][1] = os.path.join(image_root, found[i][1])
	return found


data_file = "./4_nations_2025.json"
with open(data_file, "r") as f:
	data = json.load(f)


teams_lu = [
	("Canada", "CANADA"),
	("USA", "UNITED STATES"),
	("Finland", "FINLAND"),
	("Sweden", "SWEDEN")
]

st.set_page_config(layout="wide")

st.json(data, expanded=False)

st.write(data["info"])

team_cols = st.columns(4)

loaded_flags = load_flags()


for i, keys in enumerate(teams_lu):
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


def validate(game_i):
	chx = st.session_state.get(f"slider_game_{game_i}", "None")
	options = st.session_state.get(f"game_{game_i}_options", ["None"])
	away_score = st.session_state.get(f"score_game_{game_i}_away", 0)
	home_score = st.session_state.get(f"score_game_{game_i}_home", 0)
	in_ot = st.session_state.get(f"checkbox_ot_game_{game_i}", False)
	in_so = st.session_state.get(f"checkbox_so_game_{game_i}", False)

	new_chx = options[0] if away_score > home_score else options[2]

	# print(f"{game_i=}, {new_chx=}, {away_score}-{home_score}")

	st.session_state.update({
		f"slider_game_{game_i}": new_chx,
		f"k_slider_game_{game_i}": new_chx
		# ,
		# "need_rerun": True
	})

	if away_score == home_score:
		st.session_state.update({
			f"slider_game_{game_i}": "None",
			f"k_slider_game_{game_i}": "None"
		})

	if in_ot and in_so:
		st.session_state.update({
			f"checkbox_ot_game_{game_i}": False
		})


st.write("schedule:")
st.write(data["schedule"])
st.write("loaded_flags")
st.write(loaded_flags)

for i, game_data in enumerate(data["schedule"]["games"]):
	away_i = game_data["away"]
	home_i = game_data["home"]

	if (away_i is not None) and (home_i is not None):
		away = teams_lu[away_i][0]
		home = teams_lu[home_i][0]
		date = game_data["date"]
		location = game_data["location"]
		cont = st.container(border=1)
		cols = cont.columns([0.25, 0.25, 0.5])
		with cols[0]:
			st.write(f"Game #{i+1}")
			st.write(f"{away} @ {home}")
			st.write(f"{location}")
			st.write(f"{date}")
		with cols[2]:
			options = [away, "None", home]
			st.session_state.update({f"game_{i}_options": options})
			key = f"slider_game_{i}"
			st.session_state.setdefault(key, "None")
			# st.session_state.update({f"k_{key}": st.session_state.get(key)})
			slider = st.select_slider(
				label=f"{away} @ {home}",
				options=options,
				# key=f"k_{key}",
				key=key,
				disabled=True,
				label_visibility="hidden"
			)
			# st.session_state.update({key: st.session_state.get(f"k_{key}")})
			col_sub = st.columns([0.35, 0.15, 0.15, 0.35])
			with col_sub[0]:
				# st.session_state.update({f"k_score_game_{i}_away": st.session_state.get(f"score_game_{i}_away")})
				st.session_state.setdefault(f"score_game_{i}_away", 0)
				away_score = st.number_input(
					label="Score",
					# key=f"k_score_game_{i}_away",
					key=f"score_game_{i}_away",
					min_value=0,
					max_value=20,
					step=1,
					on_change=lambda i_=i: validate(i_)
				)
				# st.session_state.update({f"score_game_{i}_away": st.session_state.get(f"k_score_game_{i}_away")})
			with col_sub[1]:
				# st.session_state.update({f"k_checkbox_ot_game_{i}": st.session_state.get(f"checkbox_ot_game_{i}")})
				st.checkbox(
					label="OT",
					# key=f"checkbox_ot_game_{i}",
					key=f"k_checkbox_ot_game_{i}",
					on_change=lambda i_=i: validate(i_)
				)
				# st.session_state.update({f"checkbox_ot_game_{i}": st.session_state.get(f"k_checkbox_ot_game_{i}")})
			with col_sub[2]:
				# st.session_state.update({f"k_checkbox_so_game_{i}": st.session_state.get(f"checkbox_so_game_{i}")})
				st.checkbox(
					label="SO",
					# key=f"k_checkbox_so_game_{i}",
					key=f"checkbox_so_game_{i}",
					on_change=lambda i_=i: validate(i_)
				)
				# st.session_state.update({f"checkbox_so_game_{i}": st.session_state.get(f"k_checkbox_so_game_{i}")})
			with col_sub[3]:
				# st.session_state.update({f"k_score_game_{i}_home": st.session_state.get(f"score_game_{i}_home")})
				st.session_state.setdefault(f"score_game_{i}_home", 0)
				home_score = st.number_input(
					label="Score",
					# key=f"k_score_game_{i}_home",
					key=f"score_game_{i}_home",
					min_value=0,
					max_value=20,
					step=1,
					on_change=lambda i_=i: validate(i_)
				)
				# st.session_state.update({f"score_game_{i}_home": st.session_state.get(f"k_score_game_{i}_home")})
			if slider != options[1]:
				chx_i = away_i if options.index(slider) == 0 else home_i
				cols[1].image(
					loaded_flags[chx_i][1],
					caption=loaded_flags[chx_i][0]
				)
				

# if not st.experimental_user.get("is_logged_in", False):
#     if st.button("Log in"):
#         st.login("Microsoft")
# else:
#     if st.button("Log out"):
#         st.logout()
#     st.write(f"Hello, {st.experimental_user.name}!")

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# try:
# 	tabs = st.tabs(["Login", "Create Account"])

# 	if tabs == "Login":
# 		authenticator.login()
# 	else:
# 		authenticator.experimental_guest_login(
# 			'Login with Microsoft',
# 			provider='microsoft',
# 			oauth2=config['oauth2']
# 		)
# except Exception as e:
#     st.error(e)

# Creating a login widget
cont = st.container(border=1)
try:
	with cont:
		authenticator.login(
			max_login_attempts=3
		)
except authenticator.LoginError as e:
	cont.error(e)

# st.write(authenticator)
# st.write(authenticator.__dict__)
# st.write(type(authenticator))
# st.write("config")
# st.write(config)
# st.write("st.session_state")
# st.write(st.session_state)


if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')

if st.session_state.get("need_rerun", False):
	st.session_state.update({"need_rerun": False})
	st.rerun()


with open('./config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

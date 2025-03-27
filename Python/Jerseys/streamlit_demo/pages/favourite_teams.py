import json
import os
import random

import pandas as pd
import streamlit as st

from PIL import Image
from typing import Optional, List

import nhl_utility as nhu


st.set_page_config(
    layout="wide",
    page_title="Favourite NHL Teams"
)

# Mins and Maxs use inclusive bounds
min_n_questions: int = 5
max_n_questions: int = 50
min_n_teams_per_question: int = 2
max_n_teams_per_question: int = 5
default_n_questions: int = 25
default_n_teams_per_questions: int = 25

full_size_image = (200, 200)
small_size_image = (50, 50)
save_file = "./favourite_teams_save.json"
image_directory = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images"
if not os.path.exists(image_directory):
    image_directory = r"C:\Users\ABriggs\Documents\Coding_Practice\Python\Hockey pool\Images"


@st.cache_data()
def load_save_data():
    if not os.path.exists(save_file):
        with open(save_file, "w") as f:
            json.dump({}, f)
        with open(save_file, "r") as f:
            return json.load(f)


@st.cache_data()
def load_image_data():
    team_images = {}
    for pth in os.listdir(image_directory):
        team = pth.replace("logo", "").replace("_", " ").replace(".png", "").replace(".jpg", "").strip()
        if "division" in team or "conference" in team:
            continue
        im_pth = os.path.join(image_directory, pth)
        img = Image.open(im_pth)
        # img_c = img.copy()
        # btn_image = ImageTk.PhotoImage(img.resize(full_size_image))
        # res_image = ImageTk.PhotoImage(img.resize(small_size_image))
        team_images[team] = {
            "path": im_pth,
            "img": img,
            "btn_img": img.resize(full_size_image),
            "res_img": img.resize(full_size_image)
        }
        # btn_images[team] = btn_image
        # res_images[team] = res_image
    return team_images


def validate_confs_divs(conf: Optional[str] = None, div: Optional[str] = None):
    do_test: bool = False
    ids = {k: v for k, v in checkbox_conf_ids.items()}
    ids.update(checkbox_div_ids)
    last = div if div is not None else (conf if conf is not None else None)
    if do_test:
        print(f"--A {conf=}, {div=}, {last=}", end=" ")
    if last:
        # check any ids linked to this id
        is_conf = last in checkbox_conf_ids
        last_id = ids[last]
        val: bool = st.session_state.get(last_id, False)
        # Need to flip val because this function is run before-update
        val = not val
        if do_test:
            print(f"--B {is_conf=}, {last=}, {last_id=}, {val=}", end=" ")
        if is_conf:
            if do_test:
                print(f"--C", end=" ")
            if conf == "e":
                if do_test:
                    print(f"--D", end=" ")
                # turn on east divisions
                st.session_state.update({
                    checkbox_div_ids["a"]: val,
                    checkbox_div_ids["m"]: val,
                    last_id: val
                })
            else:
                if do_test:
                    print(f"--E", end=" ")
                # turn on west divisions
                st.session_state.update({
                    checkbox_div_ids["p"]: val,
                    checkbox_div_ids["c"]: val,
                    last_id: val
                })
        else:
            if do_test:
                print(f"--F", end=" ")
            if div in ("p", "c"):
                if do_test:
                    print(f"--G", end=" ")
                st.session_state.update({
                    checkbox_conf_ids["w"]: val,
                    last_id: val
                })
            else:
                if do_test:
                    print(f"--H", end=" ")
                st.session_state.update({
                    checkbox_conf_ids["e"]: val,
                    last_id: val
                })
    else:
        # check all ids
        raise ValueError("COMPLETE THIS BRANCH")
    
    if do_test:
        print(f"")


def get_teams() -> List[str]:
    question_teams = []
    if st.session_state.get(k_checkbox_div_p, False):
        question_teams.extend(nhu.league["western"]["pacific"])
    if st.session_state.get(k_checkbox_div_c, False):
        question_teams.extend(nhu.league["western"]["central"])
    if st.session_state.get(k_checkbox_div_m, False):
        question_teams.extend(nhu.league["eastern"]["metropolitan"])
    if st.session_state.get(k_checkbox_div_a, False):
        question_teams.extend(nhu.league["eastern"]["atlantic"])
    return question_teams


def new_question() -> List[str]:
    # snq: int = st.session_state.get(k_slider_n_questions)
    sntpq: int = st.session_state.get(k_slider_n_teams_per_question)
    t: List[str] = get_teams()
    rs = random.sample(t, k=sntpq)
    print(f"New Question: {sntpq=}, {rs=}")
    return rs

print(f"TOP")
states = ["idle", "playing", "reviewing"]
state_idle, state_playing, state_reviewing = states

k_state: str = "state"
state = st.session_state.setdefault(k_state, state_idle)

team_images = load_image_data()
save_data = load_save_data()
st.write(save_data)
st.write(list(team_images))

# cols = st.columns(2)
# for i, team in enumerate(team_images):
#     with cols[0]:
#         st.write(team)
#     with cols[1]:
#         st.image(team_images[team]["btn_img"], caption=team)


k_slider_n_questions: str = "slider_n_questions"
k_slider_n_teams_per_question: str = "slider_n_teams_per_question"
k_checkbox_conf_e: str = "checkbox_conf_e"
k_checkbox_conf_w: str = "checkbox_conf_w"
k_checkbox_div_p: str = "checkbox_div_p"
k_checkbox_div_c: str = "checkbox_div_c"
k_checkbox_div_m: str = "checkbox_div_m"
k_checkbox_div_a: str = "checkbox_div_a"

k_question_num: str = "question_num"
k_num_questions: str = "num_questions"
k_question_history: str = "question_history"

question_history = st.session_state.setdefault(k_question_history, {"questions": [], "answers": []})
question_num = st.session_state.setdefault(k_question_num, 1)
num_questions = st.session_state.setdefault(k_num_questions, min_n_questions)


if state == state_idle:
    with st.container(border=True):
        cols_input_controls_0 = st.columns(3)
        cols_input_controls_1 = st.columns([0.8, 0.2])

    with cols_input_controls_0[0]:
        with st.container(border=True):
            slider_n_questions = st.slider(
                key=f"k_{k_slider_n_questions}",
                label="Total Questions:",
                min_value=min_n_questions,
                max_value=max_n_questions,
                value=25
            )
            slider_n_teams_per_question = st.slider(
                key=f"k_{k_slider_n_teams_per_question}",
                label="Teams per Question:",
                min_value=min_n_teams_per_question,
                max_value=max_n_teams_per_question,
                value=2
            )

    checkbox_conf_ids = {
        "e": "checkbox_conf_e",
        "w": "checkbox_conf_w"
    }
    checkbox_div_ids = {
        "p": "checkbox_div_p",
        "c": "checkbox_div_c",
        "m": "checkbox_div_m",
        "a": "checkbox_div_a"
    }
    checkbox_data = {
        k_checkbox_conf_e: ("East Conf?", {"conf": "e"}),
        k_checkbox_conf_w: ("West Conf?", {"conf": "w"}),
        k_checkbox_div_p: ("Pacific Div?", {"div": "p"}),
        k_checkbox_div_c: ("Central Div?", {"div": "c"}),
        k_checkbox_div_m: ("Metro Div?", {"div": "m"}),
        k_checkbox_div_a: ("Atlantic Div?", {"div": "a"})
    }
    checkboxes = []
    f_c, f_d = True, True
    for k, data in checkbox_data.items():
        label, id_ = data
        val = st.session_state.setdefault(k, True)
        st.session_state.update({f"k_{k}": val})
        c_ = id_.get("conf")
        d_ = id_.get("div")
        is_conf: bool = c_ is not None
        with cols_input_controls_0[1 + int(not is_conf)]:
            if is_conf and f_c:
                st.write("Conferences:")
                st.divider()
                f_c = False
            elif (not is_conf) and f_d:
                st.write("Divisions:")
                st.divider()
                f_d = False
            checkboxes.append(st.checkbox(
                label=label,
                key=f"k_{k}",
                on_change=lambda conf_=c_, div_=d_: validate_confs_divs(conf=conf_, div=div_)
            ))

    vd_teams: bool = bool(get_teams())
    vd_slider_n_questions: bool = min_n_questions <= slider_n_questions <= max_n_questions
    vd_slider_n_teams_per_question: bool = min_n_teams_per_question <= slider_n_teams_per_question <= max_n_teams_per_question
    # st.checkbox(label="vd_slider_n_questions", value=vd_slider_n_questions, disabled=True)
    # st.checkbox(label="vd_slider_n_teams_per_question", value=vd_slider_n_teams_per_question, disabled=True)
    # st.checkbox(label="vd_teams", value=vd_teams, disabled=True)
    # st.write(f"question_teams")
    # st.write(question_teams)

    if all([
        vd_teams,
        vd_slider_n_questions,
        vd_slider_n_teams_per_question
    ]):
        with cols_input_controls_1[1]:
            if st.button(
                label="submit"
            ):
                st.session_state.update({
                    k_state: state_playing,
                    k_num_questions: slider_n_questions,
                    k_slider_n_teams_per_question: slider_n_teams_per_question
                })
                st.rerun()
    else:
        with cols_input_controls_1[0]:
            st.warning("Invalid inputs")

    st.session_state.update({
        k_slider_n_questions: slider_n_questions,
        k_slider_n_teams_per_question: slider_n_teams_per_question
    })
    st.session_state.update(dict(zip(checkbox_data, checkboxes)))
elif state == state_playing:
    if len(question_history["questions"]) < question_num:
        question_history["questions"].append(new_question())
    elif len(question_history["questions"]) >= num_questions:
        st.session_state.update({
            k_state: state_reviewing
        })
        st.rerun()

    st.subheader(f"Question {question_num} / {num_questions}")
    st.divider()
    sntpq: int = st.session_state.get(k_slider_n_teams_per_question)
    # t: List[str] = get_teams()
    cols_q_options = st.columns(sntpq, gap="small")
    for i, t in enumerate(question_history["questions"][-1]):
        print(f"{i=}, {t=}")
        with cols_q_options[i]:
            # st.write(t)
            k_team = f'{nhu.reverse_lookup(t, "team").lower()}'
            if k_team not in ("new york rangers", "new york islanders"):
                k_team += f' {nhu.reverse_lookup(t, "mascot").lower()}'
            k_team = k_team.replace(".", "").strip()
            st.image(
                team_images[k_team]["btn_img"],
                caption=t
            )
            if st.button(
                label=t,
                key=f"btn_select_t_{i}"
            ):
                question_history["answers"].append(t)
                print(f"APPEND ANS {t=}")
                st.session_state.update({
                    k_question_num: question_num + 1,
                    k_question_history: question_history
                })
                st.rerun()
            # st.image(team_images[team]["btn_img"], caption=team)
else:
    st.header("Reviewing")
    st.write("question_history")
    st.write(question_history)
    st.write(pd.DataFrame(question_history["questions"]))
    st.write(
        pd.DataFrame(question_history["questions"]).rename(columns={
            i: f"Q_opt_{i}" for i in range(max_n_teams_per_question)
        }).join(
            pd.DataFrame(question_history["answers"]).rename(columns={
                0: "A_0"
            })
        )
    )

st.write("nhu.league")
st.write(nhu.league)
st.write(f"{nhu.reverse_lookup('anaheim', 'mascot')=}")
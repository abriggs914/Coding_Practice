import datetime
import json
import os
import random

import pandas as pd
import streamlit as st

from PIL import Image
from typing import Optional, List

import nhl_utility as nhu
from streamlit_utility import display_df

from utility import percent

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
save_file_data = load_save_data()
st.write("save_file_data")
st.write(save_file_data)
# st.write(list(team_images))
#
# # cols = st.columns(2)
# # for i, team in enumerate(team_images):
# #     with cols[0]:
# #         st.write(team)
# #     with cols[1]:
# #         st.image(team_images[team]["btn_img"], caption=team)


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

    with cols_input_controls_1[0]:
        if st.button(
            label="Review"
        ):
            st.session_state.update({
                k_state: state_reviewing
            })
            st.rerun()

    st.session_state.update({
        k_slider_n_questions: slider_n_questions,
        k_slider_n_teams_per_question: slider_n_teams_per_question
    })
    st.session_state.update(dict(zip(checkbox_data, checkboxes)))
elif state == state_playing:

    st.subheader(f"Question {question_num} / {num_questions}")
    print(f"Question {question_num} / {num_questions}")
    st.divider()
    sntpq: int = st.session_state.get(k_slider_n_teams_per_question)
    # t: List[str] = get_teams()

    def check_question_len():
        print(f"CQL: lqs={len(question_history['questions'])}, qn={question_num}, nq={num_questions}", end=" ")
        if len(question_history["questions"]) < question_num:
            print(f"NQ")
            question_history["questions"].append(new_question())
            st.rerun()
        elif len(question_history["questions"]) > num_questions:
            question_history["questions"].pop(-1)
            st.session_state.update({
                k_state: state_reviewing
            })
            print(f"RV")
            st.rerun()

    def click_team(t_: str, btn_key: str):
        question_history["answers"].append(t_)
        print(f"APPEND ANS {t=}")
        st.session_state.update({
            k_question_num: question_num + 1,
            k_question_history: question_history
        })

    check_question_len()

    cols_q_options = st.columns(sntpq, gap="small")
    for i, t in enumerate(question_history["questions"][-1]):
        # print(f"{i=}, {t=}")
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
            btn_key = f"btn_select_t_{i}"
            btn_select_t = st.button(
                label=t,
                key=btn_key,
                on_click=lambda t_=t, bk=btn_key: click_team(t_, bk)
            )
            if btn_select_t:
                check_question_len()
                # question_history["answers"].append(t)
                # print(f"APPEND ANS {t=}")
                # st.session_state.update({
                #     k_question_num: question_num + 1,
                #     k_question_history: question_history
                # })
                # print(f"RERUN")
                # st.rerun()
            # st.image(team_images[team]["btn_img"], caption=team)

    st.write("question_history")
    st.write(question_history)
else:
    st.header("Reviewing")

    if question_num > 1:
        st.write("question_history")
        cols_dfs = st.columns(2)
        # st.write(question_history)
        # st.write(pd.DataFrame(question_history["questions"]))
        df_hist = pd.DataFrame(question_history["questions"]).rename(columns={
            i: f"Q_opt_{i}" for i in range(max_n_teams_per_question)
        }).join(
            pd.DataFrame(question_history["answers"]).rename(columns={
                0: "A_0"
            })
        )
        with cols_dfs[0]:
            stdf_hist = display_df(
                df_hist
            )

        df_columns = df_hist.columns
        list_teams = []
        for i, col in enumerate(df_columns):
            list_teams.extend(df_hist[col].unique().tolist())
        list_teams = list(set(list_teams))
        df_data = [
            {
                "team": t,
                "xOption": 0,
                "xChosen": 0
            }
            for i, t in enumerate(list_teams)
        ]
        for i, row in df_hist.iterrows():
            for j, col in enumerate(df_columns):
                team = df_hist.loc[i, col]
                t_idx = list_teams.index(team)
                if j < (len(df_columns) - 1):
                    # question
                    df_data[t_idx]["xOption"] += 1
                else:
                    # answer
                    df_data[t_idx]["xChosen"] += 1

        df_stats = pd.DataFrame(df_data)
        df_stats["pctChosen"] = df_stats["xChosen"] / df_stats["xOption"]
        df_stats_0 = df_stats.loc[df_stats["xChosen"] > 0].sort_values(
            by=["pctChosen", "xOption"],
            ascending=[False, False]
        )
        df_stats_1 = df_stats.loc[df_stats["xChosen"] == 0].sort_values(
            by=["pctChosen", "xOption"],
            ascending=[False, True]
        )
        df_stats = pd.concat([df_stats_0, df_stats_1], ignore_index=True)
        df_stats["pctChosen"] = df_stats["pctChosen"].apply(lambda p: percent(p))
        with cols_dfs[1]:
            display_df(df_stats)

    # TODO report on each 'Game', not just the team selections.
    dfs_overall_data = {}
    dfs_team_data = {}
    for save_date_key, save_data in save_file_data.items():
        results = save_data.get("results", {})
        df_results = pd.DataFrame(results)
        # display_df(
        #     df_results,
        #     title=f"{save_date_key}"
        # )
        for i, row in df_results.iterrows():
            team = row["team"]
            if team not in dfs_team_data:
                dfs_team_data[team] = {
                    "xOption": row["xOption"],
                    "xChosen": row["xChosen"]
                }
            else:
                dfs_team_data[team]["xOption"] += row["xOption"]
                dfs_team_data[team]["xChosen"] += row["xChosen"]

    df_all_teams_results = pd.DataFrame(dfs_team_data).transpose().reset_index().rename(columns={"index": "team"})
    df_all_teams_results["pctChosen"] = df_all_teams_results["xChosen"] / df_all_teams_results["xOption"]
    df_all_teams_results_0 = df_all_teams_results.loc[df_all_teams_results["xChosen"] > 0].sort_values(
        by=["pctChosen", "xOption"],
        ascending=[False, False]
    )
    df_all_teams_results_1 = df_all_teams_results.loc[df_all_teams_results["xChosen"] == 0].sort_values(
        by=["pctChosen", "xOption"],
        ascending=[False, True]
    )
    df_all_teams_results = pd.concat([df_all_teams_results_0, df_all_teams_results_1], ignore_index=True)
    df_all_teams_results["pctChosen"] = df_all_teams_results["pctChosen"].apply(lambda p: percent(p))
    display_df(df_all_teams_results, "df_all_teams_results")

    if st.button(
        label="Play again?" if question_num > 1 else "Play?"
    ):
        if question_num > 1:
            save_data = {}
            for key, do_pop in {
                k_state: True,
                k_question_num: True,
                k_num_questions: True,
                k_question_history: True,

                k_slider_n_teams_per_question: False,
                k_slider_n_questions: False,
                k_checkbox_conf_e: False,
                k_checkbox_conf_w: False,
                k_checkbox_div_p: False,
                k_checkbox_div_c: False,
                k_checkbox_div_m: False,
                k_checkbox_div_a: False
            }.items():
                save_data.setdefault(key, st.session_state.get(key))
                if do_pop:
                    st.session_state.pop(key)

            save_data["results"] = json.loads(df_stats.to_json())

            save_file_data[f"{datetime.datetime.now():%Y-%m-%d %X}"] = save_data

            with open(save_file, "w") as f:
                json.dump(save_file_data, f)

            load_save_data.clear()
        st.rerun()

# st.write("nhu.league")
# st.write(nhu.league)
# st.write(f"{nhu.reverse_lookup('anaheim', 'mascot')=}")
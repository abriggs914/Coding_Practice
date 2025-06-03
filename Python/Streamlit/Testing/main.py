import random
import re
from difflib import SequenceMatcher

import pandas as pd
import streamlit as st
import unicodedata

from dataframe_utility import *
from streamlit_utility import *


def normalize_string(s: str):
    # Lowercase
    s = s.lower()
    # Remove accents
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode()
    # Remove all non-alphanumeric characters
    s = re.sub(r'[^a-z0-9]', '', s)
    return s


def determine_match(a: str, b: str, r_val: str = "ratio"):
    seq_match = SequenceMatcher(None, a, b)
    if r_val == "match":
        return seq_match
    else:
        return seq_match.ratio()


def new_df(do_set: bool = True):
    phrase_lens = 3, 8
    n_phrases = 100
    n_random_words = 5000
    n_random_phrases = 1000
    df_phrases = random_df(
        n_columns={
            "A": "str"
        },
        n_rows=n_random_words
    )

    phrase_idxs = [
        random.sample(list(df_phrases.index), random.randint(*phrase_lens))
        for i in range(n_phrases)
    ]

    # st.write("phrase_idxs")
    # st.write(phrase_idxs)

    phrases = [
        df_phrases.loc[idxs, "A"].values.tolist()
        for i, idxs in enumerate(phrase_idxs)
    ]
    st.session_state.update({
        k_words_used: [w for words in phrases for w in words],
    })
    phrases = [" ".join(p) for p in phrases]

    # st.write("phrases")
    # st.write(phrases)

    df = random_df(
        n_columns={
            "A": "str",
            "B": "str",
            "C": "str",
            "D": "str",
            "E": "str"
        },
        n_rows=n_random_phrases,
        defaults={
            "A": phrases,
        }
    )
    if do_set:
        st.session_state.update({
            k_df: df
        })
    return df


if __name__ == '__main__':

    st.set_page_config(
        layout="wide"
    )

    k_df: str = "df"
    k_words_used: str = "k_words_used"

    df: pd.DataFrame = st.session_state.setdefault(k_df)
    lst_words_use: list[str] = st.session_state.get(k_words_used)

    if (not isinstance(df, pd.DataFrame)) and (not df):
        df = new_df(do_set=True)
        lst_words_use = st.session_state.get(k_words_used)


    if st.button(
        label="new df",
        key="k_button_new_df"
    ):
        df = new_df(do_set=True)

    st.write("lst_words_use")
    st.write(lst_words_use)

    k_button_select_word: str = "k_button_select_word"
    selectbox_word = st.selectbox(
        label="Select word",
        options=lst_words_use,
        key=k_button_select_word
    )

    df["A_n"] = df["A"].apply(normalize_string)
    df["found"] = df["A_n"].str.contains(normalize_string(selectbox_word))
    df["A_m%"] = df["A_n"].apply(lambda s: determine_match(s, normalize_string(selectbox_word)))

    k_slider_match_strictness: str = "k_slider_match_strictness"
    options_match_strictness = [(i * 5) / 100 for i in range(21)]
    st.session_state.setdefault(k_slider_match_strictness, (options_match_strictness[-4], options_match_strictness[-1]))
    st.write("options_match_strictness")
    st.write(options_match_strictness)
    st.write("st.session_state[k_slider_match_strictness]")
    st.write(st.session_state[k_slider_match_strictness])
    slider_match_strictness = st.select_slider(
        label="Match Strictness",
        key=k_slider_match_strictness,
        options=options_match_strictness
    )

    display_df(
        df,
        "df",
        width=1500
    )

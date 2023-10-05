import streamlit as st
import pandas as pd

st.title("Let's explore session states ans callback functions")

if "number_of_rows" not in st.session_state:
    st.session_state["number_of_rows"] = 5
    # st.session_state["type"] = "Categorical"

df = pd.DataFrame({
    "A": list(range(18))[:15],
    "B": list(range(-18, 100))[:15],
    "C": list(range(180, 240))[:15],
    "D": list(range(18, 37))[:15]
})

increment = st.button("Show more columns")
if increment:
    st.session_state.number_of_rows += 1

decrement = st.button("Show fewer columns")
if decrement:
    st.session_state.number_of_rows -= 1

st.table(df.head(st.session_state["number_of_rows"]))

import os
import json
import pandas as pd
import streamlit as st

from json_utility import peek_json


st.set_page_config(
    layout="wide",
    page_title="Excel Workbook Details"
)


@st.cache_data()
def read_file(file, **kwargs) -> pd.DataFrame | dict:
    try:
        # st.write(f"A")
        return pd.read_excel(file, **kwargs)
    except Exception as e1:
        # st.write(f"B")
        # st.error(e1)
        try:
            # st.write(f"C")
            return pd.read_csv(file, **kwargs)
        except Exception as e2:    
            # st.write(f"D")
            # st.error(e2)
            try:
                # st.write(f"E")
                # st.write(type(file))
                return json.loads(file.getvalue().decode("utf-8"))
            except Exception as e3:
                # st.write(f"F")
                # st.error(e3)
                return pd.DataFrame()
        

k_file_uploader = "key_file_uploader"
lbl_file_uploader = "Upload am :red[.xlsx] or :blue[.csv]"
st.write(lbl_file_uploader)
file_uploader = st.file_uploader(
    label=lbl_file_uploader,
    accept_multiple_files=False,
    key=k_file_uploader,
    help="Program supports .json, .xlsx or .csv files",
    type=[".xlsx", ".csv", ".json"],
    label_visibility="hidden"
)

if file_uploader:
    df_json = read_file(file_uploader)
    is_json = isinstance(df_json, (dict, list))
    if is_json:
        json_ = df_json
        # try:
        peeked = peek_json(json_)
        with st.container(horizontal=True):
            with st.container():
                st.write("peeked")
                checkbox_expand_peeked = st.checkbox("expand?", key="checkbox_expand_peeked", value=False)
                st.json(peeked, expanded=checkbox_expand_peeked)
            with st.container():
                st.write("actual")
                checkbox_expand_actual = st.checkbox("expand?", key="checkbox_expand_actual", value=False)
                st.json(json_, expanded=checkbox_expand_actual)
        # except Exception as e:
            # st.error(f"{e}")
    else:
        df = df_json
        with st.container(horizontal=True):
            st.metric(f"# Rows", df.shape[0])
            st.metric(f"# Columns", df.shape[1])
        with st.expander("Column data"):
            with st.container(horizontal=True):
                st.write(dict(zip(df.columns, df.dtypes)))
                st.write(df.describe())
        try:
            st.write(f"Investigate DataFrame")
            st.dataframe(
                df.head(40)
            )
        except Exception as e:
            st.error(f"{e}")
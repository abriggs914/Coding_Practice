import pandas as pd
import streamlit as st
from dataframe_utility import *


# @st.cache_data(show_spinner=True, ttl=None)
def new_random_df() -> pd.DataFrame:
    nr = slider_n_rows
    asl = toggle_use_sublists
    return random_df(
        n_rows=nr,
        allow_sub_lists=asl
    )


def display_df(
        df: pd.DataFrame,
        title: Optional[str] = None,
        hide_index: str | bool = "if_int",
        show_shape: bool = True,
        use_container_width: bool = False,
        key: str | int | None = None
):
    title = title if title else ""
    shape = df.shape
    if show_shape:
        title = f"{title} ({shape[0]} Rows".strip()
        title += f" x {shape[1]} Cols)" if len(shape) > 1 else ")"

    if title:
        st.write(title)

    if hide_index == "if_int":
        hide_index = str(df.index.dtype).lower() == "int64"

    # st.write(f"{title=}, {hide_index=}")
    stdf = st.dataframe(
        data=df,
        key=key,
       hide_index=hide_index,
        use_container_width=use_container_width
    )
    return stdf


def change_df_columns():
    print(f"change_df_columns")
    print(stde_columns)


st.data_editor(pd.DataFrame(columns=["Name", "Type", "Value", "Min", "Max"]))


toggle_use_sublists = st.toggle(
    label="Allow Sub-Lists?"
)
slider_n_rows = st.slider(
    label="# Rows",
    min_value=0,
    value=8,
    max_value=100
)


k_df = "df"
k_df_columns = "df_columns"

if st.session_state.get(k_df) is None:
    st.session_state.update({
        k_df: new_random_df()
    })

if st.session_state.get(k_df) is None:
    st.session_state.update({
        k_df_columns: pd.DataFrame(columns=["Name", "Type", "Value", "Min", "Max"])
    })

df_columns = st.session_state.get(k_df_columns)
options_col_types = ["int", "float", "str", "datetime", "bool", "list"]

stde_columns = st.data_editor(
    data=df_columns,
    # key="k_stde_columns",
    num_rows="dynamic",
    column_config={
        "Type": st.column_config.SelectboxColumn(
            label="Type",
            default=random.choice(options_col_types),
            options=options_col_types,
        )
    }
    # ,
    # on_change=change_df_columns
)

if st.button(
    label="New DF"
):
    st.session_state.update({
        k_df: new_random_df()
    })
    st.rerun()

df = st.session_state.get(k_df)
stdf = display_df(df, "DF")

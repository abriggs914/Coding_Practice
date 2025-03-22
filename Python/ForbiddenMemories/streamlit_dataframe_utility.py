import pandas as pd
import streamlit as st
from dataframe_utility import *


# @st.cache_data(show_spinner=True, ttl=None)
def new_random_df() -> pd.DataFrame:
    nr = 5
    asl = False
    try:
        nr = slider_n_rows
        asl = toggle_use_sublists
    except NameError:
        pass
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


def update_slider_n_cols():
    n = slider_n_cols
    df = df_columns
    kc = df["Name"].index
    print(f"USNC {n=}, {len(kc)=}")
    if n < len(kc):
        # delete
        print(f"-A")
        ndf = df.loc[kc[:n]]
    elif n > len(kc):
        # add
        print(f"-B")
        ndf = pd.concat([
            df,
            pd.DataFrame([
                dict(zip(cols_df_columns, [False, excel_column_name(i + len(kc), up_to=False), *[None]*(len(cols_df_columns)-1)]))
                for i in range(n - len(kc))
            ])],
            ignore_index=True
        )
    else:
        # do nothing
        print(f"-C")
        return

    st.session_state.update({
        k_df_columns: ndf,
        k_n_cols: n
    })
    # st.rerun()


k_df = "df"
k_n_cols = "n_cols"
k_df_columns = "df_columns"
k_df_columns_edit = "df_columns_edit_index"

cols_df_columns = ["Edit", "Name", "Type", "Value", "Min", "Max"]
options_col_types = ["int", "float", "str", "datetime", "bool", "list"]
default_col_type = "str"


with st.container(border=1):

    if st.session_state.get(k_df) is None:
        st.session_state.update({
            k_df: new_random_df()
        })

    if st.session_state.get(k_df_columns) is None:
        st.session_state.update({
            k_df_columns: pd.DataFrame(columns=cols_df_columns)
        })

    df_columns: pd.DataFrame = st.session_state.get(k_df_columns)

    with st.expander("Enter some column data:"):

        slider_n_cols = st.slider(
            label="Cols",
            min_value=0,
            max_value=26
            # ,
            # on_change=update_slider_n_cols
        )
        if st.session_state.get(k_n_cols) is None:
            # print(f"A")
            st.session_state.update({k_n_cols: slider_n_cols})
        else:
            # print(f"B")
            nc = st.session_state.get(k_n_cols)
            if nc != slider_n_cols:
                # print(f"C")
                n = slider_n_cols
                df = df_columns
                kc = df["Name"].index
                # print(f"USNC {slider_n_cols=}, {len(kc)=}")
                if slider_n_cols < len(kc):
                    # delete
                    # print(f"-A")
                    ndf = df.loc[kc[:slider_n_cols]]
                    st.session_state.update({
                        k_df_columns: ndf,
                        k_n_cols: n
                    })
                    st.rerun()
                elif slider_n_cols > len(kc):
                    # add
                    # print(f"-B")
                    ndf = pd.concat([
                        df,
                        pd.DataFrame([
                            dict(zip(cols_df_columns,
                                     [
                                         False,
                                         excel_column_name(i + len(kc), up_to=False),
                                         default_col_type,
                                         *[None] * (len(cols_df_columns) - 2)
                                     ]
                                     ))
                            for i in range(slider_n_cols - len(kc))
                        ])],
                        ignore_index=True
                    )
                    st.session_state.update({
                        k_df_columns: ndf,
                        k_n_cols: n
                    })
                    st.rerun()
                else:
                    # do nothing
                    # print(f"-C")
                    pass

        if st.session_state.get(k_df_columns_edit) is None:
            st.session_state.update({k_df_columns_edit: df_columns.loc[df_columns["Edit"]].index.tolist()})
        edit_columns = st.session_state.get(k_df_columns_edit)
        edit_types = df_columns.loc[edit_columns, "Type"]

        stde_columns = st.data_editor(
            data=df_columns,
            key="k_stde_columns",
            # num_rows="dynamic",
            column_config={
                "Type": st.column_config.SelectboxColumn(
                    label="Type",
                    default="str",
                    options=options_col_types
                )
            },
            disabled=cols_df_columns[2:]
            # ,
            # on_change=change_df_columns
        )

    ctl_cols_low = st.columns([0.4, 0.6])

    with ctl_cols_low[0]:
        toggle_use_sublists = st.toggle(
            label="Allow Sub-Lists?"
        )
    with ctl_cols_low[1]:
        slider_n_rows = st.slider(
            label="# Rows",
            min_value=0,
            value=8,
            max_value=100
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

st.session_state.update({k_df_columns: stde_columns})

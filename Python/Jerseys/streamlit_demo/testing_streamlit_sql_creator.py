import datetime

import pandas as pd
import streamlit as st

from streamlit_pills import pills

from datetime_utility import is_date
from sql_utility import get_database_tables, wrap, get_table_cols, schema_parse, select_with_alias, create_sql
from utility import isnumber, get_windows_user

st.set_page_config(layout="wide")

# grid = {
#     "top_bar": st.columns([0.6, 0.2, 0.2]),
#     "title_row": st.container(),
#     "credentials_row": st.container(),
#     "content_row_0": st.container(),
#     "content_row_1": st.container(),
#     "content_row_2": st.container()
#     # ,
#     # "tab_new_request": None,
#     # "tab_edit_request": None
# }

tab_names = ["New", "Edit", "Server", "Access", "Inventory", "Code Samples"]
sm_tab_names = ["Search Tables", "SQL Creator", "Coming Soon"]

# List of searchable databases for Server [Maintenance]->[Search Tables]
list_databases = [
    "BWSdb",
    "StargateDB",
    "CompanyH",
    "SysproCompanyA",
    "SysproCompanyS",
    "SysproCompanyL",
    "uniPoint_Live"
]

MAX_QUERY_HOLD_TIME: int = 1000 * 60 * 2  # 2 hours
MAX_FILE_HOLD_TIME: int = 1000 * 60 * 6  # 6 hours
SHOW_SPINNERS: bool = True


@st.cache_data(show_spinner=SHOW_SPINNERS, ttl=MAX_QUERY_HOLD_TIME)
def get_tables(db: str) -> pd.DataFrame:
    """
    Caching return DF of Database columns.
    :param db: Database name as a string ex:'BWSdb'
    :return: pd.DataFrame(columns=["TABLE_CATALOG", "TABLE_NAME", "COLUMN_NAME", "PRIMARY_KEY", "DATA_TYPE", "CHARACTER_MAXIMUM_LENGTH"])
    """
    return get_database_tables(db)


@st.cache_data(show_spinner=SHOW_SPINNERS, ttl=MAX_QUERY_HOLD_TIME)
def get_cols(table: str, database: str):
    """
    Similar to get_tables, except that you can cross-reference with a given table name.
    :param table: Table name as string ex:'Orders'
    :param db: Database name as a string ex:'BWSdb'
    :return: pd.DataFrame(columns=["TABLE_CATALOG", "TABLE_NAME", "COLUMN_NAME", "PRIMARY_KEY", "DATA_TYPE", "CHARACTER_MAXIMUM_LENGTH"])
    """
    # st.write(f"GET_COLS -> {table=}, {database=}")
    return get_table_cols(table, database, use_streamlit_cache=True)


# with grid["content_row_2"]:
# if "df_search_cols_result" not in st.session_state:
#     search_server3_tables()

# sm_tabs = pills("Server Maintenance", options=sm_tab_names, label_visibility="hidden")
# if sm_tabs == sm_tab_names[0]:
#     st.header("Server3 Table Column Finder")
#
#     input_db_cols = st.columns(len(list_databases) + 1)
#     radio_search_rtype = input_db_cols[0].radio(
#         label="Databases:",
#         options=list_col_search_rtypes,
#         key="radio_col_search_rtype"
#     )
#     toggles_dbs = []
#     for i, db in enumerate(list_databases):
#         toggles_dbs.append(
#             input_db_cols[i + 1].toggle(
#                 label=db,
#                 key=f"toggle_db_{db}"
#             )
#         )
#     # self.list_tv_rb_db, self.list_rb_db_bts = checkbox_factory(
#     #     self.frame_db_btns,
#     #     buttons=self.list_databases,
#     #     default_values=[True for _ in self.list_databases]
#     # )
#
#     # self.tv_lbl_search_input, self.lbl_search_input, self.tv_search_input, self.search_input = entry_factory(
#     #     self,
#     #     tv_label="Search Term:",
#     #     kwargs_entry={
#     #         "width": 100,
#     #         "justify": tkinter.CENTER
#     #     }
#     # )
#     cols_button_row = st.columns([0.8, 0.2, 0.2])
#     text_col = cols_button_row[0].text_input(
#         label="Column Name:",
#         key="text_column_search",
#         placeholder="Enter a column name to search each table in the selected databases"
#     )
#     button_col_search_clear = cols_button_row[1].button(
#         label="clear",
#         on_click=lambda: st.session_state.update({"text_column_search": ""})
#     )
#     button_col_search_submit = cols_button_row[2].button(
#         label="search",
#         on_click=search_server3_tables
#     )
#
#     st.dataframe(
#         st.session_state.get("df_search_cols_result"),
#         hide_index=True,
#         use_container_width=True
#     )

# if sm_tabs == sm_tab_names[1]:
# SQL Creator

list_query_types: list[str] = ["SELECT", "UPDATE", "INSERT", "DELETE", "CREATE"]
list_join_options: list[str] = ["INNER", "LEFT", "RIGHT", "CROSS", "FULL"]

input_db_cols = st.columns(len(list_databases) + 1)
input_table_cols = st.container(border=1)
input_join_cols = st.columns([0.35, 0.65])
radio_query_type = input_db_cols[0].radio(
    label="Query Type:",
    key="radio_query_type",
    options=list_query_types,
    disabled=False
)
toggles_dbs = []
db_options_0 = []
for i, db in enumerate(list_databases):
    k = f"toggle_db_{db}"
    toggles_dbs.append(
        input_db_cols[i + 1].toggle(
            label=db,
            key=k
        )
    )
    v = st.session_state.get(k, False)
    if v:
        df_tables = get_tables(db)
        for j, table_name in enumerate(df_tables["TABLE_NAME"].dropna().unique()):
            db_options_0.append(f"{wrap(db)}.[dbo].{wrap(table_name)}")

    # table_catalog = row["TABLE_CATALOG"]
    # table_name = row["TABLE_NAME"]
    # col_name = row["COLUMN_NAME"]
    # p_key = row["PRIMARY_KEY"]
    # d_type = row["DATA_TYPE"]
    # char_max_len = row["CHARACTER_MAXIMUM_LENGTH"]

if radio_query_type == "CREATE":
#
#     # default columns for Boilerplate info
#     records = [
#         {
#             "Name": "ID",
#             "Type": "int",
#             "Size": None,
#             "Default": None
#         },
#         {
#             "Name": "DateCreated",
#             "Type": "datetime",
#             "Size": None,
#             "Default": "GETDATE()"
#         },
#         {
#             "Name": "LastModified",
#             "Type": "datetime",
#             "Size": None,
#             "Default": None
#         },
#         {
#             "Name": "Active",
#             "Type": "bit",
#             "Size": None,
#             "Default": 1
#         },
#         {
#             "Name": "DateActive",
#             "Type": "datetime",
#             "Size": None,
#             "Default": None
#         },
#         {
#             "Name": "DateInActive",
#             "Type": "datetime",
#             "Size": None,
#             "Default": None
#         }
#     ]
#     boilerplate_cols = [d["Name"] for d in records]
#
#     # New Column template data
#     ct_column_names = ["PK", "Name", "Type", "Size", "Default"]
#     ct_type_options = ["str", "int", "decimal", "float", "date", "datetime", "bit"]
#     ct_size_options = {
#         "str": range(1, 6000001),
#         "int": "na",
#         "decimal": [f"{a_}, {b_})" for a_ in range(2, 19) for b_ in range(1, 18) if (a_ - 1) >= b_],
#         "float": [f"({a_}, {b_})" for a_ in range(2, 19) for b_ in range(1, 18) if (a_ - 1) >= b_],
#         "date": "na",
#         "datetime": "na"
#     }
#
#     ct_text_db_name = input_table_cols.text_input(
#         label="Database Name:",
#         key=f"ct_text_db_name"
#     )
#     ct_text_table_name = input_table_cols.text_input(
#         label="Table Name:",
#         key=f"ct_text_table_name"
#     )
#
#     cols_ct_control = input_table_cols.columns(2)
#     with cols_ct_control[0].container(border=1):
#         with st.popover(label="info"):
#             st.write("Add these 6 boiler-plate identification columns to your table.")
#             st.write(
#                 "These exact column names are used when generating the associating triggers and backup table scripts.")
#             st.code(("""
# [ID] [int] IDENTITY(0, 1) NOT NULL,
# [DateCreated] [datetime] NULL,
# [LastModified] [datetime] NULL,
# [Active] [bit] NULL,
# [DateActive] [datetime] NULL,
# [DateInActive] [datetime] NULL
#                     """).strip(),
#                     language="sql",
#                     line_numbers=True
#                     )
#         if st.button(
#                 label="Add 6 Boilerplate cols"
#         ):
#             df_ct_nc = pd.DataFrame(
#                 data=records,
#                 columns=ct_column_names
#             )
#             df_ct_nc.loc[df_ct_nc["Name"] == "ID", "PK"] = 1
#             st.session_state.update({
#                 "ct_data": df_ct_nc
#             })
#             st.rerun()
#
#     with cols_ct_control[1].container(border=1):
#         # # [Name], [Comments], [LastModifiedBy], [Price], [Description], [ModelName]
#         # # FKs
#         general_cols = [
#             {
#                 "Name": "Name",
#                 "Label": "[Name] [NVARCHAR](50)",
#                 "Type": "str",
#                 "Size": 50,
#                 "Default": None
#             },
#             {
#                 "Name": "LastModifiedBy",
#                 "Label": "[LastModifiedBy] [NVARCHAR](50)",
#                 "Type": "str",
#                 "Size": 50,
#                 "Default": None
#             },
#             {
#                 "Name": "Comments",
#                 "Label": "[Comments] [NVARCHAR](MAX)",
#                 "Type": "str",
#                 "Size": ct_size_options["str"][-1],
#                 "Default": None
#             },
#             {
#                 "Name": "Description",
#                 "Label": "[Description] [NVARCHAR](MAX)",
#                 "Type": "str",
#                 "Size": ct_size_options["str"][-1],
#                 "Default": None
#             },
#             {
#                 "Name": "Price",
#                 "Label": "[Price] [DECIMAL](18, 2) (DEFAULT=0)",
#                 "Type": "decimal",
#                 "Size": "(18, 2)",
#                 "Default": 0
#             }
#         ]
#         cols_ct_general_cols = st.columns(len(general_cols))
#         for i, data in enumerate(general_cols):
#             col_name = data.get("Name")
#             col_label = data.get("Label")
#             col_type = data.get("Type")
#             col_size = data.get("Size")
#             col_default = data.get("Default")
#             with cols_ct_general_cols[i]:
#                 if st.button(
#                     label=f"{col_label}",
#                     key=f"ct_btn_general_col_{i}"
#                 ):
#                     if not st.session_state.get("ct_data").loc[st.session_state.get("ct_data")["Name"] == col_name].empty:
#                         st.error(f"Cannot add {col_label} (NAME='{col_name}'), as it already exists in the columns list.")
#                     else:
#                         df_ct_nc = pd.DataFrame(
#                             data=[
#                                 {
#                                     "Name": col_name,
#                                     "Type": col_type,
#                                     "Size": col_size,
#                                     "Default": col_default
#                                 }
#                             ],
#                             columns=ct_column_names
#                         )
#                         st.session_state.update({
#                             "ct_data": pd.concat([
#                                 st.session_state.get("ct_data"),
#                                 df_ct_nc
#                             ]).reset_index(drop=True)
#                         })
#                         st.rerun()
#
#     input_table_cols.subheader("Columns:")
#     if "ct_data" not in st.session_state:
#         ct_data = pd.DataFrame(columns=ct_column_names)
#         st.session_state.update({"ct_data": ct_data})
#     else:
#         ct_data = st.session_state.get("ct_data")
#
#
#     # ct_input_table = input_table_cols[0].data_editor(
#     #     data=pd.DataFrame(columns=ct_columns),
#     #     column_config={
#     #         "decimal": st.column_config.SelectboxColumn(
#     #             "Size",
#     #             options=ct_type_options
#     #         )
#     #     }
#     # )
#
#     def update_cb_pk(key: str, i: int):
#         print(f"{key=}")
#         for j, row in ct_data.iterrows():
#             ct_data.loc[j, "PK"] = 1 if i == j else 0
#             # if k != key:
#             #     st.session_state.update({k: False})
#             #     df_ct_nc.loc[df_ct_nc["index"] == i, "PK"] = 1
#             # else:
#             #     st.session_state.update({k: True})
#             #     df_ct_nc.loc[df_ct_nc["index"] == i, "PK"] = 1
#         st.session_state.update({
#             "ct_data": ct_data
#         })
#         st.rerun()
#
#     def update_cn(idx: int, direction: int):
#         df = st.session_state.get("ct_data")
#         a, b = (idx - 1, idx) if direction == -1 else (idx, idx + 1)
#         df.loc[a], df.loc[b] = df.loc[b].copy(), df.loc[a].copy()
#         df = df.reset_index(drop=True)
#         st.session_state.update({"ct_data": df})
#
#     def delete_cn(idx: int):
#         df: pd.DataFrame = st.session_state.get("ct_data")
#         # a, b = (idx - 1, idx) if direction == -1 else (idx, idx + 1)
#         # df.loc[a], df.loc[b] = df.loc[b].copy(), df.loc[a].copy()
#         df.drop(index=idx, inplace=True)
#         df = df.reset_index(drop=True)
#         st.session_state.update({"ct_data": df})
#
#     def edit_cn(idx: int):
#         col_name = ct_data.loc[idx, "Name"]
#         col_type = ct_data.loc[idx, "Type"]
#         col_size = ct_data.loc[idx, "Size"]
#         col_default = ct_data.loc[idx, "Default"]
#         st.session_state.update({
#             "ct_nc_editing": True,
#             "ct_nc_editing_revert_idx": idx,
#             "ct_nc_text_input_name": col_name,
#             "ct_nc_text_input_type": col_type,
#             "ct_nc_slider_size": col_size,
#             "ct_default_text_input": col_default
#         })
#         delete_cn(idx)
#
#     def update_selectbox_size():
#         size = st.session_state.get("ct_nc_select_box_size", "MAX")
#         if size == "MAX":
#             size = ct_size_options["str"][-1]
#         st.session_state.update({
#             "ct_nc_slider_size": int(size)
#         })
#
#
#     ct_columns = input_table_cols.columns(1 + len(ct_column_names), border=0)
#     # input_table_cols.write("---")
#     st.dataframe(ct_data)
#     list_cb_pk_keys = []
#     cont_height = 75
#     for i, col in enumerate(ct_column_names, start=1):
#         with ct_columns[i]:
#             # container_btn_bar = st.container(height=25)
#             with st.container(height=cont_height):
#                 st.write(col)
#     with ct_columns[0]:
#         with st.container(height=cont_height):
#             st.empty()
#     for i, row in ct_data.iterrows():
#         ct_pk = row["PK"]
#         ct_name = row["Name"]
#         ct_type = row["Type"]
#         ct_size = row["Size"]
#         ct_def = row["Default"]
#
#         ct_pk = 0 if pd.isna(ct_pk) else bool(ct_pk)
#         with ct_columns[0]:
#             # container_btn_bar = st.container(height=25)
#             btn_bar = st.container(height=cont_height).columns(4, gap="small")
#             if i > 0:
#                 btn_bar[0].button(
#                     label="^",
#                     key=f"ct_btn_col_up_{i}",
#                     on_click=lambda i_=i: update_cn(i_, -1)
#                 )
#             if i < ct_data.shape[0] - 1:
#                 btn_bar[1].button(
#                     label="v",
#                     key=f"ct_btn_col_down_{i}",
#                     on_click=lambda i_=i: update_cn(i_, 1)
#                 )
#             btn_bar[2].button(
#                 label="edit",
#                 key=f"ct_btn_col_edit_{i}",
#                 type="secondary",
#                 on_click=lambda i_=i: edit_cn(i_)
#             )
#             btn_bar[3].button(
#                 label="del",
#                 key=f"ct_btn_col_delete_{i}",
#                 type="primary",
#                 on_click=lambda i_=i: delete_cn(i_)
#             )
#             # st.write("CONTROLS")
#         with ct_columns[1]:
#             k = f"ct_nc_checkbox_pk_{i}"
#             list_cb_pk_keys.append(k)
#             st.session_state.update({k: ct_pk})
#             with st.container(height=cont_height):
#                 st.checkbox(
#                     label="pk",
#                     key=k,
#                     label_visibility="hidden",
#                     on_change=lambda key_=k, i_=i: update_cb_pk(key_, i_)
#                 )
#         with ct_columns[2]:
#             with st.container(height=cont_height):
#                 st.write(ct_name)
#         with ct_columns[3]:
#             with st.container(height=cont_height):
#                 st.write(ct_type)
#         with ct_columns[4]:
#             with st.container(height=cont_height):
#                 st.write(ct_size)
#         with ct_columns[5]:
#             ct_def = None if not ct_def else ct_def
#             with st.container(height=cont_height):
#                 st.write(ct_def)
#         # input_table_cols.write(f"{i=}, {row=}")
#     if ct_data.shape[0] == 0:
#         input_table_cols.write("0 columns")
#     # input_table_cols.write("---")
#
#     ct_nc_editing: bool = st.session_state.get("ct_nc_editing", False)
#
#     if ct_nc_editing or input_table_cols.button(
#         label="Add Column",
#         key=f"ct_btn_add_new_column"
#     ):
#         st.session_state.update({"ct_nc_editing": True})
#         ct_nc_text_input_name = ct_columns[2].text_input(
#             label="Name",
#             key="ct_nc_text_input_name"
#         )
#         if st.session_state.get("ct_nc_text_input_name"):
#             ct_nc_text_input_type = ct_columns[3].selectbox(
#                 label="Type",
#                 key="ct_nc_text_input_type",
#                 options=ct_type_options
#             )
#             ct_type = st.session_state.get("ct_nc_text_input_type")
#             if ct_type:
#                 validator = ct_size_options[ct_type]
#                 size_key = ""
#                 if validator != "na":
#                     if ct_type == "str":
#                         size_key = "ct_nc_slider_size"
#                         if "ct_nc_select_box_size" not in st.session_state:
#                             st.session_state.update({
#                                 "ct_nc_select_box_size": "MAX"
#                             })
#                             update_selectbox_size()
#                         ct_nc_slider_size = ct_columns[4].slider(
#                             label="Size",
#                             key=size_key,
#                             min_value=validator[0],
#                             max_value=validator[-1]
#                         )
#                         ct_nc_select_box_size = ct_columns[4].selectbox(
#                             label="Size",
#                             key="ct_nc_select_box_size",
#                             options=["25", "50", "255", "511", "1023", "MAX"],
#                             label_visibility="hidden",
#                             on_change=update_selectbox_size
#                         )
#                     elif ct_type in ["float", "decimal"]:
#                         size_key = "ct_nc_select_box_size"
#                         ct_nc_select_box_size = ct_columns[4].selectbox(
#                             label="Size",
#                             key=size_key,
#                             options=validator
#                         )
#
#                 ct_default_text_input = ct_columns[5].text_input(
#                     label="Default Value",
#                     key="ct_default_text_input"
#                 )
#
#                 ct_save_new_column_disabled = False
#                 ct_nc_name = st.session_state.get("ct_nc_text_input_name")
#                 ct_nc_type = st.session_state.get("ct_nc_text_input_type")
#                 ct_nc_size = st.session_state.get(size_key)
#                 ct_nc_default = st.session_state.get("ct_default_text_input")
#
#                 if ct_nc_default:
#                     if ct_nc_type in ("str", "float", "decimal"):
#                         # check size of default
#                         if len(ct_nc_default) > ct_nc_size:
#                             input_table_cols.warning(
#                                 f"default value '{ct_nc_default}' cannot exceed the size '{ct_nc_size}'."
#                             )
#                     if ct_nc_type in ("int", "float", "decimal", "bit"):
#                         # validate number types:
#                         if not isnumber(ct_nc_default):
#                             input_table_cols.warning(
#                                 f"default value '{ct_nc_default}' must be a number for this field."
#                             )
#                     if ct_nc_type in ("date", "datetime"):
#                         # validate date types
#                         date_val = is_date(ct_nc_default)
#                         if ct_nc_default.lower() == "getdate()":
#                             date_val = "GETDATE()"
#                         elif date_val is None:
#                             input_table_cols.warning(
#                                 f"default value '{ct_nc_default}' must be a date for this field."
#                             )
#
#                 if input_table_cols.button(
#                         label="save",
#                         key=f"ct_save_new_column",
#                         disabled=ct_save_new_column_disabled
#                 ):
#                     record = {
#                         "Name": st.session_state.get("ct_nc_text_input_name"),
#                         "Type": st.session_state.get("ct_nc_text_input_type"),
#                         "Size": st.session_state.get(size_key),
#                         "Default": st.session_state.get("ct_default_text_input")
#                     }
#                     col_names = list(map(str.lower, ct_data["Name"].tolist()))
#                     if ct_nc_name.lower() in col_names:
#                         input_table_cols.warning(
#                             f"Cannot insert another column with the name '{ct_nc_name}', only one instance per table."
#                         )
#                     else:
#                         ct_nc_editing_revert_idx = st.session_state.get("ct_nc_editing_revert_idx")
#                         if ct_nc_editing_revert_idx is not None:
#                             ct_data = pd.concat([
#                                 ct_data[:ct_nc_editing_revert_idx],
#                                 pd.DataFrame(data=[record], columns=ct_column_names),
#                                 ct_data[ct_nc_editing_revert_idx:]
#                             ]).reset_index(drop=True)
#                         else:
#                             ct_data = pd.concat([
#                                 ct_data,
#                                 pd.DataFrame(data=[record], columns=ct_column_names)
#                             ]).reset_index(drop=True)
#                         st.session_state.update({
#                             "ct_data": ct_data,
#                             "ct_nc_editing": False,
#                             "ct_nc_editing_revert_idx": None
#                         })
#                         st.rerun()
#
#     st.session_state.setdefault("user_full_name", get_windows_user())
#     user_name = st.session_state.get("user_full_name", "FULL NAME")
#     table_name = wrap(st.session_state.get("ct_text_table_name", "UNNAMED"), is_col=True, sanitize=True).removeprefix("[").removesuffix("]")
#     db_name = wrap(st.session_state.get("ct_text_db_name", "UNNAMED"), is_col=True, sanitize=True).removeprefix("[").removesuffix("]")
#     need_db_and_table_names = (not len(f"{db_name}".strip())) or (not len(f"{table_name}".strip()))
#
#     if need_db_and_table_names:
#         input_table_cols.warning("Please specify the Database and New Table Names above.")
#
#     if input_table_cols.button(
#             label="Generate SQL",
#             key="ct_btn_generate_sql",
#             disabled=need_db_and_table_names
#     ):
#         if ct_data.shape[0] > 0:
#             now = datetime.datetime.now()
#             create_table_sql = f"\n/****** Object:  Table [dbo].[{{TABLE_NAME}}]    Script Date: {now:%Y-%m-%d %H:%M:%S} ******/"
#             create_table_sql += "\n" + (f"""
# USE [{db_name}]
# GO
#
# SET ANSI_NULLS ON
# GO
#
# SET QUOTED_IDENTIFIER ON
# GO
#
#
# -- =============================================
# -- Author:\t\t<{user_name}>
# -- Create date:\t<{now:%Y-%m-%d %H:%M:%S}>
# -- Description:\t<Create Table [{db_name}].[dbo].[{{TABLE_NAME}}]>
# -- =============================================
#                 """).strip()
#             create_table_sql += "\n" + (f"""
# CREATE TABLE [dbo].[{{TABLE_NAME}}] (
#                 """).strip()
#
#             sql = create_table_sql.format(TABLE_NAME=table_name)
#             sql_hist = create_table_sql.format(TABLE_NAME=f"hist_{table_name}")
#             sql_hist_trig = f"""
#
#             WIP 2025-01-14 0410
#
# USE [{db_name}]
# GO
#
# /****** Object:  Trigger [dbo].[tr_Update{table_name}History]    Script Date: {now:%Y-%m-%d %H:%M:%S} ******/
# SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
#
# -- =============================================
# -- Author:\t\t<{user_name}>
# -- Create date:\t<{now:%Y-%m-%d %H:%M:%S}>
# -- Description:\t<Maintain History Table>
# -- =============================================
# CREATE TRIGGER [dbo].[tr_Update{table_name}History]
# ON [dbo].[{table_name}]
# AFTER INSERT, DELETE, UPDATE
# AS
# BEGIN
#     -- SET NOCOUNT ON added to prevent extra result sets from
#     -- interfering with SELECT statements.
#     SET NOCOUNT ON;
#
#     -- Prevent recursive calls
#     IF TRIGGER_NESTLEVEL() > 1 BEGIN
#         RETURN;
#     END
#
#     INSERT INTO
#         [{db_name}].[dbo].[hist_{table_name}]
#     (
#         [ModifiedID],
#         [ModifiedBy],
#         [ModifiedColumn],
#         [Modification],
#         [ValueBefore],
#         [ValueAfter]
#     )
#     SELECT
#         [C].[ID],
#         NULL,
#         (CASE
#             WHEN ([D].[Name] IS NULL) AND ([C].[Name] IS NOT NULL) THEN 'Name'
#             WHEN ([I].[Name] IS NULL) AND ([D].[Name] IS NOT NULL) THEN 'Name'
#             WHEN [D].[Name] <> [C].[Name] THEN 'Name'
#             ELSE NULL
#         END) AS [ModifiedColumn],
#         (CASE
#             WHEN ([D].[Name] IS NULL) AND ([C].[Name] IS NOT NULL) THEN 'INSERT'
#             WHEN ([I].[Name] IS NULL) AND ([D].[Name] IS NOT NULL) THEN 'DELETE'
#             WHEN [D].[Name] <> [C].[Name] THEN 'UPDATE'
#             ELSE NULL
#         END) AS [Modification],
#         [D].[Name] AS [ValueBefore],
#         [D].[Name] AS [ValueAfter]
#     FROM
#         [{db_name}].[dbo].[{table_name}] [C]
#     INNER JOIN
#         INSERTED [I]
#     ON
#         [C].[ID] = [I].[ID]
#     LEFT JOIN
#         DELETED [D]
#     ON
#         [C].[ID] = [D].[ID]
#     WHERE
#         (CASE
#             WHEN ([D].[Name] IS NULL) AND ([C].[Name] IS NOT NULL) THEN 1
#             WHEN ([I].[Name] IS NULL) AND ([D].[Name] IS NOT NULL) THEN 1
#             WHEN [D].[Name] <> [C].[Name] THEN 1
#             ELSE 0
#         END) > 0
#     ;
# END
#                     """.strip()
#
#             pk_col = None
#             default_values = []
#             bp_cols_copy = boilerplate_cols.copy()
#             has_clr_type: bool = False
#             for i, row in ct_data.iterrows():
#                 ct_nc_pk = row["PK"]
#                 ct_nc_name = row["Name"]
#                 ct_nc_type = row["Type"]
#                 ct_nc_size = row["Size"]
#                 ct_nc_def = row["Default"]
#
#                 try:
#                     bp_cols_copy.remove(ct_nc_name)
#                 except ValueError:
#                     pass
#
#                 ct_nc_pk = False if (pd.isna(ct_nc_pk) or (not ct_nc_pk)) else ct_nc_pk
#
#                 if ct_nc_size == ct_size_options["str"][-1]:
#                     ct_nc_size = "max"
#
#                 # if not ct_cn_def:
#                 #     ct_cn_def = "NULL"
#
#                 if not has_clr_type:
#                     # text, ntext, image, varchar(max), nvarchar(max), non - FILESTREAM, varbinary(max), xml or large CLR type columns.
#                     has_clr_type = (ct_nc_type == "str") and (ct_nc_size == "max")
#
#                 l_sql = ""
#
#                 if ct_nc_def:
#                     default_values.append((ct_nc_name, ct_nc_def))
#
#                 st.write(f"{ct_nc_type=}")
#
#                 match ct_nc_type:
#                     case "str":
#                         if not ct_nc_pk:
#                             l_sql = f"\n\t[{ct_nc_name}] [nvarchar]({ct_nc_size}) NULL"
#                         else:
#                             # l_sql = f"\n\t[{ct_cn_name}] [nvarchar]({ct_nc_size}) IDENTITY(0, 1) NOT NULL"
#                             st.error(f"Cannot use {ct_nc_type} values as PKs. Feature coming soon")
#                     case "date" | "datetime" | "bit" | "float":
#                         if not ct_nc_pk:
#                             l_sql = f"\n\t[{ct_nc_name}] [{ct_nc_type}] NULL"
#                         else:
#                             st.error(f"Cannot use {ct_nc_type} values as PKs.")
#                     case "decimal":
#                         if not ct_nc_pk:
#                             a, b = eval(ct_nc_size)
#                             l_sql = f"\n\t[{ct_nc_name}] [{ct_nc_type}]({a}, {b}) NULL"
#                         else:
#                             st.error(f"Cannot use {ct_nc_type} values as PKs.")
#                     case "int":
#                         if not ct_nc_pk:
#                             l_sql = f"\n\t[{ct_nc_name}] [int] NULL"
#                         else:
#                             l_sql = f"\n\t[{ct_nc_name}] [int] IDENTITY(0, 1) NOT NULL"
#                             pk_col = ct_nc_name
#                     case _:
#                         st.error("UNSURE")
#
#                 sql += f"\n\t{l_sql.strip()},"
#
#             #                     sql += """
#             # [ID] [int] IDENTITY(0,1) NOT NULL,
#             # [DateCreated] [datetime] NULL,
#             # [LastModified] [datetime] NULL,
#             # [Active] [bit] NULL,
#             # [DateActive] [datetime] NULL,
#             # [DateInActive] [datetime] NULL,
#             #
#             # [NHLAPI_ID] [nvarchar](10) NULL,
#             #
#             # [Name] [nvarchar](255) NULL,
#             # [Description] [nvarchar](max) NULL,
#             # [Comments] [nvarchar](max) NULL,
#
#             sql = sql.removesuffix(",")
#
#             # custom columns list for history table
#             sql_hist += "\n\t" + ("""
#     [ID] [int] IDENTITY(0, 1) NOT NULL,
#     [DateCreated] [datetime] NULL,
#     [ModifiedID] [int] NULL,
#     [ModifiedBy] [nvarchar](50) NULL,
#     [ModifiedColumn] [nvarchar(512)] NULL,
#     [Modification] [nvarchar(50)] NULL,
#     [ValueBefore] [nvarchar](max) NULL,
#     [ValueAfter] [nvarchar](max) NULL
#                     """).strip()
#
#             # consider CLR type columns
#             clr_type = " ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]" if has_clr_type else ""
#             if pk_col:
#                 sql += "\n\n\t" + (f"""
# CONSTRAINT [PK_{table_name}] PRIMARY KEY CLUSTERED (
#         [{pk_col}] ASC
#     )
#     WITH (
#         PAD_INDEX = OFF,
#         STATISTICS_NORECOMPUTE = OFF,
#         IGNORE_DUP_KEY = OFF,
#         ALLOW_ROW_LOCKS = ON,
#         ALLOW_PAGE_LOCKS = ON
#         --, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
#     ) ON [PRIMARY]
# ){clr_type}
# GO
#                     """).strip()
#             sql_hist += "\n\n\t" + (f"""
# CONSTRAINT [PK_hist_{table_name}] PRIMARY KEY CLUSTERED (
#         [ID] ASC
#     )
#     WITH (
#         PAD_INDEX = OFF,
#         STATISTICS_NORECOMPUTE = OFF,
#         IGNORE_DUP_KEY = OFF,
#         ALLOW_ROW_LOCKS = ON,
#         ALLOW_PAGE_LOCKS = ON
#         --, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
#     ) ON [PRIMARY]
# ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
# GO
#                 """).strip()
#
#             # add columns with default values
#             for col, val in default_values:
#                 val = val if str(val).strip().endswith("()") else f"({val})"
#                 sql += "\n\n" + (f"""
# IF (EXISTS (SELECT *
#     FROM INFORMATION_SCHEMA.TABLES
#     WHERE (([TABLE_SCHEMA] = 'dbo')
#     AND (TABLE_NAME = '{table_name}'))))
# BEGIN
#                 """).strip()
#                 sql += f"\n\tALTER TABLE [dbo].[{table_name}] ADD CONSTRAINT [DF_{table_name}_{col}] DEFAULT ({val}) FOR [{col}];"
#                 sql += "\nEND\nGO"
#
#             # add history column defaults
#             sql_hist += "\n\n" + (f"""
# IF (EXISTS (SELECT *
#     FROM INFORMATION_SCHEMA.TABLES
#     WHERE (([TABLE_SCHEMA] = 'dbo')
#     AND (TABLE_NAME = 'hist_{table_name}'))))
# BEGIN
#                 """).strip()
#             sql_hist += f"\n\tALTER TABLE [dbo].[hist_{table_name}] ADD CONSTRAINT [DF_hist_{table_name}_DateCreated] DEFAULT (GETDATE()) FOR [DateCreated];"
#             sql_hist += "\nEND\nGO"
#
#             # code for table create
#             input_table_cols.subheader("Step 1  - CREATE TABLE")
#             input_table_cols.code(sql, language="sql", line_numbers=True)
#
#             if bp_cols_copy:
#                 st.warning(
#                     f"Cannot infer Boilerplate Trigger because traditional boilerplate cols: [{', '.join(bp_cols_copy)}] could not be found. Please use the 'Boilerplate button to ensure the correct naming conventions are used.'")
#             else:
#
#                 # code for back-up table creation
#                 input_table_cols.subheader("Step 2  - CREATE Back-up TABLE")
#                 input_table_cols.code(sql_hist, language="sql", line_numbers=True)
#
#                 sql_trig = f"""
# USE [{db_name}]
# GO
#
# /****** Object:  Trigger [dbo].[tr_Update{table_name}BoilerPlate]    Script Date: {now:%Y-%m-%d %H:%M:%S} ******/
# SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
#
# -- =============================================
# -- Author:\t\t<{user_name}>
# -- Create date:\t<{now:%Y-%m-%d %H:%M:%S}>
# -- Description:\t<Maintain Boilerplate Columns>
# -- =============================================
# CREATE TRIGGER [dbo].[tr_Update{table_name}BoilerPlate]
# ON [dbo].[{table_name}]
# AFTER INSERT, DELETE, UPDATE
# AS
# BEGIN
# -- SET NOCOUNT ON added to prevent extra result sets from
# -- interfering with SELECT statements.
# SET NOCOUNT ON;
#
# -- Prevent recursive calls
# IF TRIGGER_NESTLEVEL() > 1 BEGIN
#     RETURN;
# END
#
# UPDATE
#     [{db_name}].[dbo].[{table_name}]
# SET
#     [LastModified] = GETDATE()
#     , [DateCreated] = ISNULL([C].[DateCreated], GETDATE())
#     , [DateActive] = (CASE
#         WHEN ([I].[Active] = 1) AND (([D].[Active] IS NULL) OR ([D].[Active] = 0)) THEN
#             GETDATE()
#         ELSE
#             [C].[DateActive]
#         END
#     )
#     , [DateInactive] = (CASE
#         WHEN ([I].[Active] = 0) AND (([D].[Active] IS NULL) OR ([D].[Active] = 1)) THEN
#             GETDATE()
#         ELSE
#             [C].[DateInActive]
#         END
#     )
# FROM
#     [{db_name}].[dbo].[{table_name}] [C]
# INNER JOIN
#     INSERTED [I]
# ON
#     [C].[ID] = [I].[ID]
# LEFT JOIN
#     DELETED [D]
# ON
#     [C].[ID] = [D].[ID]
# ;
# END
#                     """.strip()
#
#                 # code for boilerplate trigger creation
#                 input_table_cols.subheader("Step 3  - CREATE Boilerplate TRIGGER")
#                 input_table_cols.code(sql_trig, language="sql", line_numbers=True)
#
#                 # code for history trigger creation
#                 input_table_cols.subheader("Step 4  - CREATE History TRIGGER")
#                 input_table_cols.code(sql_hist_trig, language="sql", line_numbers=True)
#         else:
#             st.warning(
#                 "Please enter some column information first."
#             )
#
# else:
#
#     if st.session_state.get("radio_query_type" != "SELECT"):
#         st.session_state.update({"radio_query_type": "SELECT"})
#         st.rerun()
#
#     selectbox_table_0 = input_table_cols.selectbox(
#         label="Select a table:",
#         key="selectbox_table_0",
#         options=db_options_0
#     )
#
#     toggle_use_alias = input_table_cols.toggle(
#         label="Use Aliasing?",
#         key="toggle_use_alias"
#     )
#
#     if st.session_state.get("toggle_use_alias", True):
#         text_input_alias_0 = input_table_cols.text_input(
#             label="Alias: (SELECT * FROM [Table] AS #ALIAS#)",
#             key="text_input_alias_0",
#             placeholder="If left blank, the first letter of the table will be used."
#         )
#
#         toggle_use_join_0 = input_join_cols[0].toggle(
#             label="Add a JOIN?",
#             key="toggle_use_join_0"
#         )
#
#         if st.session_state.get("toggle_use_join_0", False):
#             db_options_1 = db_options_0.copy()
#             db_options_1.remove(selectbox_table_0)
#             cols_table_0 = get_cols(selectbox_table_0, selectbox_table_0)["COLUMN_NAME"].values.tolist()
#             radio_join_type_1 = input_join_cols[0].radio(
#                 label="Join type:",
#                 key="radio_join_type_1",
#                 options=list_join_options,
#                 horizontal=True
#             )
#             if st.session_state.get("radio_join_type_1") in ("LEFT", "RIGHT", "FULL"):
#                 toggle_join_type_is_outer = input_join_cols[0].toggle(
#                     label="OUTER",
#                     key="toggle_join_type_is_outer"
#                 )
#                 input_join_cols[0].write(
#                     f":red[WARNING - OUTER JOINS are missing an appropriate WHERE CLAUSE. Coming soon -- 2024-12-04]")
#             if st.session_state.get("radio_join_type_1") != "CROSS":
#                 selectbox_table_0_pk = input_join_cols[0].selectbox(
#                     label="Primary Key(s)",
#                     key="selectbox_table_0_pk",
#                     options=cols_table_0
#                 )
#             selectbox_table_1 = input_join_cols[1].selectbox(
#                 label="Select a table:",
#                 key="selectbox_table_1",
#                 options=db_options_1
#             )
#             text_input_alias_1 = input_join_cols[1].text_input(
#                 label="Alias for 1st JOINED Table",
#                 key="text_input_alias_1",
#                 placeholder="If left blank, the first letter of the table will be used."
#             )
#             cols_table_1 = get_cols(selectbox_table_1, selectbox_table_1)["COLUMN_NAME"].values.tolist()
#             if st.session_state.get("radio_join_type_1") != "CROSS":
#                 selectbox_table_1_pk = input_join_cols[1].selectbox(
#                     label="Primary Key(s)",
#                     key="selectbox_table_1_pk",
#                     options=cols_table_1
#                 )
#         else:
#             selectbox_table_1 = ""
#
#     else:
#         text_input_alias_0 = None
#
#     if st.button(
#             label="RUN"
#     ) and selectbox_table_0:
#         # st.code(
#         #     create_sql(
#         #         "Orders",
#         #         mode="update",
#         #         path_data={"Comments": None},
#         #         where="[Apples] = [Oranges]"
#         #     )
#         # )
#         # st.write(schema_parse("Orders"))
#         # st.write(schema_parse("[Orders]"))
#         # st.write(schema_parse("[dbo].[Orders]"))
#         # st.write(schema_parse("dbo.[Orders]"))
#         # st.write(schema_parse("dbo.Orders"))
#         # st.write(schema_parse("[dbo].Orders"))
#         # st.write(schema_parse("BWSdb.dbo.Orders"))
#         # st.write(schema_parse("[BWSdb].dbo.Orders"))
#         # st.write(schema_parse("BWSdb.[dbo].Orders"))
#         # st.write(schema_parse("BWSdb.dbo.[Orders]"))
#         # st.write(schema_parse("BWSdb.[dbo].[Orders]"))
#         # st.write(schema_parse("[BWSdb].[dbo].Orders"))
#         # st.write(schema_parse("[BWSdb].dbo.[Orders]"))
#         # st.write(schema_parse("[BWSdb].[dbo].[Orders]"))
#         # st.write(get_table_cols("Orders", "BWSdb"))
#         if text_input_alias_0 is not None:
#             # text_input_alias_0 = selectbox_table_0.split(".")[-1].removeprefix("[").removesuffix("]")
#             if not text_input_alias_0:
#                 text_input_alias_0 = schema_parse(selectbox_table_0)[1][0]
#             if not selectbox_table_1:
#                 code = select_with_alias(
#                     selectbox_table_0,
#                     alias=text_input_alias_0,
#                 )
#             else:
#                 if not text_input_alias_1:
#                     text_input_alias_1 = schema_parse(selectbox_table_1)[1][0]
#                 if radio_join_type_1 != "CROSS":
#                     code = select_with_alias(
#                         [
#                             (selectbox_table_0, text_input_alias_0),
#                             (selectbox_table_1, text_input_alias_1)
#                         ],
#                         f_keys=(
#                             radio_join_type_1 + f" {'OUTER' if st.session_state.get('toggle_join_type_is_outer', False) else ''}".rstrip(),
#                             selectbox_table_0_pk,
#                             selectbox_table_1_pk
#                         )
#                     )
#                 else:
#                     code = select_with_alias(
#                         [
#                             (selectbox_table_0, text_input_alias_0),
#                             (selectbox_table_1, text_input_alias_1)
#                         ]
#                     )
#         else:
#             code = create_sql(
#                 selectbox_table_0,
#                 in_line=False,
#                 fetch_cols=True
#             )
#         st.code(
#             code,
#             language="sql",
#             line_numbers=True
#         )

            # SQL Creator
    if 1:
        if 1:
            #
            # list_query_types: list[str] = ["SELECT", "UPDATE", "INSERT", "DELETE", "CREATE"]
            # list_join_options: list[str] = ["INNER", "LEFT", "RIGHT", "CROSS", "FULL"]
            #
            # input_db_cols = st.columns(len(list_databases) + 1)
            # input_table_cols = st.container(border=1)
            # input_join_cols = st.columns([0.35, 0.65])
            # radio_query_type = input_db_cols[0].radio(
            #     label="Query Type:",
            #     key="radio_query_type",
            #     options=list_query_types,
            #     disabled=False
            # )
            # toggles_dbs = []
            # db_options_0 = []
            # for i, db in enumerate(list_databases):
            #     k = f"toggle_db_{db}"
            #     toggles_dbs.append(
            #         input_db_cols[i + 1].toggle(
            #             label=db,
            #             key=k
            #         )
            #     )
            #     v = st.session_state.get(k, False)
            #     if v:
            #         df_tables = get_tables(db)
            #         for j, table_name in enumerate(df_tables["TABLE_NAME"].dropna().unique()):
            #             db_options_0.append(f"{wrap(db)}.[dbo].{wrap(table_name)}")
            #
            #     # table_catalog = row["TABLE_CATALOG"]
            #     # table_name = row["TABLE_NAME"]
            #     # col_name = row["COLUMN_NAME"]
            #     # p_key = row["PRIMARY_KEY"]
            #     # d_type = row["DATA_TYPE"]
            #     # char_max_len = row["CHARACTER_MAXIMUM_LENGTH"]

            if radio_query_type == "CREATE":
                # default columns for Boilerplate info
                records = [
                    {
                        "Name": "ID",
                        "Type": "int",
                        "Size": None,
                        "Default": None
                    },
                    {
                        "Name": "DateCreated",
                        "Type": "datetime",
                        "Size": None,
                        "Default": "GETDATE()"
                    },
                    {
                        "Name": "LastModified",
                        "Type": "datetime",
                        "Size": None,
                        "Default": None
                    },
                    {
                        "Name": "Active",
                        "Type": "bit",
                        "Size": None,
                        "Default": 1
                    },
                    {
                        "Name": "DateActive",
                        "Type": "datetime",
                        "Size": None,
                        "Default": None
                    },
                    {
                        "Name": "DateInActive",
                        "Type": "datetime",
                        "Size": None,
                        "Default": None
                    }
                ]
                boilerplate_cols = [d["Name"] for d in records]

                # New Column template data
                ct_column_names = ["PK", "Name", "Type", "Size", "Default"]
                ct_type_options = ["str", "int", "decimal", "float", "date", "datetime", "bit"]
                ct_size_options = {
                    "str": range(1, 6000001),
                    "int": "na",
                    "decimal": [f"{a_}, {b_})" for a_ in range(2, 19) for b_ in range(1, 18) if (a_ - 1) >= b_],
                    "float": [f"({a_}, {b_})" for a_ in range(2, 19) for b_ in range(1, 18) if (a_ - 1) >= b_],
                    "date": "na",
                    "datetime": "na"
                }

                ct_text_db_name = input_table_cols.text_input(
                    label="Database Name:",
                    key=f"ct_text_db_name"
                )
                ct_text_table_name = input_table_cols.text_input(
                    label="Table Name:",
                    key=f"ct_text_table_name"
                )

                cols_ct_control = input_table_cols.columns(2)
                with cols_ct_control[0].container(border=1):
                    with st.popover(label="info"):
                        st.write("Add these 6 boiler-plate identification columns to your table.")
                        st.write(
                            "These exact column names are used when generating the associating triggers and backup table scripts.")
                        st.code(("""
    [ID] [int] IDENTITY(0, 1) NOT NULL,
    [DateCreated] [datetime] NULL,
    [LastModified] [datetime] NULL,
    [Active] [bit] NULL,
    [DateActive] [datetime] NULL,
    [DateInActive] [datetime] NULL
                                    """).strip(),
                                language="sql",
                                line_numbers=True
                                )
                    if st.button(
                            label="Add 6 Boilerplate cols"
                    ):
                        df_ct_nc = pd.DataFrame(
                            data=records,
                            columns=ct_column_names
                        )
                        df_ct_nc.loc[df_ct_nc["Name"] == "ID", "PK"] = 1
                        st.session_state.update({
                            "ct_data": df_ct_nc
                        })
                        st.rerun()

                with cols_ct_control[1].container(border=1):
                    # # [Name], [Comments], [LastModifiedBy], [Price], [Description], [ModelName]
                    # # FKs
                    general_cols = [
                        {
                            "Name": "Name",
                            "Label": "[Name] [NVARCHAR](50)",
                            "Type": "str",
                            "Size": 50,
                            "Default": None
                        },
                        {
                            "Name": "LastModifiedBy",
                            "Label": "[LastModifiedBy] [NVARCHAR](50)",
                            "Type": "str",
                            "Size": 50,
                            "Default": None
                        },
                        {
                            "Name": "Comments",
                            "Label": "[Comments] [NVARCHAR](MAX)",
                            "Type": "str",
                            "Size": ct_size_options["str"][-1],
                            "Default": None
                        },
                        {
                            "Name": "Description",
                            "Label": "[Description] [NVARCHAR](MAX)",
                            "Type": "str",
                            "Size": ct_size_options["str"][-1],
                            "Default": None
                        },
                        {
                            "Name": "Price",
                            "Label": "[Price] [DECIMAL](18, 2) (DEFAULT=0)",
                            "Type": "decimal",
                            "Size": "(18, 2)",
                            "Default": 0
                        }
                    ]
                    cols_ct_general_cols = st.columns(len(general_cols))
                    for i, data in enumerate(general_cols):
                        col_name = data.get("Name")
                        col_label = data.get("Label")
                        col_type = data.get("Type")
                        col_size = data.get("Size")
                        col_default = data.get("Default")
                        with cols_ct_general_cols[i]:
                            if st.button(
                                    label=f"{col_label}",
                                    key=f"ct_btn_general_col_{i}"
                            ):
                                if not st.session_state.get("ct_data").loc[
                                    st.session_state.get("ct_data")["Name"] == col_name].empty:
                                    st.error(
                                        f"Cannot add {col_label} (NAME='{col_name}'), as it already exists in the columns list.")
                                else:
                                    df_ct_nc = pd.DataFrame(
                                        data=[
                                            {
                                                "Name": col_name,
                                                "Type": col_type,
                                                "Size": col_size,
                                                "Default": col_default
                                            }
                                        ],
                                        columns=ct_column_names
                                    )
                                    st.session_state.update({
                                        "ct_data": pd.concat([
                                            st.session_state.get("ct_data"),
                                            df_ct_nc
                                        ]).reset_index(drop=True)
                                    })
                                    st.rerun()

                input_table_cols.subheader("Columns:")
                if "ct_data" not in st.session_state:
                    ct_data = pd.DataFrame(columns=ct_column_names)
                    st.session_state.update({"ct_data": ct_data})
                else:
                    ct_data = st.session_state.get("ct_data")

                # ct_input_table = input_table_cols[0].data_editor(
                #     data=pd.DataFrame(columns=ct_columns),
                #     column_config={
                #         "decimal": st.column_config.SelectboxColumn(
                #             "Size",
                #             options=ct_type_options
                #         )
                #     }
                # )

                def update_cb_pk(key: str, i: int):
                    print(f"{key=}")
                    for j, row in ct_data.iterrows():
                        ct_data.loc[j, "PK"] = 1 if i == j else 0
                        # if k != key:
                        #     st.session_state.update({k: False})
                        #     df_ct_nc.loc[df_ct_nc["index"] == i, "PK"] = 1
                        # else:
                        #     st.session_state.update({k: True})
                        #     df_ct_nc.loc[df_ct_nc["index"] == i, "PK"] = 1
                    st.session_state.update({
                        "ct_data": ct_data
                    })
                    st.rerun()

                def update_cn(idx: int, direction: int):
                    df = st.session_state.get("ct_data")
                    a, b = (idx - 1, idx) if direction == -1 else (idx, idx + 1)
                    df.loc[a], df.loc[b] = df.loc[b].copy(), df.loc[a].copy()
                    df = df.reset_index(drop=True)
                    st.session_state.update({"ct_data": df})

                def delete_cn(idx: int):
                    df: pd.DataFrame = st.session_state.get("ct_data")
                    # a, b = (idx - 1, idx) if direction == -1 else (idx, idx + 1)
                    # df.loc[a], df.loc[b] = df.loc[b].copy(), df.loc[a].copy()
                    df.drop(index=idx, inplace=True)
                    df = df.reset_index(drop=True)
                    st.session_state.update({"ct_data": df})

                def edit_cn(idx: int):
                    col_name = ct_data.loc[idx, "Name"]
                    col_type = ct_data.loc[idx, "Type"]
                    col_size = ct_data.loc[idx, "Size"]
                    col_default = ct_data.loc[idx, "Default"]
                    st.session_state.update({
                        "ct_nc_editing": True,
                        "ct_nc_editing_revert_idx": idx,
                        "ct_nc_text_input_name": col_name,
                        "ct_nc_text_input_type": col_type,
                        "ct_nc_slider_size": col_size,
                        "ct_default_text_input": col_default
                    })
                    delete_cn(idx)

                def update_selectbox_size():
                    size = st.session_state.get("ct_nc_select_box_size", "MAX")
                    if size == "MAX":
                        size = ct_size_options["str"][-1]
                    st.session_state.update({
                        "ct_nc_slider_size": int(size)
                    })

                ct_columns = input_table_cols.columns(1 + len(ct_column_names), border=0)
                # input_table_cols.write("---")
                st.dataframe(ct_data)
                list_cb_pk_keys = []
                cont_height = 75
                for i, col in enumerate(ct_column_names, start=1):
                    with ct_columns[i]:
                        # container_btn_bar = st.container(height=25)
                        with st.container(height=cont_height):
                            st.write(col)
                with ct_columns[0]:
                    with st.container(height=cont_height):
                        st.empty()
                for i, row in ct_data.iterrows():
                    ct_pk = row["PK"]
                    ct_name = row["Name"]
                    ct_type = row["Type"]
                    ct_size = row["Size"]
                    ct_def = row["Default"]

                    ct_pk = 0 if pd.isna(ct_pk) else bool(ct_pk)
                    with ct_columns[0]:
                        # container_btn_bar = st.container(height=25)
                        btn_bar = st.container(height=cont_height).columns(4, gap="small")
                        if i > 0:
                            btn_bar[0].button(
                                label="^",
                                key=f"ct_btn_col_up_{i}",
                                on_click=lambda i_=i: update_cn(i_, -1)
                            )
                        if i < ct_data.shape[0] - 1:
                            btn_bar[1].button(
                                label="v",
                                key=f"ct_btn_col_down_{i}",
                                on_click=lambda i_=i: update_cn(i_, 1)
                            )
                        btn_bar[2].button(
                            label="edit",
                            key=f"ct_btn_col_edit_{i}",
                            type="secondary",
                            on_click=lambda i_=i: edit_cn(i_)
                        )
                        btn_bar[3].button(
                            label="del",
                            key=f"ct_btn_col_delete_{i}",
                            type="primary",
                            on_click=lambda i_=i: delete_cn(i_)
                        )
                        # st.write("CONTROLS")
                    with ct_columns[1]:
                        k = f"ct_nc_checkbox_pk_{i}"
                        list_cb_pk_keys.append(k)
                        st.session_state.update({k: ct_pk})
                        with st.container(height=cont_height):
                            st.checkbox(
                                label="pk",
                                key=k,
                                label_visibility="hidden",
                                on_change=lambda key_=k, i_=i: update_cb_pk(key_, i_)
                            )
                    with ct_columns[2]:
                        with st.container(height=cont_height):
                            st.write(ct_name)
                    with ct_columns[3]:
                        with st.container(height=cont_height):
                            st.write(ct_type)
                    with ct_columns[4]:
                        with st.container(height=cont_height):
                            st.write(ct_size)
                    with ct_columns[5]:
                        ct_def = None if not ct_def else ct_def
                        with st.container(height=cont_height):
                            st.write(ct_def)
                    # input_table_cols.write(f"{i=}, {row=}")
                if ct_data.shape[0] == 0:
                    input_table_cols.write("0 columns")
                # input_table_cols.write("---")

                ct_nc_editing: bool = st.session_state.get("ct_nc_editing", False)

                if ct_nc_editing or input_table_cols.button(
                        label="Add Column",
                        key=f"ct_btn_add_new_column"
                ):
                    st.session_state.update({"ct_nc_editing": True})
                    ct_nc_text_input_name = ct_columns[2].text_input(
                        label="Name",
                        key="ct_nc_text_input_name"
                    )
                    if st.session_state.get("ct_nc_text_input_name"):
                        ct_nc_text_input_type = ct_columns[3].selectbox(
                            label="Type",
                            key="ct_nc_text_input_type",
                            options=ct_type_options
                        )
                        ct_type = st.session_state.get("ct_nc_text_input_type")
                        if ct_type:
                            validator = ct_size_options[ct_type]
                            size_key = ""
                            if validator != "na":
                                if ct_type == "str":
                                    size_key = "ct_nc_slider_size"
                                    if "ct_nc_select_box_size" not in st.session_state:
                                        st.session_state.update({
                                            "ct_nc_select_box_size": "MAX"
                                        })
                                        update_selectbox_size()
                                    ct_nc_slider_size = ct_columns[4].slider(
                                        label="Size",
                                        key=size_key,
                                        min_value=validator[0],
                                        max_value=validator[-1]
                                    )
                                    ct_nc_select_box_size = ct_columns[4].selectbox(
                                        label="Size",
                                        key="ct_nc_select_box_size",
                                        options=["25", "50", "255", "511", "1023", "MAX"],
                                        label_visibility="hidden",
                                        on_change=update_selectbox_size
                                    )
                                elif ct_type in ["float", "decimal"]:
                                    size_key = "ct_nc_select_box_size"
                                    ct_nc_select_box_size = ct_columns[4].selectbox(
                                        label="Size",
                                        key=size_key,
                                        options=validator
                                    )

                            ct_default_text_input = ct_columns[5].text_input(
                                label="Default Value",
                                key="ct_default_text_input"
                            )

                            ct_save_new_column_disabled = False
                            ct_nc_name = st.session_state.get("ct_nc_text_input_name")
                            ct_nc_type = st.session_state.get("ct_nc_text_input_type")
                            ct_nc_size = st.session_state.get(size_key)
                            ct_nc_default = st.session_state.get("ct_default_text_input")

                            if ct_nc_default:
                                if ct_nc_type in ("str", "float", "decimal"):
                                    # check size of default
                                    if len(ct_nc_default) > ct_nc_size:
                                        input_table_cols.warning(
                                            f"default value '{ct_nc_default}' cannot exceed the size '{ct_nc_size}'."
                                        )
                                if ct_nc_type in ("int", "float", "decimal", "bit"):
                                    # validate number types:
                                    if not isnumber(ct_nc_default):
                                        input_table_cols.warning(
                                            f"default value '{ct_nc_default}' must be a number for this field."
                                        )
                                if ct_nc_type in ("date", "datetime"):
                                    # validate date types
                                    date_val = is_date(ct_nc_default)
                                    if ct_nc_default.lower() == "getdate()":
                                        date_val = "GETDATE()"
                                    elif date_val is None:
                                        input_table_cols.warning(
                                            f"default value '{ct_nc_default}' must be a date for this field."
                                        )

                            if input_table_cols.button(
                                    label="save",
                                    key=f"ct_save_new_column",
                                    disabled=ct_save_new_column_disabled
                            ):
                                record = {
                                    "Name": st.session_state.get("ct_nc_text_input_name"),
                                    "Type": st.session_state.get("ct_nc_text_input_type"),
                                    "Size": st.session_state.get(size_key),
                                    "Default": st.session_state.get("ct_default_text_input")
                                }
                                col_names = list(map(str.lower, ct_data["Name"].tolist()))
                                if ct_nc_name.lower() in col_names:
                                    input_table_cols.warning(
                                        f"Cannot insert another column with the name '{ct_nc_name}', only one instance per table."
                                    )
                                else:
                                    ct_nc_editing_revert_idx = st.session_state.get("ct_nc_editing_revert_idx")
                                    if ct_nc_editing_revert_idx is not None:
                                        ct_data = pd.concat([
                                            ct_data[:ct_nc_editing_revert_idx],
                                            pd.DataFrame(data=[record], columns=ct_column_names),
                                            ct_data[ct_nc_editing_revert_idx:]
                                        ]).reset_index(drop=True)
                                    else:
                                        ct_data = pd.concat([
                                            ct_data,
                                            pd.DataFrame(data=[record], columns=ct_column_names)
                                        ]).reset_index(drop=True)
                                    st.session_state.update({
                                        "ct_data": ct_data,
                                        "ct_nc_editing": False,
                                        "ct_nc_editing_revert_idx": None
                                    })
                                    st.rerun()

                user_name = st.session_state.get("user_full_name", "FULL NAME")
                table_name = wrap(st.session_state.get("ct_text_table_name", "UNNAMED"), is_col=True,
                                  sanitize=True).removeprefix("[").removesuffix("]")
                db_name = wrap(st.session_state.get("ct_text_db_name", "UNNAMED"), is_col=True,
                               sanitize=True).removeprefix("[").removesuffix("]")
                need_db_and_table_names = (not len(f"{db_name}".strip())) or (not len(f"{table_name}".strip()))

                if need_db_and_table_names:
                    input_table_cols.warning("Please specify the Database and New Table Names above.")

                if input_table_cols.button(
                        label="Generate SQL",
                        key="ct_btn_generate_sql",
                        disabled=need_db_and_table_names
                ):
                    if ct_data.shape[0] > 0:
                        now = datetime.datetime.now()
                        create_table_sql = f"\n/****** Object:  Table [dbo].[{{TABLE_NAME}}]    Script Date: {now:%Y-%m-%d %H:%M:%S} ******/"
                        create_table_sql += "\n" + (f"""
USE [{db_name}]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


-- =============================================
-- Author:\t\t<{user_name}>
-- Create date:\t<{now:%Y-%m-%d %H:%M:%S}>
-- Description:\t<Create Table [{db_name}].[dbo].[{{TABLE_NAME}}]>
-- =============================================
                                """).strip()
                        create_table_sql += "\n" + (f"""
CREATE TABLE [dbo].[{{TABLE_NAME}}] (
                                """).strip()

                        sql = create_table_sql.format(TABLE_NAME=table_name)
                        sql_hist = create_table_sql.format(TABLE_NAME=f"hist_{table_name}")
                        sql_hist_trig = (f"""
USE [{db_name}]
GO

/****** Object:  Trigger [dbo].[tr_Update{table_name}History]    Script Date: {now:%Y-%m-%d %H:%M:%S} ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:\t\t<{user_name}>
-- Create date:\t<{now:%Y-%m-%d %H:%M:%S}>
-- Description:\t<Maintain History Table>
-- =============================================
CREATE TRIGGER [dbo].[tr_Update{table_name}History] 
ON [dbo].[{table_name}]
AFTER INSERT, DELETE, UPDATE
AS 
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;

    -- Prevent recursive calls
    IF TRIGGER_NESTLEVEL() > 1 BEGIN
        RETURN;
    END
                        """).strip()
                        sql_hist_trig += "\n\n\t" + (f"""
    INSERT INTO
        [{db_name}].[dbo].[hist_{table_name}]
    (
        [ModifiedID],
        [ModifiedBy],
        [ModifiedColumn],
        [Modification],
        [ValueBefore],
        [ValueAfter]
    )
    /*
    SELECT
        [C].[ID],
        NULL,
        (CASE
            WHEN ([D].[Name] IS NULL) AND ([C].[Name] IS NOT NULL) THEN 'Name'
            WHEN ([I].[Name] IS NULL) AND ([D].[Name] IS NOT NULL) THEN 'Name'
            WHEN [D].[Name] <> [C].[Name] THEN 'Name'
            ELSE NULL
        END) AS [ModifiedColumn],
        (CASE
            WHEN ([D].[Name] IS NULL) AND ([C].[Name] IS NOT NULL) THEN 'INSERT'
            WHEN ([I].[Name] IS NULL) AND ([D].[Name] IS NOT NULL) THEN 'DELETE'
            WHEN [D].[Name] <> [C].[Name] THEN 'UPDATE'
            ELSE NULL
        END) AS [Modification],
        [D].[Name] AS [ValueBefore],
        [D].[Name] AS [ValueAfter]
    FROM
        [{db_name}].[dbo].[{table_name}] [C]
    INNER JOIN
        INSERTED [I]
    ON
        [C].[ID] = [I].[ID]
    LEFT JOIN
        DELETED [D]
    ON
        [C].[ID] = [D].[ID]
    WHERE 
        (CASE
            WHEN ([D].[Name] IS NULL) AND ([C].[Name] IS NOT NULL) THEN 1
            WHEN ([I].[Name] IS NULL) AND ([D].[Name] IS NOT NULL) THEN 1
            WHEN [D].[Name] <> [C].[Name] THEN 1
            ELSE 0
        END) > 0
    ;
    */
                                    """).strip()

                        union_template: str = """
    SELECT
        [C].[ID],
        NULL,
        (CASE
            WHEN ([D].[{col}] IS NULL) AND ([C].[{col}] IS NOT NULL) THEN '{col}'
            WHEN ([I].[{col}] IS NULL) AND ([D].[{col}] IS NOT NULL) THEN '{col}'
            WHEN [D].[{col}] <> [C].[{col}] THEN '{col}'
            ELSE NULL
        END) AS [ModifiedColumn],
        (CASE
            WHEN ([D].[{col}] IS NULL) AND ([C].[{col}] IS NOT NULL) THEN 'INSERT'
            WHEN ([I].[{col}] IS NULL) AND ([D].[{col}] IS NOT NULL) THEN 'DELETE'
            WHEN [D].[{col}] <> [C].[{col}] THEN 'UPDATE'
            ELSE NULL
        END) AS [Modification],
        [D].[{col}] AS [ValueBefore],
        [I].[{col}] AS [ValueAfter]
    FROM
        [{db_name}].[dbo].[{table_name}] [C]
    INNER JOIN
        INSERTED [I]
    ON
        [C].[ID] = [I].[ID]
    LEFT JOIN
        DELETED [D]
    ON
        [C].[ID] = [D].[ID]
    WHERE 
        (CASE
            WHEN ([D].[{col}] IS NULL) AND ([C].[{col}] IS NOT NULL) THEN 1
            WHEN ([I].[{col}] IS NULL) AND ([D].[{col}] IS NOT NULL) THEN 1
            WHEN [D].[{col}] <> [I].[{col}] THEN 1
            ELSE 0
        END) > 0                        
                        """
                        sql_hist_trig_lines = []

                        pk_col = None
                        default_values = []
                        bp_cols_copy = boilerplate_cols.copy()
                        has_clr_type: bool = False
                        for i, row in ct_data.iterrows():
                            ct_nc_pk = row["PK"]
                            ct_nc_name = row["Name"]
                            ct_nc_type = row["Type"]
                            ct_nc_size = row["Size"]
                            ct_nc_def = row["Default"]

                            try:
                                bp_cols_copy.remove(ct_nc_name)
                            except ValueError:
                                pass

                            ct_nc_pk = False if (pd.isna(ct_nc_pk) or (not ct_nc_pk)) else ct_nc_pk

                            if ct_nc_size == ct_size_options["str"][-1]:
                                ct_nc_size = "max"

                            # if not ct_cn_def:
                            #     ct_cn_def = "NULL"

                            if not has_clr_type:
                                # text, ntext, image, varchar(max), nvarchar(max), non - FILESTREAM, varbinary(max), xml or large CLR type columns.
                                has_clr_type = (ct_nc_type == "str") and (ct_nc_size == "max")

                            l_sql = ""

                            if ct_nc_def:
                                default_values.append((ct_nc_name, ct_nc_def))

                            st.write(f"{ct_nc_type=}")

                            match ct_nc_type:
                                case "str":
                                    if not ct_nc_pk:
                                        l_sql = f"\n\t[{ct_nc_name}] [nvarchar]({ct_nc_size}) NULL"
                                    else:
                                        # l_sql = f"\n\t[{ct_cn_name}] [nvarchar]({ct_nc_size}) IDENTITY(0, 1) NOT NULL"
                                        st.error(f"Cannot use {ct_nc_type} values as PKs. Feature coming soon")
                                case "date" | "datetime" | "bit" | "float":
                                    if not ct_nc_pk:
                                        l_sql = f"\n\t[{ct_nc_name}] [{ct_nc_type}] NULL"
                                    else:
                                        st.error(f"Cannot use {ct_nc_type} values as PKs.")
                                case "decimal":
                                    if not ct_nc_pk:
                                        a, b = eval(ct_nc_size)
                                        l_sql = f"\n\t[{ct_nc_name}] [{ct_nc_type}]({a}, {b}) NULL"
                                    else:
                                        st.error(f"Cannot use {ct_nc_type} values as PKs.")
                                case "int":
                                    if not ct_nc_pk:
                                        l_sql = f"\n\t[{ct_nc_name}] [int] NULL"
                                    else:
                                        l_sql = f"\n\t[{ct_nc_name}] [int] IDENTITY(0, 1) NOT NULL"
                                        pk_col = ct_nc_name
                                case _:
                                    st.error("UNSURE")

                            sql += f"\n\t{l_sql.strip()},"

                            sql_hist_trig_lines.append(
                                union_template.format(
                                    db_name=db_name,
                                    table_name=table_name,
                                    col=ct_nc_name
                                )
                            )

                        #                     sql += """
                        # [ID] [int] IDENTITY(0,1) NOT NULL,
                        # [DateCreated] [datetime] NULL,
                        # [LastModified] [datetime] NULL,
                        # [Active] [bit] NULL,
                        # [DateActive] [datetime] NULL,
                        # [DateInActive] [datetime] NULL,
                        #
                        # [NHLAPI_ID] [nvarchar](10) NULL,
                        #
                        # [Name] [nvarchar](255) NULL,
                        # [Description] [nvarchar](max) NULL,
                        # [Comments] [nvarchar](max) NULL,

                        sql = sql.removesuffix(",")

                        sql_hist_trig += "\n\tUNION ALL\n".join(sql_hist_trig_lines) + "\n\nEND"

                        # custom columns list for history table
                        sql_hist += "\n\t" + ("""
    [ID] [int] IDENTITY(0, 1) NOT NULL,
    [DateCreated] [datetime] NULL,
    [ModifiedID] [int] NULL,
    [ModifiedBy] [nvarchar](50) NULL,
    [ModifiedColumn] [nvarchar](512) NULL,
    [Modification] [nvarchar] (50)NULL,
    [ValueBefore] [nvarchar](max) NULL, 
    [ValueAfter] [nvarchar](max) NULL
                                    """).strip()

                        # consider CLR type columns
                        clr_type = " ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]" if has_clr_type else ""
                        if pk_col:
                            sql += "\n\n\t" + (f"""
CONSTRAINT [PK_{table_name}] PRIMARY KEY CLUSTERED (
        [{pk_col}] ASC
    )
    WITH (
        PAD_INDEX = OFF,
        STATISTICS_NORECOMPUTE = OFF,
        IGNORE_DUP_KEY = OFF,
        ALLOW_ROW_LOCKS = ON,
        ALLOW_PAGE_LOCKS = ON
        --, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
    ) ON [PRIMARY]
){clr_type}
GO
                                    """).strip()
                        sql_hist += "\n\n\t" + (f"""
CONSTRAINT [PK_hist_{table_name}] PRIMARY KEY CLUSTERED (
        [ID] ASC
    )
    WITH (
        PAD_INDEX = OFF,
        STATISTICS_NORECOMPUTE = OFF,
        IGNORE_DUP_KEY = OFF,
        ALLOW_ROW_LOCKS = ON,
        ALLOW_PAGE_LOCKS = ON
        --, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
    ) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
                                """).strip()

                        # add columns with default values
                        for col, val in default_values:
                            val = val if str(val).strip().endswith("()") else f"({val})"
                            sql += "\n\n" + (f"""
IF (EXISTS (SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE (([TABLE_SCHEMA] = 'dbo') 
    AND (TABLE_NAME = '{table_name}'))))
BEGIN
                                """).strip()
                            sql += f"\n\tALTER TABLE [dbo].[{table_name}] ADD CONSTRAINT [DF_{table_name}_{col}] DEFAULT ({val}) FOR [{col}];"
                            sql += "\nEND\nGO"

                        # add history column defaults
                        sql_hist += "\n\n" + (f"""
IF (EXISTS (SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE (([TABLE_SCHEMA] = 'dbo') 
    AND (TABLE_NAME = 'hist_{table_name}'))))
BEGIN
                                """).strip()
                        sql_hist += f"\n\tALTER TABLE [dbo].[hist_{table_name}] ADD CONSTRAINT [DF_hist_{table_name}_DateCreated] DEFAULT (GETDATE()) FOR [DateCreated];"
                        sql_hist += "\nEND\nGO"

                        # code for table create
                        input_table_cols.subheader("Step 1  - CREATE TABLE")
                        input_table_cols.code(sql, language="sql", line_numbers=True)

                        if bp_cols_copy:
                            st.warning(
                                f"Cannot infer Boilerplate Trigger because traditional boilerplate cols: [{', '.join(bp_cols_copy)}] could not be found. Please use the 'Boilerplate button to ensure the correct naming conventions are used.'")
                        else:

                            # code for back-up table creation
                            input_table_cols.subheader("Step 2  - CREATE Back-up TABLE")
                            input_table_cols.code(sql_hist, language="sql", line_numbers=True)

                            sql_trig = f"""
USE [{db_name}]
GO

/****** Object:  Trigger [dbo].[tr_Update{table_name}BoilerPlate]    Script Date: {now:%Y-%m-%d %H:%M:%S} ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:\t\t<{user_name}>
-- Create date:\t<{now:%Y-%m-%d %H:%M:%S}>
-- Description:\t<Maintain Boilerplate Columns>
-- =============================================
CREATE TRIGGER [dbo].[tr_Update{table_name}BoilerPlate] 
ON [dbo].[{table_name}]
AFTER INSERT, DELETE, UPDATE
AS 
BEGIN
-- SET NOCOUNT ON added to prevent extra result sets from
-- interfering with SELECT statements.
SET NOCOUNT ON;

-- Prevent recursive calls
IF TRIGGER_NESTLEVEL() > 1 BEGIN
    RETURN;
END

UPDATE
    [{db_name}].[dbo].[{table_name}]
SET
    [LastModified] = GETDATE()
    , [DateCreated] = ISNULL([C].[DateCreated], GETDATE())
    , [DateActive] = (CASE 
        WHEN ([I].[Active] = 1) AND (([D].[Active] IS NULL) OR ([D].[Active] = 0)) THEN
            GETDATE()
        ELSE
            [C].[DateActive]
        END
    )
    , [DateInactive] = (CASE 
        WHEN ([I].[Active] = 0) AND (([D].[Active] IS NULL) OR ([D].[Active] = 1)) THEN
            GETDATE()
        ELSE
            [C].[DateInActive] 
        END
    )
FROM
    [{db_name}].[dbo].[{table_name}] [C]
INNER JOIN
    INSERTED [I]
ON
    [C].[ID] = [I].[ID]
LEFT JOIN
    DELETED [D]
ON
    [C].[ID] = [D].[ID]
;
END
                                    """.strip()

                            # code for boilerplate trigger creation
                            input_table_cols.subheader("Step 3  - CREATE Boilerplate TRIGGER")
                            input_table_cols.code(sql_trig, language="sql", line_numbers=True)

                            # code for history trigger creation
                            input_table_cols.subheader("Step 4  - CREATE History TRIGGER")
                            input_table_cols.code(sql_hist_trig, language="sql", line_numbers=True)
                    else:
                        st.warning(
                            "Please enter some column information first."
                        )

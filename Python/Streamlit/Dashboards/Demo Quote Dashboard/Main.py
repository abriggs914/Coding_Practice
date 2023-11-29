import pandas as pd
import streamlit as st
from pyodbc_connection import connect


sql_ = """SELECT * FROM [v_SFC_BWSUnionSTGOrders];"""


@st.cache_data
def load_data():
    return connect(sql_)


def to_datetime(df_in: pd.DataFrame):
    for col in df_in.columns:
        print(f"{col=}")
        if "_date" in col.lower():
            try:
                df_in[col] = df_in[col].dt.date
            except AttributeError:
                # print(f"FAILURE {col=}")
                pass
    return df_in


if __name__ == '__main__':

    df = load_data()
    # df = pd.to_datetime(df.stack()).unstack()
    df = to_datetime(df)
    # df["Orders_WO"] = df["Orders_WO"].astype(dtype=int, errors="ignore")
    df = df.astype({"Orders_WO": int}, errors="ignore")

    print(f"{df['Orders_DateQuote'].dropna().unique()}")

    min_date_quote, max_date_quote = df["Orders_DateQuote"].dropna().min(), df["Orders_DateQuote"].dropna().max()
    min_date_order, max_date_order = df["Orders_DateOrder"].dropna().min(), df["Orders_DateOrder"].dropna().max()
    min_date_cancel, max_date_cancel = df["Orders_DateDeclined"].dropna().min(), df["Orders_DateDeclined"].dropna().max()
    min_date_delivery, max_date_delivery = df["Orders_DateDelivery"].dropna().min(), df["Orders_DateDelivery"].dropna().max()
    min_date_in_service, max_date_in_service = df["Orders_DateInService"].dropna().min(), df["Orders_DateInService"].dropna().max()
    min_date_registered, max_date_registered = df["Orders_DateRegistered"].dropna().min(), df["Orders_DateRegistered"].dropna().max()

    list_quote_numbers = df["Orders_Quote"].dropna().unique()
    list_wo_numbers = df["Orders_WO"].dropna().unique()
    list_serial_numbers = df["Orders_SerialNumber"].dropna().unique()
    list_po_numbers = df["Orders_PurchaseOrder"].dropna().unique()

    list_search_options = list(list_quote_numbers) + list(list_wo_numbers) + list(list_serial_numbers) + list(list_po_numbers)

    if "choice_searchbox" not in st.session_state:
        st.session_state["choice_searchbox"] = None

    searchbox = st.selectbox(
        label="",
        options=list_search_options,
        placeholder="Search Quote / WO / SN",
        key="choice_searchbox"
    )

    print()

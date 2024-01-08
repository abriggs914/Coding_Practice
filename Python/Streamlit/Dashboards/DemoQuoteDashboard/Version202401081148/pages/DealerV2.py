import datetime
import operator
from functools import reduce

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.metric_cards import style_metric_cards

DATA_PAGES_KEYS = {
    "df_orders": None,
    "df_options": None,
    "df_labour": None,
    "df_defects": None,
    "df_dealers": None,
    "minimum_date": None,
    "maximum_date": None,
    "sql_sp_performance": None

    ,
    "choice_n_years_input": 1,
    "choice_date_input": (None, None),
    "choice_select_dealer": None
}

if __name__ == '__main__':
    # st.markdown("## Check back in the future for more cool features!")

    today = datetime.datetime.now()

    selectable_cols_orders = {
        "OriginTable": "Company",
        "Orders_USSale": "US Sale",
        "Dealers_COMPANYNAME": "Dealer",
        "Orders_Quote": "Quote #",
        "Orders_DateQuote": "Quote Date",
        "Orders_DateOrder": "Order Date",
        "Orders_WO": "WO",
        "Orders_SalesOrder": "Sales Order",
        "Orders_ModelNo": "Model Name",
        "Products_Class": "Class",
        "Orders_Price": "Order Base Price $",
        "Cancelled": "Cancelled",
        "Orders_SerialNumber": "Serial #",
        "Orders_DateAvailable": "Available Date",
        "Orders_DateDelivery": "Delivery Date",
        "Orders_DateRequestedDelivery": "Requested Delivery Date",
        "Orders_DateFinish": "Date Finish",
        "Orders_PurchaseOrder": "PO #",
        "Orders_DatePO": "PO Date",
        "Discount1": "Discount 1",
        "Discount2": "Discount 2",
        "Discount3": "Discount 3",
        "SumDiscounts": "Total Discounts",
        "Orders_DateShipped": "Shipped Date",
        "Dealers_CITY": "Dealer City",
        "Dealers_PROVINCE": "Dealer Province"
    }
    date_cols_orders = {k: v for k, v in selectable_cols_orders.items() if "_Date" in k}

    for k, v in DATA_PAGES_KEYS.items():
        if k not in st.session_state:
            st.session_state[k] = v

    df_orders = st.session_state.get("df_orders", None)
    df_calendar = st.session_state.get("df_calendar", None)

    # Start drawing to the screen
    if df_orders is None:
        st.write(f"## Please re-run the Main page first.")
        switch_page("main")
    else:

        print(f"ORDERS\n{df_orders['Orders_DateQuote']}")

        df_orders["Cancelled"] = (
                (~(df_orders["Orders_DateDeclined"].isnull()))
                | (df_orders["Orders_DeclineRejected"] != 4)
        )
        # df_orders["Discount1"] = (
        #     f"{df_orders['Orders_Discount1']*100:.3f} %" if
        #     (df_orders["Orders_Discount1_Type"] == "Percent")
        #     else f"$ {df_orders['Orders_Discount1']:20,.2f}"
        # )
        df_orders["Discount1"] = df_orders["Orders_Discount1"]
        df_orders["Discount2"] = df_orders["Orders_Discount2"]
        df_orders["Discount3"] = df_orders["Orders_Discount3"]

        # # df_orders.loc[df_orders["Orders_Discount1_Type"] == "Percent", "Discount1"] = f"{df_orders['Orders_Discount1'] * 100:.3f} %"
        #
        #
        # # for row_data in df_orders.iterrows():
        # #     i, *row_list = row_data
        # #     row = row_list[0]
        # #     # print(f"{type(row)=}, {row=}, {type(row[0])=}, {row[0]=}")
        # #     d1 = row["Discount1"]
        # #     print(f"{i=}, PRE: {d1=}", end="")
        # #     d1 = f"{d1*100:.3f} %"
        # #     print(f" POST: {d1=}")
        #
        #
        # # df_orders["Discount1"] = np.where(
        # #     df_orders["Orders_Discount1_Type"] == "Percent",
        # #     f"{df_orders['Discount1']:.3f} %",
        # #     f"$ {df_orders['Discount1']:20,.2f}"
        # # )
        # df_orders["Discount1"] = np.where(
        #     df_orders["Orders_Discount1_Type"] == "Percent",
        #     df_orders['Discount1'].apply(lambda x: f"{x*100:.3f} %"),
        #     df_orders['Discount1'].apply(lambda x: f"$ {x:20,.2f}")
        # )
        # df_orders["Discount2"] = np.where(
        #     df_orders["Orders_Discount2_Type"] == "Percent",
        #     df_orders['Discount2'].apply(lambda x: f"{x*100:.3f} %"),
        #     df_orders['Discount2'].apply(lambda x: f"$ {x:20,.2f}")
        # )
        # df_orders["Discount3"] = np.where(
        #     df_orders["Orders_Discount3_Type"] == "Percent",
        #     df_orders['Discount3'].apply(lambda x: f"{x*100:.3f} %"),
        #     df_orders['Discount3'].apply(lambda x: f"$ {x:20,.2f}")
        # )

        # df_orders["Discount1"] = np.where(
        #     df_orders["Orders_Discount1_Type"] == "Percent",
        #     df_orders['Orders_Discount1'],
        #     df_orders['Orders_Discount1']
        # )

        # df_orders["Discount1"] = df_orders["Orders_Discount1_Type"].apply(lambda x: f"{df_orders['Orders_Discount1'] * 100:.3f} %" if x == "Percent" else f"$ {df_orders['Orders_Discount1']:20,.2f}")

        # df_orders["Orders_Discount1"] = df_orders["Orders_Discount1"].astype(float)
        # print(f"{df_orders['Orders_Discount1']=}")
        # df_orders["Discount1"] = np.where(
        #     (df_orders["Orders_Discount1_Type"] == "Percent"),
        #     f"{df_orders['Orders_Discount1'] * 100:.3f} %",
        #     f"$ {df_orders['Orders_Discount1']:20,.2f}"
        # )
        df_orders = df_orders[selectable_cols_orders.keys()]
        # df_orders = df_orders.rename(columns=selectable_cols_orders)

        column_config_orders = {
            k: st.column_config.DateColumn(
                k,
                format="%Y-%m-%d",
                disabled=True
            )
            for k in date_cols_orders
        }
        column_config_orders.update({
            k: st.column_config.NumberColumn(
                k,
                format="$ %d"
            )
            for k in selectable_cols_orders if "Discount" in k
        })
        # column_config_orders = {
        #     k: lambda x: f"{x:%Y-%m-%d}"
        #     for k in date_cols_orders
        # }

        # totals
        df_orders_today = df_orders[df_orders["Orders_DateQuote"] >= (today + datetime.timedelta(days=-1)).date()]
        print(f"SHAPE=={df_orders_today.shape}\n{df_orders_today[['Orders_DateQuote', 'Orders_Quote']]}")
        n_orders_today = df_orders_today.shape[0]

        df_explorer = df_orders.rename(columns=selectable_cols_orders)

        df_explorer_orders = dataframe_explorer(df_explorer.fillna(""), case=False)
        df_explorer_orders_today = df_explorer_orders[df_explorer_orders[selectable_cols_orders["Orders_DateQuote"]].dt.date >= (today + datetime.timedelta(days=-1)).date()]
        n_explorer_orders_today = df_explorer_orders_today.shape[0]

        add_vertical_space(2)
        st.dataframe(
            df_explorer_orders,
            use_container_width=True,
            column_config=column_config_orders
        )

        n_records, n_records_cols = df_explorer_orders.shape
        st.write(f"{n_records} Record{'' if n_records == 1 else 's'}.")

        mc_col0, mc_col1, mc_col2 = st.columns(3)
        mc_col0.metric(label="# Quotes + New", value=n_records, delta=n_explorer_orders_today)
        style_metric_cards(background_color="#343434")

        # qpd = df_explorer_orders.groupby(
        #     selectable_cols_orders["Orders_Quote"]
        # )[selectable_cols_orders[["Orders_Quote"]]].transform("count")
        qpd = df_explorer_orders.groupby(selectable_cols_orders["Orders_DateQuote"]).size().reset_index(name="Count")

        print(f"{qpd=}")

        # quotes_per_day = st.bar_chart(
        #     qpd,
        #     x=[selectable_cols_orders[k] for k in ["Orders_DateQuote", "Orders_DateOrder"]]
        #     ,y="Count"
        # )

        quotes_per_day = st.bar_chart(
            qpd,
            x=selectable_cols_orders["Orders_DateQuote"]
            ,y=[
                "Count"
            ]
        )

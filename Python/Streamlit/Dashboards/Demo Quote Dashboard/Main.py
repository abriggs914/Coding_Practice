import os.path
from functools import reduce
import operator

import pandas as pd
import streamlit as st
from pyodbc_connection import connect


sql_ = """SELECT * FROM [v_SFC_BWSUnionSTGOrders];"""

sql_options = """SELECT * FROM [v_SFC_OrdersDataOptions]"""


@st.cache_data
def load_data_orders():
    """Loading Data"""
    return connect(sql_)


@st.cache_data
def load_data_options():
    """Loading Data"""
    return connect(sql_options)


def get_options_data(company: int, quote: str):
    """Loading Options Data"""
    # return connect(f"{sql_options} WHERE [CompanyID] = {company} AND [Quote] = '{quote}'")
    return df_options[(df_options["CompanyID"] == company) & (df_options["Quote"] == quote)]


def to_datetime(df_in: pd.DataFrame):
    for col in df_in.columns:
        # print(f"{col=}")
        if "_date" in col.lower():
            try:
                df_in[col] = df_in[col].dt.date
            except AttributeError:
                # print(f"FAILURE {col=}")
                pass
    return df_in


@st.cache_data
def collect_searchbox_data():
    return list(list_quote_numbers) + list(list_wo_numbers) + list(list_serial_numbers) + list(list_po_numbers)


def what_is_searchbox_input_type() -> str | None:
    inp = st.session_state["choice_searchbox"]
    print(f"{inp=}, {type(inp)=}")
    # print(f"{list_quote_numbers}")
    # print(f"{list_wo_numbers}")
    in_qs = [q for q in list_quote_numbers if q == inp]
    in_wos = [wo for wo in list_wo_numbers if wo == inp]
    in_sns = [sn for sn in list_serial_numbers if sn == inp]
    in_pos = [po for po in list_po_numbers if po == inp]
    # print(f"\t{in_qs=}\n\t{in_wos=}\n\t{in_sns=}\n\t{in_pos=}")

    options = ["Quote", "WO", "SN", "PO"]

    sizes = [len(lst) for lst in [in_qs, in_wos, in_sns, in_pos]]
    if sum(sizes) == 0:
        # nothing found
        # print(f"NOTHING")
        return None
    elif sum(sizes) == 1:
        # exactly one occurrence of this input found
        return options[sizes.index(1)]
    else:
        # more than 1 option found
        # print(f"MORE THAN 1")
        return None

    # if inp in list_quote_numbers.values:
    # print(f"IN QUOTES {in_qs}")
    # return options[idx]


def update_data_table(input_type):

    input_search = st.session_state["choice_searchbox"]
    print(f"{input_type=}, {input_search=}")
    if input_type == "PO":
        message = f"PO == '{input_search}'"
        df_sub1 = df_orders.loc[df_orders["Orders_PO"] == input_search]
    elif input_type == "SN":
        message = f"SN == '{input_search}'"
        df_sub1 = df_orders.loc[df_orders["Orders_SerialNumber"] == input_search]
    elif input_type == "WO":
        message = f"WO == '{input_search}'"
        df_sub1 = df_orders.loc[df_orders["Orders_WO"] == input_search]
    else:
        message = f"Quote == '{input_search}'"
        df_sub1 = df_orders.loc[df_orders["Orders_Quote"] == input_search]

    print(f"{message=}")
    print(f"{df_sub1=}")

    quote_number = df_sub1.iloc[0]["Orders_Quote"]
    company = df_sub1.iloc[0]["OriginTable"]
    promo_drawing = df_sub1.iloc[0]["Products_PromoDrawing"]
    order_price = float(df_sub1.iloc[0]["Orders_Price"])

    st.markdown(f"## {company} {input_type}")

    company = 1 if company == "STG" else 0
    promo_drawing = os.path.abspath(promo_drawing)
    promo_drawing = promo_drawing.replace('/', '\\')
    promo_drawing = f"file:///{promo_drawing}"

    df_sub2 = get_options_data(company, quote_number)
    df_sub_options = df_sub2[(df_sub2["OriginTable"] == "Order Options") | (df_sub2["OriginTable"] == "Order OptionsV2")]
    df_sub_npos = df_sub2[(df_sub2["OriginTable"] == "Custom Work") | (df_sub2["OriginTable"] == "Custom WorkV2")]

    n_options, n_option_cols = df_sub_options.shape
    n_npos, n_option_cols = df_sub_npos.shape

    ttl_option_price = df_sub_options["OptionPrice"].apply(lambda x: float(x)).sum()
    ttl_option_cost = df_sub_options["OptionCost"].apply(lambda x: float(x)).sum()
    ttl_npo_price = df_sub_npos["OptionPrice"].apply(lambda x: float(x)).sum()
    ttl_npo_cost = df_sub_npos["OptionCost"].apply(lambda x: float(x)).sum()

    disc_1, disc_type_1 = df_sub1.iloc[0][["Orders_Discount1", "Orders_Discount1_Type"]]
    disc_2, disc_type_2 = df_sub1.iloc[0][["Orders_Discount2", "Orders_Discount2_Type"]]
    disc_3, disc_type_3 = df_sub1.iloc[0][["Orders_Discount3", "Orders_Discount3_Type"]]
    list_discs = [[disc_1, disc_type_1], [disc_2, disc_type_2], [disc_3, disc_type_3]]

    print("\n\t" + "\n\t".join([f"{d_} -- {dt_}" for d_, dt_ in list_discs]))

    # apply discounts Fixed-First
    ttl_fixed = sum([d_ for d_, dt_ in list_discs if dt_ == "Fixed"])
    ttl_percent = reduce(operator.mul, [1 - d_ for d_, dt_ in list_discs if dt_ == "Percent"])

    ttl_order_subtotal = order_price + ttl_option_price + ttl_npo_price
    calc_order_price = (ttl_order_subtotal + ttl_fixed) * ttl_percent
    ttl_discounts = ttl_order_subtotal - calc_order_price

    print(f"{ttl_fixed=}, {ttl_percent=}, {ttl_discounts=}, {calc_order_price=}")

    print(f"{company=}, {quote_number=}, '{promo_drawing}'")
    print(f"{df_sub2=}")
    print(f"{df_sub_options=}")
    print(f"{df_sub_npos=}")

    col_renames_orders = {
        "Orders_USSale": "US Sale",
        "Orders_Quote": "Quote",
        "Orders_WO": "WO",
        "Orders_PurchaseOrder": "PO",
        "Orders_SerialNumber": "SN",
        "Orders_ModelNo": "Model",
        "Orders_Price": "Order Base Price",
        "Products_Price": "Product Base Price",
        "Dealers_COMPANYNAME": "Dealer",
        "WipMaster_StockCode": "Syspro StockCode",
        "SalesStaff_SalesPerson": "Sales Person"
    }

    col_renames_options = {
        "OptionDescription": "Description",
        "OptionWeight": "Weight (lbs)",
        "OptionDrawPartNum": "Draw/Part Number",
        "OptionPrice": "Price",
        "OptionCost": "Cost",
        "OptionNo": "Option #",
        "OptionSections": "Section",
        "OptionSortSe": "Sort"
    }

    df_sub1 = df_sub1[col_renames_orders.keys()]
    df_sub_options = df_sub_options[col_renames_options.keys()]
    df_sub_npos = df_sub_npos[col_renames_options.keys()]
    df_sub_npos = df_sub_npos[~df_sub_npos["OptionDescription"].isin([None, "None"])]

    # print(f"{df_sub_options}")

    df_sub_options = df_sub_options.sort_values(by="OptionSortSe")
    df_sub_npos = df_sub_npos.sort_values(by="OptionSortSe")
    del df_sub_options["OptionSortSe"]
    del df_sub_npos["OptionSortSe"]

    df_sub1["Calculated Sub-Total"] = f"{ttl_order_subtotal:.2f}"
    df_sub1["Calculated Price"] = f"{calc_order_price:.2f}"
    df_sub1["Total Discounts"] = f"{ttl_discounts:.2f}"
    df_sub1["# Options"] = n_options
    df_sub1["# NPOs"] = n_npos
    df_sub1["Ttl Option Price"] = ttl_option_price
    df_sub1["Ttl Option Cost"] = ttl_option_cost
    df_sub1["Ttl NPO Price"] = ttl_npo_price
    df_sub1["Ttl NPO Cost"] = ttl_npo_cost

    df_sub1 = df_sub1.rename(columns=col_renames_orders)
    df_sub_options = df_sub_options.rename(columns=col_renames_options)
    df_sub_npos = df_sub_npos.rename(columns=col_renames_options)

    # df_table = st.dataframe(df_sub1)
    st.dataframe(df_sub1.transpose(), use_container_width=True)

    st.link_button("Promo Drawing", promo_drawing)

    expander_options = st.expander("Options")
    expander_options.dataframe(df_sub_options, hide_index=True, use_container_width=True)

    expander_npos = st.expander("NPOs")
    expander_npos.dataframe(df_sub_npos, hide_index=True, use_container_width=True)

    st.metric("Options Price", ttl_option_price, -1 * ttl_option_cost)
    st.metric("NPO Price", ttl_npo_price, -1 * ttl_npo_cost)


if __name__ == '__main__':

    # with st.spinner('Loading Data'):
    df_orders = load_data_orders()
    df_options = load_data_options()

    # df_orders = pd.to_datetime(df_orders.stack()).unstack()
    df_orders = to_datetime(df_orders)

    # df_orders["Orders_WO"] = df_orders["Orders_WO"].astype(dtype=int, errors="ignore")
    # df_orders = df_orders.astype({"Orders_WO": int}, errors="ignore")
    # df_orders["Orders_WO"] = df_orders["Orders_WO"].astype(int, errors="ignore")

    df_orders.fillna(0)
    df_options['OptionPrice'] = df_options['OptionPrice'].apply(lambda x: f"{x:.2f}")
    df_options['OptionCost'] = df_options['OptionCost'].apply(lambda x: f"{x:.2f}")

    df_orders['Orders_Price'] = df_orders['Orders_Price'].apply(lambda x: f"{x:.2f}")
    df_orders['Products_Price'] = df_orders['Products_Price'].apply(lambda x: f"{x:.2f}")

    # print(f"A {df_orders['Orders_WO']}")
    df_orders['Orders_WO'] = df_orders['Orders_WO'].apply(lambda x: f"{x:.0f}")
    # print(f"B {df_orders['Orders_WO']}")
    df_orders = df_orders.fillna({"Orders_WO": ""})
    # print(f"C {df_orders['Orders_WO']}")
    # df_orders["Orders_WO"] = df_orders["Orders_WO"].map({"nan": ""})
    # print(f"D {df_orders['Orders_WO']}")

    # print(f"{df_orders['Orders_DateQuote'].dropna().unique()}")
    # print(f"WOS == {df_orders['Orders_WO'].dropna().unique()}")

    min_date_quote, max_date_quote = df_orders["Orders_DateQuote"].dropna().min(), df_orders["Orders_DateQuote"].dropna().max()
    min_date_order, max_date_order = df_orders["Orders_DateOrder"].dropna().min(), df_orders["Orders_DateOrder"].dropna().max()
    min_date_cancel, max_date_cancel = df_orders["Orders_DateDeclined"].dropna().min(), df_orders["Orders_DateDeclined"].dropna().max()
    min_date_delivery, max_date_delivery = df_orders["Orders_DateDelivery"].dropna().min(), df_orders["Orders_DateDelivery"].dropna().max()
    min_date_in_service, max_date_in_service = df_orders["Orders_DateInService"].dropna().min(), df_orders["Orders_DateInService"].dropna().max()
    min_date_registered, max_date_registered = df_orders["Orders_DateRegistered"].dropna().min(), df_orders["Orders_DateRegistered"].dropna().max()

    list_quote_numbers = df_orders["Orders_Quote"].dropna().unique()
    list_wo_numbers = df_orders["Orders_WO"].dropna().unique()
    list_serial_numbers = df_orders["Orders_SerialNumber"].dropna().unique()
    list_po_numbers = df_orders["Orders_PurchaseOrder"].dropna().unique()

    list_search_options = collect_searchbox_data()

    if "choice_searchbox" not in st.session_state:
        st.session_state["choice_searchbox"] = None

    searchbox = st.selectbox(
        label="HIDE ME",
        options=list_search_options,
        placeholder="Search Quote / WO / SN",
        key="choice_searchbox",
        label_visibility="hidden"
    )

    if st.session_state["choice_searchbox"]:
        searchbox_input_type = what_is_searchbox_input_type()
        if searchbox_input_type is not None:
            msg = st.toast(f"LOADED {searchbox_input_type}")
            update_data_table(searchbox_input_type)
        else:
            st.warning(f"Unknown entry '{searchbox_input_type}'")
    else:
        print(f"NOTHING")

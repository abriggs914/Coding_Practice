import datetime
import json
import math
import os.path
import subprocess
from functools import reduce
import operator

import numpy as np
import pandas as pd
import pandas._libs
import streamlit as st
from pdf2image import convert_from_path
from streamlit_timeline import timeline

from json_utility import jsonify
from pyodbc_connection import connect


SETTINGS_FILE = "./settings.json"
VERSION_LOCKED = False


resources_raw = {
    "settings_icon": (
        r"\\nas1.bwsdomain.local\Public\IT\Program Resources\Sales Dashboard\settings_icon.png", "Settings Icon")
}

resources = {k: None for k in resources_raw}

sql_ = """SELECT * FROM [v_SFC_BWSUnionSTGOrders];"""

sql_calendar = """SELECT * FROM [Calendar];"""

sql_options = """SELECT * FROM [v_SFC_OrdersDataOptions]"""

sql_products = """SELECT * FROM [v_SFC_BWSUnionSTGProducts]"""

sql_labour = f"""SELECT * FROM [v_SFC_BWSUnionSTGLabour];"""

sql_dealers = f"""SELECT * FROM [v_SFC_BWSUnionSTGDealers];"""

sql_sp_performance = """EXEC sp_SFC_IndividualSalesData
	@companyID={COMPANYID}
	,@dealerID={DEALERID}
	,@productID={PRODUCTID}
	,@salesPersonID={SALESPERSONID}
	,@allCompanies={ALLCOMPANIES};
"""

sql_product_performance = """SELECT * FROM [arcProducts_PriceChanges];"""

sql_production_defects_counts = """SELECT * FROM [Defects] AS [P] LEFT JOIN [Defects_Causes] AS [C] ON [P].[CauseID] = [C].[CauseID#];"""
sql_finish_defects_counts = """SELECT * FROM [Defects_BPF] AS [F] LEFT JOIN [Defects_Causes] AS [C] ON [F].[CauseID] = [C].[CauseID#];"""
sql_print_defects_counts = """SELECT * FROM [Defects_Print] AS [P] LEFT JOIN [Defects_Print_Problems] AS [PP] ON [P].[ProblemID] = [PP].[DefPrintProbsID#];"""
sql_snags_defects_counts = """SELECT * FROM [Defects_Snags] AS [S] LEFT JOIN [Defects_Causes] AS [C] ON [S].[CauseID] = [C].[CauseID#];;"""

CACHE_TIME = 4 * 3600


@st.cache_data(ttl=CACHE_TIME, show_spinner="Fetching Orders Data...")
def load_data_orders():
    """Loading Data"""
    return connect(sql_)


@st.cache_data(ttl=CACHE_TIME, show_spinner="Fetching Options Data...")
def load_data_options():
    """Loading Options Data"""
    return connect(sql_options)


@st.cache_data(ttl=CACHE_TIME, show_spinner="Fetching Products Data...")
def load_data_products():
    """Loading Products Data"""
    return connect(sql_products)


@st.cache_data(ttl=CACHE_TIME, show_spinner="Fetching Labour Data...")
def load_data_labour():
    """Loading Products Data"""
    return connect(sql_labour)


@st.cache_data(ttl=CACHE_TIME, show_spinner="Fetching Dealers Data...")
def load_data_dealers():
    """Loading Dealers Data"""
    return connect(sql_dealers)


@st.cache_data(ttl=CACHE_TIME, show_spinner="Fetching Calendar Data...")
def load_data_calendar():
    """Loading Calendar Data"""
    return connect(sql_calendar)


@st.cache_data(ttl=CACHE_TIME, show_spinner="Fetching Defects Data...")
def load_data_defects():
    """Loading Defects Data"""
    return \
        connect(sql_production_defects_counts), \
            connect(sql_finish_defects_counts), \
            connect(sql_print_defects_counts), \
            connect(sql_snags_defects_counts)


@st.cache_data(ttl=CACHE_TIME, show_spinner="Fetching Product Data...")
def load_data_product_performance():
    """Loading Data"""
    return \
        connect(sql_product_performance), \
            connect(
                sql_product_performance,
                database="Stargatedb",
                uid="SGeu1",
                pwd="Pupplies-Hagard->Rio0"
            )


def get_options_data(company: int, quote: str):
    """Fetch options data for a company's quote number"""
    # return connect(f"{sql_options} WHERE [CompanyID] = {company} AND [Quote] = '{quote}'")
    return df_options[(df_options["CompanyID"] == company) & (df_options["Quote"] == quote)]


def get_labour_data(company: int, wo: str):
    """Fetch labour data for a company's WO"""
    # return connect(f"{sql_options} WHERE [CompanyID] = {company} AND [Quote] = '{quote}'")
    return df_labour[(df_labour["CompanyID"] == company) & (df_labour["Job"] == wo)]


def to_datetime(df_in: pd.DataFrame, is_datetime: bool = True):
    for col in df_in.columns:
        # print(f"{col=}")
        if "_date" in col.lower():
            try:
                df_in[col] = df_in[col].dt.date
                if is_datetime:
                    y, m, d = df_in[col].year, df_in[col].month, df_in[col].day
                    df_in[col] = datetime.datetime(y, m, d)
                # df_in[col] = df_in[col].astype('datetime64[ns]')
            except AttributeError:
                # print(f"FAILURE {col=}")
                pass
    return df_in


# def load_resources():
#     for k, data in resources_raw.items():
#         url, caption = data
#         image = None
#         try:
#             with open(url, "rb") as f:
#                 image = f.read()
#         except FileNotFoundError:
#             pass
#         resources.update({
#             k:
#         })


# @st.cache_data
def collect_searchbox_data():
    print(f"COLLECTING")

    keys = [
        "list_numbers_quote",
        "list_numbers_wo",
        "list_numbers_serial",
        "list_numbers_po"
    ]

    result = []
    use_bws = st.session_state["settings_allow_bws_searchbox"]
    use_stg = st.session_state["settings_allow_stg_searchbox"]
    use_q = st.session_state["settings_allow_quote_searchbox"]
    use_w = st.session_state["settings_allow_wo_searchbox"]
    use_s = st.session_state["settings_allow_serial_searchbox"]
    use_p = st.session_state["settings_allow_po_searchbox"]

    # print(f"{use_bws=}, {use_stg=}, {use_q=}, {use_w=}, {use_p=}, {use_s=}")

    if use_bws and use_stg:
        df_master = df_orders
    elif use_stg:
        df_master = df_orders_stg
    else:
        df_master = df_orders_bws
    # list_numbers_quote, list_numbers_wo, list_numbers_serial, list_numbers_po = [], [], [], []
    lsts = [[], [], [], []]
    for i, lst_k in enumerate(keys):
        m = ""
        if lst_k in st.session_state:
            m = "FOUND"
            lsts[i] = st.session_state[lst_k]
        else:
            m = "NOT FOUND"
        print(f"{m=}, {lst_k=}")
    if use_q:
        lsts[0] = list(df_master["Orders_Quote"].dropna().unique())
        result += lsts[0]
    if use_w:
        lsts[1] = list(df_master["Orders_WO"].dropna().unique())
        result += lsts[1]
    if use_s:
        lsts[2] = list(df_master["Orders_SerialNumber"].dropna().unique())
        result += lsts[2]
    if use_p:
        lsts[3] = list(df_master["Orders_PurchaseOrder"].dropna().unique())
        result += lsts[3]

    for i, lst_k in enumerate(keys):
        if lst_k not in st.session_state:
            st.session_state[lst_k] = lsts[i]
    # st.session_state["list_numbers_wo"] = list_numbers_wo
    # st.session_state["list_numbers_serial"] = list_numbers_serial
    # st.session_state["list_numbers_po"] = list_numbers_po

    print(f"LIST OF Q/Q/S/P #s == {len(result)=}")

    return result


def what_is_searchbox_input_type() -> str | None:

    list_numbers_quote = st.session_state["list_numbers_quote"]
    list_numbers_wo = st.session_state["list_numbers_wo"]
    list_numbers_serial = st.session_state["list_numbers_serial"]
    list_numbers_po = st.session_state["list_numbers_po"]

    inp = st.session_state["choice_searchbox"]
    print(f"{inp=}, {type(inp)=}")
    # print(f"{list_quote_numbers}")
    # print(f"{list_wo_numbers}")

    print(f"\t{len(list_numbers_quote)=}\n\t{len(list_numbers_wo)=}\n\t{len(list_numbers_serial)=}\n\t{len(list_numbers_po)=}")
    in_qs = [q for q in list_numbers_quote if q == inp]
    in_wos = [wo for wo in list_numbers_wo if wo == inp]
    in_sns = [sn for sn in list_numbers_serial if sn == inp]
    in_pos = [po for po in list_numbers_po if po == inp]
    print(f"\t{in_qs=}\n\t{in_wos=}\n\t{in_sns=}\n\t{in_pos=}")

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


def get_order_data(input_type, company=None):
    if company is not None:
        if isinstance(company, str):
            company = 1 if company == "STG" else 0

    input_search = st.session_state["choice_searchbox"]
    print(f"{input_type=}, {input_search=}")
    if input_type == "PO":
        message = f"PO == '{input_search}'"
        df_sub1 = df_orders.loc[df_orders["Orders_PurchaseOrder"] == input_search]
    elif input_type == "SN":
        message = f"SN == '{input_search}'"
        df_sub1 = df_orders.loc[df_orders["Orders_SerialNumber"] == input_search]
    elif input_type == "WO":
        message = f"WO == '{input_search}'"
        df_sub1 = df_orders.loc[df_orders["Orders_WO"] == input_search]
    else:
        message = f"Quote == '{input_search}'"
        df_sub1 = df_orders.loc[df_orders["Orders_Quote"] == input_search]

    if company is not None:
        message = f"{message} && Company == {company}"
        df_sub1 = df_sub1[df_sub1["Orders_CompanyID"] == company]

    return df_sub1, message


def click_option(df_idx: int):
    print(f"{df_idx=}")
    quote = df_orders.iloc[df_idx]["Orders_Quote"]
    st.session_state["choice_searchbox"] = quote


def click_promo_drawing(promo_dwng, container):
    print(f"CLICK PD {promo_dwng=}")
    if os.path.exists(promo_dwng):
        subprocess.Popen(fr'explorer /select,"{promo_dwng}')
    else:
        container.warning(f"Could not find file '{promo_dwng}'")


def click_quote_info_dir(qid, container):
    print(f"CLICK QID {qid=}")
    if os.path.exists(qid):
        subprocess.Popen(fr'explorer "{qid}')
    else:
        container.warning(f"Could not find folder '{qid}'")


def update_data_table(input_type):
    global btns_col1, btns_col2, btns_col3
    df_sub1, message = get_order_data(input_type)

    df_dates = to_datetime(df_sub1[ordered_dates_list.keys()])
    print(f"A {df_dates=}")
    # df_dates["IsCancelled"] = 1 if (not df_dates["Orders_DateDeclined"].any() and df_dates["Orders_DeclineRejected"] != 4) else 0
    # df_dates["IsCancelled"] = np.where(
    #     ~((df_dates["Orders_DateDeclined"].empty or isinstance(df_dates["Orders_DateDeclined"], pd._libs.NaTType)) and df_dates["Orders_DeclineRejected"] == 4), 1, 0)
    # df_dates["IsCancelled"] = np.where(
    #     ((~df_dates["Orders_DateDeclined"].empty
    #       or isinstance(df_dates["Orders_DateDeclined"], pd._libs.NaTType))
    #      or df_dates["Orders_DeclineRejected"] != 4
    #      ), 1, 0)
    # df_dates["IsCancelled"] = np.where(
    #     ((~isinstance(df_dates["Orders_DateDeclined"], pd._libs.NaT))
    #      or df_dates["Orders_DeclineRejected"] != 4
    #     ), 1, 0)
    # df_dates["IsCancelled"] = np.where(
    #     ((~df_dates["Orders_DateDeclined"].isnull()
    #       or ~df_dates["Orders_DateDeclined"].isna())
    #      or df_dates["Orders_DeclineRejected"] != 4
    #     ), 1, 0)
    # df_dates["IsCancelled"] = (
    #     ((~df_dates["Orders_DateDeclined"].isnull())
    #         & (~df_dates["Orders_DateDeclined"].isna()))
    #     | int(df_dates["Orders_DeclineRejected"]) != 4
    # )
    df_dates["IsCancelled"] = (
        # (~isinstance(df_dates["Orders_DateDeclined"], pd.NaT))
        (~(df_dates["Orders_DateDeclined"].isnull()))
        | (df_dates["Orders_DeclineRejected"] != 4)
    )

    # print(f"HERE")
    # print(f"{df_dates['Orders_DateDeclined']=}")
    # print(f"{df_dates['IsCancelled']=}")
    # print(f"{(df_dates['Orders_DateDeclined'] is pd.NaT)=}")
    # print(f"{(df_dates['Orders_DateDeclined'].isnull())=}")
    # print(f"{(df_dates['Orders_DateDeclined'].isna())=}")
    # print(f"{(df_dates['Orders_DeclineRejected'] != 4)=}")
    # print(f"{df_dates['Orders_DeclineRejected']=}")

    df_dates["IsOrder"] = np.where(~df_dates["Orders_DateOrder"].isnull(), 1, 0)
    del df_dates["dtProdSched_DateProd1"]
    del df_dates["dtProdSched_DateProd2"]
    del df_dates["Orders_DeclineRejected"]
    df_dates = df_dates.rename(columns=ordered_dates_list)
    unit_is_cancelled = df_dates.iloc[0]["IsCancelled"] == 1
    unit_is_ordered = df_dates.iloc[0]["IsOrder"] == 1
    del df_dates["IsCancelled"]
    del df_dates["IsOrder"]
    chartable_df_dates = df_dates.transpose()

    print(f"B {df_dates=}")

    print(f"{unit_is_cancelled=}")
    print(f"{unit_is_ordered=}")
    print(f"{message=}")
    print(f"{df_sub1=}")

    print(f"{df_sub1.shape=}")

    if df_sub1.shape[0] > 1:
        st.markdown("## Please choose an option:")
        for i, row in df_sub1.iterrows():
            o_comp = row["Orders_CompanyID"]
            o_comp = "STG" if o_comp == 1 else "BWS"
            o_quote = row["Orders_Quote"]
            o_model = row["Orders_ModelNo"]
            st.button(
                label=f"{o_comp} Quote: {o_quote}, Model: {o_model}",
                type="primary",
                on_click=lambda idx_=i: click_option(idx_)
            )
        return

    b_col1, b_col2 = st.columns(2, gap="large")
    b_col1.button(
        label="Previous Quote",
        type="primary",
        use_container_width=True,
        on_click=click_previous_quote
    )
    b_col2.button(
        label="Next Quote",
        type="primary",
        use_container_width=True,
        on_click=click_next_quote
    )

    unit_is_us = df_sub1.iloc[0]["Orders_USSale"]
    quote_number = df_sub1.iloc[0]["Orders_Quote"]
    wo_number = df_sub1.iloc[0]["Orders_WO"]
    serial_number = df_sub1.iloc[0]["Orders_SerialNumber"]
    po_number = df_sub1.iloc[0]["Orders_PurchaseOrder"]
    company = df_sub1.iloc[0]["OriginTable"]
    promo_drawing_product = df_sub1.iloc[0]["Products_PromoDrawing"]
    promo_drawing_order = df_sub1.iloc[0]["Orders_PromDrawing"]
    order_price = float(df_sub1.iloc[0]["Orders_Price"])
    product_price = float(df_sub1.iloc[0]['Products_Price'])
    date_quote = df_sub1.iloc[0]["Orders_DateQuote"]
    date_order = df_sub1.iloc[0]["Orders_DateOrder"]
    unit_is_ordered = not isinstance(date_order, pd._libs.NaTType)
    name_dealer = df_sub1.iloc[0]["Dealers_COMPANYNAME"]
    name_product = df_sub1.iloc[0]["Orders_ModelNo"]
    name_sales_person = df_sub1.iloc[0]["SalesStaff_SalesPerson"]

    wo_number = None if np.isnan(float(wo_number)) else wo_number

    id_company = df_sub1.iloc[0]["Orders_CompanyID"]
    id_dealer = df_sub1.iloc[0]["Orders_DealerID"]
    id_product = df_sub1.iloc[0]["Orders_ProductID"]
    id_sales_person = df_sub1.iloc[0]["Orders_SalePersonID"]

    st.session_state["choice_unit_cancelled"] = unit_is_cancelled
    st.session_state["choice_unit_ordered"] = unit_is_ordered
    st.session_state["choice_unit_is_us"] = unit_is_us

    t_company = "Stargate" if company == "STG" else "BWS"
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    t_col1.markdown(f"## {t_company} {input_type}")
    checkbox_unit_is_us = t_col2.checkbox(
        label="US Sale",
        key="choice_unit_is_us",
        disabled=True
    )
    checkbox_unit_is_ordered = t_col3.checkbox(
        label="Ordered",
        key="choice_unit_ordered",
        disabled=True
    )
    checkbox_unit_is_cancelled = t_col4.checkbox(
        label="Cancelled " + ("Order" if unit_is_ordered else "Quote") + ":",
        key="choice_unit_cancelled",
        disabled=True
    )

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric(label="Quote", value=quote_number)
    m_col2.metric(label="WO", value=wo_number)
    m_col3.metric(label="Serial", value=serial_number)
    m_col4.metric(label="PO", value=po_number)

    print(f"HERE '{promo_drawing_order=}'")
    s_company = company
    company = 1 if company == "STG" else 0
    if promo_drawing_order:
        promo_drawing_order = os.path.abspath(promo_drawing_order)
        promo_drawing_order = promo_drawing_order.replace('/', '\\')
        # promo_drawing = f"file:///{promo_drawing}"

    # correct links stored using Access syntax "link#link#"
    if promo_drawing_order:
        if promo_drawing_order.endswith("#"):
            if ((l := len(promo_drawing_order)) - 1) % 2 == 1:
                if promo_drawing_order[(l - 1) // 2] == "#":
                    promo_drawing_order = promo_drawing_order[:(l - 1) // 2]
    if promo_drawing_product:
        if promo_drawing_product.endswith("#"):
            if ((l := len(promo_drawing_product)) - 1) % 2 == 1:
                if promo_drawing_product[(l - 1) // 2] == "#":
                    # promo_drawing_product = promo_drawing_product[:int(math.ceil((l - 1)/2))]
                    promo_drawing_product = promo_drawing_product[:(l - 1) // 2]

    if company == 1:
        quote_info_dir = rf"\\\\nas1.bwsdomain.local\\Public\\Quote Information - Stargate\\{quote_number}\\"
    else:
        quote_info_dir = rf"\\\\nas1.bwsdomain.local\\Public\\Quote Information\\{quote_number}\\"

    df_sub2 = get_options_data(company, quote_number)
    df_sub_options = df_sub2[
        (df_sub2["OriginTable"] == "Order Options") | (df_sub2["OriginTable"] == "Order OptionsV2")]
    df_sub_npos = df_sub2[(df_sub2["OriginTable"] == "Custom Work") | (df_sub2["OriginTable"] == "Custom WorkV2")]

    df_sub_options = df_sub_options[
        ~df_sub_options["OptionDescription"].isin([None, "None", "NO OPTIONS FOR THIS WORK ORDER"])]
    df_sub_npos = df_sub_npos[~df_sub_npos["OptionDescription"].isin([None, "None"])]
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
    discs_percent = [1 - d_ for d_, dt_ in list_discs if dt_ == "Percent"]
    ttl_fixed = sum([d_ for d_, dt_ in list_discs if dt_ == "Fixed"])
    ttl_percent = reduce(operator.mul, discs_percent) if discs_percent else 1

    ttl_order_subtotal = order_price + ttl_option_price + ttl_npo_price
    calc_order_price = (ttl_order_subtotal + ttl_fixed) * ttl_percent
    ttl_discounts = ttl_order_subtotal - calc_order_price

    print(f"{ttl_fixed=}, {ttl_percent=}, {ttl_discounts=}, {calc_order_price=}")

    print(f"{company=}, {quote_number=}, '{promo_drawing_order}'")
    print(f"{df_sub2=}")
    print(f"{df_sub_options=}")
    print(f"{df_sub_npos=}")

    col_renames_orders = {
        "Orders_DateQuote": "Quote Date",
        "Orders_USSale": "US Sale",
        "Orders_Quote": "Quote",
        "Orders_WO": "WO",
        "Orders_PurchaseOrder": "PO",
        "Orders_SerialNumber": "SN",
        "Orders_ModelNo": "Model",
        "Products_Class": "Class",
        "WipMaster_StockCode": "Syspro StockCode",
        "Orders_Price": "Order Base Price",
        "Products_Price": "Product Base Price",
        "Dealers_COMPANYNAME": "Dealer",
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

    # print(f"{df_sub_options}")

    df_sub_options = df_sub_options.sort_values(by="OptionSortSe")
    df_sub_npos = df_sub_npos.sort_values(by="OptionSortSe")
    del df_sub_options["OptionSortSe"]
    del df_sub_npos["OptionSortSe"]

    df_sub1["Orders_Price"] = f"$ {order_price:20,.2f}"
    df_sub1["Products_Price"] = f"$ {product_price:20,.2f}"
    df_sub1["Calculated Sub-Total"] = f"$ {ttl_order_subtotal:20,.2f}"
    df_sub1["Calculated Price"] = f"$ {calc_order_price:20,.2f}"
    df_sub1["Total Discounts"] = f"$ {ttl_discounts:20,.2f}"
    df_sub1["Ttl Option Price"] = f"$ {ttl_option_price:20,.2f}"
    # df_sub1["Ttl Option Cost"] = f"$ {ttl_option_cost:20,.2f}"
    df_sub1["Ttl NPO Price"] = f"$ {ttl_npo_price:20,.2f}"
    # df_sub1["Ttl NPO Cost"] = f"$ {ttl_npo_cost:20,.2f}"
    df_sub1["# Options"] = n_options
    df_sub1["# NPOs"] = n_npos

    del df_sub1["Orders_USSale"]
    del df_sub1["Orders_Quote"]
    del df_sub1["Orders_WO"]
    del df_sub1["Orders_PurchaseOrder"]
    del df_sub1["Orders_SerialNumber"]

    df_sub1 = df_sub1.rename(columns=col_renames_orders)
    chartable_df_sub_options = df_sub_options.rename(columns=col_renames_options)
    chartable_df_sub_npos = df_sub_npos.rename(columns=col_renames_options)

    # df_table = st.dataframe(df_sub1)
    original_index = df_sub1.index
    chartable_model_data = df_sub1.reset_index()
    del chartable_model_data["index"]
    print(f"A {chartable_model_data=}")
    chartable_model_data = chartable_model_data.transpose()
    print(f"B {chartable_model_data=}")
    chartable_model_data = chartable_model_data.rename(columns={0: "Overview"})
    st.dataframe(
        chartable_model_data,
        use_container_width=True,
        height=550
    )

    btns_col1, btns_col2, btns_col3 = st.columns(3)

    if quote_info_dir:
        btns_col1.button(
            "Quote Info Folder",
            key="choice_quote_info_dir",
            type="primary",
            on_click=lambda qid=quote_info_dir: click_quote_info_dir(qid, btns_col1)
        )
    else:
        btns_col1.markdown(f"###### No quote information folder found for this order")

    if promo_drawing_order:
        # st.link_button("Promo Drawing", promo_drawing)
        btns_col2.button(
            "Order Promo Drawing",
            key="choice_promo_drawing_order",
            type="primary",
            on_click=lambda promo_dwng=promo_drawing_order, container=btns_col2: click_promo_drawing(promo_dwng,
                                                                                                     container)
        )
    else:
        btns_col2.markdown(f"###### No promo drawing on file for this order")

    if promo_drawing_product:
        # st.link_button("Promo Drawing", promo_drawing)
        btns_col3.button(
            "Product Promo Drawing",
            key="choice_promo_drawing_product",
            type="primary",
            on_click=lambda promo_dwng=promo_drawing_product, container=btns_col3: click_promo_drawing(promo_dwng,
                                                                                                       container)
        )
    else:
        btns_col3.markdown(f"###### No promo drawing on file for this product")

    expander_options = st.expander("Options")
    expander_options.dataframe(chartable_df_sub_options, hide_index=True, use_container_width=True)

    expander_npos = st.expander("NPOs")
    expander_npos.dataframe(chartable_df_sub_npos, hide_index=True, use_container_width=True)

    expander_move_history = st.expander("Movement History")
    expander_move_history.dataframe(
        chartable_df_dates,
        use_container_width=True,
        height=500
    )

    # for data in chartable_df_dates.iterrows():
    #     print(f"\t\t{data=}")
    # movements_data = df_dates[[""]]
    # movements_data = df_dates.to_dict()
    movement_keys = ["id", "content", "start"]
    fmt = "%Y-%m-%d"
    movements_data = [dict(zip(movement_keys, (i, dat[0], dat[1]))) for i, dat in
                      enumerate(chartable_df_dates.itertuples()) if not isinstance(dat[1], pandas._libs.NaTType)]
    movements_dict = {
        "title": {
            "text": {
                "headline": "Movements",
                "text": ""
            }
        },
        "events": []
    }
    for event in movements_data:
        movements_dict["events"].append({
            "start_date": {
                "day": event["start"].day,
                "month": event["start"].month,
                "year": event["start"].year
            },
            "text": {
                "headline": event["content"],
                "text": event["content"]
            }
        })

    print(f"{movements_data=}")
    # movements_data = movement_data
    with expander_move_history:
        movements_timeline = timeline(movements_dict, height=400)
    # movements_timeline = timeline(movements_dict, height=400)
    # expander_move_history.
    # movements_timeline = expander_move_history.timeline(movements_dict, height=400)
    # expander_move_history.write(movements_timeline)

    expander_options.metric("Options Price", f"$ {ttl_option_price:20,.2f}")  # , -1 * ttl_option_cost)
    expander_npos.metric("NPO Price", f"$ {ttl_npo_price:20,.2f}")  # , -1 * ttl_npo_cost)

    # -- Reports --

    expander_reports = st.expander("Reports")
    if company == 1:
        # STG
        path_quote_report = rf"\\NAS1.bwsdomain.local\\Public\\Quote Information - Stargate\\{quote_number}\\WIP\\"
        # path_quote_report = r"\NAS1.bwsdomain.local\Public\Quote Information - Stargate\" + str(quote_number) + r"\WIP\"
    else:
        # BWS
        path_quote_report = rf"\\NAS1.bwsdomain.local\Public\Quote Information\{quote_number}\\WIP\\"

    path_quote_report = os.path.normpath(path_quote_report)

    image_quote, image_wo = None, None
    last_file_quote, last_file_wo = None, None
    if os.path.exists(path_quote_report):
        print(f"A")
        files = os.listdir(path_quote_report)
        files.sort(key=lambda x: os.path.getmtime(rf"{path_quote_report}\{x}"), reverse=True)
        files_quote = [f for f in files if f.startswith("QUR_")]
        files_wo = [f for f in files if f.startswith("WOR_")]
        if files_quote:
            print(f"B")
            last_file_quote = files_quote[0]
            last_file_quote = os.path.normpath(rf"{path_quote_report}\{last_file_quote}")
            print(f"GETTING LASTFILE '{last_file_quote}'")
            image_quote = convert_from_path(
                last_file_quote,
                poppler_path=r"C:\Program Files (x86)\Poppler Release-23.11.0-0\poppler-23.11.0\Library\bin"
            )

            # print(f"{type(image_quote)=}, {image_quote=}")
        else:
            print(f"Not files_quote")

        if files_wo:
            print(f"B")
            last_file_wo = files_wo[0]
            last_file_wo = os.path.normpath(rf"{path_quote_report}\{last_file_wo}")
            print(f"GETTING LASTFILE '{last_file_wo}'")
            image_wo = convert_from_path(
                last_file_wo,
                poppler_path=r"C:\Program Files (x86)\Poppler Release-23.11.0-0\poppler-23.11.0\Library\bin"
            )

            # print(f"{type(image_quote)=}, {image_quote=}")
        else:
            print(f"Not files_wo")
    else:
        print(f"Not os.path.exists(path_quote_report)")

    print(f"{image_quote=}, {path_quote_report=}")
    print(f"{image_wo=}, {path_quote_report=}")

    if image_quote:
        expander_reports.markdown(f"## Quote Report")
        expander_reports.markdown(f"###### {last_file_quote}")
        for i, img in enumerate(image_quote):
            expander_reports.image(img, caption=f"Quote Report P{i + 1}", use_column_width=True)
    else:
        expander_reports.markdown(f"## Quote Report must be run in access before it can be displayed here.")

    if image_wo:
        expander_reports.markdown(f"## WO Report")
        expander_reports.markdown(f"###### {last_file_wo}")
        for i, img in enumerate(image_wo):
            expander_reports.image(img, caption=f"WO Report P{i + 1}", use_column_width=True)
    else:
        expander_reports.markdown(f"## WO Report must be run in access before it can be displayed here.")

    # -- Quote Capture Performances (QCP) --

    expander_qcp = st.expander("Quote Capture Performances")
    sql_qcp_specific = sql_sp_performance.format(
        COMPANYID=-id_company,
        DEALERID=-id_dealer,
        PRODUCTID=-id_product,
        SALESPERSONID=-id_sales_person,
        ALLCOMPANIES=0
    )
    df_qcp_specific = connect(sql_qcp_specific)

    sql_qcp_company = sql_sp_performance.format(
        COMPANYID=-id_company,
        DEALERID="NULL",
        PRODUCTID="NULL",
        SALESPERSONID="NULL",
        ALLCOMPANIES=0
    )
    df_qcp_company = connect(sql_qcp_company)
    sql_qcp_dealer = sql_sp_performance.format(
        COMPANYID="NULL",
        DEALERID=-id_dealer,
        PRODUCTID="NULL",
        SALESPERSONID="NULL",
        ALLCOMPANIES=0
    )
    df_qcp_dealer = connect(sql_qcp_dealer)
    sql_qcp_product = sql_sp_performance.format(
        COMPANYID="NULL",
        DEALERID="NULL",
        PRODUCTID=-id_product,
        SALESPERSONID="NULL",
        ALLCOMPANIES=0
    )
    df_qcp_product = connect(sql_qcp_product)
    sql_qcp_sales_person = sql_sp_performance.format(
        COMPANYID="NULL",
        DEALERID="NULL",
        PRODUCTID="NULL",
        SALESPERSONID=-id_sales_person,
        ALLCOMPANIES=0
    )
    df_qcp_sales_person = connect(sql_qcp_sales_person)

    selectable_cols = {
        "NumQuotesPrepared": "# Quotes Prepared",
        "NumInvalidQuotes": "# Invalid Quotes",
        "NumSoldDeliveredUnits": "# Sold & Delivered Quotes",
        "NumUnitsOnOrder": "# Quotes on Order",
        "NumQuotesOutToDealer": "# Quotes out to Dealer",
        "NumCancelledQuotes": "# Cancelled Quotes",
        "NumCancelledOrders": "# Cancelled Orders",

        "PctInvalidQuotes": "% Invalid Quotes",
        "PctSoldDeliveredUnits": "% Sold & Delivered Quotes",
        "PctUnitsOnOrder": "% Quotes on Order",
        "PctQuotesOutToDealer": "% Quotes out to Dealer",
        "PctCancelledQuotes": "% Cancelled Quotes",
        "PctCancelledOrders": "% Cancelled Orders"
    }

    # df_qcp_specific = df_qcp_specific[selectable_cols.keys()]
    # df_qcp_company = df_qcp_company[selectable_cols.keys()]
    # df_qcp_dealer = df_qcp_dealer[selectable_cols.keys()]
    # df_qcp_product = df_qcp_product[selectable_cols.keys()]
    # df_qcp_sales_person = df_qcp_sales_person[selectable_cols.keys()]

    # format all columns that start with prefix 'pct' indicating percentage
    for col in df_qcp_specific.columns:
        if col.startswith("Pct"):
            df_qcp_specific[col] = df_qcp_specific[col].apply(lambda x: f"{x:3.3f} %")
    for col in df_qcp_company.columns:
        if col.startswith("Pct"):
            df_qcp_company[col] = df_qcp_company[col].apply(lambda x: f"{x:3.3f} %")
    for col in df_qcp_dealer.columns:
        if col.startswith("Pct"):
            df_qcp_dealer[col] = df_qcp_dealer[col].apply(lambda x: f"{x:3.3f} %")
    for col in df_qcp_product.columns:
        if col.startswith("Pct"):
            df_qcp_product[col] = df_qcp_product[col].apply(lambda x: f"{x:3.3f} %")
    for col in df_qcp_sales_person.columns:
        if col.startswith("Pct"):
            df_qcp_sales_person[col] = df_qcp_sales_person[col].apply(lambda x: f"{x:3.3f} %")

    df_all = pd.concat(
        [
            df_qcp_specific[selectable_cols.keys()],
            df_qcp_company[selectable_cols.keys()],
            df_qcp_dealer[selectable_cols.keys()],
            df_qcp_product[selectable_cols.keys()],
            df_qcp_sales_person[selectable_cols.keys()]
        ],
        ignore_index=True
    ).rename(columns=selectable_cols).transpose().rename(
        columns=dict(zip(
            range(5),
            [
                "Specific",
                t_company,
                name_dealer,
                name_product,
                name_sales_person
            ]
        ))
    )

    # df_qcp_specific = df_qcp_specific.rename(columns=selectable_cols)
    # df_qcp_company = df_qcp_company.rename(columns=selectable_cols)
    # df_qcp_dealer = df_qcp_dealer.rename(columns=selectable_cols)
    # df_qcp_product = df_qcp_product.rename(columns=selectable_cols)
    # df_qcp_sales_person = df_qcp_sales_person.rename(columns=selectable_cols)

    # df_qcp_specific = df_qcp_specific.transpose()
    # df_qcp_company = df_qcp_company.transpose()
    # df_qcp_dealer = df_qcp_dealer.transpose()
    # df_qcp_product = df_qcp_product.transpose()
    # df_qcp_sales_person = df_qcp_sales_person.transpose()
    #
    # print(f"{df_qcp_sales_person.columns=}")

    # expander_qcp.markdown(f"### Specific to Company, Dealer, Product, and Sales Person")
    # expander_qcp.dataframe(df_qcp_specific, height=700)
    # qcp_col1, qcp_col2, qcp_col3, qcp_col4 = expander_qcp.columns(4)
    # qcp_col1.markdown(f"### Specific to Company")
    # qcp_col1.dataframe(df_qcp_company, height=700)
    # qcp_col2.markdown(f"### Specific to Dealer")
    # qcp_col2.dataframe(df_qcp_dealer, height=700)
    # qcp_col3.markdown(f"### Specific to Product")
    # qcp_col3.dataframe(df_qcp_product, height=700)
    # qcp_col4.markdown(f"### Specific to Sales Person")
    # qcp_col4.dataframe(df_qcp_sales_person, height=700)

    expander_qcp.dataframe(df_all, height=500)

    # -- Product History --

    expander_product_history = st.expander("Product History")
    df_root_product_performance = df_product_performance_stg if company == 1 else df_product_performance_bws
    df_product_performance = df_root_product_performance[df_root_product_performance["Model No"] == name_product]
    df_product_performance = df_product_performance[["ArchiveDate", "New Price", "Old Price"]]

    print(f"PRE PERFORMANCE")
    print(f"{df_product_performance.shape=} {df_product_performance=}")

    p_table = "ProductsV2" if company == 1 else "Products"
    prod_curr_price = df_products[(df_products["OGTable"] == p_table) & (df_products["Model No"] == name_product)]
    prod_curr_price = prod_curr_price.iloc[0]["Price"]
    prod_last_price = df_product_performance.iloc[df_product_performance.shape[0] - 1]["New Price"]
    print(f"{df_product_performance.index=}")
    print(f"{list(df_product_performance.columns)=}")
    df_product_performance.loc[len(df_product_performance.index)] = (
        now,
        prod_curr_price,
        prod_last_price
    )
    print(f"POST PERFORMANCE")
    print(f"{df_product_performance}")

    df_product_performance.set_index("ArchiveDate")
    df_product_performance["Change"] = df_product_performance['New Price'] - df_product_performance['Old Price']
    print(f"{df_product_performance=}")
    chartable_df_product_performance = df_product_performance.copy()
    chartable_df_product_performance["Change"] = chartable_df_product_performance["Change"].apply(
        lambda x: f"$ {x:20.2f}")
    chartable_df_product_performance["New Price"] = chartable_df_product_performance["New Price"].apply(
        lambda x: f"$ {x:20.2f}")
    chartable_df_product_performance["Old Price"] = chartable_df_product_performance["Old Price"].apply(
        lambda x: f"$ {x:20.2f}")
    expander_product_history.dataframe(
        chartable_df_product_performance,
        use_container_width=True,
        hide_index=True
    )
    expander_product_history.line_chart(
        df_product_performance,
        x="ArchiveDate",
        y=["New Price", "Old Price"]
    )

    # -- Defects --

    print(f"{wo_number=}")
    print(f"BEFORE {df_defects_finish=}")

    expander_defects_history = st.expander("Defects History")
    if wo_number is not None:
        df_sub_defects_production = df_defects_production[df_defects_production["WO#"] == wo_number]
        df_sub_defects_finish = df_defects_finish[df_defects_finish["WO#"] == wo_number]
        df_sub_defects_print = df_defects_print[df_defects_print["WO#"] == wo_number]
        df_sub_defects_snags = df_defects_snags[df_defects_snags["WO#"] == wo_number]

        print(f"AFTER {df_sub_defects_finish=}")

        expander_defects_history.markdown(f"## Print")
        expander_defects_history.dataframe(
            df_sub_defects_print
        )
        expander_defects_history.markdown(f"## Production")
        expander_defects_history.dataframe(
            df_sub_defects_production
        )
        expander_defects_history.markdown(f"## Finish Off")
        expander_defects_history.dataframe(
            df_sub_defects_finish
        )
        expander_defects_history.markdown(f"## Snags")
        expander_defects_history.dataframe(
            df_sub_defects_snags
        )
    else:
        expander_defects_history.markdown(f"## WO # Required")

    # -- Labour --

    expander_labour_history = st.expander("Labour History")
    selectable_cols_labour = {
        "Operation": "OP",
        "IMachine": "Machine",
        "IExpUnitRunTim": "Run Time Est. (H)",
        "RunTimeIssued": "Run Time Act (H)",
        # "IExpSetUpTime": "Set-Up. Est. (H)",
        # "IExpStartupTime": "Start-Up. Est. (H)",
        # "IExpShutdownTim": "Shut-down Est. (H)",
        # "IWaitTime": "Wait (H)",
        # "ICapacityReqd": "Capacity Reqd.",
        "IMaxWorkOpertrs": "Max Operators",
        "IMaxProdUnits": "Max Prod Units",
        "ITimeTaken": "Time (H)",
        # "IQuantity": "Qty",
        "IExpUnitRunTimEnt": "Est. Run Time (H)",
        "UnitValueReqd": "Value Reqd. ($)",
        # "SetUpIssued": "Set-Up Time (H)",
        # "ShutdownIssued": "Shut-down Time (H)",
        # "ValueIssued": "Value Issued (Total $)",
        # "PiecesCompleted": "Pieces Completed",
        "ValueBilled": "Value Billed",
        "OperCompleted": "OP Complete",
        "QtyCompleted": "Qty Completed",
        "QtyScrapped": "Qty Scrapped",
        "LastScrapReason": "Last Scrap Desc.",
        "PlannedQueueDate": "Planned Queue Date",
        "PlannedStartDate": "Planned Start Date",
        "PlannedEndDate": "Planned End Date",
        "ActualQueueDate": "Actual Queue Date",
        "ActualStartDate": "Actual Start Date",
        "ActualFinishDate": "Actual End Date",
        "WorkCentre": "WorkCentre",
        "WorkCentreDesc": "WorkCentre Description",
        "ElapsedTime": "Elapsed Time",
        "MovementTime": "Movement Time",
        "UnitNumOfPieces": "Num Pieces",
        "InspectionFlag": "Inspection Flag"
        # ,
        # "CapacityIssued": "Capacity Issued",
        # "ParentQtyPlanned": "Parent Qty Planned",
        # "ParentQtyPlanEnt": "Parent Qty Plan Ent"
    }
    if wo_number is not None:
        df_sub_labour = get_labour_data(company, wo_number).reset_index()
        df_sub_labour = df_sub_labour[selectable_cols_labour.keys()]

        total_run_time_est = df_sub_labour["IExpUnitRunTim"].sum()
        total_run_time_act = df_sub_labour["RunTimeIssued"].sum()

        col_lab1, col_lab2 = expander_labour_history.columns(2)

        col_lab1.metric(
            label="Total Run Time Est.",
            value=total_run_time_est
        )

        col_lab2.metric(
            label="Total Run Time Act",
            value=total_run_time_act
        )

        df_sub_labour = df_sub_labour.rename(columns=selectable_cols_labour)
        expander_labour_history.dataframe(
            df_sub_labour,
            hide_index=True,
            height=530,
            use_container_width=True
        )
    else:
        expander_labour_history.markdown(f"## WO # Required")

    if unit_is_cancelled:
        expander_defects_history.markdown(f"#### WO Cancelled")
        expander_labour_history.markdown(f"#### WO Cancelled")


def click_previous_quote():
    if not (sb_inp := st.session_state["choice_searchbox"]):
        st.warning("Please enter a BWS Quote, WO, PO, or Serial Number")
        return

    # TODO prevent going into BWS quotes from STG

    sb_inp_type = st.session_state["choice_searchbox_type"]
    df_sub1, message = get_order_data(sb_inp_type)
    idx = df_sub1.index

    if idx == 0:
        st.warning("This is the first quote.")
        return

    df_sub2 = df_orders.iloc[idx - 1].reset_index()
    prev_quote = df_sub2.iloc[0]["Orders_Quote"]
    print(f"{sb_inp=}, {sb_inp_type=}, {idx=}, {prev_quote=}")
    st.session_state["choice_searchbox"] = prev_quote


def click_next_quote():
    if not (sb_inp := st.session_state["choice_searchbox"]):
        st.warning("Please enter a BWS Quote, WO, PO, or Serial Number")
        return

    # TODO prevent going into STG quotes from BWS

    sb_inp_type = st.session_state["choice_searchbox_type"]
    df_sub1, message = get_order_data(sb_inp_type)
    idx = df_sub1.index

    print(f"{df_orders.index=}")
    print(f"{df_orders.index.stop=}")
    if idx == df_orders.index.stop:
        st.warning("This is the last quote.")
        return

    df_sub2 = df_orders.iloc[idx + 1].reset_index()
    next_quote = df_sub2.iloc[0]["Orders_Quote"]
    print(f"{sb_inp=}, {sb_inp_type=}, {idx=}, {next_quote=}")
    st.session_state["choice_searchbox"] = next_quote


def correct_wo_numbers(lst_dfs):
    """Ensure that all values in the specified 'WO' column are str representations of integers."""
    # result = []
    for df, col_name in lst_dfs:
        df[col_name] = df[col_name].apply(
            lambda x: (x if isinstance(x, str) else (f"{x:.0f}" if x is not None else None)))
    # return result


def click_settings_menu():
    # state = st.session_state["choice_settings_menu"]
    # if state
    if "choice_settings_menu" not in st.session_state:
        st.session_state["choice_settings_menu"] = False
    # st.session_state["choice_settings_menu"] = not st.session_state["choice_settings_menu"]
    st.session_state.update({
        "choice_settings_menu": not st.session_state["choice_settings_menu"]
    })


def change_settings_stargate():
    print(f"change_settings_stg")
    using_bws = st.session_state["settings_allow_bws_searchbox"]
    using_stg = st.session_state["settings_allow_stg_searchbox"]
    if not using_bws:
        #comp_col2.warning(f"")
        if not using_stg:
            # cant turn both off, since stg was last, flip bws
            st.session_state["settings_allow_bws_searchbox"] = True


def change_settings_bws():
    print(f"change_settings_bws")
    using_bws = st.session_state["settings_allow_bws_searchbox"]
    using_stg = st.session_state["settings_allow_stg_searchbox"]
    if not using_stg:
        #comp_col2.warning(f"")
        if not using_bws:
            # cant turn both off, since bws was last, flip stg
            st.session_state["settings_allow_stg_searchbox"] = True


# def change_settings_quote():

def click_settings_searchbox():
    # use_bws = st.session_state["settings_allow_bws_searchbox"]
    # use_stg = st.session_state["settings_allow_stg_searchbox"]
    use_q = st.session_state["settings_allow_quote_searchbox"]
    use_w = st.session_state["settings_allow_wo_searchbox"]
    use_s = st.session_state["settings_allow_serial_searchbox"]
    use_p = st.session_state["settings_allow_po_searchbox"]
    rng = st.session_state["settings_order_searchbox"]

    order = [
        "settings_allow_quote_searchbox",
        "settings_allow_wo_searchbox",
        "settings_allow_serial_searchbox",
        "settings_allow_po_searchbox"
    ]

    idx = rng.pop(0)
    upd = {
        "settings_order_searchbox": [*rng, idx]
    }

    if not any([use_q, use_w, use_s, use_p]):
        # print(f"A {rng=}")
        # Cant use nothing, flip the first flipped off, back on.
        # st.session_state[order[idx]] = True
        upd.update({order[idx]: True})
        # print(f"B {st.session_state['settings_order_searchbox']=}")
    st.session_state.update(upd)


def check_versioning() -> datetime.datetime:

    key = "date"

    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        data.update({key: eval(data[key])})
    except FileNotFoundError:
        data = {}

    if (not VERSION_LOCKED) or (data.get(key, None) is None):
        data.update({key: now})

        with open(SETTINGS_FILE, "w") as f:
            f.write(jsonify(data))

    print(f"check versioning")
    print(f"{data[key]=}")

    return data[key]


INITIAL_ST_SETTINGS = {
    "choice_searchbox": None,
    "choice_settings_menu": False,
    "settings_allow_bws_searchbox": True,
    "settings_allow_stg_searchbox": True,
    "settings_allow_quote_searchbox": True,
    "settings_allow_wo_searchbox": True,
    "settings_allow_serial_searchbox": True,
    "settings_allow_po_searchbox": True,
    "settings_order_searchbox": list(range(4)),
    # "list_numbers_quote": [],
    # "list_numbers_wo": [],
    # "list_numbers_serial": [],
    # "list_numbers_po": [],
    "sql_sp_performance": sql_sp_performance
}


# DATA_PAGES_KEYS = {
#     "df_orders": None,
#     "df_options": None,
#     "df_labour": None,
#     "df_dealers": None,
#     "df_defects": None,
#     "minimum_date": None,
#     "maximum_date": None,
#     "sql_sp_performance": sql_sp_performance
# }


if __name__ == '__main__':

    print(f"\n\n\n\tRERUN!!!\n\n")

    now = datetime.datetime.now()
    version_date = check_versioning()

    btns_col1, btns_col2, btns_col3 = None, None, None

    st.set_page_config(page_title="Sales Dashbord", layout="wide")
    st.title("Sales Dashboard")

    st.markdown(f"###### Version {version_date:%Y-%m-%d %H:%M}")

    # Ensure all session information has been initialized
    upd = {}
    upd_results = {}
    for k, v in INITIAL_ST_SETTINGS.items():
        if k not in st.session_state:
            upd.update({k: v})
            # st.session_state[k] = v

        upd_results[k] = f"SS[{k}] = {v}, Actual=ACT"
        # print(f"SS['{k}'] = {v}")

    st.session_state.update(upd)
    # print(f"HERE\n{st.session_state['sql_sp_performance']=}")
    # upd_results = {k: [upd_results[k].format(ACT=str(st.session_state[k])[:50])] for k, v in INITIAL_ST_SETTINGS.items()}
    # print(f"Update Results:          VVV")
    # print(f"{upd_results=}")
    # print(pd.DataFrame(upd_results))
    # print(f":Update Results          ^^^")

    settings_state = st.session_state["choice_settings_menu"]

    # st.sidebar.image(
    #     *resources_raw["settings_icon"],
    #     output_format="png"
    # )
    # st.sidebar.markdown(
    #     # f"<input type='image' id='id_img_btn_settings' src={resources_raw['settings_icon'][0]}>",
    #     f"###### [![this is the settings link](https://i.imgur.com/mQAQwvt.png)](https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=686079794781-0bt8ot3ie81iii7i17far5vj4s0p20t7.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fwebmasters.readonly&state=vryYlMrqKikWGlFVwqhnMpfqr1HMiq&prompt=consent&access_type=offline)",
    #     unsafe_allow_html=True
    # )
    # st.sidebar.toggle(
    #     label="Settings",
    #     key="choice_settings_menu",
    #     help="Open Settings Menu"
    # )
    st.sidebar.button(
        label="Settings" if not settings_state else "Main Menu",
        # key="choice_settings_menu",
        help="Open Settings Menu",
        type="secondary",
        on_click=click_settings_menu,
        disabled=True
    )

    if settings_state:
        st.markdown(f"### SETTINGS")

        st.divider()

        st.markdown(f"##### Main Searchfield Settings")
        comp_col1, comp_col2 = st.columns(2)

        comp_col1.checkbox(
            label="BWS Data",
            key="settings_allow_bws_searchbox",
            help="Allow BWS data to be searchable in the main search field.",
            on_change=change_settings_bws
        )
        comp_col2.checkbox(
            label="Stargate Data",
            key="settings_allow_stg_searchbox",
            help="Allow Stargate Data to be searchable in the main search field.",
            on_change=change_settings_stargate
        )

        st.divider()

        st.checkbox(
            label="Quote Numbers",
            key="settings_allow_quote_searchbox",
            help="Allow Quote Numbers to be searchable in the main search field.",
            # on_change=change_settings_quote
            on_change=click_settings_searchbox
        )
        st.checkbox(
            label="Work Orders",
            key="settings_allow_wo_searchbox",
            help="Allow Work Order Numbers to be searchable in the main search field.",
            # on_change=change_settings_wo
            on_change=click_settings_searchbox
        )
        st.checkbox(
            label="Serial Numbers",
            key="settings_allow_serial_searchbox",
            help="Allow Serial Numbers to be searchable in the main search field.",
            # on_change=change_settings_serial
            on_change=click_settings_searchbox
        )
        st.checkbox(
            label="Purchase Orders",
            key="settings_allow_po_searchbox",
            help="Allow Purchase Order Numbers to be searchable in the main search field.",
            # on_change=change_settings_po
            on_change=click_settings_searchbox
        )

    else:

        ordered_dates_list = {
            "Orders_DeclineRejected": "DecRej",
            "Orders_DateDeclined": "Date Declined",
            "Orders_DateQuote": "Quote Date",
            "Orders_DateOrder": "Order Date",
            "dtProdSched_DateBeam": "Beam Date",
            "dtProdSched_DateGN": "GNK Date",
            "dtProdSched_DateProd1": "Prod Date 1",
            "dtProdSched_DateProd2": "Prod Date 2",
            "Orders_DateFinish": "Finish Date",
            "Orders_DateAvailable": "Available Date",
            "Orders_DatePO": "Purchase Order",
            "Orders_DateShipped": "Shipped Date",
            "Orders_DateDelivery": "Delivery Date",
            "Orders_DateInService": "Date In Service",
            "Orders_DateRegistered": "Date Registered"
        }

        # with st.spinner('Loading Data'):
        st.empty()
        df_orders = load_data_orders()
        df_options = load_data_options()
        df_products = load_data_products()
        df_labour = load_data_labour()
        df_dealers = load_data_dealers()
        df_calendar = load_data_calendar()
        df_product_performance_bws, df_product_performance_stg = load_data_product_performance()
        df_defects_production, df_defects_finish, df_defects_print, df_defects_snags = load_data_defects()

        # df_orders = promo_dwng.to_datetime(df_orders.stack()).unstack().
        df_orders = to_datetime(df_orders, False)
        df_orders["Orders_SalesOrder"] = df_orders["Orders_SalesOrder"].astype(str)

        # df_orders["Orders_WO"] = df_orders["Orders_WO"].astype(dtype=int, errors="ignore")
        # df_orders = df_orders.astype({"Orders_WO": int}, errors="ignore")
        # df_orders["Orders_WO"] = df_orders["Orders_WO"].astype(int, errors="ignore")

        # df_orders,\
        #     df_options,\
        #     df_defects_production,\
        #     df_defects_print,\
        #     df_defects_finish,\
        #     df_defects_snags \
        #     = \
        correct_wo_numbers([
            (df_orders, "Orders_WO"),
            (df_options, "WO"),
            (df_defects_production, "WO#"),
            (df_defects_print, "WO#"),
            (df_defects_finish, "WO#"),
            (df_defects_snags, "WO#")
        ])

        # print(f"{df_options=}")

        df_orders.fillna(0)
        df_options['OptionPrice'] = df_options['OptionPrice'].apply(lambda x: f"{x:.2f}")
        df_options['OptionCost'] = df_options['OptionCost'].apply(lambda x: f"{x:.2f}")

        df_orders['Orders_Price'] = df_orders['Orders_Price'].apply(lambda x: f"{x:.2f}")
        df_orders['Products_Price'] = df_orders['Products_Price'].apply(lambda x: f"{x:.2f}")

        # print(f"A {df_orders['Orders_WO']}")
        # df_orders['Orders_WO'] = df_orders['Orders_WO'].apply(lambda x: f"{x:.0f}")
        df_orders = df_orders.fillna({"Orders_ProductID": -1})
        df_orders['Orders_ProductID'] = df_orders['Orders_ProductID'].apply(lambda x: int(f"{x:.0f}"))
        # print(f"B {df_orders['Orders_WO']}")
        df_orders = df_orders.fillna({
            "Orders_WO": "",
            "Orders_Discount1": 0,
            "Orders_Discount2": 0,
            "Orders_Discount3": 0
        })

        # calculate the price:
        df_orders["SumDiscounts"] = 0
        for row_data in df_orders.iterrows():
            i, row = row_data
            obp = float(row["Orders_Price"].removeprefix("$").strip())  # orders base price
            d1 = row["Orders_Discount1_Type"], row["Orders_Discount1"]
            d2 = row["Orders_Discount2_Type"], row["Orders_Discount2"]
            d3 = row["Orders_Discount3_Type"], row["Orders_Discount3"]
            sum_fixed = sum([dv for dt, dv in [d1, d2, d3] if dt != "Percent"])
            percents = [dv for dt, dv in [d1, d2, d3] if dt == "Percent"]
            r_percents = reduce(operator.mul, percents, 0)
            # print(f"{obp=}, {sum_fixed=}, {r_percents=}")
            # df_orders.loc[i]["SumDiscounts"] = sum_fixed + (obp * r_percents)
            df_orders.loc[i, "SumDiscounts"] = sum_fixed + (obp * r_percents)

        df_orders_bws = df_orders[df_orders["OriginTable"] == "BWS"]
        df_orders_stg = df_orders[df_orders["OriginTable"] == "STG"]

        st.session_state.update({
            "df_orders": df_orders,
            "df_options": df_options,
            "df_orders_bws": df_orders_bws,
            "df_orders_stg": df_orders_stg,
            "df_dealers": df_dealers,
            "df_calendar": df_calendar
        })

        # print(f"C {df_orders['Orders_WO']}")
        # df_orders["Orders_WO"] = df_orders["Orders_WO"].map({"nan": ""})
        # print(f"D {df_orders['Orders_WO']}")

        # print(f"{df_orders['Orders_DateQuote'].dropna().unique()}")
        # print(f"WOS == {df_orders['Orders_WO'].dropna().unique()}")

        min_date_quote, max_date_quote = df_orders["Orders_DateQuote"].dropna().min(), df_orders[
            "Orders_DateQuote"].dropna().max()
        min_date_order, max_date_order = df_orders["Orders_DateOrder"].dropna().min(), df_orders[
            "Orders_DateOrder"].dropna().max()
        min_date_cancel, max_date_cancel = df_orders["Orders_DateDeclined"].dropna().min(), df_orders[
            "Orders_DateDeclined"].dropna().max()
        min_date_delivery, max_date_delivery = df_orders["Orders_DateDelivery"].dropna().min(), df_orders[
            "Orders_DateDelivery"].dropna().max()
        min_date_in_service, max_date_in_service = df_orders["Orders_DateInService"].dropna().min(), df_orders[
            "Orders_DateInService"].dropna().max()
        min_date_registered, max_date_registered = df_orders["Orders_DateRegistered"].dropna().min(), df_orders[
            "Orders_DateRegistered"].dropna().max()

        minimum_date = min([min_date_quote, min_date_order, min_date_cancel, min_date_delivery, min_date_in_service, min_date_in_service])
        maximum_date = max([max_date_quote, max_date_order, max_date_cancel, max_date_delivery, max_date_in_service, max_date_in_service])
        st.session_state.update({
            "minimum_date": minimum_date,
            "maximum_date": maximum_date
        })

        # list_quote_numbers = df_orders["Orders_Quote"].dropna().unique()
        # list_wo_numbers = df_orders["Orders_WO"].dropna().unique()
        # list_serial_numbers = df_orders["Orders_SerialNumber"].dropna().unique()
        # list_po_numbers = df_orders["Orders_PurchaseOrder"].dropna().unique()

        # print(f"PRE COLLECTION")
        list_search_options = collect_searchbox_data()
        # print(f"POST COLLECTION")

        searchbox = st.selectbox(
            label="HIDE ME",
            options=list_search_options,
            placeholder="Search Quote / WO / SN",
            key="choice_searchbox",
            label_visibility="hidden"
        )

        if st.session_state["choice_searchbox"]:
            searchbox_input_type = what_is_searchbox_input_type()
            st.session_state["choice_searchbox_type"] = searchbox_input_type
            if searchbox_input_type is not None:
                msg = st.toast(f"LOADED {searchbox_input_type}")
                update_data_table(searchbox_input_type)
            else:
                st.warning(f"Unable to determine if '{searchbox_input_type}' is a Quote, WO, Serial, or PO Number.")
                st.warning(f"{st.session_state['choice_searchbox']=}")
        else:
            print(f"NOTHING")

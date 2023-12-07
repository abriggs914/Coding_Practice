import os.path
from functools import reduce
import operator

import numpy as np
import pandas as pd
import pandas._libs
import streamlit as st
from pdf2image import convert_from_path
from streamlit_timeline import timeline
from pyodbc_connection import connect

sql_ = """SELECT * FROM [v_SFC_BWSUnionSTGOrders];"""

sql_options = """SELECT * FROM [v_SFC_OrdersDataOptions]"""

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


def update_data_table(input_type):
    df_sub1, message = get_order_data(input_type)

    df_dates = to_datetime(df_sub1[ordered_dates_list.keys()])
    print(f"A {df_dates=}")
    # df_dates["IsCancelled"] = 1 if (not df_dates["Orders_DateDeclined"].any() and df_dates["Orders_DeclineRejected"] != 4) else 0
    df_dates["IsCancelled"] = np.where(
        (df_dates["Orders_DateDeclined"].empty and df_dates["Orders_DeclineRejected"] != 4), 1, 0)
    del df_dates["dtProdSched_DateProd1"]
    del df_dates["dtProdSched_DateProd2"]
    del df_dates["Orders_DeclineRejected"]
    df_dates = df_dates.rename(columns=ordered_dates_list)
    unit_is_cancelled = df_dates.iloc[0]["IsCancelled"] == 1
    del df_dates["IsCancelled"]
    chartable_df_dates = df_dates.transpose()

    print(f"B {df_dates=}")

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
    promo_drawing = df_sub1.iloc[0]["Products_PromoDrawing"]
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

    company = 1 if company == "STG" else 0
    if promo_drawing:
        promo_drawing = os.path.abspath(promo_drawing)
        promo_drawing = promo_drawing.replace('/', '\\')
        promo_drawing = f"file:///{promo_drawing}"

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

    print(f"{company=}, {quote_number=}, '{promo_drawing}'")
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
    chartable_model_data = df_sub1.transpose()
    st.dataframe(
        chartable_model_data,
        use_container_width=True,
        height=550
    )

    if promo_drawing:
        st.link_button("Promo Drawing", promo_drawing)

    expander_options = st.expander("Options")
    expander_options.dataframe(chartable_df_sub_options, hide_index=True, use_container_width=True)

    expander_npos = st.expander("NPOs")
    expander_npos.dataframe(chartable_df_sub_npos, hide_index=True, use_container_width=True)

    expander_move_history = st.expander("Movement History")
    expander_move_history.dataframe(chartable_df_dates, use_container_width=True, height=420)

    for data in chartable_df_dates.iterrows():
        print(f"\t\t{data=}")
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
            expander_reports.image(img, caption=f"Quote Report P{i+1}", use_column_width=True)
    else:
        expander_reports.markdown(f"## Quote Report must be run in access before it can be displayed here.")

    if image_wo:
        expander_reports.markdown(f"## WO Report")
        expander_reports.markdown(f"###### {last_file_wo}")
        for i, img in enumerate(image_wo):
            expander_reports.image(img, caption=f"WO Report P{i+1}", use_column_width=True)
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

    df_qcp_specific = df_qcp_specific.rename(columns=selectable_cols)
    df_qcp_company = df_qcp_company.rename(columns=selectable_cols)
    df_qcp_dealer = df_qcp_dealer.rename(columns=selectable_cols)
    df_qcp_product = df_qcp_product.rename(columns=selectable_cols)
    df_qcp_sales_person = df_qcp_sales_person.rename(columns=selectable_cols)

    df_qcp_specific = df_qcp_specific.transpose()
    df_qcp_company = df_qcp_company.transpose()
    df_qcp_dealer = df_qcp_dealer.transpose()
    df_qcp_product = df_qcp_product.transpose()
    df_qcp_sales_person = df_qcp_sales_person.transpose()

    print(f"{df_qcp_sales_person.columns=}")

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
        df[col_name] = df[col_name].apply(lambda x: (x if isinstance(x, str) else (f"{x:.0f}" if x is not None else None)))
    # return result


if __name__ == '__main__':

    st.set_page_config(page_title="Sales Dashboard", layout="wide")
    st.title("Sales Dashboard")
    st.markdown(f"###### Version 2023-12-05 13:51")

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
    df_product_performance_bws, df_product_performance_stg = load_data_product_performance()
    df_defects_production, df_defects_finish, df_defects_print, df_defects_snags = load_data_defects()

    # df_orders = promo_dwng.to_datetime(df_orders.stack()).unstack().
    df_orders = to_datetime(df_orders)

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

    print(f"{df_options=}")

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
    df_orders = df_orders.fillna({"Orders_WO": ""})
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
        st.session_state["choice_searchbox_type"] = searchbox_input_type
        if searchbox_input_type is not None:
            msg = st.toast(f"LOADED {searchbox_input_type}")
            update_data_table(searchbox_input_type)
        else:
            st.warning(f"Unknown entry '{searchbox_input_type}'")
    else:
        print(f"NOTHING")

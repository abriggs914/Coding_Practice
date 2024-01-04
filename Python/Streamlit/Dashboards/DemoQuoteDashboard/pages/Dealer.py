import datetime
import calendar

import pandas as pd
from dateutil import relativedelta

import dateutil
import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page

from pyodbc_connection import connect


# from nav_pages import nav_page


# from Dashboards.DemoQuoteDashboard.Main import df_dealers, df_orders, minimum_date, maximum_date
# from DemoQuoteDashboard.Main import df_dealers, df_orders, minimum_date, maximum_date
# from ..Main import df_dealers, df_orders, minimum_date, maximum_date
# from Main import df_dealers, df_orders, minimum_date, maximum_date
# from Dashboards.DemoQuoteDashboard.Main import
# import df_dealers, df_orders, minimum_date, maximum_date

# import Dashboards as DB
# from Dashboards.DemoQuoteDashboard import Main
# using Main import df_dealers, df_orders, minimum_date, maximum_date


# def nav_page(page_name, timeout_secs=3):
#     nav_script = """
#         <script type="text/javascript">
#             function attempt_nav_page(page_name, start_time, timeout_secs) {
#                 var links = window.parent.document.getElementsByTagName("a");
#                 for (var i = 0; i < links.length; i++) {
#                     if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
#                         links[i].click();
#                         return;
#                     }
#                 }
#                 var elasped = new Date() - start_time;
#                 if (elasped < timeout_secs * 1000) {
#                     setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
#                 } else {
#                     alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
#                 }
#             }
#             window.addEventListener("load", function() {
#                 attempt_nav_page("%s", new Date(), %d);
#             });
#         </script>
#     """ % (page_name, timeout_secs)
#     html(nav_script)


def time_between(date_1: datetime.datetime, date_2: datetime.datetime):
    date_format = "%Y-%m-%d"

    # Convert the date strings to datetime objects
    if isinstance(date_1, str):
        date1 = datetime.datetime.strptime(date_1, date_format)
    else:
        date1 = date_1
    if isinstance(date_2, str):
        date2 = datetime.datetime.strptime(date_2, date_format)
    else:
        date2 = date_2

    # Calculate the difference between the dates
    delta = date2 - date1
    days = delta.days

    # Calculate years, months, and days
    years, remainder = divmod(days, 365)

    # Adjust for leap years using calendar module
    leap_years = sum(calendar.isleap(year) for year in range(date1.year, date2.year + 1))
    days_without_leap_years = days - leap_years

    years = years + leap_years / 365  # Adjust for leap years

    months, days = divmod(days_without_leap_years, 30)

    # Format the description
    parts = []
    if int(years) > 0:
        parts.append(f"{int(years)} {'year' if int(years) == 1 else 'years'}")
    if int(months) > 0:
        parts.append(f"{int(months)} {'month' if int(months) == 1 else 'months'}")
    if int(days) > 0:
        parts.append(f"{int(days)} {'day' if int(days) == 1 else 'days'}")

    return ", ".join(parts) if parts else "0 days"


def to_datetime(date_in: str | datetime.datetime | datetime.date, fmt: str = ""):
    if isinstance(date_in, str):
        return datetime.datetime.strptime(date_in, fmt)
    elif isinstance(date_in, datetime.date):
        y, m, d = date_in.year, date_in.month, date_in.day
        return datetime.datetime(y, m, d)
    else:
        return date_in


def change_date_slider():
    global df_orders_in_dates
    print(f"{slider_date_input=}")
    df_orders_in_dates = clamp_orders_with_dates(*slider_date_input)


def click_n_years_from(time: datetime.datetime, n_years: int):
    key = "choice_date_input"
    sd, ed = slider_date_input
    t_is_now = time == now
    msg = ""
    if n_years == 0:
        msg += f"A"
        st.warning("0 years is not a valid input")
        return
    if n_years < 0:
        msg += f"B"
        if t_is_now:
            msg += f"C"
            # backwards from now
            ed = time
        d1 = ed + relativedelta.relativedelta(years=n_years)
        d2 = ed
    else:
        msg += f"D"
        if t_is_now:
            msg += f"E"
            # forwards from now
            sd = time
        d1 = sd
        d2 = sd + relativedelta.relativedelta(years=n_years)
    print(f"setting {msg=} {d1=:%Y-%m-%d},  {d2=:%Y-%m-%d}")
    st.session_state[k] = (d1, d2)


@st.cache_data
def clamp_orders_with_dates(d1: datetime.datetime | datetime.date, d2: datetime.datetime | datetime.date,
                            df: pd.DataFrame = None, date_key="Orders_DateQuote"):
    # d1, d2 = st.session_state[""]
    print(f"CLAMPING {df_orders=}")
    d_1 = d1 if (not isinstance(d1, datetime.datetime)) else d1.date()
    d_2 = d2 if (not isinstance(d2, datetime.datetime)) else d2.date()
    print(f"{d_1=}, {d_2=}")
    if df is not None:
        return df[(df[date_key] >= d_1) & (df[date_key] <= d_2)]
    else:
        return df_orders[(df_orders["Orders_DateQuote"] >= d_1) & (df_orders["Orders_DateQuote"] <= d_2)]


def get_dealer(dealer_name):
    df_sub = df_dealers[df_dealers["COMPANY NAME"] == dealer_name].reset_index()
    print(f"df_sub==\n\n{df_sub}")
    if not df_sub.empty:
        return df_sub.iloc[0]["ID"]
    return None


def update_dealer_selection():
    dealer_name = st.session_state["choice_select_dealer"]
    if dealer_name:

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

        print(f"UPDATING {dealer_name=}")
        id_dealer = get_dealer(dealer_name)
        print(f"{id_dealer=}")
        # print(f"{sql_sp_performance=}")
        # sql_qcp_dealer = sql_sp_performance.format(
        #     COMPANYID="NULL",
        #     DEALERID=-id_dealer,
        #     PRODUCTID="NULL",
        #     SALESPERSONID="NULL",
        #     ALLCOMPANIES=0
        # )
        # df_qcp_dealer = connect(sql_qcp_dealer)
        #
        # print(f"{sql_qcp_dealer}")
        # print(f"{df_qcp_dealer=}")
        #
        # for col in df_qcp_dealer.columns:
        #     if col.startswith("Pct"):
        #         df_qcp_dealer[col] = df_qcp_dealer[col].apply(lambda x: f"{x:3.3f} %")
        #
        # df_qcp_dealer = df_qcp_dealer[selectable_cols.keys()]

        df_orders_dealer = df_orders[df_orders["Dealers_ID"] == id_dealer]
        df_orders_dealer = clamp_orders_with_dates(*slider_date_input, df=df_orders_dealer)

        expander_dealer_quote_capture.dataframe(df_orders_dealer)

        # if df_orders_dealer.empty:
        #     expander_dealer_quote_capture.write(f"No Orders Found.")
        # else:
        #     df_orders_
        #
        #     expander_dealer_quote_capture.empty()
        #     # with expander_dealer_quote_capture:
        #     #     st.dataframe(df_qcp_dealer)
        #     expander_dealer_quote_capture.dataframe(df_qcp_dealer)
        #     # st.dataframe(df_qcp_dealer)


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

    for k, v in DATA_PAGES_KEYS.items():
        if k not in st.session_state:
            st.session_state[k] = v

    now = datetime.datetime.now()
    def_min_date, def_max_date = (now + datetime.timedelta(days=-365)), (now + datetime.timedelta(days=365))

    date_a, date_b = st.session_state.get("choice_date_input", (None, None))
    if date_a is not None and date_b is not None:
        pass
    if date_a is None and date_b is not None:
        st.session_state["choice_date_input"] = (date_b + datetime.timedelta(days=-365), date_b)
    if date_b is None and date_a is not None:
        st.session_state["choice_date_input"] = (date_a, date_a + datetime.timedelta(days=365))
    else:
        st.session_state["choice_date_input"] = (def_min_date, def_max_date)

    print(f"INIT {st.session_state['choice_date_input']=}")

    df_dealers = st.session_state.get("df_dealers", pd.DataFrame())
    df_orders = st.session_state.get("df_orders", pd.DataFrame())
    sql_sp_performance = st.session_state.get("sql_sp_performance", "")

    # Start drawing to the screen
    if df_orders is None:
        st.write(f"## Please re-run the Main page first.")
        switch_page("main")
    else:
        minimum_date = to_datetime(st.session_state.get("minimum_date", def_min_date))
        maximum_date = to_datetime(st.session_state.get("maximum_date", def_max_date))

        # one year from start date
        # one year from end date
        # one year from now

        # st containers
        expander_date_controls = st.expander("Date Controls")
        date_slide_col0, date_slide_col1 = st.columns([0.8, 0.2])
        container_dealer_selectbox = st.container()
        st.divider()
        expander_dealer_quote_capture = st.expander("Quote Capture Performance")
        if st.session_state.get("choice_select_dealer", "") == "":
            expander_dealer_quote_capture.write(f"Select a dealer first.")
        else:
            expander_dealer_quote_capture.write("")

        ny_col0, ny_col1, ny_col2, ny_col3 = expander_date_controls.columns(4)

        choice_n_years_input = ny_col0.number_input(
            "Years",
            min_value=-5,
            max_value=5,
            step=1,
            format="%d",
            help="Step N Years from a date.",
            key="choice_n_years_input"
        )

        slider_date_input = date_slide_col0.slider(
            "Select Date Range:",
            # value=(minimum_date, maximum_date),
            value=(def_min_date, def_max_date),
            format="YYYY-MM-DD",
            min_value=minimum_date,
            max_value=maximum_date
            ,
            # key="choice_date_input",
            on_change=change_date_slider
        )

        sd, ed = slider_date_input
        print(f"{sd=}, {ed=}")
        ny_col1.button(
            f"From Date 1: {sd:%Y-%m-%d}",
            on_click=lambda t1_=sd, n_=choice_n_years_input: click_n_years_from(t1_, n_),
            key="btn_n_years_from_start_date"
        )
        ny_col2.button(
            f"From Date 2: {ed:%Y-%m-%d}",
            on_click=lambda t1_=ed, n_=choice_n_years_input: click_n_years_from(t1_, n_),
            key="btn_n_years_from_end_date"
        )
        ny_col3.button(
            f"From Now:    {now:%Y-%m-%d}",
            on_click=lambda t1_=now, n_=choice_n_years_input: click_n_years_from(t1_, n_),
            key="btn_n_years_from_now"
        )

        # diff_dates = (ed - sd).days
        diff_dates = time_between(sd, ed)
        # date_slide_col1.metric("", diff_dates)
        date_slide_col1.markdown(f"### {diff_dates}")

        df_orders_in_dates = clamp_orders_with_dates(*slider_date_input)
        list_of_dealers = df_orders_in_dates["Dealers_COMPANYNAME"].dropna().unique()

        # with container_dealer_selectbox:
        #     select_dealer = st.selectbox(
        #         "Select a Dealer",
        #         options=list_of_dealers,
        #         key="choice_select_dealer",
        #         on_change=update_dealer_selection
        #     )
        #
        # with container_dealer_selectbox:
        # select_dealer = st.selectbox(
        #     "Select a Dealer",
        #     options=list_of_dealers,
        #     key="choice_select_dealer",
        #     on_change=update_dealer_selection
        # )
        select_dealer = container_dealer_selectbox.selectbox(
            "Select a Dealer",
            options=list_of_dealers,
            key="choice_select_dealer",
            on_change=update_dealer_selection
        )

        # print(f"{select_dealer=}, {st.session_state.get('choice_select_dealer', None)=}")
        if st.session_state.get("choice_select_dealer", None):
            update_dealer_selection()

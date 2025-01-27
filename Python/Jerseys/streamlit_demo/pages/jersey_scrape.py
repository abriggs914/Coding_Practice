# # import beautifulsoup as bs
# import itertools
#
# import requests
# import streamlit as st
#
#
# @st.cache_data(ttl=None, show_spinner=True)
# def query_site(url: str):
#     try:
#         return requests.get(url).json()
#     except requests.RequestException as e:
#         st.error(e)
#
#
# if __name__ == '__main__':
#     lids_base_url: str = "https://www.lids.ca/en/nhl-jerseys/o-1340+d-28447172+z-95683-9231070"
#     lids_url_filter: str = "?pageSize=96&pageNumber=2&sortOption=LowestPrice"
#
#     st.write(query_site(lids_base_url))
import os.path

import pandas as pd
import pdfplumber

from utility import money_value, next_available_file_name

pdf_path = r"C:\Users\abrig\Documents\BWS\BWS\PDF Invoice Parsing\2025\SUPERIOR PROPANE_BWS MANUFACTURING LTD - Report Dec 12023 - Nov 302024.pdf"
output_path = os.path.dirname(pdf_path)
output_file = "processed_output.xlsx"

table_header = """Event Date
Posting
Code Description Reference# TLS Units Ppu Amount Open Amount"""
table_columns = ["Event Date", "Posting Code", "Description", "Reference#", "TLS", "Units", "Ppu", "Amount", "Open Amount"]


def is_header_row(row):
    line_comp = "".join(row).replace(" ", "").strip().lower()
    th_comp = table_header.replace("\n", "").replace(" ", "").strip().lower()

    # check the first 10 characters
    is_header: bool = line_comp[:9] == th_comp[:9]

    # check the first 10 characters
    is_header = is_header and (line_comp[-6:] == th_comp[-6:])

    print(f"line_comp={line_comp[:9].rjust(25)}, th_comp={th_comp[:9].ljust(25)}")
    print(f"line_comp={line_comp[:-6].rjust(25)}, th_comp={th_comp[:-6].ljust(25)}")
    print(f"{is_header=}")

    return is_header


if __name__ == '__main__':
    all_data = []
    with pdfplumber.open(pdf_path) as f:
        for i, page in enumerate(f.pages):
            # # print(f"{page.find_tables()}")
            # ft = page.find_tables(table_settings={
            #     "explicit_horizontal_lines": "Description Reference# TLS Units Ppu Amount Open Amount"
            # })
            # print(f"{ft}")
            ft = page.extract_table(table_settings={"vertical_strategy": "text",
                                               "horizontal_strategy": "text",
                                               "snap_tolerance": 3})

            found_header: bool = False
            page_data = []
            for j, row in enumerate(ft):
                if not found_header:
                    found_header = is_header_row(row)
                else:
                    if "".join(row):
                        page_data.append(row)
            all_data.append(page_data)

            print(f"\nft: #{i}")
            print(ft)

    print("\nAll Data")
    to_append = []
    for i, page_data in enumerate(all_data):
        for j, row_data in enumerate(page_data):
            print(f"{i=}, {j=}, {row_data=}")

            ld = len(row_data)

            event_date = row_data[0]
            posting_code = row_data[1]

            description = "".join(row_data[2: ld - 7])
            reference = row_data[ld - 6]

            tls = row_data[-5]
            units = row_data[-4]
            ppu = row_data[-3]
            amount = row_data[-2]
            open_amount = row_data[-1]

            to_append.append(pd.DataFrame(
                columns=table_columns,
                data=[[
                    event_date,
                    posting_code,
                    description,
                    reference,
                    tls,
                    units,
                    ppu,
                    amount,
                    open_amount
                ]]
            ))

    df = pd.concat(to_append).reset_index(drop=True)
    df["Amount"] = df["Amount"].fillna("0").replace("", "0")
    df["Amount_M"] = df["Amount"].apply(lambda v: money_value(str(v)))
    df["Amount_M"] = df["Amount_M"].fillna(0)
    print(df)
    debits = df.loc[df["Amount"].str.startswith("-")]["Amount_M"].sum()
    credits = df.loc[~df["Amount"].str.startswith("-")]["Amount_M"].sum()
    net = debits + credits
    print(f"{debits=}")
    print(f"{credits=}")
    print(f"{net=}")

    file_name = os.path.join(output_path, output_file)
    file_name = next_available_file_name(file_name)
    df.to_excel(file_name)

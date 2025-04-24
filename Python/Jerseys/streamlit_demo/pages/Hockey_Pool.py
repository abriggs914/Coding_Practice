from typing import Any

import pandas as pd
import pdfplumber
import streamlit as st

from streamlit_pdf_viewer import pdf_viewer

from colour_utility import gradient_list
from streamlit_utility import aligned_text

file_pick_counts = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\2025\pick_counts.pdf"
file_pick_sheet = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\2025\boxpool-BWSPlayoffs2025.pdf"
excel_pick_counts = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\2025\pick_counts.xlsx"

@st.cache_data(show_spinner=True)
def load_pick_counts():
    # import pickle
    # # pdf_data  = {}
    # # with pdfplumber.open(file_pick_counts) as pdf:
    # #     for index, page in enumerate(pdf.pages):
    # #         pdf_data[index] = page.extract_table(
    # #             table_settings = {"vertical_strategy": "text",
    # #                           "horizontal_strategy": "text",
    # #                           "snap_tolerance": 3})
    # #
    # #         # for table in page.find_tables():
    # #         #     extracted = table.extract()
    # #         #     if extracted:  # Ensure non-empty
    # #         #         page_tables.append(extracted)
    # #         # if page_tables:
    # #         #     pdf_data[index] = page_tables
    # # return pdf_data
    # extracted = {}
    # with pdfplumber.open(file_pick_counts) as pdf:
    #     for i, page in enumerate(pdf.pages):
    #         # cropped = page.crop((150, 0, 450, float('inf')))
    #         tables = cropped.extract_tables()
    #         if tables:
    #             extracted[i] = tables
    # return extracted
    all_tables = []

    with pdfplumber.open(file_pick_sheet) as pdf:
        for page in pdf.pages:
            # Crop the central area of the page where your tables live
            width = page.width
            height = page.height

            # # Focus on central vertical band
            # cropped = page.within_bbox((width * 0.1, 0, width * 0.9, height))

            # Try lattice mode (looks like proper lines are used)
            tables = page.extract_tables({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_tolerance": 3,
                "join_tolerance": 3,
                # "edge_min_length": 10,
                "min_words_vertical": 1,
                "min_words_horizontal": 1
                # ,
                # "keep_blank_chars": False,
                # "intersection_tolerance": 3
            })

            for table in tables:
                # Filter empty tables (all rows empty)
                if any(any(cell.strip() for cell in row if cell) for row in table):
                    all_tables.extend(table)

    header_data = all_tables[0][0].split("\n")
    boxes_data = []
    boxes_row_data = all_tables[1:4] + all_tables[5:8]
    for i, row_data in enumerate(boxes_row_data):
        for j, box_data in enumerate(row_data):
            boxes_data.append(box_data.split("\n"))
    # return all_tables

    return {
        "header_data": header_data,
        "boxes_data": boxes_data
    }


@st.cache_data(show_spinner=True)
def load_excel_pick_counts() -> dict[Any, pd.DataFrame]:
    return pd.read_excel(
        excel_pick_counts,
        sheet_name=None
    )


def translate_player_text(p: str):
    """
    'Tomas Hertl (C) VGK'  => 'Hertl, T (VGK)'
    'Los Angeles Kings (T) LAK' => 'Los Angeles (LAK)'
    :param p:
    :return:
    """
    spl = p.strip().split(" ")
    team = f"({spl[-1]})"
    box_type = spl[-2]
    name_full = " ".join(spl[:-2])
    name_0 = spl[0]
    name_1 = spl[1]
    name_2 = spl[2]

    if box_type.removeprefix("(").removesuffix(")").lower() == "t":
        if name_1.lower() not in ["angeles", "louis"]:
            return f"{name_0} {team}"
        else:
            return f"{name_0} {name_1} {team}"
    else:
        if name_2.lower().startswith("("):
            return f"{name_1}, {name_0[0]} {team}"
        else:
            return f"{name_1} {name_2}, {name_0[0]} {team}"


@st.cache_data(show_spinner=True)
def load_annotations(df_picks: pd.DataFrame) -> list:
    annotations = []
    with pdfplumber.open(file_pick_sheet) as pdf:
        p0 = pdf.pages[0]
        for i, row in df_picks.iterrows():
            p_txt = row["boxText"]
            p0_search = p0.search(p_txt, regex=False, return_chars=False)
            st.write(f"{i=}, {p_txt=}, {p0_search=}")
            if p0_search:
                p0_search_data = p0_search[0]
                x0 = p0_search_data["x0"]
                x1 = p0_search_data["x1"]
                top = p0_search_data["top"]
                bottom = p0_search_data["bottom"]
                # bbox = [x0, top, x1, bottom]
                # # annotations.append({
                # #     "text": p_txt,
                # #     "i": i,
                # #     "bbox": bbox
                # # })
                # X and Y points are calculated from the bottom left of the page????
                # x_r = p0_search_data.get("x0")
                # y_r = p0_search_data.get("y1")
                # w_r = p0_search_data.get("width")
                # h_r = p0_search_data.get("height")
                # x_r_c, y_r_c = p0.point2coord((x_r, y_r))
                # x_r_c, y_r_c = p0.point2coord((x0, top))
                annotations.append({
                    "page": 0,
                    "x": x0,
                    "y": top,
                    "height": bottom - top,
                    "width": x1 - x0,
                    # "x": x_r_c,
                    # "y": y_r_c,
                    # "height": h_r,
                    # "width": w_r,
                    "color": "#AA1111",
                    "text": p_txt
                })
    return annotations


data_pick_counts = load_pick_counts()
st.write(data_pick_counts)

dfs_pick_counts: dict = load_excel_pick_counts()
df_pick_counts_20250422: pd.DataFrame = dfs_pick_counts["20250422"]

max_picks = int(df_pick_counts_20250422["Count"].max())
colour_grads = gradient_list(max_picks, "#FFCCCC", "#CCFFCC", as_hex=True)

df_pick_counts_20250422["colour"] = df_pick_counts_20250422["Count"].apply(lambda c: colour_grads[c - 1])
df_pick_counts_20250422["boxText"] = df_pick_counts_20250422["Player"].apply(lambda p: translate_player_text(p))

st.write("df_pick_counts_20250422")
st.write(df_pick_counts_20250422)

for i, cg in enumerate(colour_grads):
    st.markdown(aligned_text(
        f"Sample Text {i}",
        colour=cg
    ), unsafe_allow_html=True)


annotations_20250422 = load_annotations(df_pick_counts_20250422)
st.write("annotations_20250422")
st.write(annotations_20250422)

pdf_viewer_pick_sheet = pdf_viewer(
    file_pick_sheet,
    width=1800,
    height=3000,
    annotations=annotations_20250422,
    annotation_outline_size=2
)

office_pools_standings = """
<iframe marginheight="0" marginwidth="0"style="border: none;" frameborder="0"src="https://www.officepools.com/nhl/classic/widget/LK33HLQ"width="500"height="500"></iframe>
"""
st.markdown(office_pools_standings, unsafe_allow_html=True)

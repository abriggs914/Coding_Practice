import pdfplumber
import streamlit as st


file_pick_counts = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\2025\pick_counts.pdf"

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

    with pdfplumber.open(file_pick_counts) as pdf:
        for page in pdf.pages:
            # Crop the central area of the page where your tables live
            width = page.width
            height = page.height

            # Focus on central vertical band
            cropped = page.within_bbox((width * 0.1, 0, width * 0.9, height))

            # Try lattice mode (looks like proper lines are used)
            tables = cropped.extract_tables({
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
                    all_tables.append(table)

    return all_tables



data_pick_counts = load_pick_counts()
st.write(data_pick_counts)
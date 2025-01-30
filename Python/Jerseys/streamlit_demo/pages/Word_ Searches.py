import os

import pandas as pd
import numpy as np
import streamlit as st

import cv2
import pdfplumber
import pytesseract
from pytesseract import Output

from streamlit_pdf_viewer import pdf_viewer

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

word_searches_root = r"C:\Users\abrig\Documents\Coding_Practice\Resources\Word Searches\Hidden LineUps 24-25"
if not os.path.exists(word_searches_root):
    word_searches_root = word_searches_root.replace(r"Users\abrig", r"Users\abriggs")
if not os.path.exists(word_searches_root):
    st.error(f"Could not find Word Searches root '{word_searches_root}'.")
    st.stop()


st.set_page_config(layout="wide", page_title="Sports Word Searches")


@st.cache_data(ttl=None, show_spinner=True)
def load_pdf_bin(pdf_file_path: str):
    with open(pdf_file_path, "rb") as f:
        return f.read()


# def rotate_pdfs


@st.cache_data(ttl=None, show_spinner=True)
def process_pdf(team_name: str, pdf_file_path: str) -> dict:
    data = {"texts": {}, "images": {}}
    with pdfplumber.open(pdf_file_path) as f:
        # for page_num, page in enumerate(f.pages, start=1):
        #     data.append(page.extract_text_lines())
        # for page_num, page in enumerate(f.objects, start=1):
        #     data.append(page)
        # for page_num, image in enumerate(f.images, start=1):
        #     data.append(str(image)[:1000])
        page = f.pages[0]
        image = page.to_image().original.rotate(-90, expand=True)
        w = image.width
        h = image.width
        bbox = image.getbbox()
        image_clues = image.crop((
            bbox[0],
            bbox[1],
            bbox[0] + (w / 2),
            bbox[3],
        ))
        image_puzzle = image.crop((
            bbox[0] + (w / 2),
            bbox[1],
            bbox[2],
            bbox[3],
        ))
        # st.write(pytesseract.image_to_boxes(image))
        # st.write(pytesseract.image_to_osd(image))
        # st.image(image, caption=team_name)
        # st.image(image_clues, caption=f"{team_name} Clues")
        # st.image(image_puzzle, caption=f"{team_name} Puzzle")
        # data.append(pytesseract.image_to_string(image))
        data["texts"].update({
            "clues": pytesseract.image_to_data(image_clues, output_type=Output.DATAFRAME),
            "puzzle": pytesseract.image_to_data(image_puzzle, output_type=Output.DATAFRAME)
        })
        data["images"].update({
            "clues": image_clues,
            "puzzle": image_puzzle
        })
        # data.append(pytesseract.image_to_data(image, output_type=Output.DICT))

        # Convert to OpenCV format
        img = np.array(image_puzzle)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # Convert to grayscale

        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_contour = None
        max_area = 0
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:  # Only consider quadrilateral shapes
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    max_contour = approx

        if max_contour is not None:
            x, y, w, h = cv2.boundingRect(max_contour)
            st.write([x, y, w, h])
            bbox = image_puzzle.getbbox()
            image_puzzle_zoom = image_puzzle.crop([
                x, y, x + w, y + h
            ])
            image_text = image_puzzle.crop([
                bbox[0],
                bbox[1] + h + y,
                bbox[2],
                bbox[3],
            ])
            # st.image(image_puzzle_zoom, caption=f"{team_name} Puzzle")
            # st.image(image_text, caption=f"{team_name} Puzzle Text")
            data["texts"].update({
                "puzzle_text": pytesseract.image_to_data(image_text, output_type=Output.DATAFRAME),
                "puzzle": pytesseract.image_to_data(image_puzzle_zoom, output_type=Output.DATAFRAME)
            })
            data["images"].update({
                "puzzle_text": image_text,
                "puzzle": image_puzzle_zoom
            })
            if data["texts"]["puzzle_text"].loc[~pd.isna(data["texts"]["puzzle_text"]["text"])].empty:
                data["texts"].pop("puzzle_text")
                data["images"].pop("puzzle_text")
        # else:
            # st.write("NO BOXES FOUND")
            # st.image(image_puzzle, caption=f"{team_name} Puzzle")

    return data


@st.cache_data(ttl=None, show_spinner=True)
def load_word_searches() -> pd.DataFrame:
    dfs = []
    for i, file_name in enumerate(os.listdir(word_searches_root)):
        l_file_name = file_name.lower()
        if l_file_name.endswith(".pdf"):
            league_spl = l_file_name.split("_", 1)
            league_name = league_spl[0]
            team_name = league_spl[1].removesuffix(".pdf")
            dfs.append(pd.DataFrame(
                data=[{
                    "league": league_name,
                    "team": team_name,
                    "file_name": file_name,
                    "file_abs": os.path.join(word_searches_root, file_name)
                }]
            ))
    df = pd.concat(dfs).reset_index(drop=True)
    return df


df_word_searches = load_word_searches()

st.session_state.setdefault("radio_league_choice", "nhl")
radio_league_choice = st.radio(
    label="Choose a league",
    key="k_radio_league_choice",
    options=df_word_searches["league"].unique().tolist(),
    on_change=lambda: st.session_state.pop("k_selectbox_team_choice")
)

if radio_league_choice:
    selectbox_team_choice = st.selectbox(
        label="Choose a Word Search",
        key="k_selectbox_team_choice",
        options=df_word_searches.loc[df_word_searches["league"] == radio_league_choice]["team"].unique().tolist()
    )

    if selectbox_team_choice:
        title_selected_team = selectbox_team_choice.replace("_", " ").title()
        ser_team = df_word_searches.loc[
            (df_word_searches["league"] == radio_league_choice)
            & (df_word_searches["team"] == selectbox_team_choice)
        ].iloc[0]
        pdf_file_path = ser_team["file_abs"]
        st.write(pdf_file_path)
        st.write(f"{radio_league_choice=}")
        st.write(f"{selectbox_team_choice=}")
        # pdf_bin = load_pdf_bin(pdf_file_path)
        # pdf_viewer_word_search = pdf_viewer(
        #     pdf_file_path
        #     # ,
        #     # key="k_pdf_viewer_word_search"
        # )

        text_lines = process_pdf(title_selected_team, pdf_file_path)
        for k, df in text_lines["texts"].items():
            st.write(k)
            st.write(df)
            st.image(text_lines["images"][k], caption=f"{title_selected_team} {k.title()}")

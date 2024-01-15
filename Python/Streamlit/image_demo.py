import tkinter

import requests
from PIL import Image
from tkinter import PhotoImage
import streamlit as st
from io import BytesIO

import tkinter as tk

url = "https://assets.nhle.com/logos/nhl/svg/NYR_light.svg"


def prep_svg(svg_url, alt):
    # <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
    return f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
            <img src="{svg_url}" alt="{alt}" width="500" height="600">
        </svg>
    """


if __name__ == '__main__':
    # st.markdown(prep_svg(url, "NYR"), unsafe_allow_html=True)
    # # response = requests.get(url)
    # # image = Image.open(BytesIO(response.content))
    # # image = Image.open(BytesIO(response.content))
    # #
    # # try:
    # #
    # #     st.image(image, "NYR")
    # #
    # # except:
    # #
    image =
    app = tkinter.Tk()
    app.geometry(f"900x600")
    canvas = tk.Canvas(app, width=900, height=600, background="#878787")
    canvas.create_image(PhotoImage(image))

    st.session_state["image"] = Image.open()

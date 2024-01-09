from typing import Literal
import streamlit as st
import datetime


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    Streamlit utility functions
    Version..............1.01
    Date...........2024-01-09
    Author(s)....Avery Briggs
    """


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(),
                                      "%Y-%m-%dictionary")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if
            w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def aligned_text(txt: str, tag_style: Literal["h1", "h2", "h3", "h4", "h5", "h6", "p"] = "h1", h_align: Literal["left", "center", "right"] = "center", colour: str = "#FFFFFF", line_height: int = 1) -> str:
    """
    Return formatted HTML, and in-line CSS to h_align a given text in a container.
    Use with streamlit's markdown function and with 'unsafe_allow_html' set to True.
    """
    return f"<{tag_style} style='line-height: {line_height}; text-align: {h_align}; color: {colour};'>{txt}</{tag_style}>"


def hide_image_fullscreen_buttons():
    """
    Remove ALL fullscreen buttons for images created using streamlit's image function.
    https://discuss.streamlit.io/t/hide-fullscreen-option-when-displaying-images-using-st-image/19792
    """
    hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)

    hide_img_fs


def center_fullscreen_images():
    """
    Center an image when in fullscreen browsing mode
    https://discuss.streamlit.io/t/how-can-i-center-a-picture/30995/3
    """
    st.markdown(
        """
        <style>
            button[title^=Exit]+div [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )


if __name__ == '__main__':
    st.set_page_config(layout="wide")

    text = "Hello World"
    st.markdown(aligned_text(text, colour="#569072", tag_style="h6", line_height=50), unsafe_allow_html=True)

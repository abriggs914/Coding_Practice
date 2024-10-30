from typing import Literal
import streamlit as st
import datetime

from colour_utility import Colour

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """	
    Streamlit utility functions
    Version..............1.02
    Date...........2024-10-30
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


def aligned_text(
        txt: str,
        tag_style: Literal["h1", "h2", "h3", "h4", "h5", "h6", "p", "span"] = "h1",
        h_align: Literal["left", "center", "right"] = "center",
        colour: str = "#FFFFFF",
        line_height: int = 1
) -> str:
    """
    Return formatted HTML, and in-line CSS to h_align a given text in a container.
    Use with streamlit's markdown function and with 'unsafe_allow_html' set to True.
    See coloured_text() for streamlined-colour-only functionality.
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


def coloured_text(
        text: str,
        colour: str | Colour = "#000000",
        html_tags: str = "span",
        call: bool = False,
        style_only: bool = False
) -> str:
    """
    Return an HTML string of text styled with a colour.
    See aligned_text() for more functionality

    :param text: Text to be rendered.
    :param colour: Text foreground colour.
    :param html_tags: The HTML text tag you want to display the text with. Wide-open and not fully tested. stick to common text elements (headers, paragraphs, etc...)
    :param call: If True the result will immediately be displayed by calling st.markdown. Not recommended if you want to place your text within another element or container.
    :param style_only: If True return the formatted HTML style string.
    :return: Formatted HTML string.
    """
    style = f"style='color:{Colour(colour).hex_code};'"
    html = f"<{html_tags}{' ' + style}'>{text}</{html_tags}>"
    if call:
        st.markdown(html, unsafe_allow_html=True)
    if style_only:
        return style
    return html


if __name__ == '__main__':
    st.set_page_config(layout="wide")

    text = "Hello World"
    st.markdown(aligned_text(text, colour="#569072", tag_style="h6", line_height=50), unsafe_allow_html=True)

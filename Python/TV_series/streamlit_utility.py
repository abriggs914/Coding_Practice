from typing import Literal, Optional, Iterable, Any
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

import pandas as pd
import streamlit as st
import datetime

from colour_utility import Colour

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
	"""	
	Streamlit utility functions
	Version..............1.07
	Date...........2025-10-24
	Author(s)....Avery Briggs
	"""


def VERSION_DETAILS():
	return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
	return float(".".join(VERSION.lower().split("version")[-1].split("today")[0].split(".")[-2:]).strip())


def VERSION_DATE():
	return datetime.datetime.strptime(VERSION.lower().split("today")[-1].split("author")[0].split(".")[-1].strip(),
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
			button[title^=Exit]+div [path_data-testid=stImage]{
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


def rerun():
	# https://discuss.streamlit.io/t/is-it-possible-to-create-a-button-to-reset-relaod-the-whole-dashboard/6615/3
	import pyautogui
	pyautogui.hotkey("ctrl", "F5")


def screen_dimensions() -> tuple[Optional[int], Optional[int]]:
	"""
	Use JavaScript to retrieve the screen's Width and Height as integers.
	:return: (Width, Height) as an integer tuple. May return None.
	"""
	return (
		streamlit_js_eval(js_expressions='parent.innerWidth', key='SCR_W'),
		streamlit_js_eval(js_expressions='parent.innerHeight', key='SCR_H')
	)


def display_df(
		df: pd.DataFrame | pd.Series,
		title: Optional[str] = None,
		hide_index: str | bool = "if_int",
		show_shape: bool = True,

		# params for st.dataframe 20250325
		width: int | None = None,
		height: int | None = None,
		column_order: Iterable[str] | None = None,
		column_config: Any | None = None,
		key: Any | None = None,
		on_select: Literal["ignore", "rerun"] | Any = "ignore",
		selection_mode: Any = "multi-row"
):
	title = title if title else ""
	shape = df.shape
	if show_shape:
		title = f"{title} ({shape[0]} Rows".strip()
		title += f" x {shape[1]} Cols)" if len(shape) > 1 else ")"

	if title:
		st.write(title)

	if hide_index == "if_int":
		hide_index = str(df.index.dtype).lower() == "int64"

	if height is None:
		height = "auto"

	if width is None:
		width = "stretch"

	# st.write(f"{title=}, {hide_index=}")
	stdf = st.dataframe(
		data=df,
		hide_index=hide_index,
		width=width,
		height=height,
		column_order=column_order,
		column_config=column_config,
		key=key,
		on_select=on_select,
		selection_mode=selection_mode
	)
	return stdf


@st.cache_data(ttl=None, show_spinner=True)
def load_pdf_binary(pdf_file):
	with open(pdf_file, "rb") as f:
		return f.read()


def coloured_block(
		label: Optional[str] = None,
		bg: Optional[Colour | str] = None,
		width: int | str = 40,
		height: int | str = 20,
		border: bool = True,
		border_width: int | str = 1,
		border_colour: Optional[Colour | str] = None,
		contents: Optional[str] = None
) -> str:
	bg = Colour(bg if bg is not None else "#000000")
	border_colour = Colour(border_colour if border_colour is not None else "#FFFFFF")
	width = width if isinstance(width, int) else int(str(width).lower().removesuffix("px"))
	height = height if isinstance(height, int) else int(str(height).lower().removesuffix("px"))
	border_width = border_width if isinstance(border_width, int) else int(str(border_width).lower().removesuffix("px"))
	contents = contents if contents is not None else ""
	html = f"<div style='display: flex; align-items: center;'>"
	html += f"<div style='width: {width}px; height: {height}px; background-color: {bg.hex_code}; "
	if border:
		html += f"border: {border_width}px solid {border_colour.hex_code}; margin-right: 10px;'"
	html += f">{contents}</div>"
	if label:
		html += f"{label}"
	html += f"</div>"
	return html


def show_timer(seconds: Literal["indefinite"] | int = 60, count_down:bool = True, label:str = None, finish_label:str = None):
	if label is None:
		label = "Time Left" if count_down else "Time Elapsed"
	if finish_label is None:
		finish_label = "⏰ Time's up!"

	op = "-" if count_down else "+"
	if seconds == "indefinite":
		seconds = 60*60*24*365  # 1 year is good enough
	seconds_i = f"{seconds}" if count_down else "0"

	html_code = f"""
	<div id="timer" style="font-size: 24px; font-weight: bold; color: #f00;">
	  {label}: {seconds_i} seconds
	</div>
	<script>
	let seconds = {seconds_i};
	let timer = document.getElementById("timer");
	let countdown = setInterval(() => {{
		seconds {op}= 1;
		if (seconds >= 0) {{
			if (seconds <= {seconds}) {{
				timer.innerHTML = "{label}: " + seconds + " seconds";
			}} else {{
				clearInterval(countdown);
				timer.innerHTML = "{finish_label}";
			}}
		}} else {{
			clearInterval(countdown);
			timer.innerHTML = "{finish_label}";
		}}
	}}, 1000);
	</script>
	"""
	components.html(html_code, height=50)



if __name__ == '__main__':
	st.set_page_config(layout="wide")

	text = "Hello World"
	st.markdown(aligned_text(text, colour="#569072", tag_style="h6", line_height=50), unsafe_allow_html=True)
